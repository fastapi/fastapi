# API Key Authentication

There are many ways to handle security, authentication and authorization.

But let's imagine that you have your **backend** API and you want to have a simple way to authenticate requests using an **API key** in an HTTP header.

This is very common for APIs that provide services to other applications or microservices.

## API Key in Header

FastAPI provides `APIKeyHeader` to handle API key authentication using HTTP headers.

Let's look at how to implement this:

{* ../../docs_src/security/tutorial_api_key_header.py *}

## What it does

When you create an instance of `APIKeyHeader`:

```Python
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
```

* `name`: The name of the HTTP header that will contain the API key
* `auto_error`: If `True` (default), FastAPI will automatically return an error if the header is missing. If `False`, the dependency will return `None` when the header is missing.

## The dependency

When you use `api_key_header` as a dependency:

```Python
def verify_api_key(api_key: str = Security(api_key_header)):
```

FastAPI will:

1. Look for a header with the name you specified (in this case `X-API-Key`)
2. Extract the value from that header
3. Pass it as the `api_key` parameter to your function

## Verification logic

In the `verify_api_key` function:

* We check if the API key is present
* We verify that it matches our expected value
* If invalid, we raise an `HTTPException` with status code 401
* If valid, we return the API key (or could return user information)

## Using the protected endpoint

To access the protected endpoint, clients need to include the API key in the request header:

```bash
curl -H "X-API-Key: your-secret-api-key" http://localhost:8000/protected
```

Without the header:
```bash
curl http://localhost:8000/protected
# Returns: 401 Unauthorized
```

With an invalid API key:
```bash
curl -H "X-API-Key: wrong-key" http://localhost:8000/protected
# Returns: 401 Unauthorized
```

## Interactive documentation

When you go to `/docs`, you will see that your endpoints are marked as requiring authentication, and there's a way to set the API key for testing:

1. Click the "Authorize" button
2. Enter your API key in the `APIKeyHeader` field
3. Click "Authorize"
4. Now you can test the protected endpoints directly from the docs

## Multiple API Key methods

You can also combine different authentication methods. FastAPI provides:

* `APIKeyQuery`: API key in a query parameter
* `APIKeyHeader`: API key in an HTTP header (shown above)
* `APIKeyCookie`: API key in a cookie

You can use them individually or combine them for more flexible authentication.

## Real-world considerations

In a production environment, you should:

1. **Store API keys securely**: Use environment variables or a secure key management system
2. **Use strong API keys**: Generate long, random strings
3. **Implement key rotation**: Allow keys to be updated periodically
4. **Add rate limiting**: Prevent abuse of your API
5. **Log access**: Monitor who is using your API and how
6. **Use HTTPS**: Always encrypt traffic containing API keys

## Next steps

This is a basic example of API key authentication. For more complex scenarios, you might want to:

* Store API keys in a database with associated user information
* Implement different permission levels for different keys
* Add expiration dates to API keys
* Combine API key authentication with other methods like OAuth2
