from typing import Annotated

from fastapi import FastAPI, File, Form, Query, UploadFile
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing_extensions import TypeAliasType

StrListAlias = TypeAliasType("StrListAlias", list[str])
IntSetAlias = TypeAliasType("IntSetAlias", set[int])
UploadFileListAlias = TypeAliasType("UploadFileListAlias", list[UploadFile])
BytesListAlias = TypeAliasType("BytesListAlias", list[bytes])
OptionalStrListAlias = TypeAliasType("OptionalStrListAlias", list[str] | None)
ChainedListAlias = TypeAliasType("ChainedListAlias", StrListAlias)


class ItemModel(BaseModel):
    tags: StrListAlias
    counts: IntSetAlias


app = FastAPI()


@app.get("/query-list")
def get_query_list(q: Annotated[StrListAlias, Query()]):
    return {"q": q}


@app.get("/query-chained")
def get_query_chained(q: Annotated[ChainedListAlias, Query()]):
    return {"q": q}


@app.get("/query-set")
def get_query_set(s: Annotated[IntSetAlias, Query()]):
    return {"s": sorted(s)}


@app.get("/query-optional")
def get_query_optional(q: Annotated[OptionalStrListAlias, Query()] = None):
    return {"q": q}


@app.post("/form-model")
def post_form_model(item: Annotated[ItemModel, Form()]):
    return {"tags": item.tags, "counts": sorted(item.counts)}


@app.post("/upload-files")
async def post_upload_files(files: Annotated[UploadFileListAlias, File()]):
    return {"filenames": [f.filename for f in files]}


@app.post("/upload-bytes")
async def post_upload_bytes(files: Annotated[BytesListAlias, File()]):
    return {"sizes": [len(b) for b in files]}


client = TestClient(app)


def test_query_list_pep695():
    response = client.get("/query-list", params=[("q", "a"), ("q", "b"), ("q", "c")])
    assert response.status_code == 200, response.text
    assert response.json() == {"q": ["a", "b", "c"]}


def test_query_chained_alias_pep695():
    response = client.get("/query-chained", params=[("q", "1"), ("q", "2")])
    assert response.status_code == 200, response.text
    assert response.json() == {"q": ["1", "2"]}


def test_query_set_pep695():
    response = client.get(
        "/query-set", params=[("s", "1"), ("s", "2"), ("s", "2"), ("s", "3")]
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"s": [1, 2, 3]}


def test_query_optional_pep695():
    response = client.get("/query-optional")
    assert response.status_code == 200, response.text
    assert response.json() == {"q": None}

    response = client.get("/query-optional", params=[("q", "a"), ("q", "b")])
    assert response.status_code == 200, response.text
    assert response.json() == {"q": ["a", "b"]}


def test_form_model_pep695():
    response = client.post(
        "/form-model", data={"tags": ["tag1", "tag2"], "counts": ["1", "2"]}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"tags": ["tag1", "tag2"], "counts": [1, 2]}


def test_upload_files_pep695():
    response = client.post(
        "/upload-files",
        files=[
            ("files", ("test1.txt", b"hello", "text/plain")),
            ("files", ("test2.txt", b"world", "text/plain")),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"filenames": ["test1.txt", "test2.txt"]}


def test_upload_bytes_pep695():
    response = client.post(
        "/upload-bytes",
        files=[
            ("files", ("b1.bin", b"12345", "application/octet-stream")),
            ("files", ("b2.bin", b"123", "application/octet-stream")),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"sizes": [5, 3]}


def test_openapi_schema_pep695():
    schema = app.openapi()
    assert "/query-list" in schema["paths"]
    query_param = schema["paths"]["/query-list"]["get"]["parameters"][0]
    assert query_param["name"] == "q"
    assert query_param["in"] == "query"
    assert "StrListAlias" in schema["components"]["schemas"]


def test_native_pep695_syntax_on_python312():
    import sys

    if sys.version_info < (3, 12):
        return

    code = """
type NativeList = list[str]

native_app = FastAPI()

@native_app.get("/native-query")
def get_native_query(tags: Annotated[NativeList, Query()]):
    return {"tags": tags}

native_client = TestClient(native_app)
resp = native_client.get("/native-query", params=[("tags", "one"), ("tags", "two")])
assert resp.status_code == 200
assert resp.json() == {"tags": ["one", "two"]}
"""
    local_ns = {
        "FastAPI": FastAPI,
        "Annotated": Annotated,
        "Query": Query,
        "TestClient": TestClient,
    }
    exec(code, local_ns)
