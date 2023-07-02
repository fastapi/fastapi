// Int primitive operations (tagged arbitrary-precision integers)
//
// These are registered in mypyc.primitives.int_ops.

#include <Python.h>
#include "CPy.h"

#ifndef _WIN32
// On 64-bit Linux and macOS, ssize_t and long are both 64 bits, and
// PyLong_FromLong is faster than PyLong_FromSsize_t, so use the faster one
#define CPyLong_FromSsize_t PyLong_FromLong
#else
// On 64-bit Windows, ssize_t is 64 bits but long is 32 bits, so we
// can't use the above trick
#define CPyLong_FromSsize_t PyLong_FromSsize_t
#endif

CPyTagged CPyTagged_FromSsize_t(Py_ssize_t value) {
    // We use a Python object if the value shifted left by 1 is too
    // large for Py_ssize_t
    if (unlikely(CPyTagged_TooBig(value))) {
        PyObject *object = PyLong_FromSsize_t(value);
        return ((CPyTagged)object) | CPY_INT_TAG;
    } else {
        return value << 1;
    }
}

CPyTagged CPyTagged_FromVoidPtr(void *ptr) {
    if ((uintptr_t)ptr > PY_SSIZE_T_MAX) {
        PyObject *object = PyLong_FromVoidPtr(ptr);
        return ((CPyTagged)object) | CPY_INT_TAG;
    } else {
        return CPyTagged_FromSsize_t((Py_ssize_t)ptr);
    }
}

CPyTagged CPyTagged_FromInt64(int64_t value) {
    if (unlikely(CPyTagged_TooBigInt64(value))) {
        PyObject *object = PyLong_FromLongLong(value);
        return ((CPyTagged)object) | CPY_INT_TAG;
    } else {
        return value << 1;
    }
}

CPyTagged CPyTagged_FromObject(PyObject *object) {
    int overflow;
    // The overflow check knows about CPyTagged's width
    Py_ssize_t value = CPyLong_AsSsize_tAndOverflow(object, &overflow);
    if (unlikely(overflow != 0)) {
        Py_INCREF(object);
        return ((CPyTagged)object) | CPY_INT_TAG;
    } else {
        return value << 1;
    }
}

CPyTagged CPyTagged_StealFromObject(PyObject *object) {
    int overflow;
    // The overflow check knows about CPyTagged's width
    Py_ssize_t value = CPyLong_AsSsize_tAndOverflow(object, &overflow);
    if (unlikely(overflow != 0)) {
        return ((CPyTagged)object) | CPY_INT_TAG;
    } else {
        Py_DECREF(object);
        return value << 1;
    }
}

CPyTagged CPyTagged_BorrowFromObject(PyObject *object) {
    int overflow;
    // The overflow check knows about CPyTagged's width
    Py_ssize_t value = CPyLong_AsSsize_tAndOverflow(object, &overflow);
    if (unlikely(overflow != 0)) {
        return ((CPyTagged)object) | CPY_INT_TAG;
    } else {
        return value << 1;
    }
}

PyObject *CPyTagged_AsObject(CPyTagged x) {
    PyObject *value;
    if (unlikely(CPyTagged_CheckLong(x))) {
        value = CPyTagged_LongAsObject(x);
        Py_INCREF(value);
    } else {
        value = CPyLong_FromSsize_t(CPyTagged_ShortAsSsize_t(x));
        if (value == NULL) {
            CPyError_OutOfMemory();
        }
    }
    return value;
}

PyObject *CPyTagged_StealAsObject(CPyTagged x) {
    PyObject *value;
    if (unlikely(CPyTagged_CheckLong(x))) {
        value = CPyTagged_LongAsObject(x);
    } else {
        value = CPyLong_FromSsize_t(CPyTagged_ShortAsSsize_t(x));
        if (value == NULL) {
            CPyError_OutOfMemory();
        }
    }
    return value;
}

