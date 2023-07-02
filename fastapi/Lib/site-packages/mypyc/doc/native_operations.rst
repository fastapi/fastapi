Miscellaneous native operations
===============================

This is a list of various non-type-specific operations that have
custom native implementations.  If an operation has no native
implementation, mypyc will use fallback generic implementations that
are often not as fast.

.. note::

  Operations specific to various primitive types are described
  in the following sections.

Operators
---------

* ``x is y`` (this is very fast for all types)

Functions
---------

* ``isinstance(obj, type: type)``
* ``isinstance(obj, type: tuple)``
* ``cast(<type>, obj)``
* ``type(obj)``
* ``len(obj)``
* ``abs(obj)``
* ``id(obj)``
* ``iter(obj)``
* ``next(iter: Iterator)``
* ``hash(obj)``
* ``getattr(obj, attr)``
* ``getattr(obj, attr, default)``
* ``setattr(obj, attr, value)``
* ``hasattr(obj, attr)``
* ``delattr(obj, name)``
* ``slice(start, stop, step)``
* ``globals()``

Method decorators
-----------------

* ``@property``
* ``@staticmethod``
* ``@classmethod``
* ``@abc.abstractmethod``

Statements
----------

These variants of statements have custom implementations:

* ``for ... in seq:`` (for loop over a sequence)
* ``for ... in enumerate(...):``
* ``for ... in zip(...):``
