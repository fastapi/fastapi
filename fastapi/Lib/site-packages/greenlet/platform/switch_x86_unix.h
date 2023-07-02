/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 3-May-13   Ralf Schmitt  <ralf@systemexit.de>
 *     Add support for strange GCC caller-save decisions
 *     (ported from switch_aarch64_gcc.h)
 * 19-Aug-11  Alexey Borzenkov  <snaury@gmail.com>
 *      Correctly save ebp, ebx and cw
 * 07-Sep-05 (py-dev mailing list discussion)
 *      removed 'ebx' from the register-saved.  !!!! WARNING !!!!
 *      It means that this file can no longer be compiled statically!
 *      It is now only suitable as part of a dynamic library!
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
 *      slightly changed framework for spark
 * 31-Avr-02  Armin Rigo         <arigo@ulb.ac.be>
 *      Added ebx, esi and edi register-saves.
 * 01-Mar-02  Samual M. Rushing  <rushing@ironport.com>
 *      Ported from i386.
 */

#define STACK_REFPLUS 1

#ifdef SLP_EVAL

/* #define STACK_MAGIC 3 */
/* the above works fine with gcc 2.96, but 2.95.3 wants this */
#define STACK_MAGIC 0

#if __GNUC__ > 4 || (__GNUC__ == 4 && __GNUC_MINOR__ >= 5)
# define ATTR_NOCLONE __attribute__((noclone))
#else
# define ATTR_NOCLONE
#endif

static int
slp_switch(void)
{
    int err;
#ifdef _WIN32
    void *seh;
#endif
    void *ebp, *ebx;
    unsigned short cw;
    register int *stackref, stsizediff;
    __asm__ volatile ("" : : : "esi", "edi");
    __asm__ volatile ("fstcw %0" : "=m" (cw));
    __asm__ volatile ("movl %%ebp, %0" : "=m" (ebp));
    __asm__ volatile ("movl %%ebx, %0" : "=m" (ebx));
#ifdef _WIN32
    __asm__ volatile (
        "movl %%fs:0x0, %%eax\n"
        "movl %%eax, %0\n"
        : "=m" (seh)
        :
        : "eax");
#endif
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
        __asm__ volatile ("xorl %%eax, %%eax" : "=a" (err));
    }
#ifdef _WIN32
    __asm__ volatile (
        "movl %0, %%eax\n"
        "movl %%eax, %%fs:0x0\n"
        :
        : "m" (seh)
        : "eax");
#endif
    __asm__ volatile ("movl %0, %%ebx" : : "m" (ebx));
    __asm__ volatile ("movl %0, %%ebp" : : "m" (ebp));
    __asm__ volatile ("fldcw %0" : : "m" (cw));
    __asm__ volatile ("" : : : "esi", "edi");
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
