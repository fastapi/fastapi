The simplest FastAPI file could look like this:

```Python
{!./src/first_steps/tutorial001.py!}
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
{!./src/first_steps/tutorial001.py!}
```

`FastAPI` is a Python class that provides all the functionality for your API.

!!! note "Technical Details"
    `FastAPI` is a class that inherits directly from `Starlette`.

    You can use all the Starlette functionality with `FastAPI` too.

### Step 2: create a `FastAPI` "instance"

```Python hl_lines="3"
{!./src/first_steps/tutorial001.py!}
```

Here the `app` variable will be an "instance" of the class `FastAPI`.

This will be the main point of interaction to create all your API.

This `app` is the same one referred by `uvicorn` in the command:

```bash
uvicorn main:app --debug
```

If you create your app like:

```Python hl_lines="3"
{!./src/first_steps/tutorial002.py!}
```

And put it in a file `main.py`, then you would call `uvicorn` like:

```bash
uvicorn main:my_awesome_api --debug
```

### Step 3: create a path operation

#### Path

"Path" here refers to the last part of the URL starting from the first `/`.

So, in a URL like:

```
https://example.com/items/foo
```

...the path would be:

```
/items/foo
```

!!! info
    A "path" is also commonly called an "endpoint" or a "route".

Building an API, the "path" is the main way to separate "concerns" and functionalities.

#### Operation

"Operation" here refers to one of the HTTP "methods".

One of:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...and the more exotic ones:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".

---

When building APIs, you normally use these specific HTTP methods to perform a specific operation.

Normally you use:

* `POST`: to create data.
* `GET`: to read data.
* `PUT`: to update data.
* `DELETE`: to delete data.

So, in OpenAPI, each of the HTTP methods is called an "operation".

We are going to call them "operations" too.

#### Define a path operation function

```Python hl_lines="6"
{!./src/first_steps/tutorial001.py!}
```

The `@app.get("/")` tells **FastAPI** that the function right below is in charge of handling requests that go to:

* the path `/`
* using a <abbr title="an HTTP GET method"><code>get</code> operation</abbr>

You can also use the other operations:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

And the more exotic ones:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    You are free to use each operation (HTTP method) as you wish.
    
    **FastAPI** doesn't enforce any specific meaning.

    The information here is presented as a guideline, not a requirement.

    For example, when using GraphQL you normally perform all the operations using only `post`.

### Step 4: define the path operation function

```Python hl_lines="7"
{!./src/first_steps/tutorial001.py!}
```

This is a Python function. 

It will be called by FastAPI whenever it receives a request to the URL "`/`".

In this case, it is an `async` function.

---

You could also define it as a normal function instead of `async def`:

```Python hl_lines="7"
{!./src/first_steps/tutorial003.py!}
```

To know the difference, read the section about [Concurrency and `async` / `await`](/async/).

### Step 5: return the content

```Python hl_lines="8"
{!./src/first_steps/tutorial001.py!}
```

You can return a `dict`, `list`, singular values as `str`, `int`, etc.

You can also return Pydantic models (you'll see more about that later).

There are many other objects and models that will be automatically converted to JSON.
