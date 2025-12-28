import importlib
from types import ModuleType
from unittest.mock import patch

import pytest

from ...utils import needs_py310


@pytest.fixture(
    name="module",
    params=[
        pytest.param("tutorial009_py39"),
        pytest.param("tutorial009_py310", marks=needs_py310),
        pytest.param("tutorial009b_py39"),
    ],
)
def get_module(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.python_types.{request.param}")
    return mod


def test_say_hi(module: ModuleType):
    with patch("builtins.print") as mock_print:
        module.say_hi("FastAPI")
        module.say_hi()

    assert mock_print.call_count == 2
    call_args = [arg.args for arg in mock_print.call_args_list]
    assert call_args == [
        ("Hey FastAPI!",),
        ("Hello World",),
    ]
