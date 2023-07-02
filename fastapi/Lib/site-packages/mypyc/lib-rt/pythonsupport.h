// Collects code that was copied in from cpython, for a couple of different reasons:
//  * We wanted to modify it to produce a more efficient version for our uses
//  * We needed to call it and it was static :(
//  * We wanted to call it and needed to backport it

#ifndef CPY_PYTHONSUPPORT_H
#define CPY_PYTHONSUPPORT_H

#include <stdbool.h>
#include <Python.h>
#include "pythoncapi_compat.h"
#include <frameobject.h>
#include <assert.h>
#include "mypyc_util.h"

#ifdef __cplusplus
extern "C" {
#endif
#if 0
} // why isn't emacs smart enough to not indent this
#endif

/////////////////////////////////////////
// Adapted from bltinmodule.c in Python 3.7.0
_Py_IDENTIFIER(__mro_entries__);
static PyObject*
update_bases(PyObject *bases)
{
    Py_ssize_t i, j;
    PyObject *base, *meth, *new_base, *result, *new_bases = NULL;
    PyObject *stack[1] = {bases};
    assert(PyTuple_Check(bases));

    Py_ssize_t nargs = PyTuple_GET_SIZE(bases);
    for (i = 0; i < nargs; i++) {
        base = PyTuple_GET_ITEM(bases, i);
        if (PyType_Check(base)) {
            if (new_bases) {
                /* If we already have made a replacement, then we append every normal base,
                   otherwise just skip it. */
                if (PyList_Append(new_bases, base) < 0) {
                    goto error;
                }
            }
            continue;
        }
        if (_PyObject_LookupAttrId(base, &PyId___mro_entries__, &meth) < 0) {
            goto error;
        }
        if (!meth) {
            if (new_bases) {
                if (PyList_Append(new_bases, base) < 0) {
                    goto error;
                }
            }
            continue;
        }
        new_base = _PyObject_FastCall(meth, stack, 1);
        Py_DECREF(meth);
        if (!new_base) {
            goto error;
        }
        if (!PyTuple_Check(new_base)) {
            PyErr_SetString(PyExc_TypeError,
                            "__mro_entries__ must return a tuple");
            Py_DECREF(new_base);
            goto error;
        }
        if (!new_bases) {
            /* If this is a first successful replacement, create new_bases list and
               copy previously encountered bases. */
            if (!(new_bases = PyList_New(i))) {
                goto error;
            }
            for (j = 0; j < i; j++) {
                base = PyTuple_GET_ITEM(bases, j);
                PyList_SET_ITEM(new_bases, j, base);
                Py_INCREF(base);
            }
        }
        j = PyList_GET_SIZE(new_bases);
        if (PyList_SetSlice(new_bases, j, j, new_base) < 0) {
            goto error;
        }
        Py_DECREF(new_base);
    }
    if (!new_bases) {
        return bases;
    }
    result = PyList_AsTuple(new_bases);
    Py_DECREF(new_bases);
    return result;

error:
    Py_XDECREF(new_bases);
    return NULL;
}

// From Python 3.7's typeobject.c
_Py_IDENTIFIER(__init_subclass__);
static int
init_subclass(PyTypeObject *type, PyObject *kwds)
{
    PyObject *super, *func, *result;
    PyObject *args[2] = {(PyObject *)type, (PyObject *)type};

    super = _PyObject_FastCall((PyObject *)&PySuper_Type, args, 2);
    if (super == NULL) {
        return -1;
    }

    func = _PyObject_GetAttrId(super, &PyId___init_subclass__);
    Py_DECREF(super);
    if (func == NULL) {
        return -1;
    }

    result = _PyObject_FastCallDict(func, NULL, 0, kwds);
    Py_DECREF(func);
    if (result == NULL) {
        return -1;
    }

    Py_DECREF(result);
    return 0;
}

// Adapted from longobject.c in Python 3.7.0

/* This function adapted from PyLong_AsLongLongAndOverflow, but with
 * some safety checks removed and specialized to only work for objects
 * that are already longs.
 * About half of the win this provides, though, just comes from being
 * able to inline the function, which in addition to saving function call
 * overhead allows the out-parameter overflow flag to be collapsed into
 * control flow.
 * Additionally, we check against the possible range of CPyTagged, not of
 * Py_ssize_t. */
