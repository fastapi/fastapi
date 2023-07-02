// Misc primitive operations + C helpers
//
// These are registered in mypyc.primitives.misc_ops.

#include <Python.h>
#include <patchlevel.h>
#include "CPy.h"

PyObject *CPy_GetCoro(PyObject *obj)
{
    // If the type has an __await__ method, call it,
    // otherwise, fallback to calling __iter__.
    PyAsyncMethods* async_struct = Py_TYPE(obj)->tp_as_async;
    if (async_struct != NULL && async_struct->am_await != NULL) {
        return (async_struct->am_await)(obj);
    } else {
        // TODO: We should check that the type is a generator decorated with
        // asyncio.coroutine
        return PyObject_GetIter(obj);
    }
}

PyObject *CPyIter_Send(PyObject *iter, PyObject *val)
{
    // Do a send, or a next if second arg is None.
    // (This behavior is to match the PEP 380 spec for yield from.)
    _Py_IDENTIFIER(send);
    if (Py_IsNone(val)) {
        return CPyIter_Next(iter);
    } else {
        return _PyObject_CallMethodIdOneArg(iter, &PyId_send, val);
    }
}

// A somewhat hairy implementation of specifically most of the error handling
// in `yield from` error handling. The point here is to reduce code size.
//
// This implements most of the bodies of the `except` blocks in the
// pseudocode in PEP 380.
//
// Returns true (1) if a StopIteration was received and we should return.
// Returns false (0) if a value should be yielded.
// In both cases the value is stored in outp.
// Signals an error (2) if the an exception should be propagated.
int CPy_YieldFromErrorHandle(PyObject *iter, PyObject **outp)
{
    _Py_IDENTIFIER(close);
    _Py_IDENTIFIER(throw);
    PyObject *exc_type = (PyObject *)Py_TYPE(CPy_ExcState()->exc_value);
    PyObject *type, *value, *traceback;
    PyObject *_m;
    PyObject *res;
    *outp = NULL;

    if (PyErr_GivenExceptionMatches(exc_type, PyExc_GeneratorExit)) {
        _m = _PyObject_GetAttrId(iter, &PyId_close);
        if (_m) {
            res = PyObject_CallNoArgs(_m);
            Py_DECREF(_m);
            if (!res)
                return 2;
            Py_DECREF(res);
        } else if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
            PyErr_Clear();
        } else {
            return 2;
        }
    } else {
        _m = _PyObject_GetAttrId(iter, &PyId_throw);
        if (_m) {
            _CPy_GetExcInfo(&type, &value, &traceback);
            res = PyObject_CallFunctionObjArgs(_m, type, value, traceback, NULL);
            Py_DECREF(type);
            Py_DECREF(value);
            Py_DECREF(traceback);
            Py_DECREF(_m);
            if (res) {
                *outp = res;
                return 0;
            } else {
                res = CPy_FetchStopIterationValue();
                if (res) {
                    *outp = res;
                    return 1;
                }
            }
        } else if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
            PyErr_Clear();
        } else {
            return 2;
        }
    }

    CPy_Reraise();
    return 2;
}

PyObject *CPy_FetchStopIterationValue(void)
{
    PyObject *val = NULL;
    _PyGen_FetchStopIterationValue(&val);
    return val;
}

static bool _CPy_IsSafeMetaClass(PyTypeObject *metaclass) {
    // mypyc classes can't work with metaclasses in
    // general. Through some various nasty hacks we *do*
    // manage to work with TypingMeta and its friends.
    if (metaclass == &PyType_Type)
        return true;
    PyObject *module = PyObject_GetAttrString((PyObject *)metaclass, "__module__");
    if (!module) {
        PyErr_Clear();
        return false;
    }

    bool matches = false;
    if (PyUnicode_CompareWithASCIIString(module, "typing") == 0 &&
            (strcmp(metaclass->tp_name, "TypingMeta") == 0
             || strcmp(metaclass->tp_name, "GenericMeta") == 0
             || strcmp(metaclass->tp_name, "_ProtocolMeta") == 0)) {
        matches = true;
    } else if (PyUnicode_CompareWithASCIIString(module, "typing_extensions") == 0 &&
               strcmp(metaclass->tp_name, "_ProtocolMeta") == 0) {
        matches = true;
    } else if (PyUnicode_CompareWithASCIIString(module, "abc") == 0 &&
               strcmp(metaclass->tp_name, "ABCMeta") == 0) {
        matches = true;
    }
    Py_DECREF(module);
    return matches;
}

