"""Unit tests for RArray types."""

from __future__ import annotations

import unittest

from mypyc.common import PLATFORM_SIZE
from mypyc.ir.rtypes import (
    RArray,
    bool_rprimitive,
    compute_rtype_alignment,
    compute_rtype_size,
    int_rprimitive,
)


class TestRArray(unittest.TestCase):
    def test_basics(self) -> None:
        a = RArray(int_rprimitive, 10)
        assert a.item_type == int_rprimitive
        assert a.length == 10

    def test_str_conversion(self) -> None:
        a = RArray(int_rprimitive, 10)
        assert str(a) == "int[10]"
        assert repr(a) == "<RArray <RPrimitive builtins.int>[10]>"

    def test_eq(self) -> None:
        a = RArray(int_rprimitive, 10)
        assert a == RArray(int_rprimitive, 10)
        assert a != RArray(bool_rprimitive, 10)
        assert a != RArray(int_rprimitive, 9)

    def test_hash(self) -> None:
        assert hash(RArray(int_rprimitive, 10)) == hash(RArray(int_rprimitive, 10))
        assert hash(RArray(bool_rprimitive, 5)) == hash(RArray(bool_rprimitive, 5))

    def test_alignment(self) -> None:
        a = RArray(int_rprimitive, 10)
        assert compute_rtype_alignment(a) == PLATFORM_SIZE
        b = RArray(bool_rprimitive, 55)
        assert compute_rtype_alignment(b) == 1

    def test_size(self) -> None:
        a = RArray(int_rprimitive, 9)
        assert compute_rtype_size(a) == 9 * PLATFORM_SIZE
        b = RArray(bool_rprimitive, 3)
        assert compute_rtype_size(b) == 3
