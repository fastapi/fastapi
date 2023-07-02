#define STACK_REFPLUS 1

#ifdef SLP_EVAL
#define STACK_MAGIC 0

#define REGS_TO_SAVE "$9", "$10", "$11", "$12", "$13", "$14", "$15", \
		     "$f2", "$f3", "$f4", "$f5", "$f6", "$f7", "$f8", "$f9"

static int
slp_switch(void)
{
  register int ret;
  register long *stackref, stsizediff;
  __asm__ volatile ("" : : : REGS_TO_SAVE);
  __asm__ volatile ("mov $30, %0" : "=r" (stackref) : );
  {
      SLP_SAVE_STATE(stackref, stsizediff);
      __asm__ volatile (
	  "addq $30, %0, $30\n\t"
	  : /* no outputs */
	  : "r" (stsizediff)
	  );
      SLP_RESTORE_STATE();
  }
  __asm__ volatile ("" : : : REGS_TO_SAVE);
  __asm__ volatile ("mov $31, %0" : "=r" (ret) : );
  return ret;
}

#endif
