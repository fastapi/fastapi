import asyncio
import time
import warnings
from contextlib import AsyncExitStack
from typing import Dict, List, Optional

import pytest
from fastapi import Depends, FastAPI
from fastapi.dependencies.utils import (
    get_dependant,
    silence_future_exception,
    solve_dependencies,
)
from fastapi.testclient import TestClient
from starlette.requests import Request

PAR_LOW, PAR_HIGH = 0.08, 0.25
SEQPAR_LOW, SEQPAR_HIGH = 0.18, 0.35
OVERLAP_EPS = 0.05


def assert_duration_between(value: float, low: float, high: float) -> None:
    assert low <= value <= high, f"duration {value:.4f} not in [{low:.2f}, {high:.2f}]"


def assert_duration_with_sequential_and_parallel_deps(value: float) -> None:
    assert_duration_between(value, SEQPAR_LOW, SEQPAR_HIGH)


def assert_duration_with_parallel_deps(value: float) -> None:
    assert_duration_between(value, PAR_LOW, PAR_HIGH)


def get(client: TestClient, path: str):
    start = time.perf_counter()
    r = client.get(path)
    return r, time.perf_counter() - start


def new_timings() -> dict:
    return {}


def t_start(ts: dict, key: str) -> None:
    ts.setdefault(key, {})["start"] = time.perf_counter()


def t_end(ts: dict, key: str) -> None:
    ts[key]["end"] = time.perf_counter()


def assert_overlaps(
    ts: dict, a: str, b: str, *, min_overlap: float = OVERLAP_EPS
) -> None:
    overlap = min(ts[a]["end"], ts[b]["end"]) - max(ts[a]["start"], ts[b]["start"])
    assert overlap > min_overlap, (
        f"no sufficient overlap between {a} and {b}: {overlap:.4f}s"
    )


def make_async_timed_dep(
    ts: dict,
    key: str,
    *,
    delay: float = 0.1,
    value: int = 1,
    order: Optional[List[str]] = None,
):
    async def dep():
        t_start(ts, key)
        await asyncio.sleep(delay)
        t_end(ts, key)
        if order is not None:
            order.append(key)
        return value

    return dep


def make_sync_timed_dep(ts: dict, key: str, *, delay: float = 0.1, value: int = 1):
    def dep():
        t_start(ts, key)
        time.sleep(delay)
        t_end(ts, key)
        return value

    return dep


def make_security_counter_dep(
    calls: Dict, ts: Optional[Dict] = None, key_factory=None, *, delay: float = 0.1
):
    counter = {"i": 0}

    async def dep():
        calls["n"] += 1
        cur = calls["n"]
        k = None
        if ts is not None:
            counter["i"] += 1
            k = key_factory(counter["i"]) if key_factory else f"call{counter['i']}"
            t_start(ts, k)
        await asyncio.sleep(delay)
        if ts is not None and k is not None:
            t_end(ts, k)
        return cur

    return dep


def test_global_parallel_opt_in_with_per_dep_opt_out():
    app = FastAPI(depends_default_parallelizable=True)

    order = []
    ts = new_timings()

    async def seq_dep():
        await asyncio.sleep(0.1)
        order.append("seq")
        return 1

    par1 = make_async_timed_dep(ts, "p1", order=order)
    par2 = make_async_timed_dep(ts, "p2", order=order)

    @app.get("/measure1")
    async def measure(
        _: int = Depends(seq_dep, parallelizable=False),
        __: int = Depends(par1),
        ___: int = Depends(par2),
    ):
        return {"ok": True}

    client = TestClient(app)

    r, elapsed = get(client, "/measure1")

    assert r.status_code == 200
    assert_duration_with_sequential_and_parallel_deps(elapsed)
    assert_overlaps(ts, "p1", "p2")
    assert set(order) == {"seq", "p1", "p2"}


def test_global_default_false_with_per_dep_enable_parallel():
    app = FastAPI(depends_default_parallelizable=False)

    order = []
    ts = new_timings()

    async def seq_dep():
        await asyncio.sleep(0.1)
        order.append("seq")
        return 1

    par1 = make_async_timed_dep(ts, "p1", order=order)
    par2 = make_async_timed_dep(ts, "p2", order=order)

    @app.get("/measure2")
    async def measure(
        _: int = Depends(seq_dep),  # uses app default (False) -> sequential
        __: int = Depends(par1, parallelizable=True),
        ___: int = Depends(par2, parallelizable=True),
    ):
        return {"ok": True}

    client = TestClient(app)

    r, elapsed = get(client, "/measure2")

    assert r.status_code == 200
    assert_duration_with_sequential_and_parallel_deps(elapsed)
    assert_overlaps(ts, "p1", "p2")
    assert set(order) == {"seq", "p1", "p2"}


