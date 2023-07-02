"""
This module provides :class:`.GitIgnoreSpec` which replicates
*.gitignore* behavior.
"""

from typing import AnyStr, Callable, Collection, Iterable, Type, TypeVar, Union

from .pathspec import PathSpec
from .pattern import Pattern
from .patterns.gitwildmatch import (
    _DIR_MARK,
    GitWildMatchPattern,
    GitWildMatchPatternError,
)
from .util import _is_iterable

Self = TypeVar("Self", bound="GitIgnoreSpec")
"""
:class:`GitIgnoreSpec` self type hint to support Python v<3.11 using PEP
673 recommendation.
"""


class GitIgnoreSpec(PathSpec):
    """
    The :class:`GitIgnoreSpec` class extends :class:`PathSpec` to
    replicate *.gitignore* behavior.
    """

    def __eq__(self, other: object) -> bool:
        """
        Tests the equality of this gitignore-spec with *other*
        (:class:`GitIgnoreSpec`) by comparing their :attr:`~PathSpec.patterns`
        attributes. A non-:class:`GitIgnoreSpec` will not compare equal.
        """
        if isinstance(other, GitIgnoreSpec):
            return super().__eq__(other)
        elif isinstance(other, PathSpec):
            return False
        else:
            return NotImplemented

    @classmethod
    def from_lines(
        cls: Type[Self],
        lines: Iterable[AnyStr],
        pattern_factory: Union[str, Callable[[AnyStr], Pattern], None] = None,
    ) -> Self:
        """
        Compiles the pattern lines.

        *lines* (:class:`~collections.abc.Iterable`) yields each uncompiled
        pattern (:class:`str`). This simply has to yield each line so it can
        be a :class:`io.TextIOBase` (e.g., from :func:`open` or
        :class:`io.StringIO`) or the result from :meth:`str.splitlines`.

        *pattern_factory* can be :data:`None`, the name of a registered
        pattern factory (:class:`str`), or a :class:`~collections.abc.Callable`
        used to compile patterns. The callable must accept an uncompiled
        pattern (:class:`str`) and return the compiled pattern (:class:`.Pattern`).
        Default is :data:`None` for :class:`.GitWildMatchPattern`).

        Returns the :class:`GitIgnoreSpec` instance.
        """
        if pattern_factory is None:
            pattern_factory = GitWildMatchPattern

        elif (isinstance(lines, str) or callable(lines)) and _is_iterable(
            pattern_factory
        ):
            # Support reversed order of arguments from PathSpec.
            pattern_factory, lines = lines, pattern_factory

        self = super().from_lines(pattern_factory, lines)
        return self  # type: ignore

    @staticmethod
    def _match_file(
        patterns: Collection[GitWildMatchPattern],
        file: str,
    ) -> bool:
        """
        Matches the file to the patterns.

        .. NOTE:: Subclasses of :class:`.PathSpec` may override this
           method as an instance method. It does not have to be a static
           method.

        *patterns* (:class:`~collections.abc.Iterable` of :class:`~pathspec.pattern.Pattern`)
        contains the patterns to use.

        *file* (:class:`str`) is the normalized file path to be matched
        against *patterns*.

        Returns :data:`True` if *file* matched; otherwise, :data:`False`.
        """
        out_matched = False
        out_priority = 0
        for pattern in patterns:
            if pattern.include is not None:
                match = pattern.match_file(file)
                if match is not None:
                    # Pattern matched.

                    # Check for directory marker.
                    try:
                        dir_mark = match.match.group(_DIR_MARK)
                    except IndexError as e:
                        # NOTICE: The exact content of this error message is subject
                        # to change.
                        raise GitWildMatchPatternError(
                            (
                                f"Invalid git pattern: directory marker regex group is missing. "
                                f"Debug: file={file!r} regex={pattern.regex!r} "
                                f"group={_DIR_MARK!r} match={match.match!r}."
                            )
                        ) from e

                    if dir_mark:
                        # Pattern matched by a directory pattern.
                        priority = 1
                    else:
                        # Pattern matched by a file pattern.
                        priority = 2

                    if pattern.include and dir_mark:
                        out_matched = pattern.include
                        out_priority = priority
                    elif priority >= out_priority:
                        out_matched = pattern.include
                        out_priority = priority

        return out_matched
