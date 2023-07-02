// String primitive operations
//
// These are registered in mypyc.primitives.str_ops.

#include <Python.h>
#include "CPy.h"

PyObject *CPyStr_GetItem(PyObject *str, CPyTagged index) {
    if (PyUnicode_READY(str) != -1) {
        if (CPyTagged_CheckShort(index)) {
            Py_ssize_t n = CPyTagged_ShortAsSsize_t(index);
            Py_ssize_t size = PyUnicode_GET_LENGTH(str);
            if (n < 0)
                n += size;
            if (n < 0 || n >= size) {
                PyErr_SetString(PyExc_IndexError, "string index out of range");
                return NULL;
            }
            enum PyUnicode_Kind kind = (enum PyUnicode_Kind)PyUnicode_KIND(str);
            void *data = PyUnicode_DATA(str);
            Py_UCS4 ch = PyUnicode_READ(kind, data, n);
            PyObject *unicode = PyUnicode_New(1, ch);
            if (unicode == NULL)
                return NULL;

            if (PyUnicode_KIND(unicode) == PyUnicode_1BYTE_KIND) {
                PyUnicode_1BYTE_DATA(unicode)[0] = (Py_UCS1)ch;
            } else if (PyUnicode_KIND(unicode) == PyUnicode_2BYTE_KIND) {
                PyUnicode_2BYTE_DATA(unicode)[0] = (Py_UCS2)ch;
            } else {
                assert(PyUnicode_KIND(unicode) == PyUnicode_4BYTE_KIND);
                PyUnicode_4BYTE_DATA(unicode)[0] = ch;
            }
            return unicode;
        } else {
            PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
            return NULL;
        }
    } else {
        PyObject *index_obj = CPyTagged_AsObject(index);
        return PyObject_GetItem(str, index_obj);
    }
}

// A simplification of _PyUnicode_JoinArray() from CPython 3.9.6
PyObject *CPyStr_Build(Py_ssize_t len, ...) {
    Py_ssize_t i;
    va_list args;

    // Calculate the total amount of space and check
    // whether all components have the same kind.
    Py_ssize_t sz = 0;
    Py_UCS4 maxchar = 0;
    int use_memcpy = 1; // Use memcpy by default
    PyObject *last_obj = NULL;

    va_start(args, len);
    for (i = 0; i < len; i++) {
        PyObject *item = va_arg(args, PyObject *);
        if (!PyUnicode_Check(item)) {
            PyErr_Format(PyExc_TypeError,
                         "sequence item %zd: expected str instance,"
                         " %.80s found",
                         i, Py_TYPE(item)->tp_name);
            return NULL;
        }
        if (PyUnicode_READY(item) == -1)
            return NULL;

        size_t add_sz = PyUnicode_GET_LENGTH(item);
        Py_UCS4 item_maxchar = PyUnicode_MAX_CHAR_VALUE(item);
        maxchar = Py_MAX(maxchar, item_maxchar);

        // Using size_t to avoid overflow during arithmetic calculation
        if (add_sz > (size_t)(PY_SSIZE_T_MAX - sz)) {
            PyErr_SetString(PyExc_OverflowError,
                            "join() result is too long for a Python string");
            return NULL;
        }
        sz += add_sz;

        // If these strings have different kind, we would call
        // _PyUnicode_FastCopyCharacters() in the following part.
        if (use_memcpy && last_obj != NULL) {
            if (PyUnicode_KIND(last_obj) != PyUnicode_KIND(item))
                use_memcpy = 0;
        }
        last_obj = item;
    }
    va_end(args);

    // Construct the string
    PyObject *res = PyUnicode_New(sz, maxchar);
    if (res == NULL)
        return NULL;

    if (use_memcpy) {
        unsigned char *res_data = PyUnicode_1BYTE_DATA(res);
        unsigned int kind = PyUnicode_KIND(res);

        va_start(args, len);
        for (i = 0; i < len; ++i) {
            PyObject *item = va_arg(args, PyObject *);
            Py_ssize_t itemlen = PyUnicode_GET_LENGTH(item);
            if (itemlen != 0) {
                memcpy(res_data, PyUnicode_DATA(item), kind * itemlen);
                res_data += kind * itemlen;
            }
        }
        va_end(args);
        assert(res_data == PyUnicode_1BYTE_DATA(res) + kind * PyUnicode_GET_LENGTH(res));
    } else {
        Py_ssize_t res_offset = 0;

        va_start(args, len);
        for (i = 0; i < len; ++i) {
            PyObject *item = va_arg(args, PyObject *);
            Py_ssize_t itemlen = PyUnicode_GET_LENGTH(item);
            if (itemlen != 0) {
                _PyUnicode_FastCopyCharacters(res, res_offset, item, 0, itemlen);
                res_offset += itemlen;
            }
        }
        va_end(args);
        assert(res_offset == PyUnicode_GET_LENGTH(res));
    }

    assert(_PyUnicode_CheckConsistency(res, 1));
    return res;
}

