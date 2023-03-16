import timeit
import unittest.mock

import fastapi.dependencies.utils
import pytest
from fastapi import Depends, FastAPI, Request, Security
from fastapi.dependencies.utils import get_dependant, solve_dependencies
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


app = FastAPI()

counter_holder = {"counter": 0}


async def dep_counter():
    counter_holder["counter"] += 1
    return counter_holder["counter"]


# a deep and broad dependency hierarchy:
async def dep_a(count: int = Depends(dep_counter)):
    return {"a": count}


async def dep_b(count: int = Depends(dep_counter)):
    return {"b": count}


async def dep_c(count: int = Depends(dep_counter)):
    return {"b": count}


async def dep_aa(
    a: dict = Depends(dep_a), b: dict = Depends(dep_b), c: dict = Depends(dep_c)
):
    result = {}
    result.update(a)
    result.update(b)
    result.update(c)
    return {"aa": result}


async def dep_bb(
    a: dict = Depends(dep_a), b: dict = Depends(dep_b), c: dict = Depends(dep_c)
):
    result = {}
    result.update(a)
    result.update(b)
    result.update(c)
    return {"bb": result}


async def dep_cc(
    a: dict = Depends(dep_a), b: dict = Depends(dep_b), c: dict = Depends(dep_c)
):
    result = {}
    result.update(a)
    result.update(b)
    result.update(c)
    return {"cc": result}


@app.get("/depend-cache-deep")
async def get_depend_cache_deep(
    aa: dict = Depends(dep_aa),
    bb: dict = Depends(dep_bb),
    cc: dict = Depends(dep_cc),
    count: int = Security(dep_counter),
    scope_count_1: int = Security(dep_counter, scopes=["scope"]),
    scope_count_2: int = Security(dep_counter, scopes=["scope"]),
):
    return {
        "aa": aa,
        "bb": bb,
        "cc": cc,
        "scope_counter_1": scope_count_1,
        "scope_counter_2": scope_count_2,
    }


@app.get("/depend_cache_request")
async def get_depend_cache_request(request: Request):
    """
    A simple endpoint with only a basic non-field params
    """
    return {}


aclient = AsyncClient(app=app, base_url="http://")


async def test_deep_cache(capsys):
    counter_holder["counter"] = 0
    my_counter = 0

    async def wrapper(*args, **kwargs):
        nonlocal my_counter
        my_counter += 1
        return await solve_dependencies(*args, **kwargs)

    with unittest.mock.patch("fastapi.dependencies.utils.solve_dependencies", wrapper):
        response = await aclient.get("/depend-cache-deep")
    assert response.json() == {
        "aa": {"aa": {"a": 1, "b": 1}},
        "bb": {"bb": {"a": 1, "b": 1}},
        "cc": {"cc": {"a": 1, "b": 1}},
        "scope_counter_1": 2,
        "scope_counter_2": 2,
    }
    assert my_counter == 8


async def test_deep_cache_perf(capsys):
    """
    A test that can be used to test the performace of the dependency cache
    """
    await aclient.get("/depend_cache_request")
    # Enable the below to output performance information
    if False:  # pragma: no cover
        counter_holder["counter"] = 0
        with capsys.disabled():
            time_call(
                lambda: async2sync(aclient.get, "/depend-cache-deep"),
                "deep cache client requests",
            )

            call = get_endpoint_call(get_depend_cache_deep)
            time_call(lambda: async2sync(call), "deep cache direct solve")

            call = get_endpoint_call(get_depend_cache_request)
            time_call(lambda: async2sync(call), "request direct solve")


def get_endpoint_call(call, path="/foo"):  # pragma: no cover
    # create a dependency and call it directly
    dep = get_dependant(path="/foo", call=call)
    if hasattr(fastapi.dependencies.utils, "DependencySolverContext"):
        Context = fastapi.dependencies.utils.DependencySolverContext

        async def solve():
            request = Request(scope={"type": "http"})
            ctx = Context(request=request)
            return await solve_dependencies(context=ctx, dependant=dep)

    else:

        async def solve():
            request = Request(scope={"type": "http", "query_string": "", "headers": []})
            return await solve_dependencies(request=request, dependant=dep)

    return solve


def time_call(call, what):  # pragma: no cover
    timer = timeit.Timer(call)
    n, t = timer.autorange()
    tpr = t / n
    rps = n / t
    print(what)
    print(f"did {n} calls in {t} seconds")
    print(f"time per call: {tpr*1000:.2f}ms, rate: {rps:.2f}/s")


def async2sync(call, *args):  # pragma: no cover
    """
    Call an async function and manually 'await' it without an eventloop.
    Useful if we know the method doesn't block, e.g. for timing.
    """
    awaitable = call(*args)
    try:
        awaitable.send(None)
    except StopIteration:
        pass
