// Exception related primitive operations
//
// These are registered in mypyc.primitives.exc_ops.

#include <Python.h>
#include "CPy.h"

void CPy_Raise(PyObject *exc) {
    if (PyObject_IsInstance(exc, (PyObject *)&PyType_Type)) {
        PyObject *obj = PyObject_CallNoArgs(exc);
        if (!obj)
            return;
        PyErr_SetObject(exc, obj);
        Py_DECREF(obj);
    } else {
        PyErr_SetObject((PyObject *)Py_TYPE(exc), exc);
    }
}

void CPy_Reraise(void) {
    PyObject *p_type, *p_value, *p_traceback;
    PyErr_GetExcInfo(&p_type, &p_value, &p_traceback);
    PyErr_Restore(p_type, p_value, p_traceback);
}

void CPyErr_SetObjectAndTraceback(PyObject *type, PyObject *value, PyObject *traceback) {
    // Set the value and traceback of an error. Because calling
    // PyErr_Restore takes away a reference to each object passed in
    // as an argument, we manually increase the reference count of
    // each argument before calling it.
    Py_INCREF(type);
    Py_INCREF(value);
    Py_INCREF(traceback);
    PyErr_Restore(type, value, traceback);
}

tuple_T3OOO CPy_CatchError(void) {
    // We need to return the existing sys.exc_info() information, so
    // that it can be restored when we finish handling the error we
    // are catching now. Grab that triple and convert NULL values to
    // the ExcDummy object in order to simplify refcount handling in
    // generated code.
    tuple_T3OOO ret;
    PyErr_GetExcInfo(&ret.f0, &ret.f1, &ret.f2);
    _CPy_ToDummy(&ret.f0);
    _CPy_ToDummy(&ret.f1);
    _CPy_ToDummy(&ret.f2);

    if (!PyErr_Occurred()) {
        PyErr_SetString(PyExc_RuntimeError, "CPy_CatchError called with no error!");
    }

    // Retrieve the error info and normalize it so that it looks like
    // what python code needs it to be.
    PyObject *type, *value, *traceback;
    PyErr_Fetch(&type, &value, &traceback);
    // Could we avoid always normalizing?
    PyErr_NormalizeException(&type, &value, &traceback);
    if (traceback != NULL) {
        PyException_SetTraceback(value, traceback);
    }
    // Indicate that we are now handling this exception by stashing it
    // in sys.exc_info().  mypyc routines that need access to the
    // exception will read it out of there.
    PyErr_SetExcInfo(type, value, traceback);
    // Clear the error indicator, since the exception isn't
    // propagating anymore.
    PyErr_Clear();

    return ret;
}

void CPy_RestoreExcInfo(tuple_T3OOO info) {
    PyErr_SetExcInfo(_CPy_FromDummy(info.f0), _CPy_FromDummy(info.f1), _CPy_FromDummy(info.f2));
}

bool CPy_ExceptionMatches(PyObject *type) {
    return PyErr_GivenExceptionMatches((PyObject *)Py_TYPE(CPy_ExcState()->exc_value), type);
}

PyObject *CPy_GetExcValue(void) {
    PyObject *exc = CPy_ExcState()->exc_value;
    Py_INCREF(exc);
    return exc;
}

static inline void _CPy_ToNone(PyObject **p) {
    if (*p == NULL) {
        Py_INCREF(Py_None);
        *p = Py_None;
    }
}

void _CPy_GetExcInfo(PyObject **p_type, PyObject **p_value, PyObject **p_traceback) {
    PyErr_GetExcInfo(p_type, p_value, p_traceback);
    _CPy_ToNone(p_type);
    _CPy_ToNone(p_value);
    _CPy_ToNone(p_traceback);
}

tuple_T3OOO CPy_GetExcInfo(void) {
    tuple_T3OOO ret;
    _CPy_GetExcInfo(&ret.f0, &ret.f1, &ret.f2);
    return ret;
}

void CPyError_OutOfMemory(void) {
    fprintf(stderr, "fatal: out of memory\n");
    fflush(stderr);
    abort();
}

// Construct a nicely formatted type name based on __module__ and __name__.
static PyObject *CPy_GetTypeName(PyObject *type) {
    PyObject *module = NULL, *name = NULL;
    PyObject *full = NULL;

    module = PyObject_GetAttrString(type, "__module__");
    if (!module || !PyUnicode_Check(module)) {
        goto out;
    }
    name = PyObject_GetAttrString(type, "__qualname__");
    if (!name || !PyUnicode_Check(name)) {
        goto out;
    }

    if (PyUnicode_CompareWithASCIIString(module, "builtins") == 0) {
        Py_INCREF(name);
        full = name;
    } else {
        full = PyUnicode_FromFormat("%U.%U", module, name);
    }

out:
    Py_XDECREF(module);
    Py_XDECREF(name);
    return full;
}

