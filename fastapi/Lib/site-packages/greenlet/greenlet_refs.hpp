#ifndef GREENLET_REFS_HPP
#define GREENLET_REFS_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
//#include "greenlet_internal.hpp"
#include "greenlet_compiler_compat.hpp"
#include "greenlet_cpython_compat.hpp"
#include "greenlet_exceptions.hpp"

struct _greenlet;
struct _PyMainGreenlet;

typedef struct _greenlet PyGreenlet;
extern PyTypeObject PyGreenlet_Type;


#ifdef  GREENLET_USE_STDIO
#include <iostream>
using std::cerr;
using std::endl;
#endif

namespace greenlet
{
    class Greenlet;

    namespace refs
    {
        // Type checkers throw a TypeError if the argument is not
        // null, and isn't of the required Python type.
        // (We can't use most of the defined type checkers
        // like PyList_Check, etc, directly, because they are
        // implemented as macros.)
        typedef void (*TypeChecker)(void*);

        G_FP_TMPL_STATIC inline void
        NoOpChecker(void*)
        {
            return;
        }

        G_FP_TMPL_STATIC inline void
        GreenletChecker(void *p)
        {
            if (!p) {
                return;
            }

            PyTypeObject* typ = Py_TYPE(p);
            // fast, common path. (PyObject_TypeCheck is a macro or
            // static inline function, and it also does a
            // direct comparison of the type pointers, but its fast
            // path only handles one type)
            if (typ == &PyGreenlet_Type) {
                return;
            }

            if (!PyObject_TypeCheck(p, &PyGreenlet_Type)) {
                std::string err("GreenletChecker: Expected any type of greenlet, not ");
                err += Py_TYPE(p)->tp_name;
                throw TypeError(err);
            }
        }

        G_FP_TMPL_STATIC inline void
        MainGreenletExactChecker(void *p);

        template <typename T, TypeChecker>
        class PyObjectPointer;

        template<typename T, TypeChecker>
        class OwnedReference;


        template<typename T, TypeChecker>
        class BorrowedReference;

        typedef BorrowedReference<PyObject, NoOpChecker> BorrowedObject;
        typedef OwnedReference<PyObject, NoOpChecker> OwnedObject;

        class ImmortalObject;

        template<typename T, TypeChecker TC>
        class _OwnedGreenlet;

        typedef _OwnedGreenlet<PyGreenlet, GreenletChecker> OwnedGreenlet;
        typedef _OwnedGreenlet<PyGreenlet, MainGreenletExactChecker> OwnedMainGreenlet;

        template<typename T, TypeChecker TC>
        class _BorrowedGreenlet;

        typedef _BorrowedGreenlet<PyGreenlet, GreenletChecker> BorrowedGreenlet;

        G_FP_TMPL_STATIC inline void
        ContextExactChecker(void *p)
        {
            if (!p) {
                return;
            }
#if GREENLET_PY37
            if (!PyContext_CheckExact(p)) {
                throw TypeError(
                    "greenlet context must be a contextvars.Context or None"
                );
            }
#endif
        }

        typedef OwnedReference<PyObject, ContextExactChecker> OwnedContext;
    }
}

namespace greenlet {


    namespace refs {
    // A set of classes to make reference counting rules in python
    // code explicit.
    //
    // Rules of use:
    // (1) Functions returning a new reference that the caller of the
    // function is expected to dispose of should return a
    // ``OwnedObject`` object. This object automatically releases its
    // reference when it goes out of scope. It works like a ``std::shared_ptr``
    // and can be copied or used as a function parameter (but don't do
    // that). Note that constructing a ``OwnedObject`` from a
    // PyObject* steals the reference.
    // (2) Parameters to functions should be either a
    // ``OwnedObject&``, or, more generally, a ``PyObjectPointer&``.
    // If the function needs to create its own new reference, it can
    // do so by copying to a local ``OwnedObject``.
    // (3) Functions returning an existing pointer that is NOT
    // incref'd, and which the caller MUST NOT decref,
    // should return a ``BorrowedObject``.

    //
    // For a class with a single pointer member, whose constructor
    // does nothing but copy a pointer parameter into the member, and
    // which can then be converted back to the pointer type, compilers
    // generate code that's the same as just passing the pointer.
    // That is, func(BorrowedObject x) called like ``PyObject* p =
    // ...; f(p)`` has 0 overhead. Similarly, they "unpack" to the
    // pointer type with 0 overhead.
    //
    // If there are no virtual functions, no complex inheritance (maybe?) and
    // no destructor, these can be directly used as parameters in
    // Python callbacks like tp_init: the layout is the same as a
    // single pointer. Only subclasses with trivial constructors that
    // do nothing but set the single pointer member are safe to use
    // that way.


