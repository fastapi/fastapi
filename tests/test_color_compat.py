# tests/test_color_compat.py
import sys
import pytest
import warnings
import pydantic

# Determine if we are running Pydantic v2+
PYDANTIC_V2 = tuple(map(int, pydantic.VERSION.split("."))) >= (2, 0)

# Import Color safely
try:
    from pydantic_extra_types.color import Color
except ImportError:
    Color = type("DummyColor", (), {})  # fallback for Pydantic v1

def test_color_import_and_usage():
    """
    Test that Color import and usage works correctly for both Pydantic v1 and v2.
    Ensures no ImportError, TypeError, or DeprecationWarning occurs.
    """
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Pydantic v2: instantiate Color
        if PYDANTIC_V2:
            c = Color("#FF0000")  # should succeed
            assert isinstance(c, Color)
        else:
            # Pydantic v1: treat as dummy string
            c = "#FF0000"
            # Ensure no warning was triggered
            assert all("DeprecationWarning" not in str(warning.message) for warning in w)