def test_parallel_cache_only_called_once():
    app = FastAPI(depends_default_parallelizable=True)

    call_count = {"n": 0}

    async def shared():
        call_count["n"] += 1
        await asyncio.sleep(0.1)
        return call_count["n"]

    @app.get("/cache")
    async def measure(a: int = Depends(shared), b: int = Depends(shared)):
        return {"a": a, "b": b, "calls": call_count["n"]}

    client = TestClient(app)

    r, elapsed = get(client, "/cache")

    assert r.status_code == 200
    data = r.json()
    assert data["a"] == data["b"] == 1
    assert data["calls"] == 1
    assert_duration_with_parallel_deps(elapsed)


def test_parallel_exception_silences_future_warning_and_raises_once():
    app = FastAPI(depends_default_parallelizable=True)

    class BoomError(RuntimeError):
        pass

    async def failing():
        await asyncio.sleep(0.01)
        raise BoomError("boom")

    @app.get("/fail1")
    async def fail_endpoint(a: int = Depends(failing), b: int = Depends(failing)):
        return {"ok": True}  # pragma: no cover

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        with pytest.raises(BoomError):
            client.get("/fail1")
        messages = [str(x.message) for x in w]
    assert not any("Future exception was never retrieved" in m for m in messages)


def test_dependency_overrides_preserve_parallelizable():
    app = FastAPI(depends_default_parallelizable=False)

    async def original():
        await asyncio.sleep(0.1)  # pragma: no cover
        return "original"  # pragma: no cover

    async def override():
        await asyncio.sleep(0.1)
        return "override"

    @app.get("/override")
    async def ep(
        x: str = Depends(original, parallelizable=True),
        y: str = Depends(original, parallelizable=True),
    ):
        return {"x": x, "y": y}

    app.dependency_overrides[original] = override
    client = TestClient(app)

    r, elapsed = get(client, "/override")

    assert r.status_code == 200
    assert r.json() == {"x": "override", "y": "override"}
    assert_duration_with_parallel_deps(elapsed)


def test_security_parallel_and_cache_same_scope():
    from fastapi import Security

    app = FastAPI(depends_default_parallelizable=True)
    calls = {"n": 0}
    ts = new_timings()

    sec_dep = make_security_counter_dep(calls, ts)

    @app.get("/sec-same")
    async def ep(
        a: int = Security(sec_dep, scopes=["s1"]),
        b: int = Security(sec_dep, scopes=["s1"]),
    ):
        return {"a": a, "b": b, "calls": calls["n"]}

    client = TestClient(app)
    r, elapsed = get(client, "/sec-same")

    assert r.status_code == 200
    data = r.json()
    assert data["a"] == data["b"]
    assert data["calls"] == 1
    assert_duration_with_parallel_deps(elapsed)


def test_security_parallel_and_no_cache_diff_scope():
    from fastapi import Security

    app = FastAPI(depends_default_parallelizable=True)
    calls = {"n": 0}
    ts = new_timings()

    sec_dep = make_security_counter_dep(calls, ts, key_factory=lambda i: f"call{i}")

    @app.get("/sec-diff")
    async def ep(
        a: int = Security(sec_dep, scopes=["s1"]),
        b: int = Security(sec_dep, scopes=["s2"]),
    ):
        return {"a": a, "b": b, "calls": calls["n"]}

    client = TestClient(app)
    r, elapsed = get(client, "/sec-diff")

    assert r.status_code == 200
    data = r.json()
    assert data["a"] != data["b"]
    assert data["calls"] == 2
    assert_overlaps(ts, "call1", "call2")


def test_security_per_dep_enable_with_global_false():
    from fastapi import Security

    app = FastAPI(depends_default_parallelizable=False)

    ts = new_timings()

    sec_dep = make_security_counter_dep({"n": 0}, ts)

    @app.get("/sec-per-dep")
    async def ep(
        a: int = Security(sec_dep, parallelizable=True),
        b: int = Security(sec_dep, parallelizable=True),
    ):
        return {"ok": True}

    client = TestClient(app)
    r, elapsed = get(client, "/sec-per-dep")
    assert r.status_code == 200
    assert_duration_with_parallel_deps(elapsed)


def test_generator_dep_forces_sequential_even_if_parallelizable():
    app = FastAPI(depends_default_parallelizable=True)

    async def gen_dep():
        await asyncio.sleep(0.1)
        try:
            yield 1
        finally:
            pass

    async def par():
        await asyncio.sleep(0.1)
        return 2

    @app.get("/gen-seq")
    async def ep(a: int = Depends(gen_dep, parallelizable=True), b: int = Depends(par)):
        return {"ok": True}

    client = TestClient(app)
    r, elapsed = get(client, "/gen-seq")
    assert r.status_code == 200
    assert_duration_with_sequential_and_parallel_deps(elapsed)