// Create a heap type based on a template non-heap type.
// This is super hacky and maybe we should suck it up and use PyType_FromSpec instead.
// We allow bases to be NULL to represent just inheriting from object.
// We don't support NULL bases and a non-type metaclass.
PyObject *CPyType_FromTemplate(PyObject *template,
                               PyObject *orig_bases,
                               PyObject *modname) {
    PyTypeObject *template_ = (PyTypeObject *)template;
    PyHeapTypeObject *t = NULL;
    PyTypeObject *dummy_class = NULL;
    PyObject *name = NULL;
    PyObject *bases = NULL;
    PyObject *slots;

    // If the type of the class (the metaclass) is NULL, we default it
    // to being type.  (This allows us to avoid needing to initialize
    // it explicitly on windows.)
    if (!Py_TYPE(template_)) {
        Py_SET_TYPE(template_, &PyType_Type);
    }
    PyTypeObject *metaclass = Py_TYPE(template_);

    if (orig_bases) {
        bases = update_bases(orig_bases);
        // update_bases doesn't increment the refcount if nothing changes,
        // so we do it to make sure we have distinct "references" to both
        if (bases == orig_bases)
            Py_INCREF(bases);

        // Find the appropriate metaclass from our base classes. We
        // care about this because Generic uses a metaclass prior to
        // Python 3.7.
        metaclass = _PyType_CalculateMetaclass(metaclass, bases);
        if (!metaclass)
            goto error;

        if (!_CPy_IsSafeMetaClass(metaclass)) {
            PyErr_SetString(PyExc_TypeError, "mypyc classes can't have a metaclass");
            goto error;
        }
    }

    name = PyUnicode_FromString(template_->tp_name);
    if (!name)
        goto error;

    // If there is a metaclass other than type, we would like to call
    // its __new__ function. Unfortunately there doesn't seem to be a
    // good way to mix a C extension class and creating it via a
    // metaclass. We need to do it anyways, though, in order to
    // support subclassing Generic[T] prior to Python 3.7.
    //
    // We solve this with a kind of atrocious hack: create a parallel
    // class using the metaclass, determine the bases of the real
    // class by pulling them out of the parallel class, creating the
    // real class, and then merging its dict back into the original
    // class. There are lots of cases where this won't really work,
    // but for the case of GenericMeta setting a bunch of properties
    // on the class we should be fine.
    if (metaclass != &PyType_Type) {
        assert(bases && "non-type metaclasses require non-NULL bases");

        PyObject *ns = PyDict_New();
        if (!ns)
            goto error;

        if (bases != orig_bases) {
            if (PyDict_SetItemString(ns, "__orig_bases__", orig_bases) < 0)
                goto error;
        }

        dummy_class = (PyTypeObject *)PyObject_CallFunctionObjArgs(
            (PyObject *)metaclass, name, bases, ns, NULL);
        Py_DECREF(ns);
        if (!dummy_class)
            goto error;

        Py_DECREF(bases);
        bases = dummy_class->tp_bases;
        Py_INCREF(bases);
    }

    // Allocate the type and then copy the main stuff in.
    t = (PyHeapTypeObject*)PyType_GenericAlloc(&PyType_Type, 0);
    if (!t)
        goto error;
    memcpy((char *)t + sizeof(PyVarObject),
           (char *)template_ + sizeof(PyVarObject),
           sizeof(PyTypeObject) - sizeof(PyVarObject));

    if (bases != orig_bases) {
        if (PyObject_SetAttrString((PyObject *)t, "__orig_bases__", orig_bases) < 0)
            goto error;
    }

    // Having tp_base set is I think required for stuff to get
    // inherited in PyType_Ready, which we needed for subclassing
    // BaseException. XXX: Taking the first element is wrong I think though.
    if (bases) {
        t->ht_type.tp_base = (PyTypeObject *)PyTuple_GET_ITEM(bases, 0);
        Py_INCREF((PyObject *)t->ht_type.tp_base);
    }

    t->ht_name = name;
    Py_INCREF(name);
    t->ht_qualname = name;
    t->ht_type.tp_bases = bases;
    // references stolen so NULL these out
    bases = name = NULL;

    if (PyType_Ready((PyTypeObject *)t) < 0)
        goto error;

    assert(t->ht_type.tp_base != NULL);

    // XXX: This is a terrible hack to work around a cpython check on
    // the mro. It was needed for mypy.stats. I need to investigate
    // what is actually going on here.
    Py_INCREF(metaclass);
    Py_SET_TYPE(t, metaclass);

    if (dummy_class) {
        if (PyDict_Merge(t->ht_type.tp_dict, dummy_class->tp_dict, 0) != 0)
            goto error;
        // This is the *really* tasteless bit. GenericMeta's __new__
        // in certain versions of typing sets _gorg to point back to
        // the class. We need to override it to keep it from pointing
        // to the proxy.
        if (PyDict_SetItemString(t->ht_type.tp_dict, "_gorg", (PyObject *)t) < 0)
            goto error;
    }

    // Reject anything that would give us a nontrivial __slots__,
    // because the layout will conflict
    slots = PyObject_GetAttrString((PyObject *)t, "__slots__");
    if (slots) {
        // don't fail on an empty __slots__
        int is_true = PyObject_IsTrue(slots);
        Py_DECREF(slots);
        if (is_true > 0)
            PyErr_SetString(PyExc_TypeError, "mypyc classes can't have __slots__");
        if (is_true != 0)
            goto error;
    } else {
        PyErr_Clear();
    }

    if (PyObject_SetAttrString((PyObject *)t, "__module__", modname) < 0)
        goto error;

    if (init_subclass((PyTypeObject *)t, NULL))
        goto error;

    Py_XDECREF(dummy_class);

#if PY_MINOR_VERSION == 11
    // This is a hack. Python 3.11 doesn't include good public APIs to work with managed
    // dicts, which are the default for heap types. So we try to opt-out until Python 3.12.
    t->ht_type.tp_flags &= ~Py_TPFLAGS_MANAGED_DICT;
#endif
    return (PyObject *)t;

error:
    Py_XDECREF(t);
    Py_XDECREF(bases);
    Py_XDECREF(dummy_class);
    Py_XDECREF(name);
    return NULL;
}

