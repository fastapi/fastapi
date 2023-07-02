Getting started
===============

Here you will learn some basic things you need to know to get started with mypyc.

Prerequisites
-------------

You need a Python C extension development environment. The way to set this up
depends on your operating system.

macOS
*****

Install Xcode command line tools:

.. code-block::

    $ xcode-select --install

Linux
*****

You need a C compiler and CPython headers and libraries. The specifics
of how to install these varies by distribution. Here are instructions for
Ubuntu 18.04, for example:

.. code-block::

    $ sudo apt install python3-dev

Windows
*******

From `Build Tools for Visual Studio 2022 <https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2022>`_, install MSVC C++ build tools for your architecture and a Windows SDK. (latest versions recommended)

Installation
------------

Mypyc is shipped as part of the mypy distribution. Install mypy like
this (you need Python 3.5 or later):

.. code-block::

    $ python3 -m pip install -U mypy

On some systems you need to use this instead:

.. code-block::

    $ python -m pip install -U mypy

Example program
---------------

Let's start with a classic micro-benchmark, recursive fibonacci. Save
this file as ``fib.py``:

.. code-block:: python

   import time

   def fib(n: int) -> int:
       if n <= 1:
           return n
       else:
           return fib(n - 2) + fib(n - 1)

   t0 = time.time()
   fib(32)
   print(time.time() - t0)

Note that we gave the ``fib`` function a type annotation. Without it,
performance won't be as impressive after compilation.

.. note::

   `Mypy documentation
   <https://mypy.readthedocs.io/en/stable/index.html>`_ is a good
   introduction if you are new to type annotations or mypy. Mypyc uses
   mypy to perform type checking and type inference, so some familiarity
   with mypy is very useful.

Compiling and running
---------------------

We can run ``fib.py`` as a regular, interpreted program using CPython:

.. code-block:: console

    $ python3 fib.py
    0.4125328063964844

It took about 0.41s to run on my computer.

Run ``mypyc`` to compile the program to a binary C extension:

.. code-block:: console

    $ mypyc fib.py

This will generate a C extension for ``fib`` in the current working
directory.  For example, on a Linux system the generated file may be
called ``fib.cpython-37m-x86_64-linux-gnu.so``.

Since C extensions can't be run as programs, use ``python3 -c`` to run
the compiled module as a program:

.. code-block:: console

    $ python3 -c "import fib"
    0.04097270965576172

After compilation, the program is about 10x faster. Nice!

.. note::

   ``__name__`` in ``fib.py`` would now be ``"fib"``, not ``"__main__"``.

You can also pass most
`mypy command line options <https://mypy.readthedocs.io/en/stable/command_line.html>`_
to ``mypyc``.

Deleting compiled binary
------------------------

You can manually delete the C extension to get back to an interpreted
version (this example works on Linux):

.. code-block::

    $ rm fib.*.so

Using setup.py
--------------

You can also use ``setup.py`` to compile modules using mypyc. Here is an
example ``setup.py`` file::

    from setuptools import setup

    from mypyc.build import mypycify

    setup(
        name='mylib',
        packages=['mylib'],
        ext_modules=mypycify([
            'mylib/__init__.py',
            'mylib/mod.py',
        ]),
    )

We used ``mypycify(...)`` to specify which files to compile using
mypyc.  Your ``setup.py`` can include additional Python files outside
``mypycify(...)`` that won't be compiled.

Now you can build a wheel (.whl) file for the package::

    python3 setup.py bdist_wheel

The wheel is created under ``dist/``.

You can also compile the C extensions in-place, in the current directory (similar
to using ``mypyc`` to compile modules)::

    python3 setup.py build_ext --inplace

You can include most `mypy command line options
<https://mypy.readthedocs.io/en/stable/command_line.html>`_ in the
list of arguments passed to ``mypycify()``. For example, here we use
the ``--disallow-untyped-defs`` flag to require that all functions
have type annotations::

    ...
    setup(
        name='frobnicate',
        packages=['frobnicate'],
        ext_modules=mypycify([
            '--disallow-untyped-defs',  # Pass a mypy flag
            'frobnicate.py',
        ]),
    )

.. note:

   You may be tempted to use `--check-untyped-defs
   <https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-check-untyped-defs>`_
   to type check functions without type annotations. Note that this
   may reduce performance, due to many transitions between type-checked and unchecked
   code.

Recommended workflow
--------------------

A simple way to use mypyc is to always compile your code after any
code changes, but this can get tedious, especially if you have a lot
of code. Instead, you can do most development in interpreted mode.
This development workflow has worked smoothly for developing mypy and
mypyc (often we forget that we aren't working on a vanilla Python
project):

1. During development, use interpreted mode. This gives you a fast
   edit-run cycle.

2. Use type annotations liberally and use mypy to type check your code
   during development. Mypy and tests can find most errors that would
   break your compiled code, if you have good type annotation
   coverage. (Running mypy is pretty quick.)

3. After you've implemented a feature or a fix, compile your project
   and run tests again, now in compiled mode. Usually nothing will
   break here, assuming your type annotation coverage is good. This
   can happen locally or in a Continuous Integration (CI) job. If you
   have CI, compiling locally may be rarely needed.

4. Release or deploy a compiled version. Optionally, include a
   fallback interpreted version for platforms that mypyc doesn't
   support.

This mypyc workflow only involves minor tweaks to a typical Python
workflow. Most of development, testing and debugging happens in
interpreted mode. Incremental mypy runs, especially when using the
mypy daemon, are very quick (often a few hundred milliseconds).

Next steps
----------

You can sometimes get good results by just annotating your code and
compiling it. If this isn't providing meaningful performance gains, if
you have trouble getting your code to work under mypyc, or if you want
to optimize your code for maximum performance, you should read the
rest of the documentation in some detail.

Here are some specific recommendations, or you can just read the
documentation in order:

* :ref:`using-type-annotations`
* :ref:`native-classes`
* :ref:`differences-from-python`
* :ref:`performance-tips`
