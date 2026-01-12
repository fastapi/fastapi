import os
from collections.abc import Iterable
from pathlib import Path
from typing import Annotated

import typer

from scripts.doc_parsing_utils import check_translation

non_translated_sections = (
    f"reference{os.sep}",
    "release-notes.md",
    "fastapi-people.md",
    "external-links.md",
    "newsletter.md",
    "management-tasks.md",
    "management.md",
    "contributing.md",
)


cli = typer.Typer()


@cli.callback()
def callback():
    pass


def iter_all_lang_paths(lang_path_root: Path) -> Iterable[Path]:
    """
    Iterate on the markdown files to translate in order of priority.
    """

    first_dirs = [
        lang_path_root / "learn",
        lang_path_root / "tutorial",
        lang_path_root / "advanced",
        lang_path_root / "about",
        lang_path_root / "how-to",
    ]
    first_parent = lang_path_root
    yield from first_parent.glob("*.md")
    for dir_path in first_dirs:
        yield from dir_path.rglob("*.md")
    first_dirs_str = tuple(str(d) for d in first_dirs)
    for path in lang_path_root.rglob("*.md"):
        if str(path).startswith(first_dirs_str):
            continue
        if path.parent == first_parent:
            continue
        yield path


def get_all_paths(lang: str):
    res: list[str] = []
    lang_docs_root = Path("docs") / lang / "docs"
    for path in iter_all_lang_paths(lang_docs_root):
        relpath = path.relative_to(lang_docs_root)
        if not str(relpath).startswith(non_translated_sections):
            res.append(str(relpath))
    return res


def process_one_page(path: Path) -> bool:
    """
    Fix one translated document by comparing it to the English version.

    Returns True if processed successfully, False otherwise.
    """

    try:
        lang_code = path.parts[1]
        if lang_code == "en":
            print(f"Skipping English document: {path}")
            return True

        en_doc_path = Path("docs") / "en" / Path(*path.parts[2:])

        doc_lines = path.read_text(encoding="utf-8").splitlines()
        en_doc_lines = en_doc_path.read_text(encoding="utf-8").splitlines()

        doc_lines = check_translation(
            doc_lines=doc_lines,
            en_doc_lines=en_doc_lines,
            lang_code=lang_code,
            auto_fix=True,
            path=str(path),
        )

        # Write back the fixed document
        doc_lines.append("")  # Ensure file ends with a newline
        path.write_text("\n".join(doc_lines), encoding="utf-8")

    except ValueError as e:
        print(f"Error processing {path}: {e}")
        return False
    return True


@cli.command()
def fix_all(ctx: typer.Context, language: str):
    docs = get_all_paths(language)

    all_good = True
    for page in docs:
        doc_path = Path("docs") / language / "docs" / page
        res = process_one_page(doc_path)
        all_good = all_good and res

    if not all_good:
        raise typer.Exit(code=1)


@cli.command()
def fix_pages(
    doc_paths: Annotated[
        list[Path],
        typer.Argument(help="List of paths to documents."),
    ],
):
    all_good = True
    for path in doc_paths:
        res = process_one_page(path)
        all_good = all_good and res

    if not all_good:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    cli()
