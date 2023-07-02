/* -*- indent-tabs-mode: nil; tab-width: 4; -*- */
#ifndef GREENLET_COMPILER_COMPAT_HPP
#define GREENLET_COMPILER_COMPAT_HPP

/**
 * Definitions to aid with compatibility with different compilers.
 *
 * .. caution:: Use extreme care with G_NOEXCEPT.
 * Some compilers and runtimes, specifically gcc/libgcc/libstdc++ on
 * Linux, implement stack unwinding by throwing an uncatchable
 * exception, one that specifically does not appear to be an active
 * exception to the rest of the runtime. If this happens while we're in a G_NOEXCEPT function,
 * we have violated our dynamic exception contract, and so the runtime
 * will call std::terminate(), which kills the process with the
 * unhelpful message "terminate called without an active exception".
 *
 * This has happened in this scenario: A background thread is running
 * a greenlet that has made a native call and released the GIL.
 * Meanwhile, the main thread finishes and starts shutting down the
 * interpreter. When the background thread is scheduled again and
 * attempts to obtain the  GIL, it notices that the interpreter is
 * exiting and calls ``pthread_exit()``. This in turn starts to unwind
 * the stack by throwing that exception. But we had the ``PyCall``
 * functions annotated as G_NOEXCEPT, so the runtime terminated us.
 *
 * #2  0x00007fab26fec2b7 in std::terminate() () from /lib/x86_64-linux-gnu/libstdc++.so.6
 * #3  0x00007fab26febb3c in __gxx_personality_v0 () from /lib/x86_64-linux-gnu/libstdc++.so.6
 * #4  0x00007fab26f34de6 in ?? () from /lib/x86_64-linux-gnu/libgcc_s.so.1
 * #6  0x00007fab276a34c6 in __GI___pthread_unwind  at ./nptl/unwind.c:130
 * #7  0x00007fab2769bd3a in __do_cancel () at ../sysdeps/nptl/pthreadP.h:280
 * #8  __GI___pthread_exit (value=value@entry=0x0) at ./nptl/pthread_exit.c:36
 * #9  0x000000000052e567 in PyThread_exit_thread () at ../Python/thread_pthread.h:370
 * #10 0x00000000004d60b5 in take_gil at ../Python/ceval_gil.h:224
 * #11 0x00000000004d65f9 in PyEval_RestoreThread  at ../Python/ceval.c:467
 * #12 0x000000000060cce3 in setipaddr  at ../Modules/socketmodule.c:1203
 * #13 0x00000000006101cd in socket_gethostbyname
 */


/* The compiler used for Python 2.7 on Windows doesn't include
   either stdint.h or cstdint.h. Nor does it understand nullptr or have
   std::shared_ptr. = delete, etc Sigh. */
#if defined(_MSC_VER) &&  _MSC_VER <= 1500
typedef unsigned long long uint64_t;
typedef signed long long int64_t;
typedef unsigned int uint32_t;
// C++ defines NULL to be 0, which is ambiguous
// with an integer in certain cases, and won't autoconvert to a
// pointer in other cases.
#define nullptr NULL
#define G_HAS_METHOD_DELETE 0
// Use G_EXPLICIT_OP as the prefix for operator methods
// that should be explicit. Old MSVC doesn't support explicit operator
// methods.
#define G_EXPLICIT_OP
#define G_NOEXCEPT throw()
// This version doesn't support "objects with internal linkage"
// in non-type template arguments. Translation: function pointer
// template arguments cannot be for static functions.
#define G_FP_TMPL_STATIC
#else
// Newer, reasonable compilers implementing C++11 or so.
#include <cstdint>
#define G_HAS_METHOD_DELETE 1
#define G_EXPLICIT_OP explicit
#define G_NOEXCEPT noexcept
# if defined(__clang__)
#  define G_FP_TMPL_STATIC static
# else
// GCC has no problem allowing static function pointers, but emits
// tons of warnings about "whose type uses the anonymous namespace [-Wsubobject-linkage]"
#  define G_FP_TMPL_STATIC
# endif

#endif

#if G_HAS_METHOD_DELETE == 1
#    define G_NO_COPIES_OF_CLS(Cls) private:     \
    Cls(const Cls& other) = delete; \
    Cls& operator=(const Cls& other) = delete

#    define G_NO_ASSIGNMENT_OF_CLS(Cls) private:  \
    Cls& operator=(const Cls& other) = delete

#    define G_NO_COPY_CONSTRUCTOR_OF_CLS(Cls) private: \
    Cls(const Cls& other) = delete;
#else
#    define G_NO_COPIES_OF_CLS(Cls) private: \
    Cls(const Cls& other); \
    Cls& operator=(const Cls& other)

#    define G_NO_ASSIGNMENT_OF_CLS(Cls) private: \
        Cls& operator=(const Cls& other)

#    define G_NO_COPY_CONSTRUCTOR_OF_CLS(Cls) private: \
    Cls(const Cls& other);
#endif

// CAUTION: MSVC is stupidly picky:
//
// "The compiler ignores, without warning, any __declspec keywords
// placed after * or & and in front of the variable identifier in a
// declaration."
// (https://docs.microsoft.com/en-us/cpp/cpp/declspec?view=msvc-160)
//
// So pointer return types must be handled differently (because of the
// trailing *), or you get inscrutable compiler warnings like "error
// C2059: syntax error: ''"

#if defined(__GNUC__) || defined(__clang__)
/* We used to check for GCC 4+ or 3.4+, but those compilers are
   laughably out of date. Just assume they support it. */
#    define GREENLET_NOINLINE_SUPPORTED
#    define GREENLET_NOINLINE(name) __attribute__((noinline)) name
#    define GREENLET_NOINLINE_P(rtype, name) rtype __attribute__((noinline)) name
#    define UNUSED(x) UNUSED_ ## x __attribute__((__unused__))
#elif defined(_MSC_VER)
/* We used to check for  && (_MSC_VER >= 1300) but that's also out of date. */
#    define GREENLET_NOINLINE_SUPPORTED
#    define GREENLET_NOINLINE(name) __declspec(noinline) name
#    define GREENLET_NOINLINE_P(rtype, name) __declspec(noinline) rtype name
#    define UNUSED(x) UNUSED_ ## x
#endif

#if defined(_MSC_VER)
#    define G_NOEXCEPT_WIN32 G_NOEXCEPT
#else
#    define G_NOEXCEPT_WIN32
#endif


#endif
