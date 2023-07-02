"""Split namespace for argparse to allow separating options by prefix.

We use this to direct some options to an Options object and some to a
regular namespace.
"""

# In its own file largely because mypyc doesn't support its use of
# __getattr__/__setattr__ and has some issues with __dict__

from __future__ import annotations

import argparse
from typing import Any


class SplitNamespace(argparse.Namespace):
    def __init__(
        self, standard_namespace: object, alt_namespace: object, alt_prefix: str
    ) -> None:
        self.__dict__["_standard_namespace"] = standard_namespace
        self.__dict__["_alt_namespace"] = alt_namespace
        self.__dict__["_alt_prefix"] = alt_prefix

    def _get(self) -> tuple[Any, Any]:
        return (self._standard_namespace, self._alt_namespace)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith(self._alt_prefix):
            setattr(self._alt_namespace, name[len(self._alt_prefix) :], value)
        else:
            setattr(self._standard_namespace, name, value)

    def __getattr__(self, name: str) -> Any:
        if name.startswith(self._alt_prefix):
            return getattr(self._alt_namespace, name[len(self._alt_prefix) :])
        else:
            return getattr(self._standard_namespace, name)
