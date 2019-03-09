Let's imagine that you have your **backend** API in some domain.

And you have a **frontend** in another domain or in a different path of the same domain (or in a mobile application).

And you want to have a way for the frontend to authenticate with the backend, using a **username** and **password**.

We can use **OAuth2** to build that with **FastAPI**.

But let's save you the time of reading the full long specification just to find those little pieces of information you need.

Let's use the tools provided by **FastAPI** to handle security.

## How it looks

But let's first just use the code and see how it works, and then we'll come back to understand what's happening.

## Create `main.py`

Copy the example in a file `main.py`:

```Python
{!./src/security/tutorial001.py!}
```

## Run it

Run the example with:

```bash
uvicorn main:app --reload
```

## Check it

Go to the interactive docs at: <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see something like this:

<img src="/img/tutorial/security/image01.png">

!!! check "Authorize button!"
    You already have a shinny new "Authorize" button.

    And your path operation has a little lock in the top-right corner that you can click.


And if you click it, you have a little authorization form to type a `username` and `password` (and other optional fields):

<img src="/img/tutorial/security/image02.png">

!!! note
    It doesn't matter what you type in the form, it won't work yet. But we'll get there.

This is of course not the frontend for the final users, but it's a great automatic tool to document interactively all your API.

It can be used by the frontend team (that can also be yourself).

It can be used by third party applications and systems.

And it can also be used by yourself, to debug, check and test the same application.


## The `password` flow

Now let's go back a bit and understand what is all that.

The `password` "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.

OAuth2 was designed so that the backend or API could be independent of the server that authenticates the user.

But in this case, the same **FastAPI** application will handle the API and the authentication.

So, let's review it from that simplified point of view:

* The user types his `username` and `password` in the frontend, and hits `Enter`.
* The frontend (running in the user's browser) sends that `username` and `password` to a specific URL in our API.
* The API checks that `username` and `password`, and responds with a "token".
    * A "token" is just a string with some content that we can use later to verify this user.
    * Normally, a token is set to expire after some time.
    * So, the user will have to login again at some point later.
    * And if the token is stolen, the risk is less. It is not like a permanent key that will work forever.
* The frontend stores that token temporarily somewhere.
* The user clicks in the frontend to go to another section of the frontend web app.
* The frontend needs to fetch some more data from the API.
    * But it needs authentication for that specific endpoint.
    * So, to authenticate with our API, it sends a header `Authorization` with a value of `Bearer ` plus the token.
    * If the token contains `foobar`, the content of the `Authorization` header would be: `Bearer foobar`.
    * Note that although the header is case-insensitive (`Authorization` is the same as `authorization`), the value is not. So, `bearer foobar` would not be valid. It has to be `Bearer foobar`.

## **FastAPI**'s `Security`

### Import it

The same way **FastAPI** provides a `Depends`, there is a `Security` that you can import:

```Python hl_lines="1"
{!./src/security/tutorial001.py!}
```

### Use it

It is actually a subclass of `Depends`, and it has just one extra parameter that we'll see later.

But by using `Security` instead of `Depends`, **FastAPI** will know that it can use this dependency to define "security schemes" in OpenAPI.

```Python hl_lines="10"
{!./src/security/tutorial001.py!}
```

In this case, we have a `Security` definition (which at the same time is a dependency definition) that will provide a `str` that is assigned to the parameter `token`.

## **FastAPI**'s `OAuth2PasswordBearer`

**FastAPI** provides several tools, at different levels of abstraction, to implement these security features.

In this example we are going to use **OAuth2**, with the **Password** flow, using a **Bearer** token.


!!! info
    A "bearer" token is not the only option.
    
    But it's the best one for our use case.

    And it might be the best for most use cases, unless you are an OAuth2 expert and know exactly why there's another option that suits better your needs.

    In that case, **FastAPI** also provides you with the tools to build it.

`OAuth2PasswordBearer` is a class that we create passing a parameter of the URL in where the client (the frontend running in the user's browser) can use to send the `username` and `password` and get a token.

```Python hl_lines="6"
{!./src/security/tutorial001.py!}
```

It doesn't create that endpoint / path operation, but declares that that URL is the one that the client should use to get the token. That information is used in OpenAPI, and then in the interactive API documentation systems.

!!! info
    If you are a very strict "Pythonista" you might dislike the style of the parameter name `tokenUrl` instead of `token_url`.

    That's because it is using the same name as in the OpenAPI spec. So that if you need to investigate more about any of these security schemes you can just copy and paste it to find more information about it.

The `oauth2_scheme` variable is an instance of `OAuth2PasswordBearer`, but it is also a "callable".

It could be called as:

```Python
oauth2_scheme(some, parameters)
```

So, it can be used with `Security` (as it could be used with `Depends`).

## What it does

It will go and look in the request for that `Authorization` header, check if the value is `Bearer ` plus some token, and will return the token as a `str`.

If it doesn't see an `Authorization` header, or the value doesn't have a `Bearer ` token, it will respond with a 403 status code error (`FORBIDDEN`) directly.

You don't even have to check if the token exists to return an error. You can be sure that if your function is executed, it will have a `str` in that token.

You can try it already in the interactive docs:

<img src="/img/tutorial/security/image03.png">

We are not verifying the validity of the token yet, but that's a start already.

## Recap

So, in just 3 or 4 extra lines, you already have some primitive form of security.
