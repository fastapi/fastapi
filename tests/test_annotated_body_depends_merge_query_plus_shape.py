"""Query() alongside a second parameter that uses Body/Form/File + Depends(model)."""

from io import BytesIO
from typing import Annotated, Any

from fastapi import Body, Depends, FastAPI, File, Form, Query, status
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

        hit_payload = {"kind": "foo", "extra_foo": "x"}
        hit = client.post("/mix-json?client_id=hit", json=hit_payload)
        assert hit.status_code == status.HTTP_200_OK

    def test_runtime_query_plus_json_body(self) -> None:
        app = FastAPI()

        @app.post("/r-json")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, Body(), Depends(FooPayload)],
        ) -> dict[str, str]:
            return {"client": client_id, "extra": data.extra_foo}

        client = TestClient(app)
        client_id = "c1"
        extra = "helloworld"
        payload = {"kind": "foo", "extra_foo": extra}
        expected_json = {"client": client_id, "extra": extra}
        r = client.post(f"/r-json?client_id={client_id}", json=payload)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == expected_json

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

        hit_payload = {"kind": "bar", "extra_bar": "y"}
        hit = client.post("/mix-form", params={"client_id": "hit"}, data=hit_payload)
        assert hit.status_code == status.HTTP_200_OK

    def test_runtime_query_plus_form(self) -> None:
        app = FastAPI()

        @app.post("/r-form")
        def route(
            client_id: Annotated[str, Query()],
            data: Annotated[BasePayload, Form(), Depends(FooPayload)],
        ) -> dict[str, str]:
            return {"client": client_id, "extra": data.extra_foo}

        client = TestClient(app)
        client_id = "c2"
        extra = "foo"
        payload = {"kind": "foo", "extra_foo": extra}
        expected_json = {"client": client_id, "extra": extra}
        r = client.post("/r-form", params={"client_id": client_id}, data=payload)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == expected_json

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

        hit_form = {"kind": "foo", "extra_foo": "u"}
        hit_files = {
            "blob": ("up.bin", BytesIO(b"abc"), "application/octet-stream"),
        }
        hit = client.post(
            "/mix-file",
            params={"client_id": "hit"},
            data=hit_form,
            files=hit_files,
        )
        assert hit.status_code == status.HTTP_200_OK

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
        client_id = "c3"
        extra = "bar"
        filename = "up.bin"
        payload = {"kind": "bar", "extra_bar": extra}
        file_field = (filename, BytesIO(b"abc"), "application/octet-stream")
        expected_json = {"client": client_id, "extra": extra, "fn": filename}
        r = client.post(
            "/r-file",
            params={"client_id": client_id},
            data=payload,
            files={"blob": file_field},
        )
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == expected_json