    // This is the base class for things that can be done with a
    // PyObject pointer. It assumes nothing about memory management.
    // NOTE: Nothing is virtual, so subclasses shouldn't add new
    // storage fields or try to override these methods.
    template <typename T=PyObject, TypeChecker TC=NoOpChecker>
    class PyObjectPointer
    {
    public:
        typedef T PyType;
    protected:
        T* p;
    public:
        explicit PyObjectPointer(T* it=nullptr) : p(it)
        {
            TC(p);
        }

        // We don't allow automatic casting to PyObject* at this
        // level, because then we could be passed to Py_DECREF/INCREF,
        // but we want nothing to do with memory management. If you
        // know better, then you can use the get() method, like on a
        // std::shared_ptr. Except we name it borrow() to clarify that
        // if this is a reference-tracked object, the pointer you get
        // back will go away when the object does.
        // TODO: This should probably not exist here, but be moved
        // down to relevant sub-types.

        inline T* borrow() const G_NOEXCEPT
        {
            return this->p;
        }

        PyObject* borrow_o() const G_NOEXCEPT
        {
            return reinterpret_cast<PyObject*>(this->p);
        }

        inline T* operator->() const G_NOEXCEPT
        {
            return this->p;
        }

        bool is_None() const G_NOEXCEPT
        {
            return this->p == Py_None;
        }

        inline PyObject* acquire_or_None() const G_NOEXCEPT
        {
            PyObject* result = this->p ? reinterpret_cast<PyObject*>(this->p) : Py_None;
            Py_INCREF(result);
            return result;
        }

        G_EXPLICIT_OP operator bool() const G_NOEXCEPT
        {
            return p != nullptr;
        }

        inline Py_ssize_t REFCNT() const G_NOEXCEPT
        {
            return p ? Py_REFCNT(p) : -42;
        }

        inline PyTypeObject* TYPE() const G_NOEXCEPT
        {
            return p ? Py_TYPE(p) : nullptr;
        }

        inline OwnedObject PyStr() const G_NOEXCEPT;
        inline const std::string as_str() const G_NOEXCEPT;
        inline OwnedObject PyGetAttr(const ImmortalObject& name) const G_NOEXCEPT;
        inline OwnedObject PyRequireAttr(const char* const name) const;
        inline OwnedObject PyRequireAttr(const ImmortalObject& name) const;
        inline OwnedObject PyCall(const BorrowedObject& arg) const;
        inline OwnedObject PyCall(PyGreenlet* arg) const ;
        inline OwnedObject PyCall(PyObject* arg) const ;
        // PyObject_Call(this, args, kwargs);
        inline OwnedObject PyCall(const BorrowedObject args,
                                  const BorrowedObject kwargs) const;
        inline OwnedObject PyCall(const OwnedObject& args,
                                  const OwnedObject& kwargs) const;

    protected:
        void _set_raw_pointer(void* t)
        {
            TC(t);
            p = reinterpret_cast<T*>(t);
        }
        void* _get_raw_pointer() const
        {
            return p;
        }
    };

#ifdef GREENLET_USE_STDIO
        template<typename T, TypeChecker TC>
        std::ostream& operator<<(std::ostream& os, const PyObjectPointer<T, TC>& s)
        {
            const std::type_info& t = typeid(s);
            os << t.name()
               << "(addr=" << s.borrow()
               << ", refcnt=" << s.REFCNT()
               << ", value=" << s.as_str()
               << ")";

            return os;
        }
#endif

    template<typename T, TypeChecker TC>
    inline bool operator==(const PyObjectPointer<T, TC>& lhs, const void* const rhs) G_NOEXCEPT
    {
        return lhs.borrow_o() == rhs;
    }

    template<typename T, TypeChecker TC, typename X, TypeChecker XC>
    inline bool operator==(const PyObjectPointer<T, TC>& lhs, const PyObjectPointer<X, XC>& rhs) G_NOEXCEPT
    {
        return lhs.borrow_o() == rhs.borrow_o();
    }

