# patterns.py: Common wildcard searching/filtering functionality for files.
#
# Copyright (C) 2010 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Written by Boris Staletic <boris.staletic@gmail.com>

from __future__ import annotations

# Non-pure path objects are only allowed on their respective OS's.
# Thus, these utilities require "pure" path objects that don't access the filesystem.
# Since pathlib doesn't have a `case_sensitive` parameter, we have to approximate it
# by converting input paths to `PureWindowsPath` and `PurePosixPath` where:
#   - `PureWindowsPath` is always case-insensitive.
#   - `PurePosixPath` is always case-sensitive.
# Reference: https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.match
from pathlib import PurePosixPath, PureWindowsPath


def _match_path(path, included_patterns, excluded_patterns, case_sensitive):
    """Internal function same as :func:`match_path` but does not check arguments."""
    if case_sensitive:
        path = PurePosixPath(path)
    else:
        included_patterns = {pattern.lower() for pattern in included_patterns}
        excluded_patterns = {pattern.lower() for pattern in excluded_patterns}
        path = PureWindowsPath(path)

    common_patterns = included_patterns & excluded_patterns
    if common_patterns:
        raise ValueError(
            "conflicting patterns `{}` included and excluded".format(common_patterns)
        )
    return any(path.match(p) for p in included_patterns) and not any(
        path.match(p) for p in excluded_patterns
    )


def filter_paths(
    paths, included_patterns=None, excluded_patterns=None, case_sensitive=True
):
    """
    Filters from a set of paths based on acceptable patterns and
    ignorable patterns.
    :param pathnames:
        A list of path names that will be filtered based on matching and
        ignored patterns.
    :param included_patterns:
        Allow filenames matching wildcard patterns specified in this list.
        If no pattern list is specified, ["*"] is used as the default pattern,
        which matches all files.
    :param excluded_patterns:
        Ignores filenames matching wildcard patterns specified in this list.
        If no pattern list is specified, no files are ignored.
    :param case_sensitive:
        ``True`` if matching should be case-sensitive; ``False`` otherwise.
    :returns:
        A list of pathnames that matched the allowable patterns and passed
        through the ignored patterns.
    """
    included = ["*"] if included_patterns is None else included_patterns
    excluded = [] if excluded_patterns is None else excluded_patterns

    for path in paths:
        if _match_path(path, set(included), set(excluded), case_sensitive):
            yield path


def match_any_paths(
    paths, included_patterns=None, excluded_patterns=None, case_sensitive=True
):
    """
    Matches from a set of paths based on acceptable patterns and
    ignorable patterns.
    :param pathnames:
        A list of path names that will be filtered based on matching and
        ignored patterns.
    :param included_patterns:
        Allow filenames matching wildcard patterns specified in this list.
        If no pattern list is specified, ["*"] is used as the default pattern,
        which matches all files.
    :param excluded_patterns:
        Ignores filenames matching wildcard patterns specified in this list.
        If no pattern list is specified, no files are ignored.
    :param case_sensitive:
        ``True`` if matching should be case-sensitive; ``False`` otherwise.
    :returns:
        ``True`` if any of the paths matches; ``False`` otherwise.
    """
    included = ["*"] if included_patterns is None else included_patterns
    excluded = [] if excluded_patterns is None else excluded_patterns

    for path in paths:
        if _match_path(path, set(included), set(excluded), case_sensitive):
            return True
    return False
