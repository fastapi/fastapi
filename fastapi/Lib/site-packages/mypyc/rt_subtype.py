"""'Runtime subtype' check for RTypes.

A type S is a runtime subtype of T if a value of type S can be used at runtime
when a value of type T is expected without requiring any runtime conversions.

For boxed types, runtime subtyping is the same as regular subtyping.
Unboxed subtypes, on the other hand, are not runtime subtypes of object
(since they require boxing to be used as an object), but short ints
are runtime subtypes of int.

Subtyping is used to determine whether an object can be in a
particular place and runtime subtyping is used to determine whether a
coercion is necessary first.
"""

from __future__ import annotations

from mypyc.ir.rtypes import (
    RArray,
    RInstance,
    RPrimitive,
    RStruct,
    RTuple,
    RType,
    RTypeVisitor,
    RUnion,
    RVoid,
    is_bit_rprimitive,
    is_bool_rprimitive,
    is_int_rprimitive,
    is_short_int_rprimitive,
)
from mypyc.subtype import is_subtype


def is_runtime_subtype(left: RType, right: RType) -> bool:
    return left.accept(RTSubtypeVisitor(right))


class RTSubtypeVisitor(RTypeVisitor[bool]):
    """Is left a runtime subtype of right?

    A few special cases such as right being 'object' are handled in
    is_runtime_subtype and don't need to be covered here.
    """

    def __init__(self, right: RType) -> None:
        self.right = right

    def visit_rinstance(self, left: RInstance) -> bool:
        return is_subtype(left, self.right)

    def visit_runion(self, left: RUnion) -> bool:
        return not self.right.is_unboxed and is_subtype(left, self.right)

    def visit_rprimitive(self, left: RPrimitive) -> bool:
        if is_short_int_rprimitive(left) and is_int_rprimitive(self.right):
            return True
        if is_bit_rprimitive(left) and is_bool_rprimitive(self.right):
            return True
        return left is self.right

    def visit_rtuple(self, left: RTuple) -> bool:
        if isinstance(self.right, RTuple):
            return len(self.right.types) == len(left.types) and all(
                is_runtime_subtype(t1, t2)
                for t1, t2 in zip(left.types, self.right.types)
            )
        return False

    def visit_rstruct(self, left: RStruct) -> bool:
        return isinstance(self.right, RStruct) and self.right.name == left.name

    def visit_rarray(self, left: RArray) -> bool:
        return left == self.right

    def visit_rvoid(self, left: RVoid) -> bool:
        return isinstance(self.right, RVoid)