Py_ssize_t CPyTagged_AsSsize_t(CPyTagged x) {
    if (likely(CPyTagged_CheckShort(x))) {
        return CPyTagged_ShortAsSsize_t(x);
    } else {
        return PyLong_AsSsize_t(CPyTagged_LongAsObject(x));
    }
}

CPy_NOINLINE
void CPyTagged_IncRef(CPyTagged x) {
    if (unlikely(CPyTagged_CheckLong(x))) {
        Py_INCREF(CPyTagged_LongAsObject(x));
    }
}

CPy_NOINLINE
void CPyTagged_DecRef(CPyTagged x) {
    if (unlikely(CPyTagged_CheckLong(x))) {
        Py_DECREF(CPyTagged_LongAsObject(x));
    }
}

CPy_NOINLINE
void CPyTagged_XDecRef(CPyTagged x) {
    if (unlikely(CPyTagged_CheckLong(x))) {
        Py_XDECREF(CPyTagged_LongAsObject(x));
    }
}

CPyTagged CPyTagged_Negate(CPyTagged num) {
    if (CPyTagged_CheckShort(num)
            && num != (CPyTagged) ((Py_ssize_t)1 << (CPY_INT_BITS - 1))) {
        // The only possibility of an overflow error happening when negating a short is if we
        // attempt to negate the most negative number.
        return -num;
    }
    PyObject *num_obj = CPyTagged_AsObject(num);
    PyObject *result = PyNumber_Negative(num_obj);
    if (result == NULL) {
        CPyError_OutOfMemory();
    }
    Py_DECREF(num_obj);
    return CPyTagged_StealFromObject(result);
}

CPyTagged CPyTagged_Add(CPyTagged left, CPyTagged right) {
    // TODO: Use clang/gcc extension __builtin_saddll_overflow instead.
    if (likely(CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right))) {
        CPyTagged sum = left + right;
        if (likely(!CPyTagged_IsAddOverflow(sum, left, right))) {
            return sum;
        }
    }
    PyObject *left_obj = CPyTagged_AsObject(left);
    PyObject *right_obj = CPyTagged_AsObject(right);
    PyObject *result = PyNumber_Add(left_obj, right_obj);
    if (result == NULL) {
        CPyError_OutOfMemory();
    }
    Py_DECREF(left_obj);
    Py_DECREF(right_obj);
    return CPyTagged_StealFromObject(result);
}

CPyTagged CPyTagged_Subtract(CPyTagged left, CPyTagged right) {
    // TODO: Use clang/gcc extension __builtin_saddll_overflow instead.
    if (likely(CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right))) {
        CPyTagged diff = left - right;
        if (likely(!CPyTagged_IsSubtractOverflow(diff, left, right))) {
            return diff;
        }
    }
    PyObject *left_obj = CPyTagged_AsObject(left);
    PyObject *right_obj = CPyTagged_AsObject(right);
    PyObject *result = PyNumber_Subtract(left_obj, right_obj);
    if (result == NULL) {
        CPyError_OutOfMemory();
    }
    Py_DECREF(left_obj);
    Py_DECREF(right_obj);
    return CPyTagged_StealFromObject(result);
}

CPyTagged CPyTagged_Multiply(CPyTagged left, CPyTagged right) {
    // TODO: Consider using some clang/gcc extension
    if (CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right)) {
        if (!CPyTagged_IsMultiplyOverflow(left, right)) {
            return left * CPyTagged_ShortAsSsize_t(right);
        }
    }
    PyObject *left_obj = CPyTagged_AsObject(left);
    PyObject *right_obj = CPyTagged_AsObject(right);
    PyObject *result = PyNumber_Multiply(left_obj, right_obj);
    if (result == NULL) {
        CPyError_OutOfMemory();
    }
    Py_DECREF(left_obj);
    Py_DECREF(right_obj);
    return CPyTagged_StealFromObject(result);
}

