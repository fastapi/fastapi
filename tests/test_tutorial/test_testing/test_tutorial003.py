import pytest


def test_main():
    with pytest.warns(DeprecationWarning):
        from docs_src.app_testing.tutorial003_py310 import test_read_items
    test_read_items()
