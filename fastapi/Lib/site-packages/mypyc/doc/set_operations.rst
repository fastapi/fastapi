.. _set-ops:

Native set operations
======================

These ``set`` operations have fast, optimized implementations. Other
set operations use generic implementations that are often slower.

Construction
------------

Construct set with specific items:

* ``{item0, ..., itemN}``

Construct empty set:

* ``set()``

Construct set from iterable:

* ``set(x: Iterable)``

Set comprehensions:

* ``{... for ... in ...}``
* ``{... for ... in ... if ...}``

Operators
---------

* ``item in s``

Methods
-------

* ``s.add(item)``
* ``s.remove(item)``
* ``s.discard(item)``
* ``s.update(x: Iterable)``
* ``s.clear()``
* ``s.pop()``

Functions
---------

* ``len(s: set)``
