"""
This module provides utility methods for dealing with path-specs.
"""

import os
import os.path
import pathlib
import posixpath
import stat
import sys
import warnings
from collections.abc import Collection as CollectionType
from collections.abc import Iterable as IterableType
from os import PathLike
from typing import (
    Any,
    AnyStr,
    Callable,
    Collection,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Union,
)

from .pattern import Pattern

if sys.version_info >= (3, 9):
    StrPath = Union[str, PathLike[str]]
else:
    StrPath = Union[str, PathLike]

NORMALIZE_PATH_SEPS = [
    __sep for __sep in [os.sep, os.altsep] if __sep and __sep != posixpath.sep
]
"""
*NORMALIZE_PATH_SEPS* (:class:`list` of :class:`str`) contains the path
separators that need to be normalized to the POSIX separator for the
current operating system. The separators are determined by examining
:data:`os.sep` and :data:`os.altsep`.
"""

_registered_patterns = {}
"""
*_registered_patterns* (:class:`dict`) maps a name (:class:`str`) to the
registered pattern factory (:class:`~collections.abc.Callable`).
"""


def append_dir_sep(path: pathlib.Path) -> str:
    """
    Appends the path separator to the path if the path is a directory.
    This can be used to aid in distinguishing between directories and
    files on the file-system by relying on the presence of a trailing path
    separator.

    *path* (:class:`pathlib.path`) is the path to use.

    Returns the path (:class:`str`).
    """
    str_path = str(path)
    if path.is_dir():
        str_path += os.sep

    return str_path


def detailed_match_files(
    patterns: Iterable[Pattern],
    files: Iterable[str],
    all_matches: Optional[bool] = None,
) -> Dict[str, "MatchDetail"]:
    """
    Matches the files to the patterns, and returns which patterns matched
    the files.

    *patterns* (:class:`~collections.abc.Iterable` of :class:`~pathspec.pattern.Pattern`)
    contains the patterns to use.

    *files* (:class:`~collections.abc.Iterable` of :class:`str`) contains
    the normalized file paths to be matched against *patterns*.

    *all_matches* (:class:`boot` or :data:`None`) is whether to return all
    matches patterns (:data:`True`), or only the last matched pattern
    (:data:`False`). Default is :data:`None` for :data:`False`.

    Returns the matched files (:class:`dict`) which maps each matched file
    (:class:`str`) to the patterns that matched in order (:class:`.MatchDetail`).
    """
    all_files = files if isinstance(files, CollectionType) else list(files)
    return_files = {}
    for pattern in patterns:
        if pattern.include is not None:
            result_files = pattern.match(
                all_files
            )  # TODO: Replace with `.match_file()`.
            if pattern.include:
                # Add files and record pattern.
                for result_file in result_files:
                    if result_file in return_files:
                        if all_matches:
                            return_files[result_file].patterns.append(pattern)
                        else:
                            return_files[result_file].patterns[0] = pattern
                    else:
                        return_files[result_file] = MatchDetail([pattern])

            else:
                # Remove files.
                for file in result_files:
                    del return_files[file]

    return return_files


def _filter_patterns(patterns: Iterable[Pattern]) -> List[Pattern]:
    """
    Filters out null-patterns.

    *patterns* (:class:`Iterable` of :class:`.Pattern`) contains the
    patterns.

    Returns the patterns (:class:`list` of :class:`.Pattern`).
    """
    return [__pat for __pat in patterns if __pat.include is not None]


def _is_iterable(value: Any) -> bool:
    """
    Check whether the value is an iterable (excludes strings).

    *value* is the value to check,

    Returns whether *value* is a iterable (:class:`bool`).
    """
    return isinstance(value, IterableType) and not isinstance(value, (str, bytes))


