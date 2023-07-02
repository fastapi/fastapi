/* getargs implementation copied from Python 3.8 and stripped down to only include
 * the functions we need.
 * We also add support for required kwonly args and accepting *args / **kwargs.
 * A good idea would be to also vendor in the Fast versions and get our stuff
 * working with *that*.
 * Another probably good idea is to strip out all the formatting stuff we don't need
 * and then add in custom stuff that we do need.
 *
 * DOCUMENTATION OF THE EXTENSIONS:
 *  - Arguments given after a @ format specify are required keyword-only arguments.
 *    The | and $ specifiers must both appear before @.
 *  - If the first character of a format string is %, then the function can support
 *    *args and **kwargs. On seeing a %, the parser will consume two arguments,
 *    which should be pointers to variables to store the *args and **kwargs, respectively.
 *    Either pointer can be NULL, in which case the function doesn't take that
 *    variety of vararg.
 *    Unlike most format specifiers, the caller takes ownership of these objects
 *    and is responsible for decrefing them.
 *  - All arguments must use the 'O' format.
 *  - There's minimal error checking of format strings. They are generated
 *    programmatically and can be assumed valid.
 */

// These macro definitions are copied from pyport.h in Python 3.9 and later
// https://bugs.python.org/issue19569
#if defined(__clang__)
#define _Py_COMP_DIAG_PUSH _Pragma("clang diagnostic push")
#define _Py_COMP_DIAG_IGNORE_DEPR_DECLS \
    _Pragma("clang diagnostic ignored \"-Wdeprecated-declarations\"")
#define _Py_COMP_DIAG_POP _Pragma("clang diagnostic pop")
#elif defined(__GNUC__) \
    && ((__GNUC__ >= 5) || (__GNUC__ == 4) && (__GNUC_MINOR__ >= 6))
#define _Py_COMP_DIAG_PUSH _Pragma("GCC diagnostic push")
#define _Py_COMP_DIAG_IGNORE_DEPR_DECLS \
    _Pragma("GCC diagnostic ignored \"-Wdeprecated-declarations\"")
#define _Py_COMP_DIAG_POP _Pragma("GCC diagnostic pop")
#elif defined(_MSC_VER)
#define _Py_COMP_DIAG_PUSH __pragma(warning(push))
#define _Py_COMP_DIAG_IGNORE_DEPR_DECLS __pragma(warning(disable: 4996))
#define _Py_COMP_DIAG_POP __pragma(warning(pop))
#else
#define _Py_COMP_DIAG_PUSH
#define _Py_COMP_DIAG_IGNORE_DEPR_DECLS
#define _Py_COMP_DIAG_POP
#endif

#include "Python.h"
#include "pythonsupport.h"

#include <ctype.h>
#include <float.h>

#ifndef PyDict_GET_SIZE
#define PyDict_GET_SIZE(d) PyDict_Size(d)
#endif


