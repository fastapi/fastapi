/*
 * this is the internal transfer function.
 *
 * HISTORY
 * 21-Oct-21  Niyas Sait  <niyas.sait@linaro.org>
 *      First version to enable win/arm64 support.
 */

#define STACK_REFPLUS 1
#define STACK_MAGIC 0

/* Use the generic support for an external assembly language slp_switch function. */
#define EXTERNAL_ASM

#ifdef SLP_EVAL
/* This always uses the external masm assembly file. */
#endif