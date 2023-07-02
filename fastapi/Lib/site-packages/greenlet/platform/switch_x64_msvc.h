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

/* Avoid alloca redefined warning on mingw64 */
#ifndef alloca
#define alloca _alloca
#endif

#define STACK_REFPLUS 1
#define STACK_MAGIC 0

/* Use the generic support for an external assembly language slp_switch function. */
#define EXTERNAL_ASM

#ifdef SLP_EVAL
/* This always uses the external masm assembly file. */
#endif

/*
 * further self-processing support
 */

/* we have IsBadReadPtr available, so we can peek at objects */
/*
#define STACKLESS_SPY

#ifdef IMPLEMENT_STACKLESSMODULE
#include "Windows.h"
#define CANNOT_READ_MEM(p, bytes) IsBadReadPtr(p, bytes)

static int IS_ON_STACK(void*p)
{
    int stackref;
    intptr_t stackbase = ((intptr_t)&stackref) & 0xfffff000;
    return (intptr_t)p >= stackbase && (intptr_t)p < stackbase + 0x00100000;
}

#endif
*/