static int _CPy_UpdateObjFromDict(PyObject *obj, PyObject *dict)
{
    Py_ssize_t pos = 0;
    PyObject *key, *value;
    while (PyDict_Next(dict, &pos, &key, &value)) {
        if (PyObject_SetAttr(obj, key, value) != 0) {
            return -1;
        }
    }
    return 0;
}

/* Support for our partial built-in support for dataclasses.
 *
 * Take a class we want to make a dataclass, remove any descriptors
 * for annotated attributes, swap in the actual values of the class
 * variables invoke dataclass, and then restore all of the
 * descriptors.
 *
 * The purpose of all this is that dataclasses uses the values of
 * class variables to drive which attributes are required and what the
 * default values/factories are for optional attributes. This means
 * that the class dict needs to contain those values instead of getset
 * descriptors for the attributes when we invoke dataclass.
 *
 * We need to remove descriptors for attributes even when there is no
 * default value for them, or else dataclass will think the descriptor
 * is the default value. We remove only the attributes, since we don't
 * want dataclasses to try generating functions when they are already
 * implemented.
 *
 * Args:
 *   dataclass_dec: The decorator to apply
 *   tp: The class we are making a dataclass
 *   dict: The dictionary containing values that dataclasses needs
 *   annotations: The type annotation dictionary
 */
