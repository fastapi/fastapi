# Documentation Metadata in Typing

## Abstract

This document proposes a way to complement docstrings to add additional documentation to Python symbols using type annotations with `Annotated` (in class attributes, function and method parameters, return values, and variables).

## Motivation

The current standard method of documenting code APIs in Python is using docstrings. But there's no standard way to document parameters in docstrings.

There are several pseudo-standards for the format in these docstrings, and new pseudo-standards can appear easily: numpy, Google, Keras, reST, etc.

All these formats are some specific syntax inside a string. Because of this, when editing those docstrings, editors can't easily provide support for autocompletion, inline errors for broken syntax, etc.

Editors don't have a way to support all the possible micro languages in the docstrings and show nice user interfaces when developers use libraries with those different formats. They could even add support for some of the syntaxes, but probably not all, or not completely.

Because the docstring is in a different place in the code than the actual parameters and it requires duplication of information (the parameter name) the information about a parameter is easily in a place in the code quite far away from the declaration of the actual parameter. This means it's easy to refactor a function, remove a parameter, and forget to remove its docs. The same happens when adding a new parameter, it's easy to forget to add the docstring for it.

Editors can't check or ensure the consistency of the parameters and their docs.

It's not possible to programatically test these docstrings, for example to ensure documentation consistency for the parameters across several similar functions, at least not without implementing a custom syntax parser.

Some of these formats tried to account for the lack of type annotations in older Python versions, but now that information doesn't need to be there.

## Rationale

This proposal intends to address these shortcomings by extending and complementing the information in docstrings, keeping backwards compatibility with existing docstrings, and doing it in a way that leverages the Python language and structure, via type annotations with `Annotated`, and a new function in `typing`.

The reason why this would belong in the standard Python library instead of an external package is because although the implementation would be quite trivial, the actual power and benefit from it would come from being a standard, so that editors and other tools could implement support for it.

This doesn't deprecate current usage of docstrings, it's transparent to common developers (library users), and it's only opt-in for library authors that would like to adopt it.

## Specification

### `typing.doc`

The main proposal is to have a new function `doc()` in the `typing` module. Even though this is not strictly related to the type annotations, it's expected to go in `Annotated` type annotations, and to interact with type annotations.

There's also the particular benefit that it could be implemented in the `typing_extensions` package to have support for older versions of Python.

This `doc()` function would receive one single parameter `documentation` with a documentation string.

This string could be a multi-line string, in which case, when extracted by tools, should be interpreted cleaning up indentation as if using `inspect.cleandoc()`, the same procedure used for docstrings.

This string could probably contain markup, like Markdown or reST. As that could be highly debated, that decision is left for a future proposal, to focus here on the main functionality.

This specification targets static analysis tools and editors, and as such, the value passed to `doc()` should allow static evaluation and analysis. If a developer passes as the value something that requires runtime execution (e.g. a function call) the behavior of static analysis tools is unspecified and they could omit it from their process and results. For static analysis tools to be conformant with this specification they need only to support statically accessible values.

An example documenting the attributes of a class, or in this case, the keys of a `TypedDict`, could look like this:

```python
from typing import Annotated, TypedDict, NotRequired, doc


class User(TypedDict):
    firstname: Annotated[str, doc("The user's first name")]
    lastname: Annotated[str, doc("The user's last name")]
    name: Annotated[
        NotRequired[str],
        doc("The user's full name, this field is deprecated"),
    ]
```

An example documenting the parameters of a function could look like this:

```python
from typing import Annotated, doc


def create_user(
    lastname: Annotated[str, doc("The **last name** of the newly created user")],
    *,
    firstname: Annotated[
        str | None,
        doc("The **first name** of the newly created user"),
    ] = None,
    name: Annotated[
        str | None,
        doc("The user's full name, this argument is deprecated."),
    ] = None,
) -> Annotated[User, doc("The created user after saving in the database")]:
    """
    Create a new user in the system, it needs the database connection to be already
    initialized.
    """
    pass
```

