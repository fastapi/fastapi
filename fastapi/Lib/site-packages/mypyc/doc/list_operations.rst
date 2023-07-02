.. _list-ops:

Native list operations
======================

These ``list`` operations have fast, optimized implementations. Other
list operations use generic implementations that are often slower.

Construction
------------

Construct list with specific items:

* ``[item0, ..., itemN]``

Construct empty list:

* ``[]``
* ``list()``

Construct list from iterable:

* ``list(x: Iterable)``

List comprehensions:

* ``[... for ... in ...]``
* ``[... for ... in ... if ...]``

Operators
---------

* ``lst[n]`` (get item by integer index)
* ``lst[n:m]``, ``lst[n:]``, ``lst[:m]``, ``lst[:]`` (slicing)
* ``lst * n``, ``n * lst``
* ``obj in lst``

Statements
----------

Set item by integer index:

* ``lst[n] = x``

For loop over a list:

* ``for item in lst:``

Methods
-------

* ``lst.append(obj)``
* ``lst.extend(x: Iterable)``
* ``lst.insert(index, obj)``
* ``lst.pop(index=-1)``
* ``lst.remove(obj)``
* ``lst.count(obj)``
* ``lst.index(obj)``
* ``lst.reverse()``
* ``lst.sort()``

Functions
---------

* ``len(lst: list)``
