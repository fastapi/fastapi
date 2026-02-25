# Python Types Intro { #python-types-intro }

Python has support for optional "type hints" (also called "type annotations").

These **"type hints"** or annotations are a special syntax that allow declaring the <dfn title="for example: str, int, float, bool">type</dfn> of a variable.

By declaring types for your variables, editors and tools can give you better support.

This is just a **quick tutorial / refresher** about Python type hints. It covers only the minimum necessary to use them with **FastAPI**... which is actually very little.

**FastAPI** is all based on these type hints, they give it many advantages and benefits.

But even if you never use **FastAPI**, you would benefit from learning a bit about them.

/// note

If you are a Python expert, and you already know everything about type hints, skip to the next chapter.

///

## Motivation { #motivation }

Let's start with a simple example:

{* ../../docs_src/python_types/tutorial001_py310.py *}

Calling this program outputs:

```
John Doe
```

The function does the following:

* Takes a `first_name` and `last_name`.
* Converts the first letter of each one to upper case with `title()`.
* <dfn title="Puts them together, as one. With the contents of one after the other.">Concatenates</dfn> them with a space in the middle.

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### Edit it { #edit-it }

It's a very simple program.

But now imagine that you were writing it from scratch.

At some point you would have started the definition of the function, you had the parameters ready...

But then you have to call "that method that converts the first letter to upper case".

Was it `upper`? Was it `uppercase`? `first_uppercase`? `capitalize`?

Then, you try with the old programmer's friend, editor autocompletion.

You type the first parameter of the function, `first_name`, then a dot (`.`) and then hit `Ctrl+Space` to trigger the completion.

But, sadly, you get nothing useful:

<img src="/img/python-types/image01.png">

### Add types { #add-types }

Let's modify a single line from the previous version.

We will change exactly this fragment, the parameters of the function, from:

```Python
    first_name, last_name
```

to:

```Python
    first_name: str, last_name: str
```

That's it.

Those are the "type hints":

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

That is not the same as declaring default values like would be with:

```Python
    first_name="john", last_name="doe"
```

It's a different thing.

We are using colons (`:`), not equals (`=`).

And adding type hints normally doesn't change what happens from what would happen without them.

But now, imagine you are again in the middle of creating that function, but with type hints.

At the same point, you try to trigger the autocomplete with `Ctrl+Space` and you see:

<img src="/img/python-types/image02.png">

With that, you can scroll, seeing the options, until you find the one that "rings a bell":

<img src="/img/python-types/image03.png">

## More motivation { #more-motivation }

Check this function, it already has type hints:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

Because the editor knows the types of the variables, you don't only get completion, you also get error checks:

<img src="/img/python-types/image04.png">

