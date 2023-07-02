.. _tuple-ops:

Native tuple operations
=======================

These ``tuple`` operations have fast, optimized implementations. Other
tuple operations use generic implementations that are often slower.

Unless mentioned otherwise, these operations apply to both fixed-length
tuples and variable-length tuples.

Construction
------------

* ``item0, ..., itemN`` (construct a tuple)
* ``tuple(lst: list)`` (construct a variable-length tuple)
* ``tuple(lst: Iterable)`` (construct a variable-length tuple)

Operators
---------

* ``tup[n]`` (integer index)
* ``tup[n:m]``, ``tup[n:]``, ``tup[:m]`` (slicing)

Statements
----------

* ``item0, ..., itemN = tup`` (for fixed-length tuples)

Functions
---------

* ``len(tup: tuple)``
