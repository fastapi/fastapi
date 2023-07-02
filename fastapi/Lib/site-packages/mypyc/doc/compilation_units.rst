.. _compilation-units:

Compilation units
=================

When you run mypyc to compile a set of modules, these modules form a
*compilation unit*. Mypyc will use early binding for references within
the compilation unit.

If you run mypyc multiple times to compile multiple sets of modules,
each invocation will result in a new compilation unit. References
between separate compilation units will fall back to late binding,
i.e. looking up names using Python namespace dictionaries. Also, all
calls will use the slower Python calling convention, where arguments
and the return value will be boxed (and potentially unboxed again in
the called function).

For maximal performance, minimize interactions across compilation
units. The simplest way to achieve this is to compile your entire
program as a single compilation unit.
