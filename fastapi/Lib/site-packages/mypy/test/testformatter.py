from __future__ import annotations

from unittest import TestCase, main

from mypy.util import split_words, trim_source_line


class FancyErrorFormattingTestCases(TestCase):
    def test_trim_source(self) -> None:
        assert trim_source_line("0123456789abcdef", max_len=16, col=5, min_width=2) == (
            "0123456789abcdef",
            0,
        )

        # Locations near start.
        assert trim_source_line("0123456789abcdef", max_len=7, col=0, min_width=2) == (
            "0123456...",
            0,
        )
        assert trim_source_line("0123456789abcdef", max_len=7, col=4, min_width=2) == (
            "0123456...",
            0,
        )

        # Middle locations.
        assert trim_source_line("0123456789abcdef", max_len=7, col=5, min_width=2) == (
            "...1234567...",
            -2,
        )
        assert trim_source_line("0123456789abcdef", max_len=7, col=6, min_width=2) == (
            "...2345678...",
            -1,
        )
        assert trim_source_line("0123456789abcdef", max_len=7, col=8, min_width=2) == (
            "...456789a...",
            1,
        )

        # Locations near the end.
        assert trim_source_line("0123456789abcdef", max_len=7, col=11, min_width=2) == (
            "...789abcd...",
            4,
        )
        assert trim_source_line("0123456789abcdef", max_len=7, col=13, min_width=2) == (
            "...9abcdef",
            6,
        )
        assert trim_source_line("0123456789abcdef", max_len=7, col=15, min_width=2) == (
            "...9abcdef",
            6,
        )

    def test_split_words(self) -> None:
        assert split_words("Simple message") == ["Simple", "message"]
        assert split_words('Message with "Some[Long, Types]"' " in it") == [
            "Message",
            "with",
            '"Some[Long, Types]"',
            "in",
            "it",
        ]
        assert split_words('Message with "Some[Long, Types]"' " and [error-code]") == [
            "Message",
            "with",
            '"Some[Long, Types]"',
            "and",
            "[error-code]",
        ]
        assert split_words('"Type[Stands, First]" then words') == [
            '"Type[Stands, First]"',
            "then",
            "words",
        ]
        assert split_words('First words "Then[Stands, Type]"') == [
            "First",
            "words",
            '"Then[Stands, Type]"',
        ]
        assert split_words('"Type[Only, Here]"') == ['"Type[Only, Here]"']
        assert split_words("OneWord") == ["OneWord"]
        assert split_words(" ") == ["", ""]


if __name__ == "__main__":
    main()
