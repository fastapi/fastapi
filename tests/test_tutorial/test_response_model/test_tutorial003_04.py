import importlib

import pytest

from ...utils import needs_py310


# Previously, unions including `Response` in the return annotation were
# considered invalid and raised FastAPIError at import time.
# They are now supported as part of the enhanced return annotation handling.
# Importing the module should not raise FastAPIError anymore.
@pytest.mark.parametrize(
    "module_name",
    [
        pytest.param("tutorial003_04_py310", marks=needs_py310),
    ],
)
def test_response_union_with_response_is_valid(module_name: str) -> None:
    module = importlib.import_module(f"docs_src.response_model.{module_name}")
    assert module is not None
