/* -*- indent-tabs-mode: nil; tab-width: 4; -*- */
/* Format with:
 *  clang-format -i --style=file src/greenlet/greenlet.c
 *
 *
 * Fix missing braces with:
 *   clang-tidy src/greenlet/greenlet.c -fix -checks="readability-braces-around-statements"
*/
#include <cstdlib>
#include <string>
#include <algorithm>
#include <exception>


#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h" // PyMemberDef

#include "greenlet_internal.hpp"
#include "greenlet_refs.hpp"
#include "greenlet_slp_switch.hpp"
#include "greenlet_thread_state.hpp"
#include "greenlet_thread_support.hpp"
#include "greenlet_greenlet.hpp"

using greenlet::ThreadState;
using greenlet::Mutex;
using greenlet::LockGuard;
using greenlet::LockInitError;
using greenlet::PyErrOccurred;
using greenlet::Require;
using greenlet::PyFatalError;
using greenlet::ExceptionState;
using greenlet::StackState;
using greenlet::Greenlet;


// Helpers for reference counting.
// XXX: running the test cases for greenlet 1.1.2 under Python 3.10+pydebug
// with zope.testrunner's "report refcounts" option shows a growth of
// over 500 references when running 90 tests at a steady state (10 repeats)
// Running in verbose mode and adding objgraph to report gives us this
// info in a steady state:
//   Ran 90 tests with 0 failures, 0 errors and 1 skipped in 2.120 seconds.
// Showing growth
// tuple                 2811       +16
// list                  1733       +14
// function              6304       +11
// dict                  3604        +9
// cell                   707        +9
// greenlet                81        +8
// method                 103        +5
// Genlet                  40        +4
// list_iterator           30        +3
// getset_descriptor      916        +2
//   sum detail refcount=341678   sys refcount=379357   change=523
//     Leak details, changes in instances and refcounts by type/class:
//     type/class                                               insts   refs
//     -------------------------------------------------------  -----   ----
//     builtins.NoneType                                            0      2
//     builtins.cell                                                9     20
//     builtins.code                                                0     31
//     builtins.dict                                               18     91
//     builtins.frame                                              20     32
//     builtins.function                                           11     28
//     builtins.getset_descriptor                                   2      2
//     builtins.int                                                 2     42
//     builtins.list                                               14     37
//     builtins.list_iterator                                       3      3
//     builtins.method                                              5      5
//     builtins.method_descriptor                                   0      9
//     builtins.str                                                11     76
//     builtins.traceback                                           1      2
//     builtins.tuple                                              20     42
//     builtins.type                                                2     28
//     builtins.weakref                                             2      2
//     greenlet.GreenletExit                                        1      1
//     greenlet.greenlet                                            8     26
//     greenlet.tests.test_contextvars.NoContextVarsTests           0      1
//     greenlet.tests.test_gc.object_with_finalizer                 1      1
//     greenlet.tests.test_generator_nested.Genlet                  4     26
//     greenlet.tests.test_greenlet.convoluted                      1      2
//     -------------------------------------------------------  -----   ----
//     total                                                      135    509
//
// As of the commit that adds this comment, we're doing better than
// 1.1.2, but still not perfect:
//   Ran 115 tests with 0 failures, 0 errors, 1 skipped in 8.623 seconds.
// tuple            21310       +23
// dict              5428       +18
// frame              183       +17
// list              1760       +14
// function          6359       +11
// cell               698        +8
// method             105        +5
// int               2709        +4
// TheGenlet           40        +4
// list_iterator       30        +3
//   sum detail refcount=345051   sys refcount=383043   change=494
//     Leak details, changes in instances and refcounts by type/class:
//     type/class                                               insts   refs
//     -------------------------------------------------------  -----   ----
//     builtins.NoneType                                            0     12
//     builtins.bool                                                0      2
//     builtins.cell                                                8     16
//     builtins.code                                                0     28
//     builtins.dict                                               18     74
//     builtins.frame                                              17     28
//     builtins.function                                           11     28
//     builtins.getset_descriptor                                   2      2
//     builtins.int                                                 4     44
//     builtins.list                                               14     39
//     builtins.list_iterator                                       3      3
//     builtins.method                                              5      5
//     builtins.method_descriptor                                   0      8
//     builtins.str                                                -2     69
//     builtins.tuple                                              23     42
//     builtins.type                                                2     28
//     builtins.weakref                                             2      2
//     greenlet.greenlet                                            1      1
//     greenlet.main_greenlet                                       1     16
//     greenlet.tests.test_contextvars.NoContextVarsTests           0      1
//     greenlet.tests.test_gc.object_with_finalizer                 1      1
//     greenlet.tests.test_generator_nested.TheGenlet               4     29
//     greenlet.tests.test_greenlet.convoluted                      1      2
//     greenlet.tests.test_leaks.HasFinalizerTracksInstances        2      2
//     -------------------------------------------------------  -----   ----
//     total                                                      117    482

using greenlet::refs::BorrowedObject;
using greenlet::refs::BorrowedGreenlet;
using greenlet::refs::BorrowedMainGreenlet;
using greenlet::refs::OwnedObject;
using greenlet::refs::PyErrFetchParam;
using greenlet::refs::PyArgParseParam;
using greenlet::refs::ImmortalString;
using greenlet::refs::ImmortalObject;
using greenlet::refs::CreatedModule;
using greenlet::refs::PyErrPieces;
using greenlet::refs::PyObjectPointer;
using greenlet::Greenlet;
using greenlet::UserGreenlet;
using greenlet::MainGreenlet;


// ******* Implementation of things from included files
template<typename T, greenlet::refs::TypeChecker TC>
greenlet::refs::_BorrowedGreenlet<T, TC>& greenlet::refs::_BorrowedGreenlet<T, TC>::operator=(const greenlet::refs::BorrowedObject& other)
{
    this->_set_raw_pointer(static_cast<PyObject*>(other));
    return *this;
}

template <typename T, greenlet::refs::TypeChecker TC>
inline greenlet::refs::_BorrowedGreenlet<T, TC>::operator Greenlet*() const G_NOEXCEPT
{
    if (!this->p) {
        return nullptr;
    }
    return reinterpret_cast<PyGreenlet*>(this->p)->pimpl;
}

template<typename T, greenlet::refs::TypeChecker TC>
greenlet::refs::_BorrowedGreenlet<T, TC>::_BorrowedGreenlet(const BorrowedObject& p)
    : BorrowedReference<T, TC>(nullptr)
{

    this->_set_raw_pointer(p.borrow());
}

template <typename T, greenlet::refs::TypeChecker TC>
inline greenlet::refs::_OwnedGreenlet<T, TC>::operator Greenlet*() const G_NOEXCEPT
{
    if (!this->p) {
        return nullptr;
    }
    return reinterpret_cast<PyGreenlet*>(this->p)->pimpl;
}



#ifdef __clang__
#    pragma clang diagnostic push
#    pragma clang diagnostic ignored "-Wmissing-field-initializers"
#    pragma clang diagnostic ignored "-Wwritable-strings"
#elif defined(__GNUC__)
#    pragma GCC diagnostic push
//  warning: ISO C++ forbids converting a string constant to ‘char*’
// (The python APIs aren't const correct and accept writable char*)
#    pragma GCC diagnostic ignored "-Wwrite-strings"
#endif


/***********************************************************

A PyGreenlet is a range of C stack addresses that must be
saved and restored in such a way that the full range of the
stack contains valid data when we switch to it.

Stack layout for a greenlet:

               |     ^^^       |
               |  older data   |
               |               |
  stack_stop . |_______________|
        .      |               |
        .      | greenlet data |
        .      |   in stack    |
        .    * |_______________| . .  _____________  stack_copy + stack_saved
        .      |               |     |             |
        .      |     data      |     |greenlet data|
        .      |   unrelated   |     |    saved    |
        .      |      to       |     |   in heap   |
 stack_start . |     this      | . . |_____________| stack_copy
               |   greenlet    |
               |               |
               |  newer data   |
               |     vvv       |


Note that a greenlet's stack data is typically partly at its correct
place in the stack, and partly saved away in the heap, but always in
the above configuration: two blocks, the more recent one in the heap
and the older one still in the stack (either block may be empty).

Greenlets are chained: each points to the previous greenlet, which is
the one that owns the data currently in the C stack above my
stack_stop.  The currently running greenlet is the first element of
this chain.  The main (initial) greenlet is the last one.  Greenlets
whose stack is entirely in the heap can be skipped from the chain.

The chain is not related to execution order, but only to the order
in which bits of C stack happen to belong to greenlets at a particular
point in time.

The main greenlet doesn't have a stack_stop: it is responsible for the
complete rest of the C stack, and we don't know where it begins.  We
use (char*) -1, the largest possible address.

States:
  stack_stop == NULL && stack_start == NULL:  did not start yet
  stack_stop != NULL && stack_start == NULL:  already finished
  stack_stop != NULL && stack_start != NULL:  active

The running greenlet's stack_start is undefined but not NULL.

 ***********************************************************/

/*** global state ***/

/* In the presence of multithreading, this is a bit tricky; see
   greenlet_thread_state.hpp for details.
*/


static inline OwnedObject
single_result(const OwnedObject& results)
{
    if (results
        && PyTuple_Check(results.borrow())
        && PyTuple_GET_SIZE(results.borrow()) == 1) {
        PyObject* result = PyTuple_GET_ITEM(results.borrow(), 0);
        return OwnedObject::owning(result);
    }
    return results;
}



class ImmortalEventName : public ImmortalString
{
private:
    G_NO_COPIES_OF_CLS(ImmortalEventName);
public:
    ImmortalEventName(const char* const str) : ImmortalString(str)
    {}
};

class ImmortalException : public ImmortalObject
{
private:
    G_NO_COPIES_OF_CLS(ImmortalException);
public:
    ImmortalException(const char* const name, PyObject* base=nullptr) :
        ImmortalObject(name
                       // Python 2.7 isn't const correct
                       ? Require(PyErr_NewException((char*)name, base, nullptr))
                       : nullptr)
    {}

    inline bool PyExceptionMatches() const
    {
        return PyErr_ExceptionMatches(this->p) > 0;
    }

};

// This encapsulates what were previously module global "constants"
// established at init time.
// This is a step towards Python3 style module state that allows
// reloading.
// We play some tricks with placement new to be able to allocate this
// object statically still, so that references to its members don't
// incur an extra pointer indirection.
class GreenletGlobals
{
public:
    const ImmortalEventName event_switch;
    const ImmortalEventName event_throw;
    const ImmortalException PyExc_GreenletError;
    const ImmortalException PyExc_GreenletExit;
    const ImmortalObject empty_tuple;
    const ImmortalObject empty_dict;
    const ImmortalString str_run;
    Mutex* const thread_states_to_destroy_lock;
    greenlet::cleanup_queue_t thread_states_to_destroy;

    GreenletGlobals(const int UNUSED(dummy)) :
        event_switch(0),
        event_throw(0),
        PyExc_GreenletError(0),
        PyExc_GreenletExit(0),
        empty_tuple(0),
        empty_dict(0),
        str_run(0),
        thread_states_to_destroy_lock(0)
    {}

    GreenletGlobals() :
        event_switch("switch"),
        event_throw("throw"),
        PyExc_GreenletError("greenlet.error"),
        PyExc_GreenletExit("greenlet.GreenletExit", PyExc_BaseException),
        empty_tuple(Require(PyTuple_New(0))),
        empty_dict(Require(PyDict_New())),
        str_run("run"),
        thread_states_to_destroy_lock(new Mutex())
    {}

    ~GreenletGlobals()
    {
        // This object is (currently) effectively immortal, and not
        // just because of those placement new tricks; if we try to
        // deallocate the static object we allocated, and overwrote,
        // we would be doing so at C++ teardown time, which is after
        // the final Python GIL is released, and we can't use the API
        // then.
        // (The members will still be destructed, but they also don't
        // do any deallocation.)
    }

    void queue_to_destroy(ThreadState* ts) const
    {
        // we're currently accessed through a static const object,
        // implicitly marking our members as const, so code can't just
        // call push_back (or pop_back) without casting away the
        // const.
        //
        // Do that for callers.
        greenlet::cleanup_queue_t& q = const_cast<greenlet::cleanup_queue_t&>(this->thread_states_to_destroy);
        q.push_back(ts);
    }

    ThreadState* take_next_to_destroy() const
    {
        greenlet::cleanup_queue_t& q = const_cast<greenlet::cleanup_queue_t&>(this->thread_states_to_destroy);
        ThreadState* result = q.back();
        q.pop_back();
        return result;
    }
};

static const GreenletGlobals mod_globs(0);

// Protected by the GIL. Incremented when we create a main greenlet,
// in a new thread, decremented when it is destroyed.
static Py_ssize_t total_main_greenlets;

struct ThreadState_DestroyWithGIL
{
    ThreadState_DestroyWithGIL(ThreadState* state)
    {
        if (state && state->has_main_greenlet()) {
            DestroyWithGIL(state);
        }
    }

