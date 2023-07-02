"""Miscellaneous primitive ops."""

from __future__ import annotations

from mypyc.ir.ops import ERR_FALSE, ERR_MAGIC, ERR_NEVER
from mypyc.ir.rtypes import (
    bit_rprimitive,
    bool_rprimitive,
    c_int_rprimitive,
    c_pointer_rprimitive,
    c_pyssize_t_rprimitive,
    dict_rprimitive,
    int_rprimitive,
    object_pointer_rprimitive,
    object_rprimitive,
    str_rprimitive,
)
from mypyc.primitives.registry import (
    ERR_NEG_INT,
    custom_op,
    function_op,
    load_address_op,
)

# Get the 'bool' type object.
load_address_op(name="builtins.bool", type=object_rprimitive, src="PyBool_Type")

# Get the 'range' type object.
load_address_op(name="builtins.range", type=object_rprimitive, src="PyRange_Type")

# Get the boxed Python 'None' object
none_object_op = load_address_op(
    name="Py_None", type=object_rprimitive, src="_Py_NoneStruct"
)

# Get the boxed object '...'
ellipsis_op = load_address_op(
    name="...", type=object_rprimitive, src="_Py_EllipsisObject"
)

# Get the boxed NotImplemented object
not_implemented_op = load_address_op(
    name="builtins.NotImplemented",
    type=object_rprimitive,
    src="_Py_NotImplementedStruct",
)

# Get the boxed StopAsyncIteration object
stop_async_iteration_op = load_address_op(
    name="builtins.StopAsyncIteration",
    type=object_rprimitive,
    src="PyExc_StopAsyncIteration",
)

# id(obj)
function_op(
    name="builtins.id",
    arg_types=[object_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyTagged_Id",
    error_kind=ERR_NEVER,
)

# Return the result of obj.__await()__ or obj.__iter__() (if no __await__ exists)
coro_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPy_GetCoro",
    error_kind=ERR_MAGIC,
)

# Do obj.send(value), or a next(obj) if second arg is None.
# (This behavior is to match the PEP 380 spec for yield from.)
# Like next_raw_op, don't swallow StopIteration,
# but also don't propagate an error.
# Can return NULL: see next_op.
send_op = custom_op(
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyIter_Send",
    error_kind=ERR_NEVER,
)

# This is sort of unfortunate but oh well: yield_from_except performs most of the
# error handling logic in `yield from` operations. It returns a bool and passes
# a value by address.
# If the bool is true, then a StopIteration was received and we should return.
# If the bool is false, then the value should be yielded.
# The normal case is probably that it signals an exception, which gets
# propagated.
# Op used for "yield from" error handling.
# See comment in CPy_YieldFromErrorHandle for more information.
yield_from_except_op = custom_op(
    arg_types=[object_rprimitive, object_pointer_rprimitive],
    return_type=bool_rprimitive,
    c_function_name="CPy_YieldFromErrorHandle",
    error_kind=ERR_MAGIC,
)

# Create method object from a callable object and self.
method_new_op = custom_op(
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyMethod_New",
    error_kind=ERR_MAGIC,
)

# Check if the current exception is a StopIteration and return its value if so.
# Treats "no exception" as StopIteration with a None value.
# If it is a different exception, re-reraise it.
check_stop_op = custom_op(
    arg_types=[],
    return_type=object_rprimitive,
    c_function_name="CPy_FetchStopIterationValue",
    error_kind=ERR_MAGIC,
)

# Determine the most derived metaclass and check for metaclass conflicts.
# Arguments are (metaclass, bases).
py_calc_meta_op = custom_op(
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPy_CalculateMetaclass",
    error_kind=ERR_MAGIC,
    is_borrowed=True,
)

# Import a module (plain)
import_op = custom_op(
    arg_types=[str_rprimitive],
    return_type=object_rprimitive,
    c_function_name="PyImport_Import",
    error_kind=ERR_MAGIC,
)

# Table-driven import op.
import_many_op = custom_op(
    arg_types=[
        object_rprimitive,
        c_pointer_rprimitive,
        object_rprimitive,
        object_rprimitive,
        object_rprimitive,
        c_pointer_rprimitive,
    ],
    return_type=bit_rprimitive,
    c_function_name="CPyImport_ImportMany",
    error_kind=ERR_FALSE,
)

# From import helper op
import_from_many_op = custom_op(
    arg_types=[
        object_rprimitive,
        object_rprimitive,
        object_rprimitive,
        object_rprimitive,
    ],
    return_type=object_rprimitive,
    c_function_name="CPyImport_ImportFromMany",
    error_kind=ERR_MAGIC,
)

# Get the sys.modules dictionary
get_module_dict_op = custom_op(
    arg_types=[],
    return_type=dict_rprimitive,
    c_function_name="PyImport_GetModuleDict",
    error_kind=ERR_NEVER,
    is_borrowed=True,
)

# isinstance(obj, cls)
slow_isinstance_op = function_op(
    name="builtins.isinstance",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="PyObject_IsInstance",
    error_kind=ERR_NEG_INT,
    truncated_type=bool_rprimitive,
)

# Faster isinstance(obj, cls) that only works with native classes and doesn't perform
# type checking of the type argument.
fast_isinstance_op = function_op(
    "builtins.isinstance",
    arg_types=[object_rprimitive, object_rprimitive],
    return_type=bool_rprimitive,
    c_function_name="CPy_TypeCheck",
    error_kind=ERR_NEVER,
    priority=0,
)

# bool(obj) with unboxed result
bool_op = function_op(
    name="builtins.bool",
    arg_types=[object_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="PyObject_IsTrue",
    error_kind=ERR_NEG_INT,
    truncated_type=bool_rprimitive,
)

# slice(start, stop, step)
new_slice_op = function_op(
    name="builtins.slice",
    arg_types=[object_rprimitive, object_rprimitive, object_rprimitive],
    c_function_name="PySlice_New",
    return_type=object_rprimitive,
    error_kind=ERR_MAGIC,
)

# type(obj)
type_op = function_op(
    name="builtins.type",
    arg_types=[object_rprimitive],
    c_function_name="PyObject_Type",
    return_type=object_rprimitive,
    error_kind=ERR_NEVER,
)

# Get 'builtins.type' (base class of all classes)
type_object_op = load_address_op(
    name="builtins.type", type=object_rprimitive, src="PyType_Type"
)

# Create a heap type based on a template non-heap type.
# See CPyType_FromTemplate for more docs.
pytype_from_template_op = custom_op(
    arg_types=[object_rprimitive, object_rprimitive, str_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyType_FromTemplate",
    error_kind=ERR_MAGIC,
)

# Create a dataclass from an extension class. See
# CPyDataclass_SleightOfHand for more docs.
dataclass_sleight_of_hand = custom_op(
    arg_types=[object_rprimitive, object_rprimitive, dict_rprimitive, dict_rprimitive],
    return_type=bit_rprimitive,
    c_function_name="CPyDataclass_SleightOfHand",
    error_kind=ERR_FALSE,
)

# Raise ValueError if length of first argument is not equal to the second argument.
# The first argument must be a list or a variable-length tuple.
check_unpack_count_op = custom_op(
    arg_types=[object_rprimitive, c_pyssize_t_rprimitive],
    return_type=c_int_rprimitive,
    c_function_name="CPySequence_CheckUnpackCount",
    error_kind=ERR_NEG_INT,
)


# register an implementation for a singledispatch function
register_function = custom_op(
    arg_types=[object_rprimitive, object_rprimitive, object_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPySingledispatch_RegisterFunction",
    error_kind=ERR_MAGIC,
)
