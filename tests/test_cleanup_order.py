"""Regression tests for deterministic dependency-cleanup ordering (Task 2).

Testing technique: every yield dep appends its own name to a closure-local list
*after* its yield (i.e. during cleanup).  BackgroundTasks do the same.  After
the HTTP round-trip completes the test inspects the list to assert ordering.

The expected ordering is derived from the invariant documented in
``fastapi/routing.py`` (request_response) and
``fastapi/dependencies/utils.py`` (solve_dependencies):

  • Deps are pushed onto AsyncExitStack in dependant.dependencies iteration
    order (route-level deps first, then signature deps left-to-right).
  • Sub-deps of a dep are recursed *before* the parent is pushed.
  • AsyncExitStack is LIFO → last-pushed finaliser runs first.
  • function_stack exits BEFORE ``await response(…)``.
  • BackgroundTasks run *inside* ``response(…)``.
  • request_stack (inner_astack) exits AFTER ``response(…)``.
"""

import json
import logging
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# test_sibling_cleanup_is_lifo
# ---------------------------------------------------------------------------


def test_sibling_cleanup_is_lifo() -> None:
    """Two yield deps declared as (dep_a, dep_b) in the signature.
    dep_a is pushed first, dep_b second.  LIFO → dep_b cleans up first."""
    cleanup_order: list[str] = []

    def dep_a():  # type: ignore[no-untyped-def]
        yield "a"
        cleanup_order.append("dep_a")

    def dep_b():  # type: ignore[no-untyped-def]
        yield "b"
        cleanup_order.append("dep_b")

    app = FastAPI()

    @app.get("/")
    def endpoint(
        _a: Annotated[str, Depends(dep_a)],
        _b: Annotated[str, Depends(dep_b)],
    ) -> dict:
        return {"ok": True}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert cleanup_order == ["dep_b", "dep_a"]


# ---------------------------------------------------------------------------
# test_route_level_dep_cleanup_after_signature_deps
# ---------------------------------------------------------------------------


def test_route_level_dep_cleanup_after_signature_deps() -> None:
    """Route-level dep is prepended (pushed first) → cleaned up last."""
    cleanup_order: list[str] = []

    def route_dep():  # type: ignore[no-untyped-def]
        yield
        cleanup_order.append("route_dep")

    def sig_dep():  # type: ignore[no-untyped-def]
        yield
        cleanup_order.append("sig_dep")

    app = FastAPI()

    @app.get("/", dependencies=[Depends(route_dep)])
    def endpoint(_s: Annotated[None, Depends(sig_dep)]) -> dict:
        return {"ok": True}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    # sig_dep pushed after route_dep → exits first (LIFO)
    assert cleanup_order == ["sig_dep", "route_dep"]


# ---------------------------------------------------------------------------
# test_nested_dep_cleanup_order
# ---------------------------------------------------------------------------


def test_nested_dep_cleanup_order() -> None:
    """endpoint → dep_a (yield) → dep_b (yield).
    dep_b is recursed first (pushed first).  dep_a is pushed second.
    LIFO: dep_a cleans up first, then dep_b."""
    cleanup_order: list[str] = []

    def dep_b():  # type: ignore[no-untyped-def]
        yield "b"
        cleanup_order.append("dep_b")

    def dep_a(b: Annotated[str, Depends(dep_b)]):  # type: ignore[no-untyped-def]
        yield "a"
        cleanup_order.append("dep_a")

    app = FastAPI()

    @app.get("/")
    def endpoint(_a: Annotated[str, Depends(dep_a)]) -> dict:
        return {"ok": True}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert cleanup_order == ["dep_a", "dep_b"]


# ---------------------------------------------------------------------------
# test_async_and_sync_generators_share_lifo
# ---------------------------------------------------------------------------


def test_async_and_sync_generators_share_lifo() -> None:
    """A sync yield dep and an async yield dep, in that signature order.
    Both land on the same stack via enter_async_context; ordering is purely
    push order → async one (pushed second) exits first."""
    cleanup_order: list[str] = []

    def dep_sync():  # type: ignore[no-untyped-def]
        yield "sync"
        cleanup_order.append("dep_sync")

    async def dep_async():  # type: ignore[no-untyped-def]
        yield "async"
        cleanup_order.append("dep_async")

    app = FastAPI()

    @app.get("/")
    def endpoint(
        _s: Annotated[str, Depends(dep_sync)],
        _a: Annotated[str, Depends(dep_async)],
    ) -> dict:
        return {"ok": True}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert cleanup_order == ["dep_async", "dep_sync"]