    static int
    DestroyWithGIL(ThreadState* state)
    {
        // Holding the GIL.
        // Passed a non-shared pointer to the actual thread state.
        // state -> main greenlet
        assert(state->has_main_greenlet());
        PyGreenlet* main(state->borrow_main_greenlet());
        // When we need to do cross-thread operations, we check this.
        // A NULL value means the thread died some time ago.
        // We do this here, rather than in a Python dealloc function
        // for the greenlet, in case there's still a reference out
        // there.
        static_cast<MainGreenlet*>(main->pimpl)->thread_state(nullptr);

        delete state; // Deleting this runs the destructor, DECREFs the main greenlet.
        return 0;
    }
};

#if (PY_VERSION_HEX >= 0x30800A0 && PY_VERSION_HEX < 0x3090000) && !(defined(_WIN32) || defined(WIN32))
// XXX: From Python 3.8a3 [1] up until Python 3.9a6 [2][3],
// ``Py_AddPendingCall`` would try to produce a Python exception if
// the interpreter was in the beginning of shutting down when this
// function is called. However, ``Py_AddPendingCall`` doesn't require
// the GIL, and we are absolutely not holding it when we make that
// call. That means that trying to create the Python exception is
// using the C API in an undefined state; here the C API detects this
// and aborts the process with an error ("Fatal Python error: Python
// memory allocator called without holding the GIL": Add ->
// PyErr_SetString -> PyUnicode_New -> PyObject_Malloc). This arises
// (obviously) in multi-threaded programs and happens if one thread is
// exiting and cleaning up its thread-local data while the other
// thread is trying to shut down the interpreter. A crash on shutdown
// is still a crash and could result in data loss (e.g., daemon
// threads are still running, pending signal handlers may be present,
// buffers may not be flushed, there may be __del__ that need run,
// etc), so we have to work around it.
//
// Of course, we can (and do) check for whether the interpreter is
// shutting down before calling ``Py_AddPendingCall``, but that's a
// race condition since we don't hold the GIL, and so we may not
// actually get the right answer. Plus, ``Py_FinalizeEx`` actually
// calls ``_Py_FinishPendingCalls`` (which sets the pending->finishing
// flag, which is used to gate creating the exceptioen) *before*
// publishing any other data that would let us detect the shutdown
// (such as runtime->finalizing). So that point is moot.
//
// Our solution for those versions is to inline the same code, without
// the problematic bit that sets the exception. Unfortunately, all of
// the structure definitions are private/opaque, *and* we can't
// actually count on being able to include their definitions from
// ``internal/pycore_*``, because on some platforms those header files
// are incomplete (i.e., on macOS with macports 3.8, the includes are
// fine, but on Ubuntu jammy with 3.8 from ppa:deadsnakes or GitHub
// Actions 3.8 (I think it's Ubuntu 18.04), they con't be used; at
// least, I couldn't get them to work). So we need to define the
// structures and _PyRuntime data member ourself. Yet more
// unfortunately, _PyRuntime  won't link on Windows, so we can only do
// this on other platforms.
//
// [1] https://github.com/python/cpython/commit/842a2f07f2f08a935ef470bfdaeef40f87490cfc
// [2] https://github.com/python/cpython/commit/cfc3c2f8b34d3864717ab584c5b6c260014ba55a
// [3] https://github.com/python/cpython/issues/81308
# define GREENLET_BROKEN_PY_ADD_PENDING 1

// When defining these structures, the important thing is to get
// binary compatibility, i.e., structure layout. For that, we only
// need to define fields up to the ones we use; after that they're
// irrelevant UNLESS the structure is included in another structure
// *before* the structure we're interested in --- in that case, it
// must be complete. Ellipsis indicate elided trailing members.
// Pointer types are changed to void* to keep from having to define
// more structures.

// From "internal/pycore_atomic.h"

// There are several different definitions of this, including the
// plain ``int`` version, a ``volatile int`` and an ``_Atomic int``
// I don't think any of those change the size/layout.
typedef struct _Py_atomic_int {
    volatile int _value;
} _Py_atomic_int;

// This needs too much infrastructure, so we just do a regular store.
#define _Py_atomic_store_relaxed(ATOMIC_VAL, NEW_VAL) \
    (ATOMIC_VAL)->_value = NEW_VAL



// From "internal/pycore_pymem.h"
#define NUM_GENERATIONS 3


struct gc_generation {
    PyGC_Head head; // We already have this defined.
    int threshold;
    int count;
};
struct gc_generation_stats {
    Py_ssize_t collections;
    Py_ssize_t collected;
    Py_ssize_t uncollectable;
};

struct _gc_runtime_state {
    void *trash_delete_later;
    int trash_delete_nesting;
    int enabled;
    int debug;
    struct gc_generation generations[NUM_GENERATIONS];
    void *generation0;
    struct gc_generation permanent_generation;
    struct gc_generation_stats generation_stats[NUM_GENERATIONS];
    int collecting;
    void *garbage;
    void *callbacks;
    Py_ssize_t long_lived_total;
    Py_ssize_t long_lived_pending;
};

// From "internal/pycore_pystate.h"
struct _pending_calls {
    int finishing;
    PyThread_type_lock lock;
    _Py_atomic_int calls_to_do;
    int async_exc;
#define NPENDINGCALLS 32
    struct {
        int (*func)(void *);
        void *arg;
    } calls[NPENDINGCALLS];
    int first;
    int last;
};

struct _ceval_runtime_state {
    int recursion_limit;
    int tracing_possible;
    _Py_atomic_int eval_breaker;
    _Py_atomic_int gil_drop_request;
    struct _pending_calls pending;
    // ...
};

typedef struct pyruntimestate {
    int preinitializing;
    int preinitialized;
    int core_initialized;
    int initialized;
    void *finalizing;

    struct pyinterpreters {
        PyThread_type_lock mutex;
        void *head;
        void *main;
        int64_t next_id;
    } interpreters;
    // XXX Remove this field once we have a tp_* slot.
    struct _xidregistry {
        PyThread_type_lock mutex;
        void *head;
    } xidregistry;

    unsigned long main_thread;

#define NEXITFUNCS 32
    void (*exitfuncs[NEXITFUNCS])(void);
    int nexitfuncs;

    struct _gc_runtime_state gc;
    struct _ceval_runtime_state ceval;
    // ...
} _PyRuntimeState;

#define SIGNAL_PENDING_CALLS(ceval) \
    do { \
        _Py_atomic_store_relaxed(&(ceval)->pending.calls_to_do, 1); \
        _Py_atomic_store_relaxed(&(ceval)->eval_breaker, 1); \
    } while (0)

extern _PyRuntimeState _PyRuntime;

#else
# define GREENLET_BROKEN_PY_ADD_PENDING 0
#endif


struct ThreadState_DestroyNoGIL
{
#if GREENLET_BROKEN_PY_ADD_PENDING
    static int _push_pending_call(struct _pending_calls *pending,
                                  int (*func)(void *), void *arg)
    {
        int i = pending->last;
        int j = (i + 1) % NPENDINGCALLS;
        if (j == pending->first) {
            return -1; /* Queue full */
        }
        pending->calls[i].func = func;
        pending->calls[i].arg = arg;
        pending->last = j;
        return 0;
    }

    static int AddPendingCall(int (*func)(void *), void *arg)
    {
        _PyRuntimeState *runtime = &_PyRuntime;
        if (!runtime) {
            // obviously impossible
            return 0;
        }
        struct _pending_calls *pending = &runtime->ceval.pending;
        if (!pending->lock) {
            return 0;
        }
        int result = 0;
        PyThread_acquire_lock(pending->lock, WAIT_LOCK);
        if (!pending->finishing) {
            result = _push_pending_call(pending, func, arg);
        }
        PyThread_release_lock(pending->lock);
        SIGNAL_PENDING_CALLS(&runtime->ceval);
        return result;
    }
#else
    // Python < 3.8 or >= 3.9
    static int AddPendingCall(int (*func)(void*), void* arg)
    {
        return Py_AddPendingCall(func, arg);
    }
#endif

    ThreadState_DestroyNoGIL(ThreadState* state)
    {
        // We are *NOT* holding the GIL. Our thread is in the middle
        // of its death throes and the Python thread state is already
        // gone so we can't use most Python APIs. One that is safe is
        // ``Py_AddPendingCall``, unless the interpreter itself has
        // been torn down. There is a limited number of calls that can
        // be queued: 32 (NPENDINGCALLS) in CPython 3.10, so we
        // coalesce these calls using our own queue.
        if (state && state->has_main_greenlet()) {
            // mark the thread as dead ASAP.
            // this is racy! If we try to throw or switch to a
            // greenlet from this thread from some other thread before
            // we clear the state pointer, it won't realize the state
            // is dead which can crash the process.
            PyGreenlet* p = state->borrow_main_greenlet();
            assert(p->pimpl->thread_state() == state || p->pimpl->thread_state() == nullptr);
            static_cast<MainGreenlet*>(p->pimpl)->thread_state(nullptr);
        }

        // NOTE: Because we're not holding the GIL here, some other
        // Python thread could run and call ``os.fork()``, which would
        // be bad if that happenend while we are holding the cleanup
        // lock (it wouldn't function in the child process).
        // Make a best effort to try to keep the duration we hold the
        // lock short.
        // TODO: On platforms that support it, use ``pthread_atfork`` to
        // drop this lock.
        LockGuard cleanup_lock(*mod_globs.thread_states_to_destroy_lock);

        if (state && state->has_main_greenlet()) {
            // Because we don't have the GIL, this is a race condition.
            if (!PyInterpreterState_Head()) {
                // We have to leak the thread state, if the
                // interpreter has shut down when we're getting
                // deallocated, we can't run the cleanup code that
                // deleting it would imply.
                return;
            }

            mod_globs.queue_to_destroy(state);
            if (mod_globs.thread_states_to_destroy.size() == 1) {
                // We added the first item to the queue. We need to schedule
                // the cleanup.
                int result = ThreadState_DestroyNoGIL::AddPendingCall(
                    ThreadState_DestroyNoGIL::DestroyQueueWithGIL,
                    NULL);
                if (result < 0) {
                    // Hmm, what can we do here?
                    fprintf(stderr,
                            "greenlet: WARNING: failed in call to Py_AddPendingCall; "
                            "expect a memory leak.\n");
                }
            }
        }
    }

    static int
    DestroyQueueWithGIL(void* UNUSED(arg))
    {
        // We're holding the GIL here, so no Python code should be able to
        // run to call ``os.fork()``.
        while (1) {
            ThreadState* to_destroy;
            {
                LockGuard cleanup_lock(*mod_globs.thread_states_to_destroy_lock);
                if (mod_globs.thread_states_to_destroy.empty()) {
                    break;
                }
                to_destroy = mod_globs.take_next_to_destroy();
            }
            // Drop the lock while we do the actual deletion.
            ThreadState_DestroyWithGIL::DestroyWithGIL(to_destroy);
        }
        return 0;
    }

};

// The intent when GET_THREAD_STATE() is used multiple times in a function is to
// take a reference to it in a local variable, to avoid the
// thread-local indirection. On some platforms (macOS),
// accessing a thread-local involves a function call (plus an initial
// function call in each function that uses a thread local); in
// contrast, static volatile variables are at some pre-computed offset.

#if G_USE_STANDARD_THREADING == 1
typedef greenlet::ThreadStateCreator<ThreadState_DestroyNoGIL> ThreadStateCreator;
static G_THREAD_LOCAL_VAR ThreadStateCreator g_thread_state_global;
#define GET_THREAD_STATE() g_thread_state_global
#else
// if we're not using standard threading, we're using
// the Python thread-local dictionary to perform our cleanup,
// which means we're deallocated when holding the GIL. The
// thread state is valid enough still for us to destroy
// stuff.
typedef greenlet::ThreadStateCreator<ThreadState_DestroyWithGIL> ThreadStateCreator;
#define G_THREAD_STATE_DICT_CLEANUP_TYPE
#include "greenlet_thread_state_dict_cleanup.hpp"
typedef greenlet::refs::OwnedReference<PyGreenletCleanup> OwnedGreenletCleanup;
// RECALL: legacy thread-local objects (__thread on GCC, __declspec(thread) on
// MSVC) can't have constructors or destructors, they have to be
// constant. So we indirect through a pointer and a function.
static G_THREAD_LOCAL_VAR ThreadStateCreator* _g_thread_state_global_ptr = nullptr;
static ThreadStateCreator& GET_THREAD_STATE()
{
    if (!_g_thread_state_global_ptr) {
        // NOTE: If any of this fails, we'll probably go on to hard
        // crash the process, because we're returning a reference to a
        // null pointer. we've called Py_FatalError(), but have no way
        // to communicate that to the caller. Since these should
        // essentially never fail unless the entire process is borked,
        // a hard crash with a decent C++ backtrace from the exception
        // is much more useful.
        _g_thread_state_global_ptr = new ThreadStateCreator();
        if (!_g_thread_state_global_ptr) {
            throw PyFatalError("greenlet: Failed to create greenlet thread state.");
        }

        OwnedGreenletCleanup cleanup(OwnedGreenletCleanup::consuming(PyType_GenericAlloc(&PyGreenletCleanup_Type, 0)));
        if (!cleanup) {
            throw PyFatalError("greenlet: Failed to create greenlet thread state cleanup.");
        }

        cleanup->thread_state_creator = _g_thread_state_global_ptr;
        assert(PyObject_GC_IsTracked(cleanup.borrow_o()));

        PyObject* ts_dict_w = PyThreadState_GetDict();
        if (!ts_dict_w) {
            throw PyFatalError("greenlet: Failed to get Python thread state.");
        }
        if (PyDict_SetItemString(ts_dict_w, "__greenlet_cleanup", cleanup.borrow_o()) < 0) {
            throw PyFatalError("greenlet: Failed to save cleanup key in Python thread state.");
        }
    }
    return *_g_thread_state_global_ptr;
}
#endif


