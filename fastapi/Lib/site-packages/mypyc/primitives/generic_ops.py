"""Fallback primitive operations that operate on 'object' operands.

These just call the relevant Python C API function or a thin wrapper
around an API function. Most of these also have faster, specialized
ops that operate on some more specific types.

Many of these ops are given a low priority (0) so that specialized ops
will take precedence. If your specialized op doesn't seem to be used,
check that the priorities are configured properly.
"""

from __future__ import annotations

from mypyc.ir.ops import ERR_MAGIC, ERR_NEVER
from mypyc.ir.rtypes import (
    bool_rprimitive,
    c_int_rprimitive,
    c_pyssize_t_rprimitive,
    c_size_t_rprimitive,
    int_rprimitive,
    object_pointer_rprimitive,
    object_rprimitive,
    pointer_rprimitive,
)
from mypyc.primitives.registry import (
    ERR_NEG_INT,
    binary_op,
    custom_op,
    function_op,
    method_op,
    unary_op,
)

# Binary operations

for op, opid in [
    ("==", 2),  # PY_EQ
    ("!=", 3),  # PY_NE
    ("<", 0),  # PY_LT
    ("<=", 1),  # PY_LE
    (">", 4),  # PY_GT
    (">=", 5),
]:  # PY_GE
    # The result type is 'object' since that's what PyObject_RichCompare returns.
    binary_op(
        name=op,
        arg_types=[object_rprimitive, object_rprimitive],
        return_type=object_rprimitive,
        c_function_name="PyObject_RichCompare",
        error_kind=ERR_MAGIC,
        extra_int_constants=[(opid, c_int_rprimitive)],
        priority=0,
    )

for op, funcname in [
    ("+", "PyNumber_Add"),
    ("-", "PyNumber_Subtract"),
    ("*", "PyNumber_Multiply"),
    ("//", "PyNumber_FloorDivide"),
    ("/", "PyNumber_TrueDivide"),
    ("%", "PyNumber_Remainder"),
    ("<<", "PyNumber_Lshift"),
    (">>", "PyNumber_Rshift"),
    ("&", "PyNumber_And"),
    ("^", "PyNumber_Xor"),
    ("|", "PyNumber_Or"),
    ("@", "PyNumber_MatrixMultiply"),
]:
    binary_op(
        name=op,
        arg_types=[object_rprimitive, object_rprimitive],
        return_type=object_rprimitive,
        c_function_name=funcname,
        error_kind=ERR_MAGIC,
        priority=0,
    )


function_op(
    name="builtins.divmod",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyNumber_Divmod",
    error_kind=ERR_MAGIC,
    priority=0,
)


for op, funcname in [
    ("+=", "PyNumber_InPlaceAdd"),
    ("-=", "PyNumber_InPlaceSubtract"),
    ("*=", "PyNumber_InPlaceMultiply"),
    ("@=", "PyNumber_InPlaceMatrixMultiply"),
    ("//=", "PyNumber_InPlaceFloorDivide"),
    ("/=", "PyNumber_InPlaceTrueDivide"),
    ("%=", "PyNumber_InPlaceRemainder"),
    ("<<=", "PyNumber_InPlaceLshift"),
    (">>=", "PyNumber_InPlaceRshift"),
    ("&=", "PyNumber_InPlaceAnd"),
    ("^=", "PyNumber_InPlaceXor"),
    ("|=", "PyNumber_InPlaceOr"),
]:
    binary_op(
        name=op,
        arg_types=[object_rprimitive, object_rprimitive],
        return_type=object_rprimitive,
        c_function_name=funcname,
        error_kind=ERR_MAGIC,
        priority=0,
    )

for op, c_function in (("**", "CPyNumber_Power"), ("**=", "CPyNumber_InPlacePower")):
    binary_op(
        name=op,
        arg_types=[object_rprimitive, object_rprimitive],
        return_type=object_rprimitive,
        error_kind=ERR_MAGIC,
        c_function_name=c_function,
        priority=0,
    )

for arg_count, c_function in ((2, "CPyNumber_Power"), (3, "PyNumber_Power")):
    function_op(
        name="builtins.pow",
        arg_types=[object_rprimitive] * arg_count,
        return_type=object_rprimitive,
        error_kind=ERR_MAGIC,
        c_function_name=c_function,
        priority=0,
    )

binary_op(
    name="in",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="PySequence_Contains",
    error_kind=ERR_NEG_INT,
    truncated_type=bool_rprimitive,
    ordering=[1, 0],
    priority=0,
)


# Unary operations

for op, funcname in [
    ("-", "PyNumber_Negative"),
    ("+", "PyNumber_Positive"),
    ("~", "PyNumber_Invert"),
]:
    unary_op(
        name=op,
        arg_type=object_rprimitive,
        return_type=object_rprimitive,
        c_function_name=funcname,
        error_kind=ERR_MAGIC,
        priority=0,
    )

unary_op(
    name="not",
    arg_type=object_rprimitive,
    return_type=c_int_rprimitive,
    c_function_name="PyObject_Not",
    error_kind=ERR_NEG_INT,
    truncated_type=bool_rprimitive,
    priority=0,
)

