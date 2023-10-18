import pytest
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse


def http_exception_handler(request, exception):
    return JSONResponse({"exception": "http-exception"})


def request_validation_exception_handler(request, exception):
    return JSONResponse({"exception": "request-validation"})


def server_error_exception_handler(request, exception):
    return JSONResponse(status_code=500, content={"exception": "server-error"})


app = FastAPI(
    exception_handlers={
        HTTPException: http_exception_handler,
        RequestValidationError: request_validation_exception_handler,
        Exception: server_error_exception_handler,
    }
)

client = TestClient(app)


@app.get("/http-exception")
def route_with_http_exception():
    raise HTTPException(status_code=400)


@app.get("/request-validation/{param}/")
def route_with_request_validation_exception(param: int):
    pass  # pragma: no cover


@app.get("/server-error")
def route_with_server_error():
    raise RuntimeError("Oops!")


def test_override_http_exception():
    response = client.get("/http-exception")
    assert response.status_code == 200
    assert response.json() == {"exception": "http-exception"}


def test_override_request_validation_exception():
    response = client.get("/request-validation/invalid")
    assert response.status_code == 200
    assert response.json() == {"exception": "request-validation"}


def test_override_server_error_exception_raises():
    with pytest.raises(RuntimeError):
        client.get("/server-error")


def test_override_server_error_exception_response():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/server-error")
    assert response.status_code == 500
    assert response.json() == {"exception": "server-error"}


sub = APIRouter()
nested = APIRouter()


class CustomError(ValueError):
    pass


class AnotherError(ValueError):
    pass


@app.exception_handler(ValueError)
def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"message": "ValueError"})


@sub.exception_handler(CustomError)
def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(status_code=400, content={"message": "CustomError"})


@nested.exception_handler(AnotherError)
def another_error_handler(request: Request, exc: AnotherError):
    return JSONResponse(status_code=400, content={"message": "AnotherError"})


@app.get("/app/value-error")
def app_value_error():
    raise ValueError()


@sub.get("/sub/value-error")
def sub_value_error():
    raise ValueError()


@nested.get("/nested/value-error")
def nested_value_error():
    raise ValueError()


@app.get("/app/custom-error")
def app_custom_error():
    raise CustomError()


@sub.get("/sub/custom-error")
def sub_custom_error():
    raise CustomError()


@nested.get("/nested/custom-error")
def nested_custom_error():
    raise CustomError()


@app.get("/app/another-error")
def app_another_error():
    raise AnotherError()


@sub.get("/sub/another-error")
def sub_another_error():
    raise AnotherError()


@nested.get("/nested/another-error")
def nested_another_error():
    raise AnotherError()


# Routing and soexception handlers are not lazy
# router inclusion mest happens after routes
# and error handlers declaration
sub.include_router(nested)
app.include_router(sub)


@pytest.fixture(params=("app", "sub", "nested"))
def prefix(request: pytest.FixtureRequest) -> str:
    return request.param


def test_app_exception_handler(prefix):
    response = client.get(f"/{prefix}/value-error")
    assert response.status_code == 400
    assert response.json() == {"message": "ValueError"}


def test_apirouter_exception_handler(prefix):
    response = client.get(f"/{prefix}/custom-error")
    assert response.status_code == 400
    assert response.json() == {"message": "CustomError"}


def test_nested_apirouter_exception_handler(prefix):
    response = client.get(f"/{prefix}/another-error")
    assert response.status_code == 400
    assert response.json() == {"message": "AnotherError"}