int
CPyDataclass_SleightOfHand(PyObject *dataclass_dec, PyObject *tp,
                           PyObject *dict, PyObject *annotations) {
    PyTypeObject *ttp = (PyTypeObject *)tp;
    Py_ssize_t pos;
    PyObject *res;

    /* Make a copy of the original class __dict__ */
    PyObject *orig_dict = PyDict_Copy(ttp->tp_dict);
    if (!orig_dict) {
        goto fail;
    }

    /* Delete anything that had an annotation */
    pos = 0;
    PyObject *key;
    while (PyDict_Next(annotations, &pos, &key, NULL)) {
        if (PyObject_DelAttr(tp, key) != 0) {
            goto fail;
        }
    }

    /* Copy in all the attributes that we want dataclass to see */
    if (_CPy_UpdateObjFromDict(tp, dict) != 0) {
        goto fail;
    }

    /* Run the @dataclass descriptor */
    res = PyObject_CallOneArg(dataclass_dec, tp);
    if (!res) {
        goto fail;
    }
    Py_DECREF(res);

    /* Copy back the original contents of the dict */
    if (_CPy_UpdateObjFromDict(tp, orig_dict) != 0) {
        goto fail;
    }

    Py_DECREF(orig_dict);
    return 1;

fail:
    Py_XDECREF(orig_dict);
    return 0;
}

// Support for pickling; reusable getstate and setstate functions
PyObject *
CPyPickle_SetState(PyObject *obj, PyObject *state)
{
    if (_CPy_UpdateObjFromDict(obj, state) != 0) {
        return NULL;
    }
    Py_RETURN_NONE;
}

PyObject *
CPyPickle_GetState(PyObject *obj)
{
    PyObject *attrs = NULL, *state = NULL;

    attrs = PyObject_GetAttrString((PyObject *)Py_TYPE(obj), "__mypyc_attrs__");
    if (!attrs) {
        goto fail;
    }
    if (!PyTuple_Check(attrs)) {
        PyErr_SetString(PyExc_TypeError, "__mypyc_attrs__ is not a tuple");
        goto fail;
    }
    state = PyDict_New();
    if (!state) {
        goto fail;
    }

    // Collect all the values of attributes in __mypyc_attrs__
    // Attributes that are missing we just ignore
    int i;
    for (i = 0; i < PyTuple_GET_SIZE(attrs); i++) {
        PyObject *key = PyTuple_GET_ITEM(attrs, i);
        PyObject *value = PyObject_GetAttr(obj, key);
        if (!value) {
            if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
                PyErr_Clear();
                continue;
            }
            goto fail;
        }
        int result = PyDict_SetItem(state, key, value);
        Py_DECREF(value);
        if (result != 0) {
            goto fail;
        }
    }

    Py_DECREF(attrs);

    return state;
fail:
    Py_XDECREF(attrs);
    Py_XDECREF(state);
    return NULL;
}

CPyTagged CPyTagged_Id(PyObject *o) {
    return CPyTagged_FromVoidPtr(o);
}

#define MAX_INT_CHARS 22
#define _PyUnicode_LENGTH(op)                           \
    (((PyASCIIObject *)(op))->length)

// using snprintf or PyUnicode_FromFormat was way slower than
// boxing the int and calling PyObject_Str on it, so we implement our own
static int fmt_ssize_t(char *out, Py_ssize_t n) {
	bool neg = n < 0;
	if (neg) n = -n;

	// buf gets filled backward and then we copy it forward
	char buf[MAX_INT_CHARS];
	int i = 0;
	do {
		buf[i] = (n % 10) + '0';
		n /= 10;
		i++;
	} while (n);


	int len = i;
	int j = 0;
	if (neg) {
		out[j++] = '-';
		len++;
	}

	for (; j < len; j++, i--) {
		out[j] = buf[i-1];
	}
	out[j] = '\0';

	return len;
}

