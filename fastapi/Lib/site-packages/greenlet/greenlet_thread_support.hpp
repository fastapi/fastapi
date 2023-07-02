#ifndef GREENLET_THREAD_SUPPORT_HPP
#define GREENLET_THREAD_SUPPORT_HPP

/**
 * Defines various utility functions to help greenlet integrate well
 * with threads. When possible, we use portable C++ 11 threading; when
 * not possible, we will use platform specific APIs if needed and
 * available. (Currently, this is only for Python 2.7 on Windows.)
 */

#include <stdexcept>
#include "greenlet_compiler_compat.hpp"

// Allow setting this to 0 on the command line so that we
// can test these code paths on compilers that otherwise support
// standard threads.
#ifndef G_USE_STANDARD_THREADING
#if __cplusplus >= 201103
// Cool. We should have standard support
#    define G_USE_STANDARD_THREADING 1
#elif defined(_MSC_VER)
// MSVC doesn't use a modern version of __cplusplus automatically, you
// have to opt-in to update it with /Zc:__cplusplus, but that's not
// available on our old version of visual studio for Python 2.7
#    if _MSC_VER <= 1500
// Python 2.7 on Windows. Use the Python thread state and native Win32 APIs.
#        define G_USE_STANDARD_THREADING 0
#    else
// Assume we have a compiler that supports it. The Appveyor compilers
// we use all do have standard support
#        define G_USE_STANDARD_THREADING 1
#    endif
#elif defined(__GNUC__) || defined(__clang__)
// All tested versions either do, or can with the right --std argument, support what we need
#    define G_USE_STANDARD_THREADING 1
#else
#    define G_USE_STANDARD_THREADING 0
#endif
#endif /* G_USE_STANDARD_THREADING */

namespace greenlet {
    class LockInitError : public std::runtime_error
    {
    public:
        LockInitError(const char* what) : std::runtime_error(what)
        {};
    };
};


#if G_USE_STANDARD_THREADING == 1
#    define G_THREAD_LOCAL_SUPPORTS_DESTRUCTOR 1
#    include <thread>
#    include <mutex>
#    define G_THREAD_LOCAL_VAR thread_local
namespace greenlet {
    typedef std::mutex Mutex;
    typedef std::lock_guard<Mutex> LockGuard;
};
#else
// NOTE: At this writing, the mutex isn't currently required;
// we don't use a shared cleanup queue or Py_AddPendingCall in this
// model, we rely on the thread state dictionary for cleanup.
#    if defined(_MSC_VER)
//       We should only hit this case for Python 2.7 on Windows.
#        define G_THREAD_LOCAL_VAR __declspec(thread)
#        include <windows.h>
namespace greenlet {
    class Mutex
    {
        CRITICAL_SECTION _mutex;
        G_NO_COPIES_OF_CLS(Mutex);
    public:
        Mutex()
        {
            InitializeCriticalSection(&this->_mutex);
        };

        void Lock()
        {
            EnterCriticalSection(&this->_mutex);
        };

        void UnLock()
        {
            LeaveCriticalSection(&this->_mutex);
        };
    };
};
#    elif (defined(__GNUC__) || defined(__clang__)) || (defined(__SUNPRO_C))
// GCC, clang, SunStudio all use __thread for thread-local variables.
// For locks, we can use PyThread APIs, officially added in 3.2, but
// present back to 2.7
#        define G_THREAD_LOCAL_VAR __thread
#        include "pythread.h"
namespace greenlet {
    class Mutex
    {
        PyThread_type_lock _mutex;
        G_NO_COPIES_OF_CLS(Mutex);
    public:
        Mutex()
        {
            this->_mutex = PyThread_allocate_lock();
            if (!this->_mutex) {
                throw LockInitError("Failed to initialize mutex.");
            }
        };

        void Lock()
        {
            PyThread_acquire_lock(this->_mutex, WAIT_LOCK);
        };

        void UnLock()
        {
            PyThread_release_lock(this->_mutex);
        };
    };
};
#    else
#        error Unable to declare thread-local variables.
#    endif
// the RAII lock keeper for all non-standard threading platforms.
namespace greenlet {
    class LockGuard
    {
        Mutex& _mutex;
        G_NO_COPIES_OF_CLS(LockGuard);
    public:
        LockGuard(Mutex& m) : _mutex(m)
        {
            this->_mutex.Lock();
        };
        ~LockGuard()
        {
            this->_mutex.UnLock();
        };
    };

};
#endif /* G_USE_STANDARD_THREADING == 1 */

#endif /* GREENLET_THREAD_SUPPORT_HPP */
