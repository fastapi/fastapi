import pytest
from fastapi import FastAPI, HTTPException
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
