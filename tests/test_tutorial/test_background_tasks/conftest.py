import os
from pathlib import Path

import pytest


@pytest.fixture(name="path_to_log_file")
def log_path():
    log = Path("log.txt")
    yield log
    if log.is_file():
        os.remove(log)  # pragma: no cover