def iter_tree_entries(
    root: StrPath,
    on_error: Optional[Callable] = None,
    follow_links: Optional[bool] = None,
) -> Iterator["TreeEntry"]:
    """
    Walks the specified directory for all files and directories.

    *root* (:class:`str` or :class:`os.PathLike[str]`) is the root directory to
    search.

    *on_error* (:class:`~collections.abc.Callable` or :data:`None`)
    optionally is the error handler for file-system exceptions. It will be
    called with the exception (:exc:`OSError`). Reraise the exception to
    abort the walk. Default is :data:`None` to ignore file-system
    exceptions.

    *follow_links* (:class:`bool` or :data:`None`) optionally is whether
    to walk symbolic links that resolve to directories. Default is
    :data:`None` for :data:`True`.

    Raises :exc:`RecursionError` if recursion is detected.

    Returns an :class:`~collections.abc.Iterator` yielding each file or
    directory entry (:class:`.TreeEntry`) relative to *root*.
    """
    if on_error is not None and not callable(on_error):
        raise TypeError(f"on_error:{on_error!r} is not callable.")

    if follow_links is None:
        follow_links = True

    yield from _iter_tree_entries_next(
        os.path.abspath(root), "", {}, on_error, follow_links
    )


def _iter_tree_entries_next(
    root_full: str,
    dir_rel: str,
    memo: Dict[str, str],
    on_error: Callable,
    follow_links: bool,
) -> Iterator["TreeEntry"]:
    """
    Scan the directory for all descendant files.

    *root_full* (:class:`str`) the absolute path to the root directory.

    *dir_rel* (:class:`str`) the path to the directory to scan relative to
    *root_full*.

    *memo* (:class:`dict`) keeps track of ancestor directories
    encountered. Maps each ancestor real path (:class:`str`) to relative
    path (:class:`str`).

    *on_error* (:class:`~collections.abc.Callable` or :data:`None`)
    optionally is the error handler for file-system exceptions.

    *follow_links* (:class:`bool`) is whether to walk symbolic links that
    resolve to directories.

    Yields each entry (:class:`.TreeEntry`).
    """
    dir_full = os.path.join(root_full, dir_rel)
    dir_real = os.path.realpath(dir_full)

    # Remember each encountered ancestor directory and its canonical
    # (real) path. If a canonical path is encountered more than once,
    # recursion has occurred.
    if dir_real not in memo:
        memo[dir_real] = dir_rel
    else:
        raise RecursionError(
            real_path=dir_real, first_path=memo[dir_real], second_path=dir_rel
        )

    with os.scandir(dir_full) as scan_iter:
        node_ent: os.DirEntry
        for node_ent in scan_iter:
            node_rel = os.path.join(dir_rel, node_ent.name)

            # Inspect child node.
            try:
                node_lstat = node_ent.stat(follow_symlinks=False)
            except OSError as e:
                if on_error is not None:
                    on_error(e)
                continue

            if node_ent.is_symlink():
                # Child node is a link, inspect the target node.
                try:
                    node_stat = node_ent.stat()
                except OSError as e:
                    if on_error is not None:
                        on_error(e)
                    continue
            else:
                node_stat = node_lstat

            if node_ent.is_dir(follow_symlinks=follow_links):
                # Child node is a directory, recurse into it and yield its
                # descendant files.
                yield TreeEntry(node_ent.name, node_rel, node_lstat, node_stat)

                yield from _iter_tree_entries_next(
                    root_full, node_rel, memo, on_error, follow_links
                )

            elif node_ent.is_file() or node_ent.is_symlink():
                # Child node is either a file or an unfollowed link, yield it.
                yield TreeEntry(node_ent.name, node_rel, node_lstat, node_stat)

    # NOTE: Make sure to remove the canonical (real) path of the directory
    # from the ancestors memo once we are done with it. This allows the
    # same directory to appear multiple times. If this is not done, the
    # second occurrence of the directory will be incorrectly interpreted
    # as a recursion. See <https://github.com/cpburnz/python-path-specification/pull/7>.
    del memo[dir_real]


def iter_tree_files(
    root: StrPath,
    on_error: Optional[Callable] = None,
    follow_links: Optional[bool] = None,
) -> Iterator[str]:
    """
    Walks the specified directory for all files.

    *root* (:class:`str` or :class:`os.PathLike[str]`) is the root directory to
    search for files.

    *on_error* (:class:`~collections.abc.Callable` or :data:`None`)
    optionally is the error handler for file-system exceptions. It will be
    called with the exception (:exc:`OSError`). Reraise the exception to
    abort the walk. Default is :data:`None` to ignore file-system
    exceptions.

    *follow_links* (:class:`bool` or :data:`None`) optionally is whether
    to walk symbolic links that resolve to directories. Default is
    :data:`None` for :data:`True`.

    Raises :exc:`RecursionError` if recursion is detected.

    Returns an :class:`~collections.abc.Iterator` yielding the path to
    each file (:class:`str`) relative to *root*.
    """
    for entry in iter_tree_entries(root, on_error=on_error, follow_links=follow_links):
        if not entry.is_dir(follow_links):
            yield entry.path


