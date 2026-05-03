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
        ("path", "ann1", "ann2", "model_cls", "expected_ref_suffix"),
        [
            (
                "/file-a",
                File(),
                Depends(FooFilePayload),
                FooFilePayload,
                "FooFilePayload",
            ),
            (
                "/file-b",
                Depends(BarFilePayload),
                File(),
                BarFilePayload,
                "BarFilePayload",
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

    def test_runtime_file_validates_concrete_model(self) -> None:
        app = FastAPI()

        @app.post("/file-c")
        def route_file(
            data: Annotated[BasePayload, File(), Depends(FooFilePayload)],
        ) -> dict[str, str]:
            return {"extra": data.extra_foo, "fn": data.blob.filename or ""}

        client = TestClient(app)
        r = client.post(
            "/file-c",
            data={"kind": "foo", "extra_foo": "u"},
            files={"blob": ("up.txt", BytesIO(b"xyz"), "text/plain")},
        )
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"extra": "u", "fn": "up.txt"}

        bad = client.post(
            "/file-c",
            data={"kind": "foo"},
            files={"blob": ("up.txt", BytesIO(b"x"), "text/plain")},
        )
        assert bad.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

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
            ) -> None:
                pass  # pragma: no cover
