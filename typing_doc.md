# Documentation Metadata in Typing

## Abstract

This document proposes a way to complement docstrings to add additional documentation metadata to Python symbols (classes, functions, methods, variables, parameters), like marking something as "deprecated", based on the same Python language and structure, using type annotations with `Annotated` and decorators.

## Motivation

The current standard method of documenting code APIs in Python is using docstrings. But there's no standard way to add additional metadata like marking something as "deprecated", and there's no standard for how to document parameters in docstrings.

There are several pseudo-standards for the format in these docstrings, and new pseudo-standards can appear easily: numpy, Google, Keras, reST, etc.

All these formats are some specific syntax put inside a string. Because of this, when editing those docstrings, editors can't easily provide support for autocompletion, inline errors for broken syntax, etc.

Editors don't have a way to support all the possible micro languages in the docstrings and show nice user interfaces when developers use libraries with those different formats. They could even add support for some of the syntaxes, but probably not all.

Because the docstring is in a different place in the code than the actual parameters and it requires duplication of information (the parameter name) the information about a parameter is easily in a place in the code quite far away from the declaration of the actual parameter. This means it's easy to refactor a function, remove a parameter, and forget to remove its docs. The same happens when adding a new parameter, it's easy to forget to add the docstring for it.

Editors can't check or ensure the consistency of the parameters and their docs.

Some of these formats tried to account for the lack of type annotations in older Python versions, but now that information doesn't need to be there.

## Rationale

This proposal intends to address these shortcomings by extending and complementing the information in docstrings, keeping backwards compatibility with existing docstrings, and doing it in a way that leverages the Python language and structure, via type annotations with `Annotated` and decorators, and a new function in `typing`.

The reason why this would belong in the standard Python library is because although the implementation would be quite trivial, the actual power and benefit from it would come from being a standard, so that editors and other tools could implement support for it.

## Specification

### `typing.doc`

The main proposal is to have a new function `doc()` in the `typing` module. Even though this is not strictly related to the type annotations, it's expected to go in `Annotated` type annotations, and to interact mainly with type annotations.

There's also the particular benefit to having it in `typing` that it could be implemented in the `typing_extensions` package to have support for older versions of Python.

This `doc()` function would receive several parameters for metadata and documentation. It could be used inside of `Annotated`, or also as a decorator on top of classes, functions, and methods.

* `description: str`: in a parameter, this would be the description of the parameter. In a class, function, or method, it would replace the docstring.
    * This could probably contain markup, like Markdown or reST. As that could be highly debated, that decision is left for a future proposal, to focus here on the main functionality.
* `deprecated: bool`: this would mark a parameter, class, function, or method as deprecated. Editors could display it with a strike-through or other appropriate formatting.
* `discouraged: bool`: this would mark a parameter, class, function, or method as discouraged. Editors could display them similar to `deprecated`. The reason why having a `discouraged` apart from `deprecated` is that there are cases where something is not gonna be removed for backward compatibility, but it shouldn't be used in new code. An example of this is `datetime.utcnow()`.
* `extra: dict`: a dictionary containing any additional metadata that could be useful for developers or library authors.
    * An `extra` parameter instead of `**kwargs` is proposed to allow adding future standard parameters.
* `**kwargs: Any`: allows arbitrary additional keyword args. This gives type checkers the freedom to support experimental parameters without needing to wait for changes in `typing.py`. Type checkers should report errors for any unrecognized parameters. This follows the same pattern designed in [PEP 681 – Data Class Transforms](https://peps.python.org/pep-0681/).

Other possible future parameters could include:

* `version_added: str`: the version of the library where this parameter, class, method, or function was added.
* `blocks: bool`: this would mark a callable as a synchronous blocking call. This way, editors could use it to warn about using it in async contexts directly.
* `example: Any`: an example value for a parameter, or an example of the usage of the class, function, or method.

An example documenting the attributes of a class, or in this case, the keys of a `TypedDict` could look like this:

```python
from typing import Annotated, TypedDict, NotRequired, doc


class User(TypedDict):
    firstname: Annotated[str, doc(description="The user's first name")]
    lastname: Annotated[str, doc(description="The user's last name")]
    name: Annotated[
        NotRequired[str],
        doc(
            description="The user's full name, this field is deprecated",
            deprecated=True,
        ),
    ]
```

An example documenting a function could look like this:

```python
from typing import Annotated, doc

@doc(description="Create a new user in the system")
def create_user(
    lastname: Annotated[
        str, doc(description="The **last name** of the newly created user")
    ],
    *,
    firstname: Annotated[
        str | None,
        doc(description="The **first name** of the newly created user"),
    ] = None,
    name: Annotated[
        str | None,
        doc(
            descrption="The user's full name, this argument is deprecated.",
            deprecated=True,
        ),
    ] = None,
) -> Annotated[User, doc(description="The created user after saving in the database")]:
    """
    Create a new user in the system, it needs the database connection to be already
    initialized.
    """
    pass
```

In this example, the description in the `@doc()` decorator would override the docstring.

Also notice that the parameter `name` is marked as `deprecated`.

This could also be used to add more documentation to symbols in the standard library. For example:

```python
from datetime import datetime
from typing import doc


@doc(discouraged=True)
def utcnow() -> datetime:
    """
    Return the current UTC date and time, with tzinfo None.

    This function is not deprecated for backwards compatibility with legacy code, but
    is discouraged. For new code you should use: `datetime.now(timezone.utc)`.
    """
    return datetime.utcnow()
```

## Rejected Ideas

A possible alternative would be to support and try to push as a standard one of the existing docstring formats. But that would only solve the standardization.

It wouldn't solve any of the other problems, like getting editor support (syntax checks) for library authors, the distance and duplication of information between a parameter definition and its documentation in the docstring, etc.

## Open Issues

Runtime behavior is still not defined. It would probably make sense to have an attribute `__typing_doc__` on the function, method, or class. `__doc__` is already reserved for docstrings.

For parameters, it could include the same object in the same `Annotated` type annotations.

It would probably make sense to have a way to support early adopters. The same way the [`dataclass_transform` had an "Alternate Form"](https://github.com/microsoft/pyright/blob/main/specs/dataclass_transforms.md#alternate-form).

## Copyright

This document is placed in the public domain or under the
CC0-1.0-Universal license, whichever is more permissive.
