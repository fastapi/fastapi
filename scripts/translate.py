import secrets
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Iterable

import git
import typer
import yaml
from github import Github
from pydantic_ai import Agent
from rich import print

non_translated_sections = (
    "reference/",
    "release-notes.md",
    "fastapi-people.md",
    "external-links.md",
    "newsletter.md",
    "management-tasks.md",
    "management.md",
    "contributing.md",
)


general_prompt = """
For technical terms in English that don't have a common translation term use the original term in English.

If you have instructions to translate specific terms or phrases in a specific way, please follow those instructions instead of keeping the old and outdated content.

For code snippets or fragments, surrounded by backticks (`), don't translate the content, keep the original in English. For example, `list`, `dict`, keep them as is.

The content is written in markdown, write the translation in markdown as well. Don't add triple backticks (`) around the generated translation content.

When there's an example of code, the console or a terminal, normally surrounded by triple backticks and a keyword like "console" or "bash" (e.g. ```console), do not translate the content, keep the original in English.

The original content will be surrounded by triple percentage signs (%) and you should translate it to the target language. Do not include the triple percentage signs in the translation.

There are special blocks of notes, tips and others that look like:

/// note

To translate it, keep the same line and add the translation after a vertical bar.

For example, if you were translating to Spanish, you would write:

/// note | Nota

Some examples in Spanish:

Source:

/// tip

Result:

/// tip | Consejo

Source:

/// details | Preview

Result:

/// details | Vista previa
"""

app = typer.Typer()


@lru_cache
def get_langs() -> dict[str, str]:
    return yaml.safe_load(Path("docs/language_names.yml").read_text())


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
    langs = get_langs()
    language_name = langs[language]
    lang_path = Path(f"docs/{language}")
    lang_path.mkdir(exist_ok=True)
    lang_prompt_path = lang_path / "llm-prompt.md"
    assert lang_prompt_path.exists(), f"Prompt file not found: {lang_prompt_path}"
    lang_prompt_content = lang_prompt_path.read_text()

    en_docs_path = Path("docs/en/docs")
    assert str(en_path).startswith(str(en_docs_path)), (
        f"Path must be inside {en_docs_path}"
    )
    out_path = generate_lang_path(lang=language, path=en_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    original_content = en_path.read_text()
    old_translation: str | None = None
    if out_path.exists():
        print(f"Found existing translation: {out_path}")
        old_translation = out_path.read_text()
    print(f"Translating {en_path} to {language} ({language_name})")
    agent = Agent("openai:gpt-4o")

    prompt_segments = [
        general_prompt,
        lang_prompt_content,
    ]
    if old_translation:
        prompt_segments.extend(
            [
                "There's an existing previous translation for this content that is probably outdated with old content or old instructions.",
                "Update the translation only where necessary:",
                "- If the original English content has changed, reflect that in the translation.",
                "- If the previous translation violates current instructions, update it.",
                "- Otherwise, preserve the original translation **line-by-line** as-is.",
                "Do not:",
                "- Rephrase or rewrite correct lines just to improve the style.",
                "- Add or remove line breaks unless the English source changed.",
                "- Change formatting or whitespace unless absolutely required.",
                "Only change what must be changed. The goal is to minimize diffs for easier review.",
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
    out_content = f"{result.data.strip()}\n"
    print(f"Saving translation to {out_path}")
    out_path.write_text(out_content)


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
    for path in iter_all_en_paths():
        if str(path).replace("docs/en/docs/", "").startswith(non_translated_sections):
            continue
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
def remove_removable(language: str) -> None:
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
    github_token: Annotated[str, typer.Option(envvar="GITHUB_TOKEN")],
    github_repository: Annotated[str, typer.Option(envvar="GITHUB_REPOSITORY")],
) -> None:
    print("Setting up GitHub Actions git user")
    repo = git.Repo(Path(__file__).absolute().parent.parent)
    if not repo.is_dirty(untracked_files=True):
        print("Repository is clean, no changes to commit")
        return
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(
        ["git", "config", "user.email", "github-actions@github.com"], check=True
    )
    branch_name = "translate"
    if language:
        branch_name += f"-{language}"
    branch_name += f"-{secrets.token_hex(4)}"
    print(f"Creating a new branch {branch_name}")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    print("Adding updated files")
    git_path = Path("docs")
    subprocess.run(["git", "add", str(git_path)], check=True)
    print("Committing updated file")
    message = "🌐 Update translations"
    if language:
        message += f" for {language}"
    subprocess.run(["git", "commit", "-m", message], check=True)
    print("Pushing branch")
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    print("Creating PR")
    g = Github(github_token)
    gh_repo = g.get_repo(github_repository)
    pr = gh_repo.create_pull(
        title=message, body=message, base="master", head=branch_name
    )
    print(f"Created PR: {pr.number}")
    print("Finished")


if __name__ == "__main__":
    app()
