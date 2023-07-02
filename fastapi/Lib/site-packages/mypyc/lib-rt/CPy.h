// Mypyc C API

#ifndef CPY_CPY_H
#define CPY_CPY_H

#include <stdbool.h>
#include <Python.h>
#include <frameobject.h>
#include <structmember.h>
#include <assert.h>
#include <stdint.h>
#include "pythonsupport.h"
#include "mypyc_util.h"

#ifdef __cplusplus
extern "C" {
#endif
#if 0
} // why isn't emacs smart enough to not indent this
#endif

#define CPYTHON_LARGE_INT_ERRMSG "Python int too large to convert to C ssize_t"


// Naming conventions:
//
// Tagged: tagged int
// Long: tagged long int (pointer)
// Short: tagged short int (unboxed)
// Ssize_t: A Py_ssize_t, which ought to be the same width as pointers
// Object: CPython object (PyObject *)


// Tuple type definitions needed for API functions


#ifndef MYPYC_DECLARED_tuple_T3OOO
#define MYPYC_DECLARED_tuple_T3OOO
typedef struct tuple_T3OOO {
    PyObject *f0;
    PyObject *f1;
    PyObject *f2;
} tuple_T3OOO;
static tuple_T3OOO tuple_undefined_T3OOO = { NULL, NULL, NULL };
#endif

// Our return tuple wrapper for dictionary iteration helper.
#ifndef MYPYC_DECLARED_tuple_T3CIO
#define MYPYC_DECLARED_tuple_T3CIO
typedef struct tuple_T3CIO {
    char f0;  // Should continue?
    CPyTagged f1;  // Last dict offset
    PyObject *f2;  // Next dictionary key or value
} tuple_T3CIO;
static tuple_T3CIO tuple_undefined_T3CIO = { 2, CPY_INT_TAG, NULL };
#endif

// Same as above but for both key and value.
#ifndef MYPYC_DECLARED_tuple_T4CIOO
#define MYPYC_DECLARED_tuple_T4CIOO
typedef struct tuple_T4CIOO {
    char f0;  // Should continue?
    CPyTagged f1;  // Last dict offset
    PyObject *f2;  // Next dictionary key
    PyObject *f3;  // Next dictionary value
} tuple_T4CIOO;
static tuple_T4CIOO tuple_undefined_T4CIOO = { 2, CPY_INT_TAG, NULL, NULL };
#endif


// Native object operations


// Search backwards through the trait part of a vtable (which sits *before*
// the start of the vtable proper) looking for the subvtable describing a trait
// implementation. We don't do any bounds checking so we'd better be pretty sure
// we know that it is there.
static inline CPyVTableItem *CPy_FindTraitVtable(PyTypeObject *trait, CPyVTableItem *vtable) {
    int i;
    for (i = -3; ; i -= 3) {
        if ((PyTypeObject *)vtable[i] == trait) {
            return (CPyVTableItem *)vtable[i + 1];
        }
    }
}

// Use the same logic for offset table.
static inline size_t CPy_FindAttrOffset(PyTypeObject *trait, CPyVTableItem *vtable, size_t index) {
    int i;
    for (i = -3; ; i -= 3) {
        if ((PyTypeObject *)vtable[i] == trait) {
            return ((size_t *)vtable[i + 2])[index];
        }
    }
}

// Get attribute value using vtable (may return an undefined value)
#define CPY_GET_ATTR(obj, type, vtable_index, object_type, attr_type)    \
    ((attr_type (*)(object_type *))((object_type *)obj)->vtable[vtable_index])((object_type *)obj)

#define CPY_GET_ATTR_TRAIT(obj, trait, vtable_index, object_type, attr_type)   \
    ((attr_type (*)(object_type *))(CPy_FindTraitVtable(trait, ((object_type *)obj)->vtable))[vtable_index])((object_type *)obj)

// Set attribute value using vtable
#define CPY_SET_ATTR(obj, type, vtable_index, value, object_type, attr_type) \
    ((bool (*)(object_type *, attr_type))((object_type *)obj)->vtable[vtable_index])( \
        (object_type *)obj, value)

