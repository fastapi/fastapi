from __future__ import annotations

import unittest

from mypyc.codegen.emitclass import getter_name, setter_name, slot_key
from mypyc.ir.class_ir import ClassIR
from mypyc.namegen import NameGenerator


class TestEmitClass(unittest.TestCase):
    def test_slot_key(self) -> None:
        attrs = [
            "__add__",
            "__radd__",
            "__rshift__",
            "__rrshift__",
            "__setitem__",
            "__delitem__",
        ]
        s = sorted(attrs, key=lambda x: slot_key(x))
        # __delitem__ and reverse methods should come last.
        assert s == [
            "__add__",
            "__rshift__",
            "__setitem__",
            "__delitem__",
            "__radd__",
            "__rrshift__",
        ]

    def test_setter_name(self) -> None:
        cls = ClassIR(module_name="testing", name="SomeClass")
        generator = NameGenerator([["mod"]])

        # This should never be `setup`, as it will conflict with the class `setup`
        assert setter_name(cls, "up", generator) == "testing___SomeClass_set_up"

    def test_getter_name(self) -> None:
        cls = ClassIR(module_name="testing", name="SomeClass")
        generator = NameGenerator([["mod"]])

        assert getter_name(cls, "down", generator) == "testing___SomeClass_get_down"
