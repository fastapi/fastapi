/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 24-Nov-02  Christian Tismer  <tismer@tismer.com>
 *      needed to add another magic constant to insure
 *      that f in slp_eval_frame(PyFrameObject *f)
 *      STACK_REFPLUS will probably be 1 in most cases.
 *      gets included into the saved stack area.
 * 26-Sep-02  Christian Tismer  <tismer@tismer.com>
 *      again as a result of virtualized stack access,
 *      the compiler used less registers. Needed to
 *      explicit mention registers in order to get them saved.
 *      Thanks to Jeff Senn for pointing this out and help.
 * 17-Sep-02  Christian Tismer  <tismer@tismer.com>
 *      after virtualizing stack save/restore, the
 *      stack size shrunk a bit. Needed to introduce
 *      an adjustment STACK_MAGIC per platform.
 * 15-Sep-02  Gerd Woetzel       <gerd.woetzel@GMD.DE>
 *      slightly changed framework for sparc
 * 01-Mar-02  Christian Tismer  <tismer@tismer.com>
 *      Initial final version after lots of iterations for i386.
 */

#define alloca _alloca

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

#define STACK_MAGIC 0

/* Some magic to quell warnings and keep slp_switch() from crashing when built
   with VC90. Disable global optimizations, and the warning: frame pointer
   register 'ebp' modified by inline assembly code.

   We used to just disable global optimizations ("g") but upstream stackless
   Python, as well as stackman, turn off all optimizations.

References:
https://github.com/stackless-dev/stackman/blob/dbc72fe5207a2055e658c819fdeab9731dee78b9/stackman/platforms/switch_x86_msvc.h
https://github.com/stackless-dev/stackless/blob/main-slp/Stackless/platf/switch_x86_msvc.h
*/
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#pragma optimize("", off) /* so that autos are stored on the stack */
#pragma warning(disable:4731)
#pragma warning(disable:4733) /* disable warning about modifying FS[0] */

/**
 * Most modern compilers and environments handle C++ exceptions without any
 * special help from us. MSVC on 32-bit windows is an exception. There, C++
 * exceptions are dealt with using Windows' Structured Exception Handling
 * (SEH).
 *
 * SEH is implemented as a singly linked list of <function*, prev*> nodes. The
 * head of this list is stored in the Thread Information Block, which itself
 * is pointed to from the FS register. It's the first field in the structure,
 * or offset 0, so we can access it using assembly FS:[0], or the compiler
 * intrinsics and field offset information from the headers (as we do below).
 * Somewhat unusually, the tail of the list doesn't have prev == NULL, it has
 * prev == 0xFFFFFFFF.
 *
 * SEH was designed for C, and traditionally uses the MSVC compiler
 * intrinsincs __try{}/__except{}. It is also utilized for C++ exceptions by
 * MSVC; there, every throw of a C++ exception raises a SEH error with the
 * ExceptionCode 0xE06D7363; the SEH handler list is then traversed to
 * deal with the exception.
 *
 * If the SEH list is corrupt, then when a C++ exception is thrown the program
 * will abruptly exit with exit code 1. This does not use std::terminate(), so
 * std::set_terminate() is useless to debug this.
 *
 * The SEH list is closely tied to the call stack; entering a function that
 * uses __try{} or most C++ functions will push a new handler onto the front
 * of the list. Returning from the function will remove the handler. Saving
 * and restoring the head node of the SEH list (FS:[0]) per-greenlet is NOT
 * ENOUGH to make SEH or exceptions work.
 *
 * Stack switching breaks SEH because the call stack no longer necessarily
 * matches the SEH list. For example, given greenlet A that switches to
 * greenlet B, at the moment of entering greenlet B, we will have any SEH
 * handlers from greenlet A on the SEH list; greenlet B can then add its own
 * handlers to the SEH list. When greenlet B switches back to greenlet A,
 * greenlet B's handlers would still be on the SEH stack, but when switch()
 * returns control to greenlet A, we have replaced the contents of the stack
 * in memory, so all the address that greenlet B added to the SEH list are now
 * invalid: part of the call stack has been unwound, but the SEH list was out
 * of sync with the call stack. The net effect is that exception handling
 * stops working.
 *
 * Thus, when switching greenlets, we need to be sure that the SEH list
 * matches the effective call stack, "cutting out" any handlers that were
 * pushed by the greenlet that switched out and which are no longer valid.
 *
 * The easiest way to do this is to capture the SEH list at the time the main
 * greenlet for a thread is created, and, when initially starting a greenlet,
 * start a new SEH list for it, which contains nothing but the handler
 * established for the new greenlet itself, with the tail being the handlers
 * for the main greenlet. If we then save and restore the SEH per-greenlet,
 * they won't interfere with each others SEH lists. (No greenlet can unwind
 * the call stack past the handlers established by the main greenlet).
 *
 * By observation, a new thread starts with three SEH handlers on the list. By
 * the time we get around to creating the main greenlet, though, there can be
 * many more, established by transient calls that lead to the creation of the
 * main greenlet. Therefore, 3 is a magic constant telling us when to perform
 * the initial slice.
 *
 * All of this can be debugged using a vectored exception handler, which
 * operates independently of the SEH handler list, and is called first.
 * Walking the SEH list at key points can also be helpful.
 *
 * References:
 * https://en.wikipedia.org/wiki/Win32_Thread_Information_Block
 * https://devblogs.microsoft.com/oldnewthing/20100730-00/?p=13273
 * https://docs.microsoft.com/en-us/cpp/cpp/try-except-statement?view=msvc-160
 * https://docs.microsoft.com/en-us/cpp/cpp/structured-exception-handling-c-cpp?view=msvc-160
 * https://docs.microsoft.com/en-us/windows/win32/debug/structured-exception-handling
 * https://docs.microsoft.com/en-us/windows/win32/debug/using-a-vectored-exception-handler
 * https://bytepointer.com/resources/pietrek_crash_course_depths_of_win32_seh.htm
 */