#define CPY_SET_ATTR_TRAIT(obj, trait, vtable_index, value, object_type, attr_type) \
    ((bool (*)(object_type *, attr_type))(CPy_FindTraitVtable(trait, ((object_type *)obj)->vtable))[vtable_index])( \
        (object_type *)obj, value)

#define CPY_GET_METHOD(obj, type, vtable_index, object_type, method_type) \
    ((method_type)(((object_type *)obj)->vtable[vtable_index]))

#define CPY_GET_METHOD_TRAIT(obj, trait, vtable_index, object_type, method_type) \
    ((method_type)(CPy_FindTraitVtable(trait, ((object_type *)obj)->vtable)[vtable_index]))


// Int operations


CPyTagged CPyTagged_FromSsize_t(Py_ssize_t value);
CPyTagged CPyTagged_FromVoidPtr(void *ptr);
CPyTagged CPyTagged_FromInt64(int64_t value);
CPyTagged CPyTagged_FromObject(PyObject *object);
CPyTagged CPyTagged_StealFromObject(PyObject *object);
CPyTagged CPyTagged_BorrowFromObject(PyObject *object);
PyObject *CPyTagged_AsObject(CPyTagged x);
PyObject *CPyTagged_StealAsObject(CPyTagged x);
Py_ssize_t CPyTagged_AsSsize_t(CPyTagged x);
void CPyTagged_IncRef(CPyTagged x);
void CPyTagged_DecRef(CPyTagged x);
void CPyTagged_XDecRef(CPyTagged x);
CPyTagged CPyTagged_Negate(CPyTagged num);
CPyTagged CPyTagged_Invert(CPyTagged num);
CPyTagged CPyTagged_Add(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_Subtract(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_Multiply(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_FloorDivide(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_Remainder(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_And(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_Or(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_Xor(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_Rshift(CPyTagged left, CPyTagged right);
CPyTagged CPyTagged_Lshift(CPyTagged left, CPyTagged right);
bool CPyTagged_IsEq_(CPyTagged left, CPyTagged right);
bool CPyTagged_IsLt_(CPyTagged left, CPyTagged right);
PyObject *CPyTagged_Str(CPyTagged n);
CPyTagged CPyTagged_FromFloat(double f);
PyObject *CPyLong_FromStrWithBase(PyObject *o, CPyTagged base);
PyObject *CPyLong_FromStr(PyObject *o);
PyObject *CPyBool_Str(bool b);
int64_t CPyLong_AsInt64(PyObject *o);
int64_t CPyInt64_Divide(int64_t x, int64_t y);
int64_t CPyInt64_Remainder(int64_t x, int64_t y);
int32_t CPyLong_AsInt32(PyObject *o);
int32_t CPyInt32_Divide(int32_t x, int32_t y);
int32_t CPyInt32_Remainder(int32_t x, int32_t y);
void CPyInt32_Overflow(void);
double CPyTagged_TrueDivide(CPyTagged x, CPyTagged y);

static inline int CPyTagged_CheckLong(CPyTagged x) {
    return x & CPY_INT_TAG;
}

static inline int CPyTagged_CheckShort(CPyTagged x) {
    return !CPyTagged_CheckLong(x);
}

static inline void CPyTagged_INCREF(CPyTagged x) {
    if (unlikely(CPyTagged_CheckLong(x))) {
        CPyTagged_IncRef(x);
    }
}

static inline void CPyTagged_DECREF(CPyTagged x) {
    if (unlikely(CPyTagged_CheckLong(x))) {
        CPyTagged_DecRef(x);
    }
}

static inline void CPyTagged_XDECREF(CPyTagged x) {
    if (unlikely(CPyTagged_CheckLong(x))) {
        CPyTagged_XDecRef(x);
    }
}

static inline Py_ssize_t CPyTagged_ShortAsSsize_t(CPyTagged x) {
    // NOTE: Assume that we sign extend.
    return (Py_ssize_t)x >> 1;
}

static inline PyObject *CPyTagged_LongAsObject(CPyTagged x) {
    // NOTE: Assume target is not a short int.
    return (PyObject *)(x & ~CPY_INT_TAG);
}

static inline bool CPyTagged_TooBig(Py_ssize_t value) {
    // Micro-optimized for the common case where it fits.
    return (size_t)value > CPY_TAGGED_MAX
        && (value >= 0 || value < CPY_TAGGED_MIN);
}

static inline bool CPyTagged_TooBigInt64(int64_t value) {
    // Micro-optimized for the common case where it fits.
    return (uint64_t)value > CPY_TAGGED_MAX
        && (value >= 0 || value < CPY_TAGGED_MIN);
}

static inline bool CPyTagged_IsAddOverflow(CPyTagged sum, CPyTagged left, CPyTagged right) {
    // This check was copied from some of my old code I believe that it works :-)
    return (Py_ssize_t)(sum ^ left) < 0 && (Py_ssize_t)(sum ^ right) < 0;
}

static inline bool CPyTagged_IsSubtractOverflow(CPyTagged diff, CPyTagged left, CPyTagged right) {
    // This check was copied from some of my old code I believe that it works :-)
    return (Py_ssize_t)(diff ^ left) < 0 && (Py_ssize_t)(diff ^ right) >= 0;
}

static inline bool CPyTagged_IsMultiplyOverflow(CPyTagged left, CPyTagged right) {
    // This is conservative -- return false only in a small number of all non-overflow cases
    return left >= (1U << (CPY_INT_BITS/2 - 1)) || right >= (1U << (CPY_INT_BITS/2 - 1));
}

static inline bool CPyTagged_MaybeFloorDivideFault(CPyTagged left, CPyTagged right) {
    return right == 0 || left == -((size_t)1 << (CPY_INT_BITS-1));
}

static inline bool CPyTagged_MaybeRemainderFault(CPyTagged left, CPyTagged right) {
    // Division/modulus can fault when dividing INT_MIN by -1, but we
    // do our mods on still-tagged integers with the low-bit clear, so
    // -1 is actually represented as -2 and can't overflow.
    // Mod by 0 can still fault though.
    return right == 0;
}

static inline bool CPyTagged_IsEq(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left)) {
        return left == right;
    } else {
        return CPyTagged_IsEq_(left, right);
    }
}

static inline bool CPyTagged_IsNe(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left)) {
        return left != right;
    } else {
        return !CPyTagged_IsEq_(left, right);
    }
}

static inline bool CPyTagged_IsLt(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right)) {
        return (Py_ssize_t)left < (Py_ssize_t)right;
    } else {
        return CPyTagged_IsLt_(left, right);
    }
}

static inline bool CPyTagged_IsGe(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right)) {
        return (Py_ssize_t)left >= (Py_ssize_t)right;
    } else {
        return !CPyTagged_IsLt_(left, right);
    }
}

