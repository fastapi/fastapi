from __future__ import annotations

from typing import Iterable

from mypy_extensions import trait

from mypy.types import (
    AnyType,
    CallableArgument,
    CallableType,
    DeletedType,
    EllipsisType,
    ErasedType,
    Instance,
    LiteralType,
    NoneType,
    Overloaded,
    Parameters,
    ParamSpecType,
    PartialType,
    PlaceholderType,
    RawExpressionType,
    SyntheticTypeVisitor,
    TupleType,
    Type,
    TypeAliasType,
    TypedDictType,
    TypeList,
    TypeType,
    TypeVarTupleType,
    TypeVarType,
    UnboundType,
    UninhabitedType,
    UnionType,
    UnpackType,
)


@trait
class TypeTraverserVisitor(SyntheticTypeVisitor[None]):
    """Visitor that traverses all components of a type"""

    # Atomic types

    def visit_any(self, t: AnyType) -> None:
        pass

    def visit_uninhabited_type(self, t: UninhabitedType) -> None:
        pass

    def visit_none_type(self, t: NoneType) -> None:
        pass

    def visit_erased_type(self, t: ErasedType) -> None:
        pass

    def visit_deleted_type(self, t: DeletedType) -> None:
        pass

    def visit_type_var(self, t: TypeVarType) -> None:
        # Note that type variable values and upper bound aren't treated as
        # components, since they are components of the type variable
        # definition. We want to traverse everything just once.
        pass

    def visit_param_spec(self, t: ParamSpecType) -> None:
        pass

    def visit_parameters(self, t: Parameters) -> None:
        self.traverse_types(t.arg_types)

    def visit_type_var_tuple(self, t: TypeVarTupleType) -> None:
        pass

    def visit_literal_type(self, t: LiteralType) -> None:
        t.fallback.accept(self)

    # Composite types

    def visit_instance(self, t: Instance) -> None:
        self.traverse_types(t.args)

    def visit_callable_type(self, t: CallableType) -> None:
        # FIX generics
        self.traverse_types(t.arg_types)
        t.ret_type.accept(self)
        t.fallback.accept(self)

    def visit_tuple_type(self, t: TupleType) -> None:
        self.traverse_types(t.items)
        t.partial_fallback.accept(self)

    def visit_typeddict_type(self, t: TypedDictType) -> None:
        self.traverse_types(t.items.values())
        t.fallback.accept(self)

    def visit_union_type(self, t: UnionType) -> None:
        self.traverse_types(t.items)

    def visit_overloaded(self, t: Overloaded) -> None:
        self.traverse_types(t.items)

    def visit_type_type(self, t: TypeType) -> None:
        t.item.accept(self)

    # Special types (not real types)

    def visit_callable_argument(self, t: CallableArgument) -> None:
        t.typ.accept(self)

    def visit_unbound_type(self, t: UnboundType) -> None:
        self.traverse_types(t.args)

    def visit_type_list(self, t: TypeList) -> None:
        self.traverse_types(t.items)

    def visit_ellipsis_type(self, t: EllipsisType) -> None:
        pass

    def visit_placeholder_type(self, t: PlaceholderType) -> None:
        self.traverse_types(t.args)

    def visit_partial_type(self, t: PartialType) -> None:
        pass

    def visit_raw_expression_type(self, t: RawExpressionType) -> None:
        pass

    def visit_type_alias_type(self, t: TypeAliasType) -> None:
        # TODO: sometimes we want to traverse target as well
        # We need to find a way to indicate explicitly the intent,
        # maybe make this method abstract (like for TypeTranslator)?
        self.traverse_types(t.args)

    def visit_unpack_type(self, t: UnpackType) -> None:
        t.type.accept(self)

    # Helpers

    def traverse_types(self, types: Iterable[Type]) -> None:
        for typ in types:
            typ.accept(self)
