from __future__ import annotations

from typing import Iterable, Set

import mypy.types as types
from mypy.types import TypeVisitor
from mypy.util import split_module_names


def extract_module_names(type_name: str | None) -> list[str]:
    """Returns the module names of a fully qualified type name."""
    if type_name is not None:
        # Discard the first one, which is just the qualified name of the type
        possible_module_names = split_module_names(type_name)
        return possible_module_names[1:]
    else:
        return []


class TypeIndirectionVisitor(TypeVisitor[Set[str]]):
    """Returns all module references within a particular type."""

    def __init__(self) -> None:
        self.cache: dict[types.Type, set[str]] = {}
        self.seen_aliases: set[types.TypeAliasType] = set()

    def find_modules(self, typs: Iterable[types.Type]) -> set[str]:
        self.seen_aliases.clear()
        return self._visit(typs)

    def _visit(self, typ_or_typs: types.Type | Iterable[types.Type]) -> set[str]:
        typs = [typ_or_typs] if isinstance(typ_or_typs, types.Type) else typ_or_typs
        output: set[str] = set()
        for typ in typs:
            if isinstance(typ, types.TypeAliasType):
                # Avoid infinite recursion for recursive type aliases.
                if typ in self.seen_aliases:
                    continue
                self.seen_aliases.add(typ)
            if typ in self.cache:
                modules = self.cache[typ]
            else:
                modules = typ.accept(self)
                self.cache[typ] = set(modules)
            output.update(modules)
        return output

    def visit_unbound_type(self, t: types.UnboundType) -> set[str]:
        return self._visit(t.args)

    def visit_any(self, t: types.AnyType) -> set[str]:
        return set()

    def visit_none_type(self, t: types.NoneType) -> set[str]:
        return set()

    def visit_uninhabited_type(self, t: types.UninhabitedType) -> set[str]:
        return set()

    def visit_erased_type(self, t: types.ErasedType) -> set[str]:
        return set()

    def visit_deleted_type(self, t: types.DeletedType) -> set[str]:
        return set()

    def visit_type_var(self, t: types.TypeVarType) -> set[str]:
        return (
            self._visit(t.values) | self._visit(t.upper_bound) | self._visit(t.default)
        )

    def visit_param_spec(self, t: types.ParamSpecType) -> set[str]:
        return self._visit(t.upper_bound) | self._visit(t.default)

    def visit_type_var_tuple(self, t: types.TypeVarTupleType) -> set[str]:
        return self._visit(t.upper_bound) | self._visit(t.default)

    def visit_unpack_type(self, t: types.UnpackType) -> set[str]:
        return t.type.accept(self)

    def visit_parameters(self, t: types.Parameters) -> set[str]:
        return self._visit(t.arg_types)

    def visit_instance(self, t: types.Instance) -> set[str]:
        out = self._visit(t.args)
        if t.type:
            # Uses of a class depend on everything in the MRO,
            # as changes to classes in the MRO can add types to methods,
            # change property types, change the MRO itself, etc.
            for s in t.type.mro:
                out.update(split_module_names(s.module_name))
            if t.type.metaclass_type is not None:
                out.update(split_module_names(t.type.metaclass_type.type.module_name))
        return out

    def visit_callable_type(self, t: types.CallableType) -> set[str]:
        out = self._visit(t.arg_types) | self._visit(t.ret_type)
        if t.definition is not None:
            out.update(extract_module_names(t.definition.fullname))
        return out

    def visit_overloaded(self, t: types.Overloaded) -> set[str]:
        return self._visit(t.items) | self._visit(t.fallback)

    def visit_tuple_type(self, t: types.TupleType) -> set[str]:
        return self._visit(t.items) | self._visit(t.partial_fallback)

    def visit_typeddict_type(self, t: types.TypedDictType) -> set[str]:
        return self._visit(t.items.values()) | self._visit(t.fallback)

    def visit_literal_type(self, t: types.LiteralType) -> set[str]:
        return self._visit(t.fallback)

    def visit_union_type(self, t: types.UnionType) -> set[str]:
        return self._visit(t.items)

    def visit_partial_type(self, t: types.PartialType) -> set[str]:
        return set()

    def visit_type_type(self, t: types.TypeType) -> set[str]:
        return self._visit(t.item)

    def visit_type_alias_type(self, t: types.TypeAliasType) -> set[str]:
        return self._visit(types.get_proper_type(t))
