/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 07-Sep-16 Add clang support using x register naming. Fredrik Fornwall
 * 13-Apr-13 Add support for strange GCC caller-save decisions
 * 08-Apr-13 File creation. Michael Matz
 *
 * NOTES
 *
 * Simply save all callee saved registers
 *
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL
#define STACK_MAGIC 0
#define REGS_TO_SAVE "x19", "x20", "x21", "x22", "x23", "x24", "x25", "x26", \
                     "x27", "x28", "x30" /* aka lr */, \
                     "v8", "v9", "v10", "v11", \
                     "v12", "v13", "v14", "v15"

static int
slp_switch(void)
{
	int err;
	void *fp;
        long *stackref, stsizediff;
        __asm__ volatile ("" : : : REGS_TO_SAVE);
	__asm__ volatile ("str x29, %0" : "=m"(fp) : : );
        __asm__ ("mov %0, sp" : "=r" (stackref));
        {
                SLP_SAVE_STATE(stackref, stsizediff);
                __asm__ volatile (
                    "add sp,sp,%0\n"
                    "add x29,x29,%0\n"
                    :
                    : "r" (stsizediff)
                    );
		SLP_RESTORE_STATE();
		/* SLP_SAVE_STATE macro contains some return statements
		   (of -1 and 1).  It falls through only when
		   the return value of slp_save_state() is zero, which
		   is placed in x0.
		   In that case we (slp_switch) also want to return zero
		   (also in x0 of course).
		   Now, some GCC versions (seen with 4.8) think it's a
		   good idea to save/restore x0 around the call to
		   slp_restore_state(), instead of simply zeroing it
		   at the return below.  But slp_restore_state
		   writes random values to the stack slot used for this
		   save/restore (from when it once was saved above in
		   SLP_SAVE_STATE, when it was still uninitialized), so
		   "restoring" that precious zero actually makes us
		   return random values.  There are some ways to make
		   GCC not use that zero value in the normal return path
		   (e.g. making err volatile, but that costs a little
		   stack space), and the simplest is to call a function
		   that returns an unknown value (which happens to be zero),
		   so the saved/restored value is unused.  */
                /* XXX: This line produces warnings:

                   value size does not match register size specified by the
                   constraint and modifier

                   The suggested fix is to change %0 to %w0.

                   TODO: Validate and change that.
                 */
           __asm__ volatile ("mov %0, #0" : "=r" (err));
        }
        __asm__ volatile ("ldr x29, %0" : : "m" (fp) :);
        __asm__ volatile ("" : : : REGS_TO_SAVE);
        return err;
}

#endif
