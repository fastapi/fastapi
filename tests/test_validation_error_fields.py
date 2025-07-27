import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from .utils import needs_pydanticv1, needs_pydanticv2


@needs_pydanticv2
@pytest.mark.parametrize(
    "include_error_input,include_error_url",
    [(False, False), (False, True), (True, False), (True, True)],
)
def test_input_and_url_fields_with_pydanticv2(include_error_input, include_error_url):
    app = FastAPI(
        include_error_input=include_error_input, include_error_url=include_error_url
    )

    @app.get("/get1/{path_param}")
    def get1(path_param: int):
        ...

    @app.get("/get2/")
    def get2(query_param: int):
        ...

    class Body1(BaseModel):
        ...

    class Body2(BaseModel):
        ...

    @app.post("/post1/")
    def post1(body1: Body1, body2: Body2):
        ...

    router = APIRouter(
        include_error_input=include_error_input, include_error_url=include_error_url
    )

    @router.get("/get3/{path_param}")
    def get3(path_param: int):
        ...

    @router.get("/get4/")
    def get4(query_param: int):
        ...

    @router.post("/post2/")
    def post2(body1: Body1, body2: Body2):
        ...

    app.include_router(router)
    client = TestClient(app)
    with client:
        invalid = "not-an-integer"

        for path in ["get1", "get3"]:
            response = client.get(f"/{path}/{invalid}")
            assert response.status_code == 422, response.text
            error = response.json()["detail"][0]
            if include_error_input:
                assert error["input"] == invalid
            else:
                assert "input" not in error
            if include_error_url:
                assert "url" in error
            else:
                assert "url" not in error

        for path in ["get2", "get4"]:
            response = client.get(f"/{path}/")
            assert response.status_code == 422, response.text
            error = response.json()["detail"][0]
            if include_error_input:
                assert error["type"] == "missing"
                assert error["input"] is None
            else:
                assert "input" not in error
            if include_error_url:
                assert "url" in error
            else:
                assert "url" not in error

            response = client.get(f"/{path}/?query_param={invalid}")
            assert response.status_code == 422, response.text
            error = response.json()["detail"][0]
            if include_error_input:
                assert error["input"] == invalid
            else:
                assert "input" not in error
            if include_error_url:
                assert "url" in error
            else:
                assert "url" not in error

        for path in ["post1", "post2"]:
            response = client.post(f"/{path}/", json=["not-a-dict"])
            assert response.status_code == 422
            error = response.json()["detail"][0]
            if include_error_input:
                assert error["type"] == "missing"
                assert error["input"] is None
            else:
                assert "input" not in error
            if include_error_url:
                assert "url" in error
            else:
                assert "url" not in error


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
@pytest.mark.parametrize(
    "include_error_input,include_error_url",
    [(False, False), (False, True), (True, False), (True, True)],
)
def test_input_and_url_fields_with_pydanticv1(include_error_input, include_error_url):
    app = FastAPI(
        include_error_input=include_error_input, include_error_url=include_error_url
    )

    @app.get("/get1/{path_param}")
    def get1(path_param: int):
        ...

    @app.get("/get2/")
    def get2(query_param: int):
        ...

    class Body1(BaseModel):
        ...

    class Body2(BaseModel):
        ...

    @app.post("/post1/")
    def post1(body1: Body1, body2: Body2):
        ...

    router = APIRouter(
        include_error_input=include_error_input, include_error_url=include_error_url
    )

    @router.get("/get3/{path_param}")
    def get3(path_param: int):
        ...

    @router.get("/get4/")
    def get4(query_param: int):
        ...

    @router.post("/post2/")
    def post2(body1: Body1, body2: Body2):
        ...

    app.include_router(router)
    client = TestClient(app)
    with client:
        invalid = "not-an-integer"

        for path in ["get1", "get3"]:
            response = client.get(f"/{path}/{invalid}")
            assert response.status_code == 422, response.text
            error = response.json()["detail"][0]
            assert "input" not in error
            assert "url" not in error

        for path in ["get2", "get4"]:
            response = client.get(f"/{path}/")
            assert response.status_code == 422, response.text
            error = response.json()["detail"][0]
            assert "input" not in error
            assert "url" not in error

            response = client.get(f"/{path}/?query_param={invalid}")
            assert response.status_code == 422, response.text
            error = response.json()["detail"][0]
            assert "input" not in error
            assert "url" not in error

        for path in ["post1", "post2"]:
            response = client.post(f"/{path}/", json=["not-a-dict"])
            assert response.status_code == 422
            error = response.json()["detail"][0]
            assert "input" not in error
            assert "url" not in error