    template<typename T, TypeChecker TC, typename X, TypeChecker XC>
    inline bool operator!=(const PyObjectPointer<T, TC>& lhs,
                           const PyObjectPointer<X, XC>& rhs) G_NOEXCEPT
    {
        return lhs.borrow_o() != rhs.borrow_o();
    }

    template<typename T=PyObject, TypeChecker TC=NoOpChecker>
    class OwnedReference : public PyObjectPointer<T, TC>
    {
    private:
        friend class OwnedList;

    protected:
        explicit OwnedReference(T* it) : PyObjectPointer<T, TC>(it)
        {
        }

    public:

        // Constructors

        static OwnedReference<T, TC> consuming(PyObject* p)
        {
            return OwnedReference<T, TC>(reinterpret_cast<T*>(p));
        }

        static OwnedReference<T, TC> owning(T* p)
        {
            OwnedReference<T, TC> result(p);
            Py_XINCREF(result.p);
            return result;
        }

        OwnedReference() : PyObjectPointer<T, TC>(nullptr)
        {}

        explicit OwnedReference(const PyObjectPointer<>& other)
            : PyObjectPointer<T, TC>(nullptr)
        {
            T* op = other.borrow();
            TC(op);
            this->p = other.borrow();
            Py_XINCREF(this->p);
        }

        // It would be good to make use of the C++11 distinction
        // between move and copy operations, e.g., constructing from a
        // pointer should be a move operation.
        // In the common case of ``OwnedObject x = Py_SomeFunction()``,
        // the call to the copy constructor will be elided completely.
        OwnedReference(const OwnedReference<T, TC>& other)
            : PyObjectPointer<T, TC>(other.p)
        {
            Py_XINCREF(this->p);
        }

        static OwnedReference<PyObject> None()
        {
            Py_INCREF(Py_None);
            return OwnedReference<PyObject>(Py_None);
        }

        // We can assign from exactly our type without any extra checking
        OwnedReference<T, TC>& operator=(const OwnedReference<T, TC>& other)
        {
            Py_XINCREF(other.p);
            const T* tmp = this->p;
            this->p = other.p;
            Py_XDECREF(tmp);
            return *this;
        }

        OwnedReference<T, TC>& operator=(const BorrowedReference<T, TC> other)
        {
            return this->operator=(other.borrow());
        }

        OwnedReference<T, TC>& operator=(T* const other)
        {
            TC(other);
            Py_XINCREF(other);
            T* tmp = this->p;
            this->p = other;
            Py_XDECREF(tmp);
            return *this;
        }

        // We can assign from an arbitrary reference type
        // if it passes our check.
        template<typename X, TypeChecker XC>
        OwnedReference<T, TC>& operator=(const OwnedReference<X, XC>& other)
        {
            X* op = other.borrow();
            TC(op);
            return this->operator=(reinterpret_cast<T*>(op));
        }

        inline void steal(T* other)
        {
            assert(this->p == nullptr);
            TC(other);
            this->p = other;
        }

        T* relinquish_ownership()
        {
            T* result = this->p;
            this->p = nullptr;
            return result;
        }

        T* acquire() const
        {
            // Return a new reference.
            // TODO: This may go away when we have reference objects
            // throughout the code.
            Py_XINCREF(this->p);
            return this->p;
        }

        // Nothing else declares a destructor, we're the leaf, so we
        // should be able to get away without virtual.
        ~OwnedReference()
        {
            Py_CLEAR(this->p);
        }

        void CLEAR()
        {
            Py_CLEAR(this->p);
            assert(this->p == nullptr);
        }
    };

    static inline
    void operator<<=(PyObject*& target, OwnedObject& o)
    {
        target = o.relinquish_ownership();
    }

    class NewReference : public OwnedObject
    {
    private:
        G_NO_COPIES_OF_CLS(NewReference);
    public:
        // Consumes the reference. Only use this
        // for API return values.
        NewReference(PyObject* it) : OwnedObject(it)
        {
        }
    };

    class NewDictReference : public NewReference
    {
    private:
        G_NO_COPIES_OF_CLS(NewDictReference);
    public:
        NewDictReference() : NewReference(PyDict_New())
        {
            if (!this->p) {
                throw PyErrOccurred();
            }
        }

        void SetItem(const char* const key, PyObject* value)
        {
            Require(PyDict_SetItemString(this->p, key, value));
        }

