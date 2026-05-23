import importlib
import sys

import pytest

needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
needs_py314 = pytest.mark.skipif(
    sys.version_info < (3, 14), reason="requires python3.14+"
)

needs_orjson = pytest.mark.skipif(
    importlib.util.find_spec("orjson") is None,
    reason="requires orjson",
)

needs_ujson = pytest.mark.skipif(
    importlib.util.find_spec("ujson") is None,
    reason="requires ujson",
)

workdir_lock = pytest.mark.xdist_group("workdir_lock")


def skip_module_if_py_gte_314():
    """Skip entire module on Python 3.14+ at import time."""
    if sys.version_info >= (3, 14):
        pytest.skip("requires python3.13-", allow_module_level=True)
