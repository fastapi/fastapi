from http import HTTPStatus
from typing import Annotated, Any

import pytest
from fastapi import (
    Body,
    Depends,
    FastAPI,
    File,
    Form,
    Header,
    Query,
    Security,
    status,
)
from fastapi.exceptions import FastAPIError
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient

from tests._annotated_body_depends_merge_common import (
    BarPayload,
    BasePayload,
    FooPayload,
    openapi_request_body_schema_ref,
)

_MERGED_BODY_DEFAULT = FooPayload(kind="foo", extra_foo="default")


class TestAnnotatedBodyDependsMergeBody:
    @pytest.mark.parametrize(
        (
            "path",
            "ann1",
            "ann2",
            "model_cls",
            "expected_ref_suffix",
            "assert_no_query_params",
        ),
        [
            ("/a", Body(), Depends(FooPayload), FooPayload, "FooPayload", True),
            ("/b", Depends(BarPayload), Body(), BarPayload, "BarPayload", False),
        ],
    )
    def test_openapi_json_body_depends_merge(
        self,
        path: str,
        ann1: Any,
        ann2: Any,
        model_cls: type[BasePayload],
        expected_ref_suffix: str,
        assert_no_query_params: bool,
    ) -> None:
        app = FastAPI()

        @app.post(path)
        def route(
            data: Annotated[BasePayload, ann1, ann2],
        ) -> None:
            assert isinstance(data, model_cls)

        client = TestClient(app)
        schema = client.get("/openapi.json").json()
        post = schema["paths"][path]["post"]
        if assert_no_query_params:
            assert post.get("parameters") in (None, [])
        ref = openapi_request_body_schema_ref(
            schema, path=path, method="post", content_type="application/json"
        )
        assert ref.endswith(f"/{expected_ref_suffix}")

    def test_runtime_json_validates_concrete_model(self) -> None:
        app = FastAPI()

        @app.post("/c")
        def route(
            data: Annotated[BasePayload, Body(), Depends(FooPayload)],
        ) -> dict[str, str]:
            return {"extra": data.extra_foo}

        client = TestClient(app)
        r = client.post("/c", json={"kind": "foo", "extra_foo": "x"})
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"extra": "x"}

        bad = client.post("/c", json={"kind": "foo"})
        # not status.*: Starlette confused HTTP_422_UNPROCESSABLE_CONTENT HTTP_422_UNPROCESSABLE_ENTITY
        assert bad.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_merge_depends_empty_falls_back_to_declared_model(self) -> None:
        app = FastAPI()

        @app.post("/depends-empty")
        def route(
            data: Annotated[FooPayload, Body(), Depends()],
        ) -> dict[str, str]:
            return {"extra": data.extra_foo}

        client = TestClient(app)
        r = client.post("/depends-empty", json={"kind": "foo", "extra_foo": "z"})
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"extra": "z"}

    def test_merged_body_parameter_signature_default(self) -> None:
        app = FastAPI()

        @app.post("/merged-default")
        def route(
            data: Annotated[
                BasePayload, Body(), Depends(FooPayload)
            ] = _MERGED_BODY_DEFAULT,
        ) -> dict[str, str]:
            return {"extra": data.extra_foo}

        client = TestClient(app)
        empty = client.post("/merged-default")
        assert empty.status_code == status.HTTP_200_OK
        assert empty.json() == {"extra": "default"}

        overridden = client.post(
            "/merged-default", json={"kind": "foo", "extra_foo": "ov"}
        )
        assert overridden.status_code == status.HTTP_200_OK
        assert overridden.json() == {"extra": "ov"}

    def test_put_patch_json_body_depends_openapi(self) -> None:
        app = FastAPI()
        path = "/items/{item_id}"

        @app.put(path)
        def route_put(
            item_id: str,
            data: Annotated[BasePayload, Body(), Depends(FooPayload)],
        ) -> None:
            assert isinstance(data, FooPayload)

        @app.patch(path)
        def route_patch(
            item_id: str,
            data: Annotated[BasePayload, Depends(FooPayload), Body()],
        ) -> None:
            assert isinstance(data, FooPayload)

        client = TestClient(app)
        schema = client.get("/openapi.json").json()
        for method in ("put", "patch"):
            ref = openapi_request_body_schema_ref(
                schema, path=path, method=method, content_type="application/json"
            )
            assert ref.endswith("/FooPayload")

        r = client.put("/items/1", json={"kind": "foo", "extra_foo": "a"})
        assert r.status_code == status.HTTP_200_OK
        r2 = client.patch("/items/1", json={"kind": "foo", "extra_foo": "b"})
        assert r2.status_code == status.HTTP_200_OK

    def test_rejects_body_with_callable_depends(self) -> None:
        app = FastAPI()

        def not_a_model() -> None:
            return None

        with pytest.raises(FastAPIError, match="Pydantic model class"):

            @app.post("/d")
            def route_d(
                data: Annotated[BasePayload, Body(), Depends(not_a_model)],
            ) -> None:
                pass  # pragma: no cover

    def test_rejects_multiple_depends_with_body(self) -> None:
        app = FastAPI()

        with pytest.raises(FastAPIError, match="multiple `Depends`"):

            @app.post("/e")
            def route_e(
                data: Annotated[
                    BasePayload,
                    Body(),
                    Depends(FooPayload),
                    Depends(BarPayload),
                ],
            ) -> None:
                pass  # pragma: no cover

    def test_rejects_body_and_form_together(self) -> None:
        app = FastAPI()

        with pytest.raises(FastAPIError, match="multiple `Body`"):

            @app.post("/conflict")
            def route_conflict(
                data: Annotated[
                    BasePayload,
                    Body(),
                    Form(),
                    Depends(FooPayload),
                ],
            ) -> None:
                pass  # pragma: no cover

    @pytest.mark.parametrize(
        "shape_marker",
        [
            pytest.param(Body(), id="body"),
            pytest.param(Form(), id="form"),
            pytest.param(File(), id="file"),
        ],
    )
    def test_rejects_query_with_body_like_in_same_annotated(
        self, shape_marker: Any
    ) -> None:
        app = FastAPI()

        with pytest.raises(FastAPIError, match="Cannot combine `Query`"):

            @app.post("/query-shape")
            def route_bad(
                data: Annotated[
                    BasePayload,
                    shape_marker,
                    Query(),
                    Depends(FooPayload),
                ],
            ) -> None:
                pass  # pragma: no cover

    def test_rejects_multiple_query_with_depends(self) -> None:
        app = FastAPI()

        with pytest.raises(FastAPIError, match="multiple `Query`"):

            @app.post("/multi-query")
            def route_multi_query(
                data: Annotated[
                    BasePayload,
                    Query(),
                    Query(),
                    Depends(FooPayload),
                ],
            ) -> None:
                pass  # pragma: no cover

    def test_rejects_body_like_with_other_param_in_same_annotated(self) -> None:
        app = FastAPI()

        with pytest.raises(FastAPIError, match="other parameter types"):

            @app.post("/body-plus-header")
            def route_body_header(
                data: Annotated[
                    BasePayload,
                    Body(),
                    Header(),
                    Depends(FooPayload),
                ],
            ) -> None:
                pass  # pragma: no cover

    def test_rejects_security_with_body_like_merge(self) -> None:
        app = FastAPI()
        bearer = HTTPBearer(auto_error=False)

        with pytest.raises(FastAPIError, match="`Security`"):

            @app.post("/body-security")
            def route_body_security(
                data: Annotated[BasePayload, Body(), Security(bearer)],
            ) -> None:
                pass  # pragma: no cover

    def test_rejects_merge_on_path_parameter(self) -> None:
        app = FastAPI()

        with pytest.raises(FastAPIError, match="path parameter"):

            @app.post("/path/{data}")
            def route_path(
                data: Annotated[BasePayload, Body(), Depends(FooPayload)],
            ) -> None:
                pass  # pragma: no cover