The return of the `doc()` function is an instance of a class that can be checked and used at runtime, defined as:

```Python
from dataclasses import dataclass


@dataclass
class DocInfo:
    documentation: str
```

where the attribute `documentation` contains the same value string passed to the function `doc()`.

### Additional Scenarios

The main scenarios that this proposal intends to cover are described above, and for implementers to be conformant to this specification, they only need to support those scenarios described above.

Here are some additional edge case scenarios with their respective considerations, but implementers are not required to support them.

#### Type Alias

When creating a type alias, like:

```python
Username = Annotated[str, doc("The name of a user in the system")]
```

...the documentation would be considered to be carried by the parameter annotated with `Username`.

So, in a function like:

```Python
def hi(to: Username) -> None: ...
```

...it would be equivalent to:

```Python
def hi(to: Annotated[str, doc("The name of a user in the system")]) -> None: ...
```

Nevertheless, implementers would not be required to support type aliases outside of the final type annotation to be conformant with this specification, as it could require more complex dereferencing logic.

#### Annotating Type Parameters

When annotating type parameters, as in:

```Python
def hi(to: list[Annotated[str, doc("The name of a user in a list")]]) -> None: ...
```

...the documentation in `doc()` would refer to what it is annotating, in this case, each item in the list, not the list itself.

There are currently no practical use cases for documenting type parameters, so implementers are not required to support this scenario to be considered conformant, but it's included for completeness.

#### Annotating Unions

If used in one of the parameters of a union, as in:

```Python
def hi(to: str | Annotated[list[str, doc("List of user names")]]) -> None: ...
```

...again, the documentation in `doc()` would refer to what it is annotating, in this case, this documents the list itself, not its items.

In particular, the documentation would not refer to a single string passed as a parameter, only to a list.

There are currently no practical use cases for documenting unions, so implementers are not required to support this scenario to be considered conformant, but it's included for completeness.

#### Multiple `Annotated`

Continuing with the same idea above, if `Annotated` was used multiple times in the same parameter, `doc()` would refer to the type it is annotating.

So, in an example like:

```Python
def hi(to: Annotated[
        Annotated[str, doc("A user name")] | Annotated[list, doc("A list of user names")],
        doc("Who to say hi to")
    ]) -> None: ...
```

The documentation for the whole parameter `to` would be considered to be "`Who to say hi to`".

The documentation for the case where that parameter `to` is specifically a `str` would be considered to be "`A user name`".

The documentation for the case where that parameter `to` is specifically a `list` would be considered to be "`A list of user names`".

Implementers would only be required to support the top level use case, where the documentation for `to` is considered to be "`Who to say hi to`". They could optionally support having conditional documentation for when the type of the parameter passed is of one type or another, but they are not required to do so.

#### Duplications

If `doc()` is used multiple times in a single `Annotated`, it would be considered invalid usage from the developer, for example:

```Python
def hi(to: Annotated[str, doc("A user name"), doc("The current user name")]) -> None: ...
```

Implementers can consider this invalid and are not required to support this to be considered conformant.

Nevertheless, as it might be difficult to enforce it on developers, implementers can opt to support one of the `doc()` declarations.

In that case, the suggestion would be to support the last one, just because this would support overriding, for example, in:

```Python
User = Annotated[str, doc("The name of a user")]

CurrentUser = Annotated[User, doc("The name of the current user")]
```

Internally, in Python, `CurrentUser` here is equivalent to:

```Python
CurrentUser = Annotated[str, doc("The name of a user"), doc("The name of the current user")]
```

For an implementation that supports the last `doc()` appearance, the above example would be equivalent to:

```Python
def hi(to: Annotated[str, doc("The current user name")]) -> None: ...
```

## Alternate Form

To avoid delaying adoption of this proposal until after the `doc()` function has been added to the typing module, type checkers and tools may support an alternative form `__typing_doc__`. This form can be defined locally without any reliance on the `typing` or `typing_extensions` modules. It allows immediate adoption of the specification by library authors. Type checkers that have not yet adopted this specification will retain their current behavior.