static inline bool CPyTagged_IsGt(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right)) {
        return (Py_ssize_t)left > (Py_ssize_t)right;
    } else {
        return CPyTagged_IsLt_(right, left);
    }
}

static inline bool CPyTagged_IsLe(CPyTagged left, CPyTagged right) {
    if (CPyTagged_CheckShort(left) && CPyTagged_CheckShort(right)) {
        return (Py_ssize_t)left <= (Py_ssize_t)right;
    } else {
        return !CPyTagged_IsLt_(right, left);
    }
}


// Float operations


double CPyFloat_FloorDivide(double x, double y);
double CPyFloat_Pow(double x, double y);
double CPyFloat_Sin(double x);
double CPyFloat_Cos(double x);
double CPyFloat_Tan(double x);
double CPyFloat_Sqrt(double x);
double CPyFloat_Exp(double x);
double CPyFloat_Log(double x);
CPyTagged CPyFloat_Floor(double x);
CPyTagged CPyFloat_Ceil(double x);
double CPyFloat_FromTagged(CPyTagged x);
bool CPyFloat_IsInf(double x);
bool CPyFloat_IsNaN(double x);


// Generic operations (that work with arbitrary types)


/* We use intentionally non-inlined decrefs in rarely executed code
 * paths since it pretty substantially speeds up compile time. We have
 * our own copies both to avoid the null check in Py_DecRef and to avoid
 * making an indirect PIC call. */
