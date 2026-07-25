import sys
from collections.abc import Callable

import pytest
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_flat_params

if "--codspeed" not in sys.argv:
    pytest.skip(
        "Benchmark tests are skipped by default; run with --codspeed.",
        allow_module_level=True,
    )

DEPENDENCY_COUNT = 500


def _create_dependency(index: int) -> Callable[[], int]:
    def dependency() -> int:
        return index

    return dependency


def _create_dependency_chain() -> Dependant:
    root = Dependant(call=_create_dependency(0))
    current = root
    for index in range(1, DEPENDENCY_COUNT + 1):
        child = Dependant(call=_create_dependency(index))
        current.dependencies.append(child)
        current = child
    return root


def test_dependency_flattening(benchmark) -> None:
    dependant = _create_dependency_chain()

    flat_params = benchmark(get_flat_params, dependant)

    assert flat_params == []
