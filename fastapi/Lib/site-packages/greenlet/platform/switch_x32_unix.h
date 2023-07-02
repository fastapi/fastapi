/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 17-Aug-12  Fantix King <fantix.king@gmail.com>
 *      Ported from amd64.
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

#define STACK_MAGIC 0

#define REGS_TO_SAVE "r12", "r13", "r14", "r15"


static int
slp_switch(void)
{
    void* ebp;
    void* ebx;
    unsigned int csr;
    unsigned short cw;
    register int err;
    register int *stackref, stsizediff;
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    __asm__ volatile ("fstcw %0" : "=m" (cw));
    __asm__ volatile ("stmxcsr %0" : "=m" (csr));
    __asm__ volatile ("movl %%ebp, %0" : "=m" (ebp));
    __asm__ volatile ("movl %%ebx, %0" : "=m" (ebx));
    __asm__ ("movl %%esp, %0" : "=g" (stackref));
    {
        SLP_SAVE_STATE(stackref, stsizediff);
        __asm__ volatile (
            "addl %0, %%esp\n"
            "addl %0, %%ebp\n"
            :
            : "r" (stsizediff)
            );
        SLP_RESTORE_STATE();
    }
    __asm__ volatile ("movl %0, %%ebx" : : "m" (ebx));
    __asm__ volatile ("movl %0, %%ebp" : : "m" (ebp));
    __asm__ volatile ("ldmxcsr %0" : : "m" (csr));
    __asm__ volatile ("fldcw %0" : : "m" (cw));
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    __asm__ volatile ("xorl %%eax, %%eax" : "=a" (err));
    return err;
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