PyObject *CPyStr_Split(PyObject *str, PyObject *sep, CPyTagged max_split) {
    Py_ssize_t temp_max_split = CPyTagged_AsSsize_t(max_split);
    if (temp_max_split == -1 && PyErr_Occurred()) {
        PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
        return NULL;
    }
    return PyUnicode_Split(str, sep, temp_max_split);
}

PyObject *CPyStr_Replace(PyObject *str, PyObject *old_substr,
                         PyObject *new_substr, CPyTagged max_replace) {
    Py_ssize_t temp_max_replace = CPyTagged_AsSsize_t(max_replace);
    if (temp_max_replace == -1 && PyErr_Occurred()) {
        PyErr_SetString(PyExc_OverflowError, CPYTHON_LARGE_INT_ERRMSG);
        return NULL;
    }
    return PyUnicode_Replace(str, old_substr, new_substr, temp_max_replace);
}

bool CPyStr_Startswith(PyObject *self, PyObject *subobj) {
    Py_ssize_t start = 0;
    Py_ssize_t end = PyUnicode_GET_LENGTH(self);
    return PyUnicode_Tailmatch(self, subobj, start, end, -1);
}

bool CPyStr_Endswith(PyObject *self, PyObject *subobj) {
    Py_ssize_t start = 0;
    Py_ssize_t end = PyUnicode_GET_LENGTH(self);
    return PyUnicode_Tailmatch(self, subobj, start, end, 1);
}

/* This does a dodgy attempt to append in place  */
PyObject *CPyStr_Append(PyObject *o1, PyObject *o2) {
    PyUnicode_Append(&o1, o2);
    return o1;
}

PyObject *CPyStr_GetSlice(PyObject *obj, CPyTagged start, CPyTagged end) {
    if (likely(PyUnicode_CheckExact(obj)
               && CPyTagged_CheckShort(start) && CPyTagged_CheckShort(end))) {
        Py_ssize_t startn = CPyTagged_ShortAsSsize_t(start);
        Py_ssize_t endn = CPyTagged_ShortAsSsize_t(end);
        if (startn < 0) {
            startn += PyUnicode_GET_LENGTH(obj);
            if (startn < 0) {
                startn = 0;
            }
        }
        if (endn < 0) {
            endn += PyUnicode_GET_LENGTH(obj);
            if (endn < 0) {
                endn = 0;
            }
        }
        return PyUnicode_Substring(obj, startn, endn);
    }
    return CPyObject_GetSlice(obj, start, end);
}

/* Check if the given string is true (i.e. its length isn't zero) */
bool CPyStr_IsTrue(PyObject *obj) {
    Py_ssize_t length = PyUnicode_GET_LENGTH(obj);
    return length != 0;
}

Py_ssize_t CPyStr_Size_size_t(PyObject *str) {
    if (PyUnicode_READY(str) != -1) {
        return PyUnicode_GET_LENGTH(str);
    }
    return -1;
}

PyObject *CPy_Decode(PyObject *obj, PyObject *encoding, PyObject *errors) {
    const char *enc = NULL;
    const char *err = NULL;
    if (encoding) {
        enc = PyUnicode_AsUTF8AndSize(encoding, NULL);
        if (!enc) return NULL;
    }
    if (errors) {
        err = PyUnicode_AsUTF8AndSize(errors, NULL);
        if (!err) return NULL;
    }
    if (PyBytes_Check(obj)) {
        return PyUnicode_Decode(((PyBytesObject *)obj)->ob_sval,
                                ((PyVarObject *)obj)->ob_size,
                                enc, err);
    } else {
        return PyUnicode_FromEncodedObject(obj, enc, err);
    }
}

PyObject *CPy_Encode(PyObject *obj, PyObject *encoding, PyObject *errors) {
    const char *enc = NULL;
    const char *err = NULL;
    if (encoding) {
        enc = PyUnicode_AsUTF8AndSize(encoding, NULL);
        if (!enc) return NULL;
    }
    if (errors) {
        err = PyUnicode_AsUTF8AndSize(errors, NULL);
        if (!err) return NULL;
    }
    if (PyUnicode_Check(obj)) {
        return PyUnicode_AsEncodedString(obj, enc, err);
    } else {
        PyErr_BadArgument();
        return NULL;
    }
}
