Thanks to <a href="https://www.starlette.io/testclient/" target="_blank">Starlette's TestClient</a>, testing **FastAPI** applications is easy and enjoyable.

It is based on <a href="http://docs.python-requests.org" target="_blank">Requests</a>, so it's very familiar and intuitive.

With it, you can use <a href="https://docs.pytest.org/" target="_blank">pytest</a> directly with **FastAPI**.

## Using `TestClient`

Import `TestClient` from `starlette.testclient`.

Create a `TestClient` passing to it your **FastAPI**.

Create functions with a name that starts with `test_` (this is standard `pytest` conventions).

Use the `TestClient` object the same way as you do with `requests`.

Write simple `assert` statements with the standard Python expressions that you need to check (again, standard `pytest`).

```Python hl_lines="2 12 15 16 17 18"
{!./src/app_testing/tutorial001.py!}
```

!!! tip
    Notice that the testing functions are normal `def`, not `async def`. 
    
    And the calls to the client are also normal calls, not using `await`.

    This allows you to use `pytest` directly without complications.


## Separating tests

In a real application, you probably would have your tests in a different file.

And your **FastAPI** application might also be composed of several files/modules, etc.

### **FastAPI** app file

Let's say you have a file `main.py` with your **FastAPI** app:

```Python
{!./src/app_testing/main.py!}
```

### Testing file

Then you could have a file `test_main.py` with your tests, and import your `app` from the `main` module (`main.py`):

```Python
{!./src/app_testing/test_main.py!}
```

## Testing WebSockets

You can use the same `TestClient` to test WebSockets.

For this, you use the `TestClient` in a `with` statement, connecting to the WebSocket:

```Python hl_lines="27 28 29 30 31"
{!./src/app_testing/tutorial002.py!}
```

## Testing Events, `startup` and `shutdown`

When you need your event handlers (`startup` and `shutdown`) to run in your tests, you can use the `TestClient` with a `with` statement:

```Python hl_lines="9 10 11 12 20 21 22 23 24"
{!./src/app_testing/tutorial003.py!}
```
