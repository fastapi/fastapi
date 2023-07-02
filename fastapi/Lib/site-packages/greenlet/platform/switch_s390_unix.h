/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 25-Jan-12  Alexey Borzenkov <snaury@gmail.com>
 *      Fixed Linux/S390 port to work correctly with
 *      different optimization options both on 31-bit
 *      and 64-bit. Thanks to Stefan Raabe for lots
 *      of testing.
 * 24-Nov-02  Christian Tismer  <tismer@tismer.com>
 *      needed to add another magic constant to insure
 *      that f in slp_eval_frame(PyFrameObject *f)
 *      STACK_REFPLUS will probably be 1 in most cases.
 *      gets included into the saved stack area.
 * 06-Oct-02  Gustavo Niemeyer <niemeyer@conectiva.com>
 *      Ported to Linux/S390.
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

#ifdef __s390x__
#define STACK_MAGIC 20 /* 20 * 8 = 160 bytes of function call area */
#else
#define STACK_MAGIC 24 /* 24 * 4 = 96 bytes of function call area */
#endif

/* Technically, r11-r13 also need saving, but function prolog starts
   with stm(g) and since there are so many saved registers already
   it won't be optimized, resulting in all r6-r15 being saved */
#define REGS_TO_SAVE "r6", "r7", "r8", "r9", "r10", "r14", \
		     "f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", \
		     "f8", "f9", "f10", "f11", "f12", "f13", "f14", "f15"

static int
slp_switch(void)
{
    register int ret;
    register long *stackref, stsizediff;
    __asm__ volatile ("" : : : REGS_TO_SAVE);
#ifdef __s390x__
    __asm__ volatile ("lgr %0, 15" : "=r" (stackref) : );
#else
    __asm__ volatile ("lr %0, 15" : "=r" (stackref) : );
#endif
    {
        SLP_SAVE_STATE(stackref, stsizediff);
/* N.B.
   r11 may be used as the frame pointer, and in that case it cannot be
   clobbered and needs offsetting just like the stack pointer (but in cases
   where frame pointer isn't used we might clobber it accidentally). What's
   scary is that r11 is 2nd (and even 1st when GOT is used) callee saved
   register that gcc would chose for surviving function calls. However,
   since r6-r10 are clobbered above, their cost for reuse is reduced, so
   gcc IRA will chose them over r11 (not seeing r11 is implicitly saved),
   making it relatively safe to offset in all cases. :) */
        __asm__ volatile (
#ifdef __s390x__
            "agr 15, %0\n\t"
            "agr 11, %0"
#else
            "ar 15, %0\n\t"
            "ar 11, %0"
#endif
            : /* no outputs */
            : "r" (stsizediff)
            );
        SLP_RESTORE_STATE();
    }
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    __asm__ volatile ("lhi %0, 0" : "=r" (ret) : );
    return ret;
}

#endif

/*
 * further self-processing support
 */

/* 
 * if you want to add self-inspection tools, place them
 * here. See the x86_msvc for the necessary defines.
 * These features are highly experimental und not
 * essential yet.
 */