#ifdef __cplusplus
extern "C" {
#endif
int CPyArg_ParseTupleAndKeywords(PyObject *, PyObject *,
                                 const char *, const char *, const char * const *, ...);

/* Forward */
static int vgetargskeywords(PyObject *, PyObject *,
                            const char *, const char *, const char * const *, va_list *);
static void skipitem(const char **, va_list *);

/* Support for keyword arguments donated by
   Geoff Philbrick <philbric@delphi.hks.com> */

/* Return false (0) for error, else true. */
int
CPyArg_ParseTupleAndKeywords(PyObject *args,
                             PyObject *keywords,
                             const char *format,
                             const char *fname,
                             const char * const *kwlist, ...)
{
    int retval;
    va_list va;

    va_start(va, kwlist);
    retval = vgetargskeywords(args, keywords, format, fname, kwlist, &va);
    va_end(va);
    return retval;
}

#define IS_END_OF_FORMAT(c) (c == '\0' || c == ';' || c == ':')

static int
vgetargskeywords(PyObject *args, PyObject *kwargs, const char *format,
                 const char *fname, const char * const *kwlist, va_list *p_va)
{
    int min = INT_MAX;
    int max = INT_MAX;
    int required_kwonly_start = INT_MAX;
    int has_required_kws = 0;
    int i, pos, len;
    int skip = 0;
    Py_ssize_t nargs, nkwargs;
    PyObject *current_arg;
    int bound_pos_args;

    PyObject **p_args = NULL, **p_kwargs = NULL;

    assert(args != NULL && PyTuple_Check(args));
    assert(kwargs == NULL || PyDict_Check(kwargs));
    assert(format != NULL);
    assert(kwlist != NULL);
    assert(p_va != NULL);

    /* scan kwlist and count the number of positional-only parameters */
    for (pos = 0; kwlist[pos] && !*kwlist[pos]; pos++) {
    }
    /* scan kwlist and get greatest possible nbr of args */
    for (len = pos; kwlist[len]; len++) {
#ifdef DEBUG
        if (!*kwlist[len]) {
            PyErr_SetString(PyExc_SystemError,
                            "Empty keyword parameter name");
            return 0;
        }
#endif
    }

    if (*format == '%') {
        p_args = va_arg(*p_va, PyObject **);
        p_kwargs = va_arg(*p_va, PyObject **);
        format++;
    }

    nargs = PyTuple_GET_SIZE(args);
    nkwargs = (kwargs == NULL) ? 0 : PyDict_GET_SIZE(kwargs);
    if (unlikely(nargs + nkwargs > len && !p_args && !p_kwargs)) {
        /* Adding "keyword" (when nargs == 0) prevents producing wrong error
           messages in some special cases (see bpo-31229). */
        PyErr_Format(PyExc_TypeError,
                     "%.200s%s takes at most %d %sargument%s (%zd given)",
                     (fname == NULL) ? "function" : fname,
                     (fname == NULL) ? "" : "()",
                     len,
                     (nargs == 0) ? "keyword " : "",
                     (len == 1) ? "" : "s",
                     nargs + nkwargs);
        return 0;
    }

    /* convert tuple args and keyword args in same loop, using kwlist to drive process */
    for (i = 0; i < len; i++) {
        if (*format == '|') {
#ifdef DEBUG
            if (min != INT_MAX) {
                PyErr_SetString(PyExc_SystemError,
                                "Invalid format string (| specified twice)");
                return 0;
            }
#endif

            min = i;
            format++;

#ifdef DEBUG
            if (max != INT_MAX) {
                PyErr_SetString(PyExc_SystemError,
                                "Invalid format string ($ before |)");
                return 0;
            }
#endif

            /* If there are optional args, figure out whether we have
             * required keyword arguments so that we don't bail without
             * enforcing them. */
            has_required_kws = strchr(format, '@') != NULL;
        }
        if (*format == '$') {
#ifdef DEBUG
            if (max != INT_MAX) {
                PyErr_SetString(PyExc_SystemError,
                                "Invalid format string ($ specified twice)");
                return 0;
            }
#endif

            max = i;
            format++;

#ifdef DEBUG
            if (max < pos) {
                PyErr_SetString(PyExc_SystemError,
                                "Empty parameter name after $");
                return 0;
            }
#endif
            if (skip) {
                /* Now we know the minimal and the maximal numbers of
                 * positional arguments and can raise an exception with
                 * informative message (see below). */
                break;
            }
            if (unlikely(max < nargs && !p_args)) {
                if (max == 0) {
                    PyErr_Format(PyExc_TypeError,
                                 "%.200s%s takes no positional arguments",
                                 (fname == NULL) ? "function" : fname,
                                 (fname == NULL) ? "" : "()");
                }
                else {
                    PyErr_Format(PyExc_TypeError,
                                 "%.200s%s takes %s %d positional argument%s"
                                 " (%zd given)",
                                 (fname == NULL) ? "function" : fname,
                                 (fname == NULL) ? "" : "()",
                                 (min < max) ? "at most" : "exactly",
                                 max,
                                 max == 1 ? "" : "s",
                                 nargs);
                }
                return 0;
            }
        }
        if (*format == '@') {
#ifdef DEBUG
            if (min == INT_MAX && max == INT_MAX) {
                PyErr_SetString(PyExc_SystemError,
                                "Invalid format string "
                                "(@ without preceding | and $)");
                return 0;
            }
            if (required_kwonly_start != INT_MAX) {
                PyErr_SetString(PyExc_SystemError,
                                "Invalid format string (@ specified twice)");
                return 0;
            }
#endif

            required_kwonly_start = i;
            format++;
        }
#ifdef DEBUG
        if (IS_END_OF_FORMAT(*format)) {
            PyErr_Format(PyExc_SystemError,
                         "More keyword list entries (%d) than "
                         "format specifiers (%d)", len, i);
            return 0;
        }
#endif
        if (!skip) {
            if (i < nargs && i < max) {
                current_arg = PyTuple_GET_ITEM(args, i);
            }
            else if (nkwargs && i >= pos) {
                current_arg = _PyDict_GetItemStringWithError(kwargs, kwlist[i]);
                if (current_arg) {
                    --nkwargs;
                }
                else if (PyErr_Occurred()) {
                    return 0;
                }
            }
            else {
                current_arg = NULL;
            }

            if (current_arg) {
                PyObject **p = va_arg(*p_va, PyObject **);
                *p = current_arg;
                format++;
                continue;
            }

            if (i < min || i >= required_kwonly_start) {
                if (likely(i < pos)) {
                    assert (min == INT_MAX);
                    assert (max == INT_MAX);
                    skip = 1;
                    /* At that moment we still don't know the minimal and
                     * the maximal numbers of positional arguments.  Raising
                     * an exception is deferred until we encounter | and $
                     * or the end of the format. */
                }
                else {
                    if (i >= max) {
                        PyErr_Format(PyExc_TypeError,
                                     "%.200s%s missing required "
                                     "keyword-only argument '%s'",
                                     (fname == NULL) ? "function" : fname,
                                     (fname == NULL) ? "" : "()",
                                     kwlist[i]);
                    }
                    else {
                        PyErr_Format(PyExc_TypeError,
                                     "%.200s%s missing required "
                                     "argument '%s' (pos %d)",
                                     (fname == NULL) ? "function" : fname,
                                     (fname == NULL) ? "" : "()",
                                     kwlist[i], i+1);
                    }
                    return 0;
                }
            }
            /* current code reports success when all required args
             * fulfilled and no keyword args left, with no further
             * validation. XXX Maybe skip this in debug build ?
             */
            if (!nkwargs && !skip && !has_required_kws &&
                !p_args && !p_kwargs)
            {
                return 1;
            }
        }

        /* We are into optional args, skip through to any remaining
         * keyword args */
        skipitem(&format, p_va);
    }

    if (unlikely(skip)) {
        PyErr_Format(PyExc_TypeError,
                     "%.200s%s takes %s %d positional argument%s"
                     " (%zd given)",
                     (fname == NULL) ? "function" : fname,
                     (fname == NULL) ? "" : "()",
                     (Py_MIN(pos, min) < i) ? "at least" : "exactly",
                     Py_MIN(pos, min),
                     Py_MIN(pos, min) == 1 ? "" : "s",
                     nargs);
        return 0;
    }

#ifdef DEBUG
    if (!IS_END_OF_FORMAT(*format) &&
        (*format != '|') && (*format != '$') && (*format != '@'))
    {
        PyErr_Format(PyExc_SystemError,
            "more argument specifiers than keyword list entries "
            "(remaining format:'%s')", format);
        return 0;
    }
#endif

    bound_pos_args = Py_MIN(nargs, Py_MIN(max, len));
    if (p_args) {
        *p_args = PyTuple_GetSlice(args, bound_pos_args, nargs);
        if (!*p_args) {
            return 0;
        }
    }

    if (p_kwargs) {
        /* This unfortunately needs to be special cased because if len is 0 then we
         * never go through the main loop. */
        if (unlikely(nargs > 0 && len == 0 && !p_args)) {
            PyErr_Format(PyExc_TypeError,
                         "%.200s%s takes no positional arguments",
                         (fname == NULL) ? "function" : fname,
                         (fname == NULL) ? "" : "()");

            return 0;
        }

        *p_kwargs = PyDict_New();
        if (!*p_kwargs) {
            goto latefail;
        }
    }

    if (nkwargs > 0) {
        PyObject *key, *value;
        Py_ssize_t j;
        /* make sure there are no arguments given by name and position */
        for (i = pos; i < bound_pos_args && i < len; i++) {
            current_arg = _PyDict_GetItemStringWithError(kwargs, kwlist[i]);
            if (unlikely(current_arg != NULL)) {
                /* arg present in tuple and in dict */
                PyErr_Format(PyExc_TypeError,
                             "argument for %.200s%s given by name ('%s') "
                             "and position (%d)",
                             (fname == NULL) ? "function" : fname,
                             (fname == NULL) ? "" : "()",
                             kwlist[i], i+1);
                goto latefail;
            }
            else if (unlikely(PyErr_Occurred() != NULL)) {
                goto latefail;
            }
        }
        /* make sure there are no extraneous keyword arguments */
        j = 0;
        while (PyDict_Next(kwargs, &j, &key, &value)) {
            int match = 0;
            if (unlikely(!PyUnicode_Check(key))) {
                PyErr_SetString(PyExc_TypeError,
                                "keywords must be strings");
                goto latefail;
            }
            for (i = pos; i < len; i++) {
                if (CPyUnicode_EqualToASCIIString(key, kwlist[i])) {
                    match = 1;
                    break;
                }
            }
            if (!match) {
                if (unlikely(!p_kwargs)) {
                    PyErr_Format(PyExc_TypeError,
                                 "'%U' is an invalid keyword "
                                 "argument for %.200s%s",
                                 key,
                                 (fname == NULL) ? "this function" : fname,
                                 (fname == NULL) ? "" : "()");
                    goto latefail;
                } else {
                    if (PyDict_SetItem(*p_kwargs, key, value) < 0) {
                        goto latefail;
                    }
                }
            }
        }
    }

    return 1;
    /* Handle failures that have happened after we have tried to
     * create *args and **kwargs, if they exist. */
latefail:
    if (p_args) {
        Py_XDECREF(*p_args);
    }
    if (p_kwargs) {
        Py_XDECREF(*p_kwargs);
    }
    return 0;
}


static void
skipitem(const char **p_format, va_list *p_va)
{
    const char *format = *p_format;
    char c = *format++;

    if (p_va != NULL) {
        (void) va_arg(*p_va, PyObject **);
    }

    *p_format = format;
}

#ifdef __cplusplus
};
#endif
