"""Interface for accessing the file system with automatic caching.

The idea is to cache the results of any file system state reads during
a single transaction. This has two main benefits:

* This avoids redundant syscalls, as we won't perform the same OS
  operations multiple times.

* This makes it easier to reason about concurrent FS updates, as different
  operations targeting the same paths can't report different state during
  a transaction.

Note that this only deals with reading state, not writing.

Properties maintained by the API:

* The contents of the file are always from the same or later time compared
  to the reported mtime of the file, even if mtime is queried after reading
  a file.

* Repeating an operation produces the same result as the first one during
  a transaction.

* Call flush() to start a new transaction (flush the caches).

The API is a bit limited. It's easy to add new cached operations, however.
You should perform all file system reads through the API to actually take
advantage of the benefits.
"""

from __future__ import annotations

import os
import stat

from mypy_extensions import mypyc_attr

from mypy.util import hash_digest


@mypyc_attr(allow_interpreted_subclasses=True)  # for tests
class FileSystemCache:
    def __init__(self) -> None:
        # The package root is not flushed with the caches.
        # It is set by set_package_root() below.
        self.package_root: list[str] = []
        self.flush()

    def set_package_root(self, package_root: list[str]) -> None:
        self.package_root = package_root

    def flush(self) -> None:
        """Start another transaction and empty all caches."""
        self.stat_cache: dict[str, os.stat_result] = {}
        self.stat_error_cache: dict[str, OSError] = {}
        self.listdir_cache: dict[str, list[str]] = {}
        self.listdir_error_cache: dict[str, OSError] = {}
        self.isfile_case_cache: dict[str, bool] = {}
        self.exists_case_cache: dict[str, bool] = {}
        self.read_cache: dict[str, bytes] = {}
        self.read_error_cache: dict[str, Exception] = {}
        self.hash_cache: dict[str, str] = {}
        self.fake_package_cache: set[str] = set()

    def stat(self, path: str) -> os.stat_result:
        if path in self.stat_cache:
            return self.stat_cache[path]
        if path in self.stat_error_cache:
            raise copy_os_error(self.stat_error_cache[path])
        try:
            st = os.stat(path)
        except OSError as err:
            if self.init_under_package_root(path):
                try:
                    return self._fake_init(path)
                except OSError:
                    pass
            # Take a copy to get rid of associated traceback and frame objects.
            # Just assigning to __traceback__ doesn't free them.
            self.stat_error_cache[path] = copy_os_error(err)
            raise err
        self.stat_cache[path] = st
        return st

    def init_under_package_root(self, path: str) -> bool:
        """Is this path an __init__.py under a package root?

        This is used to detect packages that don't contain __init__.py
        files, which is needed to support Bazel.  The function should
        only be called for non-existing files.

        It will return True if it refers to a __init__.py file that
        Bazel would create, so that at runtime Python would think the
        directory containing it is a package.  For this to work you
        must pass one or more package roots using the --package-root
        flag.

        As an exceptional case, any directory that is a package root
        itself will not be considered to contain a __init__.py file.
        This is different from the rules Bazel itself applies, but is
        necessary for mypy to properly distinguish packages from other
        directories.

        See https://docs.bazel.build/versions/master/be/python.html,
        where this behavior is described under legacy_create_init.
        """
        if not self.package_root:
            return False
        dirname, basename = os.path.split(path)
        if basename != "__init__.py":
            return False
        if not os.path.basename(dirname).isidentifier():
            # Can't put an __init__.py in a place that's not an identifier
            return False
        try:
            st = self.stat(dirname)
        except OSError:
            return False
        else:
            if not stat.S_ISDIR(st.st_mode):
                return False
        ok = False
        drive, path = os.path.splitdrive(path)  # Ignore Windows drive name
        if os.path.isabs(path):
            path = os.path.relpath(path)
        path = os.path.normpath(path)
        for root in self.package_root:
            if path.startswith(root):
                if path == root + basename:
                    # A package root itself is never a package.
                    ok = False
                    break
                else:
                    ok = True
        return ok

    def _fake_init(self, path: str) -> os.stat_result:
        """Prime the cache with a fake __init__.py file.

        This makes code that looks for path believe an empty file by
        that name exists.  Should only be called after
        init_under_package_root() returns True.
        """
        dirname, basename = os.path.split(path)
        assert basename == "__init__.py", path
        assert not os.path.exists(path), path  # Not cached!
        dirname = os.path.normpath(dirname)
        st = self.stat(dirname)  # May raise OSError
        # Get stat result as a list so we can modify it.
        seq: list[float] = list(st)
        seq[stat.ST_MODE] = stat.S_IFREG | 0o444
        seq[stat.ST_INO] = 1
        seq[stat.ST_NLINK] = 1
        seq[stat.ST_SIZE] = 0
        st = os.stat_result(seq)
        self.stat_cache[path] = st
        # Make listdir() and read() also pretend this file exists.
        self.fake_package_cache.add(dirname)
        return st

    def listdir(self, path: str) -> list[str]:
        path = os.path.normpath(path)
        if path in self.listdir_cache:
            res = self.listdir_cache[path]
            # Check the fake cache.
            if path in self.fake_package_cache and "__init__.py" not in res:
                res.append("__init__.py")  # Updates the result as well as the cache
            return res
        if path in self.listdir_error_cache:
            raise copy_os_error(self.listdir_error_cache[path])
        try:
            results = os.listdir(path)
        except OSError as err:
            # Like above, take a copy to reduce memory use.
            self.listdir_error_cache[path] = copy_os_error(err)
            raise err
        self.listdir_cache[path] = results
        # Check the fake cache.
        if path in self.fake_package_cache and "__init__.py" not in results:
            results.append("__init__.py")
        return results

    def isfile(self, path: str) -> bool:
        try:
            st = self.stat(path)
        except OSError:
            return False
        return stat.S_ISREG(st.st_mode)

    def isfile_case(self, path: str, prefix: str) -> bool:
        """Return whether path exists and is a file.

        On case-insensitive filesystems (like Mac or Windows) this returns
        False if the case of path's last component does not exactly match
        the case found in the filesystem.

        We check also the case of other path components up to prefix.
        For example, if path is 'user-stubs/pack/mod.pyi' and prefix is 'user-stubs',
        we check that the case of 'pack' and 'mod.py' matches exactly, 'user-stubs' will be
        case insensitive on case insensitive filesystems.

        The caller must ensure that prefix is a valid file system prefix of path.
        """
        if not self.isfile(path):
            # Fast path
            return False
        if path in self.isfile_case_cache:
            return self.isfile_case_cache[path]
        head, tail = os.path.split(path)
        if not tail:
            self.isfile_case_cache[path] = False
            return False
        try:
            names = self.listdir(head)
            # This allows one to check file name case sensitively in
            # case-insensitive filesystems.
            res = tail in names
        except OSError:
            res = False
        if res:
            # Also recursively check the other path components in case sensitive way.
            res = self.exists_case(head, prefix)
        self.isfile_case_cache[path] = res
        return res

    def exists_case(self, path: str, prefix: str) -> bool:
        """Return whether path exists - checking path components in case sensitive
        fashion, up to prefix.
        """
        if path in self.exists_case_cache:
            return self.exists_case_cache[path]
        head, tail = os.path.split(path)
        if not head.startswith(prefix) or not tail:
            # Only perform the check for paths under prefix.
            self.exists_case_cache[path] = True
            return True
        try:
            names = self.listdir(head)
            # This allows one to check file name case sensitively in
            # case-insensitive filesystems.
            res = tail in names
        except OSError:
            res = False
        if res:
            # Also recursively check other path components.
            res = self.exists_case(head, prefix)
        self.exists_case_cache[path] = res
        return res

    def isdir(self, path: str) -> bool:
        try:
            st = self.stat(path)
        except OSError:
            return False
        return stat.S_ISDIR(st.st_mode)

    def exists(self, path: str) -> bool:
        try:
            self.stat(path)
        except FileNotFoundError:
            return False
        return True

    def read(self, path: str) -> bytes:
        if path in self.read_cache:
            return self.read_cache[path]
        if path in self.read_error_cache:
            raise self.read_error_cache[path]

        # Need to stat first so that the contents of file are from no
        # earlier instant than the mtime reported by self.stat().
        self.stat(path)

        dirname, basename = os.path.split(path)
        dirname = os.path.normpath(dirname)
        # Check the fake cache.
        if basename == "__init__.py" and dirname in self.fake_package_cache:
            data = b""
        else:
            try:
                with open(path, "rb") as f:
                    data = f.read()
            except OSError as err:
                self.read_error_cache[path] = err
                raise

        self.read_cache[path] = data
        self.hash_cache[path] = hash_digest(data)
        return data

    def hash_digest(self, path: str) -> str:
        if path not in self.hash_cache:
            self.read(path)
        return self.hash_cache[path]

    def samefile(self, f1: str, f2: str) -> bool:
        s1 = self.stat(f1)
        s2 = self.stat(f2)
        return os.path.samestat(s1, s2)


def copy_os_error(e: OSError) -> OSError:
    new = OSError(*e.args)
    new.errno = e.errno
    new.strerror = e.strerror
    new.filename = e.filename
    if e.filename2:
        new.filename2 = e.filename2
    return new
