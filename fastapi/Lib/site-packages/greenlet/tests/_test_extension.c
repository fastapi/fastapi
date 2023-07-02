/* This is a set of functions used by test_extension_interface.py to test the
 * Greenlet C API.
 */

#include "../greenlet.h"

#ifndef Py_RETURN_NONE
#    define Py_RETURN_NONE return Py_INCREF(Py_None), Py_None
#endif

#define TEST_MODULE_NAME "_test_extension"

static PyObject*
test_switch(PyObject* self, PyObject* greenlet)
{
    PyObject* result = NULL;

    if (greenlet == NULL || !PyGreenlet_Check(greenlet)) {
        PyErr_BadArgument();
        return NULL;
    }

    result = PyGreenlet_Switch((PyGreenlet*)greenlet, NULL, NULL);
    if (result == NULL) {
        if (!PyErr_Occurred()) {
            PyErr_SetString(PyExc_AssertionError,
                            "greenlet.switch() failed for some reason.");
        }
        return NULL;
    }
    Py_INCREF(result);
    return result;
}

static PyObject*
test_switch_kwargs(PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyGreenlet* g = NULL;
    PyObject* result = NULL;

    PyArg_ParseTuple(args, "O!", &PyGreenlet_Type, &g);

    if (g == NULL || !PyGreenlet_Check(g)) {
        PyErr_BadArgument();
        return NULL;
    }

    result = PyGreenlet_Switch(g, NULL, kwargs);
    if (result == NULL) {
        if (!PyErr_Occurred()) {
            PyErr_SetString(PyExc_AssertionError,
                            "greenlet.switch() failed for some reason.");
        }
        return NULL;
    }
    Py_XINCREF(result);
    return result;
}

static PyObject*
test_getcurrent(PyObject* self)
{
    PyGreenlet* g = PyGreenlet_GetCurrent();
    if (g == NULL || !PyGreenlet_Check(g) || !PyGreenlet_ACTIVE(g)) {
        PyErr_SetString(PyExc_AssertionError,
                        "getcurrent() returned an invalid greenlet");
        Py_XDECREF(g);
        return NULL;
    }
    Py_DECREF(g);
    Py_RETURN_NONE;
}

static PyObject*
test_setparent(PyObject* self, PyObject* arg)
{
    PyGreenlet* current;
    PyGreenlet* greenlet = NULL;

    if (arg == NULL || !PyGreenlet_Check(arg)) {
        PyErr_BadArgument();
        return NULL;
    }
    if ((current = PyGreenlet_GetCurrent()) == NULL) {
        return NULL;
    }
    greenlet = (PyGreenlet*)arg;
    if (PyGreenlet_SetParent(greenlet, current)) {
        Py_DECREF(current);
        return NULL;
    }
    Py_DECREF(current);
    if (PyGreenlet_Switch(greenlet, NULL, NULL) == NULL) {
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject*
test_new_greenlet(PyObject* self, PyObject* callable)
{
    PyObject* result = NULL;
    PyGreenlet* greenlet = PyGreenlet_New(callable, NULL);

    if (!greenlet) {
        return NULL;
    }

    result = PyGreenlet_Switch(greenlet, NULL, NULL);
    Py_CLEAR(greenlet);
    if (result == NULL) {
        return NULL;
    }

    Py_INCREF(result);
    return result;
}

static PyObject*
test_raise_dead_greenlet(PyObject* self)
{
    PyErr_SetString(PyExc_GreenletExit, "test GreenletExit exception.");
    return NULL;
}

static PyObject*
test_raise_greenlet_error(PyObject* self)
{
    PyErr_SetString(PyExc_GreenletError, "test greenlet.error exception");
    return NULL;
}

static PyObject*
test_throw(PyObject* self, PyGreenlet* g)
{
    const char msg[] = "take that sucka!";
    PyObject* msg_obj = Py_BuildValue("s", msg);
    PyGreenlet_Throw(g, PyExc_ValueError, msg_obj, NULL);
    Py_DECREF(msg_obj);
    if (PyErr_Occurred()) {
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject*
test_throw_exact(PyObject* self, PyObject* args)
{
    PyGreenlet* g = NULL;
    PyObject* typ = NULL;
    PyObject* val = NULL;
    PyObject* tb = NULL;

    if (!PyArg_ParseTuple(args, "OOOO:throw", &g, &typ, &val, &tb)) {
        return NULL;
    }

    PyGreenlet_Throw(g, typ, val, tb);
    if (PyErr_Occurred()) {
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyMethodDef test_methods[] = {
    {"test_switch",
     (PyCFunction)test_switch,
     METH_O,
     "Switch to the provided greenlet sending provided arguments, and \n"
     "return the results."},
    {"test_switch_kwargs",
     (PyCFunction)test_switch_kwargs,
     METH_VARARGS | METH_KEYWORDS,
     "Switch to the provided greenlet sending the provided keyword args."},
    {"test_getcurrent",
     (PyCFunction)test_getcurrent,
     METH_NOARGS,
     "Test PyGreenlet_GetCurrent()"},
    {"test_setparent",
     (PyCFunction)test_setparent,
     METH_O,
     "Se the parent of the provided greenlet and switch to it."},
    {"test_new_greenlet",
     (PyCFunction)test_new_greenlet,
     METH_O,
     "Test PyGreenlet_New()"},
    {"test_raise_dead_greenlet",
     (PyCFunction)test_raise_dead_greenlet,
     METH_NOARGS,
     "Just raise greenlet.GreenletExit"},
    {"test_raise_greenlet_error",
     (PyCFunction)test_raise_greenlet_error,
     METH_NOARGS,
     "Just raise greenlet.error"},
    {"test_throw",
     (PyCFunction)test_throw,
     METH_O,
     "Throw a ValueError at the provided greenlet"},
    {"test_throw_exact",
     (PyCFunction)test_throw_exact,
     METH_VARARGS,
     "Throw exactly the arguments given at the provided greenlet"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
#    define INITERROR return NULL

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT,
                                       TEST_MODULE_NAME,
                                       NULL,
                                       0,
                                       test_methods,
                                       NULL,
                                       NULL,
                                       NULL,
                                       NULL};

PyMODINIT_FUNC
PyInit__test_extension(void)
#else
#    define INITERROR return
PyMODINIT_FUNC
init_test_extension(void)
#endif
{
    PyObject* module = NULL;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&moduledef);
#else
    module = Py_InitModule(TEST_MODULE_NAME, test_methods);
#endif

    if (module == NULL) {
        INITERROR;
    }

    PyGreenlet_Import();

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