# ---------------------------------------------------------------------------
# test_cleanup_runs_on_endpoint_exception
# ---------------------------------------------------------------------------


def test_cleanup_runs_on_endpoint_exception() -> None:
    """All yield-dep finalisers still run even when the endpoint raises."""
    cleanup_order: list[str] = []

    def dep_a():  # type: ignore[no-untyped-def]
        try:
            yield "a"
        finally:
            cleanup_order.append("dep_a")

    def dep_b():  # type: ignore[no-untyped-def]
        try:
            yield "b"
        finally:
            cleanup_order.append("dep_b")

    app = FastAPI()

    @app.get("/")
    def endpoint(
        _a: Annotated[str, Depends(dep_a)],
        _b: Annotated[str, Depends(dep_b)],
    ) -> dict:
        raise RuntimeError("endpoint boom")

    # raise_server_exceptions=False so the 500 doesn't propagate into the test
    with TestClient(app, raise_server_exceptions=False) as client:
        resp = client.get("/")
    assert resp.status_code == 500
    # Both deps cleaned up, in LIFO order
    assert cleanup_order == ["dep_b", "dep_a"]


# ---------------------------------------------------------------------------
# test_function_scope_cleans_before_response_streaming
# ---------------------------------------------------------------------------


def test_function_scope_cleans_before_response_streaming() -> None:
    """A function-scoped yield dep's finaliser runs *before* the response
    body is streamed.  The streaming iterator can observe the side-effect."""
    flag: dict[str, bool] = {"cleaned": False}

    def func_dep():  # type: ignore[no-untyped-def]
        yield
        flag["cleaned"] = True

    app = FastAPI()

    @app.get("/stream")
    def stream_endpoint(_: Annotated[None, Depends(func_dep, scope="function")]) -> StreamingResponse:  # type: ignore[no-untyped-def]
        def body():  # type: ignore[no-untyped-def]
            # By the time this runs, function_stack has already exited
            yield json.dumps({"cleaned": flag["cleaned"]})

        return StreamingResponse(body(), media_type="application/json")

    with TestClient(app) as client:
        resp = client.get("/stream")
    assert resp.status_code == 200
    assert resp.json()["cleaned"] is True


# ---------------------------------------------------------------------------
# test_request_scope_cleans_after_response_streaming
# ---------------------------------------------------------------------------


def test_request_scope_cleans_after_response_streaming() -> None:
    """A request-scoped (default) yield dep's finaliser runs *after* the
    response body is streamed.  The streaming iterator sees the flag as False."""
    flag: dict[str, bool] = {"cleaned": False}

    def req_dep():  # type: ignore[no-untyped-def]
        yield
        flag["cleaned"] = True

    app = FastAPI()

    @app.get("/stream")
    def stream_endpoint(_: Annotated[None, Depends(req_dep)]) -> StreamingResponse:  # type: ignore[no-untyped-def]
        def body():  # type: ignore[no-untyped-def]
            # request_stack has NOT exited yet while the stream runs
            yield json.dumps({"cleaned": flag["cleaned"]})

        return StreamingResponse(body(), media_type="application/json")

    with TestClient(app) as client:
        resp = client.get("/stream")
    assert resp.status_code == 200
    assert resp.json()["cleaned"] is False


# ---------------------------------------------------------------------------
# test_background_task_runs_between_scopes
# ---------------------------------------------------------------------------


def test_background_task_runs_between_scopes() -> None:
    """The three phases interleave in exactly this order:
      1. function-scoped finalisers   (function_stack exits)
      2. BackgroundTasks              (inside response.__call__)
      3. request-scoped finalisers    (request_stack exits)
    """
    cleanup_order: list[str] = []

    def func_dep():  # type: ignore[no-untyped-def]
        yield
        cleanup_order.append("func_cleanup")

    def req_dep():  # type: ignore[no-untyped-def]
        yield
        cleanup_order.append("req_cleanup")

    app = FastAPI()

    @app.get("/")
    def endpoint(
        _f: Annotated[None, Depends(func_dep, scope="function")],
        _r: Annotated[None, Depends(req_dep, scope="request")],
        bg: BackgroundTasks,
    ) -> dict:
        bg.add_task(lambda: cleanup_order.append("bg_task"))
        return {"ok": True}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert cleanup_order == ["func_cleanup", "bg_task", "req_cleanup"]