static inline Py_ssize_t
CPyLong_AsSsize_tAndOverflow(PyObject *vv, int *overflow)
{
    /* This version by Tim Peters */
    PyLongObject *v = (PyLongObject *)vv;
    size_t x, prev;
    Py_ssize_t res;
    Py_ssize_t i;
    int sign;

    *overflow = 0;

    res = -1;
    i = Py_SIZE(v);

    if (likely(i == 1)) {
        res = v->ob_digit[0];
    } else if (likely(i == 0)) {
        res = 0;
    } else if (i == -1) {
        res = -(sdigit)v->ob_digit[0];
    } else {
        sign = 1;
        x = 0;
        if (i < 0) {
            sign = -1;
            i = -(i);
        }
        while (--i >= 0) {
            prev = x;
            x = (x << PyLong_SHIFT) + v->ob_digit[i];
            if ((x >> PyLong_SHIFT) != prev) {
                *overflow = sign;
                goto exit;
            }
        }
        /* Haven't lost any bits, but casting to long requires extra
         * care (see comment above).
         */
        if (x <= (size_t)CPY_TAGGED_MAX) {
            res = (Py_ssize_t)x * sign;
        }
        else if (sign < 0 && x == CPY_TAGGED_ABS_MIN) {
            res = CPY_TAGGED_MIN;
        }
        else {
            *overflow = sign;
            /* res is already set to -1 */
        }
    }
  exit:
    return res;
}

// Adapted from listobject.c in Python 3.7.0
static int
list_resize(PyListObject *self, Py_ssize_t newsize)
{
    PyObject **items;
    size_t new_allocated, num_allocated_bytes;
    Py_ssize_t allocated = self->allocated;

    /* Bypass realloc() when a previous overallocation is large enough
       to accommodate the newsize.  If the newsize falls lower than half
       the allocated size, then proceed with the realloc() to shrink the list.
    */
    if (allocated >= newsize && newsize >= (allocated >> 1)) {
        assert(self->ob_item != NULL || newsize == 0);
        Py_SET_SIZE(self, newsize);
        return 0;
    }

    /* This over-allocates proportional to the list size, making room
     * for additional growth.  The over-allocation is mild, but is
     * enough to give linear-time amortized behavior over a long
     * sequence of appends() in the presence of a poorly-performing
     * system realloc().
     * The growth pattern is:  0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...
     * Note: new_allocated won't overflow because the largest possible value
     *       is PY_SSIZE_T_MAX * (9 / 8) + 6 which always fits in a size_t.
     */
    new_allocated = (size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6);
    if (new_allocated > (size_t)PY_SSIZE_T_MAX / sizeof(PyObject *)) {
        PyErr_NoMemory();
        return -1;
    }

    if (newsize == 0)
        new_allocated = 0;
    num_allocated_bytes = new_allocated * sizeof(PyObject *);
    items = (PyObject **)PyMem_Realloc(self->ob_item, num_allocated_bytes);
    if (items == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    self->ob_item = items;
    Py_SET_SIZE(self, newsize);
    self->allocated = new_allocated;
    return 0;
}

// Changed to use PyList_SetSlice instead of the internal list_ass_slice
static PyObject *
list_pop_impl(PyListObject *self, Py_ssize_t index)
{
    PyObject *v;
    int status;

    if (Py_SIZE(self) == 0) {
        /* Special-case most common failure cause */
        PyErr_SetString(PyExc_IndexError, "pop from empty list");
        return NULL;
    }
    if (index < 0)
        index += Py_SIZE(self);
    if (index < 0 || index >= Py_SIZE(self)) {
        PyErr_SetString(PyExc_IndexError, "pop index out of range");
        return NULL;
    }
    v = self->ob_item[index];
    if (index == Py_SIZE(self) - 1) {
        status = list_resize(self, Py_SIZE(self) - 1);
        if (status >= 0)
            return v; /* and v now owns the reference the list had */
        else
            return NULL;
    }
    Py_INCREF(v);
    status = PyList_SetSlice((PyObject *)self, index, index+1, (PyObject *)NULL);
    if (status < 0) {
        Py_DECREF(v);
        return NULL;
    }
    return v;
}

// Tweaked to directly use CPyTagged
static CPyTagged
list_count(PyListObject *self, PyObject *value)
{
    Py_ssize_t count = 0;
    Py_ssize_t i;

    for (i = 0; i < Py_SIZE(self); i++) {
        int cmp = PyObject_RichCompareBool(self->ob_item[i], value, Py_EQ);
        if (cmp > 0)
            count++;
        else if (cmp < 0)
            return CPY_INT_TAG;
    }
    return CPyTagged_ShortFromSsize_t(count);
}

#if PY_VERSION_HEX < 0x03080000
static PyObject *
_PyDict_GetItemStringWithError(PyObject *v, const char *key)
{
    PyObject *kv, *rv;
    kv = PyUnicode_FromString(key);
    if (kv == NULL) {
        return NULL;
    }
    rv = PyDict_GetItemWithError(v, kv);
    Py_DECREF(kv);
    return rv;
}
#endif

#define CPyUnicode_EqualToASCIIString(x, y) _PyUnicode_EqualToASCIIString(x, y)

// Adapted from genobject.c in Python 3.7.2
// Copied because it wasn't in 3.5.2 and it is undocumented anyways.
/*
 * Set StopIteration with specified value.  Value can be arbitrary object
 * or NULL.
 *
 * Returns 0 if StopIteration is set and -1 if any other exception is set.
 */
static int
CPyGen_SetStopIterationValue(PyObject *value)
{
    PyObject *e;

    if (value == NULL ||
        (!PyTuple_Check(value) && !PyExceptionInstance_Check(value)))
    {
        /* Delay exception instantiation if we can */
        PyErr_SetObject(PyExc_StopIteration, value);
        return 0;
    }
    /* Construct an exception instance manually with
     * PyObject_CallOneArg and pass it to PyErr_SetObject.
     *
     * We do this to handle a situation when "value" is a tuple, in which
     * case PyErr_SetObject would set the value of StopIteration to
     * the first element of the tuple.
     *
     * (See PyErr_SetObject/_PyErr_CreateException code for details.)
     */
    e = PyObject_CallOneArg(PyExc_StopIteration, value);
    if (e == NULL) {
        return -1;
    }
    PyErr_SetObject(PyExc_StopIteration, e);
    Py_DECREF(e);
    return 0;
}

// Copied from dictobject.c and dictobject.h, these are not Public before
// Python 3.8. Also remove some error checks that we do in the callers.
typedef struct {
    PyObject_HEAD
    PyDictObject *dv_dict;
} _CPyDictViewObject;

static PyObject *
_CPyDictView_New(PyObject *dict, PyTypeObject *type)
{
    _CPyDictViewObject *dv = PyObject_GC_New(_CPyDictViewObject, type);
    if (dv == NULL)
        return NULL;
    Py_INCREF(dict);
    dv->dv_dict = (PyDictObject *)dict;
    PyObject_GC_Track(dv);
    return (PyObject *)dv;
}

#ifdef __cplusplus
}
#endif

