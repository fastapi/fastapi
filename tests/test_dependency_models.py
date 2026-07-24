from collections.abc import AsyncGenerator, Generator
from typing import Any

from fastapi.dependencies.models import (
    Dependant,
    _get_cache_key,
    _get_computed_scope,
    _get_oauth_scopes,
    _get_security_dependencies,
    _get_security_scheme,
    _is_async_gen_callable,
    _is_async_gen_callable_cached,
    _is_coroutine_callable,
    _is_coroutine_callable_cached,
    _is_gen_callable,
    _is_gen_callable_cached,
    _is_security_scheme,
    _uses_scopes,
)
from fastapi.security import APIKeyHeader


def sync_dependency() -> None:
    pass


async def async_dependency() -> None:
    pass


def generator_dependency() -> Generator[None, None, None]:
    yield


async def async_generator_dependency() -> AsyncGenerator[None, None]:
    yield


class UnhashableCallable:
    __hash__ = None

    async def __call__(self) -> None:
        pass


class UnhashableGeneratorCallable:
    __hash__ = None

    def __call__(self) -> Generator[None, None, None]:
        yield


class UnhashableAsyncGeneratorCallable:
    __hash__ = None

    async def __call__(self) -> AsyncGenerator[None, None]:
        yield


class EqualCallable:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, EqualCallable)

    def __hash__(self) -> int:
        return 1


class EqualAsyncCallable(EqualCallable):
    async def __call__(self) -> None:
        pass


class EqualSyncCallable(EqualCallable):
    def __call__(self) -> None:
        pass


def test_callable_classification_is_shared_by_call() -> None:
    _is_gen_callable_cached.cache_clear()
    _is_async_gen_callable_cached.cache_clear()
    _is_coroutine_callable_cached.cache_clear()

    for _ in range(2):
        assert not _is_gen_callable(async_dependency)
        assert not _is_async_gen_callable(async_dependency)
        assert _is_coroutine_callable(async_dependency)

    for cached_function in (
        _is_gen_callable_cached,
        _is_async_gen_callable_cached,
        _is_coroutine_callable_cached,
    ):
        cache_info = cached_function.cache_info()
        assert cache_info.hits == 1
        assert cache_info.misses == 1
        assert cache_info.maxsize == 1024


def test_unhashable_callable_classification() -> None:
    assert _is_coroutine_callable(UnhashableCallable())
    assert _is_gen_callable(UnhashableGeneratorCallable())
    assert _is_async_gen_callable(UnhashableAsyncGeneratorCallable())


def test_equal_callable_instances_are_cached_by_identity() -> None:
    async_callable = EqualAsyncCallable()
    sync_callable = EqualSyncCallable()

    assert async_callable == sync_callable
    assert _is_coroutine_callable(async_callable)
    assert not _is_coroutine_callable(sync_callable)


def test_callable_classification() -> None:
    assert not _is_gen_callable(sync_dependency)
    assert not _is_async_gen_callable(sync_dependency)
    assert not _is_coroutine_callable(sync_dependency)
    assert _is_gen_callable(generator_dependency)
    assert _is_async_gen_callable(async_generator_dependency)


def test_derived_values_are_not_stored_on_dependant() -> None:
    dependant = Dependant(call=async_dependency)
    uses_scopes_cache = {}

    assert _get_oauth_scopes(dependant=dependant) == []
    assert not _uses_scopes(dependant=dependant, cache=uses_scopes_cache)
    assert not _uses_scopes(dependant=dependant, cache=uses_scopes_cache)
    assert _get_security_dependencies(dependant=dependant) == []
    assert _get_computed_scope(dependant=dependant) is None
    assert _get_cache_key(dependant=dependant) == (async_dependency, (), "")

    assert not hasattr(dependant, "__dict__")


def test_security_scheme_helpers() -> None:
    security_scheme = APIKeyHeader(name="key")
    security_dependant = Dependant(call=security_scheme)
    dependant = Dependant(dependencies=[security_dependant])

    assert _is_security_scheme(dependant=security_dependant)
    assert _get_security_scheme(dependant=security_dependant) is security_scheme
    assert _get_security_dependencies(dependant=dependant) == [security_dependant]
    assert _uses_scopes(dependant=dependant)


def test_derived_values_follow_dependency_state() -> None:
    child = Dependant(call=sync_dependency)
    dependant = Dependant(
        call=sync_dependency,
        dependencies=[child],
        own_oauth_scopes=[],
        parent_oauth_scopes=["parent"],
    )

    assert _get_cache_key(dependant=dependant) == (sync_dependency, (), "")

    child.security_scopes_param_name = "scopes"
    dependant.own_oauth_scopes = ["own", "parent"]

    assert _uses_scopes(dependant=dependant)
    assert _get_oauth_scopes(dependant=dependant) == ["parent", "own"]
    assert _get_cache_key(dependant=dependant) == (
        sync_dependency,
        ("own", "parent"),
        "",
    )


def test_explicit_and_generator_scopes() -> None:
    assert (
        _get_computed_scope(dependant=Dependant(call=sync_dependency, scope="function"))
        == "function"
    )
    assert (
        _get_computed_scope(dependant=Dependant(call=generator_dependency)) == "request"
    )


def test_callable_return_annotations_are_not_used() -> None:
    class CallableWithUnhashableReturn:
        def __call__(self) -> Any:
            return None

        __hash__ = None

    assert not _is_coroutine_callable(CallableWithUnhashableReturn())
