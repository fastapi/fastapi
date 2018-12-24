Now let's build from the previous chapter and add the missing parts to have a complete security flow.

## Get the `username` and `password`

We are going to use **FastAPI** security utilities to get the `username` and `password`.

OAuth2 specifies that when using the "password flow" (that we are using) the client / user must send a `username` and `password` fields as form data.

And the spec says that the fields have to be named like that. So `user-name` or `email` wouldn't work.

But don't worry, you can show it as you wish to your final users in the frontend.

And your database models can use any other names you want.

But for the login path operation, we need to use these names to be compatible with the spec (and be able to, for example, use the integrated API documentation system).

The spec also states that the `username` and `password` must be sent as form data (so, no JSON here).

### `scopes`

The spec also says that the client can send another field of "`scopes`".

As a long string with all these "scopes" separated by spaces.

Each "scope" is just a string.

They are normally used to declare specific security permissions, for exampe:

* `"users:read"` or `"users:write"` are common examples.
* `instagram_basic` is used by Facebook / Instagram.
* `https://www.googleapis.com/auth/drive` is used by Google.

!!! info
    In OAuth2 a "scope" is just a string that declares a specific permision required.

    It doesn't matter if it has other characters like `:`, or if it is a URL.
    
    Those details are implementation specific.

    For OAuth2 they are just strings.

    And when using `scopes` it normally referes to a long string of "scopes" separated by spaces.


## Code to get the `username` and `password`

Now let's use the utilities provided by **FastAPI** to handle this.

### `OAuth2PasswordRequestForm`

First, import `OAuth2PasswordRequestForm`, and use it as the body declaration of the path `/token`:

```Python hl_lines="2 63"
{!./src/security/tutorial003.py!}
```

`OAuth2PasswordRequestForm` declares a form body with:

* The `username`.
* The `password`.
* An optional `scopes` field as a big string, composed of strings separated by spaces.
* An optional `grant_type`.

!!! tip
    The OAuth2 spec actually *requires* a field `grant_type` with a fixed value of `password`, but `OAuth2PasswordRequestForm` doesn't enforce it.

    If you need to enforce it, use `OAuth2PasswordRequestFormStrict` instead of `OAuth2PasswordRequestForm`.

* An optional `client_id` (we don't need it for our example).
* An optional `client_secret` (we don't need it for our example).

### Parse and use the form data

`OAuth2PasswordRequestForm` provides a `.parse()` method that converts the `scopes` string into an actual list of strings.

We are not using `scopes` in this example, but the functionality is there if you need it.

!!! tip
    The `.parse()` method returns a Pydantic model `OAuth2PasswordRequestData`.

    But you don't need to import it, your editor will know its type and provide you with completion and type checks automatically.

Now, get the user data from the (fake) database, using this `username`.

If there is no such user, we return an error saying "incorrect username or password".

For the error, we use the exception `HTTPException` provided by Starlette directly:

```Python hl_lines="4 64 65 66 67"
{!./src/security/tutorial003.py!}
```

### Check the password

At this point we have a the user data from our database, but we haven't checked the password.

Let's put that data in the Pydantic `UserInDB` model first.

You should never save plaintext passwords, so, we'll use the (fake) password hashing system.

If the password doesn't match, we return the same error.

```Python hl_lines="68 69 70 71"
{!./src/security/tutorial003.py!}
```

#### About `**user_dict`

`UserInDB(**user_dict)` means:
    
Pass the keys and values of the `user_dict` directly as key-value arguments, equivalent to:

```Python
UserInDB(
    username=user_dict["username"],
    email=user_dict["email"],
    full_name=user_dict["full_name"],
    disabled=user_dict["disabled"],
    hashed_password=user_dict["hashed_password"],
)
```

## Return the token

The response of the `token` endpoint must be a JSON object.

It should have a `token_type`. In our case, as we are using "Bearer" tokens, the token type should be `bearer`.

And it should have an `access_token`, with a string containing our access token.

For this simple example, we are going to just be completely insecure and return the same `username` as the token.

!!! tip
    In the next chapter, you will see a real secure implementation, with password hasing and JWT tokens.

    But for now, let's focus on the specific details we need.

```Python hl_lines="73"
{!./src/security/tutorial003.py!}
```

## Update the dependencies

Now we are going to update our dependencies.

We want to get the `current_user` *only* if this user is active.

So, we create an additional dependency `get_current_active_user` that in turn uses `get_current_user` as a dependency.

Both of these dependencies will just return an HTTP error if the user doesn't exists, or if is inactive.

So, in our endpoint, we will only get a user if the user exists, was correctly authenticated, and is active:

```Python hl_lines="49 50 51 52 53 56 57 58 59 77"
{!./src/security/tutorial003.py!}
```

## See it in action

Open the interactive docs: <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

### Authenticate

Click the "Authorize" button.

Use the credentials:

User: `johndoe`
Password: `secret`

<img src="/img/tutorial/security/image04.png">

After authenticating in the system, you will see it like:

<img src="/img/tutorial/security/image05.png">

### Get your own user data

Now use the operation `GET` with the path `/users/me`.

You will get your user's data, like:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

If you click the lock icon and logout, and then try the same operation again, you will get an HTTP 403 error of:

```JSON
{
  "detail": "Not authenticated"
}
```

## Recap

You now have the tools to implement a complete security system based on `username` and `password` for your API.

Using these tools, you can make the security system compatible with any database and with any user or data model.

The only detail missing is that it is not actually "secure" yet.

In the next chapter you'll see how to use a secure password hashing library and JWT tokens.
