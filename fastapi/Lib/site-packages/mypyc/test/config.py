from __future__ import annotations

import os

provided_prefix = os.getenv("MYPY_TEST_PREFIX", None)
if provided_prefix:
    PREFIX = provided_prefix
else:
    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    PREFIX = os.path.dirname(os.path.dirname(this_file_dir))

# Location of test data files such as test case descriptions.
test_data_prefix = os.path.join(PREFIX, "mypyc", "test-data")
