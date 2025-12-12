import importlib
from types import ModuleType

import pytest

from ...utils import needs_py310


@pytest.fixture(
    name="test_module",
    params=[
        "app_b_py39.test_main",
        pytest.param("app_b_py310.test_main", marks=needs_py310),
        "app_b_an_py39.test_main",
        pytest.param("app_b_an_py310.test_main", marks=needs_py310),
    ],
)
def get_test_module(request: pytest.FixtureRequest) -> ModuleType:
    mod: ModuleType = importlib.import_module(f"docs_src.app_testing.{request.param}")
    return mod


def test_app(test_module: ModuleType):
    test_main = test_module
    test_main.test_create_existing_item()
    test_main.test_create_item()
    test_main.test_create_item_bad_token()
    test_main.test_read_nonexistent_item()
    test_main.test_read_item()
    test_main.test_read_item_bad_token()