static PyObject *CPyTagged_ShortToStr(Py_ssize_t n) {
    PyObject *obj = PyUnicode_New(MAX_INT_CHARS, 127);
    if (!obj) return NULL;
    int len = fmt_ssize_t((char *)PyUnicode_1BYTE_DATA(obj), n);
    _PyUnicode_LENGTH(obj) = len;
    return obj;
}

PyObject *CPyTagged_Str(CPyTagged n) {
    if (CPyTagged_CheckShort(n)) {
        return CPyTagged_ShortToStr(CPyTagged_ShortAsSsize_t(n));
    } else {
        return PyObject_Str(CPyTagged_AsObject(n));
    }
}

void CPyDebug_Print(const char *msg) {
    printf("%s\n", msg);
    fflush(stdout);
}

int CPySequence_CheckUnpackCount(PyObject *sequence, Py_ssize_t expected) {
    Py_ssize_t actual = Py_SIZE(sequence);
    if (unlikely(actual != expected)) {
        if (actual < expected) {
            PyErr_Format(PyExc_ValueError, "not enough values to unpack (expected %zd, got %zd)",
                         expected, actual);
        } else {
            PyErr_Format(PyExc_ValueError, "too many values to unpack (expected %zd)", expected);
        }
        return -1;
    }
    return 0;
}

// Parse an integer (size_t) encoded as a variable-length binary sequence.
static const char *parse_int(const char *s, size_t *len) {
    Py_ssize_t n = 0;
    while ((unsigned char)*s >= 0x80) {
        n = (n << 7) + (*s & 0x7f);
        s++;
    }
    n = (n << 7) | *s++;
    *len = n;
    return s;
}

// Initialize static constant array of literal values
int CPyStatics_Initialize(PyObject **statics,
                          const char * const *strings,
                          const char * const *bytestrings,
                          const char * const *ints,
                          const double *floats,
                          const double *complex_numbers,
                          const int *tuples,
                          const int *frozensets) {
    PyObject **result = statics;
    // Start with some hard-coded values
    *result++ = Py_None;
    Py_INCREF(Py_None);
    *result++ = Py_False;
    Py_INCREF(Py_False);
    *result++ = Py_True;
    Py_INCREF(Py_True);
    if (strings) {
        for (; **strings != '\0'; strings++) {
            size_t num;
            const char *data = *strings;
            data = parse_int(data, &num);
            while (num-- > 0) {
                size_t len;
                data = parse_int(data, &len);
                PyObject *obj = PyUnicode_FromStringAndSize(data, len);
                if (obj == NULL) {
                    return -1;
                }
                PyUnicode_InternInPlace(&obj);
                *result++ = obj;
                data += len;
            }
        }
    }
    if (bytestrings) {
        for (; **bytestrings != '\0'; bytestrings++) {
            size_t num;
            const char *data = *bytestrings;
            data = parse_int(data, &num);
            while (num-- > 0) {
                size_t len;
                data = parse_int(data, &len);
                PyObject *obj = PyBytes_FromStringAndSize(data, len);
                if (obj == NULL) {
                    return -1;
                }
                *result++ = obj;
                data += len;
            }
        }
    }
    if (ints) {
        for (; **ints != '\0'; ints++) {
            size_t num;
            const char *data = *ints;
            data = parse_int(data, &num);
            while (num-- > 0) {
                char *end;
                PyObject *obj = PyLong_FromString(data, &end, 10);
                if (obj == NULL) {
                    return -1;
                }
                data = end;
                data++;
                *result++ = obj;
            }
        }
    }
    if (floats) {
        size_t num = (size_t)*floats++;
        while (num-- > 0) {
            PyObject *obj = PyFloat_FromDouble(*floats++);
            if (obj == NULL) {
                return -1;
            }
            *result++ = obj;
        }
    }
    if (complex_numbers) {
        size_t num = (size_t)*complex_numbers++;
        while (num-- > 0) {
            double real = *complex_numbers++;
            double imag = *complex_numbers++;
            PyObject *obj = PyComplex_FromDoubles(real, imag);
            if (obj == NULL) {
                return -1;
            }
            *result++ = obj;
        }
    }
    if (tuples) {
        int num = *tuples++;
        while (num-- > 0) {
            int num_items = *tuples++;
            PyObject *obj = PyTuple_New(num_items);
            if (obj == NULL) {
                return -1;
            }
            int i;
            for (i = 0; i < num_items; i++) {
                PyObject *item = statics[*tuples++];
                Py_INCREF(item);
                PyTuple_SET_ITEM(obj, i, item);
            }
            *result++ = obj;
        }
    }
    if (frozensets) {
        int num = *frozensets++;
        while (num-- > 0) {
            int num_items = *frozensets++;
            PyObject *obj = PyFrozenSet_New(NULL);
            if (obj == NULL) {
                return -1;
            }
            for (int i = 0; i < num_items; i++) {
                PyObject *item = statics[*frozensets++];
                Py_INCREF(item);
                if (PySet_Add(obj, item) == -1) {
                    return -1;
                }
            }
            *result++ = obj;
        }
    }
    return 0;
}

