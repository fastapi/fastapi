.. _dict-ops:

Native dict operations
======================

These ``dict`` operations have fast, optimized implementations. Other
dictionary operations use generic implementations that are often slower.

Construction
------------

Construct dict from keys and values:

* ``{key: value,  ...}``

Construct empty dict:

* ``{}``
* ``dict()``

Construct dict from another object:

* ``dict(d: dict)``
* ``dict(x: Iterable)``

Dict comprehensions:

* ``{...: ... for ... in ...}``
* ``{...: ... for ... in ... if ...}``

Operators
---------

* ``d[key]``
* ``value in d``

Statements
----------

* ``d[key] = value``
* ``for key in d:``

Methods
-------

* ``d.get(key)``
* ``d.get(key, default)``
* ``d.keys()``
* ``d.values()``
* ``d.items()``
* ``d.copy()``
* ``d.clear()``
* ``d1.update(d2: dict)``
* ``d.update(x: Iterable)``

Functions
---------

* ``len(d: dict)``
