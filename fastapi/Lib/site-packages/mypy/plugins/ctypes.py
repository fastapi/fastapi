"""Plugin to provide accurate types for some parts of the ctypes module."""

from __future__ import annotations

# Fully qualified instead of "from mypy.plugin import ..." to avoid circular import problems.
import mypy.plugin
from mypy import nodes
from mypy.maptype import map_instance_to_supertype
from mypy.messages import format_type
from mypy.subtypes import is_subtype
from mypy.typeops import make_simplified_union
from mypy.types import (
    AnyType,
    CallableType,
    Instance,
    NoneType,
    ProperType,
    Type,
    TypeOfAny,
    UnionType,
    flatten_nested_unions,
    get_proper_type,
)


def _find_simplecdata_base_arg(
    tp: Instance, api: mypy.plugin.CheckerPluginInterface
) -> ProperType | None:
    """Try to find a parametrized _SimpleCData in tp's bases and return its single type argument.

    None is returned if _SimpleCData appears nowhere in tp's (direct or indirect) bases.
    """
    if tp.type.has_base("_ctypes._SimpleCData"):
        simplecdata_base = map_instance_to_supertype(
            tp,
            api.named_generic_type(
                "_ctypes._SimpleCData", [AnyType(TypeOfAny.special_form)]
            ).type,
        )
        assert (
            len(simplecdata_base.args) == 1
        ), "_SimpleCData takes exactly one type argument"
        return get_proper_type(simplecdata_base.args[0])
    return None


def _autoconvertible_to_cdata(
    tp: Type, api: mypy.plugin.CheckerPluginInterface
) -> Type:
    """Get a type that is compatible with all types that can be implicitly converted to the given
    CData type.

    Examples:
    * c_int -> Union[c_int, int]
    * c_char_p -> Union[c_char_p, bytes, int, NoneType]
    * MyStructure -> MyStructure
    """
    allowed_types = []
    # If tp is a union, we allow all types that are convertible to at least one of the union
    # items. This is not quite correct - strictly speaking, only types convertible to *all* of the
    # union items should be allowed. This may be worth changing in the future, but the more
    # correct algorithm could be too strict to be useful.
    for t in flatten_nested_unions([tp]):
        t = get_proper_type(t)
        # Every type can be converted from itself (obviously).
        allowed_types.append(t)
        if isinstance(t, Instance):
            unboxed = _find_simplecdata_base_arg(t, api)
            if unboxed is not None:
                # If _SimpleCData appears in tp's (direct or indirect) bases, its type argument
                # specifies the type's "unboxed" version, which can always be converted back to
                # the original "boxed" type.
                allowed_types.append(unboxed)

                if t.type.has_base("ctypes._PointerLike"):
                    # Pointer-like _SimpleCData subclasses can also be converted from
                    # an int or None.
                    allowed_types.append(api.named_generic_type("builtins.int", []))
                    allowed_types.append(NoneType())

    return make_simplified_union(allowed_types)


def _autounboxed_cdata(tp: Type) -> ProperType:
    """Get the auto-unboxed version of a CData type, if applicable.

    For *direct* _SimpleCData subclasses, the only type argument of _SimpleCData in the bases list
    is returned.
    For all other CData types, including indirect _SimpleCData subclasses, tp is returned as-is.
    """
    tp = get_proper_type(tp)

    if isinstance(tp, UnionType):
        return make_simplified_union([_autounboxed_cdata(t) for t in tp.items])
    elif isinstance(tp, Instance):
        for base in tp.type.bases:
            if base.type.fullname == "_ctypes._SimpleCData":
                # If tp has _SimpleCData as a direct base class,
                # the auto-unboxed type is the single type argument of the _SimpleCData type.
                assert len(base.args) == 1
                return get_proper_type(base.args[0])
    # If tp is not a concrete type, or if there is no _SimpleCData in the bases,
    # the type is not auto-unboxed.
    return tp


def _get_array_element_type(tp: Type) -> ProperType | None:
    """Get the element type of the Array type tp, or None if not specified."""
    tp = get_proper_type(tp)
    if isinstance(tp, Instance):
        assert tp.type.fullname == "_ctypes.Array"
        if len(tp.args) == 1:
            return get_proper_type(tp.args[0])
    return None