// Call super(type(self), self)
PyObject *
CPy_Super(PyObject *builtins, PyObject *self) {
    PyObject *super_type = PyObject_GetAttrString(builtins, "super");
    if (!super_type)
        return NULL;
    PyObject *result = PyObject_CallFunctionObjArgs(
        super_type, (PyObject*)Py_TYPE(self), self, NULL);
    Py_DECREF(super_type);
    return result;
}

static bool import_single(PyObject *mod_id, PyObject **mod_static,
                          PyObject *globals_id, PyObject *globals_name, PyObject *globals) {
    if (*mod_static == Py_None) {
        CPyModule *mod = PyImport_Import(mod_id);
        if (mod == NULL) {
            return false;
        }
        *mod_static = mod;
    }

    PyObject *mod_dict = PyImport_GetModuleDict();
    CPyModule *globals_mod = CPyDict_GetItem(mod_dict, globals_id);
    if (globals_mod == NULL) {
        return false;
    }
    int ret = CPyDict_SetItem(globals, globals_name, globals_mod);
    Py_DECREF(globals_mod);
    if (ret < 0) {
        return false;
    }

    return true;
}

// Table-driven import helper. See transform_import() in irbuild for the details.
bool CPyImport_ImportMany(PyObject *modules, CPyModule **statics[], PyObject *globals,
                          PyObject *tb_path, PyObject *tb_function, Py_ssize_t *tb_lines) {
    for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(modules); i++) {
        PyObject *module = PyTuple_GET_ITEM(modules, i);
        PyObject *mod_id = PyTuple_GET_ITEM(module, 0);
        PyObject *globals_id = PyTuple_GET_ITEM(module, 1);
        PyObject *globals_name = PyTuple_GET_ITEM(module, 2);

        if (!import_single(mod_id, statics[i], globals_id, globals_name, globals)) {
            assert(PyErr_Occurred() && "error indicator should be set on bad import!");
            PyObject *typ, *val, *tb;
            PyErr_Fetch(&typ, &val, &tb);
            const char *path = PyUnicode_AsUTF8(tb_path);
            if (path == NULL) {
                path = "<unable to display>";
            }
            const char *function = PyUnicode_AsUTF8(tb_function);
            if (function == NULL) {
                function = "<unable to display>";
            }
            PyErr_Restore(typ, val, tb);
            CPy_AddTraceback(path, function, tb_lines[i], globals);
            return false;
        }
    }
    return true;
}