def iter_tree(root, on_error=None, follow_links=None):
    """
    DEPRECATED: The :func:`.iter_tree` function is an alias for the
    :func:`.iter_tree_files` function.
    """
    warnings.warn(
        ("util.iter_tree() is deprecated. Use util.iter_tree_files() instead."),
        DeprecationWarning,
        stacklevel=2,
    )
    return iter_tree_files(root, on_error=on_error, follow_links=follow_links)


def lookup_pattern(name: str) -> Callable[[AnyStr], Pattern]:
    """
    Lookups a registered pattern factory by name.

    *name* (:class:`str`) is the name of the pattern factory.

    Returns the registered pattern factory (:class:`~collections.abc.Callable`).
    If no pattern factory is registered, raises :exc:`KeyError`.
    """
    return _registered_patterns[name]


def match_file(patterns: Iterable[Pattern], file: str) -> bool:
    """
    Matches the file to the patterns.

    *patterns* (:class:`~collections.abc.Iterable` of :class:`~pathspec.pattern.Pattern`)
    contains the patterns to use.

    *file* (:class:`str`) is the normalized file path to be matched
    against *patterns*.

    Returns :data:`True` if *file* matched; otherwise, :data:`False`.
    """
    matched = False
    for pattern in patterns:
        if pattern.include is not None:
            if pattern.match_file(file) is not None:
                matched = pattern.include

    return matched


def match_files(
    patterns: Iterable[Pattern],
    files: Iterable[str],
) -> Set[str]:
    """
    DEPRECATED: This is an old function no longer used. Use the :func:`.match_file`
    function with a loop for better results.

    Matches the files to the patterns.

    *patterns* (:class:`~collections.abc.Iterable` of :class:`~pathspec.pattern.Pattern`)
    contains the patterns to use.

    *files* (:class:`~collections.abc.Iterable` of :class:`str`) contains
    the normalized file paths to be matched against *patterns*.

    Returns the matched files (:class:`set` of :class:`str`).
    """
    warnings.warn(
        (
            "util.match_files() is deprecated. Use util.match_file() with a "
            "loop for better results."
        ),
        DeprecationWarning,
        stacklevel=2,
    )

    use_patterns = _filter_patterns(patterns)

    return_files = set()
    for file in files:
        if match_file(use_patterns, file):
            return_files.add(file)

    return return_files


def normalize_file(
    file: StrPath,
    separators: Optional[Collection[str]] = None,
) -> str:
    """
    Normalizes the file path to use the POSIX path separator (i.e.,
    :data:`'/'`), and make the paths relative (remove leading :data:`'/'`).

    *file* (:class:`str` or :class:`os.PathLike[str]`) is the file path.

    *separators* (:class:`~collections.abc.Collection` of :class:`str`; or
    :data:`None`) optionally contains the path separators to normalize.
    This does not need to include the POSIX path separator (:data:`'/'`),
    but including it will not affect the results. Default is :data:`None`
    for :data:`NORMALIZE_PATH_SEPS`. To prevent normalization, pass an
    empty container (e.g., an empty tuple :data:`()`).

    Returns the normalized file path (:class:`str`).
    """
    # Normalize path separators.
    if separators is None:
        separators = NORMALIZE_PATH_SEPS

    # Convert path object to string.
    norm_file: str = os.fspath(file)

    for sep in separators:
        norm_file = norm_file.replace(sep, posixpath.sep)

    if norm_file.startswith("/"):
        # Make path relative.
        norm_file = norm_file[1:]

    elif norm_file.startswith("./"):
        # Remove current directory prefix.
        norm_file = norm_file[2:]

    return norm_file


