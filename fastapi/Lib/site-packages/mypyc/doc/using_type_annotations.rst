.. _using-type-annotations:

Using type annotations
======================

You will get the most out of mypyc if you compile code with precise
type annotations. Not all type annotations will help performance
equally, however. Using types such as :ref:`primitive types
<primitive-types>`, :ref:`native classes <native-class-intro>`,
:ref:`union types <union-types>`, :ref:`trait types <trait-types>`,
and :ref:`tuple types <tuple-types>` as much as possible is a key to
major performance gains over CPython.

In contrast, some other types, including ``Any``, are treated as
:ref:`erased types <erased-types>`.  Operations on erased types use
generic operations that work with arbitrary objects, similar to how
the CPython interpreter works. If you only use erased types, the only
notable benefits over CPython will be the removal of interpreter
overhead (from compilation) and a bit of :ref:`early binding
<early-binding>`, which will usually only give minor performance
gains.

.. _primitive-types:

Primitive types
---------------

The following built-in types are treated as *primitive types* by
mypyc, and many operations on these types have efficient
implementations:

* ``int`` (:ref:`native operations <int-ops>`)
* ``i64`` (:ref:`documentation <native-ints>`, :ref:`native operations <int-ops>`)
* ``i32`` (:ref:`documentation <native-ints>`, :ref:`native operations <int-ops>`)
* ``float`` (:ref:`native operations <float-ops>`)
* ``bool`` (:ref:`native operations <bool-ops>`)
* ``str`` (:ref:`native operations <str-ops>`)
* ``List[T]`` (:ref:`native operations <list-ops>`)
* ``Dict[K, V]`` (:ref:`native operations <dict-ops>`)
* ``Set[T]`` (:ref:`native operations <set-ops>`)
* ``Tuple[T, ...]`` (variable-length tuple; :ref:`native operations <tuple-ops>`)
* ``None``

The link after each type lists all supported native, optimized
operations for the type. You can use all operations supported by
Python, but *native operations* will have custom, optimized
implementations.

Primitive containers
--------------------

Primitive container objects such as ``list`` and ``dict`` don't
maintain knowledge of the item types at runtime -- the item type is
*erased*.

This means that item types are checked when items are accessed, not
when a container is passed as an argument or assigned to another
variable. For example, here we have a runtime type error on the final
line of ``example`` (the ``Any`` type means an arbitrary, unchecked
value)::

    from typing import List, Any

    def example(a: List[Any]) -> None:
        b: List[int] = a  # No error -- items are not checked
        print(b[0])  # Error here -- got str, but expected int

    example(["x"])

.. _native-class-intro:

Native classes
--------------

Classes that get compiled to C extensions are called native
classes. Most common operations on instances of these classes are
optimized, including construction, attribute access and method calls.

Native class definitions look exactly like normal Python class
definitions.  A class is usually native if it's in a compiled module
(though there are some exceptions).

Consider this example:

.. code-block::

   class Point:
       def __init__(self, x: int, y: int) -> None:
           self.x = x
           self.y = y

   def shift(p: Point) -> Point:
       return Point(p.x + 1, p.y + 1)

All operations in the above example use native operations, if the file
is compiled.

Native classes have some notable different from Python classes:

* Only attributes and methods defined in the class body or methods are
  supported.  If you try to assign to an undefined attribute outside
  the class definition, ``AttributeError`` will be raised. This enables
  an efficient memory layout and fast method calls for native classes.

* Native classes usually don't define the ``__dict__`` attribute (they
  don't have an attribute dictionary). This follows from only having
  a specific set of attributes.

* Native classes can't have an arbitrary metaclass or use most class
  decorators.

Native classes only support single inheritance. A limited form of
multiple inheritance is supported through *trait types*. You generally
must inherit from another native class (or ``object``). By default,
you can't inherit a Python class from a native class (but there's
an :ref:`override <inheritance>` to allow that).

See :ref:`native-classes` for more details.

.. _tuple-types:

Tuple types
-----------

