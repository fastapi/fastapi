import pytest
from fastapi import Depends, FastAPI
from starlette.testclient import TestClient

app = FastAPI()


class CallableDependency:
    def __call__(self, value: str) -> str:
        return value


class AsyncCallableDependency:
    async def __call__(self, value: str) -> str:
        return value


class MethodsDependency:
    def synchronous(self, value: str) -> str:
        return value

    async def asynchronous(self, value: str) -> str:
        return value


callable_dependency = CallableDependency()
async_callable_dependency = AsyncCallableDependency()
methods_dependency = MethodsDependency()


@app.get("/callable-dependency")
async def get_callable_dependency(value: str = Depends(callable_dependency)):
    return value


@app.get("/async-callable-dependency")
async def get_callable_dependency(value: str = Depends(async_callable_dependency)):
    return value


@app.get("/synchronous-method-dependency")
async def get_synchronous_method_dependency(
    value: str = Depends(methods_dependency.synchronous),
):
    return value


@app.get("/asynchronous-method-dependency")
async def get_asynchronous_method_dependency(
    value: str = Depends(methods_dependency.asynchronous),
):
    return value


client = TestClient(app)


@pytest.mark.parametrize(
    "route,value",
    [
        ("/callable-dependency", "callable-dependency"),
        ("/async-callable-dependency", "async-callable-dependency"),
        ("/synchronous-method-dependency", "synchronous-method-dependency"),
        ("/asynchronous-method-dependency", "asynchronous-method-dependency"),
    ],
)
def test_class_dependency(route, value):
    response = client.get(route, params={"value": value})
    assert response.status_code == 200
    assert response.json() == value
