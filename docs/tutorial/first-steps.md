The simplest FastAPI file could look like this:

```Python
{!tutorial/src/first-steps/tutorial001.py!}
```

Copy that to a file `main.py`.

Run the live server:

```bash
uvicorn main:app --debug
```

!!! note
    The command `uvicorn main:app` refers to:

    * `main`: the file `main.py` (the Python "module").
    * `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
    * `--debug`: make the server restart after code changes. Only use for development.

You will see an output like:

```hl_lines="4"
INFO: Started reloader process [17961]
INFO: Started server process [17962]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

That last line shows the URL where your app is being served, in your local machine.

### Check it

Open your browser at <a href="http://127.0.0.1:8000" target="_blank">http://127.0.0.1:8000</a>. 

You will see the JSON response as:

```JSON
{"hello": "world"}
```

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>. 

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)


### Alternative API docs

And now, go to <a href="http://127.0.0.1:8000/redoc" target="_blank">http://127.0.0.1:8000/redoc</a>.

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

If you are curious about how the raw OpenAPI schema looks like, it is just an automatically generated JSON with the descriptions of all your API.

You can see it directly at: <a href="http://127.0.0.1:8000/openapi.json" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

It will show a JSON starting with something like:

```JSON
{
    "openapi": "3.0.2",
    "info": {
        "title": "Fast API",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

## Recap, step by step

### Step 1: import `FastAPI`

```Python hl_lines="1"
{!tutorial/src/first-steps/tutorial001.py!}
```

`FastAPI` is a Python class that provides all the functionality for your API.

### Step 2: create a `FastAPI` "instance"

```Python hl_lines="3"
{!tutorial/src/first-steps/tutorial001.py!}
```

Here the `app` variable will be an "instance" of the class `FastAPI`.

This will be the main point of interaction to create all your API endpoints.

This `app` is the same one referred by `uvicorn` in thet command:

```bash
uvicorn main:app --debug
```

If you create your app like:

```Python hl_lines="3"
{!tutorial/src/first-steps/tutorial002.py!}
```

And put it in a file `main.py`, then you would call `uvicorn` like:

```bash
uvicorn main:my_awesome_api --debug
```

### Step 3: create an endpoint

```Python hl_lines="6"
{!tutorial/src/first-steps/tutorial001.py!}
```

The `@app.get("/")` tells **FastAPI** that the function right below is an endpoint and that it should go to the path route `/`.

You can also use other HTTP methods:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

And more exotic ones:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

### Step 4: define the endpoint function

```Python hl_lines="7"
{!tutorial/src/first-steps/tutorial001.py!}
```

This is a Python function. 

It will be called by FastAPI whenever it receives a request to the URL "`/`".

In this case, it is an `async` function.

---

You could also define it as a normal function instead of `async def`:

```Python hl_lines="7"
{!tutorial/src/first-steps/tutorial003.py!}
```

To know the difference, read the section about [Concurrency and `async` / `await`](/async/).

### Step 5: return the content

```Python hl_lines="8"
{!tutorial/src/first-steps/tutorial001.py!}
```

You can return a `dict`, `list`, singular values as `str`, `int`, etc.

You can also return Pydantic models (you'll see more about that later).

There are many other objects and models that will be automatically converted to JSON.
