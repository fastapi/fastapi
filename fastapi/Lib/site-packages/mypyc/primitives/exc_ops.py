"""Exception-related primitive ops."""

from __future__ import annotations

from mypyc.ir.ops import ERR_ALWAYS, ERR_FALSE, ERR_NEVER
from mypyc.ir.rtypes import bit_rprimitive, exc_rtuple, object_rprimitive, void_rtype
from mypyc.primitives.registry import custom_op

# If the argument is a class, raise an instance of the class. Otherwise, assume
# that the argument is an exception object, and raise it.
raise_exception_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=void_rtype,
    c_function_name="CPy_Raise",
    error_kind=ERR_ALWAYS,
)

# Raise StopIteration exception with the specified value (which can be NULL).
set_stop_iteration_value = custom_op(
    arg_types=[object_rprimitive],
    return_type=void_rtype,
    c_function_name="CPyGen_SetStopIterationValue",
    error_kind=ERR_ALWAYS,
)

# Raise exception with traceback.
# Arguments are (exception type, exception value, traceback).
raise_exception_with_tb_op = custom_op(
    arg_types=[object_rprimitive, object_rprimitive, object_rprimitive],
    return_type=void_rtype,
    c_function_name="CPyErr_SetObjectAndTraceback",
    error_kind=ERR_ALWAYS,
)

# Reraise the currently raised exception.
reraise_exception_op = custom_op(
    arg_types=[],
    return_type=void_rtype,
    c_function_name="CPy_Reraise",
    error_kind=ERR_ALWAYS,
)

# Propagate exception if the CPython error indicator is set (an exception was raised).
no_err_occurred_op = custom_op(
    arg_types=[],
    return_type=bit_rprimitive,
    c_function_name="CPy_NoErrOccured",
    error_kind=ERR_FALSE,
)

err_occurred_op = custom_op(
    arg_types=[],
    return_type=object_rprimitive,
    c_function_name="PyErr_Occurred",
    error_kind=ERR_NEVER,
    is_borrowed=True,
)

# Keep propagating a raised exception by unconditionally giving an error value.
# This doesn't actually raise an exception.
keep_propagating_op = custom_op(
    arg_types=[],
    return_type=bit_rprimitive,
    c_function_name="CPy_KeepPropagating",
    error_kind=ERR_FALSE,
)

# Catches a propagating exception and makes it the "currently
# handled exception" (by sticking it into sys.exc_info()). Returns the
# exception that was previously being handled, which must be restored
# later.
error_catch_op = custom_op(
    arg_types=[],
    return_type=exc_rtuple,
    c_function_name="CPy_CatchError",
    error_kind=ERR_NEVER,
)

# Restore an old "currently handled exception" returned from.
# error_catch (by sticking it into sys.exc_info())
restore_exc_info_op = custom_op(
    arg_types=[exc_rtuple],
    return_type=void_rtype,
    c_function_name="CPy_RestoreExcInfo",
    error_kind=ERR_NEVER,
)

# Checks whether the exception currently being handled matches a particular type.
exc_matches_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=bit_rprimitive,
    c_function_name="CPy_ExceptionMatches",
    error_kind=ERR_NEVER,
)

# Get the value of the exception currently being handled.
get_exc_value_op = custom_op(
    arg_types=[],
    return_type=object_rprimitive,
    c_function_name="CPy_GetExcValue",
    error_kind=ERR_NEVER,
)

# Get exception info (exception type, exception instance, traceback object).
get_exc_info_op = custom_op(
    arg_types=[],
    return_type=exc_rtuple,
    c_function_name="CPy_GetExcInfo",
    error_kind=ERR_NEVER,
)