// This helper function is a simplification of cpython/ceval.c/import_from()
static PyObject *CPyImport_ImportFrom(PyObject *module, PyObject *package_name,
                                      PyObject *import_name, PyObject *as_name) {
    // check if the imported module has an attribute by that name
    PyObject *x = PyObject_GetAttr(module, import_name);
    if (x == NULL) {
        // if not, attempt to import a submodule with that name
        PyObject *fullmodname = PyUnicode_FromFormat("%U.%U", package_name, import_name);
        if (fullmodname == NULL) {
            goto fail;
        }

        // The following code is a simplification of cpython/import.c/PyImport_GetModule()
        x = PyObject_GetItem(module, fullmodname);
        Py_DECREF(fullmodname);
        if (x == NULL) {
            goto fail;
        }
    }
    return x;

fail:
    PyErr_Clear();
    PyObject *package_path = PyModule_GetFilenameObject(module);
    PyObject *errmsg = PyUnicode_FromFormat("cannot import name %R from %R (%S)",
                                            import_name, package_name, package_path);
    // NULL checks for errmsg and package_name done by PyErr_SetImportError.
    PyErr_SetImportError(errmsg, package_name, package_path);
    Py_DECREF(package_path);
    Py_DECREF(errmsg);
    return NULL;
}

PyObject *CPyImport_ImportFromMany(PyObject *mod_id, PyObject *names, PyObject *as_names,
                                   PyObject *globals) {
    PyObject *mod = PyImport_ImportModuleLevelObject(mod_id, globals, 0, names, 0);
    if (mod == NULL) {
        return NULL;
    }

    for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(names); i++) {
        PyObject *name = PyTuple_GET_ITEM(names, i);
        PyObject *as_name = PyTuple_GET_ITEM(as_names, i);
        PyObject *obj = CPyImport_ImportFrom(mod, mod_id, name, as_name);
        if (obj == NULL) {
            Py_DECREF(mod);
            return NULL;
        }
        int ret = CPyDict_SetItem(globals, as_name, obj);
        Py_DECREF(obj);
        if (ret < 0) {
            Py_DECREF(mod);
            return NULL;
        }
    }
    return mod;
}

// From CPython
static PyObject *
CPy_BinopTypeError(PyObject *left, PyObject *right, const char *op) {
    PyErr_Format(PyExc_TypeError,
                 "unsupported operand type(s) for %.100s: "
                 "'%.100s' and '%.100s'",
                 op,
                 Py_TYPE(left)->tp_name,
                 Py_TYPE(right)->tp_name);
    return NULL;
}

PyObject *
CPy_CallReverseOpMethod(PyObject *left,
                        PyObject *right,
                        const char *op,
                        _Py_Identifier *method) {
    // Look up reverse method
    PyObject *m = _PyObject_GetAttrId(right, method);
    if (m == NULL) {
        // If reverse method not defined, generate TypeError instead AttributeError
        if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
            CPy_BinopTypeError(left, right, op);
        }
        return NULL;
    }
    // Call reverse method
    PyObject *result = PyObject_CallOneArg(m, left);
    Py_DECREF(m);
    return result;
}

