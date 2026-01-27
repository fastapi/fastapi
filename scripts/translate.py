import json
import secrets
import subprocess
from collections.abc import Iterable
from functools import lru_cache
from os import sep as pathsep
from pathlib import Path
from typing import Annotated

import git
import typer
import yaml
from github import Github
from pydantic_ai import Agent
from rich import print

non_translated_sections = (
    f"reference{pathsep}",
    "release-notes.md",
    "fastapi-people.md",
    "external-links.md",
    "newsletter.md",
    "management-tasks.md",
    "management.md",
    "contributing.md",
)

general_prompt_path = Path(__file__).absolute().parent / "general-llm-prompt.md"
general_prompt = general_prompt_path.read_text(encoding="utf-8")

app = typer.Typer()


@lru_cache
def get_langs() -> dict[str, str]:
    return yaml.safe_load(Path("docs/language_names.yml").read_text(encoding="utf-8"))


def generate_lang_path(*, lang: str, path: Path) -> Path:
    en_docs_path = Path("docs/en/docs")
    assert str(path).startswith(str(en_docs_path)), (
        f"Path must be inside {en_docs_path}"
    )
    lang_docs_path = Path(f"docs/{lang}/docs")
    out_path = Path(str(path).replace(str(en_docs_path), str(lang_docs_path)))
    return out_path


def generate_en_path(*, lang: str, path: Path) -> Path:
    en_docs_path = Path("docs/en/docs")
    assert not str(path).startswith(str(en_docs_path)), (
        f"Path must not be inside {en_docs_path}"
    )
    lang_docs_path = Path(f"docs/{lang}/docs")
    out_path = Path(str(path).replace(str(lang_docs_path), str(en_docs_path)))
    return out_path


