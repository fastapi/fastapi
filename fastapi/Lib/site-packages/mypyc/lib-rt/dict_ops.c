// Dict primitive operations
//
// These are registered in mypyc.primitives.dict_ops.

#include <Python.h>
#include "CPy.h"

#ifndef Py_TPFLAGS_MAPPING
#define Py_TPFLAGS_MAPPING (1 << 6)
#endif

// Dict subclasses like defaultdict override things in interesting
// ways, so we don't want to just directly use the dict methods. Not
// sure if it is actually worth doing all this stuff, but it saves
// some indirections.
PyObject *CPyDict_GetItem(PyObject *dict, PyObject *key) {
    if (PyDict_CheckExact(dict)) {
        PyObject *res = PyDict_GetItemWithError(dict, key);
        if (!res) {
            if (!PyErr_Occurred()) {
                PyErr_SetObject(PyExc_KeyError, key);
            }
        } else {
            Py_INCREF(res);
        }
        return res;
    } else {
        return PyObject_GetItem(dict, key);
    }
}

PyObject *CPyDict_Build(Py_ssize_t size, ...) {
    Py_ssize_t i;

    PyObject *res = _PyDict_NewPresized(size);
    if (res == NULL) {
        return NULL;
    }

    va_list args;
    va_start(args, size);

    for (i = 0; i < size; i++) {
        PyObject *key = va_arg(args, PyObject *);
        PyObject *value = va_arg(args, PyObject *);
        if (PyDict_SetItem(res, key, value)) {
            Py_DECREF(res);
            return NULL;
        }
    }

    va_end(args);
    return res;
}

PyObject *CPyDict_Get(PyObject *dict, PyObject *key, PyObject *fallback) {
    // We are dodgily assuming that get on a subclass doesn't have
    // different behavior.
    PyObject *res = PyDict_GetItemWithError(dict, key);
    if (!res) {
        if (PyErr_Occurred()) {
            return NULL;
        }
        res = fallback;
    }
    Py_INCREF(res);
    return res;
}

PyObject *CPyDict_GetWithNone(PyObject *dict, PyObject *key) {
    return CPyDict_Get(dict, key, Py_None);
}

PyObject *CPyDict_SetDefault(PyObject *dict, PyObject *key, PyObject *value) {
    if (PyDict_CheckExact(dict)) {
        PyObject* ret = PyDict_SetDefault(dict, key, value);
        Py_XINCREF(ret);
        return ret;
    }
    _Py_IDENTIFIER(setdefault);
    return _PyObject_CallMethodIdObjArgs(dict, &PyId_setdefault, key, value, NULL);
}

PyObject *CPyDict_SetDefaultWithNone(PyObject *dict, PyObject *key) {
    return CPyDict_SetDefault(dict, key, Py_None);
}

PyObject *CPyDict_SetDefaultWithEmptyDatatype(PyObject *dict, PyObject *key,
                                              int data_type) {
    PyObject *res = CPyDict_GetItem(dict, key);
    if (!res) {
        // CPyDict_GetItem() would generates a PyExc_KeyError
        // when key is not found.
        PyErr_Clear();

        PyObject *new_obj;
        if (data_type == 1) {
            new_obj = PyList_New(0);
        } else if (data_type == 2) {
            new_obj = PyDict_New();
        } else if (data_type == 3) {
            new_obj = PySet_New(NULL);
        } else {
            return NULL;
        }

        if (CPyDict_SetItem(dict, key, new_obj) == -1) {
            return NULL;
        } else {
            return new_obj;
        }
    } else {
        return res;
    }
}

int CPyDict_SetItem(PyObject *dict, PyObject *key, PyObject *value) {
    if (PyDict_CheckExact(dict)) {
        return PyDict_SetItem(dict, key, value);
    } else {
        return PyObject_SetItem(dict, key, value);
    }
}

static inline int CPy_ObjectToStatus(PyObject *obj) {
    if (obj) {
        Py_DECREF(obj);
        return 0;
    } else {
        return -1;
    }
}

static int CPyDict_UpdateGeneral(PyObject *dict, PyObject *stuff) {
    _Py_IDENTIFIER(update);
    PyObject *res = _PyObject_CallMethodIdOneArg(dict, &PyId_update, stuff);
    return CPy_ObjectToStatus(res);
}

int CPyDict_UpdateInDisplay(PyObject *dict, PyObject *stuff) {
    // from https://github.com/python/cpython/blob/55d035113dfb1bd90495c8571758f504ae8d4802/Python/ceval.c#L2710
    int ret = PyDict_Update(dict, stuff);
    if (ret < 0) {
        if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
            PyErr_Format(PyExc_TypeError,
                         "'%.200s' object is not a mapping",
                         Py_TYPE(stuff)->tp_name);
        }
    }
    return ret;
}

