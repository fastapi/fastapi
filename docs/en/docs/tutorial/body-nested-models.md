# Body - Nested Models

With **FastAPI**, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).

## List fields

You can define an attribute to be a subtype. For example, a Python `list`:

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial001.py!}
```

This will make `tags` be a list of items. Although it doesn't declare the type of each of the items.

## List fields with type parameter

But Python has a specific way to declare lists with internal types, or "type parameters":

### Import typing's `List`

First, import `List` from standard Python's `typing` module:

```Python hl_lines="1"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

### Declare a `List` with a type parameter

To declare types that have type parameters (internal types), like `list`, `dict`, `tuple`:

* Import them from the `typing` module
* Pass the internal type(s) as "type parameters" using square brackets: `[` and `]`

```Python
from typing import List

my_list: List[str]
```

That's all standard Python syntax for type declarations.

Use that same standard syntax for model attributes with internal types.

So, in our example, we can make `tags` be specifically a "list of strings":

```Python hl_lines="14"
{!../../../docs_src/body_nested_models/tutorial002.py!}
```

## Set types

But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.

And Python has a special data type for sets of unique items, the `set`.

Then we can import `Set` and declare `tags` as a `set` of `str`:

```Python hl_lines="1  14"
{!../../../docs_src/body_nested_models/tutorial003.py!}
```

With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.

And whenever you output that data, even if the source had duplicates, it will be output as a set of unique items.

And it will be annotated / documented accordingly too.

## Nested Models

Each attribute of a Pydantic model has a type.

But that type can itself be another Pydantic model.

So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.

All that, arbitrarily nested.

### Define a submodel

For example, we can define an `Image` model:

```Python hl_lines="9-11"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

### Use the submodel as a type

And then we can use it as the type of an attribute:

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial004.py!}
```

This would mean that **FastAPI** would expect a body similar to:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

Again, doing just that declaration, with **FastAPI** you get:

* Editor support (completion, etc), even for nested models
* Data conversion
* Data validation
* Automatic documentation

## Special types and validation

Apart from normal singular types like `str`, `int`, `float`, etc. You can use more complex singular types that inherit from `str`.

To see all the options you have, checkout the docs for <a href="https://pydantic-docs.helpmanual.io/usage/types/" class="external-link" target="_blank">Pydantic's exotic types</a>. You will see some examples in the next chapter.

For example, as in the `Image` model we have a `url` field, we can declare it to be instead of a `str`, a Pydantic's `HttpUrl`:

```Python hl_lines="4  10"
{!../../../docs_src/body_nested_models/tutorial005.py!}
```

The string will be checked to be a valid URL, and documented in JSON Schema / OpenAPI as such.

## Attributes with lists of submodels

You can also use Pydantic models as subtypes of `list`, `set`, etc:

```Python hl_lines="20"
{!../../../docs_src/body_nested_models/tutorial006.py!}
```

This will expect (convert, validate, document, etc) a JSON body like:

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

!!! info
    Notice how the `images` key now has a list of image objects.

## Deeply nested models

You can define arbitrarily deeply nested models:

```Python hl_lines="9  14  20  23  27"
{!../../../docs_src/body_nested_models/tutorial007.py!}
```

!!! info
    Notice how `Offer` has a list of `Item`s, which in turn have an optional list of `Image`s

## Bodies of pure lists

If the top level value of the JSON body you expect is a JSON `array` (a Python `list`), you can declare the type in the parameter of the function, the same as in Pydantic models:

```Python
images: List[Image]
```

as in:

```Python hl_lines="15"
{!../../../docs_src/body_nested_models/tutorial008.py!}
```

## Editor support everywhere

And you get editor support everywhere.

Even for items inside of lists:

<img src="/img/tutorial/body-nested-models/image01.png">

You couldn't get this kind of editor support if you were working directly with `dict` instead of Pydantic models.

But you don't have to worry about them either, incoming dicts are converted automatically and your output is converted automatically to JSON too.

## Bodies of arbitrary `dict`s

You can also declare a body as a `dict` with keys of some type and values of other type.

Without having to know beforehand what are the valid field/attribute names (as would be the case with Pydantic models).

This would be useful if you want to receive keys that you don't already know.

---

Other useful case is when you want to have keys of other type, e.g. `int`.

That's what we are going to see here.

In this case, you would accept any `dict` as long as it has `int` keys with `float` values:

```Python hl_lines="9"
{!../../../docs_src/body_nested_models/tutorial009.py!}
```

!!! tip
    Have in mind that JSON only supports `str` as keys.

    But Pydantic has automatic data conversion.

    This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.
    
    And the `dict` you receive as `weights` will actually have `int` keys and `float` values.

## Recap

With **FastAPI** you have the maximum flexibility provided by Pydantic models, while keeping your code simple, short and elegant.

But with all the benefits:

* Editor support (completion everywhere!)
* Data conversion (a.k.a. parsing / serialization)
* Data validation
* Schema documentation
* Automatic docs