@app.command()
def translate_page(
    *,
    language: Annotated[str, typer.Option(envvar="LANGUAGE")],
    en_path: Annotated[Path, typer.Option(envvar="EN_PATH")],
) -> None:
    assert language != "en", (
        "`en` is the source language, choose another language as translation target"
    )
    langs = get_langs()
    language_name = langs[language]
    lang_path = Path(f"docs/{language}")
    lang_path.mkdir(exist_ok=True)
    lang_prompt_path = lang_path / "llm-prompt.md"
    assert lang_prompt_path.exists(), f"Prompt file not found: {lang_prompt_path}"
    lang_prompt_content = lang_prompt_path.read_text(encoding="utf-8")

    en_docs_path = Path("docs/en/docs")
    assert str(en_path).startswith(str(en_docs_path)), (
        f"Path must be inside {en_docs_path}"
    )
    out_path = generate_lang_path(lang=language, path=en_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    original_content = en_path.read_text(encoding="utf-8")
    old_translation: str | None = None
    if out_path.exists():
        print(f"Found existing translation: {out_path}")
        old_translation = out_path.read_text(encoding="utf-8")
    print(f"Translating {en_path} to {language} ({language_name})")
    agent = Agent("openai:gpt-5.2")

    prompt_segments = [
        general_prompt,
        lang_prompt_content,
    ]
    if old_translation:
        prompt_segments.extend(
            [
                "There is an existing previous translation for the original English content, that may be outdated.",
                "Update the translation only where necessary:",
                "- If the original English content has added parts, also add these parts to the translation.",
                "- If the original English content has removed parts, also remove them from the translation, unless you were instructed earlier to not do that in specific cases.",
                "- If parts of the original English content have changed, also change those parts in the translation.",
                "- If the previous translation violates current instructions, update it.",
                "- Otherwise, preserve the original translation LINE-BY-LINE, AS-IS.",
                "Do not:",
                "- rephrase or rewrite correct lines just to improve the style.",
                "- add or remove line breaks, unless the original English content changed.",
                "- change formatting or whitespace unless absolutely required.",
                "Only change what must be changed. The goal is to minimize diffs for easier human review.",
                "UNLESS you were instructed earlier to behave different, there MUST NOT be whole sentences or partial sentences in the updated translation, which are not in the original English content, and there MUST NOT be whole sentences or partial sentences in the original English content, which are not in the updated translation. Remember: the updated translation shall be IN SYNC with the original English content.",
                "Previous translation:",
                f"%%%\n{old_translation}%%%",
            ]
        )
    prompt_segments.extend(
        [
            f"Translate to {language} ({language_name}).",
            "Original content:",
            f"%%%\n{original_content}%%%",
        ]
    )
    prompt = "\n\n".join(prompt_segments)
    print(f"Running agent for {out_path}")
    result = agent.run_sync(prompt)
    out_content = f"{result.output.strip()}\n"
    print(f"Saving translation to {out_path}")
    out_path.write_text(out_content, encoding="utf-8", newline="\n")


def iter_all_en_paths() -> Iterable[Path]:
    """
    Iterate on the markdown files to translate in order of priority.
    """
    first_dirs = [
        Path("docs/en/docs/learn"),
        Path("docs/en/docs/tutorial"),
        Path("docs/en/docs/advanced"),
        Path("docs/en/docs/about"),
        Path("docs/en/docs/how-to"),
    ]
    first_parent = Path("docs/en/docs")
    yield from first_parent.glob("*.md")
    for dir_path in first_dirs:
        yield from dir_path.rglob("*.md")
    first_dirs_str = tuple(str(d) for d in first_dirs)
    for path in Path("docs/en/docs").rglob("*.md"):
        if str(path).startswith(first_dirs_str):
            continue
        if path.parent == first_parent:
            continue
        yield path


def iter_en_paths_to_translate() -> Iterable[Path]:
    en_docs_root = Path("docs/en/docs/")
    for path in iter_all_en_paths():
        relpath = path.relative_to(en_docs_root)
        if not str(relpath).startswith(non_translated_sections):
            yield path


@app.command()
def translate_lang(language: Annotated[str, typer.Option(envvar="LANGUAGE")]) -> None:
    paths_to_process = list(iter_en_paths_to_translate())
    print("Original paths:")
    for p in paths_to_process:
        print(f"  - {p}")
    print(f"Total original paths: {len(paths_to_process)}")
    missing_paths: list[Path] = []
    skipped_paths: list[Path] = []
    for p in paths_to_process:
        lang_path = generate_lang_path(lang=language, path=p)
        if lang_path.exists():
            skipped_paths.append(p)
            continue
        missing_paths.append(p)
    print("Paths to skip:")
    for p in skipped_paths:
        print(f"  - {p}")
    print(f"Total paths to skip: {len(skipped_paths)}")
    print("Paths to process:")
    for p in missing_paths:
        print(f"  - {p}")
    print(f"Total paths to process: {len(missing_paths)}")
    for p in missing_paths:
        print(f"Translating: {p}")
        translate_page(language="es", en_path=p)
        print(f"Done translating: {p}")


def get_llm_translatable() -> list[str]:
    translatable_langs = []
    langs = get_langs()
    for lang in langs:
        if lang == "en":
            continue
        lang_prompt_path = Path(f"docs/{lang}/llm-prompt.md")
        if lang_prompt_path.exists():
            translatable_langs.append(lang)
    return translatable_langs


@app.command()
def list_llm_translatable() -> list[str]:
    translatable_langs = get_llm_translatable()
    print("LLM translatable languages:", translatable_langs)
    return translatable_langs


@app.command()
def llm_translatable_json(
    language: Annotated[str | None, typer.Option(envvar="LANGUAGE")] = None,
) -> None:
    translatable_langs = get_llm_translatable()
    if language:
        if language in translatable_langs:
            print(json.dumps([language]))
            return
        else:
            raise typer.Exit(code=1)
    print(json.dumps(translatable_langs))


@app.command()
def commands_json(
    command: Annotated[str | None, typer.Option(envvar="COMMAND")] = None,
) -> None:
    available_commands = [
        "translate-page",
        "translate-lang",
        "update-outdated",
        "add-missing",
        "update-and-add",
        "remove-removable",
    ]
    default_commands = [
        "remove-removable",
        "update-outdated",
        "add-missing",
    ]
    if command:
        if command in available_commands:
            print(json.dumps([command]))
            return
        else:
            raise typer.Exit(code=1)
    print(json.dumps(default_commands))


@app.command()
def list_removable(language: str) -> list[Path]:
    removable_paths: list[Path] = []
    lang_paths = Path(f"docs/{language}").rglob("*.md")
    for path in lang_paths:
        en_path = generate_en_path(lang=language, path=path)
        if not en_path.exists():
            removable_paths.append(path)
    print(removable_paths)
    return removable_paths


@app.command()
def list_all_removable() -> list[Path]:
    all_removable_paths: list[Path] = []
    langs = get_langs()
    for lang in langs:
        if lang == "en":
            continue
        removable_paths = list_removable(lang)
        all_removable_paths.extend(removable_paths)
    print(all_removable_paths)
    return all_removable_paths


@app.command()
def remove_removable(language: Annotated[str, typer.Option(envvar="LANGUAGE")]) -> None:
    removable_paths = list_removable(language)
    for path in removable_paths:
        path.unlink()
        print(f"Removed: {path}")
    print("Done removing all removable paths")


@app.command()
def remove_all_removable() -> None:
    all_removable = list_all_removable()
    for removable_path in all_removable:
        removable_path.unlink()
        print(f"Removed: {removable_path}")
    print("Done removing all removable paths")


@app.command()
def list_missing(language: str) -> list[Path]:
    missing_paths: list[Path] = []
    en_lang_paths = list(iter_en_paths_to_translate())
    for path in en_lang_paths:
        lang_path = generate_lang_path(lang=language, path=path)
        if not lang_path.exists():
            missing_paths.append(path)
    print(missing_paths)
    return missing_paths


@app.command()
def list_outdated(language: str) -> list[Path]:
    dir_path = Path(__file__).absolute().parent.parent
    repo = git.Repo(dir_path)

    outdated_paths: list[Path] = []
    en_lang_paths = list(iter_en_paths_to_translate())
    for path in en_lang_paths:
        lang_path = generate_lang_path(lang=language, path=path)
        if not lang_path.exists():
            continue
        en_commit_datetime = list(repo.iter_commits(paths=path, max_count=1))[
            0
        ].committed_datetime
        lang_commit_datetime = list(repo.iter_commits(paths=lang_path, max_count=1))[
            0
        ].committed_datetime
        if lang_commit_datetime < en_commit_datetime:
            outdated_paths.append(path)
    print(outdated_paths)
    return outdated_paths


@app.command()
def update_outdated(language: Annotated[str, typer.Option(envvar="LANGUAGE")]) -> None:
    outdated_paths = list_outdated(language)
    for path in outdated_paths:
        print(f"Updating lang: {language} path: {path}")
        translate_page(language=language, en_path=path)
        print(f"Done updating: {path}")
    print("Done updating all outdated paths")


@app.command()
def add_missing(language: Annotated[str, typer.Option(envvar="LANGUAGE")]) -> None:
    missing_paths = list_missing(language)
    for path in missing_paths:
        print(f"Adding lang: {language} path: {path}")
        translate_page(language=language, en_path=path)
        print(f"Done adding: {path}")
    print("Done adding all missing paths")


@app.command()
def update_and_add(language: Annotated[str, typer.Option(envvar="LANGUAGE")]) -> None:
    print(f"Updating outdated translations for {language}")
    update_outdated(language=language)
    print(f"Adding missing translations for {language}")
    add_missing(language=language)
    print(f"Done updating and adding for {language}")


@app.command()
def make_pr(
    *,
    language: Annotated[str | None, typer.Option(envvar="LANGUAGE")] = None,
    command: Annotated[str | None, typer.Option(envvar="COMMAND")] = None,
    github_token: Annotated[str, typer.Option(envvar="GITHUB_TOKEN")],
    github_repository: Annotated[str, typer.Option(envvar="GITHUB_REPOSITORY")],
    commit_in_place: Annotated[
        bool, typer.Option(envvar="COMMIT_IN_PLACE", show_default=True)
    ] = False,
) -> None:
    print("Setting up GitHub Actions git user")
    repo = git.Repo(Path(__file__).absolute().parent.parent)
    if not repo.is_dirty(untracked_files=True):
        print("Repository is clean, no changes to commit")
        return
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(
        ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
        check=True,
    )
    current_branch = repo.active_branch.name
    if current_branch == "master" and commit_in_place:
        print("Can't commit directly to master")
        raise typer.Exit(code=1)

    if not commit_in_place:
        branch_name = "translate"
        if language:
            branch_name += f"-{language}"
        if command:
            branch_name += f"-{command}"
        branch_name += f"-{secrets.token_hex(4)}"
        print(f"Creating a new branch {branch_name}")
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    else:
        print(f"Committing in place on branch {current_branch}")
    print("Adding updated files")
    git_path = Path("docs")
    subprocess.run(["git", "add", str(git_path)], check=True)
    print("Committing updated file")
    message = "🌐 Update translations"
    if language:
        message += f" for {language}"
    if command:
        message += f" ({command})"
    subprocess.run(["git", "commit", "-m", message], check=True)
    print("Pushing branch")
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    if not commit_in_place:
        print("Creating PR")
        g = Github(github_token)
        gh_repo = g.get_repo(github_repository)
        body = (
            message
            + "\n\nThis PR was created automatically using LLMs."
            + f"\n\nIt uses the prompt file https://github.com/fastapi/fastapi/blob/master/docs/{language}/llm-prompt.md."
            + "\n\nIn most cases, it's better to make PRs updating that file so that the LLM can do a better job generating the translations than suggesting changes in this PR."
        )
        pr = gh_repo.create_pull(
            title=message, body=body, base="master", head=branch_name
        )
        print(f"Created PR: {pr.number}")
    print("Finished")


if __name__ == "__main__":
    app()
