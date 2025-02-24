# API Key Authentication

Another authentication method, particularly for machine-to-machine communication, is an API key. An API key is a string that the application will expect with each request from a particular client. The API key can be sent as a header, a cookie, or a query parameter.

<!-- TODO: currently we return 403 in the implementation! discuss with @tiangolo et al -->
If the API key is missing or invalid, the application returns an HTTP 401 "Unauthorized" error to the client.

/// warning

It is generally recommended to use API keys for programmatic access only, and to keep the API Key secret between the client(s) authenticated by the key and the server. Depending on your use case, this may mean storing this value in an environment variable or encrypted database (instead of hard-coding it, as in the examples below), and even providing a
unique API key for each client trying to authenticate.

///

/// tip
Please refer to the [API Reference](../../reference/security/index.md#api-key-security-schemes){.internal-link target=_blank} for specifics on the underlying security schemes used.
///

## Simple API Key Auth using Header

* Import `APIKeyHeader`.
* Create an `APIKeyHeader`, specifying what header to parse as the API key.
* Create a `verify_api_key` function that checks the API Key in the Header.
* Add `Depends(verify_api_key)` either globally or to a single endpoint (see example)

```Python hl_lines="5  7  14  23"
{!../../docs_src/security/tutorial008.py!}
```

The client will need to send a request with the correct header:

```http
GET /secure-data HTTP/1.1
X-API-Key: mysecretapikey
```

## API Key Auth using Cookies

The process is similar to using `APIKeyHeader`, except we use a `APIKeyCookie`
instance, instead:

```Python hl_lines="5  7  14  23"
{!../../docs_src/security/tutorial009.py!}
```

The client will then need to pass in the key as a cookie (note that the name of the cookie is case-sensitive!):

```http
GET /secure-data HTTP/1.1
Cookie: X-API-KEY=mysecretapikey
```

## API Key Auth using Query Param

/// warning
Passing API keys via query params is considered less secure, since it will be
visible as part of the URL (for example, in browser history or access logs).
///

Again, similar to the approaches above, except we use `APIKeyQuery`:
```Python hl_lines="5  7  14  23"
{!../../docs_src/security/tutorial010.py!}
```

The client will then need to pass in the key as part of the query param:

```http
GET /secure-data?x-api-key=mysecretapikey HTTP/1.1
```
