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
For technical terms in English that don't have a common translation term, use the original term in English.

For code snippets or fragments, surrounded by backticks (`), don't translate the content, keep the original in English. For example, `list`, `dict`, keep them as is.

The content is written in Markdown, write the translation in Markdown as well.


When there is a code block, surrounded by triple backticks, do not translate its content, except for comments in the language which the code block uses.

Examples:

Source (English) – The code block is a bash code example with one comment:

```bash
# Print greeting
echo "Hello, World!"
```

Result (German):

```bash
# Gruß ausgeben
echo "Hello, World!"
```

Source (English) – The code block is a console example containing HTML tags. No comments, nothing to change here:

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

Result (German):

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

Source (English) – The code block is a console example containing 5 comments:

```console
// Go to the home directory
$ cd
// Create a directory for all your code projects
$ mkdir code
// Enter into that code directory
$ cd code
// Create a directory for this project
$ mkdir awesome-project
// Enter into that project directory
$ cd awesome-project
```

Result (German):

```console
// Gehe zum Home-Verzeichnis
$ cd
// Erstelle ein Verzeichnis für alle Ihre Code-Projekte
$ mkdir code
// Gehe in dieses Code-Verzeichnis
$ cd code
// Erstelle ein Verzeichnis für dieses Projekt
$ mkdir awesome-project
// Gehe in dieses Projektverzeichnis
$ cd awesome-project
```

If there is an existing translation and its Mermaid diagram is in sync with the Mermaid diagram in the English source, except a few translated words, then use the Mermaid diagram of the existing translation. The human editor of the translation translated these words in the Mermaid diagram. Keep these translations, do not revert them back to the English source.

Example:

Source (English):

```mermaid
flowchart LR
    subgraph global[global env]
        harry-1[harry v1]
    end
    subgraph stone-project[philosophers-stone project]
        stone(philosophers-stone) -->|requires| harry-1
    end
```

Existing translation (German) – has three translations:

```mermaid
flowchart LR
    subgraph global[globale Umgebung]
        harry-1[harry v1]
    end
    subgraph stone-project[philosophers-stone-Projekt]
        stone(philosophers-stone) -->|benötigt| harry-1
    end
```

Result (German) – You change nothing:

```mermaid
flowchart LR
    subgraph global[globale Umgebung]
        harry-1[harry v1]
    end
    subgraph stone-project[philosophers-stone-Projekt]
        stone(philosophers-stone) -->|benötigt| harry-1
    end
```


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


Do not convert occurrences of four slashes in a row at the start of a line (`////`) to a level four Markdown heading (`####`). The four slashes are a special syntax, which, for example, declares some text to be part of a tab in the final rendered document.

Example:

Source (English):

//// tab | Linux, macOS, Windows Bash

Wrong Result (German):

#### tab | Linux, macOS, Windows Bash

Correct Result (German):

//// tab | Linux, macOS, Windows Bash


Every Markdown heading in the English text (all levels) ends with a part inside curly brackets. This part denotes the hash of this heading, which is used in links to this heading. In translations, translate the heading, but do not translate this hash part, so that links do not break.

Examples of how to translate a heading:

Source (English):

## Alternative API docs { #alternative-api-docs }

Result (Spanish):

## Documentación de la API alternativa { #alternative-api-docs }

Source (English):

### Example { #example }

Result (German):

### Beispiel { #example }


Use the following rules for links (apply both to Markdown-style links ([text](url)) and to HTML-style <a> tags):

1) For relative URLs only translate link text. Do not translate the URL or its parts

Example:

Source (English):

[One of the fastest Python frameworks available](#performance)

Result (German):

[Eines der schnellsten verfügbaren Python-Frameworks](#performance)

2) For absolute URLs which DO NOT start EXACTLY with "https://fastapi.tiangolo.com", only translate link text and leave the URL unchanged.

Example:

Source (English):

<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel docs</a>

Result (German):

<a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel-Dokumentation</a>

3) For absolute URLs which DO start EXACTLY with "https://fastapi.tiangolo.com", only translate link text and change the URL by adding language code (https://fastapi.tiangolo.com/{language_code}[rest part of the url]).

Example:

Source (English):

<a href="https://fastapi.tiangolo.com/tutorial/path-params/#documentation" class="external-link" target="_blank">Documentation</a>

Result (Spanish):

<a href="https://fastapi.tiangolo.com/es/tutorial/path-params/#documentation" class="external-link" target="_blank">Documentación</a>

3.1) Do not add language codes for URLs that point to static assets (e.g., images, CSS, JavaScript).

Example:

Source (English):

<a href="https://fastapi.tiangolo.com/img/something.jpg" class="external-link" target="_blank">Something</a>

Result (Spanish):

<a href="https://fastapi.tiangolo.com/img/something.jpg" class="external-link" target="_blank">Algo</a>

4) For internal links, only translate link text.

Example:

Source (English):

[Create Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}

Result (German):

[Pull Requests erzeugen](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}

5) Do not translate anchor fragments in links (the part after #), as they must remain the same to work correctly.

5.1) If an existing translation has a link with an anchor fragment different to the anchor fragment in the English source, then this is an error. Fix this by using the anchor fragment of the English source.

Example:

Source (English):

[Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}

Existing wrong translation (German) – notice the wrongly translated anchor fragment:

[Body – Mehrere Parameter: Einfache Werte im Body](body-multiple-params.md#einzelne-werte-im-body){.internal-link target=_blank}.

Result (German) – you fix the anchor fragment:

[Body – Mehrere Parameter: Einfache Werte im Body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.

5.2) Do not add anchor fragments at will, even if this makes sense. If the English source has no anchor, don't add one.

Example:

Source (English):

Create a [virtual environment](../virtual-environments.md){.internal-link target=_blank}

Wrong translation (German) – Anchor added to the URL.

Erstelle eine [virtuelle Umgebung](../virtual-environments.md#create-a-virtual-environment){.internal-link target=_blank}

Good translation (German) – URL stays like in the English source.

Erstelle eine [Virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank}


"""

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
    agent = Agent("openai:gpt-5")

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