CPy_NOINLINE
static void CPy_DecRef(PyObject *p) {
    CPy_DECREF(p);
}

CPy_NOINLINE
static void CPy_XDecRef(PyObject *p) {
    CPy_XDECREF(p);
}

static inline CPyTagged CPyObject_Size(PyObject *obj) {
    Py_ssize_t s = PyObject_Size(obj);
    if (s < 0) {
        return CPY_INT_TAG;
    } else {
        // Technically __len__ could return a really big number, so we
        // should allow this to produce a boxed int. In practice it
        // shouldn't ever if the data structure actually contains all
        // the elements, but...
        return CPyTagged_FromSsize_t(s);
    }
}

#ifdef MYPYC_LOG_GETATTR
static void CPy_LogGetAttr(const char *method, PyObject *obj, PyObject *attr) {
    PyObject *module = PyImport_ImportModule("getattr_hook");
    if (module) {
        PyObject *res = PyObject_CallMethodObjArgs(module, method, obj, attr, NULL);
        Py_XDECREF(res);
        Py_DECREF(module);
    }
    PyErr_Clear();
}
#else
#define CPy_LogGetAttr(method, obj, attr) (void)0
#endif

// Intercept a method call and log it. This needs to be a macro
// because there is no API that accepts va_args for making a
// call. Worse, it needs to use the comma operator to return the right
// value.
#define CPyObject_CallMethodObjArgs(obj, attr, ...)             \
    (CPy_LogGetAttr("log_method", (obj), (attr)),               \
     PyObject_CallMethodObjArgs((obj), (attr), __VA_ARGS__))

// This one is a macro for consistency with the above, I guess.
#define CPyObject_GetAttr(obj, attr)                       \
    (CPy_LogGetAttr("log", (obj), (attr)),                 \
     PyObject_GetAttr((obj), (attr)))

CPyTagged CPyObject_Hash(PyObject *o);
PyObject *CPyObject_GetAttr3(PyObject *v, PyObject *name, PyObject *defl);
PyObject *CPyIter_Next(PyObject *iter);
PyObject *CPyNumber_Power(PyObject *base, PyObject *index);
PyObject *CPyNumber_InPlacePower(PyObject *base, PyObject *index);
PyObject *CPyObject_GetSlice(PyObject *obj, CPyTagged start, CPyTagged end);


// List operations


PyObject *CPyList_Build(Py_ssize_t len, ...);
PyObject *CPyList_GetItem(PyObject *list, CPyTagged index);
PyObject *CPyList_GetItemUnsafe(PyObject *list, CPyTagged index);
PyObject *CPyList_GetItemShort(PyObject *list, CPyTagged index);
PyObject *CPyList_GetItemBorrow(PyObject *list, CPyTagged index);
PyObject *CPyList_GetItemShortBorrow(PyObject *list, CPyTagged index);
PyObject *CPyList_GetItemInt64(PyObject *list, int64_t index);
PyObject *CPyList_GetItemInt64Borrow(PyObject *list, int64_t index);
bool CPyList_SetItem(PyObject *list, CPyTagged index, PyObject *value);
bool CPyList_SetItemUnsafe(PyObject *list, CPyTagged index, PyObject *value);
bool CPyList_SetItemInt64(PyObject *list, int64_t index, PyObject *value);
PyObject *CPyList_PopLast(PyObject *obj);
PyObject *CPyList_Pop(PyObject *obj, CPyTagged index);
CPyTagged CPyList_Count(PyObject *obj, PyObject *value);
int CPyList_Insert(PyObject *list, CPyTagged index, PyObject *value);
PyObject *CPyList_Extend(PyObject *o1, PyObject *o2);
int CPyList_Remove(PyObject *list, PyObject *obj);
CPyTagged CPyList_Index(PyObject *list, PyObject *obj);
PyObject *CPySequence_Multiply(PyObject *seq, CPyTagged t_size);
PyObject *CPySequence_RMultiply(CPyTagged t_size, PyObject *seq);
PyObject *CPyList_GetSlice(PyObject *obj, CPyTagged start, CPyTagged end);
int CPySequence_Check(PyObject *obj);


