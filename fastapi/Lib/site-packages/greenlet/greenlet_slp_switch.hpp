#ifndef GREENLET_SLP_SWITCH_HPP
#define GREENLET_SLP_SWITCH_HPP

#include "greenlet_compiler_compat.hpp"
#include "greenlet_refs.hpp"

/*
 * the following macros are spliced into the OS/compiler
 * specific code, in order to simplify maintenance.
 */
// We can save about 10% of the time it takes to switch greenlets if
// we thread the thread state through the slp_save_state() and the
// following slp_restore_state() calls from
// slp_switch()->g_switchstack() (which already needs to access it).
//
// However:
//
// that requires changing the prototypes and implementations of the
// switching functions. If we just change the prototype of
// slp_switch() to accept the argument and update the macros, without
// changing the implementation of slp_switch(), we get crashes on
// 64-bit Linux and 32-bit x86 (for reasons that aren't 100% clear);
// on the other hand, 64-bit macOS seems to be fine. Also, 64-bit
// windows is an issue because slp_switch is written fully in assembly
// and currently ignores its argument so some code would have to be
// adjusted there to pass the argument on to the
// ``slp_save_state_asm()`` function (but interestingly, because of
// the calling convention, the extra argument is just ignored and
// things function fine, albeit slower, if we just modify
// ``slp_save_state_asm`()` to fetch the pointer to pass to the
// macro.)
//
// Our compromise is to use a *glabal*, untracked, weak, pointer
// to the necessary thread state during the process of switching only.
// This is safe because we're protected by the GIL, and if we're
// running this code, the thread isn't exiting. This also nets us a
// 10-12% speed improvement.

static greenlet::Greenlet* volatile switching_thread_state = nullptr;


#ifdef GREENLET_NOINLINE_SUPPORTED
extern "C" {
static int GREENLET_NOINLINE(slp_save_state_trampoline)(char* stackref);
static void GREENLET_NOINLINE(slp_restore_state_trampoline)();
}
#define GREENLET_NOINLINE_INIT() \
    do {                         \
    } while (0)
#else
/* force compiler to call functions via pointers */
/* XXX: Do we even want/need to support such compilers? This code path
   is untested on CI. */
extern "C" {
static int (slp_save_state_trampoline)(char* stackref);
static void (slp_restore_state_trampoline)();
}
#define GREENLET_NOINLINE(name) cannot_inline_##name
#define GREENLET_NOINLINE_INIT()                                  \
    do {                                                              \
            slp_save_state_trampoline = GREENLET_NOINLINE(slp_save_state_trampoline); \
            slp_restore_state_trampoline = GREENLET_NOINLINE(slp_restore_state_trampoline); \
    } while (0)
#endif

#define SLP_SAVE_STATE(stackref, stsizediff) \
do {                                                    \
    assert(switching_thread_state);  \
    stackref += STACK_MAGIC;                 \
    if (slp_save_state_trampoline((char*)stackref))    \
        return -1;                                     \
    if (!switching_thread_state->active()) \
        return 1;                                      \
    stsizediff = switching_thread_state->stack_start() - (char*)stackref; \
} while (0)

#define SLP_RESTORE_STATE() slp_restore_state_trampoline()

#define SLP_EVAL
extern "C" {
#define slp_switch GREENLET_NOINLINE(slp_switch)
#include "slp_platformselect.h"
}
#undef slp_switch

#ifndef STACK_MAGIC
#    error \
        "greenlet needs to be ported to this platform, or taught how to detect your compiler properly."
#endif /* !STACK_MAGIC */



#ifdef EXTERNAL_ASM
/* CCP addition: Make these functions, to be called from assembler.
 * The token include file for the given platform should enable the
 * EXTERNAL_ASM define so that this is included.
 */
extern "C" {
intptr_t
slp_save_state_asm(intptr_t* ref)
{
    intptr_t diff;
    SLP_SAVE_STATE(ref, diff);
    return diff;
}

void
slp_restore_state_asm(void)
{
    SLP_RESTORE_STATE();
}

extern int slp_switch(void);
};
#endif

#endif
