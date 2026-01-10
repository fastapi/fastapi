import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner


@pytest.fixture(name="runner")
def get_runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture(name="root_dir")
def prepare_paths(runner):
    docs_dir = Path("docs")
    en_docs_dir = docs_dir / "en" / "docs"
    lang_docs_dir = docs_dir / "lang" / "docs"
    en_docs_dir.mkdir(parents=True, exist_ok=True)
    lang_docs_dir.mkdir(parents=True, exist_ok=True)
    yield Path.cwd()


@pytest.fixture
def copy_test_files(root_dir: Path, request: pytest.FixtureRequest):
    en_file_path = Path(request.param[0])
    translation_file_path = Path(request.param[1])
    shutil.copy(str(en_file_path), str(root_dir / "docs" / "en" / "docs" / "doc.md"))
    shutil.copy(
        str(translation_file_path), str(root_dir / "docs" / "lang" / "docs" / "doc.md")
    )