To use this alternate form, library authors should include the following declaration within their type stubs or source files.

```Python
from dataclasses import dataclass


@dataclass
class DocInfo:
    documentation: str


def __typing_doc__(
    documentation: str,
) -> DocInfo:
    return DocInfo(documentation)
```

And then they can use it in the same places they would use `doc()`.

This alternate form can be used by early adopters including libraries, linters, editors, type checkers, documentation generation tools and others.

**Note**: this mimics and blatantly copies the pattern from the early versions of the [`dataclass_transform` specification](https://github.com/microsoft/pyright/blob/main/specs/dataclass_transforms.md#alternate-form).

## Rejected Ideas

### Standardize Current Docstrings

A possible alternative would be to support and try to push as a standard one of the existing docstring formats. But that would only solve the standardization.

It wouldn't solve any of the other problems, like getting editor support (syntax checks) for library authors, the distance and duplication of information between a parameter definition and its documentation in the docstring, etc.

### Extra Metadata and Decorator

An earlier version of this proposal included several parameters for additional metadata, including a way to deprecate parameters. To allow also deprecating functions and classes, it was expected to also be used as a decorator. But this functionality is covered by `typing.deprecated()` in [PEP 702](https://peps.python.org/pep-0702/), so it was dropped from this proposal.

The previously proposed parameters were:

* `description: str`: in a parameter, this would be the description of the parameter. In a class, function, or method, it would replace the docstring.
    * This could probably contain markup, like Markdown or reST. As that could be highly debated, that decision is left for a future proposal, to focus here on the main functionality.
* `deprecated: bool`: this would mark a parameter, class, function, or method as deprecated. Editors could display it with a strike-through or other appropriate formatting.
* `discouraged: bool`: this would mark a parameter, class, function, or method as discouraged. Editors could display them similar to `deprecated`. The reason why having a `discouraged` apart from `deprecated` is that there are cases where something is not gonna be removed for backward compatibility, but it shouldn't be used in new code. An example of this is `datetime.utcnow()`.
* `raises: Mapping[Type[BaseException], str | None]`: in a class, function, or method, this indicates the types of exceptions that could be raised by calling it in they keys of the dictionary. Each value would be the description for each exception, possibly being `None` when the exception has no description. Editors and tooling could show a warning (e.g. a colored underline) if the call is not wrapped in a `try` block or the parent caller doesn't include the same exceptions in its `raises` parameter.
* `extra: dict`: a dictionary containing any additional metadata that could be useful for developers or library authors.
    * An `extra` parameter instead of `**kwargs` is proposed to allow adding future standard parameters.
* `**kwargs: Any`: allows arbitrary additional keyword args. This gives type checkers the freedom to support experimental parameters without needing to wait for changes in `typing.py`. Type checkers should report errors for any unrecognized parameters. This follows the same pattern designed in [PEP 681 – Data Class Transforms](https://peps.python.org/pep-0681/).

A way to declare some of these parameters could still be useful in the future, but taking early feedback on this document, all that was postponed to future proposals. This also shifts the focus from an all-encompasing function `doc()` with multiple parameters to multiple composable functions, having `doc()` handle one single use case: additional documentation in `Annotated`.

This design change also allows better interoperability with other proposals like `typing.deprecated()`, as in the future it could be considered to allow having `typing.deprecated()` also in `Annotated` to deprecate individual parameters, coexisting with `doc()`.

## Open Issues

### Verbosity

The main argument against this would be the increased verbosity.

Nevertheless, this verbosity would not affect end users as they would not see the internal code using `typing.doc()`.

And the cost of dealing with the additional verbosity would only be carried by those library maintainers that decide to opt-in into this feature.

Any authors that decide not to adopt it, are free to continue using docstrings with any particular format they decide, no docstrings at all, etc.

This argument could be analogous to the argument against type annotations in general, as they do indeed increase verbosity, in exchange for their features. But again, as with type annotations, this would be optional and only to be used by those that are willing to take the extra verbosity in exchange for the benefits.

### Doc is not Typing

It could also be argued that documentation is not really part of typing, or that it should live in a different module. Or that this information should not be part of the signature but live in another place (like the docstring).

Nevertheless, type annotations in Python could already be considered, by default, mainly documentation: they carry additional information about variables, parameters, return types, and by default they don't have any runtime behavior.

It could be argued that this proposal extends the type of information that type annotations carry, the same way as [PEP 702](https://peps.python.org/pep-0702/) extends them to include deprecation information.

And as described above, being able to include this in `typing_extensions` to support older versions of Python is a very simple and practical reason why it would make sense to have this as part of `typing`.

### Multiple Standards

Another argument against this would be that it would create another standard, and that there are already several pseudo-standards for docstrings. It could seem better to formalize one of the currently existing standards.

Nevertheless, as stated above, none of those standards cover the general drawbacks of a doctsring-based approach that this proposal solves naturally.

None of the editors have full docstring editing support (even when they have rendering support). Again, this is solved by this proposal just by using standard Python syntax and structures instead of a docstring microsyntax.

The effort required to implement support for this proposal by tools would be minimal compared to that required for alternative docstring-based pseudo-standards, as for this proposal, editors would only need to access an already existing value in their ASTs, instead of writing a parsers for a new string microsyntax.

In the same way, it can be seen that, in many cases, a new standard that takes advantage of new features and solves several problems from previous methods can be worth having. As is the case with the new `pyproject.toml`, `dataclass_transform`, the new typing pipe/union (`|`) operator, and other cases.

### Adoption

As this is a new standard and proposal, it would only make sense if it had interest from the community.

Fortunately there's already interest from several mainstream libraries from several developers and teams, including FastAPI, Typer, SQLModel, Asyncer (from the author of this proposal), Pydantic, Strawberry, and others, from other teams.

There's also interest and support from documentation tools, like [mkdocstrings](https://github.com/mkdocstrings/mkdocstrings), which added support even for an earlier version of this proposal.

All the CPython core developers contacted for early feedback (at least 4) have shown interest and support for this proposal.

Editor developers (VS Code and PyCharm) have shown some interest, while showing concerns about the verbosity of the proposal, although not about the implementation (which is what would affect them the most). And they have shown they would consider adding support for this if it were to become an official standard. In that case, they would only need to add support for rendering, as support for editing, which is normally non-existing for other standards, is already there, as they already support editing standard Python syntax.

### Bike Shedding

I think `doc()` is a good name for the main function. But it might make sense to consider changing the names for the other parts.

The returned class containing info currently named `DocInfo` could instead be named just `Doc`. Although it could make verbal conversations more confusing as it's the same word as the name of the function.

The parameter received by `doc()` currently named `documentation` could instead be named also `doc`, but it would make it more ambiguous in discussions to distinguish when talking about the function and the parameter, although it would simplify the amount of terms, but as these terms refer to different things closely related, it could make sense to have different names.

The parameter received by `doc()` currently named `documentation` could instead be named `value`, but the word "documentation" might convey better the meaning.

The parameter received by `doc()` currently named `documentation` could be a position-only parameter, in which case the name wouldn't matter much. But then there wouldn't be a way to make it match with the `DocInfo` attribute.

The `DocInfo` class has a single attribute `documentation`, this name matches the parameter passed to `doc()`. It could be named something different, like `doc`, but this would mean a mismatch between the `doc()` parameter `documentation` and the equivalent attribute `doc`, and it would mean that in one case (in the function), the term `doc` refers to a function, and in the other case (the resulting class) the term `doc` refers to a string value.

This shows the logic to select the current terms, but it could all be discussed further.

## Copyright

This document is placed in the public domain or under the
CC0-1.0-Universal license, whichever is more permissive.
