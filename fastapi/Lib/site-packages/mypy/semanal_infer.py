"""Simple type inference for decorated functions during semantic analysis."""

from __future__ import annotations

from mypy.nodes import ARG_POS, CallExpr, Decorator, Expression, FuncDef, RefExpr, Var
from mypy.semanal_shared import SemanticAnalyzerInterface
from mypy.typeops import function_type
from mypy.types import (
    AnyType,
    CallableType,
    ProperType,
    Type,
    TypeOfAny,
    TypeVarType,
    get_proper_type,
)
from mypy.typevars import has_no_typevars


def infer_decorator_signature_if_simple(
    dec: Decorator, analyzer: SemanticAnalyzerInterface
) -> None:
    """Try to infer the type of the decorated function.

    This lets us resolve additional references to decorated functions
    during type checking. Otherwise the type might not be available
    when we need it, since module top levels can't be deferred.

    This basically uses a simple special-purpose type inference
    engine just for decorators.
    """
    if dec.var.is_property:
        # Decorators are expected to have a callable type (it's a little odd).
        if dec.func.type is None:
            dec.var.type = CallableType(
                [AnyType(TypeOfAny.special_form)],
                [ARG_POS],
                [None],
                AnyType(TypeOfAny.special_form),
                analyzer.named_type("builtins.function"),
                name=dec.var.name,
            )
        elif isinstance(dec.func.type, CallableType):
            dec.var.type = dec.func.type
        return
    decorator_preserves_type = True
    for expr in dec.decorators:
        preserve_type = False
        if isinstance(expr, RefExpr) and isinstance(expr.node, FuncDef):
            if expr.node.type and is_identity_signature(expr.node.type):
                preserve_type = True
        if not preserve_type:
            decorator_preserves_type = False
            break
    if decorator_preserves_type:
        # No non-identity decorators left. We can trivially infer the type
        # of the function here.
        dec.var.type = function_type(dec.func, analyzer.named_type("builtins.function"))
    if dec.decorators:
        return_type = calculate_return_type(dec.decorators[0])
        if return_type and isinstance(return_type, AnyType):
            # The outermost decorator will return Any so we know the type of the
            # decorated function.
            dec.var.type = AnyType(TypeOfAny.from_another_any, source_any=return_type)
        sig = find_fixed_callable_return(dec.decorators[0])
        if sig:
            # The outermost decorator always returns the same kind of function,
            # so we know that this is the type of the decorated function.
            orig_sig = function_type(dec.func, analyzer.named_type("builtins.function"))
            sig.name = orig_sig.items[0].name
            dec.var.type = sig


def is_identity_signature(sig: Type) -> bool:
    """Is type a callable of form T -> T (where T is a type variable)?"""
    sig = get_proper_type(sig)
    if isinstance(sig, CallableType) and sig.arg_kinds == [ARG_POS]:
        if isinstance(sig.arg_types[0], TypeVarType) and isinstance(
            sig.ret_type, TypeVarType
        ):
            return sig.arg_types[0].id == sig.ret_type.id
    return False


def calculate_return_type(expr: Expression) -> ProperType | None:
    """Return the return type if we can calculate it.

    This only uses information available during semantic analysis so this
    will sometimes return None because of insufficient information (as
    type inference hasn't run yet).
    """
    if isinstance(expr, RefExpr):
        if isinstance(expr.node, FuncDef):
            typ = expr.node.type
            if typ is None:
                # No signature -> default to Any.
                return AnyType(TypeOfAny.unannotated)
            # Explicit Any return?
            if isinstance(typ, CallableType):
                return get_proper_type(typ.ret_type)
            return None
        elif isinstance(expr.node, Var):
            return get_proper_type(expr.node.type)
    elif isinstance(expr, CallExpr):
        return calculate_return_type(expr.callee)
    return None


def find_fixed_callable_return(expr: Expression) -> CallableType | None:
    """Return the return type, if expression refers to a callable that returns a callable.

    But only do this if the return type has no type variables. Return None otherwise.
    This approximates things a lot as this is supposed to be called before type checking
    when full type information is not available yet.
    """
    if isinstance(expr, RefExpr):
        if isinstance(expr.node, FuncDef):
            typ = expr.node.type
            if typ:
                if isinstance(typ, CallableType) and has_no_typevars(typ.ret_type):
                    ret_type = get_proper_type(typ.ret_type)
                    if isinstance(ret_type, CallableType):
                        return ret_type
    elif isinstance(expr, CallExpr):
        t = find_fixed_callable_return(expr.callee)
        if t:
            ret_type = get_proper_type(t.ret_type)
            if isinstance(ret_type, CallableType):
                return ret_type
    return None