def normalize_files(
    files: Iterable[StrPath],
    separators: Optional[Collection[str]] = None,
) -> Dict[str, List[StrPath]]:
    """
    DEPRECATED: This function is no longer used. Use the :func:`.normalize_file`
    function with a loop for better results.

    Normalizes the file paths to use the POSIX path separator.

    *files* (:class:`~collections.abc.Iterable` of :class:`str` or
    :class:`os.PathLike[str]`) contains the file paths to be normalized.

    *separators* (:class:`~collections.abc.Collection` of :class:`str`; or
    :data:`None`) optionally contains the path separators to normalize.
    See :func:`normalize_file` for more information.

    Returns a :class:`dict` mapping each normalized file path (:class:`str`)
    to the original file paths (:class:`list` of :class:`str` or
    :class:`os.PathLike[str]`).
    """
    warnings.warn(
        (
            "util.normalize_files() is deprecated. Use util.normalize_file() "
            "with a loop for better results."
        ),
        DeprecationWarning,
        stacklevel=2,
    )

    norm_files = {}
    for path in files:
        norm_file = normalize_file(path, separators=separators)
        if norm_file in norm_files:
            norm_files[norm_file].append(path)
        else:
            norm_files[norm_file] = [path]

    return norm_files


def register_pattern(
    name: str,
    pattern_factory: Callable[[AnyStr], Pattern],
    override: Optional[bool] = None,
) -> None:
    """
    Registers the specified pattern factory.

    *name* (:class:`str`) is the name to register the pattern factory
    under.

    *pattern_factory* (:class:`~collections.abc.Callable`) is used to
    compile patterns. It must accept an uncompiled pattern (:class:`str`)
    and return the compiled pattern (:class:`.Pattern`).

    *override* (:class:`bool` or :data:`None`) optionally is whether to
    allow overriding an already registered pattern under the same name
    (:data:`True`), instead of raising an :exc:`AlreadyRegisteredError`
    (:data:`False`). Default is :data:`None` for :data:`False`.
    """
    if not isinstance(name, str):
        raise TypeError(f"name:{name!r} is not a string.")

    if not callable(pattern_factory):
        raise TypeError(f"pattern_factory:{pattern_factory!r} is not callable.")

    if name in _registered_patterns and not override:
        raise AlreadyRegisteredError(name, _registered_patterns[name])

    _registered_patterns[name] = pattern_factory


class AlreadyRegisteredError(Exception):
    """
    The :exc:`AlreadyRegisteredError` exception is raised when a pattern
    factory is registered under a name already in use.
    """

    def __init__(
        self,
        name: str,
        pattern_factory: Callable[[AnyStr], Pattern],
    ) -> None:
        """
        Initializes the :exc:`AlreadyRegisteredError` instance.

        *name* (:class:`str`) is the name of the registered pattern.

        *pattern_factory* (:class:`~collections.abc.Callable`) is the
        registered pattern factory.
        """
        super(AlreadyRegisteredError, self).__init__(name, pattern_factory)

    @property
    def message(self) -> str:
        """
        *message* (:class:`str`) is the error message.
        """
        return "{name!r} is already registered for pattern factory:{pattern_factory!r}.".format(
            name=self.name,
            pattern_factory=self.pattern_factory,
        )

    @property
    def name(self) -> str:
        """
        *name* (:class:`str`) is the name of the registered pattern.
        """
        return self.args[0]

    @property
    def pattern_factory(self) -> Callable[[AnyStr], Pattern]:
        """
        *pattern_factory* (:class:`~collections.abc.Callable`) is the
        registered pattern factory.
        """
        return self.args[1]


class RecursionError(Exception):
    """
    The :exc:`RecursionError` exception is raised when recursion is
    detected.
    """

    def __init__(
        self,
        real_path: str,
        first_path: str,
        second_path: str,
    ) -> None:
        """
        Initializes the :exc:`RecursionError` instance.

        *real_path* (:class:`str`) is the real path that recursion was
        encountered on.

        *first_path* (:class:`str`) is the first path encountered for
        *real_path*.

        *second_path* (:class:`str`) is the second path encountered for
        *real_path*.
        """
        super(RecursionError, self).__init__(real_path, first_path, second_path)

    @property
    def first_path(self) -> str:
        """
        *first_path* (:class:`str`) is the first path encountered for
        :attr:`self.real_path <RecursionError.real_path>`.
        """
        return self.args[1]

    @property
    def message(self) -> str:
        """
        *message* (:class:`str`) is the error message.
        """
        return "Real path {real!r} was encountered at {first!r} and then {second!r}.".format(
            real=self.real_path,
            first=self.first_path,
            second=self.second_path,
        )

    @property
    def real_path(self) -> str:
        """
        *real_path* (:class:`str`) is the real path that recursion was
        encountered on.
        """
        return self.args[0]

    @property
    def second_path(self) -> str:
        """
        *second_path* (:class:`str`) is the second path encountered for
        :attr:`self.real_path <RecursionError.real_path>`.
        """
        return self.args[2]


