"""Primitive tuple ops for *variable-length* tuples.

Note: Varying-length tuples are represented as boxed Python tuple
objects, i.e. tuple_rprimitive (RPrimitive), not RTuple.
"""

from __future__ import annotations

from mypyc.ir.ops import ERR_FALSE, ERR_MAGIC
from mypyc.ir.rtypes import (
    bit_rprimitive,
    c_pyssize_t_rprimitive,
    int_rprimitive,
    list_rprimitive,
    object_rprimitive,
    tuple_rprimitive,
)
from mypyc.primitives.registry import custom_op, function_op, load_address_op, method_op

# Get the 'builtins.tuple' type object.
load_address_op(name="builtins.tuple", type=object_rprimitive, src="PyTuple_Type")

# tuple[index] (for an int index)
tuple_get_item_op = method_op(
    name="__getitem__",
    arg_types=[tuple_rprimitive, int_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPySequenceTuple_GetItem",
    error_kind=ERR_MAGIC,
)

# Construct a boxed tuple from items: (item1, item2, ...)
new_tuple_op = custom_op(
    arg_types=[c_pyssize_t_rprimitive],
    return_type=tuple_rprimitive,
    c_function_name="PyTuple_Pack",
    error_kind=ERR_MAGIC,
    var_arg_type=object_rprimitive,
)

new_tuple_with_length_op = custom_op(
    arg_types=[c_pyssize_t_rprimitive],
    return_type=tuple_rprimitive,
    c_function_name="PyTuple_New",
    error_kind=ERR_MAGIC,
)

# PyTuple_SET_ITEM does no error checking,
# and should only be used to fill in brand new tuples.
new_tuple_set_item_op = custom_op(
    arg_types=[tuple_rprimitive, int_rprimitive, object_rprimitive],
    return_type=bit_rprimitive,
    c_function_name="CPySequenceTuple_SetItemUnsafe",
    error_kind=ERR_FALSE,
    steals=[False, False, True],
)

# Construct tuple from a list.
list_tuple_op = function_op(
    name="builtins.tuple",
    arg_types=[list_rprimitive],
    return_type=tuple_rprimitive,
    c_function_name="PyList_AsTuple",
    error_kind=ERR_MAGIC,
    priority=2,
)

# Construct tuple from an arbitrary (iterable) object.
function_op(
    name="builtins.tuple",
    arg_types=[object_rprimitive],
    return_type=tuple_rprimitive,
    c_function_name="PySequence_Tuple",
    error_kind=ERR_MAGIC,
)

# tuple[begin:end]
tuple_slice_op = custom_op(
    arg_types=[tuple_rprimitive, int_rprimitive, int_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPySequenceTuple_GetSlice",
    error_kind=ERR_MAGIC,
)
