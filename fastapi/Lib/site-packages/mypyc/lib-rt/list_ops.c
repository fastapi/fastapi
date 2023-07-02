// List primitive operations
//
// These are registered in mypyc.primitives.list_ops.

#include <Python.h>
#include "CPy.h"

#ifndef Py_TPFLAGS_SEQUENCE
#define Py_TPFLAGS_SEQUENCE (1 << 5)
#endif

PyObject *CPyList_Build(Py_ssize_t len, ...) {
    Py_ssize_t i;

    PyObject *res = PyList_New(len);
    if (res == NULL) {
        return NULL;
    }

    va_list args;
    va_start(args, len);
    for (i = 0; i < len; i++) {
        // Steals the reference
        PyObject *value = va_arg(args, PyObject *);
        PyList_SET_ITEM(res, i, value);
    }
    va_end(args);

    return res;
}

PyObject *CPyList_GetItemUnsafe(PyObject *list, CPyTagged index) {
    Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
    PyObject *result = PyList_GET_ITEM(list, n);
    Py_INCREF(result);
    return result;
}

PyObject *CPyList_GetItemShort(PyObject *list, CPyTagged index) {
    Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
    Py_ssize_t size = PyList_GET_SIZE(list);
    if (n >= 0) {
        if (n >= size) {
            PyErr_SetString(PyExc_IndexError, "list index out of range");
            return NULL;
        }
    } else {
        n += size;
        if (n < 0) {
            PyErr_SetString(PyExc_IndexError, "list index out of range");
            return NULL;
        }
    }
    PyObject *result = PyList_GET_ITEM(list, n);
    Py_INCREF(result);
    return result;
}

PyObject *CPyList_GetItemShortBorrow(PyObject *list, CPyTagged index) {
    Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
    Py_ssize_t size = PyList_GET_SIZE(list);
    if (n >= 0) {
        if (n >= size) {
            PyErr_SetString(PyExc_IndexError, "list index out of range");
            return NULL;
        }
    } else {
        n += size;
        if (n < 0) {
            PyErr_SetString(PyExc_IndexError, "list index out of range");
            return NULL;
        }
    }
    return PyList_GET_ITEM(list, n);
}

PyObject *CPyList_GetItem(PyObject *list, CPyTagged index) {
    if (CPyTagged_CheckShort(index)) {
        Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
        Py_ssize_t size = PyList_GET_SIZE(list);
        if (n >= 0) {
            if (n >= size) {
                PyErr_SetString(PyExc_IndexError, "list index out of range");
                return NULL;
            }
        } else {
            n += size;
            if (n < 0) {
                PyErr_SetString(PyExc_IndexError, "list index out of range");
                return NULL;
            }
        }
        PyObject *result = PyList_GET_ITEM(list, n);
        Py_INCREF(result);
        return result;
    } else {
        PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
        return NULL;
    }
}

PyObject *CPyList_GetItemBorrow(PyObject *list, CPyTagged index) {
    if (CPyTagged_CheckShort(index)) {
        Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
        Py_ssize_t size = PyList_GET_SIZE(list);
        if (n >= 0) {
            if (n >= size) {
                PyErr_SetString(PyExc_IndexError, "list index out of range");
                return NULL;
            }
        } else {
            n += size;
            if (n < 0) {
                PyErr_SetString(PyExc_IndexError, "list index out of range");
                return NULL;
            }
        }
        return PyList_GET_ITEM(list, n);
    } else {
        PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
        return NULL;
    }
}

PyObject *CPyList_GetItemInt64(PyObject *list, int64_t index) {
    size_t size = PyList_GET_SIZE(list);
    if (likely((uint64_t)index < size)) {
        PyObject *result = PyList_GET_ITEM(list, index);
        Py_INCREF(result);
        return result;
    }
    if (index >= 0) {
        PyErr_SetString(PyExc_IndexError, "list index out of range");
        return NULL;
    }
    index += size;
    if (index < 0) {
        PyErr_SetString(PyExc_IndexError, "list index out of range");
        return NULL;
    }
    PyObject *result = PyList_GET_ITEM(list, index);
    Py_INCREF(result);
    return result;
}

PyObject *CPyList_GetItemInt64Borrow(PyObject *list, int64_t index) {
    size_t size = PyList_GET_SIZE(list);
    if (likely((uint64_t)index < size)) {
        return PyList_GET_ITEM(list, index);
    }
    if (index >= 0) {
        PyErr_SetString(PyExc_IndexError, "list index out of range");
        return NULL;
    }
    index += size;
    if (index < 0) {
        PyErr_SetString(PyExc_IndexError, "list index out of range");
        return NULL;
    }
    return PyList_GET_ITEM(list, index);
}

bool CPyList_SetItem(PyObject *list, CPyTagged index, PyObject *value) {
    if (CPyTagged_CheckShort(index)) {
        Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
        Py_ssize_t size = PyList_GET_SIZE(list);
        if (n >= 0) {
            if (n >= size) {
                PyErr_SetString(PyExc_IndexError, "list assignment index out of range");
                return false;
            }
        } else {
            n += size;
            if (n < 0) {
                PyErr_SetString(PyExc_IndexError, "list assignment index out of range");
                return false;
            }
        }
        // PyList_SET_ITEM doesn't decref the old element, so we do
        Py_DECREF(PyList_GET_ITEM(list, n));
        // N.B: Steals reference
        PyList_SET_ITEM(list, n, value);
        return true;
    } else {
        PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
        return false;
    }
}

