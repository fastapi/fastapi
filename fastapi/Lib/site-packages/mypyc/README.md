mypyc: Mypy to Python C Extension Compiler
==========================================

**NOTE: We are in the process of moving the mypyc README to the**
**[mypyc repository](https://github.com/mypyc/mypyc)**

**This may be out of date!**

Mypyc is a compiler that compiles mypy-annotated, statically typed
Python modules into CPython C extensions. Currently our primary focus
is on making mypy faster through compilation -- the default mypy wheels
are compiled with mypyc.  Compiled mypy is about 4x faster than
without compilation.

Mypyc compiles what is essentially a Python language variant using "strict"
semantics. This means (among some other things):

 * Most type annotations are enforced at runtime (raising ``TypeError`` on mismatch)

 * Classes are compiled into extension classes without ``__dict__``
   (much, but not quite, like if they used ``__slots__``)

 * Monkey patching doesn't work

 * Instance attributes won't fall back to class attributes if undefined

 * Also there are still a bunch of bad bugs and unsupported features :)

Compiled modules can import arbitrary Python modules, and compiled modules
can be used from other Python modules.  Typically mypyc is used to only
compile modules that contain performance bottlenecks.

You can run compiled modules also as normal, interpreted Python
modules, since mypyc targets valid Python code. This means that
all Python developer tools and debuggers can be used.

macOS Requirements
------------------

* macOS Sierra or later

* Xcode command line tools

* Python 3.5+ from python.org (other versions are untested)

Linux Requirements
------------------

* A recent enough C/C++ build environment

* Python 3.5+

Windows Requirements
--------------------

* Windows has been tested with Windows 10 and MSVC 2017.

* Python 3.5+

Quick Start for Contributors
----------------------------

First clone the mypy git repository:

    $ git clone https://github.com/python/mypy.git
    $ cd mypy

Optionally create a virtualenv (recommended):

    $ python3 -m venv <directory>
    $ source <directory>/bin/activate

Then install the dependencies:

    $ python3 -m pip install -r test-requirements.txt

Now you can run the tests:

    $ pytest -q mypyc

Look at the [issue tracker](https://github.com/mypyc/mypyc/issues)
for things to work on. Please express your interest in working on an
issue by adding a comment before doing any significant work, since
there is a risk of duplicate work.

Note that the issue tracker is hosted on the mypyc GitHub project, not
with mypy itself.

Documentation
-------------

We have some [developer documentation](doc/dev-intro.md).

Development Status and Roadmap
------------------------------

These are the current planned major milestones:

1. [DONE] Support a smallish but useful Python subset. Focus on compiling
   single modules, while the rest of the program is interpreted and does not
   need to be type checked.

2. [DONE] Support compiling multiple modules as a single compilation unit (or
   dynamic linking of compiled modules).  Without this inter-module
   calls will use slower Python-level objects, wrapper functions and
   Python namespaces.

3. [DONE] Mypyc can compile mypy.

4. [DONE] Optimize some important performance bottlenecks.

5. [PARTIALLY DONE] Generate useful errors for code that uses unsupported Python
   features instead of crashing or generating bad code.

6. [DONE] Release a version of mypy that includes a compiled mypy.

7.
    1. More feature/compatibility work. (100% compatibility with Python is distinctly
       an anti-goal, but more than we have now is a good idea.)
    2. [DONE] Support compiling Black, which is a prominent tool that could benefit
       and has maintainer buy-in.
       (Let us know if you maintain another Python tool or library and are
       interested in working with us on this!)
    3. More optimization! Code size reductions in particular are likely to
       be valuable and will speed up mypyc compilation.

8.  We'll see! Adventure is out there!

Future
------

We have some ideas for
[future improvements and optimizations](doc/future.md).
