import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from .utils import needs_pydanticv2


@needs_pydanticv2
@pytest.mark.parametrize(
    "include_error_input,include_error_url",
    [(False, False), (False, True), (True, False), (True, True)],
)
def test_input_and_url_fields(include_error_input, include_error_url):
    app = FastAPI(
        include_error_input=include_error_input, include_error_url=include_error_url
    )

    @app.get("/path1/{path_param}")
    def path1(path_param: int):
        return {"path_param": path_param}

    @app.get("/path2/")
    def path2(query_param: int):
        return query_param

    router = APIRouter()

    @app.get("/path3/{path_param}")
    def path3(path_param: int):
        return {"path_param": path_param}

    @app.get("/path4/")
    def path4(query_param: int):
        return query_param

    app.include_router(router, prefix="/prefix")
    client = TestClient(app)

    with client:
        invalid = "not-an-integer"

        for path in ["path1", "path3"]:
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

        for path in ["path2", "path4"]:
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
