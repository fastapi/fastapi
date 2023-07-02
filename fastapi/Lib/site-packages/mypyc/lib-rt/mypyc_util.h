#ifndef MYPYC_UTIL_H
#define MYPYC_UTIL_H

#include <Python.h>
#include <frameobject.h>
#include <assert.h>

#if defined(__clang__) || defined(__GNUC__)
#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)
#define CPy_Unreachable() __builtin_unreachable()
#else
#define likely(x)       (x)
#define unlikely(x)     (x)
#define CPy_Unreachable() abort()
#endif

#if defined(__clang__) || defined(__GNUC__)
#define CPy_NOINLINE __attribute__((noinline))
#elif defined(_MSC_VER)
#define CPy_NOINLINE __declspec(noinline)
#else
#define CPy_NOINLINE
#endif

// INCREF and DECREF that assert the pointer is not NULL.
// asserts are disabled in release builds so there shouldn't be a perf hit.
// I'm honestly kind of surprised that this isn't done by default.
#define CPy_INCREF(p) do { assert(p); Py_INCREF(p); } while (0)
#define CPy_DECREF(p) do { assert(p); Py_DECREF(p); } while (0)
// Here just for consistency
#define CPy_XDECREF(p) Py_XDECREF(p)

// Tagged integer -- our representation of Python 'int' objects.
// Small enough integers are represented as unboxed integers (shifted
// left by 1); larger integers (larger than 63 bits on a 64-bit
// platform) are stored as a tagged pointer (PyObject *)
// representing a Python int object, with the lowest bit set.
// Tagged integers are always normalized. A small integer *must not*
// have the tag bit set.
typedef size_t CPyTagged;

typedef size_t CPyPtr;

#define CPY_INT_BITS (CHAR_BIT * sizeof(CPyTagged))

#define CPY_TAGGED_MAX (((Py_ssize_t)1 << (CPY_INT_BITS - 2)) - 1)
#define CPY_TAGGED_MIN (-((Py_ssize_t)1 << (CPY_INT_BITS - 2)))
#define CPY_TAGGED_ABS_MIN (0-(size_t)CPY_TAGGED_MIN)

typedef PyObject CPyModule;

// Tag bit used for long integers
#define CPY_INT_TAG 1

// Error value for fixed-width (low-level) integers
#define CPY_LL_INT_ERROR -113

// Error value for floats
#define CPY_FLOAT_ERROR -113.0

typedef void (*CPyVTableItem)(void);

static inline CPyTagged CPyTagged_ShortFromInt(int x) {
    return x << 1;
}

static inline CPyTagged CPyTagged_ShortFromSsize_t(Py_ssize_t x) {
    return x << 1;
}

#endif