Now you know that you have to fix it, convert `age` to a string with `str(age)`:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Declaring types { #declaring-types }

You just saw the main place to declare type hints. As function parameters.

This is also the main place you would use them with **FastAPI**.

### Simple types { #simple-types }

You can declare all the standard Python types, not only `str`.

You can use, for example:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` module { #typing-module }

For some additional use cases, you might need to import some things from the standard library `typing` module, for example when you want to declare that something has "any type", you can use `Any` from `typing`:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Generic types { #generic-types }

Some types can take "type parameters" in square brackets, to define their internal types, for example a "list of strings" would be declared `list[str]`.

These types that can take type parameters are called **Generic types** or **Generics**.

You can use the same builtin types as generics (with square brackets and types inside):

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

For example, let's define a variable to be a `list` of `str`.

Declare the variable, with the same colon (`:`) syntax.

As the type, put `list`.

As the list is a type that contains some internal types, you put them in square brackets:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info

Those internal types in the square brackets are called "type parameters".

In this case, `str` is the type parameter passed to `list`.

///

That means: "the variable `items` is a `list`, and each of the items in this list is a `str`".

By doing that, your editor can provide support even while processing items from the list:

<img src="/img/python-types/image05.png">

Without types, that's almost impossible to achieve.

Notice that the variable `item` is one of the elements in the list `items`.

And still, the editor knows it is a `str`, and provides support for that.

#### Tuple and Set { #tuple-and-set }

You would do the same to declare `tuple`s and `set`s:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

This means:

* The variable `items_t` is a `tuple` with 3 items, an `int`, another `int`, and a `str`.
* The variable `items_s` is a `set`, and each of its items is of type `bytes`.

#### Dict { #dict }

To define a `dict`, you pass 2 type parameters, separated by commas.

The first type parameter is for the keys of the `dict`.

The second type parameter is for the values of the `dict`:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

This means:

* The variable `prices` is a `dict`:
    * The keys of this `dict` are of type `str` (let's say, the name of each item).
    * The values of this `dict` are of type `float` (let's say, the price of each item).

#### Union { #union }

You can declare that a variable can be any of **several types**, for example, an `int` or a `str`.

To define it you use the <dfn title='also called "bitwise or operator", but that meaning is not relevant here'>vertical bar (`|`)</dfn> to separate both types.

This is called a "union", because the variable can be anything in the union of those two sets of types.

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

This means that `item` could be an `int` or a `str`.

#### Possibly `None` { #possibly-none }

You can declare that a value could have a type, like `str`, but that it could also be `None`.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

Using `str | None` instead of just `str` will let the editor help you detect errors where you could be assuming that a value is always a `str`, when it could actually be `None` too.

### Classes as types { #classes-as-types }

You can also declare a class as the type of a variable.

Let's say you have a class `Person`, with a name:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

Then you can declare a variable to be of type `Person`:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

And then, again, you get all the editor support:

<img src="/img/python-types/image06.png">

Notice that this means "`one_person` is an **instance** of the class `Person`".

It doesn't mean "`one_person` is the **class** called `Person`".

## Pydantic models { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> is a Python library to perform data validation.

You declare the "shape" of the data as classes with attributes.

And each attribute has a type.

Then you create an instance of that class with some values and it will validate the values, convert them to the appropriate type (if that's the case) and give you an object with all the data.

And you get all the editor support with that resulting object.

An example from the official Pydantic docs:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info

To learn more about <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, check its docs</a>.

///

**FastAPI** is all based on Pydantic.

You will see a lot more of all this in practice in the [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

## Type Hints with Metadata Annotations { #type-hints-with-metadata-annotations }

Python also has a feature that allows putting **additional <dfn title="Data about the data, in this case, information about the type, e.g. a description.">metadata</dfn>** in these type hints using `Annotated`.

You can import `Annotated` from `typing`.

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python itself doesn't do anything with this `Annotated`. And for editors and other tools, the type is still `str`.

But you can use this space in `Annotated` to provide **FastAPI** with additional metadata about how you want your application to behave.

The important thing to remember is that **the first *type parameter*** you pass to `Annotated` is the **actual type**. The rest, is just metadata for other tools.

For now, you just need to know that `Annotated` exists, and that it's standard Python. 😎

Later you will see how **powerful** it can be.

/// tip

The fact that this is **standard Python** means that you will still get the **best possible developer experience** in your editor, with the tools you use to analyze and refactor your code, etc. ✨

And also that your code will be very compatible with many other Python tools and libraries. 🚀

///

## Type hints in **FastAPI** { #type-hints-in-fastapi }

**FastAPI** takes advantage of these type hints to do several things.

With **FastAPI** you declare parameters with type hints and you get:

* **Editor support**.
* **Type checks**.

...and **FastAPI** uses the same declarations to:

* **Define requirements**: from request path parameters, query parameters, headers, bodies, dependencies, etc.
* **Convert data**: from the request to the required type.
* **Validate data**: coming from each request:
    * Generating **automatic errors** returned to the client when the data is invalid.
* **Document** the API using OpenAPI:
    * which is then used by the automatic interactive documentation user interfaces.

This might all sound abstract. Don't worry. You'll see all this in action in the [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

The important thing is that by using standard Python types, in a single place (instead of adding more classes, decorators, etc), **FastAPI** will do a lot of the work for you.

/// info

If you already went through all the tutorial and came back to see more about types, a good resource is <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">the "cheat sheet" from `mypy`</a>.

///
