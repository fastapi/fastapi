from pathlib import Path

import pytest
from typer.testing import CliRunner

from scripts.translation_fixer import cli

data_path = Path(
    "scripts/tests/test_translation_fixer/test_code_blocks/data"
).absolute()


@pytest.mark.parametrize(
    "copy_test_files",
    [(f"{data_path}/en_doc.md", f"{data_path}/translated_doc_wrong_lang_code.md")],
    indirect=True,
)
def test_wrong_lang_code_1(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 1, result.output

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(f"{data_path}/translated_doc_wrong_lang_code.md").read_text(
        "utf-8"
    )

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert "Error processing docs/lang/docs/doc.md" in result.output
    assert (
        "Code block (lines 16-19) has different language than the original block ('yaml' vs 'toml')"
    ) in result.output


@pytest.mark.parametrize(
    "copy_test_files",
    [(f"{data_path}/en_doc.md", f"{data_path}/translated_doc_wrong_lang_code_2.md")],
    indirect=True,
)
def test_wrong_lang_code_2(runner: CliRunner, root_dir: Path, copy_test_files):
    result = runner.invoke(
        cli,
        ["fix-pages", "docs/lang/docs/doc.md"],
    )
    assert result.exit_code == 1, result.output

    fixed_content = (root_dir / "docs" / "lang" / "docs" / "doc.md").read_text("utf-8")
    expected_content = Path(
        f"{data_path}/translated_doc_wrong_lang_code_2.md"
    ).read_text("utf-8")

    assert fixed_content == expected_content  # Translated doc remains unchanged
    assert "Error processing docs/lang/docs/doc.md" in result.output
    assert (
        "Code block (lines 16-19) has different language than the original block ('' vs 'toml')"
    ) in result.output
