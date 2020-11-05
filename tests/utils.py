import sys

import pytest

skip_py36 = pytest.mark.skipif(sys.version_info < (3, 7), reason="skip python3.6")
skip_py38 = pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9")
