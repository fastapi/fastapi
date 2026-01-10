import shutil
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

skip_on_windows = pytest.mark.skipif(
    sys.platform == "win32", reason="Skipping on Windows"
)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        item.add_marker(skip_on_windows)


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
