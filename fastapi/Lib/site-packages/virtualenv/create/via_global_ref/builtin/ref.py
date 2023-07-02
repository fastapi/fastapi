"""
Virtual environments in the traditional sense are built as reference to the host python. This file allows declarative
references to elements on the file system, allowing our system to automatically detect what modes it can support given
the constraints: e.g. can the file system symlink, can the files be read, executed, etc.
"""  # noqa: D205

from __future__ import annotations

import os
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from stat import S_IXGRP, S_IXOTH, S_IXUSR

from virtualenv.info import fs_is_case_sensitive, fs_supports_symlink
from virtualenv.util.path import copy, make_exe, symlink


class RefMust:
    NA = "NA"
    COPY = "copy"
    SYMLINK = "symlink"


class RefWhen:
    ANY = "ANY"
    COPY = "copy"
    SYMLINK = "symlink"


class PathRef(metaclass=ABCMeta):
    """Base class that checks if a file reference can be symlink/copied."""

    FS_SUPPORTS_SYMLINK = fs_supports_symlink()
    FS_CASE_SENSITIVE = fs_is_case_sensitive()

    def __init__(self, src, must=RefMust.NA, when=RefWhen.ANY) -> None:
        self.must = must
        self.when = when
        self.src = src
        try:
            self.exists = src.exists()
        except OSError:
            self.exists = False
        self._can_read = None if self.exists else False
        self._can_copy = None if self.exists else False
        self._can_symlink = None if self.exists else False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(src={self.src})"

    @property
    def can_read(self):
        if self._can_read is None:
            if self.src.is_file():
                try:
                    with self.src.open("rb"):
                        self._can_read = True
                except OSError:
                    self._can_read = False
            else:
                self._can_read = os.access(str(self.src), os.R_OK)
        return self._can_read

    @property
    def can_copy(self):
        if self._can_copy is None:
            if self.must == RefMust.SYMLINK:
                self._can_copy = self.can_symlink
            else:
                self._can_copy = self.can_read
        return self._can_copy

    @property
    def can_symlink(self):
        if self._can_symlink is None:
            if self.must == RefMust.COPY:
                self._can_symlink = self.can_copy
            else:
                self._can_symlink = self.FS_SUPPORTS_SYMLINK and self.can_read
        return self._can_symlink

    @abstractmethod
    def run(self, creator, symlinks):
        raise NotImplementedError

    def method(self, symlinks):
        if self.must == RefMust.SYMLINK:
            return symlink
        if self.must == RefMust.COPY:
            return copy
        return symlink if symlinks else copy


class ExePathRef(PathRef, metaclass=ABCMeta):
    """Base class that checks if a executable can be references via symlink/copy."""

    def __init__(self, src, must=RefMust.NA, when=RefWhen.ANY) -> None:
        super().__init__(src, must, when)
        self._can_run = None

    @property
    def can_symlink(self):
        if self.FS_SUPPORTS_SYMLINK:
            return self.can_run
        return False

    @property
    def can_run(self):
        if self._can_run is None:
            mode = self.src.stat().st_mode
            for key in [S_IXUSR, S_IXGRP, S_IXOTH]:
                if mode & key:
                    self._can_run = True
                break
            else:
                self._can_run = False
        return self._can_run


class PathRefToDest(PathRef):
    """Link a path on the file system."""

    def __init__(self, src, dest, must=RefMust.NA, when=RefWhen.ANY) -> None:
        super().__init__(src, must, when)
        self.dest = dest

    def run(self, creator, symlinks):
        dest = self.dest(creator, self.src)
        method = self.method(symlinks)
        dest_iterable = dest if isinstance(dest, list) else (dest,)
        if not dest.parent.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
        for dst in dest_iterable:
            method(self.src, dst)


class ExePathRefToDest(PathRefToDest, ExePathRef):
    """Link a exe path on the file system."""

    def __init__(
        self, src, targets, dest, must=RefMust.NA, when=RefWhen.ANY
    ) -> None:  # noqa: PLR0913
        ExePathRef.__init__(self, src, must, when)
        PathRefToDest.__init__(self, src, dest, must, when)
        if not self.FS_CASE_SENSITIVE:
            targets = list(OrderedDict((i.lower(), None) for i in targets).keys())
        self.base = targets[0]
        self.aliases = targets[1:]
        self.dest = dest

    def run(self, creator, symlinks):
        bin_dir = self.dest(creator, self.src).parent
        dest = bin_dir / self.base
        method = self.method(symlinks)
        method(self.src, dest)
        if not symlinks:
            make_exe(dest)
        for extra in self.aliases:
            link_file = bin_dir / extra
            if link_file.exists():
                link_file.unlink()
            if symlinks:
                link_file.symlink_to(self.base)
            else:
                copy(self.src, link_file)
            if not symlinks:
                make_exe(link_file)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(src={self.src}, alias={self.aliases})"


__all__ = [
    "ExePathRef",
    "ExePathRefToDest",
    "PathRefToDest",
    "PathRef",
    "RefWhen",
    "RefMust",
]
