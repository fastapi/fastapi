from fastapi import FastAPI
from fastapi.responses import (
    JSONResponse,
    ORJSONResponse,
    RedirectResponse,
    Response,
    UJSONResponse,
)
from fastapi.testclient import TestClient


def test_response_classes_have_default_status_code_attribute() -> None:
    assert Response.default_status_code == 200
    assert JSONResponse.default_status_code == 200
    assert RedirectResponse.default_status_code == 307


def test_json_variants_default_status_code_attribute() -> None:
    assert UJSONResponse.default_status_code == JSONResponse.default_status_code
    assert ORJSONResponse.default_status_code == JSONResponse.default_status_code


class CustomResponse(Response):
    default_status_code = 204


app = FastAPI()


@app.get("/", response_class=CustomResponse)
def read_root() -> str:
    return "Hello"


client = TestClient(app)


def test_default_status_code_used_for_instances() -> None:
    response = Response()
    assert response.status_code == 200
    custom_response = Response(status_code=201)
    assert custom_response.status_code == 201
    assert Response.default_status_code == 200


def test_custom_response_status_code_handling_and_openapi() -> None:
    response = client.get("/")
    assert response.status_code == 204
    openapi_schema = app.openapi()
    assert "204" in openapi_schema["paths"]["/"]["get"]["responses"]
    overridden = CustomResponse(status_code=202)
    assert overridden.status_code == 202


def test_default_status_code_inherited_in_subclass() -> None:
    class ParentResponse(Response):
        default_status_code = 203

    class ChildResponse(ParentResponse):
        pass

    app = FastAPI()

    @app.get("/child", response_class=ChildResponse)
    def read_child() -> str:
        return "Child"

    child_client = TestClient(app)
    response = child_client.get("/child")
    assert response.status_code == 203
    openapi_schema = app.openapi()
    assert "203" in openapi_schema["paths"]["/child"]["get"]["responses"]
