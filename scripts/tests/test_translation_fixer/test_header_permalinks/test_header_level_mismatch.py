from pathlib import Path

import pytest
from typer.testing import CliRunner

from scripts.translation_fixer import cli

data_path = Path(
    "scripts/tests/test_translation_fixer/test_header_permalinks/data"
).absolute()


@pytest.mark.parametrize(
    "copy_test_files",
    [(f"{data_path}/en_doc.md", f"{data_path}/translated_doc_level_mismatch_1.md")],
    indirect=True,
)
def test_level_mismatch_1(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 1

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(
        f"{data_path}/translated_doc_level_mismatch_1.md"
    ).read_text("utf-8")

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert "Error processing docs/lang/docs/doc.md" in result.output
    assert (
        "Header levels do not match between document and original document"
        " (found #, expected ##) for header №2 in line 5"
    ) in result.output


@pytest.mark.parametrize(
    "copy_test_files",
    [(f"{data_path}/en_doc.md", f"{data_path}/translated_doc_level_mismatch_2.md")],
    indirect=True,
)
def test_level_mismatch_2(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 1

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(
        f"{data_path}/translated_doc_level_mismatch_2.md"
    ).read_text("utf-8")

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert "Error processing docs/lang/docs/doc.md" in result.output
    assert (
        "Header levels do not match between document and original document"
        " (found ##, expected #) for header №4 in line 13"
    ) in result.output
