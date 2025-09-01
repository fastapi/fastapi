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

general_prompt = """
### About literal text in this prompt

1) In the following instructions (after I say: `The above rules are in effect now`) the two characters `«` and `»` will be used to surround text and characters which you shall interpret literally. The `«` and the `»` are not part of the literal text (they are the meta characters denoting it).

2) Furthermore, text surrounded by `«««` and `»»»` is a block of literal text which spans multiple lines. To get its content, dedent all lines of the block until the `«««` and `»»»` are at column zero, then remove the newline after the `«««` and the newline before the `»»»`. The `«««` and the `»»»` are not part of the literal text block (they are the meta characters denoting it).

3) The above two syntaxes – `«...»` and `«««...»»»` – are used to denote literal text. Other forms of quotation marks – especially backticks and triple backticks – do NOT denote literal text.

The above rules are relevant, because we will give code examples for Markdown. Markdown uses backticks to denote inline code and code blocks. So, if you see text surrounded by backticks, then do not interpret it as literal text and throw away the backticks, but interpret it as a Markdown code block or a Markdown code snippet, and keep the backticks.

The above rules are in effect now.


### Definitions of terms used in this prompt

Backtick
    The character «`»
    Unicode U+0060 (GRAVE ACCENT)

Single backtick
    A single backtick – «`»

triple backticks
    Three backticks in a row – «```»

Neutral double quote
    The character «"»
    Unicode U+0022 (QUOTATION MARK)

Neutral single quote
    The character «'»
    Unicode U+0027 (APOSTROPHE)

English double typographic quotes
    The characters «“» and «”»
    Unicode U+201C (LEFT DOUBLE QUOTATION MARK) and Unicode U+201D (RIGHT DOUBLE QUOTATION MARK)

English single typographic quotes
    The characters «‘» and «’»
    Unicode U+2018 (LEFT SINGLE QUOTATION MARK) and Unicode U+2019 (RIGHT SINGLE QUOTATION MARK)

Code snippet
    Also called "inline code". Text in a Markdown document which is surrounded by single backticks. A paragraph can have a more than one code snippets.

    Example:

        «`i am a code snippet`»

    Example:

        «`first code snippet` `second code snippet` `third code snippet`»

Code block
    Text in a Markdown document which is surrounded by triple backticks. Spreads multiple lines.

    Example:

        «««
        ```
        Hello
        World
        ```
        »»»

    Example:

        «««
        ```python
        print("hello World")
        ```
        »»»


### Your task

Translate an English text – the original content – to a target language.

The original content is written in Markdown, write the translation in Markdown as well.

The original content will be surrounded by triple percentage signs («%%%»). Do not include the triple percentage signs in the translation.


### Technical terms in English

For technical terms in English that don't have a common translation term, use the original term in English.


### Content of code snippets

Do not translate the content of code snippets, keep the original in English. For example, «`list`», «`dict`», keep them as is.


### Content of code blocks

Do not translate the content of code blocks, except for comments in the language which the code block uses.

Examples:

    Source (English) – The code block is a bash code example with one comment:

        «««
        ```bash
        # Print greeting
        echo "Hello, World!"
        ```
        »»»

    Result (German):

        «««
        ```bash
        # Gruß ausgeben
        echo "Hello, World!"
        ```
        »»»

    Source (English) – The code block is a console example containing HTML tags. No comments, so nothing to change here:

        «««
        ```console
        $ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
        <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
                Searching for package file structure
        ```
        »»»

    Result (German):

        «««
        ```console
        $ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
        <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
                Searching for package file structure
        ```
        »»»

    Source (English) – The code block is a console example containing 5 comments:

        «««
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
        »»»

    Result (German):

        «««
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
        »»»

If there is an existing translation and its Mermaid diagram is in sync with the Mermaid diagram in the English source, except a few translated words, then use the Mermaid diagram of the existing translation. The human editor of the translation translated these words in the Mermaid diagram. Keep these translations, do not revert them back to the English source.

Example:

    Source (English):

        «««
        ```mermaid
        flowchart LR
            subgraph global[global env]
                harry-1[harry v1]
            end
            subgraph stone-project[philosophers-stone project]
                stone(philosophers-stone) -->|requires| harry-1
            end
        ```
        »»»

    Existing translation (German) – has three translations:

        «««
        ```mermaid
        flowchart LR
            subgraph global[globale Umgebung]
                harry-1[harry v1]
            end
            subgraph stone-project[philosophers-stone-Projekt]
                stone(philosophers-stone) -->|benötigt| harry-1
            end
        ```
        »»»

    Result (German) – you change nothing:

        «««
        ```mermaid
        flowchart LR
            subgraph global[globale Umgebung]
                harry-1[harry v1]
            end
            subgraph stone-project[philosophers-stone-Projekt]
                stone(philosophers-stone) -->|benötigt| harry-1
            end
        ```
        »»»


### Special blocks

There are special blocks of notes, tips and others that look like:

    «««
    /// note
    »»»

To translate it, keep the same line and add the translation after a vertical bar.

For example, if you were translating to Spanish, you would write:

    «««
    /// note | Nota
    »»»

Some examples in Spanish:

    Source:

        «««
        /// tip
        »»»

    Result:

        «««
        /// tip | Consejo
        »»»

    Source:

        «««
        /// details | Preview
        »»»

    Result:

        «««
        /// details | Vista previa
        »»»


### Tab blocks

There are special blocks surrounded by four slashes («////»). They mark text, which will be rendered as part of a tab in the final document. The scheme is:

    «««
    //// tab | {tab title}
    {tab content, may span many lines}
    ////
    »»»

Keep everything before the vertical bar («|») as is, including the vertical bar. Translate the tab title. Translate the tab content, applying the rules you know. Keep the four block closing slashes as is.

Examples:

    Source (English):

        «««
        //// tab | Python 3.8+ non-Annotated
        Hello
        ////
        »»»

    Result (German):

        «««
        //// tab | Python 3.8+ nicht annotiert
        Hallo
        ////
        »»»

    Source (English) – Here there is nothing to translate in the tab title:

        «««
        //// tab | Linux, macOS, Windows Bash
        Hello again
        ////
        »»»

    Result (German):

        «««
        //// tab | Linux, macOS, Windows Bash
        Hallo wieder
        ////
        »»»


### Headings

Every Markdown heading in the English text (all levels) ends with a part inside curly brackets. This part denotes the hash of this heading, which is used in links to this heading. In translations, translate the heading, but do not translate this hash part, so that links do not break.

Examples of how to translate a heading:

    Source (English):

        «««
        ## Alternative API docs { #alternative-api-docs }
        »»»

    Result (Spanish):

        «««
        ## Documentación de la API alternativa { #alternative-api-docs }
        »»»

    Source (English):

        «««
        ### Example { #example }
        »»»

    Result (German):

        «««
        ### Beispiel { #example }
        »»»


### Links

Use the following rules for links (apply both to Markdown-style links («[text](url)») and to HTML-style «<a>» tags):

1) For relative URLs, only translate link text. Do not translate the URL or its parts

Example:

    Source (English):

        «««
        [One of the fastest Python frameworks available](#performance)
        »»»

    Result (German):

        «««
        [Eines der schnellsten verfügbaren Python-Frameworks](#performance)
        »»»

2) For absolute URLs which DO NOT start EXACTLY with «https://fastapi.tiangolo.com», only translate link text and leave the URL unchanged.

Example:

    Source (English):

        «««
        <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel docs</a>
        »»»

    Result (German):

        «««
        <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel-Dokumentation</a>
        »»»

3) For absolute URLs which DO start EXACTLY with «https://fastapi.tiangolo.com», only translate link text and change the URL by adding language code («https://fastapi.tiangolo.com/{language_code}[rest part of the url]»).

Example:

    Source (English):

        «««
        <a href="https://fastapi.tiangolo.com/tutorial/path-params/#documentation" class="external-link" target="_blank">Documentation</a>
        »»»

    Result (Spanish):

        «««
        <a href="https://fastapi.tiangolo.com/es/tutorial/path-params/#documentation" class="external-link" target="_blank">Documentación</a>
        »»»

3.1) Do not add language codes for URLs that point to static assets (e.g., images, CSS, JavaScript).

Example:

    Source (English):

        «««
        <a href="https://fastapi.tiangolo.com/img/something.jpg" class="external-link" target="_blank">Something</a>
        »»»

    Result (Spanish):

        «««
        <a href="https://fastapi.tiangolo.com/img/something.jpg" class="external-link" target="_blank">Algo</a>
        »»»

4) For internal links, only translate link text.

Example:

    Source (English):

        «««
        [Create Pull Requests](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}
        »»»

    Result (German):

        «««
        [Pull Requests erzeugen](help-fastapi.md#create-a-pull-request){.internal-link target=_blank}
        »»»

5) Do not translate anchor fragments in links (the part after «#»), as they must remain the same to work correctly.

5.1) If an existing translation has a link with an anchor fragment different to the anchor fragment in the English source, then this is an error. Fix this by using the anchor fragment of the English source.

Example:

    Source (English):

        «««
        [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}
        »»»

    Existing wrong translation (German) – notice the wrongly translated anchor fragment:

        «««
        [Body – Mehrere Parameter: Einfache Werte im Body](body-multiple-params.md#einzelne-werte-im-body){.internal-link target=_blank}.
        »»»

    Result (German) – you fix the anchor fragment:

        «««
        [Body – Mehrere Parameter: Einfache Werte im Body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
        »»»

5.2) Do not add anchor fragments at will, even if this makes sense. If the English source has no anchor, don't add one.

Example:

    Source (English):

        «««
        Create a [virtual environment](../virtual-environments.md){.internal-link target=_blank}
        »»»

    Wrong translation (German) – Anchor added to the URL.

        «««
        Erstelle eine [virtuelle Umgebung](../virtual-environments.md#create-a-virtual-environment){.internal-link target=_blank}
        »»»

    Good translation (German) – URL stays like in the English source.

        «««
        Erstelle eine [Virtuelle Umgebung](../virtual-environments.md){.internal-link target=_blank}
        »»»


### Abbr elements

Translate HTML abbr elements as follows:

1) If the title attribute gives the full phrase for an abbreviation, then keep the phrase, append a dash («–»), followed by the translation of the phrase.

Examples:

    Source (English):

        «««
        <abbr title="Internet of Things">IoT</abbr>
        <abbr title="Central Processing Unit">CPU</abbr>
        <abbr title="too long; didn't read"><strong>TL;DR:</strong></abbr>
        »»»

    Result (German):

        «««
        <abbr title="Internet of Things – Internet der Dinge">IoT</abbr>
        <abbr title="Central Processing Unit – Zentrale Verarbeitungseinheit">CPU</abbr>
        <abbr title="too long; didn't read – zu lang; hab's nicht gelesen"><strong>TL;DR:</strong></abbr>
        »»»

Conversion scheme title attribute:

    Source (English):

        {full phrase}

    Result (German):

        {full phrase} – {translation of full phrase}

1.1) If the translation of the phrase starts with the same letters, then just use the translation.

Examples:

    Source (English):

        «««
        <abbr title="JSON Web Tokens">JWT</abbr>
        <abbr title="Enumeration">`Enum`</abbr>
        <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>
        »»»

    Result (German):

        «««
        <abbr title="JSON Web Tokens">JWT</abbr>
        <abbr title="Enumeration">`Enum`</abbr>
        <abbr title="Asynchrones Server-Gateway-Interface">ASGI</abbr>
        »»»

Conversion scheme title attribute:

    Source (English):

        {full phrase}

    Result (German):

        {translation of full phrase}

2) If the title attribute explains something in its own words, then translate it, if possible.

Examples:

    Source (English):

        «««
        <abbr title="also known as: endpoints, routes">path</abbr>
        <abbr title="A program that checks for code errors">linter</abbr>
        <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>
        <abbr title="before 2023-03">0.95.0</abbr>
        <abbr title="2023-08-26">at the time of writing this</abbr>
        »»»

    Result (German):

        «««
        <abbr title="auch bekannt als: Endpunkte, Routen">Pfad</abbr>
        <abbr title="Programm das auf Fehler im Code prüft">Linter</abbr>
        <abbr title="Konvertieren des Strings eines HTTP-Requests in Python-Daten">„Parsen“</abbr>
        <abbr title="vor 2023-03">0.95.0</abbr>
        <abbr title="2023-08-26">zum Zeitpunkt als das hier geschrieben wurde</abbr>
        »»»

Conversion scheme title attribute:

    Source (English):

        {explanation}

    Result (German):

        {translation of explanation}

3) If the title attribute gives the full phrase for an abbreviation, followed by a colon («:») or a comma («,»), followed by an explanation, then keep the phrase, append a dash («–»), followed by the translation of the phrase, followed by a colon («:»), followed by the translation of the explanation.

Examples:

    Source (English):

        «««
        <abbr title="Input/Output: disk reading or writing, network communication.">I/O</abbr>
        <abbr title="Content Delivery Network: Service, that provides static files.">CDN</abbr>
        <abbr title="Integrated Development Environment, similar to a code editor">IDE</abbr>
        <abbr title="Object Relational Mapper, a fancy term for a library where some classes represent SQL tables and instances represent rows in those tables">"ORMs"</abbr>
        »»»

    Result (German):

        «««
        <abbr title="Input/Output – Eingabe/Ausgabe: Lesen oder Schreiben auf der Festplatte, Netzwerkkommunikation.">I/O</abbr>
        <abbr title="Content Delivery Network – Inhalte auslieferndes Netzwerk: Dienst, der statische Dateien bereitstellt.">CDN</abbr>
        <abbr title="Integrated Development Environment – Integrierte Entwicklungsumgebung: Ähnlich einem Code-Editor">IDE</abbr>
        <abbr title="Object Relational Mapper – Objektrelationaler Mapper: Ein Fachbegriff für eine Bibliothek, in der einige Klassen SQL-Tabellen und Instanzen Zeilen in diesen Tabellen darstellen">„ORMs“</abbr>
        »»»

Conversion scheme title attribute:

    Source (English):

        {full phrase}: {explanation}

    OR

    Source (English):

        {full phrase}, {explanation}

    Result (German):

        {full phrase} – {translation of full phrase}: {translation of explanation}

3.1) For the full phrase (the part before the dash in the translation) rule 1.1 also applies, speak, you can leave the original full phrase away and just use the translated full phrase, if it starts with the same letters. The result becomes:

Conversion scheme title attribute:

    Result (German):

        {translation of full phrase}: {translation of explanation}

4) If there is an HTML abbr element in a sentence in an existing translation, but that element does not exist in the related sentence in the English text, then keep that HTML abbr element in the translation, do not change or remove it. Except when you remove the whole sentence from the translation, because the whole sentence was removed from the English text. The reasoning for this rule is, that such abbr elements are manually added by the human editor of the translation, in order to translate or explain an English word to the human readers of the translation. They would not make sense in the English text, but they do make sense in the translation. So keep them in the translation, even though they are not part of the English text. This rule only applies to HTML abbr elements.


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
    language: Annotated[
        str,
        typer.Option(envvar="LANGUAGE", help="Target language, e.g. `es`, `fr`, `de`"),
    ],
    en_path: Annotated[
        Path,
        typer.Option(
            envvar="EN_PATH",
            help="Path to the English source, relative to the FastAPI root directory. If not given, `docs/en/docs/_llm-test.md` is used.",
        ),
    ] = Path("docs/en/docs/_llm-test.md"),
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
    en_docs_root = Path("docs/en/docs/")
    for path in iter_all_en_paths():
        relpath = path.relative_to(en_docs_root)
        if not str(relpath).startswith(non_translated_sections):
            yield path


@app.command()
def translate_lang(
    language: Annotated[
        str,
        typer.Option(envvar="LANGUAGE", help="Target language, e.g. `es`, `fr`, `de`"),
    ],
    mode: Annotated[
        str,
        typer.Option(
            help="Which files of the target language to translate, one of: `missing`, `existing`, `all`"
        ),
    ] = "missing",
    verbose: Annotated[bool, typer.Option(help="Print all paths")] = False,
    preview: Annotated[
        bool, typer.Option(help="Show what will be done, but do not translate")
    ] = False,
) -> None:
    allowed_modes = ["missing", "existing", "all"]
    assert mode in allowed_modes, (
        f"`mode` parameter must be one of {', '.join(f'`{mode}`' for mode in allowed_modes)}"
    )

    translatable_paths = list(iter_en_paths_to_translate())
    missing_paths: list[Path] = []
    existing_paths: list[Path] = []
    for p in translatable_paths:
        lang_path = generate_lang_path(lang=language, path=p)
        (existing_paths if lang_path.exists() else missing_paths).append(p)

    def print_pathinfo(title: str, paths: list[Path], verbose: bool = verbose):
        print(f"{len(paths)} {title}", end="")
        if verbose and paths:
            print(":")
            for p in paths:
                print(f"  - {p}")
        else:
            print()

    print_pathinfo("translatable paths", translatable_paths)
    print_pathinfo("paths with a translation", existing_paths)
    print_pathinfo("paths with no translation", missing_paths)

    print(f"Mode: translate {mode}")
    if mode == "missing" or (mode == "all" and len(existing_paths) == 0):
        tbd_paths = missing_paths
        action = "translate"
    elif mode == "existing" or (mode == "all" and len(missing_paths) == 0):
        tbd_paths = existing_paths
        action = "update"
    else:
        tbd_paths = translatable_paths
        action = "translate/update"
    print(f"{len(tbd_paths)} paths to {action}")

    if not preview:
        for c, p in enumerate(tbd_paths):
            print(f"({c + 1}/{len(tbd_paths)}) Translating: {p}")
            translate_page(language=language, en_path=p)
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