CPyTagged CPyTagged_FloorDivide(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left)
        && CPyTagged_CheckShort(right)
        && !CPyTagged_MaybeFloorDivideFault(left, right)) {
        Py_ssize_t result = CPyTagged_ShortAsSsize_t(left) / CPyTagged_ShortAsSsize_t(right);
        if (((Py_ssize_t)left < 0) != (((Py_ssize_t)right) < 0)) {
            if (result * right != left) {
                // Round down
                result--;
            }
        }
        return result << 1;
    }
    PyObject *left_obj = CPyTagged_AsObject(left);
    PyObject *right_obj = CPyTagged_AsObject(right);
    PyObject *result = PyNumber_FloorDivide(left_obj, right_obj);
    Py_DECREF(left_obj);
    Py_DECREF(right_obj);
    // Handle exceptions honestly because it could be ZeroDivisionError
    if (result == NULL) {
        return CPY_INT_TAG;
    } else {
        return CPyTagged_StealFromObject(result);
    }
}

CPyTagged CPyTagged_Remainder(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right)
        && !CPyTagged_MaybeRemainderFault(left, right)) {
        Py_ssize_t result = (Py_ssize_t)left % (Py_ssize_t)right;
        if (((Py_ssize_t)right < 0) != ((Py_ssize_t)left < 0) && result != 0) {
            result += right;
        }
        return result;
    }
    PyObject *left_obj = CPyTagged_AsObject(left);
    PyObject *right_obj = CPyTagged_AsObject(right);
    PyObject *result = PyNumber_Remainder(left_obj, right_obj);
    Py_DECREF(left_obj);
    Py_DECREF(right_obj);
    // Handle exceptions honestly because it could be ZeroDivisionError
    if (result == NULL) {
        return CPY_INT_TAG;
    } else {
        return CPyTagged_StealFromObject(result);
    }
}

bool CPyTagged_IsEq_(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(right)) {
        return false;
    } else {
        PyObject *left_obj = CPyTagged_AsObject(left);
        PyObject *right_obj = CPyTagged_AsObject(right);
        int result = PyObject_RichCompareBool(left_obj, right_obj, Py_EQ);
        Py_DECREF(left_obj);
        Py_DECREF(right_obj);
        if (result == -1) {
            CPyError_OutOfMemory();
        }
        return result;
    }
}

bool CPyTagged_IsLt_(CPyTagged left, CPyTagged right) {
    PyObject *left_obj = CPyTagged_AsObject(left);
    PyObject *right_obj = CPyTagged_AsObject(right);
    int result = PyObject_RichCompareBool(left_obj, right_obj, Py_LT);
    Py_DECREF(left_obj);
    Py_DECREF(right_obj);
    if (result == -1) {
        CPyError_OutOfMemory();
    }
    return result;
}

PyObject *CPyLong_FromStrWithBase(PyObject *o, CPyTagged base) {
    Py_ssize_t base_size_t = CPyTagged_AsSsize_t(base);
    return PyLong_FromUnicodeObject(o, base_size_t);
}

PyObject *CPyLong_FromStr(PyObject *o) {
    CPyTagged base = CPyTagged_FromSsize_t(10);
    return CPyLong_FromStrWithBase(o, base);
}

CPyTagged CPyTagged_FromFloat(double f) {
    if (f < ((double)CPY_TAGGED_MAX + 1.0) && f > (CPY_TAGGED_MIN - 1.0)) {
        return (Py_ssize_t)f << 1;
    }
    PyObject *o = PyLong_FromDouble(f);
    if (o == NULL)
        return CPY_INT_TAG;
    return CPyTagged_StealFromObject(o);
}

PyObject *CPyBool_Str(bool b) {
    return PyObject_Str(b ? Py_True : Py_False);
}

static void CPyLong_NormalizeUnsigned(PyLongObject *v) {
    Py_ssize_t i = v->ob_base.ob_size;
    while (i > 0 && v->ob_digit[i - 1] == 0)
        i--;
    v->ob_base.ob_size = i;
}

