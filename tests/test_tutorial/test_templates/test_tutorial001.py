import os
import shutil

from fastapi.testclient import TestClient


def test_main():
    if os.path.isdir("./static"):  # pragma: nocover
        shutil.rmtree("./static")
    if os.path.isdir("./templates"):  # pragma: nocover
        shutil.rmtree("./templates")
    shutil.copytree("./docs_src/templates/templates/", "./templates")
    shutil.copytree("./docs_src/templates/static/", "./static")
    from docs_src.templates.tutorial001 import app

    client = TestClient(app)
    response = client.get("/items/foo")
    assert response.status_code == 200, response.text
    assert (
        b'<h1><a href="http://testserver/items/foo">Item ID: foo</a></h1>'
        in response.content
    )
    response = client.get("/static/styles.css")
    assert response.status_code == 200, response.text
    assert b"color: green;" in response.content
    shutil.rmtree("./templates")
    shutil.rmtree("./static")
