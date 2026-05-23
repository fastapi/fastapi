from pathlib import Path

import pytest
from typer.testing import CliRunner

from scripts.translation_fixer import cli

data_path = Path(
    "scripts/tests/test_translation_fixer/test_code_includes/data"
).absolute()


@pytest.mark.parametrize(
    "copy_test_files",
    [(f"{data_path}/en_doc.md", f"{data_path}/translated_doc_number_gt.md")],
    indirect=True,
)
def test_gt(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 1

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(f"{data_path}/translated_doc_number_gt.md").read_text(
        "utf-8"
    )

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert "Error processing docs/lang/docs/doc.md" in result.output
    assert (
        "Number of code include placeholders does not match the number of code includes "
        "in the original document (4 vs 3)"
    ) in result.output


@pytest.mark.parametrize(
    "copy_test_files",
    [(f"{data_path}/en_doc.md", f"{data_path}/translated_doc_number_lt.md")],
    indirect=True,
)
def test_lt(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 1

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(f"{data_path}/translated_doc_number_lt.md").read_text(
        "utf-8"
    )

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert "Error processing docs/lang/docs/doc.md" in result.output
    assert (
        "Number of code include placeholders does not match the number of code includes "
        "in the original document (2 vs 3)"
    ) in result.output
