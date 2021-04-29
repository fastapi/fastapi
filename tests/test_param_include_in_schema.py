from typing import Optional

import pytest
from fastapi import Cookie, FastAPI, Header, Path, Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/hidden_cookie")
async def hidden_cookie(
    hidden_cookie: Optional[str] = Cookie(None, include_in_schema=False)
):
    return {"hidden_cookie": hidden_cookie}


@app.get("/hidden_header")
async def hidden_header(
    hidden_header: Optional[str] = Header(None, include_in_schema=False)
):
    return {"hidden_header": hidden_header}


@app.get("/hidden_path/{hidden_path}")
async def hidden_path(hidden_path: str = Path(..., include_in_schema=False)):
    return {"hidden_path": hidden_path}


@app.get("/hidden_query")
async def hidden_query(hidden_query: str = Query(None, include_in_schema=False)):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_schema = response.json()
    assert (
        openapi_schema["paths"]["/hidden_cookie"]["get"].get("parameters", None) is None
    )
    assert (
        openapi_schema["paths"]["/hidden_header"]["get"].get("parameters", None) is None
    )
    assert (
        openapi_schema["paths"]["/hidden_path/{hidden_path}"]["get"].get(
            "parameters", None
        )
        is None
    )
    assert (
        openapi_schema["paths"]["/hidden_query"]["get"].get("parameters", None) is None
    )


@pytest.mark.parametrize(
    "path,cookies,expected_status,expected_response",
    [
        (
            "/hidden_cookie",
            {"hidden_cookie": "hidden_cookie"},
            200,
            {"hidden_cookie": "hidden_cookie"},
        ),
    ],
)
def test_hidden_cookie(path, cookies, expected_status, expected_response):
    response = client.get(path, cookies=cookies)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "path,headers,expected_status,expected_response",
    [
        (
            "/hidden_header",
            {"Hidden-Header": "hidden_header"},
            200,
            {"hidden_header": "hidden_header"},
        ),
    ],
)
def test_hidden_header(path, headers, expected_status, expected_response):
    response = client.get(path, headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        (
            "/hidden_path/hidden_path",
            200,
            {"hidden_path": "hidden_path"},
        ),
    ],
)
def test_hidden_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        (
            "/hidden_query?hidden_query=hidden_query",
            200,
            {"hidden_query": "hidden_query"},
        ),
        (
            "/hidden_query",
            200,
            {"hidden_query": "Not found"},
        ),
    ],
)
def test_hidden_query(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