// Bitwise op '&', '|' or '^' using the generic (slow) API
static CPyTagged GenericBitwiseOp(CPyTagged a, CPyTagged b, char op) {
    PyObject *aobj = CPyTagged_AsObject(a);
    PyObject *bobj = CPyTagged_AsObject(b);
    PyObject *r;
    if (op == '&') {
        r = PyNumber_And(aobj, bobj);
    } else if (op == '|') {
        r = PyNumber_Or(aobj, bobj);
    } else {
        r = PyNumber_Xor(aobj, bobj);
    }
    if (unlikely(r == NULL)) {
        CPyError_OutOfMemory();
    }
    Py_DECREF(aobj);
    Py_DECREF(bobj);
    return CPyTagged_StealFromObject(r);
}

// Return pointer to digits of a PyLong object. If it's a short
// integer, place digits in the buffer buf instead to avoid memory
// allocation (it's assumed to be big enough). Return the number of
// digits in *size. *size is negative if the integer is negative.
static digit *GetIntDigits(CPyTagged n, Py_ssize_t *size, digit *buf) {
    if (CPyTagged_CheckShort(n)) {
        Py_ssize_t val = CPyTagged_ShortAsSsize_t(n);
        bool neg = val < 0;
        int len = 1;
        if (neg) {
            val = -val;
        }
        buf[0] = val & PyLong_MASK;
        if (val > (Py_ssize_t)PyLong_MASK) {
            val >>= PyLong_SHIFT;
            buf[1] = val & PyLong_MASK;
            if (val > (Py_ssize_t)PyLong_MASK) {
                buf[2] = val >> PyLong_SHIFT;
                len = 3;
            } else {
                len = 2;
            }
        }
        *size = neg ? -len : len;
        return buf;
    } else {
        PyLongObject *obj = (PyLongObject *)CPyTagged_LongAsObject(n);
        *size = obj->ob_base.ob_size;
        return obj->ob_digit;
    }
}

// Shared implementation of bitwise '&', '|' and '^' (specified by op) for at least
// one long operand. This is somewhat optimized for performance.
static CPyTagged BitwiseLongOp(CPyTagged a, CPyTagged b, char op) {
    // Directly access the digits, as there is no fast C API function for this.
    digit abuf[3];
    digit bbuf[3];
    Py_ssize_t asize;
    Py_ssize_t bsize;
    digit *adigits = GetIntDigits(a, &asize, abuf);
    digit *bdigits = GetIntDigits(b, &bsize, bbuf);

    PyLongObject *r;
    if (unlikely(asize < 0 || bsize < 0)) {
        // Negative operand. This is slower, but bitwise ops on them are pretty rare.
        return GenericBitwiseOp(a, b, op);
    }
    // Optimized implementation for two non-negative integers.
    // Swap a and b as needed to ensure a is no longer than b.
    if (asize > bsize) {
        digit *tmp = adigits;
        adigits = bdigits;
        bdigits = tmp;
        Py_ssize_t tmp_size = asize;
        asize = bsize;
        bsize = tmp_size;
    }
    r = _PyLong_New(op == '&' ? asize : bsize);
    if (unlikely(r == NULL)) {
        CPyError_OutOfMemory();
    }
    Py_ssize_t i;
    if (op == '&') {
        for (i = 0; i < asize; i++) {
            r->ob_digit[i] = adigits[i] & bdigits[i];
        }
    } else {
        if (op == '|') {
            for (i = 0; i < asize; i++) {
                r->ob_digit[i] = adigits[i] | bdigits[i];
            }
        } else {
            for (i = 0; i < asize; i++) {
                r->ob_digit[i] = adigits[i] ^ bdigits[i];
            }
        }
        for (; i < bsize; i++) {
            r->ob_digit[i] = bdigits[i];
        }
    }
    CPyLong_NormalizeUnsigned(r);
    return CPyTagged_StealFromObject((PyObject *)r);
}

// Bitwise '&'
CPyTagged CPyTagged_And(CPyTagged left, CPyTagged right) {
    if (likely(CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right))) {
        return left & right;
    }
    return BitwiseLongOp(left, right, '&');
}

