/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 16-Oct-20  Jesse Gorzinski <jgorzins@us.ibm.com>
 *      Copied from Linux PPC64 implementation
 * 04-Sep-18  Alexey Borzenkov  <snaury@gmail.com>
 *      Workaround a gcc bug using manual save/restore of r30
 * 21-Mar-18  Tulio Magno Quites Machado Filho  <tuliom@linux.vnet.ibm.com>
 *      Added r30 to the list of saved registers in order to fully comply with
 *      both ppc64 ELFv1 ABI and the ppc64le ELFv2 ABI, that classify this
 *      register as a nonvolatile register used for local variables.
 * 21-Mar-18  Laszlo Boszormenyi  <gcs@debian.org>
 *      Save r2 (TOC pointer) manually.
 * 10-Dec-13  Ulrich Weigand  <uweigand@de.ibm.com>
 *	Support ELFv2 ABI.  Save float/vector registers.
 * 09-Mar-12 Michael Ellerman <michael@ellerman.id.au>
 *      64-bit implementation, copied from 32-bit.
 * 07-Sep-05 (py-dev mailing list discussion)
 *      removed 'r31' from the register-saved.  !!!! WARNING !!!!
 *      It means that this file can no longer be compiled statically!
 *      It is now only suitable as part of a dynamic library!
 * 14-Jan-04  Bob Ippolito <bob@redivi.com>
 *      added cr2-cr4 to the registers to be saved.
 *      Open questions: Should we save FP registers?
 *      What about vector registers?
 *      Differences between darwin and unix?
 * 24-Nov-02  Christian Tismer  <tismer@tismer.com>
 *      needed to add another magic constant to insure
 *      that f in slp_eval_frame(PyFrameObject *f)
 *      STACK_REFPLUS will probably be 1 in most cases.
 *      gets included into the saved stack area.
 * 04-Oct-02  Gustavo Niemeyer <niemeyer@conectiva.com>
 *      Ported from MacOS version.
 * 17-Sep-02  Christian Tismer  <tismer@tismer.com>
 *      after virtualizing stack save/restore, the
 *      stack size shrunk a bit. Needed to introduce
 *      an adjustment STACK_MAGIC per platform.
 * 15-Sep-02  Gerd Woetzel       <gerd.woetzel@GMD.DE>
 *      slightly changed framework for sparc
 * 29-Jun-02  Christian Tismer  <tismer@tismer.com>
 *      Added register 13-29, 31 saves. The same way as
 *      Armin Rigo did for the x86_unix version.
 *      This seems to be now fully functional!
 * 04-Mar-02  Hye-Shik Chang  <perky@fallin.lv>
 *      Ported from i386.
 * 31-Jul-12  Trevor Bowen    <trevorbowen@gmail.com>
 *      Changed memory constraints to register only.
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

#define STACK_MAGIC 6

#if defined(__ALTIVEC__)
#define ALTIVEC_REGS \
       "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", \
       "v28", "v29", "v30", "v31",
#else
#define ALTIVEC_REGS
#endif

#define REGS_TO_SAVE "r14", "r15", "r16", "r17", "r18", "r19", "r20",  \
       "r21", "r22", "r23", "r24", "r25", "r26", "r27", "r28", "r29",  \
       "r31",                                                    \
       "fr14", "fr15", "fr16", "fr17", "fr18", "fr19", "fr20", "fr21", \
       "fr22", "fr23", "fr24", "fr25", "fr26", "fr27", "fr28", "fr29", \
       "fr30", "fr31", \
       ALTIVEC_REGS \
       "cr2", "cr3", "cr4"

static int
slp_switch(void)
{
    register int err;
    register long *stackref, stsizediff;
    void * toc;
    void * r30;
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    __asm__ volatile ("std 2, %0" : "=m" (toc));
    __asm__ volatile ("std 30, %0" : "=m" (r30));
    __asm__ ("mr %0, 1" : "=r" (stackref) : );
    {
        SLP_SAVE_STATE(stackref, stsizediff);
        __asm__ volatile (
            "mr 11, %0\n"
            "add 1, 1, 11\n"
            : /* no outputs */
            : "r" (stsizediff)
            : "11"
            );
        SLP_RESTORE_STATE();
    }
    __asm__ volatile ("ld 30, %0" : : "m" (r30));
    __asm__ volatile ("ld 2, %0" : : "m" (toc));
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    __asm__ volatile ("li %0, 0" : "=r" (err));
    return err;
}

#endif
