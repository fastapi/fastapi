# Future

This document introduces some ideas for future improvements.

## Basic Optimizations

Implement basic optimizations such as common subexpression elimination and
loop invariant code motion.

Importantly, common subexpression elimination could be used to avoid
redundant type checks.

## Operation-specific Optimizations

Some operations or combinations of successive operations can be
replaced with more efficient operations. Examples:

* If `s` is a string, `s[i] == 'x'` doesn't need to construct the
  intermediate single-character string object `s[i]` but just compare
  the character value to `ord('x')`.

* `a + ':' + b` (two string concetenations) can be implemented as
  single three-operand concatenation that doesn't construct an
  intermediate object.

* `x in {1, 3}` can be translated into `x == 1 or x == 3` (more
  generally we need to evaluate all right-hand-side items).

## Integer Range Analysis

Implement integer range analysis. This can be used in various ways:

* Use untagged representations for some registers.
* Use faster integer arithmetic operations for operations that
  only deal with short integers or that can't overflow.
* Remove redundant list and string index checks.

## Always Defined Attributes

Somehow make it possible to enforce that attributes in a class are always
defined. This makes attribute access faster since we don't need to explicitly
check if the attribute is defined.
