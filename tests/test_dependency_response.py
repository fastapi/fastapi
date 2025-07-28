from typing import AsyncGenerator, Generator

from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI()


def dependency_gen(value: str) -> Generator[str, None, None]:
    response: Response = yield
    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.body == b'"response_get_dependency_gen"'
    response.headers["X-Test"] = value


async def dependency_async_gen(value: str) -> AsyncGenerator[str, None]:
    response = yield
    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.body == b'"response_get_dependency_async_gen"'
    response.headers["X-Test"] = value


async def sub_dependency_async_gen(value: str) -> AsyncGenerator[str, None]:
    response = yield
    assert isinstance(response, Response)
    response.status_code = 201
    assert response.body == b'"response_get_sub_dependency_async_gen"'
    response.headers["X-Test"] = value


async def parent_dependency(result=Depends(sub_dependency_async_gen)):
    return result


@app.get("/dependency-gen", dependencies=[Depends(dependency_gen)])
async def get_dependency_gen():
    return "response_get_dependency_gen"


@app.get("/dependency-async-gen", dependencies=[Depends(dependency_async_gen)])
async def get_dependency_async_gen():
    return "response_get_dependency_async_gen"


@app.get("/sub-dependency-gen", dependencies=[Depends(parent_dependency)])
async def get_sub_dependency_gen():
    return "response_get_sub_dependency_async_gen"


client = TestClient(app)


def test_dependency_gen():
    response = client.get("/dependency-gen", params={"value": "test"})
    assert response.status_code == 200
    assert response.content == b'"response_get_dependency_gen"'
    assert response.headers["X-Test"] == "test"


def test_dependency_async_gen():
    response = client.get("/dependency-async-gen", params={"value": "test"})
    assert response.status_code == 200
    assert response.content == b'"response_get_dependency_async_gen"'
    assert response.headers["X-Test"] == "test"


def test_sub_dependency_gen():
    response = client.get("/sub-dependency-gen", params={"value": "test"})
    assert response.status_code == 201
    assert response.content == b'"response_get_sub_dependency_async_gen"'
    assert response.headers["X-Test"] == "test"
