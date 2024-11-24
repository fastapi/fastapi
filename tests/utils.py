import sys

import pytest
from fastapi._compat import PYDANTIC_V2
from inline_snapshot import Snapshot

needs_py39 = pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9+")
needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
needs_pydanticv2 = pytest.mark.skipif(not PYDANTIC_V2, reason="requires Pydantic v2")
needs_pydanticv1 = pytest.mark.skipif(PYDANTIC_V2, reason="requires Pydantic v1")


def snapshot_pydantic(*, v1: Snapshot, v2: Snapshot):
    return v2 if PYDANTIC_V2 else v1