# abs(obj)
function_op(
    name="builtins.abs",
    arg_types=[object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyNumber_Absolute",
    error_kind=ERR_MAGIC,
    priority=0,
)

# obj1[obj2]
method_op(
    name="__getitem__",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyObject_GetItem",
    error_kind=ERR_MAGIC,
    priority=0,
)

# obj1[obj2] = obj3
method_op(
    name="__setitem__",
    arg_types=[object_rprimitive, object_rprimitive, object_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="PyObject_SetItem",
    error_kind=ERR_NEG_INT,
    priority=0,
)

# del obj1[obj2]
method_op(
    name="__delitem__",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="PyObject_DelItem",
    error_kind=ERR_NEG_INT,
    priority=0,
)

# hash(obj)
function_op(
    name="builtins.hash",
    arg_types=[object_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyObject_Hash",
    error_kind=ERR_MAGIC,
)

# getattr(obj, attr)
py_getattr_op = function_op(
    name="builtins.getattr",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyObject_GetAttr",
    error_kind=ERR_MAGIC,
)

# getattr(obj, attr, default)
function_op(
    name="builtins.getattr",
    arg_types=[object_rprimitive, object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyObject_GetAttr3",
    error_kind=ERR_MAGIC,
)

# setattr(obj, attr, value)
py_setattr_op = function_op(
    name="builtins.setattr",
    arg_types=[object_rprimitive, object_rprimitive, object_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="PyObject_SetAttr",
    error_kind=ERR_NEG_INT,
)

# hasattr(obj, attr)
py_hasattr_op = function_op(
    name="builtins.hasattr",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=bool_rprimitive,
    c_function_name="PyObject_HasAttr",
    error_kind=ERR_NEVER,
)

# del obj.attr
py_delattr_op = function_op(
    name="builtins.delattr",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="PyObject_DelAttr",
    error_kind=ERR_NEG_INT,
)

# Call callable object with N positional arguments: func(arg1, ..., argN)
# Arguments are (func, arg1, ..., argN).
py_call_op = custom_op(
    arg_types=[],
    return_type=object_rprimitive,
    c_function_name="PyObject_CallFunctionObjArgs",
    error_kind=ERR_MAGIC,
    var_arg_type=object_rprimitive,
    extra_int_constants=[(0, pointer_rprimitive)],
)

# Call callable object using positional and/or keyword arguments (Python 3.8+)
py_vectorcall_op = custom_op(
    arg_types=[
        object_rprimitive,  # Callable
        object_pointer_rprimitive,  # Args (PyObject **)
        c_size_t_rprimitive,  # Number of positional args
        object_rprimitive,
    ],  # Keyword arg names tuple (or NULL)
    return_type=object_rprimitive,
    c_function_name="_PyObject_Vectorcall",
    error_kind=ERR_MAGIC,
)

# Call method using positional and/or keyword arguments (Python 3.9+)
py_vectorcall_method_op = custom_op(
    arg_types=[
        object_rprimitive,  # Method name
        object_pointer_rprimitive,  # Args, including self (PyObject **)
        c_size_t_rprimitive,  # Number of positional args, including self
        object_rprimitive,
    ],  # Keyword arg names tuple (or NULL)
    return_type=object_rprimitive,
    c_function_name="PyObject_VectorcallMethod",
    error_kind=ERR_MAGIC,
)

# Call callable object with positional + keyword args: func(*args, **kwargs)
# Arguments are (func, *args tuple, **kwargs dict).
py_call_with_kwargs_op = custom_op(
    arg_types=[object_rprimitive, object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyObject_Call",
    error_kind=ERR_MAGIC,
)

# Call method with positional arguments: obj.method(arg1, ...)
# Arguments are (object, attribute name, arg1, ...).
py_method_call_op = custom_op(
    arg_types=[],
    return_type=object_rprimitive,
    c_function_name="CPyObject_CallMethodObjArgs",
    error_kind=ERR_MAGIC,
    var_arg_type=object_rprimitive,
    extra_int_constants=[(0, pointer_rprimitive)],
)

# len(obj)
generic_len_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyObject_Size",
    error_kind=ERR_MAGIC,
)

# len(obj)
# same as generic_len_op, however return py_ssize_t
generic_ssize_t_len_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=c_pyssize_t_rprimitive,
    c_function_name="PyObject_Size",
    error_kind=ERR_NEG_INT,
)

# iter(obj)
iter_op = function_op(
    name="builtins.iter",
    arg_types=[object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyObject_GetIter",
    error_kind=ERR_MAGIC,
)
# next(iterator)
#
# Although the error_kind is set to be ERR_NEVER, this can actually
# return NULL, and thus it must be checked using Branch.IS_ERROR.
next_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyIter_Next",
    error_kind=ERR_NEVER,
)
# next(iterator)
#
# Do a next, don't swallow StopIteration, but also don't propagate an
# error. (N.B: This can still return NULL without an error to
# represent an implicit StopIteration, but if StopIteration is
# *explicitly* raised this will not swallow it.)
# Can return NULL: see next_op.
next_raw_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyIter_Next",
    error_kind=ERR_NEVER,
)

# this would be aiter(obj) if it existed
aiter_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPy_GetAIter",
    error_kind=ERR_MAGIC,
)

# this would be anext(obj) if it existed
anext_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPy_GetANext",
    error_kind=ERR_MAGIC,
)
