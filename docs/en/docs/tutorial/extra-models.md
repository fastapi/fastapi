# Extra Models { #extra-models }

Continuing with the previous example, it will be common to have more than one related model.

This is especially the case for user models, because:

* The **input model** needs to be able to have a password.
* The **output model** should not have a password.
* The **database model** would probably need to have a hashed password.

/// danger

Never store user's plaintext passwords. Always store a "secure hash" that you can then verify.

If you don't know, you will learn what a "password hash" is in the [security chapters](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.

///

## Multiple models { #multiple-models }

Here's a general idea of how the models could look like with their password fields and the places where they are used:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}


/// info

In Pydantic v1 the method was called `.dict()`, it was deprecated (but still supported) in Pydantic v2, and renamed to `.model_dump()`.

The examples here use `.dict()` for compatibility with Pydantic v1, but you should use `.model_dump()` instead if you can use Pydantic v2.

///

### About `**user_in.dict()` { #about-user-in-dict }

#### Pydantic's `.dict()` { #pydantics-dict }

`user_in` is a Pydantic model of class `UserIn`.

Pydantic models have a `.dict()` method that returns a `dict` with the model's data.

So, if we create a Pydantic object `user_in` like:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

and then we call:

```Python
user_dict = user_in.dict()
```

we now have a `dict` with the data in the variable `user_dict` (it's a `dict` instead of a Pydantic model object).

And if we call:

```Python
print(user_dict)
```

we would get a Python `dict` with:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Unpacking a `dict` { #unpacking-a-dict }

If we take a `dict` like `user_dict` and pass it to a function (or class) with `**user_dict`, Python will "unpack" it. It will pass the keys and values of the `user_dict` directly as key-value arguments.

So, continuing with the `user_dict` from above, writing:

```Python
UserInDB(**user_dict)
```

would result in something equivalent to:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Or more exactly, using `user_dict` directly, with whatever contents it might have in the future:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### A Pydantic model from the contents of another { #a-pydantic-model-from-the-contents-of-another }

As in the example above we got `user_dict` from `user_in.dict()`, this code:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

would be equivalent to:

```Python
UserInDB(**user_in.dict())
```

...because `user_in.dict()` is a `dict`, and then we make Python "unpack" it by passing it to `UserInDB` prefixed with `**`.

So, we get a Pydantic model from the data in another Pydantic model.

#### Unpacking a `dict` and extra keywords { #unpacking-a-dict-and-extra-keywords }

And then adding the extra keyword argument `hashed_password=hashed_password`, like in:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

...ends up being like:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning

The supporting additional functions `fake_password_hasher` and `fake_save_user` are just to demo a possible flow of the data, but they of course are not providing any real security.

///

## Reduce duplication { #reduce-duplication }

Reducing code duplication is one of the core ideas in **FastAPI**.

As code duplication increments the chances of bugs, security issues, code desynchronization issues (when you update in one place but not in the others), etc.

And these models are all sharing a lot of the data and duplicating attribute names and types.

We could do better.

We can declare a `UserBase` model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation, etc).

All the data conversion, validation, documentation, etc. will still work as normally.

That way, we can declare just the differences between the models (with plaintext `password`, with `hashed_password` and without password):

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` or `anyOf` { #union-or-anyof }

You can declare a response to be the `Union` of two or more types, that means, that the response would be any of them.

It will be defined in OpenAPI with `anyOf`.

To do that, use the standard Python type hint <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

/// note

When defining a <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a>, include the most specific type first, followed by the less specific type. In the example below, the more specific `PlaneItem` comes before `CarItem` in `Union[PlaneItem, CarItem]`.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}


### `Union` in Python 3.10 { #union-in-python-3-10 }

In this example we pass `Union[PlaneItem, CarItem]` as the value of the argument `response_model`.

Because we are passing it as a **value to an argument** instead of putting it in a **type annotation**, we have to use `Union` even in Python 3.10.

If it was in a type annotation we could have used the vertical bar, as:

```Python
some_variable: PlaneItem | CarItem
```

But if we put that in the assignment `response_model=PlaneItem | CarItem` we would get an error, because Python would try to perform an **invalid operation** between `PlaneItem` and `CarItem` instead of interpreting that as a type annotation.

## List of models { #list-of-models }

The same way, you can declare responses of lists of objects.

For that, use the standard Python `typing.List` (or just `list` in Python 3.9 and above):

{* ../../docs_src/extra_models/tutorial004_py39.py hl[18] *}


## Response with arbitrary `dict` { #response-with-arbitrary-dict }

You can also declare a response using a plain arbitrary `dict`, declaring just the type of the keys and values, without using a Pydantic model.

This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.

In this case, you can use `typing.Dict` (or just `dict` in Python 3.9 and above):

{* ../../docs_src/extra_models/tutorial005_py39.py hl[6] *}


## Recap { #recap }

Use multiple Pydantic models and inherit freely for each case.

You don't need to have a single data model per entity if that entity must be able to have different "states". As the case with the user "entity" with a state including `password`, `password_hash` and no password.
