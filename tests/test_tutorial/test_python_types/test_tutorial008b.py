import importlib
from types import ModuleType
from unittest.mock import patch

import pytest

from ...utils import needs_py310


@pytest.fixture(
    name="module",
    params=[
        pytest.param("tutorial008b_py39"),
        pytest.param("tutorial008b_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.python_types.{request.param}")
    return mod


def test_process_items(module: ModuleType):
    with patch("builtins.print") as mock_print:
        module.process_item("a")

    assert mock_print.call_count == 1
    mock_print.assert_called_with("a")
