.. _str-ops:

Native string operations
========================

These ``str`` operations have fast, optimized implementations. Other
string operations use generic implementations that are often slower.

Construction
------------

* String literal
* ``str(x: int)``
* ``str(x: object)``

Operators
---------

* Concatenation (``s1 + s2``)
* Indexing (``s[n]``)
* Slicing (``s[n:m]``, ``s[n:]``, ``s[:m]``)
* Comparisons (``==``, ``!=``)
* Augmented assignment (``s1 += s2``)

Methods
-------

* ``s1.endswith(s2: str)``
* ``s.join(x: Iterable)``
* ``s.replace(old: str, new: str)``
* ``s.replace(old: str, new: str, count: int)``
* ``s.split()``
* ``s.split(sep: str)``
* ``s.split(sep: str, maxsplit: int)``
* ``s1.startswith(s2: str)``
