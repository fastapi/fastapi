# API Key Auth

A common alternative to HTTP Basic Auth is using API Keys.

In API Key Auth, the application expects the secret key, in header, or cookie, query or parameter, depending on setup.

If it doesn't receive it, it returns HTTP 403 "Forbidden" error.

## Simple API Key Auth using header

We'll protect the entire API (rather than single endpoints)

* Import `APIKeyHeader`.
* Create an `APIKeyHeader`, specifying what header to parse as API key.
* Create a "`security` scheme" using the `APIKeyHeader`.
* Use that `security` as a dependency in your FastAPI `app`.

```Python hl_lines="2  6  10"
{!../../../docs_src/security/tutorial008.py!}
```


## TODO

- Finish "simple API Key Auth using header" section
- Add variant for per-path auth
- Add variant for API Key Cookie, param, query...
- TIP: You will likely want to set the secret API Key via an environment variable or config file, have a look at using pydantic Settings to do so.

