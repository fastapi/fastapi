from __future__ import annotations

from mypyc.ir.ops import Register, Value
from mypyc.ir.rtypes import RInstance, RType, object_rprimitive


class AssignmentTarget:
    """Abstract base class for assignment targets during IR building."""

    type: RType = object_rprimitive


class AssignmentTargetRegister(AssignmentTarget):
    """Register as an assignment target.

    This is used for local variables and some temporaries.
    """

    def __init__(self, register: Register) -> None:
        self.register = register
        self.type = register.type


class AssignmentTargetIndex(AssignmentTarget):
    """base[index] as assignment target"""

    def __init__(self, base: Value, index: Value) -> None:
        self.base = base
        self.index = index
        # TODO: object_rprimitive won't be right for user-defined classes. Store the
        #       lvalue type in mypy and use a better type to avoid unneeded boxing.
        self.type = object_rprimitive


class AssignmentTargetAttr(AssignmentTarget):
    """obj.attr as assignment target"""

    def __init__(self, obj: Value, attr: str, can_borrow: bool = False) -> None:
        self.obj = obj
        self.attr = attr
        self.can_borrow = can_borrow
        if isinstance(obj.type, RInstance) and obj.type.class_ir.has_attr(attr):
            # Native attribute reference
            self.obj_type: RType = obj.type
            self.type = obj.type.attr_type(attr)
        else:
            # Python attribute reference
            self.obj_type = object_rprimitive
            self.type = object_rprimitive


class AssignmentTargetTuple(AssignmentTarget):
    """x, ..., y as assignment target"""

    def __init__(
        self, items: list[AssignmentTarget], star_idx: int | None = None
    ) -> None:
        self.items = items
        self.star_idx = star_idx
