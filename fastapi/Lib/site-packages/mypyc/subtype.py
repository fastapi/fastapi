"""Subtype check for RTypes."""

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
    is_fixed_width_rtype,
    is_int_rprimitive,
    is_object_rprimitive,
    is_short_int_rprimitive,
    is_tagged,
    is_tuple_rprimitive,
)


def is_subtype(left: RType, right: RType) -> bool:
    if is_object_rprimitive(right):
        return True
    elif isinstance(right, RUnion):
        if isinstance(left, RUnion):
            for left_item in left.items:
                if not any(
                    is_subtype(left_item, right_item) for right_item in right.items
                ):
                    return False
            return True
        else:
            return any(is_subtype(left, item) for item in right.items)
    return left.accept(SubtypeVisitor(right))


class SubtypeVisitor(RTypeVisitor[bool]):
    """Is left a subtype of right?

    A few special cases such as right being 'object' are handled in
    is_subtype and don't need to be covered here.
    """

    def __init__(self, right: RType) -> None:
        self.right = right

    def visit_rinstance(self, left: RInstance) -> bool:
        return (
            isinstance(self.right, RInstance)
            and self.right.class_ir in left.class_ir.mro
        )

    def visit_runion(self, left: RUnion) -> bool:
        return all(is_subtype(item, self.right) for item in left.items)

    def visit_rprimitive(self, left: RPrimitive) -> bool:
        right = self.right
        if is_bool_rprimitive(left):
            if is_tagged(right) or is_fixed_width_rtype(right):
                return True
        elif is_bit_rprimitive(left):
            if (
                is_bool_rprimitive(right)
                or is_tagged(right)
                or is_fixed_width_rtype(right)
            ):
                return True
        elif is_short_int_rprimitive(left):
            if is_int_rprimitive(right):
                return True
        elif is_fixed_width_rtype(left):
            if is_int_rprimitive(right):
                return True
        return left is right

    def visit_rtuple(self, left: RTuple) -> bool:
        if is_tuple_rprimitive(self.right):
            return True
        if isinstance(self.right, RTuple):
            return len(self.right.types) == len(left.types) and all(
                is_subtype(t1, t2) for t1, t2 in zip(left.types, self.right.types)
            )
        return False

    def visit_rstruct(self, left: RStruct) -> bool:
        return isinstance(self.right, RStruct) and self.right.name == left.name

    def visit_rarray(self, left: RArray) -> bool:
        return left == self.right

    def visit_rvoid(self, left: RVoid) -> bool:
        return isinstance(self.right, RVoid)
