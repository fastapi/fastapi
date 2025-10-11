import sys

import pytest
from fastapi._compat import PYDANTIC_V2
from inline_snapshot import Snapshot

needs_py39 = pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9+")
needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
needs_py_lt_314 = pytest.mark.skipif(
    sys.version_info > (3, 13), reason="requires python3.13-"
)
needs_pydanticv2 = pytest.mark.skipif(not PYDANTIC_V2, reason="requires Pydantic v2")
needs_pydanticv1 = pytest.mark.skipif(PYDANTIC_V2, reason="requires Pydantic v1")


def skip_module_if_py_gte_314():
    """Skip entire module on Python 3.14+ at import time."""
    if sys.version_info >= (3, 14):
        pytest.skip("requires python3.13-", allow_module_level=True)


def pydantic_snapshot(
    *,
    v2: Snapshot,
    v1: Snapshot,  # TODO: remove v1 argument when deprecating Pydantic v1
):
    """
    This function should be used like this:

    >>> assert value == pydantic_snapshot(v2=snapshot(),v1=snapshot())

    inline-snapshot will create the snapshots when pytest is executed for each versions of pydantic.

    It is also possible to use the function inside snapshots for version-specific values.

    >>> assert value == snapshot({
        "data": "some data",
        "version_specific": pydantic_snapshot(v2=snapshot(),v1=snapshot()),
    })
    """
    return v2 if PYDANTIC_V2 else v1