def test_context_sensitivity_bubbles_up_from_subdeps():
    app = FastAPI(depends_default_parallelizable=True)

    async def gen_dep():
        await asyncio.sleep(0.1)
        try:
            yield 1
        finally:
            pass

    async def a_dep(_: int = Depends(gen_dep)):
        return 10

    async def par():
        await asyncio.sleep(0.1)
        return 2

    @app.get("/bubble")
    async def ep(a: int = Depends(a_dep, parallelizable=True), b: int = Depends(par)):
        return {"ok": True}

    client = TestClient(app)
    r, elapsed = get(client, "/bubble")
    assert r.status_code == 200
    assert_duration_with_sequential_and_parallel_deps(elapsed)


def test_background_tasks_created_and_parallel_siblings():
    from starlette.background import BackgroundTasks

    app = FastAPI(depends_default_parallelizable=True)

    flag = {"ran": False}

    def bg():
        flag["ran"] = True

    async def needs_bg(tasks: BackgroundTasks):
        tasks.add_task(bg)
        return 1

    async def par():
        await asyncio.sleep(0.1)
        return 2

    @app.get("/bg")
    async def ep(_: int = Depends(needs_bg), __: int = Depends(par)):
        return {"ok": True}

    client = TestClient(app)
    r, elapsed = get(client, "/bg")
    assert r.status_code == 200
    assert_duration_with_parallel_deps(elapsed)
    time.sleep(0.02)
    assert flag["ran"] is True


def test_exception_order_sequential_then_parallel():
    app = FastAPI(depends_default_parallelizable=True)

    class SeqErr(RuntimeError):
        pass

    class ParErr(RuntimeError):
        pass

    async def fail_seq():
        raise SeqErr("seq first")

    async def fail_par():
        await asyncio.sleep(0.01)
        raise ParErr("par later")

    @app.get("/ex-order-a")
    async def ep(_: int = Depends(fail_seq), __: int = Depends(fail_par)):
        return {"ok": True}  # pragma: no cover

    client = TestClient(app)
    with pytest.raises(SeqErr):
        client.get("/ex-order-a")


def test_exception_order_with_parallel_siblings():
    app = FastAPI(depends_default_parallelizable=True)

    class AErr(RuntimeError):
        pass

    class BErr(RuntimeError):
        pass

    async def fail_a():
        await asyncio.sleep(0.01)
        raise AErr("a")

    async def fail_b():
        await asyncio.sleep(0.01)
        raise BErr("b")

    @app.get("/ex-order-b")
    async def ep(_: int = Depends(fail_a), __: int = Depends(fail_b)):
        return {"ok": True}  # pragma: no cover

    client = TestClient(app)
    with pytest.raises(AErr):
        client.get("/ex-order-b")


def test_threadpool_parallelization_for_sync_functions():
    app = FastAPI(depends_default_parallelizable=True)

    ts = new_timings()

    s1 = make_sync_timed_dep(ts, "s1")
    s2 = make_sync_timed_dep(ts, "s2")

    @app.get("/sync")
    def ep(_: int = Depends(s1), __: int = Depends(s2)):
        return {"ok": True}

    client = TestClient(app)
    r, elapsed = get(client, "/sync")
    assert r.status_code == 200
    assert_duration_with_parallel_deps(elapsed)
    assert_overlaps(ts, "s1", "s2")


def test_security_scopes_cache_key_multiple():
    from fastapi import Security

    app = FastAPI(depends_default_parallelizable=True)
    calls = {"n": 0}
    ts = new_timings()

    sec_dep = make_security_counter_dep(calls, ts, key_factory=lambda i: f"call{i}")

    @app.get("/sec-multi")
    async def ep(
        a: int = Security(sec_dep, scopes=["a"]),
        b: int = Security(sec_dep, scopes=["a"]),
        c: int = Security(sec_dep, scopes=["b"]),
    ):
        return {"a": a, "b": b, "c": c, "calls": calls["n"]}

    client = TestClient(app)
    r, elapsed = get(client, "/sec-multi")
    assert r.status_code == 200
    data = r.json()
    assert data["a"] == data["b"]
    assert data["c"] != data["a"]
    assert data["calls"] == 2
    assert_overlaps(ts, "call1", "call2")


def test_cached_value_converted_to_future_and_awaited():
    app = FastAPI()

    async def low() -> int:
        return 999  # pragma: no cover

    async def wrapper(x: int = Depends(low)) -> int:
        return x  # pragma: no cover

    @app.get("/cov")
    async def cov(request: Request):
        async with AsyncExitStack() as astack:
            dep = get_dependant(path="/cov", call=wrapper)
            # Pre-populate cache with a non-Future raw value
            dependency_cache = {(low, ()): 777}
            solved = await solve_dependencies(
                request=request,
                dependant=dep,
                dependency_cache=dependency_cache,
                async_exit_stack=astack,
                embed_body_fields=False,
            )
            return {"x": solved.values["x"]}

    client = TestClient(app)
    r = client.get("/cov")
    assert r.status_code == 200
    assert r.json() == {"x": 777}


def test_silence_future_exception_handles_exception_path() -> None:
    class Dummy:
        def exception(self):
            raise Exception("boom")

    silence_future_exception(Dummy())
