from __future__ import annotations

import unittest

from mypyc.namegen import (
    NameGenerator,
    candidate_suffixes,
    exported_name,
    make_module_translation_map,
)


class TestNameGen(unittest.TestCase):
    def test_candidate_suffixes(self) -> None:
        assert candidate_suffixes("foo") == ["", "foo."]
        assert candidate_suffixes("foo.bar") == ["", "bar.", "foo.bar."]

    def test_exported_name(self) -> None:
        assert exported_name("foo") == "foo"
        assert exported_name("foo.bar") == "foo___bar"

    def test_make_module_translation_map(self) -> None:
        assert make_module_translation_map(["foo", "bar"]) == {
            "foo": "foo.",
            "bar": "bar.",
        }
        assert make_module_translation_map(["foo.bar", "foo.baz"]) == {
            "foo.bar": "bar.",
            "foo.baz": "baz.",
        }
        assert make_module_translation_map(["zar", "foo.bar", "foo.baz"]) == {
            "foo.bar": "bar.",
            "foo.baz": "baz.",
            "zar": "zar.",
        }
        assert make_module_translation_map(["foo.bar", "fu.bar", "foo.baz"]) == {
            "foo.bar": "foo.bar.",
            "fu.bar": "fu.bar.",
            "foo.baz": "baz.",
        }

    def test_name_generator(self) -> None:
        g = NameGenerator([["foo", "foo.zar"]])
        assert g.private_name("foo", "f") == "foo___f"
        assert g.private_name("foo", "C.x.y") == "foo___C___x___y"
        assert g.private_name("foo", "C.x.y") == "foo___C___x___y"
        assert g.private_name("foo.zar", "C.x.y") == "zar___C___x___y"
        assert g.private_name("foo", "C.x_y") == "foo___C___x_y"
        assert g.private_name("foo", "C_x_y") == "foo___C_x_y"
        assert g.private_name("foo", "C_x_y") == "foo___C_x_y"
        assert g.private_name("foo", "___") == "foo______3_"
