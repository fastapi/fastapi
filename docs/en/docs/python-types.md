# Type Hints

**Type hints** (also called type annotations) allow you to set the type of a variable by declaring them in function parameters. Type hints save you time trying to remmeber the names of functions associated with various variable types by letting your coding editor do the work for you. FastAPI takes advantage of Python's `typing` library to create reliable editor support and provide quick type checks within a compatible coding language.

This document offers a quick overview of type hinting works for:
* Variables
* Classes
* Pydantic models
* Metadata annotations

## How they work

Suppose you want to write the following function from scratch:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```
  
If you're unable to remember the name of `title()`, you may want to search it using `Ctrl + Space` in your coding editor. However, without type hints, finding the appropriate function becomes more complicated.

<img src="/img/python-types/image01.png">

Looking back to the original parameters:

```Python
    first_name, last_name
```

would become the following with type hints:

```Python
    first_name: str, last_name: str
```

Then the function becomes:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

!!! Type hints vs default values
    Type hints are different from setting a variable's value. 

Now, if you're attempting to write a function in your coding editor, you can navigate through a list of functions associated with your variable's type.

<img src="/img/python-types/image03.png">

Type hints also help your coding editor to spot errors in type consistency faster. For example, take the following function:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Your coding editor would be able to recognize that there's a problem in your code.

<img src="/img/python-types/image04.png">

In this case, the solution is to  convert `age` to a string with `str(age)`.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```


## Declaring types
Simple types are variables that hold only one type, such as `int` or `str`. Generic types are variable types that can hold multiple types, such as `list` or `dict`, within square brakets `[ ]`. Both are declared with simple brackets `( : )` next to the variable's name. To see detailed examples of type hinting, visit <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">the type hinting cheat sheet from `mypy`</a>.

Type hinting works for all variable types for all versions of Python. As Python advances, newer versions come with improved support for type hints. In many cases you won't need `import` to use the `typing` module when declaring type hints. Choosing a more up-to-date version of Python can allow you to take advantage of added simplicity.



## Lists, Tuples, Sets, and Dicts
Sequences can hold multiple values. Below are examples on how to create functions using generic types such as `list`, `tuple`, `set`, and `dict`.

=== "Python 3.9+"

    1. Within your function's parameter, declare your variable's type with a colon `( : )`.
    2. Enter the type (list, tuple, set, or dict).
    3. Enter the internal type (also called type parameter) that your list accepts within square brakets `[ ]`. 

    List
    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial006_py39.py!}
    ```
    
    Tuple or Set
    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial007_py39.py!}
    ```

    Dict
    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial008_py39.py!}
    ```

=== "Python 3.8+"

    1. From `typing`, import `List`, `Tuple`, `Set`, or `Dict` (with capital first letters):

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial006.py!}
    ```

    2. Within your function's parameter, declare your variable's type with a colon `( : )`.
    3. Enter the type (list, tuple, set, or dict).
    4. Enter the internal type (also called type parameter) that your list accepts within square brakets `[ ]`. 

    List
    ```Python hl_lines="4"
    {!> ../../../docs_src/python_types/tutorial006.py!}
    ```
    Tuple or Set
     ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial007.py!}
    ```
    Dict
    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial008.py!}
    ```


## Union

A `union` allows a variable to hold multiple types such as `int` or `str`. Below are examples of setting a variable with multiple types.

=== "Python 3.10+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial008b_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial008b.py!}
    ```

## None
Some variables can hold the value `None`. Below are examples of allowing a variable to take on a type of `None`.

=== "Python 3.10+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial009_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial009.py!}
    ```

=== "Python 3.8+ alternative"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial009b.py!}
    ```

!!! Best practices
    Avoid using `Optional[SomeType]` and instead **use `Union[SomeType, None]`**. Though these both do the same thing, the latter is clearer for other developers to understand your code.



## Classes as types

A class is a blueprint for creating objects. Like with variables, you can also declare a class as the type of a variable.

Let's say you have a class called `Person` with `one_person` being an instance:

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Then you declare the variable `one_person` to be of the type `Person`:

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

Your editor will still recognize your `typing`:

<img src="/img/python-types/image06.png">


## Pydantic models

FastAPI is largely based on <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, a Python library that performs data validation. Pydantic works by validating values of an instance to convert them into an object with the appropriate types for each value. To learn more about Pydantic, <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">visit Pydantic's documentation</a>.

An example from the official Pydantic docs:

=== "Python 3.10+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011_py310.py!}
    ```

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011_py39.py!}
    ```

=== "Python 3.8+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011.py!}
    ```

## Type Hints with Metadata Annotations

Python's `Annotated` library allows you to enter additional metadata in type hints. They are useful for providing FastAPI with more information about how you want your application to behave.

=== "Python 3.9+"

    In Python 3.9, `Annotated` is part of the standard library, so you can import it from `typing`.

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial013_py39.py!}
    ```

=== "Python 3.8+"

    In versions below Python 3.9, you import `Annotated` from `typing_extensions`.

    It will already be installed with **FastAPI**.

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial013.py!}
    ```