Greenlet::Greenlet(PyGreenlet* p)
{
    p ->pimpl = this;
}

Greenlet::Greenlet(PyGreenlet* p, const StackState& initial_stack)
    : stack_state(initial_stack)
{
    // can't use a delegating constructor because of
    // MSVC for Python 2.7
    p->pimpl = this;
}

UserGreenlet::UserGreenlet(PyGreenlet* p,BorrowedGreenlet the_parent)
    : Greenlet(p), _parent(the_parent)
{
    this->_self = p;
}


MainGreenlet::MainGreenlet(PyGreenlet* p, ThreadState* state)
    : Greenlet(p, StackState::make_main()),
      _self(p),
      _thread_state(state)
{
    total_main_greenlets++;
}

ThreadState*
MainGreenlet::thread_state() const G_NOEXCEPT
{
    return this->_thread_state;
}

void
MainGreenlet::thread_state(ThreadState* t) G_NOEXCEPT
{
    assert(!t);
    this->_thread_state = t;
}

BorrowedGreenlet
UserGreenlet::self() const G_NOEXCEPT
{
    return this->_self;
}

BorrowedGreenlet
MainGreenlet::self() const G_NOEXCEPT
{
    return BorrowedGreenlet(this->_self.borrow());
}

const BorrowedMainGreenlet
UserGreenlet::main_greenlet() const
{
    return this->_main_greenlet;
}

const BorrowedMainGreenlet
MainGreenlet::main_greenlet() const
{
    return this->_self;
}

static PyGreenlet*
green_create_main(ThreadState* state)
{
    PyGreenlet* gmain;

    /* create the main greenlet for this thread */
    gmain = (PyGreenlet*)PyType_GenericAlloc(&PyGreenlet_Type, 0);
    if (gmain == NULL) {
        Py_FatalError("green_create_main failed to alloc");
        return NULL;
    }
    new MainGreenlet(gmain, state);

    assert(Py_REFCNT(gmain) == 1);
    return gmain;
}


BorrowedMainGreenlet
UserGreenlet::find_main_greenlet_in_lineage() const
{
    if (this->started()) {
        assert(this->_main_greenlet);
        return BorrowedMainGreenlet(this->_main_greenlet);
    }

    if (!this->_parent) {
        /* garbage collected greenlet in chain */
        // XXX: WHAT?
        return BorrowedMainGreenlet(nullptr);
    }

    return this->_parent->find_main_greenlet_in_lineage();
}


BorrowedMainGreenlet
MainGreenlet::find_main_greenlet_in_lineage() const
{
    return BorrowedMainGreenlet(this->_self);
}

/***********************************************************/

/* Some functions must not be inlined:
   * slp_restore_state, when inlined into slp_switch might cause
     it to restore stack over its own local variables
   * slp_save_state, when inlined would add its own local
     variables to the saved stack, wasting space
   * slp_switch, cannot be inlined for obvious reasons
   * g_initialstub, when inlined would receive a pointer into its
     own stack frame, leading to incomplete stack save/restore

g_initialstub is a member function and declared virtual so that the
compiler always calls it through a vtable.

slp_save_state and slp_restore_state are also member functions. They
are called from trampoline functions that themselves are declared as
not eligible for inlining.
*/



/* add forward declarations */


static void
g_calltrace(const OwnedObject& tracefunc,
            const ImmortalEventName& event,
            const BorrowedGreenlet& origin,
            const BorrowedGreenlet& target);

static OwnedObject
g_handle_exit(const OwnedObject& greenlet_result);





/**
 * CAUTION: May invoke arbitrary Python code.
 *
 * Figure out what the result of ``greenlet.switch(arg, kwargs)``
 * should be and transfers ownership of it to the left-hand-side.
 *
 * If switch() was just passed an arg tuple, then we'll just return that.
 * If only keyword arguments were passed, then we'll pass the keyword
 * argument dict. Otherwise, we'll create a tuple of (args, kwargs) and
 * return both.
 */
OwnedObject& operator<<=(OwnedObject& lhs, greenlet::SwitchingArgs& rhs) G_NOEXCEPT
{
    // Because this may invoke arbitrary Python code, which could
    // result in switching back to us, we need to get the
    // arguments locally on the stack.
    assert(rhs);
    OwnedObject args = rhs.args();
    OwnedObject kwargs = rhs.kwargs();
    rhs.CLEAR();
    // We shouldn't be called twice for the same switch.
    assert(args || kwargs);
    assert(!rhs);

    if (!kwargs) {
        lhs = args;
    }
    else if (!PyDict_Size(kwargs.borrow())) {
        lhs = args;
    }
    else if (!PySequence_Length(args.borrow())) {
        lhs = kwargs;
    }
    else {
        lhs = OwnedObject::consuming(PyTuple_Pack(2, args.borrow(), kwargs.borrow()));
    }
    return lhs;
}



void Greenlet::release_args()
{
    this->switch_args.CLEAR();
}


void* UserGreenlet::operator new(size_t UNUSED(count))
{
    return allocator.allocate(1);
}


void UserGreenlet::operator delete(void* ptr)
{
    return allocator.deallocate(static_cast<UserGreenlet*>(ptr),
                                1);
}

void* MainGreenlet::operator new(size_t UNUSED(count))
{
    return allocator.allocate(1);
}


void MainGreenlet::operator delete(void* ptr)
{
    return allocator.deallocate(static_cast<MainGreenlet*>(ptr),
                                1);
}


OwnedObject
Greenlet::throw_GreenletExit_during_dealloc(const ThreadState& UNUSED(current_thread_state))
{
    // If we're killed because we lost all references in the
    // middle of a switch, that's ok. Don't reset the args/kwargs,
    // we still want to pass them to the parent.
    PyErr_SetString(mod_globs.PyExc_GreenletExit,
                    "Killing the greenlet because all references have vanished.");
    // To get here it had to have run before
    return this->g_switch();
}

OwnedObject
UserGreenlet::throw_GreenletExit_during_dealloc(const ThreadState& current_thread_state)
{
    /* The dying greenlet cannot be a parent of ts_current
       because the 'parent' field chain would hold a
       reference */
    UserGreenlet::ParentIsCurrentGuard with_current_parent(this, current_thread_state);

    // We don't care about the return value, only whether an
    // exception happened. Whether or not an exception happens,
    // we need to restore the parent in case the greenlet gets
    // resurrected.
    return Greenlet::throw_GreenletExit_during_dealloc(current_thread_state);
}

ThreadState*
UserGreenlet::thread_state() const G_NOEXCEPT
{
    // TODO: maybe make this throw, if the thread state isn't there?
    // if (!this->main_greenlet) {
    //     throw std::runtime_error("No thread state"); // TODO: Better exception
    // }
    if (!this->_main_greenlet) {
        return nullptr;
    }
    return this->_main_greenlet->thread_state();
}



bool
UserGreenlet::was_running_in_dead_thread() const G_NOEXCEPT
{
    return this->_main_greenlet && !this->thread_state();
}

bool
MainGreenlet::was_running_in_dead_thread() const G_NOEXCEPT
{
    return !this->_thread_state;
}

inline void
Greenlet::slp_restore_state() G_NOEXCEPT
{
#ifdef SLP_BEFORE_RESTORE_STATE
    SLP_BEFORE_RESTORE_STATE();
#endif
    this->stack_state.copy_heap_to_stack(
           this->thread_state()->borrow_current()->stack_state);
}


inline int
Greenlet::slp_save_state(char *const stackref) G_NOEXCEPT
{
    // XXX: This used to happen in the middle, before saving, but
    // after finding the next owner. Does that matter? This is
    // only defined for Sparc/GCC where it flushes register
    // windows to the stack (I think)
#ifdef SLP_BEFORE_SAVE_STATE
    SLP_BEFORE_SAVE_STATE();
#endif
    return this->stack_state.copy_stack_to_heap(stackref,
                                                this->thread_state()->borrow_current()->stack_state);
}


OwnedObject
UserGreenlet::g_switch()
{
    try {
        this->check_switch_allowed();
    }
    catch(const PyErrOccurred&) {
        this->release_args();
        throw;
    }

    // Switching greenlets used to attempt to clean out ones that need
    // deleted *if* we detected a thread switch. Should it still do
    // that?
    // An issue is that if we delete a greenlet from another thread,
    // it gets queued to this thread, and ``kill_greenlet()`` switches
    // back into the greenlet

    /* find the real target by ignoring dead greenlets,
       and if necessary starting a greenlet. */
    switchstack_result_t err;
    Greenlet* target = this;
    // TODO: probably cleaner to handle the case where we do
    // switch to ourself separately from the other cases.
    // This can probably even further be simplified if we keep
    // track of the switching_state we're going for and just call
    // into g_switch() if it's not ourself. The main problem with that
    // is that we would be using more stack space.
    bool target_was_me = true;
    while (target) {

        if (target->active()) {
            if (!target_was_me) {
                target->args() <<= this->switch_args;
                assert(!this->switch_args);
            }
            err = target->g_switchstack();
            break;
        }
        if (!target->started()) {
            // We never encounter a main greenlet that's not started.
            assert(!target->main());
            UserGreenlet* real_target = static_cast<UserGreenlet*>(target);
            assert(real_target);
            void* dummymarker;

            if (!target_was_me) {
                target->args() <<= this->switch_args;
                assert(!this->switch_args);
            }

            try {
                // This can only throw back to us while we're
                // still in this greenlet. Once the new greenlet
                // is bootstrapped, it has its own exception state.
                err = real_target->g_initialstub(&dummymarker);
            }
            catch (const PyErrOccurred&) {
                this->release_args();
                throw;
            }
            catch (const GreenletStartedWhileInPython&) {
                // The greenlet was started sometime before this
                // greenlet actually switched to it, i.e.,
                // "concurrent" calls to switch() or throw().
                // We need to retry the switch.
                // Note that the current greenlet has been reset
                // to this one (or we wouldn't be running!)
                continue;
            }
            break;
        }

        target = target->parent();
        target_was_me = false;
    }
    // The this pointer and all other stack or register based
    // variables are invalid now, at least where things succeed
    // above.
    // But this one, probably not so much? It's not clear if it's
    // safe to throw an exception at this point.

    if (err.status < 0) {
        // XXX: This code path is untested.
        assert(PyErr_Occurred());
        assert(!err.the_state_that_switched);
        assert(!err.origin_greenlet);
        return OwnedObject();
    }

    return err.the_state_that_switched->g_switch_finish(err);
}

OwnedObject
MainGreenlet::g_switch()
{
    try {
        this->check_switch_allowed();
    }
    catch(const PyErrOccurred&) {
        this->release_args();
        throw;
    }

    switchstack_result_t err = this->g_switchstack();
    if (err.status < 0) {
        // XXX: This code path is untested.
        assert(PyErr_Occurred());
        assert(!err.the_state_that_switched);
        assert(!err.origin_greenlet);
        return OwnedObject();
    }

    return err.the_state_that_switched->g_switch_finish(err);
}


OwnedGreenlet
Greenlet::g_switchstack_success() G_NOEXCEPT
{
    PyThreadState* tstate = PyThreadState_GET();
    // restore the saved state
    this->python_state >> tstate;
    this->exception_state >> tstate;

    // The thread state hasn't been changed yet.
    ThreadState* thread_state = this->thread_state();
    OwnedGreenlet result(thread_state->get_current());
    thread_state->set_current(this->self());
    //assert(thread_state->borrow_current().borrow() == this->_self);
    return result;
}


