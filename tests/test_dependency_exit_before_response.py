from typing import AsyncGenerator, Generator

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()


expected_response = {"detail": "Something went wrong after"}


class AsyncCallableGenDependency:
    async def __call__(self) -> AsyncGenerator[str, None]:
        yield
        raise HTTPException(status_code=400, detail=expected_response["detail"])


class ExceptionToHandle(Exception):
    pass


class AsyncCallableGenDependencyExceptionHandled:
    async def __call__(self) -> AsyncGenerator[str, None]:
        yield
        raise ExceptionToHandle()


@app.exception_handler(ExceptionToHandle)
async def after_yield_exception_handler(request: Request, exc: ExceptionToHandle):
    return JSONResponse(status_code=200)


class AsyncCallableGenDependencyFailException:
    async def __call__(self) -> AsyncGenerator[str, None]:
        yield
        raise Exception()


class CallableGenDependency:
    def __call__(self) -> Generator[str, None, None]:
        yield
        raise HTTPException(status_code=400, detail=expected_response["detail"])


class CallableGenDependencyFailException:
    def __call__(self) -> Generator[str, None, None]:
        yield
        raise Exception()


async_generator_dependency = AsyncCallableGenDependency()
async_generator_dependency_exception_handled_after = (
    AsyncCallableGenDependencyExceptionHandled()
)
async_generator_dependency_fail = AsyncCallableGenDependencyFailException()
sync_generator_dependency = CallableGenDependency()
sync_generator_dependency_fail = CallableGenDependencyFailException()


@app.get(
    "/async-generator-dependency-fail-late",
    dependencies=[Depends(async_generator_dependency, exit_before_response=True)],
)
async def async_generator_dependency():
    return


@app.get(
    "/async-generator-dependency-fail-late-handled",
    dependencies=[
        Depends(
            async_generator_dependency_exception_handled_after,
            exit_before_response=True,
        )
    ],
)
async def async_generator_dependency_exception_handled():
    return


@app.get(
    "/async-generator-dependency-fail-late-error",
    dependencies=[Depends(async_generator_dependency_fail, exit_before_response=True)],
)
async def async_generator_dependency_error():
    return


@app.get(
    "/sync-generator-dependency-fail-late",
    dependencies=[Depends(sync_generator_dependency, exit_before_response=True)],
)
async def sync_generator_dependency():
    return


@app.get(
    "/sync-generator-dependency-fail-late-error",
    dependencies=[Depends(sync_generator_dependency_fail, exit_before_response=True)],
)
async def sync_generator_dependency():
    return


client = TestClient(app, raise_server_exceptions=False)


@pytest.mark.parametrize(
    "route",
    ["/async-generator-dependency-fail-late", "/sync-generator-dependency-fail-late"],
)
def test_http_exception_before_response(route):
    response = client.get(route)
    assert response.status_code == 400, response.text
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "route",
    [
        "/async-generator-dependency-fail-late-error",
        "/sync-generator-dependency-fail-late-error",
    ],
)
def test_fail_before_response(route):
    response = client.get(route)
    assert response.status_code == 500


@pytest.mark.parametrize(
    "route",
    ["/async-generator-dependency-fail-late-handled"],
)
def test_fail_before_response_and_handled_after(route):
    response = client.get(route)
    assert response.status_code == 200
