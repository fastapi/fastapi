#ifndef GREENLET_THREAD_STATE_DICT_CLEANUP_HPP
#define GREENLET_THREAD_STATE_DICT_CLEANUP_HPP

#include "greenlet_internal.hpp"
#include "greenlet_thread_state.hpp"

#ifdef __clang__
#    pragma clang diagnostic push
#    pragma clang diagnostic ignored "-Wmissing-field-initializers"
#endif

#ifndef G_THREAD_STATE_DICT_CLEANUP_TYPE
// shut the compiler up if it looks at this file in isolation
#define ThreadStateCreator int
#endif

// Define a Python object that goes in the Python thread state dict
// when the greenlet thread state is created, and which owns the
// reference to the greenlet thread local state.
// When the thread state dict is cleaned up, so too is the thread
// state. This works best if we make sure there are no circular
// references to the thread state.
typedef struct _PyGreenletCleanup {
    PyObject_HEAD
    ThreadStateCreator* thread_state_creator;
} PyGreenletCleanup;

static void
cleanup_do_dealloc(PyGreenletCleanup* self)
{
    ThreadStateCreator* tmp = self->thread_state_creator;
    self->thread_state_creator = nullptr;
    if (tmp) {
        delete tmp;
    }
}

static void
cleanup_dealloc(PyGreenletCleanup* self)
{
    PyObject_GC_UnTrack(self);
    cleanup_do_dealloc(self);
}

static int
cleanup_clear(PyGreenletCleanup* self)
{
    // This method is never called by our test cases.
    cleanup_do_dealloc(self);
    return 0;
}

static int
cleanup_traverse(PyGreenletCleanup* self, visitproc visit, void* arg)
{
    if (self->thread_state_creator) {
        return self->thread_state_creator->tp_traverse(visit, arg);
    }
    return 0;
}

static int
cleanup_is_gc(PyGreenlet* UNUSED(self))
{
    return 1;
}

static PyTypeObject PyGreenletCleanup_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "greenlet._greenlet.ThreadStateCleanup",
    sizeof(struct _PyGreenletCleanup),
    0,                   /* tp_itemsize */
    /* methods */
    (destructor)cleanup_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_compare */
    0,                         /* tp_repr */
    0,                         /* tp_as _number*/
    0,                         /* tp_as _sequence*/
    0,                         /* tp_as _mapping*/
    0,                         /* tp_hash */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer*/
    G_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "Internal use only",                        /* tp_doc */
    (traverseproc)cleanup_traverse, /* tp_traverse */
    (inquiry)cleanup_clear,         /* tp_clear */
    0,                                  /* tp_richcompare */
    // XXX: Don't our flags promise a weakref?
    0,                           /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    0,                      /* tp_methods */
    0,                      /* tp_members */
    0,                      /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,         /* tp_dictoffset */
    0,               /* tp_init */
    PyType_GenericAlloc,                  /* tp_alloc */
    PyType_GenericNew,                          /* tp_new */
    PyObject_GC_Del,                   /* tp_free */
    (inquiry)cleanup_is_gc,         /* tp_is_gc */
};

#ifdef __clang__
#    pragma clang diagnostic pop
#endif


#endif
