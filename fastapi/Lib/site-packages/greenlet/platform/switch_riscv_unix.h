#define STACK_REFPLUS 1

#ifdef SLP_EVAL
#define STACK_MAGIC 0

#define REGS_TO_SAVE "s0", "s1", "s2", "s3", "s4", "s5", \
		     "s6", "s7", "s8", "s9", "s10", "s11", "fs0", "fs1", \
		     "fs2", "fs3", "fs4", "fs5", "fs6", "fs7", "fs8", "fs9", \
		     "fs10", "fs11"

static int
slp_switch(void)
{
  int ret;
  long *stackref, stsizediff;
  __asm__ volatile ("" : : : REGS_TO_SAVE);
  __asm__ volatile ("mv %0, sp" : "=r" (stackref) : );
  {
      SLP_SAVE_STATE(stackref, stsizediff);
      __asm__ volatile (
	  "add sp, sp, %0\n\t"
	  : /* no outputs */
	  : "r" (stsizediff)
	  );
      SLP_RESTORE_STATE();
  }
  __asm__ volatile ("" : : : REGS_TO_SAVE);
  __asm__ volatile ("mv %0, zero" : "=r" (ret) : );
  return ret;
}

#endif
