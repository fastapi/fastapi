#ifdef SLP_EVAL
#define STACK_MAGIC 0
#define REG_FP "r8"
#ifdef __CSKYABIV2__
#define REGS_TO_SAVE_GENERAL "r4", "r5", "r6", "r7", "r9", "r10", "r11", "r15",\
                             "r16", "r17", "r18", "r19", "r20", "r21", "r22",\
                             "r23", "r24", "r25"

#if defined (__CSKY_HARD_FLOAT__) || (__CSKY_VDSP__)
#define REGS_TO_SAVE REGS_TO_SAVE_GENERAL, "vr8", "vr9", "vr10", "vr11", "vr12",\
                                           "vr13", "vr14", "vr15"
#else
#define REGS_TO_SAVE REGS_TO_SAVE_GENERAL
#endif
#else
#define REGS_TO_SAVE "r9", "r10", "r11", "r12", "r13", "r15"
#endif


static int
#ifdef __GNUC__
__attribute__((optimize("no-omit-frame-pointer")))
#endif
slp_switch(void)
{
        register int *stackref, stsizediff;
        int result;

        __asm__ volatile ("" : : : REGS_TO_SAVE);
        __asm__ ("mov %0, sp" : "=r" (stackref));
        {
                SLP_SAVE_STATE(stackref, stsizediff);
                __asm__ volatile (
                    "addu sp,%0\n"
                    "addu "REG_FP",%0\n"
                    :
                    : "r" (stsizediff)
                    );
		
                SLP_RESTORE_STATE();
        }
        __asm__ volatile ("movi %0, 0" : "=r" (result));
        __asm__ volatile ("" : : : REGS_TO_SAVE);

        return result;
}

#endif