Greenlet::switchstack_result_t
UserGreenlet::g_initialstub(void* mark)
{
    OwnedObject run;

    // We need to grab a reference to the current switch arguments
    // in case we're entered concurrently during the call to
    // GetAttr() and have to try again.
    // We'll restore them when we return in that case.
    // Scope them tightly to avoid ref leaks.
    {
        SwitchingArgs args(this->switch_args);

        /* save exception in case getattr clears it */
        PyErrPieces saved;

        /*
          self.run is the object to call in the new greenlet.
          This could run arbitrary python code and switch greenlets!
        */
        run = this->_self.PyRequireAttr(mod_globs.str_run);

        /* restore saved exception */
        saved.PyErrRestore();


        /* recheck that it's safe to switch in case greenlet reparented anywhere above */
        this->check_switch_allowed();

        /* by the time we got here another start could happen elsewhere,
         * that means it should now be a regular switch.
         * This can happen if the Python code is a subclass that implements
         * __getattribute__ or __getattr__, or makes ``run`` a descriptor;
         * all of those can run arbitrary code that switches back into
         * this greenlet.
         */
        if (this->stack_state.started()) {
            // the successful switch cleared these out, we need to
            // restore our version.
            assert(!this->switch_args);
            this->switch_args <<= args;

            throw GreenletStartedWhileInPython();
        }
    }

    // Sweet, if we got here, we have the go-ahead and will switch
    // greenlets.
    // Nothing we do from here on out should allow for a thread or
    // greenlet switch: No arbitrary calls to Python, including
    // decref'ing

#if GREENLET_USE_CFRAME
    /* OK, we need it, we're about to switch greenlets, save the state. */
    /*
      See green_new(). This is a stack-allocated variable used
      while *self* is in PyObject_Call().
      We want to defer copying the state info until we're sure
      we need it and are in a stable place to do so.
    */
    _PyCFrame trace_info;

    this->python_state.set_new_cframe(trace_info);
#endif
    /* start the greenlet */
    ThreadState& thread_state = GET_THREAD_STATE().state();
    this->stack_state = StackState(mark,
                                   thread_state.borrow_current()->stack_state);
    this->python_state.set_initial_state(PyThreadState_GET());
    this->exception_state.clear();
    this->_main_greenlet = thread_state.get_main_greenlet();

    /* perform the initial switch */
    switchstack_result_t err = this->g_switchstack();
    /* returns twice!
       The 1st time with ``err == 1``: we are in the new greenlet.
       This one owns a greenlet that used to be current.
       The 2nd time with ``err <= 0``: back in the caller's
       greenlet; this happens if the child finishes or switches
       explicitly to us. Either way, the ``err`` variable is
       created twice at the same memory location, but possibly
       having different ``origin`` values. Note that it's not
       constructed for the second time until the switch actually happens.
    */
    if (err.status == 1) {
        // This never returns! Calling inner_bootstrap steals
        // the contents of our run object within this stack frame, so
        // it is not valid to do anything with it.
        this->inner_bootstrap(err.origin_greenlet, run);
        Py_FatalError("greenlet: inner_bootstrap returned\n");
    }
    // The child will take care of decrefing this.
    run.relinquish_ownership();

    // In contrast, notice that we're keeping the origin greenlet
    // around as an owned reference; we need it to call the trace
    // function for the switch back into the parent. It was only
    // captured at the time the switch actually happened, though,
    // so we haven't been keeping an extra reference around this
    // whole time.

    /* back in the parent */
    if (err.status < 0) {
        /* start failed badly, restore greenlet state */
        // XXX: This code path is not tested.
        this->stack_state = StackState();
        this->_main_greenlet.CLEAR();
        fprintf(stderr, "greenlet: g_initialstub: starting child failed.\n");
    }
    return err;
}


void
UserGreenlet::inner_bootstrap(OwnedGreenlet& origin_greenlet, OwnedObject& _run) G_NOEXCEPT_WIN32
{
    // The arguments here would be another great place for move.
    // As it is, we take them as a reference so that when we clear
    // them we clear what's on the stack above us. Do that NOW, and
    // without using a C++ RAII object,
    // so there's no way that exiting the parent frame can clear it,
    // or we clear it unexpectedly. This arises in the context of the
    // interpreter shutting down. See https://github.com/python-greenlet/greenlet/issues/325
    PyObject* run = _run.relinquish_ownership();

    /* in the new greenlet */
    assert(this->thread_state()->borrow_current() == this->_self);
    // C++ exceptions cannot propagate to the parent greenlet from
    // here. (TODO: Do we need a catch(...) clause, perhaps on the
    // function itself? ALl we could do is terminate the program.)
    // NOTE: On 32-bit Windows, the call chain is extremely
    // important here in ways that are subtle, having to do with
    // the depth of the SEH list. The call to restore it MUST NOT
    // add a new SEH handler to the list, or we'll restore it to
    // the wrong thing.
    this->thread_state()->restore_exception_state();
    /* stack variables from above are no good and also will not unwind! */
    // EXCEPT: That can't be true, we access run, among others, here.

    this->stack_state.set_active(); /* running */

    // XXX: We could clear this much earlier, right?
    // Or would that introduce the possibility of running Python
    // code when we don't want to?
    this->_run_callable.CLEAR();


    // We're about to possibly run Python code again, which
    // could switch back to us, so we need to grab the
    // arguments locally.
    SwitchingArgs args;
    args <<= this->switch_args;
    assert(!this->switch_args);

    // The first switch we need to manually call the trace
    // function here instead of in g_switch_finish, because we
    // never return there.

    if (OwnedObject tracefunc = this->thread_state()->get_tracefunc()) {
        try {
            g_calltrace(tracefunc,
                        args ? mod_globs.event_switch : mod_globs.event_throw,
                        origin_greenlet,
                        this->_self);
        }
        catch (const PyErrOccurred&) {
            /* Turn trace errors into switch throws */
            args.CLEAR();
        }
    }

    // We no longer need the origin, it was only here for
    // tracing.
    // We may never actually exit this stack frame so we need
    // to explicitly clear it.
    // This could run Python code and switch.
    origin_greenlet.CLEAR();

    OwnedObject result;
    if (!args) {
        /* pending exception */
        result = NULL;
    }
    else {
        /* call g.run(*args, **kwargs) */
        // This could result in further switches
        try {
            //result = run.PyCall(args.args(), args.kwargs());
            result = OwnedObject::consuming(PyObject_Call(run, args.args().borrow(), args.kwargs().borrow()));
        }
        catch(...) {
            // Unhandled C++ exception!

            // If we declare ourselves as noexcept, if we don't catch
            // this here, most platforms will just abort() the
            // process. But on 64-bit Windows with older versions of
            // the C runtime, this can actually corrupt memory and
            // just return. We see this when compiling with the
            // Windows 7.0 SDK targeting Windows Server 2008, but not
            // when using the Appveyor Visual Studio 2019 image. So
            // this currently only affects Python 2.7 on Windows 64.
            // That is, the tests pass and the runtime aborts
            // everywhere else.
            //
            // However, if we catch it and try to continue with a
            // Python error, then all Windows 64 bit platforms corrupt
            // memory. So all we can do is manually abort, hopefully
            // with a good error message. (Note that the above was
            // tested WITHOUT the `/EHr` switch being used at compile
            // time, so MSVC may have "optimized" out important
            // checking. Using that switch, we may be in a better
            // place in terms of memory corruption.) But sometimes it
            // can't be caught here at all, which is confusing but not
            // terribly surprising; so again, the G_NOEXCEPT_WIN32
            // plus "/EHr".
            //
            // Hopefully the basic C stdlib is still functional enough
            // for us to at least print an error.
            //
            // It gets more complicated than that, though, on some
            // platforms, specifically at least Linux/gcc/libstdc++. They use
            // an exception to unwind the stack when a background
            // thread exits. (See comments about G_NOEXCEPT.) So this
            // may not actually represent anything untoward. On those
            // platforms we allow throws of this to propagate, or
            // attempt to anyway.
# if defined(WIN32) || defined(_WIN32)
            Py_FatalError(
                "greenlet: Unhandled C++ exception from a greenlet run function. "
                "Because memory is likely corrupted, terminating process.");
            std::abort();
#else
            throw;
#endif
        }
    }
    args.CLEAR();
    Py_CLEAR(run);

    if (!result
        && mod_globs.PyExc_GreenletExit.PyExceptionMatches()
        && (this->switch_args)) {
        // This can happen, for example, if our only reference
        // goes away after we switch back to the parent.
        // See test_dealloc_switch_args_not_lost
        PyErrPieces clear_error;
        result <<= this->switch_args;
        result = single_result(result);
    }
    this->release_args();
    this->python_state.did_finish(PyThreadState_GET());

    result = g_handle_exit(result);
    assert(this->thread_state()->borrow_current() == this->_self);

    /* jump back to parent */
    this->stack_state.set_inactive(); /* dead */


    // TODO: Can we decref some things here? Release our main greenlet
    // and maybe parent?
    for (Greenlet* parent = this->_parent;
         parent;
         parent = parent->parent()) {
        // We need to somewhere consume a reference to
        // the result; in most cases we'll never have control
        // back in this stack frame again. Calling
        // green_switch actually adds another reference!
        // This would probably be clearer with a specific API
        // to hand results to the parent.
        parent->args() <<= result;
        assert(!result);
        // The parent greenlet now owns the result; in the
        // typical case we'll never get back here to assign to
        // result and thus release the reference.
        try {
            result = parent->g_switch();
        }
        catch (const PyErrOccurred&) {
            // Ignore.
        }

        /* Return here means switch to parent failed,
         * in which case we throw *current* exception
         * to the next parent in chain.
         */
        assert(!result);
    }
    /* We ran out of parents, cannot continue */
    PyErr_WriteUnraisable(this->self().borrow_o());
    Py_FatalError("greenlet: ran out of parent greenlets while propagating exception; "
                  "cannot continue");
    std::abort();
}


Greenlet::switchstack_result_t
Greenlet::g_switchstack(void)
{
    { /* save state */
        if (this->thread_state()->is_current(this->self())) {
            // Hmm, nothing to do.
            // TODO: Does this bypass trace events that are
            // important?
            return switchstack_result_t(0,
                                        this, this->thread_state()->borrow_current());
        }
        BorrowedGreenlet current = this->thread_state()->borrow_current();
        PyThreadState* tstate = PyThreadState_GET();
        current->python_state << tstate;
        current->exception_state << tstate;
        this->python_state.will_switch_from(tstate);
        switching_thread_state = this;
    }
    // If this is the first switch into a greenlet, this will
    // return twice, once with 1 in the new greenlet, once with 0
    // in the origin.
    int err = slp_switch();

    if (err < 0) { /* error */
        // XXX: This code path is not tested.
        BorrowedGreenlet current(GET_THREAD_STATE().state().borrow_current());
        //current->top_frame = NULL; // This probably leaks?
        current->exception_state.clear();

        switching_thread_state = nullptr;
        //GET_THREAD_STATE().state().wref_target(NULL);
        this->release_args();
        // It's important to make sure not to actually return an
        // owned greenlet here, no telling how long before it
        // could be cleaned up.
        // TODO: Can this be a throw? How stable is the stack in
        // an error case like this?
        return switchstack_result_t(err);
    }

    // No stack-based variables are valid anymore.

    // But the global is volatile so we can reload it without the
    // compiler caching it from earlier.
    Greenlet* after_switch = switching_thread_state;
    OwnedGreenlet origin = after_switch->g_switchstack_success();
    switching_thread_state = nullptr;
    return switchstack_result_t(err, after_switch, origin);
}


inline void
Greenlet::check_switch_allowed() const
{
    // TODO: Make this take a parameter of the current greenlet,
    // or current main greenlet, to make the check for
    // cross-thread switching cheaper. Surely somewhere up the
    // call stack we've already accessed the thread local variable.

    // We expect to always have a main greenlet now; accessing the thread state
    // created it. However, if we get here and cleanup has already
    // begun because we're a greenlet that was running in a
    // (now dead) thread, these invariants will not hold true. In
    // fact, accessing `this->thread_state` may not even be possible.

    // If the thread this greenlet was running in is dead,
    // we'll still have a reference to a main greenlet, but the
    // thread state pointer we have is bogus.
    // TODO: Give the objects an API to determine if they belong
    // to a dead thread.

    const BorrowedMainGreenlet main_greenlet = this->find_main_greenlet_in_lineage();

    if (!main_greenlet) {
        throw PyErrOccurred(mod_globs.PyExc_GreenletError,
                            "cannot switch to a garbage collected greenlet");
    }

    if (!main_greenlet->thread_state()) {
        throw PyErrOccurred(mod_globs.PyExc_GreenletError,
                            "cannot switch to a different thread (which happens to have exited)");
    }

    // The main greenlet we found was from the .parent lineage.
    // That may or may not have any relationship to the main
    // greenlet of the running thread. We can't actually access
    // our this->thread_state members to try to check that,
    // because it could be in the process of getting destroyed,
    // but setting the main_greenlet->thread_state member to NULL
    // may not be visible yet. So we need to check against the
    // current thread state (once the cheaper checks are out of
    // the way)
    const BorrowedMainGreenlet current_main_greenlet = GET_THREAD_STATE().state().borrow_main_greenlet();
    if (
        // lineage main greenlet is not this thread's greenlet
        current_main_greenlet != main_greenlet
        || (
            // atteched to some thread
            this->main_greenlet()
            // XXX: Same condition as above. Was this supposed to be
            // this->main_greenlet()?
            && current_main_greenlet != main_greenlet)
        // switching into a known dead thread (XXX: which, if we get here,
        // is bad, because we just accessed the thread state, which is
        // gone!)
        || (!current_main_greenlet->thread_state())) {
        throw PyErrOccurred(mod_globs.PyExc_GreenletError,
                            "cannot switch to a different thread");
    }
}


