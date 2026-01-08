import sys

import pytest

needs_py39 = pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9+")
needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
needs_py_lt_314 = pytest.mark.skipif(
    sys.version_info >= (3, 14), reason="requires python3.13-"
)


def skip_module_if_py_gte_314():
    """Skip entire module on Python 3.14+ at import time."""
    if sys.version_info >= (3, 14):
        pytest.skip("requires python3.13-", allow_module_level=True)
