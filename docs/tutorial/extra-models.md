Continuing with the previous example, it will be common to have more than one related model.

This is especially the case for user models, because:

* The **input model** needs to be able to have a password.
* The **output model** should do not have a password.
* The **database model** would probably need to have a hashed password.

!!! danger
    Never store user's plaintext passwords. Always store a "secure hash" that you can then verify.

    If you don't know, you will learn what a "password hash" is in the <a href="/tutorial/security/simple-oauth2/#password-hashing" target="_blank">security chapters</a>.

## Multiple models

Here's a general idea of how the models could look like with their password fields and the places where they are used:

```Python hl_lines="8 10 15 21 23 32 34 39 40"
{!./src/extra_models/tutorial001.py!}
```

#### About `**user_dict`

`UserInDB(**user_dict)` means:
    
Pass the keys and values of the `user_dict` directly as key-value arguments, equivalent to:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

And then adding the extra `hashed_password=hashed_password`, like in:

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

!!! warning
    The supporting additional functions are just to demo a possible flow of the data, but they of course are not providing any real security.

## Reduce duplication

Reducing code duplication is one of the core ideas in **FastAPI**.

As code duplication increments the chances of bugs, security issues, code desynchronization issues (when you update in one place but not in the others), etc.

And these models are all sharing a lot of the data and duplicating attribute names and types.

We could do better.

We can declare a `Userbase` model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation, etc).

All the data conversion, validation, documentation, etc. will still work as normally.

That way, we can declare just the differences between the models (with plaintext `password`, with `hashed_password` and without password):

```Python hl_lines="8 14 15 18 19 22 23"
{!./src/extra_models/tutorial002.py!}
```

## Recap

Use multiple Pydantic models and inherit freely for each case. You don't need to have a single data model per entity if that entity must be able to have different "states". As the case with the user "entity" with a state including `password`, `password_hash` and no password.