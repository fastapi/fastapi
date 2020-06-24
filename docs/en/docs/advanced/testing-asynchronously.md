# Testing Asynchronously

While using the `TestClient` provided by FastAPI you might encounter some difficulties when testing your code: While you can test your (asynchronous) routes with it, you can't test any other asynchronous functions in your (synchronous) pytest functions. 

Being able to use asynchronous functions in your tests could for example be useful when you're querying your database asynchronously. Imagine you want to call your route and then verify that your backend successfully wrote the correct data in the database.

Let's look at how we can make that work.

## Pytest-Asyncio

If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. Pytest provides a neat library for this, called `pytest-asyncio`, that allows us to specify that some test functions are to be called asynchronously.

You can install it via `python3 -m pip install pytest-asyncio`

## HTTPX

By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions. The `TestClient` does some magic inside to abstract from the fact that it calls the asynchronous routes, and that magic doesn't work anymore when we're using it inside asynchronous functions.

Luckily there's a nice alternative, called <a href="https://www.python-httpx.org/" class="external-link" target="_blank">HTTPX</a>. HTTPX is a HTTP client for Python 3 that allows us to query our routes similarly to how we did it with the `TestClient`. If you're familiar with the <a href="https://requests.readthedocs.io/en/master/" class="external-link" target="_blank">Requests</a> library, you'll find that the API of HTTPX is almost identical. The important difference for us is that with HTTPX we are not limited to synchronous, but can also make asynchronous requests.

## Example

For a simple example, let's consider the following `main.py` module:

```Python
{!../../../docs_src/testing_asynchronously/main.py!}
```

The `test_main.py` module that contains the tests for `main.py` could look like this now:

```Python
{!../../../docs_src/testing_asynchronously/test_main.py!}
```

## In Detail

```Python hl_lines="8"
{!../../../docs_src/testing_asynchronously/test_main.py!}
```

This marker tells pytest that this test function should be called asynchronously. Note that the test function is now `async def` instead of just `def`.

```Python hl_lines="10 11"
{!../../../docs_src/testing_asynchronously/test_main.py!}
```

This is the equivalent to:

```Python
response = client.get('/')
```

that we used to make our requests with the `TestClient`. Note that we're using async/await here — the request is asynchronous.
