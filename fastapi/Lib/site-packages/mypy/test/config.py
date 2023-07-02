from __future__ import annotations

import os.path

provided_prefix = os.getenv("MYPY_TEST_PREFIX", None)
if provided_prefix:
    PREFIX = provided_prefix
else:
    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    PREFIX = os.path.dirname(os.path.dirname(this_file_dir))

# Location of test data files such as test case descriptions.
test_data_prefix = os.path.join(PREFIX, "test-data", "unit")
package_path = os.path.join(PREFIX, "test-data", "packages")

# Temp directory used for the temp files created when running test cases.
# This is *within* the tempfile.TemporaryDirectory that is chroot'ed per testcase.
# It is also hard-coded in numerous places, so don't change it.
test_temp_dir = "tmp"

# The PEP 561 tests do a bunch of pip installs which, even though they operate
# on distinct temporary virtual environments, run into race conditions on shared
# file-system state. To make this work reliably in parallel mode, we'll use a
# FileLock courtesy of the tox-dev/py-filelock package.
# Ref. https://github.com/python/mypy/issues/12615
# Ref. mypy/test/testpep561.py
pip_lock = os.path.join(package_path, ".pip_lock")
pip_timeout = 60
