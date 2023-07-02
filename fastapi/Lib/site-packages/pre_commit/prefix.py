from __future__ import annotations

import os.path
from typing import NamedTuple


class Prefix(NamedTuple):
    prefix_dir: str

    def path(self, *parts: str) -> str:
        return os.path.normpath(os.path.join(self.prefix_dir, *parts))

    def exists(self, *parts: str) -> bool:
        return os.path.exists(self.path(*parts))

    def star(self, end: str) -> tuple[str, ...]:
        paths = os.listdir(self.prefix_dir)
        return tuple(path for path in paths if path.endswith(end))
