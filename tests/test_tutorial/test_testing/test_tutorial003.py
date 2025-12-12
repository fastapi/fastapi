import pytest


def test_main():
    with pytest.warns(DeprecationWarning):
        from docs_src.app_testing.tutorial003_py39 import test_read_items
    test_read_items()
