You can define Cookie parameters the same way you define `Query` and `Path` parameteres.

## Import `Cookie`

First import `Cookie`:

```Python hl_lines="1"
{!./tutorial/src/cookie-params/tutorial001.py!}
```

## Declare `Cookie` parameteres

Then declare the cookie parameters using the same structure as with `Path` and `Query`.

The first value is the default value, you can pass all the extra validation or annotation parameteres:

```Python hl_lines="7"
{!./tutorial/src/cookie-params/tutorial001.py!}
```

!!! info
    `Cookie` is a "sister" class of `Path` and `Query`. It also inherits from the same common `Param` class.

!!! info
    To declare cookies, you need to use `Cookie`, because otherwise the parameters would be interpreted as query parameteres.

## Recap

Declare cookies with `Cookie`, using the same common pattern as `Query` and `Path`.
