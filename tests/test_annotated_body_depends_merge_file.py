from http import HTTPStatus
from io import BytesIO
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI, File, Form, status
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient

from tests._annotated_body_depends_merge_common import (
    BarFilePayload,
    BasePayload,
    FooFilePayload,
    FooPayload,
)


class TestAnnotatedBodyDependsMergeFile:
    @pytest.mark.parametrize(
        ("path", "ann1", "ann2", "model_cls", "expected_ref_suffix", "payload"),
        [
            (
                "/file-a",
                File(),
                Depends(FooFilePayload),
                FooFilePayload,
                "FooFilePayload",
                {"kind": "foo", "extra_foo": "hit"},
            ),
            (
                "/file-b",
                Depends(BarFilePayload),
                File(),
                BarFilePayload,
                "BarFilePayload",
                {"kind": "bar", "extra_bar": "hit"},
            ),
        ],
    )
    def test_openapi_file_depends_merge(
        self,
        path: str,
        ann1: Any,
        ann2: Any,
        model_cls: type[BasePayload],
        expected_ref_suffix: str,
        payload: dict[str, str],
    ) -> None:
        app = FastAPI()

        @app.post(path)
        def route_file(
            data: Annotated[BasePayload, ann1, ann2],
        ) -> None:
            assert isinstance(data, model_cls)

        client = TestClient(app)
        schema = client.get("/openapi.json").json()
        rb = schema["paths"][path]["post"]["requestBody"]
        content = rb["content"]
        assert "multipart/form-data" in content
        ref = content["multipart/form-data"]["schema"]["$ref"]
        assert ref.endswith(f"/{expected_ref_suffix}")

        blob = ("blob.bin", BytesIO(b"x"), "application/octet-stream")
        ok = client.post(path, data=payload, files={"blob": blob})
        assert ok.status_code == status.HTTP_200_OK

    def test_runtime_file_validates_concrete_model(self) -> None:
        app = FastAPI()

        @app.post("/file-c")
        def route_file(
            data: Annotated[BasePayload, File(), Depends(FooFilePayload)],
        ) -> dict[str, str]:
            return {"extra": data.extra_foo, "fn": data.blob.filename or ""}

        client = TestClient(app)
        extra = "info"
        filename = "file.txt"
        payload = {"kind": "foo", "extra_foo": extra}
        file_field = (filename, BytesIO(b"xyz"), "text/plain")
        expected_json = {"extra": extra, "fn": filename}
        r = client.post("/file-c", data=payload, files={"blob": file_field})
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == expected_json

        bad = client.post(
            "/file-c",
            data={"kind": "foo"},
            files={"blob": ("up.txt", BytesIO(b"x"), "text/plain")},
        )
        # not status.*: Starlette confused HTTP_422_UNPROCESSABLE_CONTENT HTTP_422_UNPROCESSABLE_ENTITY
        assert bad.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_rejects_file_and_form_together(self) -> None:
        app = FastAPI()

        with pytest.raises(FastAPIError, match="multiple `Body`"):

            @app.post("/file-conflict")
            def route_conflict(
                data: Annotated[
                    BasePayload,
                    File(),
                    Form(),
                    Depends(FooPayload),
                ],
            ) -> None: ...