# ---------------------------------------------------------------------------
# test_cleanup_order_metadata_populated
# ---------------------------------------------------------------------------


def test_cleanup_order_metadata_populated() -> None:
    """scope["fastapi_dependency_cleanup_order"] is populated with one entry
    per generator dep that was successfully pushed onto a stack."""
    captured: list[list[dict]] = []  # type: ignore[type-arg]

    async def capture(request: Request):  # type: ignore[no-untyped-def]
        yield
        # By the time this finaliser runs, all pushes have been recorded.
        captured.append(
            list(request.scope.get("fastapi_dependency_cleanup_order", []))
        )

    def dep_a():  # type: ignore[no-untyped-def]
        yield "a"

    def dep_b():  # type: ignore[no-untyped-def]
        yield "b"

    app = FastAPI(dependency_debug_url="/_debug/deps")

    @app.get("/")
    def endpoint(
        _cap: Annotated[None, Depends(capture)],
        _a: Annotated[str, Depends(dep_a)],
        _b: Annotated[str, Depends(dep_b)],
    ) -> dict:
        return {"ok": True}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200

    assert len(captured) == 1
    metadata = captured[0]

    # Three generators were pushed: capture, dep_a, dep_b
    assert len(metadata) == 3

    # Order indices are monotonically increasing from 0
    assert [m["order"] for m in metadata] == [0, 1, 2]

    # Names match push order (signature order)
    assert metadata[0]["callable_name"] == "capture"
    assert metadata[1]["callable_name"] == "dep_a"
    assert metadata[2]["callable_name"] == "dep_b"

    # All are request-scoped (no explicit scope on generators → default "request")
    for m in metadata:
        assert m["scope"] == "request"


# ---------------------------------------------------------------------------
# test_cleanup_order_metadata_survives_exception
# ---------------------------------------------------------------------------


def test_cleanup_order_metadata_survives_exception() -> None:
    """If a generator dep raises *before* its yield (setup failure), it is
    never pushed onto the stack and therefore never recorded.  Deps that were
    successfully pushed before it still appear in the metadata."""
    captured: list[list[dict]] = []  # type: ignore[type-arg]

    async def capture(request: Request):  # type: ignore[no-untyped-def]
        try:
            yield
        finally:
            captured.append(
                list(request.scope.get("fastapi_dependency_cleanup_order", []))
            )

    def dep_ok():  # type: ignore[no-untyped-def]
        yield "ok"

    def dep_raises():  # type: ignore[no-untyped-def]
        raise ValueError("setup failure")
        yield "never"  # pragma: no cover  # noqa: RET503

    app = FastAPI(dependency_debug_url="/_debug/deps")

    @app.get("/")
    def endpoint(
        _cap: Annotated[None, Depends(capture)],
        _ok: Annotated[str, Depends(dep_ok)],
        _bad: Annotated[str, Depends(dep_raises)],
    ) -> dict:
        return {"ok": True}  # pragma: no cover

    with TestClient(app, raise_server_exceptions=False) as client:
        resp = client.get("/")
    # The ValueError propagates → 500
    assert resp.status_code == 500

    # capture and dep_ok were pushed; dep_raises was not
    assert len(captured) == 1
    metadata = captured[0]
    assert len(metadata) == 2
    names = [m["callable_name"] for m in metadata]
    assert "capture" in names
    assert "dep_ok" in names
    assert "dep_raises" not in names


# ---------------------------------------------------------------------------
# test_use_cache_false_shared_dep_cleanup_runs_per_encounter
# ---------------------------------------------------------------------------


