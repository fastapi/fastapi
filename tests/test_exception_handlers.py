import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse


class CustomException1(HTTPException):
    pass


class CustomException2(HTTPException):
    pass


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


def raise_value_error():
    raise ValueError()


def dependency_with_yield():
    yield raise_value_error()


@app.get("/dependency-with-yield", dependencies=[Depends(dependency_with_yield)])
def with_yield(): ...


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


def test_traceback_for_dependency_with_yield():
    client = TestClient(app, raise_server_exceptions=True)
    with pytest.raises(ValueError) as exc_info:
        client.get("/dependency-with-yield")
    last_frame = exc_info.traceback[-1]
    assert str(last_frame.path) == __file__
    assert last_frame.lineno == raise_value_error.__code__.co_firstlineno


def test_exception_handler_with_single_exception():
    local_app = FastAPI()

    @local_app.exception_handler(CustomException1)
    def custom_exception_handler(request, exception):
        pass  # pragma: no cover

    assert (
        local_app.exception_handlers.get(CustomException1) == custom_exception_handler
    )


@pytest.mark.parametrize(
    "exceptions",
    [
        (CustomException1, CustomException2),  # Tuple of exceptions
        [CustomException1, CustomException2],  # List of exceptions
    ],
)
def test_exception_handler_with_multiple_exceptions(exceptions):
    local_app = FastAPI()

    @local_app.exception_handler(exceptions)
    def custom_exception_handler(request, exception):
        pass  # pragma: no cover

    assert local_app.exception_handlers.get(exceptions[0]) == custom_exception_handler

    assert local_app.exception_handlers.get(exceptions[1]) == custom_exception_handler


def test_exception_handler_with_single_status_code():
    local_app = FastAPI()

    @local_app.exception_handler(409)
    def http_409_status_code_handler(request, exception):
        pass  # pragma: no cover

    assert local_app.exception_handlers.get(409) == http_409_status_code_handler


@pytest.mark.parametrize(
    "status_codes",
    [
        (401, 403),  # Tuple of status codes
        [401, 403],  # List of status codes
    ],
)
def test_exception_handler_with_multiple_status_codes(status_codes):
    local_app = FastAPI()

    @local_app.exception_handler(status_codes)
    def auth_errors_handler(request, exception):
        pass  # pragma: no cover

    assert local_app.exception_handlers.get(status_codes[0]) == auth_errors_handler
    assert local_app.exception_handlers.get(status_codes[1]) == auth_errors_handler
