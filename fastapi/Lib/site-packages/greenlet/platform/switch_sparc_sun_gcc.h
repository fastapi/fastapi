/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 16-May-15  Alexey Borzenkov <snaury@gmail.com>
 *      Move stack spilling code inside save/restore functions
 * 30-Aug-13  Floris Bruynooghe <flub@devork.be>
        Clean the register windows again before returning.
        This does not clobber the PIC register as it leaves
        the current window intact and is required for multi-
        threaded code to work correctly.
 * 08-Mar-11  Floris Bruynooghe <flub@devork.be>
 *      No need to set return value register explicitly
 *      before the stack and framepointer are adjusted
 *      as none of the other registers are influenced by
 *      this.  Also don't needlessly clean the windows
 *      ('ta %0" :: "i" (ST_CLEAN_WINDOWS)') as that
 *      clobbers the gcc PIC register (%l7).
 * 24-Nov-02  Christian Tismer  <tismer@tismer.com>
 *      needed to add another magic constant to insure
 *      that f in slp_eval_frame(PyFrameObject *f)
 *      STACK_REFPLUS will probably be 1 in most cases.
 *      gets included into the saved stack area.
 * 17-Sep-02  Christian Tismer  <tismer@tismer.com>
 *      after virtualizing stack save/restore, the
 *      stack size shrunk a bit. Needed to introduce
 *      an adjustment STACK_MAGIC per platform.
 * 15-Sep-02  Gerd Woetzel       <gerd.woetzel@GMD.DE>
 *      added support for SunOS sparc with gcc
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL


#define STACK_MAGIC 0


#if defined(__sparcv9)
#define SLP_FLUSHW __asm__ volatile ("flushw")
#else
#define SLP_FLUSHW __asm__ volatile ("ta 3") /* ST_FLUSH_WINDOWS */
#endif

/* On sparc we need to spill register windows inside save/restore functions */
#define SLP_BEFORE_SAVE_STATE() SLP_FLUSHW
#define SLP_BEFORE_RESTORE_STATE() SLP_FLUSHW


static int
slp_switch(void)
{
    register int err;
    register int *stackref, stsizediff;

    /* Put current stack pointer into stackref.
     * Register spilling is done in save/restore.
     */
    __asm__ volatile ("mov %%sp, %0" : "=r" (stackref));

    {
        /* Thou shalt put SLP_SAVE_STATE into a local block */
        /* Copy the current stack onto the heap */
        SLP_SAVE_STATE(stackref, stsizediff);

        /* Increment stack and frame pointer by stsizediff */
        __asm__ volatile (
            "add %0, %%sp, %%sp\n\t"
            "add %0, %%fp, %%fp"
            : : "r" (stsizediff));

        /* Copy new stack from it's save store on the heap */
        SLP_RESTORE_STATE();

        __asm__ volatile ("mov %1, %0" : "=r" (err) : "i" (0));
        return err;
    }
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