OwnedObject
Greenlet::g_switch_finish(const switchstack_result_t& err)
{

    ThreadState& state = *this->thread_state();
    try {
        // Our only caller handles the bad error case
        assert(err.status >= 0);
        assert(state.borrow_current() == this->self());

        if (OwnedObject tracefunc = state.get_tracefunc()) {
            g_calltrace(tracefunc,
                        this->args() ? mod_globs.event_switch : mod_globs.event_throw,
                        err.origin_greenlet,
                        this->self());
        }
        // The above could have invoked arbitrary Python code, but
        // it couldn't switch back to this object and *also*
        // throw an exception, so the args won't have changed.

        if (PyErr_Occurred()) {
            // We get here if we fell of the end of the run() function
            // raising an exception. The switch itself was
            // successful, but the function raised.
            // valgrind reports that memory allocated here can still
            // be reached after a test run.
            throw PyErrOccurred();
        }

        OwnedObject result;
        result <<= this->switch_args;
        assert(!this->switch_args);
        return result;
    }
    catch (const PyErrOccurred&) {
        /* Turn switch errors into switch throws */
        /* Turn trace errors into switch throws */
        this->release_args();
        throw;
    }
}


greenlet::PythonAllocator<UserGreenlet> UserGreenlet::allocator;
greenlet::PythonAllocator<MainGreenlet> MainGreenlet::allocator;


extern "C" {
static int GREENLET_NOINLINE(slp_save_state_trampoline)(char* stackref)
{
    return switching_thread_state->slp_save_state(stackref);
}
static void GREENLET_NOINLINE(slp_restore_state_trampoline)()
{
    switching_thread_state->slp_restore_state();
}
}



/***********************************************************/

class TracingGuard
{
private:
    PyThreadState* tstate;
public:
    TracingGuard()
        : tstate(PyThreadState_GET())
    {
        PyThreadState_EnterTracing(this->tstate);
    }

    ~TracingGuard()
    {
        PyThreadState_LeaveTracing(this->tstate);
        this->tstate = nullptr;
    }

    inline void CallTraceFunction(const OwnedObject& tracefunc,
                                  const ImmortalEventName& event,
                                  const BorrowedGreenlet& origin,
                                  const BorrowedGreenlet& target)
    {
        // TODO: This calls tracefunc(event, (origin, target)). Add a shortcut
        // function for that that's specialized to avoid the Py_BuildValue
        // string parsing, or start with just using "ON" format with PyTuple_Pack(2,
        // origin, target). That seems like what the N format is meant
        // for.
        // XXX: Why does event not automatically cast back to a PyObject?
        // It tries to call the "deleted constructor ImmortalEventName
        // const" instead.
        assert(tracefunc);
        assert(event);
        assert(origin);
        assert(target);
        NewReference retval(PyObject_CallFunction(tracefunc.borrow(),
                                             "O(OO)",
                                             event.borrow(),
                                             origin.borrow(),
                                             target.borrow()));
        if (!retval) {
            throw PyErrOccurred();
        }
    }
};

static void
g_calltrace(const OwnedObject& tracefunc,
            const ImmortalEventName& event,
            const BorrowedGreenlet& origin,
            const BorrowedGreenlet& target)
{
    PyErrPieces saved_exc;
    try {
        TracingGuard tracing_guard;
        tracing_guard.CallTraceFunction(tracefunc, event, origin, target);
    }
    catch (const PyErrOccurred&) {
        // In case of exceptions trace function is removed,
        // and any existing exception is replaced with the tracing
        // exception.
        GET_THREAD_STATE().state().set_tracefunc(Py_None);
        throw;
    }

    saved_exc.PyErrRestore();
}



static OwnedObject
g_handle_exit(const OwnedObject& greenlet_result)
{
    if (!greenlet_result && mod_globs.PyExc_GreenletExit.PyExceptionMatches()) {
        /* catch and ignore GreenletExit */
        PyErrFetchParam val;
        PyErr_Fetch(PyErrFetchParam(), val, PyErrFetchParam());
        if (!val) {
            return OwnedObject::None();
        }
        return OwnedObject(val);
    }

    if (greenlet_result) {
        // package the result into a 1-tuple
        // PyTuple_Pack increments the reference of its arguments,
        // so we always need to decref the greenlet result;
        // the owner will do that.
        return OwnedObject::consuming(PyTuple_Pack(1, greenlet_result.borrow()));
    }

    return OwnedObject();
}



/***********************************************************/

static PyGreenlet*
green_new(PyTypeObject* type, PyObject* UNUSED(args), PyObject* UNUSED(kwds))
{
    PyGreenlet* o =
        (PyGreenlet*)PyBaseObject_Type.tp_new(type, mod_globs.empty_tuple, mod_globs.empty_dict);
    if (o) {
        new UserGreenlet(o, GET_THREAD_STATE().state().borrow_current());
        assert(Py_REFCNT(o) == 1);
    }
    return o;
}

static int
green_setrun(BorrowedGreenlet self, BorrowedObject nrun, void* c);
static int
green_setparent(BorrowedGreenlet self, BorrowedObject nparent, void* c);

static int
green_init(BorrowedGreenlet self, BorrowedObject args, BorrowedObject kwargs)
{
    PyArgParseParam run;
    PyArgParseParam nparent;
    static const char* const kwlist[] = {
        "run",
        "parent",
        NULL
    };

    // recall: The O specifier does NOT increase the reference count.
    if (!PyArg_ParseTupleAndKeywords(
             args, kwargs, "|OO:green", (char**)kwlist, &run, &nparent)) {
        return -1;
    }

    if (run) {
        if (green_setrun(self, run, NULL)) {
            return -1;
        }
    }
    if (nparent && !nparent.is_None()) {
        return green_setparent(self, nparent, NULL);
    }
    return 0;
}


UserGreenlet::ParentIsCurrentGuard::ParentIsCurrentGuard(UserGreenlet* p,
                                                     const ThreadState& thread_state)
    : oldparent(p->_parent),
      greenlet(p)
{
    p->_parent = thread_state.get_current();
}

UserGreenlet::ParentIsCurrentGuard::~ParentIsCurrentGuard()
{
    this->greenlet->_parent = oldparent;
    oldparent.CLEAR();
}


void
Greenlet::murder_in_place()
{
    if (this->active()) {
        assert(!this->is_currently_running_in_some_thread());
        this->deactivate_and_free();
    }
}

void
UserGreenlet::murder_in_place()
{
    this->_main_greenlet.CLEAR();
    Greenlet::murder_in_place();
}

inline void
Greenlet::deactivate_and_free()
{
    if (!this->active()) {
        return;
    }
    // Throw away any saved stack.
    this->stack_state = StackState();
    assert(!this->stack_state.active());
    // Throw away any Python references.
    // We're holding a borrowed reference to the last
    // frame we executed. Since we borrowed it, the
    // normal traversal, clear, and dealloc functions
    // ignore it, meaning it leaks. (The thread state
    // object can't find it to clear it when that's
    // deallocated either, because by definition if we
    // got an object on this list, it wasn't
    // running and the thread state doesn't have
    // this frame.)
    // So here, we *do* clear it.
    this->python_state.tp_clear(true);
}

bool
Greenlet::belongs_to_thread(const ThreadState* thread_state) const
{
    if (!this->thread_state() // not running anywhere, or thread
                              // exited
        || !thread_state) { // same, or there is no thread state.
        return false;
    }
    return true;
}

bool
UserGreenlet::belongs_to_thread(const ThreadState* thread_state) const
{
    return Greenlet::belongs_to_thread(thread_state) && this->_main_greenlet == thread_state->borrow_main_greenlet();
}

void
Greenlet::deallocing_greenlet_in_thread(const ThreadState* current_thread_state)
{
    /* Cannot raise an exception to kill the greenlet if
       it is not running in the same thread! */
    if (this->belongs_to_thread(current_thread_state)) {
        assert(current_thread_state);
        // To get here it had to have run before
        /* Send the greenlet a GreenletExit exception. */

        // We don't care about the return value, only whether an
        // exception happened.
        this->throw_GreenletExit_during_dealloc(*current_thread_state);
        return;
    }

    // Not the same thread! Temporarily save the greenlet
    // into its thread's deleteme list, *if* it exists.
    // If that thread has already exited, and processed its pending
    // cleanup, we'll never be able to clean everything up: we won't
    // be able to raise an exception.
    // That's mostly OK! Since we can't add it to a list, our refcount
    // won't increase, and we'll go ahead with the DECREFs later.
    ThreadState *const  thread_state = this->thread_state();
    if (thread_state) {
        thread_state->delete_when_thread_running(this->self());
    }
    else {
        // The thread is dead, we can't raise an exception.
        // We need to make it look non-active, though, so that dealloc
        // finishes killing it.
        this->deactivate_and_free();
    }
    return;
}


int
Greenlet::tp_traverse(visitproc visit, void* arg)
{

    int result;
    if ((result = this->exception_state.tp_traverse(visit, arg)) != 0) {
        return result;
    }
    //XXX: This is ugly. But so is handling everything having to do
    //with the top frame.
    bool visit_top_frame = this->was_running_in_dead_thread();
    // When true, the thread is dead. Our implicit weak reference to the
    // frame is now all that's left; we consider ourselves to
    // strongly own it now.
    if ((result = this->python_state.tp_traverse(visit, arg, visit_top_frame)) != 0) {
        return result;
    }
    return 0;
}

int
UserGreenlet::tp_traverse(visitproc visit, void* arg)
{
    Py_VISIT(this->_parent.borrow_o());
    Py_VISIT(this->_main_greenlet.borrow_o());
    Py_VISIT(this->_run_callable.borrow_o());

    return Greenlet::tp_traverse(visit, arg);
}

int
MainGreenlet::tp_traverse(visitproc visit, void* arg)
{
    if (this->_thread_state) {
        // we've already traversed main, (self), don't do it again.
        int result = this->_thread_state->tp_traverse(visit, arg, false);
        if (result) {
            return result;
        }
    }
    return Greenlet::tp_traverse(visit, arg);
}

static int
green_traverse(PyGreenlet* self, visitproc visit, void* arg)
{
    // We must only visit referenced objects, i.e. only objects
    // Py_INCREF'ed by this greenlet (directly or indirectly):
    //
    // - stack_prev is not visited: holds previous stack pointer, but it's not
    //    referenced
    // - frames are not visited as we don't strongly reference them;
    //    alive greenlets are not garbage collected
    //    anyway. This can be a problem, however, if this greenlet is
    //    never allowed to finish, and is referenced from the frame: we
    //    have an uncollectible cycle in that case. Note that the
    //    frame object itself is also frequently not even tracked by the GC
    //    starting with Python 3.7 (frames are allocated by the
    //    interpreter untracked, and only become tracked when their
    //    evaluation is finished if they have a refcount > 1). All of
    //    this is to say that we should probably strongly reference
    //    the frame object. Doing so, while always allowing GC on a
    //    greenlet, solves several leaks for us.

    Py_VISIT(self->dict);
    if (!self->pimpl) {
        // Hmm. I have seen this at interpreter shutdown time,
        // I think. That's very odd because this doesn't go away until
        // we're ``green_dealloc()``, at which point we shouldn't be
        // traversed anymore.
        return 0;
    }

    return self->pimpl->tp_traverse(visit, arg);
}

static int
green_is_gc(BorrowedGreenlet self)
{
    int result = 0;
    /* Main greenlet can be garbage collected since it can only
       become unreachable if the underlying thread exited.
       Active greenlets --- including those that are suspended ---
       cannot be garbage collected, however.
    */
    if (self->main() || !self->active()) {
        result = 1;
    }
    // The main greenlet pointer will eventually go away after the thread dies.
    if (self->was_running_in_dead_thread()) {
        // Our thread is dead! We can never run again. Might as well
        // GC us. Note that if a tuple containing only us and other
        // immutable objects had been scanned before this, when we
        // would have returned 0, the tuple will take itself out of GC
        // tracking and never be investigated again. So that could
        // result in both us and the tuple leaking due to an
        // unreachable/uncollectible reference. The same goes for
        // dictionaries.
        //
        // It's not a great idea to be changing our GC state on the
        // fly.
        result = 1;
    }
    return result;
}


int
Greenlet::tp_clear()
{
    bool own_top_frame = this->was_running_in_dead_thread();
    this->exception_state.tp_clear();
    this->python_state.tp_clear(own_top_frame);
    return 0;
}

int
UserGreenlet::tp_clear()
{
    Greenlet::tp_clear();
    this->_parent.CLEAR();
    this->_main_greenlet.CLEAR();
    this->_run_callable.CLEAR();
    return 0;
}


static int
green_clear(PyGreenlet* self)
{
    /* Greenlet is only cleared if it is about to be collected.
       Since active greenlets are not garbage collectable, we can
       be sure that, even if they are deallocated during clear,
       nothing they reference is in unreachable or finalizers,
       so even if it switches we are relatively safe. */
    // XXX: Are we responsible for clearing weakrefs here?
    Py_CLEAR(self->dict);
    return self->pimpl->tp_clear();
}

