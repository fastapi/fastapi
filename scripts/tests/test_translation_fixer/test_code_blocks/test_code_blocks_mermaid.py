from pathlib import Path

import pytest
from typer.testing import CliRunner

from scripts.translation_fixer import cli

data_path = Path(
    "scripts/tests/test_translation_fixer/test_code_blocks/data"
).absolute()


@pytest.mark.parametrize(
    "copy_test_files",
    [(f"{data_path}/en_doc.md", f"{data_path}/translated_doc_mermaid_translated.md")],
    indirect=True,
)
def test_translated(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 0, result.output

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(
        f"{data_path}/translated_doc_mermaid_translated.md"
    ).read_text("utf-8")

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert (
        "Skipping mermaid code block replacement (lines 41-44). This should be checked manually."
    ) in result.output


@pytest.mark.parametrize(
    "copy_test_files",
    [
        (
            f"{data_path}/en_doc.md",
            f"{data_path}/translated_doc_mermaid_not_translated.md",
        )
    ],
    indirect=True,
)
def test_not_translated(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 0, result.output

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(
        f"{data_path}/translated_doc_mermaid_not_translated.md"
    ).read_text("utf-8")

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert ("Skipping mermaid code block replacement") not in result.output
