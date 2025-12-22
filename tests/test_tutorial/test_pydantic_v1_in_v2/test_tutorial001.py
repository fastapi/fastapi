import sys
from typing import Any

import pytest

from tests.utils import skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()


import importlib

from ...utils import needs_py310


@pytest.fixture(
    name="mod",
    params=[
        "tutorial001_an_py39",
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.pydantic_v1_in_v2.{request.param}")
    return mod


def test_model(mod: Any):
    item = mod.Item(name="Foo", size=3.4)
    assert item.dict() == {"name": "Foo", "description": None, "size": 3.4}
