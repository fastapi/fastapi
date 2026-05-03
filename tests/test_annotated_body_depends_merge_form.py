from http import HTTPStatus
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI, Form, status
from fastapi.testclient import TestClient

from tests._annotated_body_depends_merge_common import (
    BarPayload,
    BasePayload,
    FooPayload,
)


class TestAnnotatedBodyDependsMergeForm:
    @pytest.mark.parametrize(
        ("path", "ann1", "ann2", "model_cls", "expected_ref_suffix"),
        [
            ("/form-a", Form(), Depends(FooPayload), FooPayload, "FooPayload"),
            ("/form-b", Depends(BarPayload), Form(), BarPayload, "BarPayload"),
        ],
    )
    def test_openapi_form_depends_merge(
        self,
        path: str,
        ann1: Any,
        ann2: Any,
        model_cls: type[BasePayload],
        expected_ref_suffix: str,
    ) -> None:
        app = FastAPI()

        @app.post(path)
        def route_form(
            data: Annotated[BasePayload, ann1, ann2],
        ) -> None:
            assert isinstance(data, model_cls)

        client = TestClient(app)
        schema = client.get("/openapi.json").json()
        rb = schema["paths"][path]["post"]["requestBody"]
        content = rb["content"]
        assert "application/x-www-form-urlencoded" in content
        ref = content["application/x-www-form-urlencoded"]["schema"]["$ref"]
        assert ref.endswith(f"/{expected_ref_suffix}")

    def test_runtime_form_validates_concrete_model(self) -> None:
        app = FastAPI()

        @app.post("/form-c")
        def route_form(
            data: Annotated[BasePayload, Form(), Depends(FooPayload)],
        ) -> dict[str, str]:
            return {"extra": data.extra_foo}

        client = TestClient(app)
        r = client.post(
            "/form-c",
            data={"kind": "foo", "extra_foo": "z"},
        )
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"extra": "z"}

        bad = client.post("/form-c", data={"kind": "foo"})
        # not status.*: Starlette confused HTTP_422_UNPROCESSABLE_CONTENT HTTP_422_UNPROCESSABLE_ENTITY
        assert bad.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
