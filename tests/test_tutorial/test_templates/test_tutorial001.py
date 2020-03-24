import shutil

from fastapi.testclient import TestClient


def test_main():
    shutil.copytree("./docs_src/templates/templates/", "./templates")
    shutil.copytree("./docs_src/templates/static/", "./static")
    from templates.tutorial001 import app

    client = TestClient(app)
    response = client.get("/items/foo")
    assert response.status_code == 200
    assert b"<h1>Item ID: foo</h1>" in response.content
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert b"color: green;" in response.content
    shutil.rmtree("./templates")
    shutil.rmtree("./static")
