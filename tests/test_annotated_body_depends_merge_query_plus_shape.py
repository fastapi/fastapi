"""Query() alongside a second parameter that uses Body/Form/File + Depends(model)."""

from io import BytesIO
from typing import Annotated, Any

from fastapi import Body, Depends, FastAPI, File, Form, Query
from fastapi.testclient import TestClient

from tests._annotated_body_depends_merge_common import (
    BarFilePayload,
    BarPayload,
    BasePayload,
    FooFilePayload,
    FooPayload,
    openapi_request_body_schema_ref,
)


def _param_names(post_schema: dict[str, Any]) -> list[str]:
    params = post_schema.get("parameters") or []
    return [p["name"] for p in params]


class TestQueryPlusMergedShape:
    def test_openapi_query_plus_json_body(self) -> None:
        app = FastAPI()

        @app.post("/mix-json")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, Body(), Depends(FooPayload)],
        ) -> None:
            assert isinstance(data, FooPayload)

        client = TestClient(app)
        schema = client.get("/openapi.json").json()
        post = schema["paths"]["/mix-json"]["post"]
        assert "client_id" in _param_names(post)
        ref = openapi_request_body_schema_ref(
            schema,
            path="/mix-json",
            method="post",
            content_type="application/json",
        )
        assert ref.endswith("/FooPayload")

    def test_runtime_query_plus_json_body(self) -> None:
        app = FastAPI()

        @app.post("/r-json")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, Body(), Depends(FooPayload)],
        ) -> dict[str, str]:
            return {"client": client_id, "extra": data.extra_foo}

        client = TestClient(app)
        r = client.post(
            "/r-json?client_id=c1",
            json={"kind": "foo", "extra_foo": "e"},
        )
        assert r.status_code == 200
        assert r.json() == {"client": "c1", "extra": "e"}

    def test_openapi_query_plus_form(self) -> None:
        app = FastAPI()

        @app.post("/mix-form")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, Form(), Depends(BarPayload)],
        ) -> None:
            assert isinstance(data, BarPayload)

        client = TestClient(app)
        schema = client.get("/openapi.json").json()
        post = schema["paths"]["/mix-form"]["post"]
        assert "client_id" in _param_names(post)
        rb = post["requestBody"]["content"]
        assert "application/x-www-form-urlencoded" in rb
        ref = rb["application/x-www-form-urlencoded"]["schema"]["$ref"]
        assert ref.endswith("/BarPayload")

    def test_runtime_query_plus_form(self) -> None:
        app = FastAPI()

        @app.post("/r-form")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, Form(), Depends(FooPayload)],
        ) -> dict[str, str]:
            return {"client": client_id, "extra": data.extra_foo}

        client = TestClient(app)
        r = client.post(
            "/r-form",
            params={"client_id": "c2"},
            data={"kind": "foo", "extra_foo": "f"},
        )
        assert r.status_code == 200
        assert r.json() == {"client": "c2", "extra": "f"}

    def test_openapi_query_plus_file_multipart(self) -> None:
        app = FastAPI()

        @app.post("/mix-file")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, File(), Depends(FooFilePayload)],
        ) -> None:
            assert isinstance(data, FooFilePayload)

        client = TestClient(app)
        schema = client.get("/openapi.json").json()
        post = schema["paths"]["/mix-file"]["post"]
        assert "client_id" in _param_names(post)
        rb = post["requestBody"]["content"]
        assert "multipart/form-data" in rb
        ref = rb["multipart/form-data"]["schema"]["$ref"]
        assert ref.endswith("/FooFilePayload")

    def test_runtime_query_plus_file_multipart(self) -> None:
        app = FastAPI()

        @app.post("/r-file")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, File(), Depends(BarFilePayload)],
        ) -> dict[str, str]:
            return {
                "client": client_id,
                "extra": data.extra_bar,
                "fn": data.blob.filename or "",
            }

        client = TestClient(app)
        r = client.post(
            "/r-file",
            params={"client_id": "c3"},
            data={"kind": "bar", "extra_bar": "b"},
            files={"blob": ("up.bin", BytesIO(b"abc"), "application/octet-stream")},
        )
        assert r.status_code == 200
        assert r.json() == {"client": "c3", "extra": "b", "fn": "up.bin"}