// Dict operations


PyObject *CPyDict_GetItem(PyObject *dict, PyObject *key);
int CPyDict_SetItem(PyObject *dict, PyObject *key, PyObject *value);
PyObject *CPyDict_Get(PyObject *dict, PyObject *key, PyObject *fallback);
PyObject *CPyDict_GetWithNone(PyObject *dict, PyObject *key);
PyObject *CPyDict_SetDefault(PyObject *dict, PyObject *key, PyObject *value);
PyObject *CPyDict_SetDefaultWithNone(PyObject *dict, PyObject *key);
PyObject *CPyDict_SetDefaultWithEmptyDatatype(PyObject *dict, PyObject *key, int data_type);
PyObject *CPyDict_Build(Py_ssize_t size, ...);
int CPyDict_Update(PyObject *dict, PyObject *stuff);
int CPyDict_UpdateInDisplay(PyObject *dict, PyObject *stuff);
int CPyDict_UpdateFromAny(PyObject *dict, PyObject *stuff);
PyObject *CPyDict_FromAny(PyObject *obj);
PyObject *CPyDict_KeysView(PyObject *dict);
PyObject *CPyDict_ValuesView(PyObject *dict);
PyObject *CPyDict_ItemsView(PyObject *dict);
PyObject *CPyDict_Keys(PyObject *dict);
PyObject *CPyDict_Values(PyObject *dict);
PyObject *CPyDict_Items(PyObject *dict);
char CPyDict_Clear(PyObject *dict);
PyObject *CPyDict_Copy(PyObject *dict);
PyObject *CPyDict_GetKeysIter(PyObject *dict);
PyObject *CPyDict_GetItemsIter(PyObject *dict);
PyObject *CPyDict_GetValuesIter(PyObject *dict);
tuple_T3CIO CPyDict_NextKey(PyObject *dict_or_iter, CPyTagged offset);
tuple_T3CIO CPyDict_NextValue(PyObject *dict_or_iter, CPyTagged offset);
tuple_T4CIOO CPyDict_NextItem(PyObject *dict_or_iter, CPyTagged offset);
int CPyMapping_Check(PyObject *obj);

// Check that dictionary didn't change size during iteration.
static inline char CPyDict_CheckSize(PyObject *dict, CPyTagged size) {
    if (!PyDict_CheckExact(dict)) {
        // Dict subclasses will be checked by Python runtime.
        return 1;
    }
    Py_ssize_t py_size = CPyTagged_AsSsize_t(size);
    Py_ssize_t dict_size = PyDict_Size(dict);
    if (py_size != dict_size) {
        PyErr_SetString(PyExc_RuntimeError, "dictionary changed size during iteration");
        return 0;
    }
    return 1;
}


// Str operations


PyObject *CPyStr_Build(Py_ssize_t len, ...);
PyObject *CPyStr_GetItem(PyObject *str, CPyTagged index);
PyObject *CPyStr_Split(PyObject *str, PyObject *sep, CPyTagged max_split);
PyObject *CPyStr_Replace(PyObject *str, PyObject *old_substr, PyObject *new_substr, CPyTagged max_replace);
PyObject *CPyStr_Append(PyObject *o1, PyObject *o2);
PyObject *CPyStr_GetSlice(PyObject *obj, CPyTagged start, CPyTagged end);
bool CPyStr_Startswith(PyObject *self, PyObject *subobj);
bool CPyStr_Endswith(PyObject *self, PyObject *subobj);
bool CPyStr_IsTrue(PyObject *obj);
Py_ssize_t CPyStr_Size_size_t(PyObject *str);
PyObject *CPy_Decode(PyObject *obj, PyObject *encoding, PyObject *errors);
PyObject *CPy_Encode(PyObject *obj, PyObject *encoding, PyObject *errors);


