"""Primitive float ops."""

from __future__ import annotations

from mypyc.ir.ops import ERR_MAGIC, ERR_MAGIC_OVERLAPPING, ERR_NEVER
from mypyc.ir.rtypes import (
    bool_rprimitive,
    float_rprimitive,
    int_rprimitive,
    object_rprimitive,
    str_rprimitive,
)
from mypyc.primitives.registry import binary_op, function_op, load_address_op

# Get the 'builtins.float' type object.
load_address_op(name="builtins.float", type=object_rprimitive, src="PyFloat_Type")

binary_op(
    name="//",
    arg_types=[float_rprimitive, float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_FloorDivide",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# float(int)
int_to_float_op = function_op(
    name="builtins.float",
    arg_types=[int_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_FromTagged",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# float(str)
function_op(
    name="builtins.float",
    arg_types=[str_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyFloat_FromString",
    error_kind=ERR_MAGIC,
)

# abs(float)
function_op(
    name="builtins.abs",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="fabs",
    error_kind=ERR_NEVER,
)

# math.sin(float)
function_op(
    name="math.sin",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_Sin",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# math.cos(float)
function_op(
    name="math.cos",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_Cos",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# math.tan(float)
function_op(
    name="math.tan",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_Tan",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# math.sqrt(float)
function_op(
    name="math.sqrt",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_Sqrt",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# math.exp(float)
function_op(
    name="math.exp",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_Exp",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# math.log(float)
function_op(
    name="math.log",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_Log",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# math.floor(float)
function_op(
    name="math.floor",
    arg_types=[float_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyFloat_Floor",
    error_kind=ERR_MAGIC,
)

# math.ceil(float)
function_op(
    name="math.ceil",
    arg_types=[float_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyFloat_Ceil",
    error_kind=ERR_MAGIC,
)

# math.fabs(float)
function_op(
    name="math.fabs",
    arg_types=[float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="fabs",
    error_kind=ERR_NEVER,
)

# math.pow(float, float)
pow_op = function_op(
    name="math.pow",
    arg_types=[float_rprimitive, float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="CPyFloat_Pow",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# math.copysign(float, float)
copysign_op = function_op(
    name="math.copysign",
    arg_types=[float_rprimitive, float_rprimitive],
    return_type=float_rprimitive,
    c_function_name="copysign",
    error_kind=ERR_NEVER,
)

# math.isinf(float)
function_op(
    name="math.isinf",
    arg_types=[float_rprimitive],
    return_type=bool_rprimitive,
    c_function_name="CPyFloat_IsInf",
    error_kind=ERR_NEVER,
)

# math.isnan(float)
function_op(
    name="math.isnan",
    arg_types=[float_rprimitive],
    return_type=bool_rprimitive,
    c_function_name="CPyFloat_IsNaN",
    error_kind=ERR_NEVER,
)
