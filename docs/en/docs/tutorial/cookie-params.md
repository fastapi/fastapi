# Cookie Parameters

You can define Cookie parameters the same way you define `Query` and `Path` parameters.

## Import `Cookie`

First import `Cookie`:

=== "Python 3.6 and above"

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="1"
    {!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
    ```

## Declare `Cookie` parameters

Then declare the cookie parameters using the same structure as with `Path` and `Query`.

The first value is the default value, you can pass all the extra validation or annotation parameters:

=== "Python 3.6 and above"

    ```Python hl_lines="9"
    {!> ../../../docs_src/cookie_params/tutorial001.py!}
    ```

=== "Python 3.10 and above"

    ```Python hl_lines="7"
    {!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
    ```

!!! note "Technical Details"
    `Cookie` is a "sister" class of `Path` and `Query`. It also inherits from the same common `Param` class.

    But remember that when you import `Query`, `Path`, `Cookie` and others from `fastapi`, those are actually functions that return special classes.

!!! info
    To declare cookies, you need to use `Cookie`, because otherwise the parameters would be interpreted as query parameters.

## Recap

Declare cookies with `Cookie`, using the same common pattern as `Query` and `Path`.
