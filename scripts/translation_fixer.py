import difflib
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Annotated

import typer

from scripts.doc_parsing_utils import (
    extract_code_includes,
    extract_header_permalinks,
    extract_html_links,
    extract_markdown_links,
    extract_multiline_code_blocks,
    replace_code_includes_with_placeholders,
    replace_header_permalinks,
    replace_html_links,
    replace_markdown_links,
    replace_multiline_code_blocks_in_text,
    replace_placeholders_with_code_includes,
)

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

        # Fix code includes
        en_code_includes = extract_code_includes(en_doc_lines)
        doc_lines_with_placeholders = replace_code_includes_with_placeholders(doc_lines)
        fixed_doc_lines = replace_placeholders_with_code_includes(
            doc_lines_with_placeholders, en_code_includes
        )
        if fixed_doc_lines != doc_lines:
            print(f"Fixing code includes in: {path}")
            diff = difflib.unified_diff(
                doc_lines, fixed_doc_lines, fromfile="translation", tofile="fixed"
            )
            print("\n".join(diff))

        doc_lines = fixed_doc_lines

        # Fix permalinks
        en_permalinks = extract_header_permalinks(en_doc_lines)
        doc_permalinks = extract_header_permalinks(doc_lines)

        fixed_doc_lines = replace_header_permalinks(
            doc_lines, doc_permalinks, en_permalinks
        )
        if fixed_doc_lines != doc_lines:
            print(f"Fixing header permalinks in: {path}")
        doc_lines = fixed_doc_lines

        # Fix markdown links
        en_markdown_links = extract_markdown_links(en_doc_lines)
        fixed_doc_lines = replace_markdown_links(
            doc_lines, en_markdown_links, lang_code
        )
        if fixed_doc_lines != doc_lines:
            print(f"Fixing markdown links in: {path}")
        doc_lines = fixed_doc_lines

        # Fix HTML links
        en_html_links = extract_html_links(en_doc_lines)
        fixed_doc_lines = replace_html_links(doc_lines, en_html_links, lang_code)
        if fixed_doc_lines != doc_lines:
            print(f"Fixing HTML links in: {path}")
        doc_lines = fixed_doc_lines

        # Fix multiline code blocks
        en_code_blocks = extract_multiline_code_blocks(en_doc_lines)
        doc_code_blocks = extract_multiline_code_blocks(doc_lines)
        fixed_doc_lines = replace_multiline_code_blocks_in_text(
            doc_lines, doc_code_blocks, en_code_blocks
        )
        if fixed_doc_lines != doc_lines:
            print(f"Fixing multiline code blocks in: {path}")
        doc_lines = fixed_doc_lines

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