        void SetItem(const PyObjectPointer<>& key, PyObject* value)
        {
            Require(PyDict_SetItem(this->p, key.borrow_o(), value));
        }
    };

    template<typename T=PyGreenlet, TypeChecker TC=GreenletChecker>
    class _OwnedGreenlet: public OwnedReference<T, TC>
    {
    private:
    protected:
        _OwnedGreenlet(T* it) : OwnedReference<T, TC>(it)
        {}

    public:
        _OwnedGreenlet() : OwnedReference<T, TC>()
        {}

        _OwnedGreenlet(const _OwnedGreenlet<T, TC>& other) : OwnedReference<T, TC>(other)
        {
        }
        _OwnedGreenlet(OwnedMainGreenlet& other) :
            OwnedReference<T, TC>(reinterpret_cast<T*>(other.acquire()))
        {
        }
        _OwnedGreenlet(const BorrowedGreenlet& other);
        // Steals a reference.
        static _OwnedGreenlet<T, TC> consuming(PyGreenlet* it)
        {
            return _OwnedGreenlet<T, TC>(reinterpret_cast<T*>(it));
        }

        inline _OwnedGreenlet<T, TC>& operator=(const OwnedGreenlet& other)
        {
            return this->operator=(other.borrow());
        }

        inline _OwnedGreenlet<T, TC>& operator=(const BorrowedGreenlet& other);

        _OwnedGreenlet<T, TC>& operator=(const OwnedMainGreenlet& other)
        {
            PyGreenlet* owned = other.acquire();
            Py_XDECREF(this->p);
            this->p = reinterpret_cast<T*>(owned);
            return *this;
        }

        _OwnedGreenlet<T, TC>& operator=(T* const other)
        {
            OwnedReference<T, TC>::operator=(other);
            return *this;
        }

        T* relinquish_ownership()
        {
            T* result = this->p;
            this->p = nullptr;
            return result;
        }

        PyObject* relinquish_ownership_o()
        {
            return reinterpret_cast<PyObject*>(relinquish_ownership());
        }

        inline Greenlet* operator->() const G_NOEXCEPT;
        inline operator Greenlet*() const G_NOEXCEPT;
    };

    template <typename T=PyObject, TypeChecker TC=NoOpChecker>
    class BorrowedReference : public PyObjectPointer<T, TC>
    {
    public:
        // Allow implicit creation from PyObject* pointers as we
        // transition to using these classes. Also allow automatic
        // conversion to PyObject* for passing to C API calls and even
        // for Py_INCREF/DECREF, because we ourselves do no memory management.
        BorrowedReference(T* it) : PyObjectPointer<T, TC>(it)
        {}

        BorrowedReference(const PyObjectPointer<T>& ref) : PyObjectPointer<T, TC>(ref.borrow())
        {}

        BorrowedReference() : PyObjectPointer<T, TC>(nullptr)
        {}

        operator T*() const
        {
            return this->p;
        }
    };

    typedef BorrowedReference<PyObject> BorrowedObject;
    //typedef BorrowedReference<PyGreenlet> BorrowedGreenlet;

    template<typename T=PyGreenlet, TypeChecker TC=GreenletChecker>
    class _BorrowedGreenlet : public BorrowedReference<T, TC>
    {
    public:
        _BorrowedGreenlet() :
            BorrowedReference<T, TC>(nullptr)
        {}

        _BorrowedGreenlet(T* it) :
            BorrowedReference<T, TC>(it)
        {}

        _BorrowedGreenlet(const BorrowedObject& it);

        _BorrowedGreenlet(const OwnedGreenlet& it) :
            BorrowedReference<T, TC>(it.borrow())
        {}

        _BorrowedGreenlet<T, TC>& operator=(const BorrowedObject& other);

        // We get one of these for PyGreenlet, but one for PyObject
        // is handy as well
        operator PyObject*() const
        {
            return reinterpret_cast<PyObject*>(this->p);
        }
        inline Greenlet* operator->() const G_NOEXCEPT;
        inline operator Greenlet*() const G_NOEXCEPT;
    };

    typedef _BorrowedGreenlet<PyGreenlet> BorrowedGreenlet;

    template<typename T, TypeChecker TC>
    _OwnedGreenlet<T, TC>::_OwnedGreenlet(const BorrowedGreenlet& other)
        : OwnedReference<T, TC>(reinterpret_cast<T*>(other.borrow()))
    {
        Py_XINCREF(this->p);
    }