// Bitwise '|'
CPyTagged CPyTagged_Or(CPyTagged left, CPyTagged right) {
    if (likely(CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right))) {
        return left | right;
    }
    return BitwiseLongOp(left, right, '|');
}

// Bitwise '^'
CPyTagged CPyTagged_Xor(CPyTagged left, CPyTagged right) {
    if (likely(CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right))) {
        return left ^ right;
    }
    return BitwiseLongOp(left, right, '^');
}

// Bitwise '~'
CPyTagged CPyTagged_Invert(CPyTagged num) {
    if (likely(CPyTagged_CheckShort(num) && num != CPY_TAGGED_ABS_MIN)) {
        return ~num & ~CPY_INT_TAG;
    } else {
        PyObject *obj = CPyTagged_AsObject(num);
        PyObject *result = PyNumber_Invert(obj);
        if (unlikely(result == NULL)) {
            CPyError_OutOfMemory();
        }
        Py_DECREF(obj);
        return CPyTagged_StealFromObject(result);
    }
}

// Bitwise '>>'
CPyTagged CPyTagged_Rshift(CPyTagged left, CPyTagged right) {
    if (likely(CPyTagged_CheckShort(left)
               && CPyTagged_CheckShort(right)
               && (Py_ssize_t)right >= 0)) {
        CPyTagged count = CPyTagged_ShortAsSsize_t(right);
        if (unlikely(count >= CPY_INT_BITS)) {
            if ((Py_ssize_t)left >= 0) {
                return 0;
            } else {
                return CPyTagged_ShortFromInt(-1);
            }
        }
        return ((Py_ssize_t)left >> count) & ~CPY_INT_TAG;
    } else {
        // Long integer or negative shift -- use generic op
        PyObject *lobj = CPyTagged_AsObject(left);
        PyObject *robj = CPyTagged_AsObject(right);
        PyObject *result = PyNumber_Rshift(lobj, robj);
        Py_DECREF(lobj);
        Py_DECREF(robj);
        if (result == NULL) {
            // Propagate error (could be negative shift count)
            return CPY_INT_TAG;
        }
        return CPyTagged_StealFromObject(result);
    }
}

static inline bool IsShortLshiftOverflow(Py_ssize_t short_int, Py_ssize_t shift) {
    return ((Py_ssize_t)(short_int << shift) >> shift) != short_int;
}

// Bitwise '<<'
CPyTagged CPyTagged_Lshift(CPyTagged left, CPyTagged right) {
    if (likely(CPyTagged_CheckShort(left)
               && CPyTagged_CheckShort(right)
               && (Py_ssize_t)right >= 0
               && right < CPY_INT_BITS * 2)) {
        CPyTagged shift = CPyTagged_ShortAsSsize_t(right);
        if (!IsShortLshiftOverflow(left, shift))
            // Short integers, no overflow
            return left << shift;
    }
    // Long integer or out of range shift -- use generic op
    PyObject *lobj = CPyTagged_AsObject(left);
    PyObject *robj = CPyTagged_AsObject(right);
    PyObject *result = PyNumber_Lshift(lobj, robj);
    Py_DECREF(lobj);
    Py_DECREF(robj);
    if (result == NULL) {
        // Propagate error (could be negative shift count)
        return CPY_INT_TAG;
    }
    return CPyTagged_StealFromObject(result);
}

int64_t CPyLong_AsInt64(PyObject *o) {
    if (likely(PyLong_Check(o))) {
        PyLongObject *lobj = (PyLongObject *)o;
        Py_ssize_t size = Py_SIZE(lobj);
        if (likely(size == 1)) {
            // Fast path
            return lobj->ob_digit[0];
        } else if (likely(size == 0)) {
            return 0;
        }
    }
    // Slow path
    int overflow;
    int64_t result = PyLong_AsLongLongAndOverflow(o, &overflow);
    if (result == -1) {
        if (PyErr_Occurred()) {
            return CPY_LL_INT_ERROR;
        } else if (overflow) {
            PyErr_SetString(PyExc_OverflowError, "int too large to convert to i64");
            return CPY_LL_INT_ERROR;
        }
    }
    return result;
}

