from contextlib import contextmanager
from unittest.mock import patch


class DependendencyOverrides(dict):
    @contextmanager
    def __call__(self, overrides: dict):
        with patch.dict(self, overrides):
            yield
