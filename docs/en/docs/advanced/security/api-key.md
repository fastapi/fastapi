# API Key Auth

A common alternative to HTTP Basic Auth is using API Keys.

In API Key Auth, the application expects the secret key, in header, or cookie, query or parameter, depending on setup.

If header isn't received it, FastAPI can return an HTTP 403 "Forbidden" error.

## Simple API Key Auth using header

We'll protect the entire API under a Key (rather than single endpoints).

* Import `APIKeyHeader`.
* Create an `APIKeyHeader`, specifying what header to parse as API key.
* Create a `get_api_key` function to check the key
* Create a `security` from the `get_api_key` function, used as a dependency in your FastAPI `app`.

```Python hl_lines="5  7  14  23"
{!../../../docs_src/security/tutorial008.py!}
```

This API now requires authentication to hit any endpoint:


<img src="/img/tutorial/security/image13.png">

!!! tip
    In the simplest case of a single, static API Key secret, you likely want it to be sourced from an environment variable or config file.

    Have a look at [Pydantic settings](../../settings){.internal-link target=_blank} to do it.

## A look at the Header

Note how the `APIKeyHeader` describes the expected header name, and the
description ends up on the documentation for the authentication: the description
is a perfect place to link to your developer documentation's "Generate a token"
section.

```Python hl_lines="8  9"
{!../../../docs_src/security/tutorial008.py!}
```

As for the `auto_error` parameter, it can be set to `True` so that missing the
header returns automatic HTTP 403 "Forbidden".

## Protecting single endpoints

Alternatively, the `Security` dependency can be defined at path level to protect
not the whole API, but specific, sensitive endpoints.

```Python
@app.post("/admin/password_reset", dependencies=[Security(get_api_key)]
def password_reset(user: int, new_password: str):
```

## API Key in Cookies

For convenience, API Keys can be pushed in cookies instead.

<!-- Note: tutorial009.py is 100 %CLONED from tests/test_security_api_key_cookie.py -->

```Python hl_lines="2 7 14"
{!../../../docs_src/security/tutorial009.py!}
```

Users can call this via:

```Python
response = client.get("/users/me", cookies={"key": "secret"})
```

## API Key in Query

To round up the multiple ways to use API Keys, one can set the API key as query parameter.

<!-- Note: tutorial010.py is 100 %CLONED from tests/test_security_api_key_query.py -->
```Python hl_lines="2 7 14"
{!../../../docs_src/security/tutorial010.py!}
```

Users can call this via:

```Python
response = client.get("/users/me?key=secret")
```

Note that setting `auto_error` to `False` can useful to support multiple
methods for providing API Key, checking successively for Cookie, falling back to
header, etc.