#if PY_VERSION_HEX >= 0x030A0000  // 3.10
static int
_CPyObject_HasAttrId(PyObject *v, _Py_Identifier *name) {
    PyObject *tmp = NULL;
    int result = _PyObject_LookupAttrId(v, name, &tmp);
    if (tmp) {
        Py_DECREF(tmp);
    }
    return result;
}
#else
#define _CPyObject_HasAttrId _PyObject_HasAttrId
#endif

#if PY_VERSION_HEX < 0x03090000
// OneArgs and NoArgs functions got added in 3.9
#define _PyObject_CallMethodIdNoArgs(self, name) \
    _PyObject_CallMethodIdObjArgs((self), (name), NULL)
#define _PyObject_CallMethodIdOneArg(self, name, arg) \
    _PyObject_CallMethodIdObjArgs((self), (name), (arg), NULL)
#endif

// Copied from genobject.c in Python 3.10
static int
gen_is_coroutine(PyObject *o)
{
    if (PyGen_CheckExact(o)) {
        PyCodeObject *code = (PyCodeObject *)((PyGenObject*)o)->gi_code;
        if (code->co_flags & CO_ITERABLE_COROUTINE) {
            return 1;
        }
    }
    return 0;
}

/*
 *   This helper function returns an awaitable for `o`:
 *     - `o` if `o` is a coroutine-object;
 *     - `type(o)->tp_as_async->am_await(o)`
 *
 *   Raises a TypeError if it's not possible to return
 *   an awaitable and returns NULL.
 */
static PyObject *
CPyCoro_GetAwaitableIter(PyObject *o)
{
    unaryfunc getter = NULL;
    PyTypeObject *ot;

    if (PyCoro_CheckExact(o) || gen_is_coroutine(o)) {
        /* 'o' is a coroutine. */
        Py_INCREF(o);
        return o;
    }

    ot = Py_TYPE(o);
    if (ot->tp_as_async != NULL) {
        getter = ot->tp_as_async->am_await;
    }
    if (getter != NULL) {
        PyObject *res = (*getter)(o);
        if (res != NULL) {
            if (PyCoro_CheckExact(res) || gen_is_coroutine(res)) {
                /* __await__ must return an *iterator*, not
                   a coroutine or another awaitable (see PEP 492) */
                PyErr_SetString(PyExc_TypeError,
                                "__await__() returned a coroutine");
                Py_CLEAR(res);
            } else if (!PyIter_Check(res)) {
                PyErr_Format(PyExc_TypeError,
                             "__await__() returned non-iterator "
                             "of type '%.100s'",
                             Py_TYPE(res)->tp_name);
                Py_CLEAR(res);
            }
        }
        return res;
    }

    PyErr_Format(PyExc_TypeError,
                 "object %.100s can't be used in 'await' expression",
                 ot->tp_name);
    return NULL;
}


#endif
