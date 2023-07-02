"""Primitive bytes ops."""

from __future__ import annotations

from mypyc.ir.ops import ERR_MAGIC
from mypyc.ir.rtypes import (
    RUnion,
    bytes_rprimitive,
    c_int_rprimitive,
    c_pyssize_t_rprimitive,
    dict_rprimitive,
    int_rprimitive,
    list_rprimitive,
    object_rprimitive,
    str_rprimitive,
)
from mypyc.primitives.registry import (
    ERR_NEG_INT,
    binary_op,
    custom_op,
    function_op,
    load_address_op,
    method_op,
)

# Get the 'bytes' type object.
load_address_op(name="builtins.bytes", type=object_rprimitive, src="PyBytes_Type")

# bytes(obj)
function_op(
    name="builtins.bytes",
    arg_types=[RUnion([list_rprimitive, dict_rprimitive, str_rprimitive])],
    return_type=bytes_rprimitive,
    c_function_name="PyBytes_FromObject",
    error_kind=ERR_MAGIC,
)

# bytearray(obj)
function_op(
    name="builtins.bytearray",
    arg_types=[object_rprimitive],
    return_type=bytes_rprimitive,
    c_function_name="PyByteArray_FromObject",
    error_kind=ERR_MAGIC,
)

# bytes ==/!= (return -1/0/1)
bytes_compare = custom_op(
    arg_types=[bytes_rprimitive, bytes_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="CPyBytes_Compare",
    error_kind=ERR_NEG_INT,
)

# bytes + bytes
# bytearray + bytearray
binary_op(
    name="+",
    arg_types=[bytes_rprimitive, bytes_rprimitive],
    return_type=bytes_rprimitive,
    c_function_name="CPyBytes_Concat",
    error_kind=ERR_MAGIC,
    steals=[True, False],
)

# bytes[begin:end]
bytes_slice_op = custom_op(
    arg_types=[bytes_rprimitive, int_rprimitive, int_rprimitive],
    return_type=bytes_rprimitive,
    c_function_name="CPyBytes_GetSlice",
    error_kind=ERR_MAGIC,
)

# bytes[index]
# bytearray[index]
method_op(
    name="__getitem__",
    arg_types=[bytes_rprimitive, int_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyBytes_GetItem",
    error_kind=ERR_MAGIC,
)

# bytes.join(obj)
method_op(
    name="join",
    arg_types=[bytes_rprimitive, object_rprimitive],
    return_type=bytes_rprimitive,
    c_function_name="CPyBytes_Join",
    error_kind=ERR_MAGIC,
)

# Join bytes objects and return a new bytes.
# The first argument is the total number of the following bytes.
bytes_build_op = custom_op(
    arg_types=[c_pyssize_t_rprimitive],
    return_type=bytes_rprimitive,
    c_function_name="CPyBytes_Build",
    error_kind=ERR_MAGIC,
    var_arg_type=bytes_rprimitive,
)