// Bytes operations


PyObject *CPyBytes_Build(Py_ssize_t len, ...);
PyObject *CPyBytes_GetSlice(PyObject *obj, CPyTagged start, CPyTagged end);
CPyTagged CPyBytes_GetItem(PyObject *o, CPyTagged index);
PyObject *CPyBytes_Concat(PyObject *a, PyObject *b);
PyObject *CPyBytes_Join(PyObject *sep, PyObject *iter);


int CPyBytes_Compare(PyObject *left, PyObject *right);


// Set operations


bool CPySet_Remove(PyObject *set, PyObject *key);


// Tuple operations


PyObject *CPySequenceTuple_GetItem(PyObject *tuple, CPyTagged index);
PyObject *CPySequenceTuple_GetSlice(PyObject *obj, CPyTagged start, CPyTagged end);
bool CPySequenceTuple_SetItemUnsafe(PyObject *tuple, CPyTagged index, PyObject *value);


// Exception operations


// mypyc is not very good at dealing with refcount management of
// pointers that might be NULL. As a workaround for this, the
// exception APIs that might want to return NULL pointers instead
// return properly refcounted pointers to this dummy object.
struct ExcDummyStruct { PyObject_HEAD };
extern struct ExcDummyStruct _CPy_ExcDummyStruct;
extern PyObject *_CPy_ExcDummy;

static inline void _CPy_ToDummy(PyObject **p) {
    if (*p == NULL) {
        Py_INCREF(_CPy_ExcDummy);
        *p = _CPy_ExcDummy;
    }
}

static inline PyObject *_CPy_FromDummy(PyObject *p) {
    if (p == _CPy_ExcDummy) return NULL;
    Py_INCREF(p);
    return p;
}

static int CPy_NoErrOccured(void) {
    return PyErr_Occurred() == NULL;
}

static inline bool CPy_KeepPropagating(void) {
    return 0;
}
// We want to avoid the public PyErr_GetExcInfo API for these because
// it requires a bunch of spurious refcount traffic on the parts of
// the triple we don't care about.
#define CPy_ExcState() PyThreadState_GET()->exc_info

void CPy_Raise(PyObject *exc);
void CPy_Reraise(void);
void CPyErr_SetObjectAndTraceback(PyObject *type, PyObject *value, PyObject *traceback);
tuple_T3OOO CPy_CatchError(void);
void CPy_RestoreExcInfo(tuple_T3OOO info);
bool CPy_ExceptionMatches(PyObject *type);
PyObject *CPy_GetExcValue(void);
tuple_T3OOO CPy_GetExcInfo(void);
void _CPy_GetExcInfo(PyObject **p_type, PyObject **p_value, PyObject **p_traceback);
void CPyError_OutOfMemory(void);
void CPy_TypeError(const char *expected, PyObject *value);
void CPy_AddTraceback(const char *filename, const char *funcname, int line, PyObject *globals);
void CPy_TypeErrorTraceback(const char *filename, const char *funcname, int line,
                            PyObject *globals, const char *expected, PyObject *value);
void CPy_AttributeError(const char *filename, const char *funcname, const char *classname,
                        const char *attrname, int line, PyObject *globals);


// Misc operations

#if PY_VERSION_HEX >= 0x03080000
#define CPy_TRASHCAN_BEGIN(op, dealloc) Py_TRASHCAN_BEGIN(op, dealloc)
#define CPy_TRASHCAN_END(op) Py_TRASHCAN_END
#else
#define CPy_TRASHCAN_BEGIN(op, dealloc) Py_TRASHCAN_SAFE_BEGIN(op)
#define CPy_TRASHCAN_END(op) Py_TRASHCAN_SAFE_END(op)
#endif

