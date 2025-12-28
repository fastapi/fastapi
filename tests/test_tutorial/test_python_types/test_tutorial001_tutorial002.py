import runpy
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "tutorial001_py39",
        "tutorial002_py39",
    ],
)
def test_run_module(module_name: str):
    with patch("builtins.print") as mock_print:
        runpy.run_module(f"docs_src.python_types.{module_name}", run_name="__main__")

    mock_print.assert_called_with("John Doe")
