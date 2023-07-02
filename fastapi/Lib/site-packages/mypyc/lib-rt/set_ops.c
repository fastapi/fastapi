// Set primitive operations
//
// These are registered in mypyc.primitives.set_ops.

#include <Python.h>
#include "CPy.h"

bool CPySet_Remove(PyObject *set, PyObject *key) {
    int success = PySet_Discard(set, key);
    if (success == 1) {
        return true;
    }
    if (success == 0) {
        _PyErr_SetKeyError(key);
    }
    return false;
}
