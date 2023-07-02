.. _float-ops:

Native float operations
========================

These ``float`` operations have fast, optimized implementations. Other
floating point operations use generic implementations that are often
slower.

Construction
------------

* Float literal
* ``float(x: int)``
* ``float(x: i64)``
* ``float(x: i32)``
* ``float(x: str)``
* ``float(x: float)`` (no-op)

Operators
---------

* Arithmetic (``+``, ``-``, ``*``, ``/``, ``//``, ``%``)
* Comparisons (``==``, ``!=``, ``<``, etc.)
* Augmented assignment (``x += y``, etc.)

Functions
---------

* ``int(f)``
* ``i32(f)`` (convert to ``i32``)
* ``i64(f)`` (convert to ``i64``)
* ``abs(f)``
* ``math.sin(f)``
* ``math.cos(f)``
* ``math.tan(f)``
* ``math.sqrt(f)``
* ``math.exp(f)``
* ``math.log(f)``
* ``math.floor(f)``
* ``math.ceil(f)``
* ``math.fabs(f)``
* ``math.pow(x, y)``
* ``math.copysign(x, y)``
* ``math.isinf(f)``
* ``math.isnan(f)``
