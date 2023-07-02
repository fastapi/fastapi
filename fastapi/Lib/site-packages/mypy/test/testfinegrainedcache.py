"""Tests for fine-grained incremental checking using the cache.

All of the real code for this lives in testfinegrained.py.
"""

# We can't "import FineGrainedSuite from ..." because that will cause pytest
# to collect the non-caching tests when running this file.
from __future__ import annotations

import mypy.test.testfinegrained


class FineGrainedCacheSuite(mypy.test.testfinegrained.FineGrainedSuite):
    use_cache = True
    test_name_suffix = "_cached"
    files = mypy.test.testfinegrained.FineGrainedSuite.files + [
        "fine-grained-cache-incremental.test"
    ]
