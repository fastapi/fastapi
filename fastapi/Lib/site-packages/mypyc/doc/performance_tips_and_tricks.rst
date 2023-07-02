.. _performance-tips:

Performance tips and tricks
===========================

Performance optimization is part art, part science. Just using mypyc
in a simple manner will likely make your code faster, but squeezing
the most performance out of your code requires the use of some
techniques we'll summarize below.

Profiling
---------

If you are speeding up existing code, understanding where time is
spent is important. Mypyc speeds up code that you compile. If most of
the time is spent elsewhere, you may come back disappointed. For
example, if you spend 40% of time outside compiled code, even if
compiled code would go 100x faster, overall performance will only be
2.5x faster.

A simple (but often effective) approach is to record the time in
various points of program execution using ``time.time()``, and to
print out elapsed time (or to write it to a log file).

The stdlib modules ``profile`` and ``cProfile`` can provide much more
detailed data. (But these only work well with non-compiled code.)

Avoiding slow libraries
-----------------------

If profiling indicates that a lot of time is spent in the stdlib or
third-party libraries, you still have several options.

First, if most time is spent in a few library features, you can
perhaps easily reimplement them in type-annotated Python, or extract
the relevant code and annotate it. Now it may be easy to compile this
code to speed it up.

Second, you may be able to avoid the library altogether, or use an
alternative, more efficient library to achieve the same purpose.

Type annotations
----------------

As discussed earlier, type annotations are key to major performance
gains. You should at least consider adding annotations to any
performance-critical functions and classes.  It may also be helpful to
annotate code called by this code, even if it's not compiled, since
this may help mypy infer better types in the compile code. If you use
libraries, ensure they have stub files with decent type annotation
coverage. Writing a stub file is often easy, and you only need to
annotate features you use a lot.

If annotating external code or writing stubs feel too burdensome, a
simple workaround is to annotate variables explicitly. For example,
here we call ``acme.get_items()``, but it has no type annotation. We
can use an explicit type annotation for the variable to which we
assign the result::

    from typing import List, Tuple
    import acme

    def work() -> None:
        # Annotate "items" to help mypyc
        items: List[Tuple[int, str]] = acme.get_items()
        for item in items:
            ...  # Do some work here

Without the annotation on ``items``, the type would be ``Any`` (since
``acme`` has no type annotation), resulting in slower, generic
operations being used later in the function.

Avoiding slow Python features
-----------------------------

Mypyc can optimize some features more effectively than others. Here
the difference is sometimes big -- some things only get marginally
faster at best, while others can get 10x faster, or more. Avoiding
these slow features in performance-critical parts of your code can
help a lot.

These are some of the most important things to avoid:

* Using class decorators or metaclasses in compiled code (that aren't
  properly supported by mypyc)

* Heavy reliance on interpreted Python libraries (C extensions are
  usually fine)

These things also tend to be relatively slow:

* Using Python classes and instances of Python classes (native classes
  are much faster)

* Calling decorated functions (``@property``, ``@staticmethod``, and
  ``@classmethod`` are special cased and thus fast)

* Calling nested functions

* Calling functions or methods defined in other compilation units

* Using ``*args`` or ``**kwargs``

* Using generator functions

* Using callable values (i.e. not leveraging early binding to call
  functions or methods)

Nested functions can often be replaced with module-level functions or
methods of native classes.

Callable values and nested functions can sometimes be replaced with an
instance of a native class with a single method only, such as
``call(...)``. You can derive the class from an ABC, if there are
multiple possible functions.

.. note::

   Some slow features will likely get efficient implementations in the
   future. You should check this section every once in a while to see
   if some additional operations are fast.

Using fast native features
--------------------------

Some native operations are particularly quick relative to the
corresponding interpreted operations. Using them as much as possible
may allow you to see 10x or more in performance gains.

Some things are not much (or any) faster in compiled code, such as set
math operations. In contrast, calling a method of a native class is
much faster in compiled code.

If you are used to optimizing for CPython, you might have replaced
some class instances with dictionaries, as they can be
faster. However, in compiled code, this "optimization" would likely
slow down your code.

Similarly, caching a frequently called method in a local variable can
help in CPython, but it can slow things down in compiled code, since
the code won't use :ref:`early binding <early-binding>`::

    def squares(n: int) -> List[int]:
        a = []
        append = a.append  # Not a good idea in compiled code!
        for i in range(n):
            append(i * i)
        return a

Here are examples of features that are fast, in no particular order
(this list is *not* exhaustive):

* Calling compiled functions directly defined in the same compilation
  unit (with positional and/or keyword arguments)

* Calling methods of native classes defined in the same compilation
  unit (with positional and/or keyword arguments)

* Many integer operations

* Many ``float`` operations

* Booleans

* :ref:`Native list operations <list-ops>`, such as indexing,
  ``append``, and list comprehensions

* While loops

* For loops over ranges and lists, and with ``enumerate`` or ``zip``

* Reading dictionary items

* ``isinstance()`` checks against native classes and instances of
  primitive types (and unions of them)

* Accessing local variables

* Accessing attributes of native classes

* Accessing final module-level attributes

* Comparing strings for equality

These features are also fast, but somewhat less so (relative to other
related operations):

* Constructing instances of native classes

* Constructing dictionaries

* Setting dictionary items

* Native :ref:`dict <dict-ops>` and :ref:`set <set-ops>` operations

* Accessing module-level variables

Generally anything documented as a native operation is fast, even if
it's not explicitly mentioned here

Adjusting garbage collection
----------------------------

Compilation does not speed up cyclic garbage collection. If everything
else gets much faster, it's possible that garbage collection will take
a big fraction of time. You can use ``gc.set_threshold()`` to adjust
the garbage collector to run less often::

    import gc

    # Spend less time in gc; do this before significant computation
    gc.set_threshold(150000)

    ...  # Actual work happens here

Fast interpreter shutdown
-------------------------

If you allocate many objects, it's possible that your program spends a
lot of time cleaning up when the Python runtime shuts down. Mypyc
won't speed up the shutdown of a Python process much.

You can call ``os._exit(code)`` to immediately terminate the Python
process, skipping normal cleanup. This can give a nice boost to a
batch process or a command-line tool.

.. note::

   This can be dangerous and can lose data. You need to ensure
   that all streams are flushed and everything is otherwise cleaned up
   properly.

Work smarter
------------

Usually there are many things you can do to improve performance, even
if most tweaks will yield only minor gains. The key to being effective
is to focus on things that give a large gain with a small effort.

For example, low-level optimizations, such as avoiding a nested
function, can be pointless, if you could instead avoid a metaclass --
to allow a key class to be compiled as a native class. The latter
optimization could speed up numerous method calls and attribute
accesses, just like that.
