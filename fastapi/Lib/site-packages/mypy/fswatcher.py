"""Watch parts of the file system for changes."""

from __future__ import annotations

from typing import AbstractSet, Iterable, NamedTuple

from mypy.fscache import FileSystemCache


class FileData(NamedTuple):
    st_mtime: float
    st_size: int
    hash: str


class FileSystemWatcher:
    """Watcher for file system changes among specific paths.

    All file system access is performed using FileSystemCache. We
    detect changed files by stat()ing them all and comparing hashes
    of potentially changed files. If a file has both size and mtime
    unmodified, the file is assumed to be unchanged.

    An important goal of this class is to make it easier to eventually
    use file system events to detect file changes.

    Note: This class doesn't flush the file system cache. If you don't
    manually flush it, changes won't be seen.
    """

    # TODO: Watching directories?
    # TODO: Handle non-files

    def __init__(self, fs: FileSystemCache) -> None:
        self.fs = fs
        self._paths: set[str] = set()
        self._file_data: dict[str, FileData | None] = {}

    def dump_file_data(self) -> dict[str, tuple[float, int, str]]:
        return {k: v for k, v in self._file_data.items() if v is not None}

    def set_file_data(self, path: str, data: FileData) -> None:
        self._file_data[path] = data

    def add_watched_paths(self, paths: Iterable[str]) -> None:
        for path in paths:
            if path not in self._paths:
                # By storing None this path will get reported as changed by
                # find_changed if it exists.
                self._file_data[path] = None
        self._paths |= set(paths)

    def remove_watched_paths(self, paths: Iterable[str]) -> None:
        for path in paths:
            if path in self._file_data:
                del self._file_data[path]
        self._paths -= set(paths)

    def _update(self, path: str) -> None:
        st = self.fs.stat(path)
        hash_digest = self.fs.hash_digest(path)
        self._file_data[path] = FileData(st.st_mtime, st.st_size, hash_digest)

    def _find_changed(self, paths: Iterable[str]) -> AbstractSet[str]:
        changed = set()
        for path in paths:
            old = self._file_data[path]
            try:
                st = self.fs.stat(path)
            except FileNotFoundError:
                if old is not None:
                    # File was deleted.
                    changed.add(path)
                    self._file_data[path] = None
            else:
                if old is None:
                    # File is new.
                    changed.add(path)
                    self._update(path)
                # Round mtimes down, to match the mtimes we write to meta files
                elif st.st_size != old.st_size or int(st.st_mtime) != int(old.st_mtime):
                    # Only look for changes if size or mtime has changed as an
                    # optimization, since calculating hash is expensive.
                    new_hash = self.fs.hash_digest(path)
                    self._update(path)
                    if st.st_size != old.st_size or new_hash != old.hash:
                        # Changed file.
                        changed.add(path)
        return changed

    def find_changed(self) -> AbstractSet[str]:
        """Return paths that have changes since the last call, in the watched set."""
        return self._find_changed(self._paths)

    def update_changed(self, remove: list[str], update: list[str]) -> AbstractSet[str]:
        """Alternative to find_changed() given explicit changes.

        This only calls self.fs.stat() on added or updated files, not
        on all files.  It believes all other files are unchanged!

        Implies add_watched_paths() for add and update, and
        remove_watched_paths() for remove.
        """
        self.remove_watched_paths(remove)
        self.add_watched_paths(update)
        return self._find_changed(update)
