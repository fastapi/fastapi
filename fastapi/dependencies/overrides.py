from contextlib import contextmanager
from typing import Dict, Callable, Any
from unittest.mock import patch


class DependendencyOverrides(Dict[Callable[..., Any], Callable[..., Any]]):
    @contextmanager
    def __call__(self, overrides: dict):
        with patch.dict(self, overrides):
            yield
