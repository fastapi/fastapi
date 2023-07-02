from collections.abc import Callable
from re import Pattern

__all__ = ["TextWrapper", "wrap", "fill", "dedent", "indent", "shorten"]

class TextWrapper:
    width: int
    initial_indent: str
    subsequent_indent: str
    expand_tabs: bool
    replace_whitespace: bool
    fix_sentence_endings: bool
    drop_whitespace: bool
    break_long_words: bool
    break_on_hyphens: bool
    tabsize: int
    max_lines: int | None
    placeholder: str

    # Attributes not present in documentation
    sentence_end_re: Pattern[str]
    wordsep_re: Pattern[str]
    wordsep_simple_re: Pattern[str]
    whitespace_trans: str
    unicode_whitespace_trans: dict[int, int]
    uspace: int
    x: str  # leaked loop variable
    def __init__(
        self,
        width: int = 70,
        initial_indent: str = "",
        subsequent_indent: str = "",
        expand_tabs: bool = True,
        replace_whitespace: bool = True,
        fix_sentence_endings: bool = False,
        break_long_words: bool = True,
        drop_whitespace: bool = True,
        break_on_hyphens: bool = True,
        tabsize: int = 8,
        *,
        max_lines: int | None = None,
        placeholder: str = " [...]",
    ) -> None: ...
    # Private methods *are* part of the documented API for subclasses.
    def _munge_whitespace(self, text: str) -> str: ...
    def _split(self, text: str) -> list[str]: ...
    def _fix_sentence_endings(self, chunks: list[str]) -> None: ...
    def _handle_long_word(
        self, reversed_chunks: list[str], cur_line: list[str], cur_len: int, width: int
    ) -> None: ...
    def _wrap_chunks(self, chunks: list[str]) -> list[str]: ...
    def _split_chunks(self, text: str) -> list[str]: ...
    def wrap(self, text: str) -> list[str]: ...
    def fill(self, text: str) -> str: ...

def wrap(
    text: str,
    width: int = 70,
    *,
    initial_indent: str = "",
    subsequent_indent: str = "",
    expand_tabs: bool = True,
    tabsize: int = 8,
    replace_whitespace: bool = True,
    fix_sentence_endings: bool = False,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    drop_whitespace: bool = True,
    max_lines: int | None = None,
    placeholder: str = " [...]",
) -> list[str]: ...
def fill(
    text: str,
    width: int = 70,
    *,
    initial_indent: str = "",
    subsequent_indent: str = "",
    expand_tabs: bool = True,
    tabsize: int = 8,
    replace_whitespace: bool = True,
    fix_sentence_endings: bool = False,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    drop_whitespace: bool = True,
    max_lines: int | None = None,
    placeholder: str = " [...]",
) -> str: ...
def shorten(
    text: str,
    width: int,
    *,
    initial_indent: str = "",
    subsequent_indent: str = "",
    expand_tabs: bool = True,
    tabsize: int = 8,
    replace_whitespace: bool = True,
    fix_sentence_endings: bool = False,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    drop_whitespace: bool = True,
    # Omit `max_lines: int = None`, it is forced to 1 here.
    placeholder: str = " [...]",
) -> str: ...
def dedent(text: str) -> str: ...
def indent(
    text: str, prefix: str, predicate: Callable[[str], bool] | None = None
) -> str: ...