     class BorrowedMainGreenlet
            : public _BorrowedGreenlet<PyGreenlet, MainGreenletExactChecker>
    {
    public:
        BorrowedMainGreenlet(const OwnedMainGreenlet& it) :
            _BorrowedGreenlet<PyGreenlet, MainGreenletExactChecker>(it.borrow())
        {}
        BorrowedMainGreenlet(PyGreenlet* it=nullptr)
            : _BorrowedGreenlet<PyGreenlet, MainGreenletExactChecker>(it)
        {}
    };

    template<typename T, TypeChecker TC>
    _OwnedGreenlet<T, TC>& _OwnedGreenlet<T, TC>::operator=(const BorrowedGreenlet& other)
    {
        return this->operator=(other.borrow());
    }


    class ImmortalObject : public PyObjectPointer<>
    {
    private:
        G_NO_ASSIGNMENT_OF_CLS(ImmortalObject);
    public:
        explicit ImmortalObject(PyObject* it) : PyObjectPointer<>(it)
        {
        }

        /**
         * Become the new owner of the object. Does not change the
         * reference count.
         */
        ImmortalObject& operator=(PyObject* it)
        {
            assert(this->p == nullptr);
            this->p = it;
            return *this;
        }

        static ImmortalObject consuming(PyObject* it)
        {
            return ImmortalObject(it);
        }

        inline operator PyObject*() const
        {
            return this->p;
        }
    };

    class ImmortalString : public ImmortalObject
    {
    private:
        G_NO_COPIES_OF_CLS(ImmortalString);
        const char* str;
    public:
        ImmortalString(const char* const str) :
            ImmortalObject(str ? Require(Greenlet_Intern(str)) : nullptr)
        {
            this->str = str;
        }

        inline ImmortalString& operator=(const char* const str)
        {
            if (!this->p) {
                this->p = Require(Greenlet_Intern(str));
                this->str = str;
            }
            else {
                assert(this->str == str);
            }
            return *this;
        }

    };

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyStr() const G_NOEXCEPT
    {
        if (!this->p) {
            return OwnedObject();
        }
        return OwnedObject::consuming(PyObject_Str(reinterpret_cast<PyObject*>(this->p)));
    }