#define GREENLET_NEEDS_EXCEPTION_STATE_SAVED


typedef struct _GExceptionRegistration {
    struct _GExceptionRegistration* prev;
    void* handler_f;
} GExceptionRegistration;

static void
slp_set_exception_state(const void *const seh_state)
{
    // Because the stack from from which we do this is ALSO a handler, and
    // that one we want to keep, we need to relink the current SEH handler
    // frame to point to this one, cutting out the middle men, as it were.
    //
    // Entering a try block doesn't change the SEH frame, but entering a
    // function containing a try block does.
    GExceptionRegistration* current_seh_state = (GExceptionRegistration*)__readfsdword(FIELD_OFFSET(NT_TIB, ExceptionList));
    current_seh_state->prev = (GExceptionRegistration*)seh_state;
}


static GExceptionRegistration*
x86_slp_get_third_oldest_handler()
{
    GExceptionRegistration* a = NULL; /* Closest to the top */
    GExceptionRegistration* b = NULL; /* second */
    GExceptionRegistration* c = NULL;
    GExceptionRegistration* seh_state = (GExceptionRegistration*)__readfsdword(FIELD_OFFSET(NT_TIB, ExceptionList));
    a = b = c = seh_state;

    while (seh_state && seh_state != (GExceptionRegistration*)0xFFFFFFFF) {
        if ((void*)seh_state->prev < (void*)100) {
            fprintf(stderr, "\tERROR: Broken SEH chain.\n");
            return NULL;
        }
        a = b;
        b = c;
        c = seh_state;

        seh_state = seh_state->prev;
    }
    return a ? a : (b ? b : c);
}


static void*
slp_get_exception_state()
{
    // XXX: There appear to be three SEH handlers on the stack already at the
    // start of the thread. Is that a guarantee? Almost certainly not. Yet in
    // all observed cases it has been three. This is consistent with
    // faulthandler off or on, and optimizations off or on. It may not be
    // consistent with other operating system versions, though: we only have
    // CI on one or two versions (don't ask what there are).
    // In theory we could capture the number of handlers on the chain when
    // PyInit__greenlet is called: there are probably only the default
    // handlers at that point (unless we're embedded and people have used
    // __try/__except or a C++ handler)?
    return x86_slp_get_third_oldest_handler();
}

static int
slp_switch(void)
{
    /* MASM syntax is typically reversed from other assemblers.
       It is usually <instruction> <destination> <source>
     */
    int *stackref, stsizediff;
    /* store the structured exception state for this stack */
    DWORD seh_state = __readfsdword(FIELD_OFFSET(NT_TIB, ExceptionList));
    __asm mov stackref, esp;
    /* modify EBX, ESI and EDI in order to get them preserved */
    __asm mov ebx, ebx;
    __asm xchg esi, edi;
    {
        SLP_SAVE_STATE(stackref, stsizediff);
        __asm {
            mov     eax, stsizediff
            add     esp, eax
            add     ebp, eax
        }
        SLP_RESTORE_STATE();
    }
    __writefsdword(FIELD_OFFSET(NT_TIB, ExceptionList), seh_state);
    return 0;
}