int CPyDict_Update(PyObject *dict, PyObject *stuff) {
    if (PyDict_CheckExact(dict)) {
        return PyDict_Update(dict, stuff);
    } else {
        return CPyDict_UpdateGeneral(dict, stuff);
    }
}

int CPyDict_UpdateFromAny(PyObject *dict, PyObject *stuff) {
    if (PyDict_CheckExact(dict)) {
        // Argh this sucks
        _Py_IDENTIFIER(keys);
        if (PyDict_Check(stuff) || _CPyObject_HasAttrId(stuff, &PyId_keys)) {
            return PyDict_Update(dict, stuff);
        } else {
            return PyDict_MergeFromSeq2(dict, stuff, 1);
        }
    } else {
        return CPyDict_UpdateGeneral(dict, stuff);
    }
}

PyObject *CPyDict_FromAny(PyObject *obj) {
    if (PyDict_Check(obj)) {
        return PyDict_Copy(obj);
    } else {
        int res;
        PyObject *dict = PyDict_New();
        if (!dict) {
            return NULL;
        }
        _Py_IDENTIFIER(keys);
        if (_CPyObject_HasAttrId(obj, &PyId_keys)) {
            res = PyDict_Update(dict, obj);
        } else {
            res = PyDict_MergeFromSeq2(dict, obj, 1);
        }
        if (res < 0) {
            Py_DECREF(dict);
            return NULL;
        }
        return dict;
    }
}

PyObject *CPyDict_KeysView(PyObject *dict) {
    if (PyDict_CheckExact(dict)){
        return _CPyDictView_New(dict, &PyDictKeys_Type);
    }
    _Py_IDENTIFIER(keys);
    return _PyObject_CallMethodIdNoArgs(dict, &PyId_keys);
}

PyObject *CPyDict_ValuesView(PyObject *dict) {
    if (PyDict_CheckExact(dict)){
        return _CPyDictView_New(dict, &PyDictValues_Type);
    }
    _Py_IDENTIFIER(values);
    return _PyObject_CallMethodIdNoArgs(dict, &PyId_values);
}

PyObject *CPyDict_ItemsView(PyObject *dict) {
    if (PyDict_CheckExact(dict)){
        return _CPyDictView_New(dict, &PyDictItems_Type);
    }
    _Py_IDENTIFIER(items);
    return _PyObject_CallMethodIdNoArgs(dict, &PyId_items);
}

PyObject *CPyDict_Keys(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        return PyDict_Keys(dict);
    }
    // Inline generic fallback logic to also return a list.
    PyObject *list = PyList_New(0);
    _Py_IDENTIFIER(keys);
    PyObject *view = _PyObject_CallMethodIdNoArgs(dict, &PyId_keys);
    if (view == NULL) {
        return NULL;
    }
    PyObject *res = _PyList_Extend((PyListObject *)list, view);
    Py_DECREF(view);
    if (res == NULL) {
        return NULL;
    }
    Py_DECREF(res);
    return list;
}

PyObject *CPyDict_Values(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        return PyDict_Values(dict);
    }
    // Inline generic fallback logic to also return a list.
    PyObject *list = PyList_New(0);
    _Py_IDENTIFIER(values);
    PyObject *view = _PyObject_CallMethodIdNoArgs(dict, &PyId_values);
    if (view == NULL) {
        return NULL;
    }
    PyObject *res = _PyList_Extend((PyListObject *)list, view);
    Py_DECREF(view);
    if (res == NULL) {
        return NULL;
    }
    Py_DECREF(res);
    return list;
}

PyObject *CPyDict_Items(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        return PyDict_Items(dict);
    }
    // Inline generic fallback logic to also return a list.
    PyObject *list = PyList_New(0);
    _Py_IDENTIFIER(items);
    PyObject *view = _PyObject_CallMethodIdNoArgs(dict, &PyId_items);
    if (view == NULL) {
        return NULL;
    }
    PyObject *res = _PyList_Extend((PyListObject *)list, view);
    Py_DECREF(view);
    if (res == NULL) {
        return NULL;
    }
    Py_DECREF(res);
    return list;
}

char CPyDict_Clear(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        PyDict_Clear(dict);
    } else {
        _Py_IDENTIFIER(clear);
        PyObject *res = _PyObject_CallMethodIdNoArgs(dict, &PyId_clear);
        if (res == NULL) {
            return 0;
        }
    }
    return 1;
}

PyObject *CPyDict_Copy(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        return PyDict_Copy(dict);
    }
    _Py_IDENTIFIER(copy);
    return _PyObject_CallMethodIdNoArgs(dict, &PyId_copy);
}

PyObject *CPyDict_GetKeysIter(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        // Return dict itself to indicate we can use fast path instead.
        Py_INCREF(dict);
        return dict;
    }
    return PyObject_GetIter(dict);
}

