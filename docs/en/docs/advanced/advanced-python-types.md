# Advanced Python Types { #advanced-python-types }

Here are some additional ideas that might be useful when working with Python types.

## Using `Union` or `Optional` { #using-union-or-optional }

If your code for some reason can't use `|`, for example if it's not in a type annotation but in something like `response_model=`, instead of using the vertical bar (`|`) you can use `Union` from `typing`.

For example, you could declare that something could be a `str` or `None`:

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing` also has a shortcut to declare that something could be `None`, with `Optional`.

Here's a tip from my very **subjective** point of view:

* 🚨 Avoid using `Optional[SomeType]`
* Instead ✨ **use `Union[SomeType, None]`** ✨.

Both are equivalent and underneath they are the same, but I would recommend `Union` instead of `Optional` because the word "**optional**" would seem to imply that the value is optional, and it actually means "it can be `None`", even if it's not optional and is still required.

I think `Union[SomeType, None]` is more explicit about what it means.

It's just about the words and names. But those words can affect how you and your teammates think about the code.

As an example, let's take this function:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

The parameter `name` is defined as `Optional[str]`, but it is **not optional**, you cannot call the function without the parameter:

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

The `name` parameter is **still required** (not *optional*) because it doesn't have a default value. Still, `name` accepts `None` as the value:

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

The good news is, in most cases, you will be able to simply use `|` to define unions of types:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

So, normally you don't have to worry about names like `Optional` and `Union`. 😎
