import os
import shutil
import sys
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pytest
from typer.testing import CliRunner

skip_on_windows = pytest.mark.skipif(
    sys.platform == "win32", reason="Skipping on Windows"
)


THIS_DIR = Path(__file__).parent.resolve()


def pytest_collection_modifyitems(config, items: list[pytest.Item]) -> None:
    if sys.platform != "win32":
        return

    for item in items:
        item_path = Path(item.fspath).resolve()
        if item_path.is_relative_to(THIS_DIR):
            item.add_marker(skip_on_windows)


@contextmanager
def changing_dir(directory: str | Path) -> Generator[None, None, None]:
    initial_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(initial_dir)


@pytest.fixture(name="runner")
def get_runner(tmp_path: Path):
    with changing_dir(tmp_path):
        yield CliRunner()


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
