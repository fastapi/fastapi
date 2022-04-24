# API Key Auth

A common alternative to HTTP Basic Auth is using API Keys.

In API Key Auth, the application expects the secret key, in header, or cookie, query or parameter, depending on setup.

If it doesn't receive it, it returns HTTP 403 "Forbidden" error.

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
    You like want the API Key secret to be sourced from environment variable or config file.

    Have a look at [Pydantic settings](../../settings){.internal-link target=_blank} to do it.

## Protecting single endpoints

Alternatively, the `Security` dependency can be defined at path level to protect
not the whole API, but specific, sensitive endpoints.

```Python
@app.post("/admin/password_reset", dependencies=[Security(get_api_key)]
def password_reset(user: int, new_password: str):
```

## TODO Cookies, Query...

All the variants of the API Key rainbow


Also maybe go more in depth for the fact that `X-API-KEY` is the header's name?
