#ifndef GREENLET_EXCEPTIONS_HPP
#define GREENLET_EXCEPTIONS_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdexcept>
#include <string>

#ifdef __clang__
#    pragma clang diagnostic push
#    pragma clang diagnostic ignored "-Wunused-function"
#endif

namespace greenlet {

    class PyErrOccurred : public std::runtime_error
    {
    public:
        PyErrOccurred() : std::runtime_error("")
        {
            assert(PyErr_Occurred());
        }

        PyErrOccurred(PyObject* exc_kind, const char* const msg)
            : std::runtime_error(msg)
        {
            PyErr_SetString(exc_kind, msg);
        }
        PyErrOccurred(PyObject* exc_kind, const std::string msg)
            : std::runtime_error(msg)
        {
            // This copies the c_str, so we don't have any lifetime
            // issues to worry about.
            PyErr_SetString(exc_kind, msg.c_str());
        }
    };

    class TypeError : public PyErrOccurred
    {
    public:
        TypeError(const char* const what)
            : PyErrOccurred(PyExc_TypeError, what)
        {
        }
        TypeError(const std::string what)
            : PyErrOccurred(PyExc_TypeError, what)
        {
        }
    };

    class ValueError : public PyErrOccurred
    {
    public:
        ValueError(const char* const what)
            : PyErrOccurred(PyExc_ValueError, what)
        {
        }
    };

    class AttributeError : public PyErrOccurred
    {
    public:
        AttributeError(const char* const what)
            : PyErrOccurred(PyExc_AttributeError, what)
        {
        }
    };

    /**
     * Calls `Py_FatalError` when constructed, so you can't actually
     * throw this. It just makes static analysis easier.
     */
    class PyFatalError : public std::runtime_error
    {
    public:
        PyFatalError(const char* const msg)
            : std::runtime_error(msg)
        {
            Py_FatalError(msg);
        }
    };

    static inline PyObject*
    Require(PyObject* p)
    {
        if (!p) {
            throw PyErrOccurred();
        }
        return p;
    };

    static inline void
    Require(const int retval)
    {
        if (retval < 0) {
            throw PyErrOccurred();
        }
    };


};
#ifdef __clang__
#    pragma clang diagnostic pop
#endif

#endif
