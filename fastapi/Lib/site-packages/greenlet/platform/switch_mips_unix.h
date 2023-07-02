/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 20-Sep-14 Matt Madison <madison@bliss-m.org>
 *      Re-code the saving of the gp register for MIPS64.
 * 05-Jan-08 Thiemo Seufer  <ths@debian.org>
 *      Ported from ppc.
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

#define STACK_MAGIC 0

#define REGS_TO_SAVE "$16", "$17", "$18", "$19", "$20", "$21", "$22", \
       "$23", "$30"
static int
slp_switch(void)
{
    register int err;
    register int *stackref, stsizediff;
#ifdef __mips64
    uint64_t gpsave;
#endif
    __asm__ __volatile__ ("" : : : REGS_TO_SAVE);
#ifdef __mips64
    __asm__ __volatile__ ("sd $28,%0" : "=m" (gpsave) : : );
#endif
    __asm__ ("move %0, $29" : "=r" (stackref) : );
    {
        SLP_SAVE_STATE(stackref, stsizediff);
        __asm__ __volatile__ (
#ifdef __mips64
            "daddu $29, %0\n"
#else
            "addu $29, %0\n"
#endif
            : /* no outputs */
            : "r" (stsizediff)
            );
        SLP_RESTORE_STATE();
    }
#ifdef __mips64
    __asm__ __volatile__ ("ld $28,%0" : : "m" (gpsave) : );
#endif
    __asm__ __volatile__ ("" : : : REGS_TO_SAVE);
    __asm__ __volatile__ ("move %0, $0" : "=r" (err));
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
