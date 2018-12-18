You can define Header parameters the same way you define `Query`, `Path` and `Cookie` parameteres.

## Import `Header`

First import `Header`:

```Python hl_lines="1"
{!./tutorial/src/header_params/tutorial001.py!}
```

## Declare `Header` parameteres

Then declare the header parameters using the same structure as with `Path`, `Query` and `Cookie`.

The first value is the default value, you can pass all the extra validation or annotation parameteres:

```Python hl_lines="7"
{!./tutorial/src/header_params/tutorial001.py!}
```

!!! info
    `Header` is a "sister" class of `Path`, `Query` and `Cookie`. It also inherits from the same common `Param` class.

!!! info
    To declare headers, you need to use `Header`, because otherwise the parameters would be interpreted as query parameteres.

## Automatic conversion

`Header` has a little extra functionality on top of what `Path`, `Query` and `Cookie` provide.

Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (`-`).

But a variable like `user-agent` is invalid in Python.

So, by default, `Header` will convert the parameter names characters from underscore (`_`) to hyphen (`-`) to extract and document the headers.

Also, HTTP headers are case-insensitive, so, you can declare them with standard Python style (also known as "snake_case").

So, you can use `user_agent` as you normally would in Python code, instead of needing to capitalize the first letters as `User_Agent` or something similar.

If for some reason you need to disable automatic conversion of underscores to hyphens, set the parameter `convert_underscores` of `Header` to `False`:

```Python hl_lines="7"
{!./tutorial/src/header_params/tutorial002.py!}
```

!!! warning
    Before setting `convert_underscores` to `False`, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.

## Recap

Declare headeres with `Header`, using the same common pattern as `Query`, `Path` and `Cookie`.

And don't worry about underscores in your variables, **FastAPI** will take care of converting them.
