Introduction
============

Mypyc compiles Python modules to C extensions. It uses standard Python
`type hints
<https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html>`_ to
generate fast code.

The compiled language is a strict, *gradually typed* Python variant. It
restricts the use of some dynamic Python features to gain performance,
but it's mostly compatible with standard Python.

Mypyc uses `mypy <https://www.mypy-lang.org/>`_ to perform type
checking and type inference. Most type system features in the stdlib
`typing <https://docs.python.org/3/library/typing.html>`_ module are
supported.

Compiled modules can import arbitrary Python modules and third-party
libraries. You can compile anything from a single performance-critical
module to your entire codebase. You can run the modules you compile
also as normal, interpreted Python modules.

Existing code with type annotations is often **1.5x to 5x** faster
when compiled. Code tuned for mypyc can be **5x to 10x** faster.

Mypyc currently aims to speed up non-numeric code, such as server
applications. Mypyc is also used to compile itself (and mypy).

Why mypyc?
----------

**Easy to get started.** Compiled code has the look and feel of
regular Python code. Mypyc supports familiar Python syntax and idioms.

**Expressive types.** Mypyc fully supports standard Python type hints.
Mypyc has local type inference, generics, optional types, tuple types,
union types, and more. Type hints act as machine-checked
documentation, making code not only faster but also easier to
understand and modify.

**Python ecosystem.** Mypyc runs on top of CPython, the
standard Python implementation. You can use any third-party libraries,
including C extensions, installed with pip. Mypyc uses only valid Python
syntax, so all Python editors and IDEs work perfectly.

**Fast program startup.** Mypyc uses ahead-of-time compilation, so
compilation does not slow down program startup. Slow program startup
is a common issue with JIT compilers.

**Migration path for existing code.** Existing Python code often
requires only minor changes to compile using mypyc.

**Waiting for compilation is optional.** Compiled code also runs as
normal Python code. You can use interpreted Python during development,
with familiar and fast workflows.

**Runtime type safety.** Mypyc protects you from segfaults and memory
corruption. Any unexpected runtime type safety violation is a bug in
mypyc. Runtime values are checked against type annotations. (Without
mypyc, type annotations are ignored at runtime.)

**Find errors statically.** Mypyc uses mypy for static type checking
that helps catch many bugs.

Use cases
---------

**Fix only performance bottlenecks.** Often most time is spent in a few
Python modules or functions. Add type annotations and compile these
modules for easy performance gains.

**Compile it all.** During development you can use interpreted mode,
for a quick edit-run cycle. In releases all non-test code is compiled.
This is how mypy achieved a 4x performance improvement over interpreted
Python.

**Take advantage of existing type hints.** If you already use type
annotations in your code, adopting mypyc will be easier. You've already
done most of the work needed to use mypyc.

**Alternative to a lower-level language.** Instead of writing
performance-critical code in C, C++, Cython or Rust, you may get good
performance while staying in the comfort of Python.

**Migrate C extensions.** Maintaining C extensions is not always fun
for a Python developer. With mypyc you may get performance similar to
the original C, with the convenience of Python.

Differences from Cython
-----------------------

Mypyc targets many similar use cases as Cython. Mypyc does many things
differently, however:

* No need to use non-standard syntax, such as ``cpdef``, or extra
  decorators to get good performance. Clean, normal-looking
  type-annotated Python code can be fast without language extensions.
  This makes it practical to compile entire codebases without a
  developer productivity hit.

* Mypyc has first-class support for features in the ``typing`` module,
  such as tuple types, union types and generics.

* Mypyc has powerful type inference, provided by mypy. Variable type
  annotations are not needed for optimal performance.

* Mypyc fully integrates with mypy for robust and seamless static type
  checking.

* Mypyc performs strict enforcement of type annotations at runtime,
  resulting in better runtime type safety and easier debugging.

Unlike Cython, mypyc doesn't directly support interfacing with C libraries
or speeding up numeric code.

How does it work
----------------

Mypyc uses several techniques to produce fast code:

* Mypyc uses *ahead-of-time compilation* to native code. This removes
  CPython interpreter overhead.

* Mypyc enforces type annotations (and type comments) at runtime,
  raising ``TypeError`` if runtime values don't match annotations.
  Value types only need to be checked in the boundaries between
  dynamic and static typing.

* Compiled code uses optimized, type-specific primitives.

* Mypyc uses *early binding* to resolve called functions and name
  references at compile time. Mypyc avoids many dynamic namespace
  lookups.

* Classes are compiled to *C extension classes*. They use `vtables
  <https://en.wikipedia.org/wiki/Virtual_method_table>`_ for fast
  method calls and attribute access.

* Mypyc treats compiled functions, classes, and attributes declared
  ``Final`` as immutable.

* Mypyc has memory-efficient, unboxed representations for integers and
  booleans.

Development status
------------------

Mypyc is currently alpha software. It's only recommended for
production use cases with careful testing, and if you are willing to
contribute fixes or to work around issues you will encounter.
