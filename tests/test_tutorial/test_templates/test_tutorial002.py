import shutil
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tests.utils import workdir_lock


@pytest.mark.parametrize("root_path", ["", "/api/v1"])
@pytest.mark.parametrize("mount_path", ["", "/subapp"])
@workdir_lock
def test_main(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    root_path: str,
    mount_path: str,
):
    tutorial_dir = Path(__file__).resolve().parents[3] / "docs_src" / "templates"
    shutil.copytree(tutorial_dir / "templates", tmp_path / "templates")
    shutil.copytree(tutorial_dir / "static", tmp_path / "static")
    monkeypatch.chdir(tmp_path)
    from docs_src.templates.tutorial002_py310 import app

    if mount_path:
        main_app = FastAPI()
        main_app.mount(mount_path, app)
    else:
        main_app = app

    client = TestClient(main_app, root_path=root_path, base_url="https://example.com")
    prefix = root_path + mount_path
    response = client.get(f"{prefix}/items/42")
    assert response.status_code == 200, response.text
    assert f'<a href="{prefix}/items/42">Item ID: 42</a>' in response.text
    assert f'<link href="{prefix}/static/styles.css" rel="stylesheet">' in response.text
    response = client.get(f"{prefix}/static/styles.css")
    assert response.status_code == 200, response.text
    assert "color: green;" in response.text