/**
 * Returns 0 on failure (the object was resurrected) or 1 on success.
 **/
static int
_green_dealloc_kill_started_non_main_greenlet(BorrowedGreenlet self)
{
    /* Hacks hacks hacks copied from instance_dealloc() */
    /* Temporarily resurrect the greenlet. */
    assert(self.REFCNT() == 0);
    Py_SET_REFCNT(self.borrow(), 1);
    /* Save the current exception, if any. */
    PyErrPieces saved_err;
    try {
        // BY THE TIME WE GET HERE, the state may actually be going
        // away
        // if we're shutting down the interpreter and freeing thread
        // entries,
        // this could result in freeing greenlets that were leaked. So
        // we can't try to read the state.
        self->deallocing_greenlet_in_thread(
              self->thread_state()
              ? static_cast<ThreadState*>(GET_THREAD_STATE())
              : nullptr);
    }
    catch (const PyErrOccurred&) {
        PyErr_WriteUnraisable(self.borrow_o());
        /* XXX what else should we do? */
    }
    /* Check for no resurrection must be done while we keep
     * our internal reference, otherwise PyFile_WriteObject
     * causes recursion if using Py_INCREF/Py_DECREF
     */
    if (self.REFCNT() == 1 && self->active()) {
        /* Not resurrected, but still not dead!
           XXX what else should we do? we complain. */
        PyObject* f = PySys_GetObject("stderr");
        Py_INCREF(self.borrow_o()); /* leak! */
        if (f != NULL) {
            PyFile_WriteString("GreenletExit did not kill ", f);
            PyFile_WriteObject(self.borrow_o(), f, 0);
            PyFile_WriteString("\n", f);
        }
    }
    /* Restore the saved exception. */
    saved_err.PyErrRestore();
    /* Undo the temporary resurrection; can't use DECREF here,
     * it would cause a recursive call.
     */
    assert(self.REFCNT() > 0);

    Py_ssize_t refcnt = self.REFCNT() - 1;
    Py_SET_REFCNT(self.borrow_o(), refcnt);
    if (refcnt != 0) {
        /* Resurrected! */
        _Py_NewReference(self.borrow_o());
        Py_SET_REFCNT(self.borrow_o(), refcnt);
        /* Better to use tp_finalizer slot (PEP 442)
         * and call ``PyObject_CallFinalizerFromDealloc``,
         * but that's only supported in Python 3.4+; see
         * Modules/_io/iobase.c for an example.
         *
         * The following approach is copied from iobase.c in CPython 2.7.
         * (along with much of this function in general). Here's their
         * comment:
         *
         * When called from a heap type's dealloc, the type will be
         * decref'ed on return (see e.g. subtype_dealloc in typeobject.c). */
        if (PyType_HasFeature(self.TYPE(), Py_TPFLAGS_HEAPTYPE)) {
            Py_INCREF(self.TYPE());
        }

        PyObject_GC_Track((PyObject*)self);

        _Py_DEC_REFTOTAL;
#ifdef COUNT_ALLOCS
        --Py_TYPE(self)->tp_frees;
        --Py_TYPE(self)->tp_allocs;
#endif /* COUNT_ALLOCS */
        return 0;
    }
    return 1;
}


Greenlet::~Greenlet()
{
    // XXX: Can't do this. tp_clear is a virtual function, and by the
    // time we're here, we've sliced off our child classes.
    //this->tp_clear();
}

UserGreenlet::~UserGreenlet()
{
    // Python 3.11: If we don't clear out the raw frame datastack
    // when deleting an unfinished greenlet,
    // TestLeaks.test_untracked_memory_doesnt_increase_unfinished_thread_dealloc_in_main fails.
    this->python_state.did_finish(nullptr);
    this->tp_clear();
}

MainGreenlet::~MainGreenlet()
{
    total_main_greenlets--;
    this->tp_clear();
}

static void
green_dealloc(PyGreenlet* self)
{
    PyObject_GC_UnTrack(self);
    BorrowedGreenlet me(self);
    if (me->active()
        && me->started()
        && !me->main()) {
        if (!_green_dealloc_kill_started_non_main_greenlet(me)) {
            return;
        }
    }

    if (self->weakreflist != NULL) {
        PyObject_ClearWeakRefs((PyObject*)self);
    }
    Py_CLEAR(self->dict);

    if (self->pimpl) {
        // In case deleting this, which frees some memory,
        // somehow winds up calling back into us. That's usually a
        //bug in our code.
        Greenlet* p = self->pimpl;
        self->pimpl = nullptr;
        delete p;
    }
    // and finally we're done. self is now invalid.
    Py_TYPE(self)->tp_free((PyObject*)self);
}



static OwnedObject
throw_greenlet(BorrowedGreenlet self, PyErrPieces& err_pieces)
{
    PyObject* result = nullptr;
    err_pieces.PyErrRestore();
    assert(PyErr_Occurred());
    if (self->started() && !self->active()) {
        /* dead greenlet: turn GreenletExit into a regular return */
        result = g_handle_exit(OwnedObject()).relinquish_ownership();
    }

    self->args() <<= result;

    return single_result(self->g_switch());
}



PyDoc_STRVAR(
    green_switch_doc,
    "switch(*args, **kwargs)\n"
    "\n"
    "Switch execution to this greenlet.\n"
    "\n"
    "If this greenlet has never been run, then this greenlet\n"
    "will be switched to using the body of ``self.run(*args, **kwargs)``.\n"
    "\n"
    "If the greenlet is active (has been run, but was switch()'ed\n"
    "out before leaving its run function), then this greenlet will\n"
    "be resumed and the return value to its switch call will be\n"
    "None if no arguments are given, the given argument if one\n"
    "argument is given, or the args tuple and keyword args dict if\n"
    "multiple arguments are given.\n"
    "\n"
    "If the greenlet is dead, or is the current greenlet then this\n"
    "function will simply return the arguments using the same rules as\n"
    "above.\n");

static PyObject*
green_switch(PyGreenlet* self, PyObject* args, PyObject* kwargs)
{
    using greenlet::SwitchingArgs;
    SwitchingArgs switch_args(OwnedObject::owning(args), OwnedObject::owning(kwargs));
    self->pimpl->args() <<= switch_args;


    // If we're switching out of a greenlet, and that switch is the
    // last thing the greenlet does, the greenlet ought to be able to
    // go ahead and die at that point. Currently, someone else must
    // manually switch back to the greenlet so that we "fall off the
    // end" and can perform cleanup. You'd think we'd be able to
    // figure out that this is happening using the frame's ``f_lasti``
    // member, which is supposed to be an index into
    // ``frame->f_code->co_code``, the bytecode string. However, in
    // recent interpreters, ``f_lasti`` tends not to be updated thanks
    // to things like the PREDICT() macros in ceval.c. So it doesn't
    // really work to do that in many cases. For example, the Python
    // code:
    //     def run():
    //         greenlet.getcurrent().parent.switch()
    // produces bytecode of len 16, with the actual call to switch()
    // being at index 10 (in Python 3.10). However, the reported
    // ``f_lasti`` we actually see is...5! (Which happens to be the
    // second byte of the CALL_METHOD op for ``getcurrent()``).

    try {
        OwnedObject result = single_result(self->pimpl->g_switch());
#ifndef NDEBUG
        // Note that the current greenlet isn't necessarily self. If self
        // finished, we went to one of its parents.
        assert(!self->pimpl->args());

        const BorrowedGreenlet& current = GET_THREAD_STATE().state().borrow_current();
        // It's possible it's never been switched to.
        assert(!current->args());
#endif
        return result.relinquish_ownership();
    }
    catch(const PyErrOccurred&) {
        return nullptr;
    }
}

PyDoc_STRVAR(
    green_throw_doc,
    "Switches execution to this greenlet, but immediately raises the\n"
    "given exception in this greenlet.  If no argument is provided, the "
    "exception\n"
    "defaults to `greenlet.GreenletExit`.  The normal exception\n"
    "propagation rules apply, as described for `switch`.  Note that calling "
    "this\n"
    "method is almost equivalent to the following::\n"
    "\n"
    "    def raiser():\n"
    "        raise typ, val, tb\n"
    "    g_raiser = greenlet(raiser, parent=g)\n"
    "    g_raiser.switch()\n"
    "\n"
    "except that this trick does not work for the\n"
    "`greenlet.GreenletExit` exception, which would not propagate\n"
    "from ``g_raiser`` to ``g``.\n");

static PyObject*
green_throw(PyGreenlet* self, PyObject* args)
{
    PyArgParseParam typ(mod_globs.PyExc_GreenletExit);
    PyArgParseParam val;
    PyArgParseParam tb;

    if (!PyArg_ParseTuple(args, "|OOO:throw", &typ, &val, &tb)) {
        return NULL;
    }

    try {
        // Both normalizing the error and the actual throw_greenlet
        // could throw PyErrOccurred.
        PyErrPieces err_pieces(typ.borrow(), val.borrow(), tb.borrow());

        return throw_greenlet(self, err_pieces).relinquish_ownership();
    }
    catch (const PyErrOccurred&) {
        return nullptr;
    }
}

static int
green_bool(PyGreenlet* self)
{
    return self->pimpl->active();
}

static PyObject*
green_getdict(PyGreenlet* self, void* UNUSED(context))
{
    if (self->dict == NULL) {
        self->dict = PyDict_New();
        if (self->dict == NULL) {
            return NULL;
        }
    }
    Py_INCREF(self->dict);
    return self->dict;
}

static int
green_setdict(PyGreenlet* self, PyObject* val, void* UNUSED(context))
{
    PyObject* tmp;

    if (val == NULL) {
        PyErr_SetString(PyExc_TypeError, "__dict__ may not be deleted");
        return -1;
    }
    if (!PyDict_Check(val)) {
        PyErr_SetString(PyExc_TypeError, "__dict__ must be a dictionary");
        return -1;
    }
    tmp = self->dict;
    Py_INCREF(val);
    self->dict = val;
    Py_XDECREF(tmp);
    return 0;
}

static bool
_green_not_dead(BorrowedGreenlet self)
{
    // XXX: Where else should we do this?
    // Probably on entry to most Python-facing functions?
    if (self->was_running_in_dead_thread()) {
        self->deactivate_and_free();
        return false;
    }
    return self->active() || !self->started();
}


static PyObject*
green_getdead(BorrowedGreenlet self, void* UNUSED(context))
{
    if (_green_not_dead(self)) {
        Py_RETURN_FALSE;
    }
    else {
        Py_RETURN_TRUE;
    }
}

static PyObject*
green_get_stack_saved(PyGreenlet* self, void* UNUSED(context))
{
    return PyLong_FromSsize_t(self->pimpl->stack_saved());
}


static PyObject*
green_getrun(BorrowedGreenlet self, void* UNUSED(context))
{
    try {
        OwnedObject result(self->run());
        return result.relinquish_ownership();
    }
    catch(const PyErrOccurred&) {
        return nullptr;
    }
}

void
UserGreenlet::run(const BorrowedObject nrun)
{
    if (this->started()) {
        throw AttributeError(
                        "run cannot be set "
                        "after the start of the greenlet");
    }
    this->_run_callable = nrun;
}

const OwnedObject&
MainGreenlet::run() const
{
    throw AttributeError("Main greenlets do not have a run attribute.");
}

void
MainGreenlet::run(const BorrowedObject UNUSED(nrun))
{
   throw AttributeError("Main greenlets do not have a run attribute.");
}

static int
green_setrun(BorrowedGreenlet self, BorrowedObject nrun, void* UNUSED(context))
{
    try {
        self->run(nrun);
        return 0;
    }
    catch(const PyErrOccurred&) {
        return -1;
    }
}

static PyObject*
green_getparent(BorrowedGreenlet self, void* UNUSED(context))
{
    return self->parent().acquire_or_None();
}

using greenlet::AttributeError;

const OwnedGreenlet
UserGreenlet::parent() const
{
    return this->_parent;
}

void
UserGreenlet::parent(const BorrowedObject raw_new_parent)
{
    if (!raw_new_parent) {
        throw AttributeError("can't delete attribute");
    }

    BorrowedMainGreenlet main_greenlet_of_new_parent;
    BorrowedGreenlet new_parent(raw_new_parent.borrow()); // could
                                                          // throw
                                                          // TypeError!
    for (BorrowedGreenlet p = new_parent; p; p = p->parent()) {
        if (p == this->_self) {
            throw ValueError("cyclic parent chain");
        }
        main_greenlet_of_new_parent = p->main_greenlet();
    }

    if (!main_greenlet_of_new_parent) {
        throw ValueError("parent must not be garbage collected");
    }

    if (this->started()
        && this->_main_greenlet != main_greenlet_of_new_parent) {
        throw ValueError("parent cannot be on a different thread");
    }

    this->_parent = new_parent;
}

void
MainGreenlet::parent(const BorrowedObject raw_new_parent)
{
    if (!raw_new_parent) {
        throw AttributeError("can't delete attribute");
    }
    throw AttributeError("cannot set the parent of a main greenlet");
}

