# Python Types Intro

**Python 3.6+** has support for optional "type hints".

These **"type hints"** are a new syntax (since Python 3.6+) that allow declaring the <abbr title="for example: str, int, float, bool">type</abbr> of a variable.

By declaring types for your variables, editors and tools can give you better support.

This is just a **quick tutorial / refresher** about Python type hints. It covers only the minimum necessary to use them with **FastAPI**... which is actually very little.

**FastAPI** is all based on these type hints, they give it many advantages and benefits.

But even if you never use **FastAPI**, you would benefit from learning a bit about them.

!!! note
    If you are a Python expert, and you already know everything about type hints, skip to the next chapter.

## Motivation

Let's start with a simple example:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

Calling this program outputs:

```
John Doe
```

The function does the following: 

* Takes a `first_name` and `last_name`.
* Converts the first letter of each one to upper case with `title()`.
* <abbr title="Puts them together, as one. With the contents of one after the other.">Concatenates</abbr> them with a space in the middle.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Edit it

It's a very simple program.

But now imagine that you were writing it from scratch.

At some point you would have started the definition of the function, you had the parameters ready...

But then you have to call "that method that converts the first letter to upper case".

Was it `upper`? Was it `uppercase`? `first_uppercase`? `capitalize`?

Then, you try with the old programmer's friend, editor autocompletion.

You type the first parameter of the function, `first_name`, then a dot (`.`) and then hit `Ctrl+Space` to trigger the completion.

But, sadly, you get nothing useful:

<img src="/img/python-types/image01.png">

### Add types

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

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

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

## More motivation

Check this function, it already has type hints:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Because the editor knows the types of the variables, you don't only get completion, you also get error checks:

<img src="/img/python-types/image04.png">

Now you know that you have to fix it, convert `age` to a string with `str(age)`:

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Declaring types

You just saw the main place to declare type hints. As function parameters.

This is also the main place you would use them with **FastAPI**.

### Simple types

You can declare all the standard Python types, not only `str`.

You can use, for example:

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Generic types with type parameters

There are some data structures that can contain other values, like `dict`, `list`, `set` and `tuple`. And the internal values can have their own type too.

To declare those types and the internal types, you can use the standard Python module `typing`.

It exists specifically to support these type hints.

#### `List`

For example, let's define a variable to be a `list` of `str`.

From `typing`, import `List` (with a capital `L`):

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial006.py!}
```

Declare the variable, with the same colon (`:`) syntax.

As the type, put the `List`.

As the list is a type that contains some internal types, you put them in square brackets:

```Python hl_lines="4"
{!../../../docs_src/python_types/tutorial006.py!}
```

!!! tip
    Those internal types in the square brackets are called "type parameters".

    In this case, `str` is the type parameter passed to `List`.

That means: "the variable `items` is a `list`, and each of the items in this list is a `str`".

By doing that, your editor can provide support even while processing items from the list:

<img src="/img/python-types/image05.png">

Without types, that's almost impossible to achieve.

Notice that the variable `item` is one of the elements in the list `items`.

And still, the editor knows it is a `str`, and provides support for that.

#### `Tuple` and `Set`

You would do the same to declare `tuple`s and `set`s:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial007.py!}
```

This means:

* The variable `items_t` is a `tuple` with 3 items, an `int`, another `int`, and a `str`.
* The variable `items_s` is a `set`, and each of its items is of type `bytes`.

#### `Dict`

To define a `dict`, you pass 2 type parameters, separated by commas.

The first type parameter is for the keys of the `dict`.

The second type parameter is for the values of the `dict`:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial008.py!}
```

This means:

* The variable `prices` is a `dict`:
    * The keys of this `dict` are of type `str` (let's say, the name of each item).
    * The values of this `dict` are of type `float` (let's say, the price of each item).

#### `Optional`

You can also use `Optional` to declare that a variable has a type, like `str`, but that it is "optional", which means that it could also be `None`:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

Using `Optional[str]` instead of just `str` will let the editor help you detecting errors where you could be assuming that a value is always a `str`, when it could actually be `None` too.

#### Generic types

These types that take type parameters in square brackets, like:

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...and others.

are called **Generic types** or **Generics**.

### Classes as types

You can also declare a class as the type of a variable.

Let's say you have a class `Person`, with a name:

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Then you can declare a variable to be of type `Person`:

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

And then, again, you get all the editor support:

<img src="/img/python-types/image06.png">

## Pydantic models

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> is a Python library to perform data validation.

You declare the "shape" of the data as classes with attributes.

And each attribute has a type.

Then you create an instance of that class with some values and it will validate the values, convert them to the appropriate type (if that's the case) and give you an object with all the data.

And you get all the editor support with that resulting object.

Taken from the official Pydantic docs:

```Python
{!../../../docs_src/python_types/tutorial011.py!}
```

!!! info
    To learn more about <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic, check its docs</a>.

**FastAPI** is all based on Pydantic.

You will see a lot more of all this in practice in the [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

## Type hints in **FastAPI**

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

!!! info
    If you already went through all the tutorial and came back to see more about types, a good resource is <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">the "cheat sheet" from `mypy`</a>.
