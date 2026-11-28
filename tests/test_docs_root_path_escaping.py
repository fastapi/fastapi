from fastapi import FastAPI
from fastapi.testclient import TestClient

sub_app = FastAPI()
app = FastAPI()
# A parameterized Mount writes the raw matched path prefix into the request
# `root_path`, so the docs routes receive request data as their base URL.
app.mount("/{tenant}", sub_app)

client = TestClient(app)

PAYLOAD = "/%27%2Balert(1)%2B%27"


def test_swagger_ui_escapes_request_controlled_urls():
    response = client.get(f"{PAYLOAD}/docs")
    assert response.status_code == 200
    # The payload must not be able to close the JavaScript string literal.
    assert "'+alert(1)+'" not in response.text
    assert "\\'+alert(1)+\\'" in response.text
    assert response.text.count("\\'+alert(1)+\\'") == 2  # openapi + oauth2 urls


def test_redoc_escapes_request_controlled_url():
    response = client.get(f"{PAYLOAD}/redoc")
    assert response.status_code == 200
    assert "'+alert(1)+'" not in response.text
    assert (
        '<redoc spec-url="/&#x27;+alert(1)+&#x27;/openapi.json"></redoc>'
        in response.text
    )


def test_docs_urls_unchanged_without_special_characters():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "url: '/openapi.json'," in response.text
    assert "window.location.origin + '/docs/oauth2-redirect'" in response.text
    assert "\\'" not in response.text
