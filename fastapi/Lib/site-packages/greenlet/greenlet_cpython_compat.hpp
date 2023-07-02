/* -*- indent-tabs-mode: nil; tab-width: 4; -*- */
#ifndef GREENLET_CPYTHON_COMPAT_H
#define GREENLET_CPYTHON_COMPAT_H

/**
 * Helpers for compatibility with multiple versions of CPython.
 */

#define PY_SSIZE_T_CLEAN
#include "Python.h"

// These enable writing template functions or classes specialized
// based on the Python version. Write both versions of the function,
// one with the WHEN version, one with the WHEN_NOT version.
// Instantiate the template using the G_IS_PY37 macro.
struct GREENLET_WHEN_PY37
{
    typedef GREENLET_WHEN_PY37* Yes;
    // We really just want an alias, `using Yes = IsIt`,
    // but old MSVC for Py27 doesn't support that.
    typedef GREENLET_WHEN_PY37* IsIt;
};

struct GREENLET_WHEN_NOT_PY37
{
    typedef GREENLET_WHEN_NOT_PY37* No;
    typedef GREENLET_WHEN_NOT_PY37* IsIt;
};


#if PY_VERSION_HEX >= 0x030700A3
#    define GREENLET_PY37 1
typedef GREENLET_WHEN_PY37 G_IS_PY37;
#else
#    define GREENLET_PY37 0
typedef GREENLET_WHEN_NOT_PY37 G_IS_PY37;
#endif


#if PY_VERSION_HEX >= 0x30A00B1
/*
Python 3.10 beta 1 changed tstate->use_tracing to a nested cframe member.
See https://github.com/python/cpython/pull/25276
We have to save and restore this as well.
*/
#    define GREENLET_USE_CFRAME 1
#else
#    define GREENLET_USE_CFRAME 0
#endif

#if PY_VERSION_HEX >= 0x30B00A4
/*
Greenlet won't compile on anything older than Python 3.11 alpha 4 (see
https://bugs.python.org/issue46090). Summary of breaking internal changes:
- Python 3.11 alpha 1 changed how frame objects are represented internally.
  - https://github.com/python/cpython/pull/30122
- Python 3.11 alpha 3 changed how recursion limits are stored.
  - https://github.com/python/cpython/pull/29524
- Python 3.11 alpha 4 changed how exception state is stored. It also includes a
  change to help greenlet save and restore the interpreter frame "data stack".
  - https://github.com/python/cpython/pull/30122
  - https://github.com/python/cpython/pull/30234
*/
#    define GREENLET_PY311 1
#else
#    define GREENLET_PY311 0
#endif

#ifndef Py_SET_REFCNT
/* Py_REFCNT and Py_SIZE macros are converted to functions
https://bugs.python.org/issue39573 */
#    define Py_SET_REFCNT(obj, refcnt) Py_REFCNT(obj) = (refcnt)
#endif

#ifndef _Py_DEC_REFTOTAL
/* _Py_DEC_REFTOTAL macro has been removed from Python 3.9 by:
  https://github.com/python/cpython/commit/49932fec62c616ec88da52642339d83ae719e924
*/
#    ifdef Py_REF_DEBUG
#        define _Py_DEC_REFTOTAL _Py_RefTotal--
#    else
#        define _Py_DEC_REFTOTAL
#    endif
#endif
// Define these flags like Cython does if we're on an old version.
#ifndef Py_TPFLAGS_CHECKTYPES
  #define Py_TPFLAGS_CHECKTYPES 0
#endif
#ifndef Py_TPFLAGS_HAVE_INDEX
  #define Py_TPFLAGS_HAVE_INDEX 0
#endif
#ifndef Py_TPFLAGS_HAVE_NEWBUFFER
  #define Py_TPFLAGS_HAVE_NEWBUFFER 0
#endif
#ifndef Py_TPFLAGS_HAVE_FINALIZE
  #define Py_TPFLAGS_HAVE_FINALIZE 0
#endif
#ifndef Py_TPFLAGS_HAVE_VERSION_TAG
   #define Py_TPFLAGS_HAVE_VERSION_TAG 0
#endif

#define G_TPFLAGS_DEFAULT Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_VERSION_TAG | Py_TPFLAGS_CHECKTYPES | Py_TPFLAGS_HAVE_NEWBUFFER | Py_TPFLAGS_HAVE_GC

#if PY_MAJOR_VERSION >= 3
#    define GNative_FromFormat PyUnicode_FromFormat
#else
#    define GNative_FromFormat PyString_FromFormat
#endif

#if PY_MAJOR_VERSION >= 3
#    define Greenlet_Intern PyUnicode_InternFromString
#else
#    define Greenlet_Intern PyString_InternFromString
#endif

#if PY_VERSION_HEX < 0x03090000
// The official version only became available in 3.9
#    define PyObject_GC_IsTracked(o) _PyObject_GC_IS_TRACKED(o)
#endif

#if PY_MAJOR_VERSION < 3
struct PyModuleDef {
    int unused;
    const char* const m_name;
    const char* m_doc;
    Py_ssize_t m_size;
    PyMethodDef* m_methods;
    // Then several more fields we're not currently using.
};
#define PyModuleDef_HEAD_INIT 1
PyObject* PyModule_Create(PyModuleDef* m)
{
    return Py_InitModule(m->m_name, m->m_methods);
}
#endif

// bpo-43760 added PyThreadState_EnterTracing() to Python 3.11.0a2
#if PY_VERSION_HEX < 0x030B00A2 && !defined(PYPY_VERSION)
static inline void PyThreadState_EnterTracing(PyThreadState *tstate)
{
    tstate->tracing++;
#if PY_VERSION_HEX >= 0x030A00A1
    tstate->cframe->use_tracing = 0;
#else
    tstate->use_tracing = 0;
#endif
}
#endif

// bpo-43760 added PyThreadState_LeaveTracing() to Python 3.11.0a2
#if PY_VERSION_HEX < 0x030B00A2 && !defined(PYPY_VERSION)
static inline void PyThreadState_LeaveTracing(PyThreadState *tstate)
{
    tstate->tracing--;
    int use_tracing = (tstate->c_tracefunc != NULL
                       || tstate->c_profilefunc != NULL);
#if PY_VERSION_HEX >= 0x030A00A1
    tstate->cframe->use_tracing = use_tracing;
#else
    tstate->use_tracing = use_tracing;
#endif
}
#endif

#endif /* GREENLET_CPYTHON_COMPAT_H */
