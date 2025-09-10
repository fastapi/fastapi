import importlib

import pytest
from fastapi.exceptions import FastAPIError

from ...utils import needs_py310


@pytest.mark.parametrize(
    "module",
    [
        "tutorial003_04",
        pytest.param("tutorial003_04_py310", marks=needs_py310),
    ],
)
def test_invalid_response_model(module: str):
    with pytest.raises(FastAPIError):
        importlib.import_module(f"docs_src.response_model.{module}")
