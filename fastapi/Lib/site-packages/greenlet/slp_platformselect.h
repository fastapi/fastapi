/*
 * Platform Selection for Stackless Python
 */
#ifdef __cplusplus
extern "C" {
#endif
#if   defined(MS_WIN32) && !defined(MS_WIN64) && defined(_M_IX86) && defined(_MSC_VER)
#include "platform/switch_x86_msvc.h" /* MS Visual Studio on X86 */
#elif defined(MS_WIN64) && defined(_M_X64) && defined(_MSC_VER) || defined(__MINGW64__)
#include "platform/switch_x64_msvc.h" /* MS Visual Studio on X64 */
#elif  defined(MS_WIN64) && defined(_M_ARM64)
#include "platform/switch_arm64_msvc.h" /* MS Visual Studio on ARM64 */
#elif defined(__GNUC__) && defined(__amd64__) && defined(__ILP32__)
#include "platform/switch_x32_unix.h" /* gcc on amd64 with x32 ABI */
#elif defined(__GNUC__) && defined(__amd64__)
#include "platform/switch_amd64_unix.h" /* gcc on amd64 */
#elif defined(__GNUC__) && defined(__i386__)
#include "platform/switch_x86_unix.h" /* gcc on X86 */
#elif defined(__GNUC__) && defined(__powerpc64__) && (defined(__linux__) || defined(__FreeBSD__))
#include "platform/switch_ppc64_linux.h" /* gcc on PowerPC 64-bit */
#elif defined(__GNUC__) && defined(__PPC__) && (defined(__linux__) || defined(__FreeBSD__))
#include "platform/switch_ppc_linux.h" /* gcc on PowerPC */
#elif defined(__GNUC__) && defined(__ppc__) && defined(__APPLE__)
#include "platform/switch_ppc_macosx.h" /* Apple MacOS X on PowerPC */
#elif defined(__GNUC__) && defined(__powerpc64__) && defined(_AIX)
#include "platform/switch_ppc64_aix.h" /* gcc on AIX/PowerPC 64-bit */
#elif defined(__GNUC__) && defined(_ARCH_PPC) && defined(_AIX)
#include "platform/switch_ppc_aix.h" /* gcc on AIX/PowerPC */
#elif defined(__GNUC__) && defined(sparc)
#include "platform/switch_sparc_sun_gcc.h" /* SunOS sparc with gcc */
#elif defined(__SUNPRO_C) && defined(sparc) && defined(sun)
#include "platform/switch_sparc_sun_gcc.h" /* SunStudio on amd64 */
#elif defined(__SUNPRO_C) && defined(__amd64__) && defined(sun)
#include "platform/switch_amd64_unix.h" /* SunStudio on amd64 */
#elif defined(__SUNPRO_C) && defined(__i386__) && defined(sun)
#include "platform/switch_x86_unix.h" /* SunStudio on x86 */
#elif defined(__GNUC__) && defined(__s390__) && defined(__linux__)
#include "platform/switch_s390_unix.h"	/* Linux/S390 */
#elif defined(__GNUC__) && defined(__s390x__) && defined(__linux__)
#include "platform/switch_s390_unix.h"	/* Linux/S390 zSeries (64-bit) */
#elif defined(__GNUC__) && defined(__arm__)
#ifdef __APPLE__
#include <TargetConditionals.h>
#endif
#if TARGET_OS_IPHONE
#include "platform/switch_arm32_ios.h" /* iPhone OS on arm32 */
#else
#include "platform/switch_arm32_gcc.h" /* gcc using arm32 */
#endif
#elif defined(__GNUC__) && defined(__mips__) && defined(__linux__)
#include "platform/switch_mips_unix.h" /* Linux/MIPS */
#elif defined(__GNUC__) && defined(__aarch64__)
#include "platform/switch_aarch64_gcc.h" /* Aarch64 ABI */
#elif defined(__GNUC__) && defined(__mc68000__)
#include "platform/switch_m68k_gcc.h" /* gcc on m68k */
#elif defined(__GNUC__) && defined(__csky__)
#include "platform/switch_csky_gcc.h" /* gcc on csky */
#elif defined(__GNUC__) && defined(__riscv)
#include "platform/switch_riscv_unix.h" /* gcc on RISC-V */
#elif defined(__GNUC__) && defined(__alpha__)
#include "platform/switch_alpha_unix.h" /* gcc on DEC Alpha */
#endif
#ifdef __cplusplus
};
#endif
