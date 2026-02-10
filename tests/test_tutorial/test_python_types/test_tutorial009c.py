import importlib
import re
from types import ModuleType
from unittest.mock import patch

import pytest

from ...utils import needs_py310


@pytest.fixture(
    name="module",
    params=[
        pytest.param("tutorial009c_py39"),
        pytest.param("tutorial009c_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.python_types.{request.param}")
    return mod


def test_say_hi(module: ModuleType):
    with patch("builtins.print") as mock_print:
        module.say_hi("FastAPI")

    mock_print.assert_called_once_with("Hey FastAPI!")

    with pytest.raises(
        TypeError,
        match=re.escape("say_hi() missing 1 required positional argument: 'name'"),
    ):
        module.say_hi()
