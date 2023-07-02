from __future__ import annotations

import unittest

from mypyc.ir.class_ir import ClassIR
from mypyc.ir.rtypes import (
    RInstance,
    RTuple,
    RUnion,
    bool_rprimitive,
    int_rprimitive,
    list_rprimitive,
    object_rprimitive,
)


class TestTupleNames(unittest.TestCase):
    def setUp(self) -> None:
        self.inst_a = RInstance(ClassIR("A", "__main__"))
        self.inst_b = RInstance(ClassIR("B", "__main__"))

    def test_names(self) -> None:
        assert RTuple([int_rprimitive, int_rprimitive]).unique_id == "T2II"
        assert (
            RTuple([list_rprimitive, object_rprimitive, self.inst_a]).unique_id
            == "T3OOO"
        )
        assert (
            RTuple([list_rprimitive, object_rprimitive, self.inst_b]).unique_id
            == "T3OOO"
        )
        assert RTuple([]).unique_id == "T0"
        assert (
            RTuple([RTuple([]), RTuple([int_rprimitive, int_rprimitive])]).unique_id
            == "T2T0T2II"
        )
        assert (
            RTuple(
                [bool_rprimitive, RUnion([bool_rprimitive, int_rprimitive])]
            ).unique_id
            == "T2CO"
        )