def array_constructor_callback(ctx: mypy.plugin.FunctionContext) -> Type:
    """Callback to provide an accurate signature for the ctypes.Array constructor."""
    # Extract the element type from the constructor's return type, i. e. the type of the array
    # being constructed.
    et = _get_array_element_type(ctx.default_return_type)
    if et is not None:
        allowed = _autoconvertible_to_cdata(et, ctx.api)
        assert (
            len(ctx.arg_types) == 1
        ), "The stub of the ctypes.Array constructor should have a single vararg parameter"
        for arg_num, (arg_kind, arg_type) in enumerate(
            zip(ctx.arg_kinds[0], ctx.arg_types[0]), 1
        ):
            if arg_kind == nodes.ARG_POS and not is_subtype(arg_type, allowed):
                ctx.api.msg.fail(
                    "Array constructor argument {} of type {}"
                    " is not convertible to the array element type {}".format(
                        arg_num,
                        format_type(arg_type, ctx.api.options),
                        format_type(et, ctx.api.options),
                    ),
                    ctx.context,
                )
            elif arg_kind == nodes.ARG_STAR:
                ty = ctx.api.named_generic_type("typing.Iterable", [allowed])
                if not is_subtype(arg_type, ty):
                    it = ctx.api.named_generic_type("typing.Iterable", [et])
                    ctx.api.msg.fail(
                        "Array constructor argument {} of type {}"
                        " is not convertible to the array element type {}".format(
                            arg_num,
                            format_type(arg_type, ctx.api.options),
                            format_type(it, ctx.api.options),
                        ),
                        ctx.context,
                    )

    return ctx.default_return_type


def array_getitem_callback(ctx: mypy.plugin.MethodContext) -> Type:
    """Callback to provide an accurate return type for ctypes.Array.__getitem__."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        unboxed = _autounboxed_cdata(et)
        assert (
            len(ctx.arg_types) == 1
        ), "The stub of ctypes.Array.__getitem__ should have exactly one parameter"
        assert (
            len(ctx.arg_types[0]) == 1
        ), "ctypes.Array.__getitem__'s parameter should not be variadic"
        index_type = get_proper_type(ctx.arg_types[0][0])
        if isinstance(index_type, Instance):
            if index_type.type.has_base("builtins.int"):
                return unboxed
            elif index_type.type.has_base("builtins.slice"):
                return ctx.api.named_generic_type("builtins.list", [unboxed])
    return ctx.default_return_type


def array_setitem_callback(ctx: mypy.plugin.MethodSigContext) -> CallableType:
    """Callback to provide an accurate signature for ctypes.Array.__setitem__."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        allowed = _autoconvertible_to_cdata(et, ctx.api)
        assert len(ctx.default_signature.arg_types) == 2
        index_type = get_proper_type(ctx.default_signature.arg_types[0])
        if isinstance(index_type, Instance):
            arg_type = None
            if index_type.type.has_base("builtins.int"):
                arg_type = allowed
            elif index_type.type.has_base("builtins.slice"):
                arg_type = ctx.api.named_generic_type("builtins.list", [allowed])
            if arg_type is not None:
                # Note: arg_type can only be None if index_type is invalid, in which case we use
                # the default signature and let mypy report an error about it.
                return ctx.default_signature.copy_modified(
                    arg_types=ctx.default_signature.arg_types[:1] + [arg_type]
                )
    return ctx.default_signature


def array_iter_callback(ctx: mypy.plugin.MethodContext) -> Type:
    """Callback to provide an accurate return type for ctypes.Array.__iter__."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        unboxed = _autounboxed_cdata(et)
        return ctx.api.named_generic_type("typing.Iterator", [unboxed])
    return ctx.default_return_type


def array_value_callback(ctx: mypy.plugin.AttributeContext) -> Type:
    """Callback to provide an accurate type for ctypes.Array.value."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        types: list[Type] = []
        for tp in flatten_nested_unions([et]):
            tp = get_proper_type(tp)
            if isinstance(tp, AnyType):
                types.append(AnyType(TypeOfAny.from_another_any, source_any=tp))
            elif isinstance(tp, Instance) and tp.type.fullname == "ctypes.c_char":
                types.append(ctx.api.named_generic_type("builtins.bytes", []))
            elif isinstance(tp, Instance) and tp.type.fullname == "ctypes.c_wchar":
                types.append(ctx.api.named_generic_type("builtins.str", []))
            else:
                ctx.api.msg.fail(
                    'Array attribute "value" is only available'
                    ' with element type "c_char" or "c_wchar", not {}'.format(
                        format_type(et, ctx.api.options)
                    ),
                    ctx.context,
                )
        return make_simplified_union(types)
    return ctx.default_attr_type


def array_raw_callback(ctx: mypy.plugin.AttributeContext) -> Type:
    """Callback to provide an accurate type for ctypes.Array.raw."""
    et = _get_array_element_type(ctx.type)
    if et is not None:
        types: list[Type] = []
        for tp in flatten_nested_unions([et]):
            tp = get_proper_type(tp)
            if (
                isinstance(tp, AnyType)
                or isinstance(tp, Instance)
                and tp.type.fullname == "ctypes.c_char"
            ):
                types.append(ctx.api.named_generic_type("builtins.bytes", []))
            else:
                ctx.api.msg.fail(
                    'Array attribute "raw" is only available'
                    ' with element type "c_char", not {}'.format(
                        format_type(et, ctx.api.options)
                    ),
                    ctx.context,
                )
        return make_simplified_union(types)
    return ctx.default_attr_type