const OwnedGreenlet
MainGreenlet::parent() const
{
    return OwnedGreenlet(); // null becomes None
}

static int
green_setparent(BorrowedGreenlet self, BorrowedObject nparent, void* UNUSED(context))
{
    try {
        self->parent(nparent);
    }
    catch(const PyErrOccurred&) {
        return -1;
    }
    return 0;
}

#ifdef Py_CONTEXT_H
#    define GREENLET_NO_CONTEXTVARS_REASON "This build of greenlet"
#else
#    define GREENLET_NO_CONTEXTVARS_REASON "This Python interpreter"
#endif

namespace greenlet
{

template<>
const OwnedObject
Greenlet::context<GREENLET_WHEN_PY37>(GREENLET_WHEN_PY37::Yes) const
{
    using greenlet::PythonStateContext;
    OwnedObject result;

    if (this->is_currently_running_in_some_thread()) {
        /* Currently running greenlet: context is stored in the thread state,
           not the greenlet object. */
        if (GET_THREAD_STATE().state().is_current(this->self())) {
            result = PythonStateContext<G_IS_PY37>::context(PyThreadState_GET());
        }
        else {
            throw ValueError(
                            "cannot get context of a "
                            "greenlet that is running in a different thread");
        }
    }
    else {
        /* Greenlet is not running: just return context. */
        result = this->python_state.context();
    }
    if (!result) {
        result = OwnedObject::None();
    }
    return result;
}

template<>
const OwnedObject
Greenlet::context<GREENLET_WHEN_NOT_PY37>(GREENLET_WHEN_NOT_PY37::No) const
{
    throw AttributeError(
                         GREENLET_NO_CONTEXTVARS_REASON
                         "does not support context variables"
    );
}

template<>
void Greenlet::context<GREENLET_WHEN_PY37>(BorrowedObject given, GREENLET_WHEN_PY37::Yes)
{
    using greenlet::PythonStateContext;
    if (!given) {
        throw AttributeError("can't delete context attribute");
    }
    if (given.is_None()) {
        /* "Empty context" is stored as NULL, not None. */
        given = nullptr;
    }

    //checks type, incrs refcnt
    greenlet::refs::OwnedContext context(given);
    PyThreadState* tstate = PyThreadState_GET();

    if (this->is_currently_running_in_some_thread()) {
        if (!GET_THREAD_STATE().state().is_current(this->self())) {
            throw ValueError("cannot set context of a greenlet"
                             " that is running in a different thread");
        }

        /* Currently running greenlet: context is stored in the thread state,
           not the greenlet object. */
        OwnedObject octx = OwnedObject::consuming(PythonStateContext<G_IS_PY37>::context(tstate));
        PythonStateContext<G_IS_PY37>::context(tstate, context.relinquish_ownership());
    }
    else {
        /* Greenlet is not running: just set context. Note that the
           greenlet may be dead.*/
        this->python_state.context() = context;
    }
}

template<>
void
Greenlet::context<GREENLET_WHEN_NOT_PY37>(BorrowedObject UNUSED(given), GREENLET_WHEN_NOT_PY37::No)
{
    throw AttributeError(
                         GREENLET_NO_CONTEXTVARS_REASON
                         "does not support context variables"
    );
}

};

static PyObject*
green_getcontext(const PyGreenlet* self, void* UNUSED(context))
{
    const Greenlet *const g = self->pimpl;
    try {
        OwnedObject result(g->context<G_IS_PY37>());
        return result.relinquish_ownership();
    }
    catch(const PyErrOccurred&) {
        return nullptr;
    }
}

static int
green_setcontext(BorrowedGreenlet self, PyObject* nctx, void* UNUSED(context))
{
    try {
        self->context<G_IS_PY37>(nctx, G_IS_PY37::IsIt());
        return 0;
    }
    catch(const PyErrOccurred&) {
        return -1;
    }
}

#undef GREENLET_NO_CONTEXTVARS_REASON

static PyObject*
green_getframe(BorrowedGreenlet self, void* UNUSED(context))
{
    const PythonState::OwnedFrame& top_frame = self->top_frame();
    return top_frame.acquire_or_None();
}

static PyObject*
green_getstate(PyGreenlet* self)
{
    PyErr_Format(PyExc_TypeError,
                 "cannot serialize '%s' object",
                 Py_TYPE(self)->tp_name);
    return nullptr;
}

static PyObject*
green_repr(BorrowedGreenlet self)
{
    /*
      Return a string like
      <greenlet.greenlet at 0xdeadbeef [current][active started]|dead main>

      The handling of greenlets across threads is not super good.
      We mostly use the internal definitions of these terms, but they
      generally should make sense to users as well.
     */
    PyObject* result;
    int never_started = !self->started() && !self->active();

    const char* const tp_name = Py_TYPE(self)->tp_name;

    if (_green_not_dead(self)) {
        /* XXX: The otid= is almost useless because you can't correlate it to
         any thread identifier exposed to Python. We could use
         PyThreadState_GET()->thread_id, but we'd need to save that in the
         greenlet, or save the whole PyThreadState object itself.

         As it stands, its only useful for identifying greenlets from the same thread.
        */
        const char* state_in_thread;
        if (self->was_running_in_dead_thread()) {
            // The thread it was running in is dead!
            // This can happen, especially at interpreter shut down.
            // It complicates debugging output because it may be
            // impossible to access the current thread state at that
            // time. Thus, don't access the current thread state.
            state_in_thread = " (thread exited)";
        }
        else {
            state_in_thread = GET_THREAD_STATE().state().is_current(self)
                ? " current"
                : (self->started() ? " suspended" : "");
        }
        result = GNative_FromFormat(
            "<%s object at %p (otid=%p)%s%s%s%s>",
            tp_name,
            self.borrow_o(),
            self->thread_state(),
            state_in_thread,
            self->active() ? " active" : "",
            never_started ? " pending" : " started",
            self->main() ? " main" : ""
        );
    }
    else {
        result = GNative_FromFormat(
            "<%s object at %p (otid=%p) %sdead>",
            tp_name,
            self.borrow_o(),
            self->thread_state(),
            self->was_running_in_dead_thread()
            ? "(thread exited) "
            : ""
            );
    }

    return result;
}

/*****************************************************************************
 * C interface
 *
 * These are exported using the CObject API
 */
extern "C" {
static PyGreenlet*
PyGreenlet_GetCurrent(void)
{
    return GET_THREAD_STATE().state().get_current().relinquish_ownership();
}

static int
PyGreenlet_SetParent(PyGreenlet* g, PyGreenlet* nparent)
{
    return green_setparent((PyGreenlet*)g, (PyObject*)nparent, NULL);
}

static PyGreenlet*
PyGreenlet_New(PyObject* run, PyGreenlet* parent)
{
    using greenlet::refs::NewDictReference;
    // In the past, we didn't use green_new and green_init, but that
    // was a maintenance issue because we duplicated code. This way is
    // much safer, but slightly slower. If that's a problem, we could
    // refactor green_init to separate argument parsing from initialization.
    OwnedGreenlet g = OwnedGreenlet::consuming(green_new(&PyGreenlet_Type, nullptr, nullptr));
    if (!g) {
        return NULL;
    }

    try {
        NewDictReference kwargs;
        if (run) {
            kwargs.SetItem(mod_globs.str_run, run);
        }
        if (parent) {
            kwargs.SetItem("parent", (PyObject*)parent);
        }

        Require(green_init(g, mod_globs.empty_tuple, kwargs));
    }
    catch (const PyErrOccurred&) {
        return nullptr;
    }

    return g.relinquish_ownership();
}

static PyObject*
PyGreenlet_Switch(PyGreenlet* g, PyObject* args, PyObject* kwargs)
{
    PyGreenlet* self = (PyGreenlet*)g;

    if (!PyGreenlet_Check(self)) {
        PyErr_BadArgument();
        return NULL;
    }

    if (args == NULL) {
        args = mod_globs.empty_tuple;
    }

    if (kwargs == NULL || !PyDict_Check(kwargs)) {
        kwargs = NULL;
    }

    return green_switch(g, args, kwargs);
}

static PyObject*
PyGreenlet_Throw(PyGreenlet* self, PyObject* typ, PyObject* val, PyObject* tb)
{
    if (!PyGreenlet_Check(self)) {
        PyErr_BadArgument();
        return nullptr;
    }
    try {
        PyErrPieces err_pieces(typ, val, tb);
        return throw_greenlet(self, err_pieces).relinquish_ownership();
    }
    catch (const PyErrOccurred&) {
        return nullptr;
    }
}

static int
Extern_PyGreenlet_MAIN(PyGreenlet* self)
{
    if (!PyGreenlet_Check(self)) {
        PyErr_BadArgument();
        return -1;
    }
    return self->pimpl->main();
}

static int
Extern_PyGreenlet_ACTIVE(PyGreenlet* self)
{
    if (!PyGreenlet_Check(self)) {
        PyErr_BadArgument();
        return -1;
    }
    return self->pimpl->active();
}

static int
Extern_PyGreenlet_STARTED(PyGreenlet* self)
{
    if (!PyGreenlet_Check(self)) {
        PyErr_BadArgument();
        return -1;
    }
    return self->pimpl->started();
}

static PyGreenlet*
Extern_PyGreenlet_GET_PARENT(PyGreenlet* self)
{
    if (!PyGreenlet_Check(self)) {
        PyErr_BadArgument();
        return NULL;
    }
    // This can return NULL even if there is no exception
    return self->pimpl->parent().acquire();
}
} // extern C.
/** End C API ****************************************************************/

static PyMethodDef green_methods[] = {
    {"switch",
     reinterpret_cast<PyCFunction>(green_switch),
     METH_VARARGS | METH_KEYWORDS,
     green_switch_doc},
    {"throw", (PyCFunction)green_throw, METH_VARARGS, green_throw_doc},
    {"__getstate__", (PyCFunction)green_getstate, METH_NOARGS, NULL},
    {NULL, NULL} /* sentinel */
};

static PyGetSetDef green_getsets[] = {
    {"__dict__", (getter)green_getdict, (setter)green_setdict, /*XXX*/ NULL},
    {"run", (getter)green_getrun, (setter)green_setrun, /*XXX*/ NULL},
    {"parent", (getter)green_getparent, (setter)green_setparent, /*XXX*/ NULL},
    {"gr_frame", (getter)green_getframe, NULL, /*XXX*/ NULL},
    {"gr_context",
     (getter)green_getcontext,
     (setter)green_setcontext,
     /*XXX*/ NULL},
    {"dead", (getter)green_getdead, NULL, /*XXX*/ NULL},
    {"_stack_saved", (getter)green_get_stack_saved, NULL, /*XXX*/ NULL},
    {NULL}};

static PyMemberDef green_members[] = {
    {NULL}
};

static PyNumberMethods green_as_number = {
    NULL, /* nb_add */
    NULL, /* nb_subtract */
    NULL, /* nb_multiply */
#if PY_MAJOR_VERSION < 3
    NULL, /* nb_divide */
#endif
    NULL,                /* nb_remainder */
    NULL,                /* nb_divmod */
    NULL,                /* nb_power */
    NULL,                /* nb_negative */
    NULL,                /* nb_positive */
    NULL,                /* nb_absolute */
    (inquiry)green_bool, /* nb_bool */
};


PyTypeObject PyGreenlet_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "greenlet.greenlet", /* tp_name */
    sizeof(PyGreenlet),  /* tp_basicsize */
    0,                   /* tp_itemsize */
    /* methods */
    (destructor)green_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_compare */
    (reprfunc)green_repr,      /* tp_repr */
    &green_as_number,          /* tp_as _number*/
    0,                         /* tp_as _sequence*/
    0,                         /* tp_as _mapping*/
    0,                         /* tp_hash */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer*/
    G_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "greenlet(run=None, parent=None) -> greenlet\n\n"
    "Creates a new greenlet object (without running it).\n\n"
    " - *run* -- The callable to invoke.\n"
    " - *parent* -- The parent greenlet. The default is the current "
    "greenlet.",                        /* tp_doc */
    (traverseproc)green_traverse, /* tp_traverse */
    (inquiry)green_clear,         /* tp_clear */
    0,                                  /* tp_richcompare */
    offsetof(PyGreenlet, weakreflist),  /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    green_methods,                      /* tp_methods */
    green_members,                      /* tp_members */
    green_getsets,                      /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    offsetof(PyGreenlet, dict),         /* tp_dictoffset */
    (initproc)green_init,               /* tp_init */
    PyType_GenericAlloc,                  /* tp_alloc */
    (newfunc)green_new,                          /* tp_new */
    PyObject_GC_Del,                   /* tp_free */
    (inquiry)green_is_gc,         /* tp_is_gc */
};



PyDoc_STRVAR(mod_getcurrent_doc,
             "getcurrent() -> greenlet\n"
             "\n"
             "Returns the current greenlet (i.e. the one which called this "
             "function).\n");