Fixed-length
`tuple types <https://mypy.readthedocs.io/en/stable/kinds_of_types.html#tuple-types>`_
such as ``Tuple[int, str]`` are represented
as :ref:`value types <value-and-heap-types>` when stored in variables,
passed as arguments, or returned from functions. Value types are
allocated in the low-level machine stack or in CPU registers, as
opposed to *heap types*, which are allocated dynamically from the
heap.

Like all value types, tuples will be *boxed*, i.e. converted to
corresponding heap types, when stored in Python containers, or passed
to non-native code. A boxed tuple value will be a regular Python tuple
object.

.. _union-types:

Union types
-----------

`Union types <https://mypy.readthedocs.io/en/stable/kinds_of_types.html#union-types>`_
and
`optional types <https://mypy.readthedocs.io/en/stable/kinds_of_types.html#optional-types-and-the-none-type>`_
that contain primitive types, native class types and
trait types are also efficient. If a union type has
:ref:`erased <erased-types>` items, accessing items with
non-erased types is often still quite efficient.

A value with a union types is always :ref:`boxed <value-and-heap-types>`,
even if it contains a value that also has an unboxed representation, such
as an integer or a boolean.

For example, using ``Optional[int]`` is quite efficient, but the value
will always be boxed. A plain ``int`` value will usually be faster, since
it has an unboxed representation.

.. _trait-types:

Trait types
-----------

Trait types enable a form of multiple inheritance for native classes.
A native class can inherit any number of traits.  Trait types are
defined as classes using the ``mypy_extensions.trait`` decorator::

    from mypy_extensions import trait

    @trait
    class MyTrait:
        def method(self) -> None:
            ...

Traits can define methods, properties and attributes. They often
define abstract methods. Traits can be generic.

If a class subclasses both a non-trait class and traits, the traits
must be placed at the end of the base class list::

    class Base: ...

    class Derived(Base, MyTrait, FooTrait):  # OK
        ...

    class Derived2(MyTrait, FooTrait, Base):
        # Error: traits should come last
        ...

Traits have some special properties:

* You shouldn't create instances of traits (though mypyc does not
  prevent it yet).

* Traits can subclass other traits, but they can't subclass non-trait
  classes (other than ``object``).

* Accessing methods or attributes through a trait type is somewhat
  less efficient than through a native class type, but this is much
  faster than through Python class types or other
  :ref:`erased types <erased-types>`.

You need to install ``mypy-extensions`` to use ``@trait``:

.. code-block:: text

    pip install --upgrade mypy-extensions

.. _erased-types:

Erased types
------------

Mypyc supports many other kinds of types as well, beyond those
described above.  However, these types don't have customized
operations, and they are implemented using *type erasure*.  Type
erasure means that all other types are equivalent to untyped values at
runtime, i.e. they are the equivalent of the type ``Any``. Erased
types include these:

* Python classes (including ABCs)

* Non-mypyc extension types and primitive types (including built-in
  types that are not primitives)

* `Callable types <https://mypy.readthedocs.io/en/stable/kinds_of_types.html#callable-types-and-lambdas>`_

* `Type variable types <https://mypy.readthedocs.io/en/stable/generics.html>`_

* Type `Any <https://mypy.readthedocs.io/en/stable/dynamic_typing.html>`_

* Protocol types

Using erased types can still improve performance, since they can
enable better types to be inferred for expressions that use these
types.  For example, a value with type ``Callable[[], int]`` will not
allow native calls. However, the return type is a primitive type, and
we can use fast operations on the return value::

    from typing import Callable

    def call_and_inc(f: Callable[[], int]) -> int:
        # Slow call, since f has an erased type
        n = f()
        # Fast increment; inferred type of n is int (primitive type)
        n += 1
        return n

If the type of the argument ``f`` was ``Any``, the type of ``n`` would
also be ``Any``, resulting in a generic, slower increment operation
being used.

Strict runtime type checking
----------------------------

Compiled code ensures that any variable or expression with a
non-erased type only has compatible values at runtime. This is in
contrast with using *optional static typing*, such as by using mypy,
when type annotations are not enforced at runtime. Mypyc ensures
type safety both statically and at runtime.

