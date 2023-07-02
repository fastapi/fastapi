/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 2014-01-06  Andreas Schwab  <schwab@linux-m68k.org>
 *      File created.
 */

#ifdef SLP_EVAL

#define STACK_MAGIC 0

#define REGS_TO_SAVE "%d2", "%d3", "%d4", "%d5", "%d6", "%d7", \
		     "%a2", "%a3", "%a4"

static int
slp_switch(void)
{
  int err;
  int *stackref, stsizediff;
  void *fp, *a5;
  __asm__ volatile ("" : : : REGS_TO_SAVE);
  __asm__ volatile ("move.l %%fp, %0" : "=m"(fp));
  __asm__ volatile ("move.l %%a5, %0" : "=m"(a5));
  __asm__ ("move.l %%sp, %0" : "=r"(stackref));
  {
    SLP_SAVE_STATE(stackref, stsizediff);
    __asm__ volatile ("add.l %0, %%sp; add.l %0, %%fp" : : "r"(stsizediff));
    SLP_RESTORE_STATE();
    __asm__ volatile ("clr.l %0" : "=g" (err));
  }
  __asm__ volatile ("move.l %0, %%a5" : : "m"(a5));
  __asm__ volatile ("move.l %0, %%fp" : : "m"(fp));
  __asm__ volatile ("" : : : REGS_TO_SAVE);
  return err;
}

#endif
