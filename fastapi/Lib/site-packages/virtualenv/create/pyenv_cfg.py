from __future__ import annotations

import logging
from collections import OrderedDict


class PyEnvCfg:
    def __init__(self, content, path) -> None:
        self.content = content
        self.path = path

    @classmethod
    def from_folder(cls, folder):
        return cls.from_file(folder / "pyvenv.cfg")

    @classmethod
    def from_file(cls, path):
        content = cls._read_values(path) if path.exists() else OrderedDict()
        return PyEnvCfg(content, path)

    @staticmethod
    def _read_values(path):
        content = OrderedDict()
        for line in path.read_text(encoding="utf-8").splitlines():
            equals_at = line.index("=")
            key = line[:equals_at].strip()
            value = line[equals_at + 1 :].strip()
            content[key] = value
        return content

    def write(self):
        logging.debug("write %s", self.path)
        text = ""
        for key, value in self.content.items():
            line = f"{key} = {value}"
            logging.debug("\t%s", line)
            text += line
            text += "\n"
        self.path.write_text(text, encoding="utf-8")

    def refresh(self):
        self.content = self._read_values(self.path)
        return self.content

    def __setitem__(self, key, value) -> None:
        self.content[key] = value

    def __getitem__(self, key):
        return self.content[key]

    def __contains__(self, item) -> bool:
        return item in self.content

    def update(self, other):
        self.content.update(other)
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self.path})"


__all__ = [
    "PyEnvCfg",
]