def test_use_cache_false_shared_dep_cleanup_runs_per_encounter() -> None:
    """use_cache=False on a shared yield dep bypasses the cache check
    (utils.py:674) on every encounter.  Each encounter calls
    enter_async_context independently → one push per encounter, one
    finaliser per push.  The two finalisers are NOT adjacent in the LIFO
    sequence; they are interleaved with the branch deps that triggered them.

    Expected full event sequence (setup + cleanup):
      shared:setup  branch_a:setup  shared:setup  branch_b:setup
      branch_b:cleanup  shared:cleanup  branch_a:cleanup  shared:cleanup

    Failure mode guarded: an optimisation that deduplicates
    enter_async_context calls regardless of use_cache would collapse the
    two shared finalisers into one, silently dropping cleanup work."""
    order: list[str] = []

    def shared():  # type: ignore[no-untyped-def]
        order.append("shared:setup")
        yield "s"
        order.append("shared:cleanup")

    def branch_a(s: Annotated[str, Depends(shared, use_cache=False)]):  # type: ignore[no-untyped-def]
        order.append("branch_a:setup")
        yield "a"
        order.append("branch_a:cleanup")

    def branch_b(s: Annotated[str, Depends(shared, use_cache=False)]):  # type: ignore[no-untyped-def]
        order.append("branch_b:setup")
        yield "b"
        order.append("branch_b:cleanup")

    app = FastAPI()

    @app.get("/")
    def endpoint(
        _a: Annotated[str, Depends(branch_a)],
        _b: Annotated[str, Depends(branch_b)],
    ) -> dict:
        return {}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert order == [
        "shared:setup",
        "branch_a:setup",
        "shared:setup",
        "branch_b:setup",
        "branch_b:cleanup",
        "shared:cleanup",
        "branch_a:cleanup",
        "shared:cleanup",
    ]


# ---------------------------------------------------------------------------
# test_background_task_observes_function_scoped_resource_as_invalidated
# ---------------------------------------------------------------------------


def test_background_task_observes_function_scoped_resource_as_invalidated() -> None:
    """function_stack exits before response() is called.  BackgroundTasks
    execute inside response().  A function-scoped dep that invalidates a
    shared mutable resource during its cleanup does so *before* any
    BackgroundTask reads it.

    Expected state seen by BackgroundTask: 'closed'  (not 'open').

    Failure mode guarded: moving ``await response(…)`` inside the
    function_stack async-with block would make function-scoped resources
    still alive during BackgroundTask execution, masking use-after-close
    bugs in production."""
    state: dict[str, str] = {}
    bg_saw: list[str] = []

    def func_dep():  # type: ignore[no-untyped-def]
        state["status"] = "open"
        yield state
        state["status"] = "closed"

    app = FastAPI()

    @app.get("/")
    def endpoint(
        res: Annotated[dict, Depends(func_dep, scope="function")],
        bg: BackgroundTasks,
    ) -> dict:
        bg.add_task(lambda: bg_saw.append(state["status"]))
        return {}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert bg_saw == ["closed"]


# ---------------------------------------------------------------------------
# test_function_scope_cleanup_can_enqueue_background_task
# ---------------------------------------------------------------------------


def test_function_scope_cleanup_can_enqueue_background_task() -> None:
    """function_stack exits before BackgroundTasks.__call__ snapshots
    self.tasks and sets _executed.  A function-scoped dep's cleanup code
    that calls bg.add_task() runs before the snapshot → the task is
    captured and executed.

    Expected run order: endpoint, from_func_cleanup.

    Failure mode guarded: moving the _executed flag or the task snapshot
    to before function_stack exit would silently drop tasks enqueued
    during function-scoped cleanup."""
    ran: list[str] = []

    def func_dep(bg: BackgroundTasks):  # type: ignore[no-untyped-def]
        yield
        bg.add_task(lambda: ran.append("from_func_cleanup"))

    app = FastAPI()

    @app.get("/")
    def endpoint(_f: Annotated[None, Depends(func_dep, scope="function")]) -> dict:
        ran.append("endpoint")
        return {}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert ran == ["endpoint", "from_func_cleanup"]


# ---------------------------------------------------------------------------
# test_request_scope_cleanup_cannot_enqueue_background_task
# ---------------------------------------------------------------------------