// Tweaked version of _PyArg_Parser in CPython
typedef struct CPyArg_Parser {
    const char *format;
    const char * const *keywords;
    const char *fname;
    const char *custom_msg;
    int pos;               /* number of positional-only arguments */
    int min;               /* minimal number of arguments */
    int max;               /* maximal number of positional arguments */
    int has_required_kws;  /* are there any keyword-only arguments? */
    int required_kwonly_start;
    int varargs;           /* does the function accept *args or **kwargs? */
    PyObject *kwtuple;     /* tuple of keyword parameter names */
    struct CPyArg_Parser *next;
} CPyArg_Parser;

// mypy lets ints silently coerce to floats, so a mypyc runtime float
// might be an int also
static inline bool CPyFloat_Check(PyObject *o) {
    return PyFloat_Check(o) || PyLong_Check(o);
}

// TODO: find an unified way to avoid inline functions in non-C back ends that can not
//       use inline functions
static inline bool CPy_TypeCheck(PyObject *o, PyObject *type) {
    return PyObject_TypeCheck(o, (PyTypeObject *)type);
}

static inline PyObject *CPy_CalculateMetaclass(PyObject *type, PyObject *o) {
    return (PyObject *)_PyType_CalculateMetaclass((PyTypeObject *)type, o);
}

PyObject *CPy_GetCoro(PyObject *obj);
PyObject *CPyIter_Send(PyObject *iter, PyObject *val);
int CPy_YieldFromErrorHandle(PyObject *iter, PyObject **outp);
PyObject *CPy_FetchStopIterationValue(void);
PyObject *CPyType_FromTemplate(PyObject *template_,
                               PyObject *orig_bases,
                               PyObject *modname);
PyObject *CPyType_FromTemplateWarpper(PyObject *template_,
                                      PyObject *orig_bases,
                                      PyObject *modname);
int CPyDataclass_SleightOfHand(PyObject *dataclass_dec, PyObject *tp,
                               PyObject *dict, PyObject *annotations);
PyObject *CPyPickle_SetState(PyObject *obj, PyObject *state);
PyObject *CPyPickle_GetState(PyObject *obj);
CPyTagged CPyTagged_Id(PyObject *o);
void CPyDebug_Print(const char *msg);
void CPy_Init(void);
int CPyArg_ParseTupleAndKeywords(PyObject *, PyObject *,
                                 const char *, const char *, const char * const *, ...);
int CPyArg_ParseStackAndKeywords(PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames,
                                 CPyArg_Parser *parser, ...);
int CPyArg_ParseStackAndKeywordsNoArgs(PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames,
                                       CPyArg_Parser *parser, ...);
int CPyArg_ParseStackAndKeywordsOneArg(PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames,
                                       CPyArg_Parser *parser, ...);
int CPyArg_ParseStackAndKeywordsSimple(PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames,
                                       CPyArg_Parser *parser, ...);

int CPySequence_CheckUnpackCount(PyObject *sequence, Py_ssize_t expected);
int CPyStatics_Initialize(PyObject **statics,
                          const char * const *strings,
                          const char * const *bytestrings,
                          const char * const *ints,
                          const double *floats,
                          const double *complex_numbers,
                          const int *tuples,
                          const int *frozensets);
PyObject *CPy_Super(PyObject *builtins, PyObject *self);
PyObject *CPy_CallReverseOpMethod(PyObject *left, PyObject *right, const char *op,
                                  _Py_Identifier *method);

bool CPyImport_ImportMany(PyObject *modules, CPyModule **statics[], PyObject *globals,
                          PyObject *tb_path, PyObject *tb_function, Py_ssize_t *tb_lines);
PyObject *CPyImport_ImportFromMany(PyObject *mod_id, PyObject *names, PyObject *as_names,
                                   PyObject *globals);

PyObject *CPySingledispatch_RegisterFunction(PyObject *singledispatch_func, PyObject *cls,
                                             PyObject *func);

PyObject *CPy_GetAIter(PyObject *obj);
PyObject *CPy_GetANext(PyObject *aiter);

#ifdef __cplusplus
}
#endif

#endif // CPY_CPY_H
