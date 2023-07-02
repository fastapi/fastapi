"""
This module implements Git's wildmatch pattern matching which itself is
derived from Rsync's wildmatch. Git uses wildmatch for its ".gitignore"
files.
"""

import re
import warnings
from typing import AnyStr, Optional, Tuple

from .. import util
from ..pattern import RegexPattern

_BYTES_ENCODING = "latin1"
"""
The encoding to use when parsing a byte string pattern.
"""

_DIR_MARK = "ps_d"
"""
The regex group name for the directory marker. This is only used by
:class:`GitIgnoreSpec`.
"""


class GitWildMatchPatternError(ValueError):
    """
    The :class:`GitWildMatchPatternError` indicates an invalid git wild match
    pattern.
    """

    pass


class GitWildMatchPattern(RegexPattern):
    """
    The :class:`GitWildMatchPattern` class represents a compiled Git
    wildmatch pattern.
    """

    # Keep the dict-less class hierarchy.
    __slots__ = ()

    @classmethod
    def pattern_to_regex(
        cls,
        pattern: AnyStr,
    ) -> Tuple[Optional[AnyStr], Optional[bool]]:
        """
        Convert the pattern into a regular expression.

        *pattern* (:class:`str` or :class:`bytes`) is the pattern to convert
        into a regular expression.

        Returns the uncompiled regular expression (:class:`str`, :class:`bytes`,
        or :data:`None`); and whether matched files should be included
        (:data:`True`), excluded (:data:`False`), or if it is a
        null-operation (:data:`None`).
        """
        if isinstance(pattern, str):
            return_type = str
        elif isinstance(pattern, bytes):
            return_type = bytes
            pattern = pattern.decode(_BYTES_ENCODING)
        else:
            raise TypeError(f"pattern:{pattern!r} is not a unicode or byte string.")

        original_pattern = pattern
        pattern = pattern.strip()

        if pattern.startswith("#"):
            # A pattern starting with a hash ('#') serves as a comment
            # (neither includes nor excludes files). Escape the hash with a
            # back-slash to match a literal hash (i.e., '\#').
            regex = None
            include = None

        elif pattern == "/":
            # EDGE CASE: According to `git check-ignore` (v2.4.1), a single
            # '/' does not match any file.
            regex = None
            include = None

        elif pattern:
            if pattern.startswith("!"):
                # A pattern starting with an exclamation mark ('!') negates the
                # pattern (exclude instead of include). Escape the exclamation
                # mark with a back-slash to match a literal exclamation mark
                # (i.e., '\!').
                include = False
                # Remove leading exclamation mark.
                pattern = pattern[1:]
            else:
                include = True

            # Allow a regex override for edge cases that cannot be handled
            # through normalization.
            override_regex = None

            # Split pattern into segments.
            pattern_segs = pattern.split("/")

            # Normalize pattern to make processing easier.

            # EDGE CASE: Deal with duplicate double-asterisk sequences.
            # Collapse each sequence down to one double-asterisk. Iterate over
            # the segments in reverse and remove the duplicate double
            # asterisks as we go.
            for i in range(len(pattern_segs) - 1, 0, -1):
                prev = pattern_segs[i - 1]
                seg = pattern_segs[i]
                if prev == "**" and seg == "**":
                    del pattern_segs[i]

            if (
                len(pattern_segs) == 2
                and pattern_segs[0] == "**"
                and not pattern_segs[1]
            ):
                # EDGE CASE: The '**/' pattern should match everything except
                # individual files in the root directory. This case cannot be
                # adequately handled through normalization. Use the override.
                override_regex = f"^.+(?P<{_DIR_MARK}>/).*$"

            if not pattern_segs[0]:
                # A pattern beginning with a slash ('/') will only match paths
                # directly on the root directory instead of any descendant
                # paths. So, remove empty first segment to make pattern relative
                # to root.
                del pattern_segs[0]

            elif len(pattern_segs) == 1 or (
                len(pattern_segs) == 2 and not pattern_segs[1]
            ):
                # A single pattern without a beginning slash ('/') will match
                # any descendant path. This is equivalent to "**/{pattern}". So,
                # prepend with double-asterisks to make pattern relative to
                # root.
                # EDGE CASE: This also holds for a single pattern with a
                # trailing slash (e.g. dir/).
                if pattern_segs[0] != "**":
                    pattern_segs.insert(0, "**")

            else:
                # EDGE CASE: A pattern without a beginning slash ('/') but
                # contains at least one prepended directory (e.g.
                # "dir/{pattern}") should not match "**/dir/{pattern}",
                # according to `git check-ignore` (v2.4.1).
                pass

            if not pattern_segs:
                # After resolving the edge cases, we end up with no pattern at
                # all. This must be because the pattern is invalid.
                raise GitWildMatchPatternError(
                    f"Invalid git pattern: {original_pattern!r}"
                )

            if not pattern_segs[-1] and len(pattern_segs) > 1:
                # A pattern ending with a slash ('/') will match all descendant
                # paths if it is a directory but not if it is a regular file.
                # This is equivalent to "{pattern}/**". So, set last segment to
                # a double-asterisk to include all descendants.
                pattern_segs[-1] = "**"

            if override_regex is None:
                # Build regular expression from pattern.
                output = ["^"]
                need_slash = False
                end = len(pattern_segs) - 1
                for i, seg in enumerate(pattern_segs):
                    if seg == "**":
                        if i == 0 and i == end:
                            # A pattern consisting solely of double-asterisks ('**')
                            # will match every path.
                            output.append(f"[^/]+(?:(?P<{_DIR_MARK}>/).*)?")
                        elif i == 0:
                            # A normalized pattern beginning with double-asterisks
                            # ('**') will match any leading path segments.
                            output.append("(?:.+/)?")
                            need_slash = False
                        elif i == end:
                            # A normalized pattern ending with double-asterisks ('**')
                            # will match any trailing path segments.
                            output.append(f"(?P<{_DIR_MARK}>/).*")
                        else:
                            # A pattern with inner double-asterisks ('**') will match
                            # multiple (or zero) inner path segments.
                            output.append("(?:/.+)?")
                            need_slash = True

                    elif seg == "*":
                        # Match single path segment.
                        if need_slash:
                            output.append("/")

                        output.append("[^/]+")

                        if i == end:
                            # A pattern ending without a slash ('/') will match a file
                            # or a directory (with paths underneath it). E.g., "foo"
                            # matches "foo", "foo/bar", "foo/bar/baz", etc.
                            output.append(f"(?:(?P<{_DIR_MARK}>/).*)?")

                        need_slash = True

                    else:
                        # Match segment glob pattern.
                        if need_slash:
                            output.append("/")

                        try:
                            output.append(cls._translate_segment_glob(seg))
                        except ValueError as e:
                            raise GitWildMatchPatternError(
                                f"Invalid git pattern: {original_pattern!r}"
                            ) from e

                        if i == end:
                            # A pattern ending without a slash ('/') will match a file
                            # or a directory (with paths underneath it). E.g., "foo"
                            # matches "foo", "foo/bar", "foo/bar/baz", etc.
                            output.append(f"(?:(?P<{_DIR_MARK}>/).*)?")

                        need_slash = True

                output.append("$")
                regex = "".join(output)

            else:
                # Use regex override.
                regex = override_regex

        else:
            # A blank pattern is a null-operation (neither includes nor
            # excludes files).
            regex = None
            include = None

        if regex is not None and return_type is bytes:
            regex = regex.encode(_BYTES_ENCODING)

        return regex, include

    @staticmethod
    def _translate_segment_glob(pattern: str) -> str:
        """
        Translates the glob pattern to a regular expression. This is used in
        the constructor to translate a path segment glob pattern to its
        corresponding regular expression.

        *pattern* (:class:`str`) is the glob pattern.

        Returns the regular expression (:class:`str`).
        """
        # NOTE: This is derived from `fnmatch.translate()` and is similar to
        # the POSIX function `fnmatch()` with the `FNM_PATHNAME` flag set.

        escape = False
        regex = ""
        i, end = 0, len(pattern)
        while i < end:
            # Get next character.
            char = pattern[i]
            i += 1

            if escape:
                # Escape the character.
                escape = False
                regex += re.escape(char)

            elif char == "\\":
                # Escape character, escape next character.
                escape = True

            elif char == "*":
                # Multi-character wildcard. Match any string (except slashes),
                # including an empty string.
                regex += "[^/]*"

            elif char == "?":
                # Single-character wildcard. Match any single character (except
                # a slash).
                regex += "[^/]"

            elif char == "[":
                # Bracket expression wildcard. Except for the beginning
                # exclamation mark, the whole bracket expression can be used
                # directly as regex but we have to find where the expression
                # ends.
                # - "[][!]" matches ']', '[' and '!'.
                # - "[]-]" matches ']' and '-'.
                # - "[!]a-]" matches any character except ']', 'a' and '-'.
                j = i
                # Pass brack expression negation.
                if j < end and pattern[j] == "!":
                    j += 1
                # Pass first closing bracket if it is at the beginning of the
                # expression.
                if j < end and pattern[j] == "]":
                    j += 1
                # Find closing bracket. Stop once we reach the end or find it.
                while j < end and pattern[j] != "]":
                    j += 1

                if j < end:
                    # Found end of bracket expression. Increment j to be one past
                    # the closing bracket:
                    #
                    #  [...]
                    #   ^   ^
                    #   i   j
                    #
                    j += 1
                    expr = "["

                    if pattern[i] == "!":
                        # Braket expression needs to be negated.
                        expr += "^"
                        i += 1
                    elif pattern[i] == "^":
                        # POSIX declares that the regex bracket expression negation
                        # "[^...]" is undefined in a glob pattern. Python's
                        # `fnmatch.translate()` escapes the caret ('^') as a
                        # literal. To maintain consistency with undefined behavior,
                        # I am escaping the '^' as well.
                        expr += "\\^"
                        i += 1

                    # Build regex bracket expression. Escape slashes so they are
                    # treated as literal slashes by regex as defined by POSIX.
                    expr += pattern[i:j].replace("\\", "\\\\")

                    # Add regex bracket expression to regex result.
                    regex += expr

                    # Set i to one past the closing bracket.
                    i = j

                else:
                    # Failed to find closing bracket, treat opening bracket as a
                    # bracket literal instead of as an expression.
                    regex += "\\["

            else:
                # Regular character, escape it for regex.
                regex += re.escape(char)

        if escape:
            raise ValueError(
                f"Escape character found with no next character to escape: {pattern!r}"
            )

        return regex

    @staticmethod
    def escape(s: AnyStr) -> AnyStr:
        """
        Escape special characters in the given string.

        *s* (:class:`str` or :class:`bytes`) a filename or a string that you
        want to escape, usually before adding it to a ".gitignore".

        Returns the escaped string (:class:`str` or :class:`bytes`).
        """
        if isinstance(s, str):
            return_type = str
            string = s
        elif isinstance(s, bytes):
            return_type = bytes
            string = s.decode(_BYTES_ENCODING)
        else:
            raise TypeError(f"s:{s!r} is not a unicode or byte string.")

        # Reference: https://git-scm.com/docs/gitignore#_pattern_format
        meta_characters = r"[]!*#?"

        out_string = "".join("\\" + x if x in meta_characters else x for x in string)

        if return_type is bytes:
            return out_string.encode(_BYTES_ENCODING)
        else:
            return out_string


util.register_pattern("gitwildmatch", GitWildMatchPattern)


class GitIgnorePattern(GitWildMatchPattern):
    """
    The :class:`GitIgnorePattern` class is deprecated by :class:`GitWildMatchPattern`.
    This class only exists to maintain compatibility with v0.4.
    """

    def __init__(self, *args, **kw) -> None:
        """
        Warn about deprecation.
        """
        self._deprecated()
        super(GitIgnorePattern, self).__init__(*args, **kw)

    @staticmethod
    def _deprecated() -> None:
        """
        Warn about deprecation.
        """
        warnings.warn(
            (
                "GitIgnorePattern ('gitignore') is deprecated. Use "
                "GitWildMatchPattern ('gitwildmatch') instead."
            ),
            DeprecationWarning,
            stacklevel=3,
        )

    @classmethod
    def pattern_to_regex(cls, *args, **kw):
        """
        Warn about deprecation.
        """
        cls._deprecated()
        return super(GitIgnorePattern, cls).pattern_to_regex(*args, **kw)


# Register `GitIgnorePattern` as "gitignore" for backward compatibility
# with v0.4.
util.register_pattern("gitignore", GitIgnorePattern)
