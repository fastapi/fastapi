# Async Tests with Lifespan Trigger

You’ve already seen how to test your **FastAPI** applications using `TestClient`. So far, you’ve primarily written synchronous tests using def functions.

However, asynchronous test functions can be useful, especially when querying your database asynchronously. For instance, you may want to test that sending requests to your **FastAPI** app successfully writes correct data to the database using an async library. Let’s explore how to achieve this.

## pytest.mark.anyio

If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. AnyIO provides a neat plugin for this, that allows us to specify that some test functions are to be called asynchronously.

/// note

You can also use <a href="https://pytest-asyncio.readthedocs.io/en/latest/" class="external-link" target="_blank">PyTest asyncio</a>.

///


## HTTPX

Even if your **FastAPI** application uses normal `def` functions instead of `async def`, it is still an `async` application underneath.

The `TestClient` does some magic inside to call the asynchronous FastAPI application in your normal `def` test functions, using standard pytest. But that magic doesn't work anymore when we're using it inside asynchronous functions. By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions.

The `TestClient` is based on <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, and luckily, we can use it directly to test the API.

## Example

For a simple example, let's consider a file structure similar to the one described in [Bigger Applications](../tutorial/bigger-applications.md){.internal-link target=_blank} and [Testing](../tutorial/testing.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

The file `main.py` would have:

{* ../../docs_src/async_tests/main.py *}

The file `test_main.py` would have the tests for `main.py`, it could look like this now:

{* ../../docs_src/async_tests/test_main.py *}

## Run it

You can run your tests as usual via:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## In Detail

The lifespan function demonstrates how to manage the lifecycle of application-wide resources. During the app's lifespan, we open a resource (`some_state_open`) at startup and clean it up (`some_state_close`) during shutdown.  

We use **ASGITransport** from **HTTPX** to interact directly with the **FastAPI** app in an async test environment.

When testing **FastAPI** apps with a custom lifespan, it's critical to manually trigger it in the test context to ensure proper setup and teardown of resources.  

If you observe issues with state initialization or teardown in your tests, ensure that the lifespan is correctly invoked, and verify the app's state before and after requests.  


## Other Asynchronous Function Calls

As the testing function is now asynchronous, you can now also call (and await) other async functions apart from sending requests to your FastAPI application in your tests, exactly as you would call them anywhere else in your code.

/// tip

If you encounter a `RuntimeError: Task attached to a different loop` when integrating asynchronous function calls in your tests, you can override the default pytest event loop using the following fixture:

```python
@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
```

///