``Any`` types and erased types in general can compromise type safety,
and this is by design. Inserting strict runtime type checks for all
possible values would be too expensive and against the goal of
high performance.

.. _value-and-heap-types:

Value and heap types
--------------------

In CPython, memory for all objects is dynamically allocated on the
heap. All Python types are thus *heap types*. In compiled code, some
types are *value types* -- no object is (necessarily) allocated on the
heap.  ``bool``, ``float``, ``None``, :ref:`native integer types <native-ints>`
and fixed-length tuples are value types.

``int`` is a hybrid. For typical integer values, it is a value
type. Large enough integer values, those that require more than 63
bits (or 31 bits on 32-bit platforms) to represent, use a heap-based
representation (same as CPython).

Value types have a few differences from heap types:

* When an instance of a value type is used in a context that expects a
  heap value, for example as a list item, it will transparently switch
  to a heap-based representation (boxing) as needed.

* Similarly, mypyc transparently changes from a heap-based
  representation to a value representation (unboxing).

* Object identity of integers, floating point values and tuples is not
  preserved. You should use ``==`` instead of ``is`` if you are comparing
  two integers, floats or fixed-length tuples.

* When an instance of a subclass of a value type is converted to the
  base type, it is implicitly converted to an instance of the target
  type.  For example, a ``bool`` value assigned to a variable with an
  ``int`` type will be converted to the corresponding integer.

The latter conversion is the only implicit type conversion that
happens in mypyc programs.

Example::

    def example() -> None:
        # A small integer uses the value (unboxed) representation
        x = 5
        # A large integer uses the heap (boxed) representation
        x = 2**500
        # Lists always contain boxed integers
        a = [55]
        # When reading from a list, the object is automatically unboxed
        x = a[0]
        # True is converted to 1 on assignment
        x = True

Since integers and floating point values have a different runtime
representations and neither can represent all the values of the other
type, type narrowing of floating point values through assignment is
disallowed in compiled code. For consistency, mypyc rejects assigning
an integer value to a float variable even in variable initialization.
An explicit conversion is required.

Examples::

    def narrowing(n: int) -> None:
        # Error: Incompatible value representations in assignment
        # (expression has type "int", variable has type "float")
        x: float = 0

        y: float = 0.0  # Ok

        if f():
            y = n  # Error
        if f():
            y = float(n)  # Ok

.. _native-ints:

Native integer types
--------------------

You can use the native integer types ``i64`` (64-bit signed integer)
and ``i32`` (32-bit signed integer) if you know that integer values
will always fit within fixed bounds. These types are faster than the
arbitrary-precision ``int`` type, since they don't require overflow
checks on operations. ``i32`` may also use less memory than ``int``
values. The types are imported from the ``mypy_extensions`` module
(installed via ``pip install mypy_extensions``).

Example::

    from mypy_extensions import i64

    def sum_list(l: list[i64]) -> i64:
        s: i64 = 0
        for n in l:
            s += n
        return s

    # Implicit conversions from int to i64
    print(sum_list([1, 3, 5]))

.. note::

  Since there are no overflow checks when performing native integer
  arithmetic, the above function could result in an overflow or other
  undefined behavior if the sum might not fit within 64 bits.

  The behavior when running as interpreted Python program will be
  different if there are overflows. Declaring native integer types
  have no effect unless code is compiled. Native integer types are
  effectively equivalent to ``int`` when interpreted.

Native integer types have these additional properties:

* Values can be implicitly converted between ``int`` and a native
  integer type (both ways).

* Conversions between different native integer types must be explicit.
  A conversion to a narrower native integer type truncates the value
  without a runtime overflow check.

* If a binary operation (such as ``+``) or an augmented assignment
  (such as ``+=``) mixes native integer and ``int`` values, the
  ``int`` operand is implicitly coerced to the native integer type
  (native integer types are "sticky").

* You can't mix different native integer types in binary
  operations. Instead, convert between types explicitly.

For more information about native integer types, refer to
:ref:`native integer operations <int-ops>`.