static PyObject*
mod_getcurrent(PyObject* UNUSED(module))
{
    return GET_THREAD_STATE().state().get_current().relinquish_ownership_o();
}

PyDoc_STRVAR(mod_settrace_doc,
             "settrace(callback) -> object\n"
             "\n"
             "Sets a new tracing function and returns the previous one.\n");
static PyObject*
mod_settrace(PyObject* UNUSED(module), PyObject* args)
{
    PyArgParseParam tracefunc;
    if (!PyArg_ParseTuple(args, "O", &tracefunc)) {
        return NULL;
    }
    ThreadState& state = GET_THREAD_STATE();
    OwnedObject previous = state.get_tracefunc();
    if (!previous) {
        previous = Py_None;
    }

    state.set_tracefunc(tracefunc);

    return previous.relinquish_ownership();
}

PyDoc_STRVAR(mod_gettrace_doc,
             "gettrace() -> object\n"
             "\n"
             "Returns the currently set tracing function, or None.\n");

static PyObject*
mod_gettrace(PyObject* UNUSED(module))
{
    OwnedObject tracefunc = GET_THREAD_STATE().state().get_tracefunc();
    if (!tracefunc) {
        tracefunc = Py_None;
    }
    return tracefunc.relinquish_ownership();
}

PyDoc_STRVAR(mod_set_thread_local_doc,
             "set_thread_local(key, value) -> None\n"
             "\n"
             "Set a value in the current thread-local dictionary. Debbuging only.\n");

static PyObject*
mod_set_thread_local(PyObject* UNUSED(module), PyObject* args)
{
    PyArgParseParam key;
    PyArgParseParam value;
    PyObject* result = NULL;

    if (PyArg_UnpackTuple(args, "set_thread_local", 2, 2, &key, &value)) {
        if(PyDict_SetItem(
                          PyThreadState_GetDict(), // borrow
                          key,
                          value) == 0 ) {
            // success
            Py_INCREF(Py_None);
            result = Py_None;
        }
    }
    return result;
}

PyDoc_STRVAR(mod_get_pending_cleanup_count_doc,
             "get_pending_cleanup_count() -> Integer\n"
             "\n"
             "Get the number of greenlet cleanup operations pending. Testing only.\n");


static PyObject*
mod_get_pending_cleanup_count(PyObject* UNUSED(module))
{
    LockGuard cleanup_lock(*mod_globs.thread_states_to_destroy_lock);
    return PyLong_FromSize_t(mod_globs.thread_states_to_destroy.size());
}

PyDoc_STRVAR(mod_get_total_main_greenlets_doc,
             "get_total_main_greenlets() -> Integer\n"
             "\n"
             "Quickly return the number of main greenlets that exist. Testing only.\n");

static PyObject*
mod_get_total_main_greenlets(PyObject* UNUSED(module))
{
    return PyLong_FromSize_t(total_main_greenlets);
}

PyDoc_STRVAR(mod_get_clocks_used_doing_optional_cleanup_doc,
             "get_clocks_used_doing_optional_cleanup() -> Integer\n"
             "\n"
             "Get the number of clock ticks the program has used doing optional "
             "greenlet cleanup.\n"
             "Beginning in greenlet 2.0, greenlet tries to find and dispose of greenlets\n"
             "that leaked after a thread exited. This requires invoking Python's garbage collector,\n"
             "which may have a performance cost proportional to the number of live objects.\n"
             "This function returns the amount of processor time\n"
             "greenlet has used to do this. In programs that run with very large amounts of live\n"
             "objects, this metric can be used to decide whether the cost of doing this cleanup\n"
             "is worth the memory leak being corrected. If not, you can disable the cleanup\n"
             "using ``enable_optional_cleanup(False)``.\n"
             "The units are arbitrary and can only be compared to themselves (similarly to ``time.clock()``);\n"
             "for example, to see how it scales with your heap. You can attempt to convert them into seconds\n"
             "by dividing by the value of CLOCKS_PER_SEC."
             "If cleanup has been disabled, returns None."
             "\n"
             "This is an implementation specific, provisional API. It may be changed or removed\n"
             "in the future.\n"
             ".. versionadded:: 2.0"
             );
static PyObject*
mod_get_clocks_used_doing_optional_cleanup(PyObject* UNUSED(module))
{
    std::clock_t& clocks = ThreadState::clocks_used_doing_gc();

    if (clocks == std::clock_t(-1)) {
        Py_RETURN_NONE;
    }
    // This might not actually work on some implementations; clock_t
    // is an opaque type.
    return PyLong_FromSsize_t(clocks);
}

PyDoc_STRVAR(mod_enable_optional_cleanup_doc,
             "mod_enable_optional_cleanup(bool) -> None\n"
             "\n"
             "Enable or disable optional cleanup operations.\n"
             "See ``get_clocks_used_doing_optional_cleanup()`` for details.\n"
             );
static PyObject*
mod_enable_optional_cleanup(PyObject* UNUSED(module), PyObject* flag)
{
    int is_true = PyObject_IsTrue(flag);
    if (is_true == -1) {
        return nullptr;
    }

    std::clock_t& clocks = ThreadState::clocks_used_doing_gc();
    if (is_true) {
        // If we already have a value, we don't want to lose it.
        if (clocks == std::clock_t(-1)) {
            clocks = 0;
        }
    }
    else {
        clocks = std::clock_t(-1);
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(mod_get_tstate_trash_delete_nesting_doc,
             "get_tstate_trash_delete_nesting() -> Integer\n"
             "\n"
             "Return the 'trash can' nesting level. Testing only.\n");
static PyObject*
mod_get_tstate_trash_delete_nesting(PyObject* UNUSED(module))
{
    PyThreadState* tstate = PyThreadState_GET();
    return PyLong_FromLong(tstate->trash_delete_nesting);
}

static PyMethodDef GreenMethods[] = {
    {"getcurrent",
     (PyCFunction)mod_getcurrent,
     METH_NOARGS,
     mod_getcurrent_doc},
    {"settrace", (PyCFunction)mod_settrace, METH_VARARGS, mod_settrace_doc},
    {"gettrace", (PyCFunction)mod_gettrace, METH_NOARGS, mod_gettrace_doc},
    {"set_thread_local", (PyCFunction)mod_set_thread_local, METH_VARARGS, mod_set_thread_local_doc},
    {"get_pending_cleanup_count", (PyCFunction)mod_get_pending_cleanup_count, METH_NOARGS, mod_get_pending_cleanup_count_doc},
    {"get_total_main_greenlets", (PyCFunction)mod_get_total_main_greenlets, METH_NOARGS, mod_get_total_main_greenlets_doc},
    {"get_clocks_used_doing_optional_cleanup", (PyCFunction)mod_get_clocks_used_doing_optional_cleanup, METH_NOARGS, mod_get_clocks_used_doing_optional_cleanup_doc},
    {"enable_optional_cleanup", (PyCFunction)mod_enable_optional_cleanup, METH_O, mod_enable_optional_cleanup_doc},
    {"get_tstate_trash_delete_nesting", (PyCFunction)mod_get_tstate_trash_delete_nesting, METH_NOARGS, mod_get_tstate_trash_delete_nesting_doc},
    {NULL, NULL} /* Sentinel */
};

static const char* const copy_on_greentype[] = {
    "getcurrent",
    "error",
    "GreenletExit",
    "settrace",
    "gettrace",
    NULL
};

static struct PyModuleDef greenlet_module_def = {
    PyModuleDef_HEAD_INIT,
    "greenlet._greenlet",
    NULL,
    -1,
    GreenMethods,
};



static PyObject*
greenlet_internal_mod_init() G_NOEXCEPT
{
    static void* _PyGreenlet_API[PyGreenlet_API_pointers];
    GREENLET_NOINLINE_INIT();

    try {
        CreatedModule m(greenlet_module_def);

        Require(PyType_Ready(&PyGreenlet_Type));

#if G_USE_STANDARD_THREADING == 0
        Require(PyType_Ready(&PyGreenletCleanup_Type));
#endif

        new((void*)&mod_globs) GreenletGlobals;
        ThreadState::init();

        m.PyAddObject("greenlet", PyGreenlet_Type);
        m.PyAddObject("error", mod_globs.PyExc_GreenletError);
        m.PyAddObject("GreenletExit", mod_globs.PyExc_GreenletExit);

        m.PyAddObject("GREENLET_USE_GC", 1);
        m.PyAddObject("GREENLET_USE_TRACING", 1);
        // The macros are eithre 0 or 1; the 0 case can be interpreted
        // the same as NULL, which is ambiguous with a pointer.
        m.PyAddObject("GREENLET_USE_CONTEXT_VARS", (long)GREENLET_PY37);
        m.PyAddObject("GREENLET_USE_STANDARD_THREADING", (long)G_USE_STANDARD_THREADING);

        OwnedObject clocks_per_sec = OwnedObject::consuming(PyLong_FromSsize_t(CLOCKS_PER_SEC));
        m.PyAddObject("CLOCKS_PER_SEC", clocks_per_sec);

        /* also publish module-level data as attributes of the greentype. */
        // XXX: This is weird, and enables a strange pattern of
        // confusing the class greenlet with the module greenlet; with
        // the exception of (possibly) ``getcurrent()``, this
        // shouldn't be encouraged so don't add new items here.
        for (const char* const* p = copy_on_greentype; *p; p++) {
            OwnedObject o = m.PyRequireAttr(*p);
            PyDict_SetItemString(PyGreenlet_Type.tp_dict, *p, o.borrow());
        }

        /*
         * Expose C API
         */

        /* types */
        _PyGreenlet_API[PyGreenlet_Type_NUM] = (void*)&PyGreenlet_Type;

        /* exceptions */
        _PyGreenlet_API[PyExc_GreenletError_NUM] = (void*)mod_globs.PyExc_GreenletError;
        _PyGreenlet_API[PyExc_GreenletExit_NUM] = (void*)mod_globs.PyExc_GreenletExit;

        /* methods */
        _PyGreenlet_API[PyGreenlet_New_NUM] = (void*)PyGreenlet_New;
        _PyGreenlet_API[PyGreenlet_GetCurrent_NUM] = (void*)PyGreenlet_GetCurrent;
        _PyGreenlet_API[PyGreenlet_Throw_NUM] = (void*)PyGreenlet_Throw;
        _PyGreenlet_API[PyGreenlet_Switch_NUM] = (void*)PyGreenlet_Switch;
        _PyGreenlet_API[PyGreenlet_SetParent_NUM] = (void*)PyGreenlet_SetParent;

        /* Previously macros, but now need to be functions externally. */
        _PyGreenlet_API[PyGreenlet_MAIN_NUM] = (void*)Extern_PyGreenlet_MAIN;
        _PyGreenlet_API[PyGreenlet_STARTED_NUM] = (void*)Extern_PyGreenlet_STARTED;
        _PyGreenlet_API[PyGreenlet_ACTIVE_NUM] = (void*)Extern_PyGreenlet_ACTIVE;
        _PyGreenlet_API[PyGreenlet_GET_PARENT_NUM] = (void*)Extern_PyGreenlet_GET_PARENT;

        /* XXX: Note that our module name is ``greenlet._greenlet``, but for
           backwards compatibility with existing C code, we need the _C_API to
           be directly in greenlet.
        */
        const NewReference c_api_object(Require(
                                           PyCapsule_New(
                                               (void*)_PyGreenlet_API,
                                               "greenlet._C_API",
                                               NULL)));
        m.PyAddObject("_C_API", c_api_object);
        assert(c_api_object.REFCNT() == 2);

        // cerr << "Sizes:"
        //      << "\n\tGreenlet       : " << sizeof(Greenlet)
        //      << "\n\tUserGreenlet   : " << sizeof(UserGreenlet)
        //      << "\n\tMainGreenlet   : " << sizeof(MainGreenlet)
        //      << "\n\tExceptionState : " << sizeof(greenlet::ExceptionState)
        //      << "\n\tPythonState    : " << sizeof(greenlet::PythonState)
        //      << "\n\tStackState     : " << sizeof(greenlet::StackState)
        //      << "\n\tSwitchingArgs  : " << sizeof(greenlet::SwitchingArgs)
        //      << "\n\tOwnedObject    : " << sizeof(greenlet::refs::OwnedObject)
        //      << "\n\tBorrowedObject : " << sizeof(greenlet::refs::BorrowedObject)
        //      << "\n\tPyGreenlet     : " << sizeof(PyGreenlet)
        //      << endl;

        return m.borrow(); // But really it's the main reference.
    }
    catch (const LockInitError& e) {
        PyErr_SetString(PyExc_MemoryError, e.what());
        return NULL;
    }
    catch (const PyErrOccurred&) {
        return NULL;
    }

}

extern "C" {
#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC
PyInit__greenlet(void)
{
    return greenlet_internal_mod_init();
}
#else
PyMODINIT_FUNC
init_greenlet(void)
{
    greenlet_internal_mod_init();
}
#endif
};

#ifdef __clang__
#    pragma clang diagnostic pop
#elif defined(__GNUC__)
#    pragma GCC diagnostic pop
#endif
