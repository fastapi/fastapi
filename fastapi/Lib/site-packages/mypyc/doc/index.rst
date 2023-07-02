.. mypyc documentation master file, created by
   sphinx-quickstart on Sun Apr  5 14:01:55 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mypyc documentation!
===============================

Mypyc compiles Python modules to C extensions. It uses standard Python
`type hints
<https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html>`_ to
generate fast code.

.. toctree::
   :maxdepth: 2
   :caption: First steps

   introduction
   getting_started

.. toctree::
   :maxdepth: 2
   :caption: Using mypyc

   using_type_annotations
   native_classes
   differences_from_python
   compilation_units

.. toctree::
   :maxdepth: 2
   :caption: Native operations reference

   native_operations
   int_operations
   bool_operations
   float_operations
   str_operations
   list_operations
   dict_operations
   set_operations
   tuple_operations

.. toctree::
   :maxdepth: 2
   :caption: Advanced topics

   performance_tips_and_tricks

.. toctree::
   :hidden:
   :caption: Project Links

   GitHub <https://github.com/python/mypy>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
