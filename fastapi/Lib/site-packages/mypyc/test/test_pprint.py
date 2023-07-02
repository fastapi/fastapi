from __future__ import annotations

import unittest

from mypyc.ir.ops import Assign, BasicBlock, Integer, IntOp, Op, Register, Unreachable
from mypyc.ir.pprint import generate_names_for_ir
from mypyc.ir.rtypes import int_rprimitive


def register(name: str) -> Register:
    return Register(int_rprimitive, "foo", is_arg=True)


def make_block(ops: list[Op]) -> BasicBlock:
    block = BasicBlock()
    block.ops.extend(ops)
    return block


class TestGenerateNames(unittest.TestCase):
    def test_empty(self) -> None:
        assert generate_names_for_ir([], []) == {}

    def test_arg(self) -> None:
        reg = register("foo")
        assert generate_names_for_ir([reg], []) == {reg: "foo"}

    def test_int_op(self) -> None:
        n1 = Integer(2)
        n2 = Integer(4)
        op1 = IntOp(int_rprimitive, n1, n2, IntOp.ADD)
        op2 = IntOp(int_rprimitive, op1, n2, IntOp.ADD)
        block = make_block([op1, op2, Unreachable()])
        assert generate_names_for_ir([], [block]) == {op1: "r0", op2: "r1"}

    def test_assign(self) -> None:
        reg = register("foo")
        n = Integer(2)
        op1 = Assign(reg, n)
        op2 = Assign(reg, n)
        block = make_block([op1, op2])
        assert generate_names_for_ir([reg], [block]) == {reg: "foo"}
