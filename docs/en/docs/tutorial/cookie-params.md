# Cookie Parameters

You can define Cookie parameters the same way you define `Query` and `Path` parameters.

## Import `Cookie`

First import `Cookie`:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## Declare `Cookie` parameters

Then declare the cookie parameters using the same structure as with `Path` and `Query`.

You can define the default value as well as all the extra validation or annotation parameters:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Technical Details

`Cookie` is a "sister" class of `Path` and `Query`. It also inherits from the same common `Param` class.

But remember that when you import `Query`, `Path`, `Cookie` and others from `fastapi`, those are actually functions that return special classes.

///

/// info

To declare cookies, you need to use `Cookie`, because otherwise the parameters would be interpreted as query parameters.

///

## Recap

Declare cookies with `Cookie`, using the same common pattern as `Query` and `Path`.
