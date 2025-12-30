from pathlib import Path
from typing import Annotated

import typer

from scripts.doc_parsing_utils import (
    extract_code_includes,
    extract_header_permalinks,
    extract_html_links,
    extract_markdown_links,
    replace_code_includes_with_placeholders,
    replace_header_permalinks,
    replace_html_links,
    replace_markdown_links,
    replace_placeholders_with_code_includes,
)

cli = typer.Typer()


@cli.callback()
def callback():
    pass


@cli.command()
def fix_pages(
    doc_paths: Annotated[
        list[Path],
        typer.Argument(help="List of paths to documents."),
    ],
):
    for path in doc_paths:
        lang_code = path.parts[1]
        if lang_code == "en":
            print(f"Skipping English document: {path}")
            continue

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
        doc_lines = fixed_doc_lines

        # Fix permalinks
        en_permalinks = extract_header_permalinks(en_doc_lines)
        fixed_doc_lines = replace_header_permalinks(doc_lines, en_permalinks)
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
        # TODO: Implement

        # Write back the fixed document
        doc_lines.append("")  # Ensure file ends with a newline
        path.write_text("\n".join(doc_lines), encoding="utf-8")


if __name__ == "__main__":
    cli()