// Get the type of a value as a string, expanding tuples to include
// all the element types.
static PyObject *CPy_FormatTypeName(PyObject *value) {
    if (Py_IsNone(value)) {
        return PyUnicode_FromString("None");
    }

    if (!PyTuple_CheckExact(value)) {
        return CPy_GetTypeName((PyObject *)Py_TYPE(value));
    }

    if (PyTuple_GET_SIZE(value) > 10) {
        return PyUnicode_FromFormat("tuple[<%d items>]", PyTuple_GET_SIZE(value));
    }

    // Most of the logic is all for tuples, which is the only interesting case
    PyObject *output = PyUnicode_FromString("tuple[");
    if (!output) {
        return NULL;
    }
    /* This is quadratic but if that ever matters something is really weird. */
    int i;
    for (i = 0; i < PyTuple_GET_SIZE(value); i++) {
        PyObject *s = CPy_FormatTypeName(PyTuple_GET_ITEM(value, i));
        if (!s) {
            Py_DECREF(output);
            return NULL;
        }
        PyObject *next = PyUnicode_FromFormat("%U%U%s", output, s,
                                              i + 1 == PyTuple_GET_SIZE(value) ? "]" : ", ");
        Py_DECREF(output);
        Py_DECREF(s);
        if (!next) {
            return NULL;
        }
        output = next;
    }
    return output;
}

CPy_NOINLINE
void CPy_TypeError(const char *expected, PyObject *value) {
    PyObject *out = CPy_FormatTypeName(value);
    if (out) {
        PyErr_Format(PyExc_TypeError, "%s object expected; got %U", expected, out);
        Py_DECREF(out);
    } else {
        PyErr_Format(PyExc_TypeError, "%s object expected; and errored formatting real type!",
                     expected);
    }
}

// The PyFrameObject type definition (struct _frame) has been moved
// to the internal C API: to the pycore_frame.h header file.
// https://github.com/python/cpython/pull/31530
#if PY_VERSION_HEX >= 0x030b00a6
#include "internal/pycore_frame.h"
#endif

// This function is basically exactly the same with _PyTraceback_Add
// which is available in all the versions we support.
// We're continuing to use this because we'll probably optimize this later.
void CPy_AddTraceback(const char *filename, const char *funcname, int line, PyObject *globals) {
    PyObject *exc, *val, *tb;
    PyThreadState *thread_state = PyThreadState_GET();
    PyFrameObject *frame_obj;

    // We need to save off the exception state because in 3.8,
    // PyFrame_New fails if there is an error set and it fails to look
    // up builtins in the globals. (_PyTraceback_Add documents that it
    // needs to do it because it decodes the filename according to the
    // FS encoding, which could have a decoder in Python. We don't do
    // that so *that* doesn't apply to us.)
    PyErr_Fetch(&exc, &val, &tb);
    PyCodeObject *code_obj = PyCode_NewEmpty(filename, funcname, line);
    if (code_obj == NULL) {
        goto error;
    }

    frame_obj = PyFrame_New(thread_state, code_obj, globals, 0);
    if (frame_obj == NULL) {
        Py_DECREF(code_obj);
        goto error;
    }
    frame_obj->f_lineno = line;
    PyErr_Restore(exc, val, tb);
    PyTraceBack_Here(frame_obj);
    Py_DECREF(code_obj);
    Py_DECREF(frame_obj);

    return;

error:
    _PyErr_ChainExceptions(exc, val, tb);
}

CPy_NOINLINE
void CPy_TypeErrorTraceback(const char *filename, const char *funcname, int line,
                            PyObject *globals, const char *expected, PyObject *value) {
    CPy_TypeError(expected, value);
    CPy_AddTraceback(filename, funcname, line, globals);
}

void CPy_AttributeError(const char *filename, const char *funcname, const char *classname,
                        const char *attrname, int line, PyObject *globals) {
    char buf[500];
    snprintf(buf, sizeof(buf), "attribute '%.200s' of '%.200s' undefined", attrname, classname);
    PyErr_SetString(PyExc_AttributeError, buf);
    CPy_AddTraceback(filename, funcname, line, globals);
}