/* re-enable ebp warning and global optimizations. */
#pragma optimize("", on)
#pragma warning(default:4731)
#pragma warning(default:4733) /* disable warning about modifying FS[0] */


#endif

/*
 * further self-processing support
 */

/* we have IsBadReadPtr available, so we can peek at objects */
#define STACKLESS_SPY

#ifdef GREENLET_DEBUG

#define CANNOT_READ_MEM(p, bytes) IsBadReadPtr(p, bytes)

static int IS_ON_STACK(void*p)
{
    int stackref;
    int stackbase = ((int)&stackref) & 0xfffff000;
    return (int)p >= stackbase && (int)p < stackbase + 0x00100000;
}

static void
x86_slp_show_seh_chain()
{
    GExceptionRegistration* seh_state = (GExceptionRegistration*)__readfsdword(FIELD_OFFSET(NT_TIB, ExceptionList));
    fprintf(stderr, "====== SEH Chain ======\n");
    while (seh_state && seh_state != (GExceptionRegistration*)0xFFFFFFFF) {
        fprintf(stderr, "\tSEH_chain addr: %p handler: %p prev: %p\n",
                seh_state,
                seh_state->handler_f, seh_state->prev);
        if ((void*)seh_state->prev < (void*)100) {
            fprintf(stderr, "\tERROR: Broken chain.\n");
            break;
        }
        seh_state = seh_state->prev;
    }
    fprintf(stderr, "====== End SEH Chain ======\n");
    fflush(NULL);
    return;
}

//addVectoredExceptionHandler constants:
//CALL_FIRST means call this exception handler first;
//CALL_LAST means call this exception handler last
#define CALL_FIRST 1
#define CALL_LAST 0

LONG WINAPI
GreenletVectorHandler(PEXCEPTION_POINTERS ExceptionInfo)
{
    // We get one of these for every C++ exception, with code
    // E06D7363
    // This is a special value that means "C++ exception from MSVC"
    // https://devblogs.microsoft.com/oldnewthing/20100730-00/?p=13273
    //
    // Install in the module init function with:
    // AddVectoredExceptionHandler(CALL_FIRST, GreenletVectorHandler);
    PEXCEPTION_RECORD ExceptionRecord = ExceptionInfo->ExceptionRecord;

    fprintf(stderr,
            "GOT VECTORED EXCEPTION:\n"
            "\tExceptionCode   : %p\n"
            "\tExceptionFlags  : %p\n"
            "\tExceptionAddr   : %p\n"
            "\tNumberparams    : %ld\n",
            ExceptionRecord->ExceptionCode,
            ExceptionRecord->ExceptionFlags,
            ExceptionRecord->ExceptionAddress,
            ExceptionRecord->NumberParameters
            );
    if (ExceptionRecord->ExceptionFlags & 1) {
        fprintf(stderr,  "\t\tEH_NONCONTINUABLE\n" );
    }
    if (ExceptionRecord->ExceptionFlags & 2) {
        fprintf(stderr,  "\t\tEH_UNWINDING\n" );
    }
    if (ExceptionRecord->ExceptionFlags & 4) {
        fprintf(stderr, "\t\tEH_EXIT_UNWIND\n" );
    }
    if (ExceptionRecord->ExceptionFlags & 8) {
        fprintf(stderr,  "\t\tEH_STACK_INVALID\n" );
    }
    if (ExceptionRecord->ExceptionFlags & 0x10) {
        fprintf(stderr,  "\t\tEH_NESTED_CALL\n" );
    }
    if (ExceptionRecord->ExceptionFlags & 0x20) {
        fprintf(stderr,  "\t\tEH_TARGET_UNWIND\n" );
    }
    if (ExceptionRecord->ExceptionFlags & 0x40) {
        fprintf(stderr,  "\t\tEH_COLLIDED_UNWIND\n" );
    }
    fprintf(stderr, "\n");
    fflush(NULL);
    for(DWORD i = 0; i < ExceptionRecord->NumberParameters; i++) {
        fprintf(stderr, "\t\t\tParam %ld: %lX\n", i, ExceptionRecord->ExceptionInformation[i]);
    }

    if (ExceptionRecord->NumberParameters == 3) {
        fprintf(stderr, "\tAbout to traverse SEH chain\n");
        // C++ Exception records have 3 params.
        x86_slp_show_seh_chain();
    }

    return EXCEPTION_CONTINUE_SEARCH;
}




#endif