def test_request_scope_cleanup_cannot_enqueue_background_task(caplog) -> None:
    """request_stack exits after BackgroundTasks.__call__ has already set
    _executed=True.  A request-scoped dep's cleanup call to add_task hits
    the guard in background.py, logs a warning, and the task is never
    added to the list.

    Expected: 'from_req_cleanup' does NOT appear in ran; a log warning
    containing 'already been executed' is emitted.

    Failure mode guarded: removing or deferring the _executed guard would
    allow request-scoped cleanup to silently enqueue tasks that execute
    in an undefined order relative to the response lifecycle."""
    ran: list[str] = []

    def req_dep(bg: BackgroundTasks):  # type: ignore[no-untyped-def]
        yield
        bg.add_task(lambda: ran.append("from_req_cleanup"))

    app = FastAPI()

    @app.get("/")
    def endpoint(_r: Annotated[None, Depends(req_dep)]) -> dict:
        ran.append("endpoint")
        return {}

    with TestClient(app) as client:
        with caplog.at_level(logging.WARNING, logger="fastapi.background"):
            resp = client.get("/")
    assert resp.status_code == 200
    assert "from_req_cleanup" not in ran
    assert any("already been executed" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# test_transitive_scope_leak_through_plain_wrapper
# ---------------------------------------------------------------------------


def test_transitive_scope_leak_through_plain_wrapper() -> None:
    """The DependencyScopeError guard (utils.py:284-287) checks only the
    direct child's scope field.  A plain (non-generator) function inserted
    between a request-scoped generator parent and a function-scoped
    generator grandchild has scope=None; the guard does not fire.  The
    plain wrapper returns the same object the function-scoped dep yielded.
    By the time the request-scoped parent's cleanup runs, the
    function-scoped grandchild has already invalidated that object.

    Expected: route registers without DependencyScopeError; request_dep's
    cleanup observes resource status == 'closed'.

    Failure mode guarded (documentation): this test documents a known
    single-depth limitation.  If transitive scope validation is added,
    this test must be updated to reflect the new behaviour."""
    cleanup_saw: list[str] = []
    resource: dict[str, str] = {}

    def func_dep():  # type: ignore[no-untyped-def]
        resource["status"] = "open"
        yield resource
        resource["status"] = "closed"

    def plain_wrapper(
        res: Annotated[dict, Depends(func_dep, scope="function")],
    ) -> dict:
        return res  # pass-through; not a generator

    def request_dep(res: Annotated[dict, Depends(plain_wrapper)]):  # type: ignore[no-untyped-def]
        yield
        cleanup_saw.append(res["status"])

    app = FastAPI()

    @app.get("/")
    def endpoint(_r: Annotated[None, Depends(request_dep)]) -> dict:
        return {}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert cleanup_saw == ["closed"]


# ---------------------------------------------------------------------------
# test_multiple_route_deps_exit_in_reverse_declaration_order
# ---------------------------------------------------------------------------


def test_multiple_route_deps_exit_in_reverse_declaration_order() -> None:
    """Route-level deps are prepended via ``dependencies[::-1]`` +
    ``insert(0, …)`` (routing.py:479-483), which preserves their original
    declaration order at the front of dependant.dependencies.  They are
    therefore pushed first and exit last, in reverse declaration order
    (LIFO).

    Declaration order: r1, r2, r3.
    Push order:        r1, r2, r3.
    Cleanup order:     r3, r2, r1.

    Failure mode guarded: changing the reversal + insert pattern (e.g.,
    a plain append loop) would reverse the declaration order of route
    deps at the front of the list, producing cleanup order r1, r2, r3."""
    order: list[str] = []

    def r1():  # type: ignore[no-untyped-def]
        yield
        order.append("r1")

    def r2():  # type: ignore[no-untyped-def]
        yield
        order.append("r2")

    def r3():  # type: ignore[no-untyped-def]
        yield
        order.append("r3")

    app = FastAPI()

    @app.get("/", dependencies=[Depends(r1), Depends(r2), Depends(r3)])
    def endpoint() -> dict:
        return {}

    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    assert order == ["r3", "r2", "r1"]


# ---------------------------------------------------------------------------
# test_shared_dep_cleanup_position_is_first_dfs_encounter
# ---------------------------------------------------------------------------


def test_shared_dep_cleanup_position_is_first_dfs_encounter() -> None:
    """With use_cache=True (the default) a shared dep is pushed exactly
    once — during the first branch whose DFS recursion reaches it.
    Subsequent encounters hit the cache (utils.py:674) and skip the push.
    The shared dep's cleanup position in the LIFO sequence is therefore
    anchored to whichever branch appears first in the signature, not to
    where the shared dep is declared.

    Both sub-cases below put shared as the deepest node.  Swapping which
    branch is listed first swaps the two branches' cleanup positions but
    shared always exits last (it was pushed first).

    Failure mode guarded: changing cache-store or cache-check semantics
    (e.g., storing only when use_cache=True) would move the shared dep's
    cleanup to a different position depending on encounter order."""

    # ── sub-case: branch_a listed first ──
    order_a: list[str] = []

    def shared_a():  # type: ignore[no-untyped-def]
        yield "s"
        order_a.append("shared")

    def ba(s: Annotated[str, Depends(shared_a)]):  # type: ignore[no-untyped-def]
        yield "a"
        order_a.append("branch_a")

    def bb_a(s: Annotated[str, Depends(shared_a)]):  # type: ignore[no-untyped-def]
        yield "b"
        order_a.append("branch_b")

    app_a = FastAPI()

    @app_a.get("/")
    def ep_a(
        _a: Annotated[str, Depends(ba)],
        _b: Annotated[str, Depends(bb_a)],
    ) -> dict:
        return {}

    with TestClient(app_a) as client:
        client.get("/")
    # push: shared, branch_a, branch_b  →  LIFO: branch_b, branch_a, shared
    assert order_a == ["branch_b", "branch_a", "shared"]

    # ── sub-case: branch_b listed first ──
    order_b: list[str] = []

    def shared_b():  # type: ignore[no-untyped-def]
        yield "s"
        order_b.append("shared")

    def ba_b(s: Annotated[str, Depends(shared_b)]):  # type: ignore[no-untyped-def]
        yield "a"
        order_b.append("branch_a")

    def bb(s: Annotated[str, Depends(shared_b)]):  # type: ignore[no-untyped-def]
        yield "b"
        order_b.append("branch_b")

    app_b = FastAPI()

    @app_b.get("/")
    def ep_b(
        _b: Annotated[str, Depends(bb)],
        _a: Annotated[str, Depends(ba_b)],
    ) -> dict:
        return {}

    with TestClient(app_b) as client:
        client.get("/")
    # push: shared, branch_b, branch_a  →  LIFO: branch_a, branch_b, shared
    assert order_b == ["branch_a", "branch_b", "shared"]


# ---------------------------------------------------------------------------
# test_dep_setup_failure_partial_cleanup
# ---------------------------------------------------------------------------


def test_dep_setup_failure_partial_cleanup() -> None:
    """When a dep raises before its yield (setup failure) the exception
    propagates out of solve_dependencies.  Deps that were already pushed
    onto the stack before the failing dep are unwound normally (LIFO).
    Deps declared after the failing dep in the signature are never
    reached and never pushed — their cleanup does not run.

    Signature order: dep_ok_1, dep_boom, dep_ok_2.
    dep_ok_1 is pushed.  dep_boom raises during setup — never pushed.
    dep_ok_2 is never reached.

    Expected cleanup set: dep_ok_1 only.

    Failure mode guarded: an 'all or nothing' error handler that skips
    stack unwinding on setup failure would prevent dep_ok_1 from
    cleaning up, leaking its resource."""
    order: list[str] = []

    def dep_ok_1():  # type: ignore[no-untyped-def]
        try:
            yield "ok1"
        finally:
            order.append("dep_ok_1:cleanup")

    def dep_boom():  # type: ignore[no-untyped-def]
        raise RuntimeError("setup boom")
        yield  # pragma: no cover  # noqa: RET503

    def dep_ok_2():  # type: ignore[no-untyped-def]
        try:
            yield "ok2"
        finally:
            order.append("dep_ok_2:cleanup")

    app = FastAPI()

    @app.get("/")
    def endpoint(
        _a: Annotated[str, Depends(dep_ok_1)],
        _b: Annotated[str, Depends(dep_boom)],
        _c: Annotated[str, Depends(dep_ok_2)],
    ) -> dict:
        return {}  # pragma: no cover

    with TestClient(app, raise_server_exceptions=False) as client:
        resp = client.get("/")
    assert resp.status_code == 500
    assert order == ["dep_ok_1:cleanup"]