    template<typename T, TypeChecker TC>
    inline const std::string PyObjectPointer<T, TC>::as_str() const G_NOEXCEPT
    {
        // NOTE: This is not Python exception safe.
        if (this->p) {
            // The Python APIs return a cached char* value that's only valid
            // as long as the original object stays around, and we're
            // about to (probably) toss it. Hence the copy to std::string.
            OwnedObject py_str = this->PyStr();
            if (!py_str) {
                return "(nil)";
            }
#if PY_MAJOR_VERSION >= 3
            return PyUnicode_AsUTF8(py_str.borrow());
#else
            return PyString_AsString(py_str.borrow());
#endif
        }
        return "(nil)";
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyGetAttr(const ImmortalObject& name) const G_NOEXCEPT
    {
        assert(this->p);
        return OwnedObject::consuming(PyObject_GetAttr(reinterpret_cast<PyObject*>(this->p), name));
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyRequireAttr(const char* const name) const
    {
        assert(this->p);
        return OwnedObject::consuming(Require(PyObject_GetAttrString(this->p, name)));
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyRequireAttr(const ImmortalObject& name) const
    {
        assert(this->p);
        return OwnedObject::consuming(Require(
                   PyObject_GetAttr(reinterpret_cast<PyObject*>(this->p),
                                    name)));
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyCall(const BorrowedObject& arg) const
    {
        return this->PyCall(arg.borrow());
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyCall(PyGreenlet* arg) const
    {
        return this->PyCall(reinterpret_cast<PyObject*>(arg));
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyCall(PyObject* arg) const
    {
        assert(this->p);
        return OwnedObject::consuming(PyObject_CallFunctionObjArgs(this->p, arg, NULL));
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyCall(const BorrowedObject args,
                                                  const BorrowedObject kwargs) const
    {
        assert(this->p);
        return OwnedObject::consuming(PyObject_Call(this->p, args, kwargs));
    }

    template<typename T, TypeChecker TC>
    inline OwnedObject PyObjectPointer<T, TC>::PyCall(const OwnedObject& args,
                                                  const OwnedObject& kwargs) const
    {
        assert(this->p);
        return OwnedObject::consuming(PyObject_Call(this->p, args.borrow(), kwargs.borrow()));
    }

    G_FP_TMPL_STATIC inline void
    ListChecker(void * p)
    {
        if (!p) {
            return;
        }
        if (!PyList_Check(p)) {
            throw TypeError("Expected a list");
        }
    }

    class OwnedList : public OwnedReference<PyObject, ListChecker>
    {
    private:
        G_NO_ASSIGNMENT_OF_CLS(OwnedList);
    public:
        // TODO: Would like to use move.
        explicit OwnedList(const OwnedObject& other)
            : OwnedReference<PyObject, ListChecker>(other)
        {
        }

        OwnedList& operator=(const OwnedObject& other)
        {
            if (other && PyList_Check(other.p)) {
                // Valid list. Own a new reference to it, discard the
                // reference to what we did own.
                PyObject* new_ptr = other.p;
                Py_INCREF(new_ptr);
                Py_XDECREF(this->p);
                this->p = new_ptr;
            }
            else {
                // Either the other object was NULL (an error) or it
                // wasn't a list. Either way, we're now invalidated.
                Py_XDECREF(this->p);
                this->p = nullptr;
            }
            return *this;
        }

        inline bool empty() const
        {
            return PyList_GET_SIZE(p) == 0;
        }

        inline Py_ssize_t size() const
        {
            return PyList_GET_SIZE(p);
        }

        inline BorrowedObject at(const Py_ssize_t index) const
        {
            return PyList_GET_ITEM(p, index);
        }

        inline void clear()
        {
            PyList_SetSlice(p, 0, PyList_GET_SIZE(p), NULL);
        }
    };

    // Use this to represent the module object used at module init
    // time.
    // This could either be a borrowed (Py2) or new (Py3) reference;
    // either way, we don't want to do any memory management
    // on it here, Python itself will handle that.
    // XXX: Actually, that's not quite right. On Python 3, if an
    // exception occurs before we return to the interpreter, this will
    // leak; but all previous versions also had that problem.
    class CreatedModule : public PyObjectPointer<>
    {
    private:
        G_NO_COPIES_OF_CLS(CreatedModule);
    public:
        CreatedModule(PyModuleDef& mod_def) : PyObjectPointer<>(
            Require(PyModule_Create(&mod_def)))
        {
        }

        // PyAddObject(): Add a reference to the object to the module.
        // On return, the reference count of the object is unchanged.
        //
        // The docs warn that PyModule_AddObject only steals the
        // reference on success, so if it fails after we've incref'd
        // or allocated, we're responsible for the decref.
        void PyAddObject(const char* name, const long new_bool)
        {
            OwnedObject p = OwnedObject::consuming(Require(PyBool_FromLong(new_bool)));
            this->PyAddObject(name, p);
        }

        void PyAddObject(const char* name, const OwnedObject& new_object)
        {
            // The caller already owns a reference they will decref
            // when their variable goes out of scope, we still need to
            // incref/decref.
            this->PyAddObject(name, new_object.borrow());
        }

        void PyAddObject(const char* name, const ImmortalObject& new_object)
        {
            this->PyAddObject(name, new_object.borrow());
        }

        void PyAddObject(const char* name, PyTypeObject& type)
        {
            this->PyAddObject(name, reinterpret_cast<PyObject*>(&type));
        }

        void PyAddObject(const char* name, PyObject* new_object)
        {
            Py_INCREF(new_object);
            try {
                Require(PyModule_AddObject(this->p, name, new_object));
            }
            catch (const PyErrOccurred&) {
                Py_DECREF(p);
                throw;
            }
        }
    };

    class PyErrFetchParam : public PyObjectPointer<>
    {
        // Not an owned object, because we can't be initialized with
        // one, and we only sometimes acquire ownership.
    private:
        G_NO_COPIES_OF_CLS(PyErrFetchParam);
    public:
        // To allow declaring these and passing them to
        // PyErr_Fetch we implement the empty constructor,
        // and the address operator.
        PyErrFetchParam() : PyObjectPointer<>(nullptr)
        {
        }

        PyObject** operator&()
        {
            return &this->p;
        }

        // This allows us to pass one directly without the &,
        // BUT it has higher precedence than the bool operator
        // if it's not explicit.
        operator PyObject**()
        {
            return &this->p;
        }

        // We don't want to be able to pass these to Py_DECREF and
        // such so we don't have the implicit PyObject* conversion.

        inline PyObject* relinquish_ownership()
        {
            PyObject* result = this->p;
            this->p = nullptr;
            return result;
        }

        ~PyErrFetchParam()
        {
            Py_XDECREF(p);
        }
    };

    class OwnedErrPiece : public OwnedObject
    {
    private:

    public:
        // Unlike OwnedObject, this increments the refcount.
        OwnedErrPiece(PyObject* p=nullptr) : OwnedObject(p)
        {
            this->acquire();
        }

        PyObject** operator&()
        {
            return &this->p;
        }

        inline operator PyObject*() const
        {
            return this->p;
        }

        operator PyTypeObject*() const
        {
            return reinterpret_cast<PyTypeObject*>(this->p);
        }
    };

    class PyErrPieces
    {
    private:
        OwnedErrPiece type;
        OwnedErrPiece instance;
        OwnedErrPiece traceback;
        bool restored;
    public:
        // Takes new references; if we're destroyed before
        // restoring the error, we drop the references.
        PyErrPieces(PyObject* t, PyObject* v, PyObject* tb) :
            type(t),
            instance(v),
            traceback(tb),
            restored(0)
        {
            this->normalize();
        }

        PyErrPieces() :
            restored(0)
        {
            // PyErr_Fetch transfers ownership to us, so
            // we don't actually need to INCREF; but we *do*
            // need to DECREF if we're not restored.
            PyErrFetchParam t, v, tb;
            PyErr_Fetch(&t, &v, &tb);
            type.steal(t.relinquish_ownership());
            instance.steal(v.relinquish_ownership());
            traceback.steal(tb.relinquish_ownership());
        }

        void PyErrRestore()
        {
            // can only do this once
            assert(!this->restored);
            this->restored = true;
            PyErr_Restore(
                this->type.relinquish_ownership(),
                this->instance.relinquish_ownership(),
                this->traceback.relinquish_ownership());
            assert(!this->type && !this->instance && !this->traceback);
        }

    private:
        void normalize()
        {
            // First, check the traceback argument, replacing None,
            // with NULL
            if (traceback.is_None()) {
                traceback = nullptr;
            }

            if (traceback && !PyTraceBack_Check(traceback.borrow())) {
                throw PyErrOccurred(PyExc_TypeError,
                                    "throw() third argument must be a traceback object");
            }

            if (PyExceptionClass_Check(type)) {
                // If we just had a type, we'll now have a type and
                // instance.
                // The type's refcount will have gone up by one
                // because of the instance and the instance will have
                // a refcount of one. Either way, we owned, and still
                // do own, exactly one reference.
                PyErr_NormalizeException(&type, &instance, &traceback);

            }
            else if (PyExceptionInstance_Check(type)) {
                /* Raising an instance --- usually that means an
                   object that is a subclass of BaseException, but on
                   Python 2, that can also mean an arbitrary old-style
                   object. The value should be a dummy. */
                if (instance && !instance.is_None()) {
                    throw PyErrOccurred(
                                    PyExc_TypeError,
                                    "instance exception may not have a separate value");
                }
                /* Normalize to raise <class>, <instance> */
                this->instance = this->type;
                this->type = PyExceptionInstance_Class(instance.borrow());

                /*
                  It would be tempting to do this:

                Py_ssize_t type_count = Py_REFCNT(Py_TYPE(instance.borrow()));
                this->type = PyExceptionInstance_Class(instance.borrow());
                assert(this->type.REFCNT() == type_count + 1);

                But that doesn't work on Python 2 in the case of
                old-style instances: The result of Py_TYPE is going to
                be the global shared <type instance> that all
                old-style classes have, while the return of Instance_Class()
                will be the Python-level class object. The two are unrelated.
                */
            }
            else {
                /* Not something you can raise. throw() fails. */
                PyErr_Format(PyExc_TypeError,
                     "exceptions must be classes, or instances, not %s",
                             Py_TYPE(type.borrow())->tp_name);
                throw PyErrOccurred();
            }
        }
    };

    // PyArg_Parse's O argument returns a borrowed reference.
    class PyArgParseParam : public BorrowedObject
    {
    private:
        G_NO_COPIES_OF_CLS(PyArgParseParam);
    public:
        explicit PyArgParseParam(PyObject* p=nullptr) : BorrowedObject(p)
        {
        }

        inline PyObject** operator&()
        {
            return &this->p;
        }
    };

};};

#endif