bool CPyList_SetItemInt64(PyObject *list, int64_t index, PyObject *value) {
    size_t size = PyList_GET_SIZE(list);
    if (unlikely((uint64_t)index >= size)) {
        if (index > 0) {
            PyErr_SetString(PyExc_IndexError, "list assignment index out of range");
            return false;
        }
        index += size;
        if (index < 0) {
            PyErr_SetString(PyExc_IndexError, "list assignment index out of range");
            return false;
        }
    }
    // PyList_SET_ITEM doesn't decref the old element, so we do
    Py_DECREF(PyList_GET_ITEM(list, index));
    // N.B: Steals reference
    PyList_SET_ITEM(list, index, value);
    return true;
}

// This function should only be used to fill in brand new lists.
bool CPyList_SetItemUnsafe(PyObject *list, CPyTagged index, PyObject *value) {
    if (CPyTagged_CheckShort(index)) {
        Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
        PyList_SET_ITEM(list, n, value);
        return true;
    } else {
        PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
        return false;
    }
}

PyObject *CPyList_PopLast(PyObject *obj)
{
    // I tried a specalized version of pop_impl for just removing the
    // last element and it wasn't any faster in microbenchmarks than
    // the generic one so I ditched it.
    return list_pop_impl((PyListObject *)obj, -1);
}

PyObject *CPyList_Pop(PyObject *obj, CPyTagged index)
{
    if (CPyTagged_CheckShort(index)) {
        Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
        return list_pop_impl((PyListObject *)obj, n);
    } else {
        PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
        return NULL;
    }
}

CPyTagged CPyList_Count(PyObject *obj, PyObject *value)
{
    return list_count((PyListObject *)obj, value);
}

int CPyList_Insert(PyObject *list, CPyTagged index, PyObject *value)
{
    if (CPyTagged_CheckShort(index)) {
        Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
        return PyList_Insert(list, n, value);
    }
    // The max range doesn't exactly coincide with ssize_t, but we still
    // want to keep the error message compatible with CPython.
    PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
    return -1;
}

PyObject *CPyList_Extend(PyObject *o1, PyObject *o2) {
    return _PyList_Extend((PyListObject *)o1, o2);
}

// Return -2 or error, -1 if not found, or index of first match otherwise.
static Py_ssize_t _CPyList_Find(PyObject *list, PyObject *obj) {
    Py_ssize_t i;
    for (i = 0; i < Py_SIZE(list); i++) {
        PyObject *item = PyList_GET_ITEM(list, i);
        Py_INCREF(item);
        int cmp = PyObject_RichCompareBool(item, obj, Py_EQ);
        Py_DECREF(item);
        if (cmp != 0) {
            if (cmp > 0) {
                return i;
            } else {
                return -2;
            }
        }
    }
    return -1;
}

int CPyList_Remove(PyObject *list, PyObject *obj) {
    Py_ssize_t index = _CPyList_Find(list, obj);
    if (index == -2) {
        return -1;
    }
    if (index == -1) {
        PyErr_SetString(PyExc_ValueError, "list.remove(x): x not in list");
        return -1;
    }
    return PyList_SetSlice(list, index, index + 1, NULL);
}

CPyTagged CPyList_Index(PyObject *list, PyObject *obj) {
    Py_ssize_t index = _CPyList_Find(list, obj);
    if (index == -2) {
        return CPY_INT_TAG;
    }
    if (index == -1) {
        PyErr_SetString(PyExc_ValueError, "value is not in list");
        return CPY_INT_TAG;
    }
    return index << 1;
}

PyObject *CPySequence_Multiply(PyObject *seq, CPyTagged t_size) {
    Py_ssize_t size = CPyTagged_AsSsize_t(t_size);
    if (size == -1 && PyErr_Occurred()) {
        return NULL;
    }
    return PySequence_Repeat(seq, size);
}

PyObject *CPySequence_RMultiply(CPyTagged t_size, PyObject *seq) {
    return CPySequence_Multiply(seq, t_size);
}

PyObject *CPyList_GetSlice(PyObject *obj, CPyTagged start, CPyTagged end) {
    if (likely(PyList_CheckExact(obj)
               && CPyTagged_CheckShort(start) && CPyTagged_CheckShort(end))) {
        Py_ssize_t startn = CPyTagged_ShortAsSsize_t(start);
        Py_ssize_t endn = CPyTagged_ShortAsSsize_t(end);
        if (startn < 0) {
            startn += PyList_GET_SIZE(obj);
        }
        if (endn < 0) {
            endn += PyList_GET_SIZE(obj);
        }
        return PyList_GetSlice(obj, startn, endn);
    }
    return CPyObject_GetSlice(obj, start, end);
}

int CPySequence_Check(PyObject *obj) {
    return Py_TYPE(obj)->tp_flags & Py_TPFLAGS_SEQUENCE;
}