PyObject *CPySingledispatch_RegisterFunction(PyObject *singledispatch_func,
                                             PyObject *cls,
                                             PyObject *func) {
    PyObject *registry = PyObject_GetAttrString(singledispatch_func, "registry");
    PyObject *register_func = NULL;
    PyObject *typing = NULL;
    PyObject *get_type_hints = NULL;
    PyObject *type_hints = NULL;

    if (registry == NULL) goto fail;
    if (func == NULL) {
        // one argument case
        if (PyType_Check(cls)) {
            // passed a class
            // bind cls to the first argument so that register gets called again with both the
            // class and the function
            register_func = PyObject_GetAttrString(singledispatch_func, "register");
            if (register_func == NULL) goto fail;
            return PyMethod_New(register_func, cls);
        }
        // passed a function
        PyObject *annotations = PyFunction_GetAnnotations(cls);
        const char *invalid_first_arg_msg =
            "Invalid first argument to `register()`: %R. "
            "Use either `@register(some_class)` or plain `@register` "
            "on an annotated function.";

        if (annotations == NULL) {
            PyErr_Format(PyExc_TypeError, invalid_first_arg_msg, cls);
            goto fail;
        }

        Py_INCREF(annotations);

        func = cls;
        typing = PyImport_ImportModule("typing");
        if (typing == NULL) goto fail;
        get_type_hints = PyObject_GetAttrString(typing, "get_type_hints");

        type_hints = PyObject_CallOneArg(get_type_hints, func);
        PyObject *argname;
        Py_ssize_t pos = 0;
        if (!PyDict_Next(type_hints, &pos, &argname, &cls)) {
            // the functools implementation raises the same type error if annotations is an empty dict
            PyErr_Format(PyExc_TypeError, invalid_first_arg_msg, cls);
            goto fail;
        }
        if (!PyType_Check(cls)) {
            const char *invalid_annotation_msg = "Invalid annotation for %R. %R is not a class.";
            PyErr_Format(PyExc_TypeError, invalid_annotation_msg, argname, cls);
            goto fail;
        }
    }
    if (PyDict_SetItem(registry, cls, func) == -1) {
        goto fail;
    }

    // clear the cache so we consider the newly added function when dispatching
    PyObject *dispatch_cache = PyObject_GetAttrString(singledispatch_func, "dispatch_cache");
    if (dispatch_cache == NULL) goto fail;
    PyDict_Clear(dispatch_cache);

    Py_INCREF(func);
    return func;

fail:
    Py_XDECREF(registry);
    Py_XDECREF(register_func);
    Py_XDECREF(typing);
    Py_XDECREF(get_type_hints);
    Py_XDECREF(type_hints);
    return NULL;

}

// Adapated from ceval.c GET_AITER
PyObject *CPy_GetAIter(PyObject *obj)
{
    unaryfunc getter = NULL;
    PyTypeObject *type = Py_TYPE(obj);

    if (type->tp_as_async != NULL) {
        getter = type->tp_as_async->am_aiter;
    }

    if (getter == NULL) {
        PyErr_Format(PyExc_TypeError,
                     "'async for' requires an object with "
                     "__aiter__ method, got %.100s",
                     type->tp_name);
        Py_DECREF(obj);
        return NULL;
    }

    PyObject *iter = (*getter)(obj);
    if (!iter) {
        return NULL;
    }

    if (Py_TYPE(iter)->tp_as_async == NULL ||
        Py_TYPE(iter)->tp_as_async->am_anext == NULL) {

        PyErr_Format(PyExc_TypeError,
                     "'async for' received an object from __aiter__ "
                     "that does not implement __anext__: %.100s",
                     Py_TYPE(iter)->tp_name);
        Py_DECREF(iter);
        return NULL;
    }

    return iter;
}

// Adapated from ceval.c GET_ANEXT
PyObject *CPy_GetANext(PyObject *aiter)
{
    unaryfunc getter = NULL;
    PyObject *next_iter = NULL;
    PyObject *awaitable = NULL;
    PyTypeObject *type = Py_TYPE(aiter);

    if (PyAsyncGen_CheckExact(aiter)) {
        awaitable = type->tp_as_async->am_anext(aiter);
        if (awaitable == NULL) {
            goto error;
        }
    } else {
        if (type->tp_as_async != NULL){
            getter = type->tp_as_async->am_anext;
        }

        if (getter != NULL) {
            next_iter = (*getter)(aiter);
            if (next_iter == NULL) {
                goto error;
            }
        }
        else {
            PyErr_Format(PyExc_TypeError,
                         "'async for' requires an iterator with "
                         "__anext__ method, got %.100s",
                         type->tp_name);
            goto error;
        }

        awaitable = CPyCoro_GetAwaitableIter(next_iter);
        if (awaitable == NULL) {
            _PyErr_FormatFromCause(
                PyExc_TypeError,
                "'async for' received an invalid object "
                "from __anext__: %.100s",
                Py_TYPE(next_iter)->tp_name);

            Py_DECREF(next_iter);
            goto error;
        } else {
            Py_DECREF(next_iter);
        }
    }

    return awaitable;
error:
    return NULL;
}