PyObject *CPyDict_GetItemsIter(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        // Return dict itself to indicate we can use fast path instead.
        Py_INCREF(dict);
        return dict;
    }
    _Py_IDENTIFIER(items);
    PyObject *view = _PyObject_CallMethodIdNoArgs(dict, &PyId_items);
    if (view == NULL) {
        return NULL;
    }
    PyObject *iter = PyObject_GetIter(view);
    Py_DECREF(view);
    return iter;
}

PyObject *CPyDict_GetValuesIter(PyObject *dict) {
    if (PyDict_CheckExact(dict)) {
        // Return dict itself to indicate we can use fast path instead.
        Py_INCREF(dict);
        return dict;
    }
    _Py_IDENTIFIER(values);
    PyObject *view = _PyObject_CallMethodIdNoArgs(dict, &PyId_values);
    if (view == NULL) {
        return NULL;
    }
    PyObject *iter = PyObject_GetIter(view);
    Py_DECREF(view);
    return iter;
}

static void _CPyDict_FromNext(tuple_T3CIO *ret, PyObject *dict_iter) {
    // Get next item from iterator and set "should continue" flag.
    ret->f2 = PyIter_Next(dict_iter);
    if (ret->f2 == NULL) {
        ret->f0 = 0;
        Py_INCREF(Py_None);
        ret->f2 = Py_None;
    } else {
        ret->f0 = 1;
    }
}

// Helpers for fast dictionary iteration, return a single tuple
// instead of writing to multiple registers, for exact dicts use
// the fast path, and fall back to generic iterator logic for subclasses.
tuple_T3CIO CPyDict_NextKey(PyObject *dict_or_iter, CPyTagged offset) {
    tuple_T3CIO ret;
    Py_ssize_t py_offset = CPyTagged_AsSsize_t(offset);
    PyObject *dummy;

    if (PyDict_CheckExact(dict_or_iter)) {
        ret.f0 = PyDict_Next(dict_or_iter, &py_offset, &ret.f2, &dummy);
        if (ret.f0) {
            ret.f1 = CPyTagged_FromSsize_t(py_offset);
        } else {
            // Set key to None, so mypyc can manage refcounts.
            ret.f1 = 0;
            ret.f2 = Py_None;
        }
        // PyDict_Next() returns borrowed references.
        Py_INCREF(ret.f2);
    } else {
        // offset is dummy in this case, just use the old value.
        ret.f1 = offset;
        _CPyDict_FromNext(&ret, dict_or_iter);
    }
    return ret;
}

tuple_T3CIO CPyDict_NextValue(PyObject *dict_or_iter, CPyTagged offset) {
    tuple_T3CIO ret;
    Py_ssize_t py_offset = CPyTagged_AsSsize_t(offset);
    PyObject *dummy;

    if (PyDict_CheckExact(dict_or_iter)) {
        ret.f0 = PyDict_Next(dict_or_iter, &py_offset, &dummy, &ret.f2);
        if (ret.f0) {
            ret.f1 = CPyTagged_FromSsize_t(py_offset);
        } else {
            // Set value to None, so mypyc can manage refcounts.
            ret.f1 = 0;
            ret.f2 = Py_None;
        }
        // PyDict_Next() returns borrowed references.
        Py_INCREF(ret.f2);
    } else {
        // offset is dummy in this case, just use the old value.
        ret.f1 = offset;
        _CPyDict_FromNext(&ret, dict_or_iter);
    }
    return ret;
}

tuple_T4CIOO CPyDict_NextItem(PyObject *dict_or_iter, CPyTagged offset) {
    tuple_T4CIOO ret;
    Py_ssize_t py_offset = CPyTagged_AsSsize_t(offset);

    if (PyDict_CheckExact(dict_or_iter)) {
        ret.f0 = PyDict_Next(dict_or_iter, &py_offset, &ret.f2, &ret.f3);
        if (ret.f0) {
            ret.f1 = CPyTagged_FromSsize_t(py_offset);
        } else {
            // Set key and value to None, so mypyc can manage refcounts.
            ret.f1 = 0;
            ret.f2 = Py_None;
            ret.f3 = Py_None;
        }
    } else {
        ret.f1 = offset;
        PyObject *item = PyIter_Next(dict_or_iter);
        if (item == NULL || !PyTuple_Check(item) || PyTuple_GET_SIZE(item) != 2) {
            if (item != NULL) {
                PyErr_SetString(PyExc_TypeError, "a tuple of length 2 expected");
            }
            ret.f0 = 0;
            ret.f2 = Py_None;
            ret.f3 = Py_None;
        } else {
            ret.f0 = 1;
            ret.f2 = PyTuple_GET_ITEM(item, 0);
            ret.f3 = PyTuple_GET_ITEM(item, 1);
            Py_DECREF(item);
        }
    }
    // PyDict_Next() returns borrowed references.
    Py_INCREF(ret.f2);
    Py_INCREF(ret.f3);
    return ret;
}

int CPyMapping_Check(PyObject *obj) {
    return Py_TYPE(obj)->tp_flags & Py_TPFLAGS_MAPPING;
}
