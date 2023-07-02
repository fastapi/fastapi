from __future__ import annotations

from mypy.erasetype import erase_typevars
from mypy.nodes import TypeInfo
from mypy.types import (
    AnyType,
    Instance,
    ParamSpecType,
    TupleType,
    Type,
    TypeOfAny,
    TypeVarLikeType,
    TypeVarTupleType,
    TypeVarType,
    UnpackType,
)


def fill_typevars(typ: TypeInfo) -> Instance | TupleType:
    """For a non-generic type, return instance type representing the type.

    For a generic G type with parameters T1, .., Tn, return G[T1, ..., Tn].
    """
    tvs: list[Type] = []
    # TODO: why do we need to keep both typ.type_vars and typ.defn.type_vars?
    for i in range(len(typ.defn.type_vars)):
        tv: TypeVarLikeType | UnpackType = typ.defn.type_vars[i]
        # Change the line number
        if isinstance(tv, TypeVarType):
            tv = tv.copy_modified(line=-1, column=-1)
        elif isinstance(tv, TypeVarTupleType):
            tv = UnpackType(
                TypeVarTupleType(
                    tv.name,
                    tv.fullname,
                    tv.id,
                    tv.upper_bound,
                    tv.tuple_fallback,
                    tv.default,
                    line=-1,
                    column=-1,
                )
            )
        else:
            assert isinstance(tv, ParamSpecType)
            tv = ParamSpecType(
                tv.name,
                tv.fullname,
                tv.id,
                tv.flavor,
                tv.upper_bound,
                tv.default,
                line=-1,
                column=-1,
            )
        tvs.append(tv)
    inst = Instance(typ, tvs)
    if typ.tuple_type is None:
        return inst
    return typ.tuple_type.copy_modified(fallback=inst)


def fill_typevars_with_any(typ: TypeInfo) -> Instance | TupleType:
    """Apply a correct number of Any's as type arguments to a type."""
    inst = Instance(typ, [AnyType(TypeOfAny.special_form)] * len(typ.defn.type_vars))
    if typ.tuple_type is None:
        return inst
    return typ.tuple_type.copy_modified(fallback=inst)


def has_no_typevars(typ: Type) -> bool:
    # We test if a type contains type variables by erasing all type variables
    # and comparing the result to the original type. We use comparison by equality that
    # in turn uses `__eq__` defined for types. Note: we can't use `is_same_type` because
    # it is not safe with unresolved forward references, while this function may be called
    # before forward references resolution patch pass. Note also that it is not safe to use
    # `is` comparison because `erase_typevars` doesn't preserve type identity.
    return typ == erase_typevars(typ)
