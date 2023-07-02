from __future__ import annotations

from contextlib import contextmanager
from inspect import isasyncgenfunction, iscoroutinefunction
from typing import Any, Dict, Generator, Tuple, cast

import pytest
import sniffio

from ._core._eventloop import get_all_backends, get_asynclib
from .abc import TestRunner

_current_runner: TestRunner | None = None


def extract_backend_and_options(backend: object) -> tuple[str, dict[str, Any]]:
    if isinstance(backend, str):
        return backend, {}
    elif isinstance(backend, tuple) and len(backend) == 2:
        if isinstance(backend[0], str) and isinstance(backend[1], dict):
            return cast(Tuple[str, Dict[str, Any]], backend)

    raise TypeError("anyio_backend must be either a string or tuple of (string, dict)")


@contextmanager
def get_runner(
    backend_name: str, backend_options: dict[str, Any]
) -> Generator[TestRunner, object, None]:
    global _current_runner
    if _current_runner:
        yield _current_runner
        return

    asynclib = get_asynclib(backend_name)
    token = None
    if sniffio.current_async_library_cvar.get(None) is None:
        # Since we're in control of the event loop, we can cache the name of the async library
        token = sniffio.current_async_library_cvar.set(backend_name)

    try:
        backend_options = backend_options or {}
        with asynclib.TestRunner(**backend_options) as runner:
            _current_runner = runner
            yield runner
    finally:
        _current_runner = None
        if token:
            sniffio.current_async_library_cvar.reset(token)


def pytest_configure(config: Any) -> None:
    config.addinivalue_line(
        "markers",
        "anyio: mark the (coroutine function) test to be run "
        "asynchronously via anyio.",
    )


def pytest_fixture_setup(fixturedef: Any, request: Any) -> None:
    def wrapper(*args, anyio_backend, **kwargs):  # type: ignore[no-untyped-def]
        backend_name, backend_options = extract_backend_and_options(anyio_backend)
        if has_backend_arg:
            kwargs["anyio_backend"] = anyio_backend

        with get_runner(backend_name, backend_options) as runner:
            if isasyncgenfunction(func):
                yield from runner.run_asyncgen_fixture(func, kwargs)
            else:
                yield runner.run_fixture(func, kwargs)

    # Only apply this to coroutine functions and async generator functions in requests that involve
    # the anyio_backend fixture
    func = fixturedef.func
    if isasyncgenfunction(func) or iscoroutinefunction(func):
        if "anyio_backend" in request.fixturenames:
            has_backend_arg = "anyio_backend" in fixturedef.argnames
            fixturedef.func = wrapper
            if not has_backend_arg:
                fixturedef.argnames += ("anyio_backend",)


@pytest.hookimpl(tryfirst=True)
def pytest_pycollect_makeitem(collector: Any, name: Any, obj: Any) -> None:
    if collector.istestfunction(obj, name):
        inner_func = obj.hypothesis.inner_test if hasattr(obj, "hypothesis") else obj
        if iscoroutinefunction(inner_func):
            marker = collector.get_closest_marker("anyio")
            own_markers = getattr(obj, "pytestmark", ())
            if marker or any(marker.name == "anyio" for marker in own_markers):
                pytest.mark.usefixtures("anyio_backend")(obj)


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem: Any) -> bool | None:
    def run_with_hypothesis(**kwargs: Any) -> None:
        with get_runner(backend_name, backend_options) as runner:
            runner.run_test(original_func, kwargs)

    backend = pyfuncitem.funcargs.get("anyio_backend")
    if backend:
        backend_name, backend_options = extract_backend_and_options(backend)

        if hasattr(pyfuncitem.obj, "hypothesis"):
            # Wrap the inner test function unless it's already wrapped
            original_func = pyfuncitem.obj.hypothesis.inner_test
            if original_func.__qualname__ != run_with_hypothesis.__qualname__:
                if iscoroutinefunction(original_func):
                    pyfuncitem.obj.hypothesis.inner_test = run_with_hypothesis

            return None

        if iscoroutinefunction(pyfuncitem.obj):
            funcargs = pyfuncitem.funcargs
            testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}
            with get_runner(backend_name, backend_options) as runner:
                runner.run_test(pyfuncitem.obj, testargs)

            return True

    return None


@pytest.fixture(params=get_all_backends())
def anyio_backend(request: Any) -> Any:
    return request.param


@pytest.fixture
def anyio_backend_name(anyio_backend: Any) -> str:
    if isinstance(anyio_backend, str):
        return anyio_backend
    else:
        return anyio_backend[0]


@pytest.fixture
def anyio_backend_options(anyio_backend: Any) -> dict[str, Any]:
    if isinstance(anyio_backend, str):
        return {}
    else:
        return anyio_backend[1]
