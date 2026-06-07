from fastapi import Depends, FastAPI, Security
from fastapi.testclient import TestClient

app = FastAPI()

counter_holder = {"counter": 0}


async def dep_counter():
    counter_holder["counter"] += 1
    return counter_holder["counter"]


async def super_dep(count: int = Depends(dep_counter)):
    return count


@app.get("/counter/")
async def get_counter(count: int = Depends(dep_counter)):
    return {"counter": count}


@app.get("/sub-counter/")
async def get_sub_counter(
    subcount: int = Depends(super_dep), count: int = Depends(dep_counter)
):
    return {"counter": count, "subcounter": subcount}


@app.get("/sub-counter-no-cache/")
async def get_sub_counter_no_cache(
    subcount: int = Depends(super_dep),
    count: int = Depends(dep_counter, use_cache=False),
):
    return {"counter": count, "subcounter": subcount}


async def super_dep_no_cache_child(
    count: int = Depends(dep_counter, use_cache=False),
):
    return count


@app.get("/cached-parent-no-cache-child/")
async def get_cached_parent_no_cache_child(
    # The same cached dependency is referenced twice. On the second reference the
    # cached result is reused without re-solving its sub-tree, so its non-cached
    # child (dep_counter) runs only once instead of once per reference.
    first: int = Depends(super_dep_no_cache_child),
    second: int = Depends(super_dep_no_cache_child),
):
    return {"first": first, "second": second}


@app.get("/scope-counter")
async def get_scope_counter(
    count: int = Security(dep_counter),
    scope_count_1: int = Security(dep_counter, scopes=["scope"]),
    scope_count_2: int = Security(dep_counter, scopes=["scope"]),
):
    return {
        "counter": count,
        "scope_counter_1": scope_count_1,
        "scope_counter_2": scope_count_2,
    }


client = TestClient(app)


def test_normal_counter():
    counter_holder["counter"] = 0
    response = client.get("/counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 1}
    response = client.get("/counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 2}


def test_sub_counter():
    counter_holder["counter"] = 0
    response = client.get("/sub-counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 1, "subcounter": 1}
    response = client.get("/sub-counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 2, "subcounter": 2}


def test_sub_counter_no_cache():
    counter_holder["counter"] = 0
    response = client.get("/sub-counter-no-cache/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 2, "subcounter": 1}
    response = client.get("/sub-counter-no-cache/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 4, "subcounter": 3}


def test_cached_parent_does_not_resolve_no_cache_child_twice():
    counter_holder["counter"] = 0
    response = client.get("/cached-parent-no-cache-child/")
    assert response.status_code == 200, response.text
    # The cached parent is solved once; its non-cached child runs only once and
    # the second reference reuses the cached parent value.
    assert response.json() == {"first": 1, "second": 1}
    assert counter_holder["counter"] == 1


def test_security_cache():
    counter_holder["counter"] = 0
    response = client.get("/scope-counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 1, "scope_counter_1": 2, "scope_counter_2": 2}
    response = client.get("/scope-counter/")
    assert response.status_code == 200, response.text
    assert response.json() == {"counter": 3, "scope_counter_1": 4, "scope_counter_2": 4}
