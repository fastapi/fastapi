/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 31-May-15 iOS support. Ported from arm32. Proton <feisuzhu@163.com>
 *
 * NOTES
 *
 *   It is not possible to detect if fp is used or not, so the supplied
 *   switch function needs to support it, so that you can remove it if
 *   it does not apply to you.
 *
 * POSSIBLE ERRORS
 *
 *   "fp cannot be used in asm here"
 *
 *   - Try commenting out "fp" in REGS_TO_SAVE.
 *
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

#define STACK_MAGIC 0
#define REG_SP "sp"
#define REG_SPSP "sp,sp"
#define REG_FP "r7"
#define REG_FPFP "r7,r7"
#define REGS_TO_SAVE_GENERAL "r4", "r5", "r6", "r8", "r10", "r11", "lr"
#define REGS_TO_SAVE REGS_TO_SAVE_GENERAL, "d8", "d9", "d10", "d11", \
                                           "d12", "d13", "d14", "d15"

static int
#ifdef __GNUC__
__attribute__((optimize("no-omit-frame-pointer")))
#endif
slp_switch(void)
{
        void *fp;
        register int *stackref, stsizediff, result;
        __asm__ volatile ("" : : : REGS_TO_SAVE);
        __asm__ volatile ("str " REG_FP ",%0" : "=m" (fp));
        __asm__ ("mov %0," REG_SP : "=r" (stackref));
        {
                SLP_SAVE_STATE(stackref, stsizediff);
                __asm__ volatile (
                    "add " REG_SPSP ",%0\n"
                    "add " REG_FPFP ",%0\n"
                    :
                    : "r" (stsizediff)
                    : REGS_TO_SAVE /* Clobber registers, force compiler to
                                    * recalculate address of void *fp from REG_SP or REG_FP */
                );
                SLP_RESTORE_STATE();
        }
        __asm__ volatile (
            "ldr " REG_FP ", %1\n\t"
            "mov %0, #0"
            : "=r" (result)
            : "m" (fp)
            : REGS_TO_SAVE /* Force compiler to restore saved registers after this */
        );
        return result;
}

#endif