class MatchDetail(object):
    """
    The :class:`.MatchDetail` class contains information about
    """

    # Make the class dict-less.
    __slots__ = ("patterns",)

    def __init__(self, patterns: Sequence[Pattern]) -> None:
        """
        Initialize the :class:`.MatchDetail` instance.

        *patterns* (:class:`~collections.abc.Sequence` of :class:`~pathspec.pattern.Pattern`)
        contains the patterns that matched the file in the order they were
        encountered.
        """

        self.patterns = patterns
        """
		*patterns* (:class:`~collections.abc.Sequence` of :class:`~pathspec.pattern.Pattern`)
		contains the patterns that matched the file in the order they were
		encountered.
		"""


class TreeEntry(object):
    """
    The :class:`.TreeEntry` class contains information about a file-system
    entry.
    """

    # Make the class dict-less.
    __slots__ = ("_lstat", "name", "path", "_stat")

    def __init__(
        self,
        name: str,
        path: str,
        lstat: os.stat_result,
        stat: os.stat_result,
    ) -> None:
        """
        Initialize the :class:`.TreeEntry` instance.

        *name* (:class:`str`) is the base name of the entry.

        *path* (:class:`str`) is the relative path of the entry.

        *lstat* (:class:`os.stat_result`) is the stat result of the direct
        entry.

        *stat* (:class:`os.stat_result`) is the stat result of the entry,
        potentially linked.
        """

        self._lstat: os.stat_result = lstat
        """
		*_lstat* (:class:`os.stat_result`) is the stat result of the direct
		entry.
		"""

        self.name: str = name
        """
		*name* (:class:`str`) is the base name of the entry.
		"""

        self.path: str = path
        """
		*path* (:class:`str`) is the path of the entry.
		"""

        self._stat: os.stat_result = stat
        """
		*_stat* (:class:`os.stat_result`) is the stat result of the linked
		entry.
		"""

    def is_dir(self, follow_links: Optional[bool] = None) -> bool:
        """
        Get whether the entry is a directory.

        *follow_links* (:class:`bool` or :data:`None`) is whether to follow
        symbolic links. If this is :data:`True`, a symlink to a directory
        will result in :data:`True`. Default is :data:`None` for :data:`True`.

        Returns whether the entry is a directory (:class:`bool`).
        """
        if follow_links is None:
            follow_links = True

        node_stat = self._stat if follow_links else self._lstat
        return stat.S_ISDIR(node_stat.st_mode)

    def is_file(self, follow_links: Optional[bool] = None) -> bool:
        """
        Get whether the entry is a regular file.

        *follow_links* (:class:`bool` or :data:`None`) is whether to follow
        symbolic links. If this is :data:`True`, a symlink to a regular file
        will result in :data:`True`. Default is :data:`None` for :data:`True`.

        Returns whether the entry is a regular file (:class:`bool`).
        """
        if follow_links is None:
            follow_links = True

        node_stat = self._stat if follow_links else self._lstat
        return stat.S_ISREG(node_stat.st_mode)

    def is_symlink(self) -> bool:
        """
        Returns whether the entry is a symbolic link (:class:`bool`).
        """
        return stat.S_ISLNK(self._lstat.st_mode)

    def stat(self, follow_links: Optional[bool] = None) -> os.stat_result:
        """
        Get the cached stat result for the entry.

        *follow_links* (:class:`bool` or :data:`None`) is whether to follow
        symbolic links. If this is :data:`True`, the stat result of the
        linked file will be returned. Default is :data:`None` for :data:`True`.

        Returns that stat result (:class:`os.stat_result`).
        """
        if follow_links is None:
            follow_links = True

        return self._stat if follow_links else self._lstat