int64_t CPyInt64_Divide(int64_t x, int64_t y) {
    if (y == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "integer division or modulo by zero");
        return CPY_LL_INT_ERROR;
    }
    if (y == -1 && x == INT64_MIN) {
        PyErr_SetString(PyExc_OverflowError, "integer division overflow");
        return CPY_LL_INT_ERROR;
    }
    int64_t d = x / y;
    // Adjust for Python semantics
    if (((x < 0) != (y < 0)) && d * y != x) {
        d--;
    }
    return d;
}

int64_t CPyInt64_Remainder(int64_t x, int64_t y) {
    if (y == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "integer division or modulo by zero");
        return CPY_LL_INT_ERROR;
    }
    // Edge case: avoid core dump
    if (y == -1 && x == INT64_MIN) {
        return 0;
    }
    int64_t d = x % y;
    // Adjust for Python semantics
    if (((x < 0) != (y < 0)) && d != 0) {
        d += y;
    }
    return d;
}

int32_t CPyLong_AsInt32(PyObject *o) {
    if (likely(PyLong_Check(o))) {
        PyLongObject *lobj = (PyLongObject *)o;
        Py_ssize_t size = lobj->ob_base.ob_size;
        if (likely(size == 1)) {
            // Fast path
            return lobj->ob_digit[0];
        } else if (likely(size == 0)) {
            return 0;
        }
    }
    // Slow path
    int overflow;
    long result = PyLong_AsLongAndOverflow(o, &overflow);
    if (result > 0x7fffffffLL || result < -0x80000000LL) {
        overflow = 1;
        result = -1;
    }
    if (result == -1) {
        if (PyErr_Occurred()) {
            return CPY_LL_INT_ERROR;
        } else if (overflow) {
            PyErr_SetString(PyExc_OverflowError, "int too large to convert to i32");
            return CPY_LL_INT_ERROR;
        }
    }
    return result;
}

int32_t CPyInt32_Divide(int32_t x, int32_t y) {
    if (y == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "integer division or modulo by zero");
        return CPY_LL_INT_ERROR;
    }
    if (y == -1 && x == INT32_MIN) {
        PyErr_SetString(PyExc_OverflowError, "integer division overflow");
        return CPY_LL_INT_ERROR;
    }
    int32_t d = x / y;
    // Adjust for Python semantics
    if (((x < 0) != (y < 0)) && d * y != x) {
        d--;
    }
    return d;
}

int32_t CPyInt32_Remainder(int32_t x, int32_t y) {
    if (y == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "integer division or modulo by zero");
        return CPY_LL_INT_ERROR;
    }
    // Edge case: avoid core dump
    if (y == -1 && x == INT32_MIN) {
        return 0;
    }
    int32_t d = x % y;
    // Adjust for Python semantics
    if (((x < 0) != (y < 0)) && d != 0) {
        d += y;
    }
    return d;
}

void CPyInt32_Overflow() {
    PyErr_SetString(PyExc_OverflowError, "int too large to convert to i32");
}

double CPyTagged_TrueDivide(CPyTagged x, CPyTagged y) {
    if (unlikely(y == 0)) {
        PyErr_SetString(PyExc_ZeroDivisionError, "division by zero");
        return CPY_FLOAT_ERROR;
    }
    if (likely(!CPyTagged_CheckLong(x) && !CPyTagged_CheckLong(y))) {
        return (double)((Py_ssize_t)x >> 1) / (double)((Py_ssize_t)y >> 1);
    } else {
        PyObject *xo = CPyTagged_AsObject(x);
        PyObject *yo = CPyTagged_AsObject(y);
        PyObject *result = PyNumber_TrueDivide(xo, yo);
        if (result == NULL) {
            return CPY_FLOAT_ERROR;
        }
        return PyFloat_AsDouble(result);
    }
    return 1.0;
}
