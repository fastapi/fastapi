<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal-vector.svg" alt='FastAPI'></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://travis-ci.org/tiangolo/fastapi">
    <img src="https://travis-ci.org/tiangolo/fastapi.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi">
    <img src="https://codecov.io/gh/tiangolo/fastapi/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://badge.fury.io/py/fastapi.svg" alt="Package version">
</a>
</p>

---

**Documentation**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

**Source Code**: [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

---

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+.

The key features are:

* **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic).

* **Fast to code**: Increase the speed to develop features by about 200% to 300% *.
* **Less bugs**: Reduce about 40% of human (developer) induced errors. *
* **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Less bugs.
* **Robust**: Get production-ready code. With automatic interactive documentation.
* **Standards-based**: Based on (and fully compatible with) the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" target="_blank">OpenAPI</a> and <a href="http://json-schema.org/" target="_blank">JSON Schema</a>.

<small>* estimation based on tests on an internal development team, building production applications.</small>


## Requirements

Python 3.6+

FastAPI stands on the shoulders of giants:

* <a href="https://www.starlette.io/" target="_blank">Starlette</a> for the web parts.
* <a href="https://pydantic-docs.helpmanual.io/" target="_blank">Pydantic</a> for the data parts.


## Installation

```bash
$ pip install fastapi
```

You will also need an ASGI server, for production such as <a href="http://www.uvicorn.org" target="_blank">uvicorn</a>.

```bash
$ pip install uvicorn
```

## Example

* Create a file `main.py` with:

```Python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {'hello': 'world'}
```

Or if your code uses `async` / `await`, use `async def`:

```Python hl_lines="6"
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def read_root():
    return {'hello': 'world'}
```

!!! note
    If you don't know, check the section about [`async` and `await` in the docs](async.md).


* Run the server with:

```bash
uvicorn main:app --debug
```

!!! note
    The command `uvicorn main:app` refers to:

    * `main`: the file `main.py` (the Python "module").
    * `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
    * `--debug`: make the server restart after code changes. Only do this for development.

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

## Example upgrade

Now modify the file `main.py` to include:

* a path parameter `item_id`.
* a body, declared using standard Python types (thanks to Pydantic).
* an optional query parameter `q`.


```Python hl_lines="2 7 8 9 10 19"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get('/')
async def read_root():
    return {'hello': 'world'}


@app.post('/items/{item_id}')
async def create_item(item_id: int, item: Item, q: str = None):
    return {"item_name": item.name, "item_id": item_id, "query": q}
```

The server should reload automatically (because you added `--debug` to the `uvicorn` command above).

### Interactive API docs upgrade

Now go to <a href="http://127.0.0.1:8000/docs" target="_blank">http://127.0.0.1:8000/docs</a>.

* The interactive API documentation will be automatically updated, including the new query, and body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Click on the button "Try it out", it allows you to fill the parameters and directly interact with the API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Then click on the "Execute" button, the user interface will communicate with your API, send the parameters, get the results and show them on the screen:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)


### Alternative API docs upgrade

And now, go to <a href="http://127.0.0.1:8000/redoc" target="_blank">http://127.0.0.1:8000/redoc</a>.

* The alternative documentation will also reflect the new query parameter and body:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)


### Recap

In summary, you declare **once** the types of parameters, body, etc. as function parameters. 

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard **Python 3.6+**.

For example, for an `int`:

```Python
item_id: int
```

or for a more complex `Item` model:

```Python
item: Item
```

...and with that single declaration you get:

* Editor support, including:
    * Completion.
    * Type checks.
* Validation of data:
    * Automatic and clear errors when the data is invalid.
    * Validation even for deeply nested JSON objects.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> of input data: coming from the network, to Python data and types. Reading from:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> of output data: converting from Python data and types to network data (as JSON):
    * Convert Python types (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` objects.
    * `UUID` objects.
    * Database models.
    * ...and many more.
* Automatic interactive API documentation, including 2 alternative user interfaces:
    * Swagger UI.
    * ReDoc.

---

Coming back to the previous code example, **FastAPI** will:

* Validate that there is an `item_id` in the path.
* Validate that the `item_id` is of type `int`.
    * If it is not, the client will see a useful, clear error.
* Check if there is an optional query parameter named `q` (as in `http://127.0.0.1:8000/items/foo?q=somequery`).
    * As the `q` parameter is declared with `= None`, it is optional.
    * Without the `None` it would be required (as is the body).
* Read the body as JSON:
    * Check that it has a required attribute `name` that should be a `str`. 
    * Check that is has a required attribute `price` that has to be a `float`.
    * Check that it has an optional attribute `is_offer`, that should be a `bool`, if present.
    * All this would also work for deeply nested JSON objects.
* Convert from and to JSON automatically.
* Document everything as an OpenAPI schema, that can be used by:
    * Interactive documentation sytems.
    * Automatic client code generation systems, for many languages.
* Provide 2 interactive documentation web interfaces directly.


---

We just scratched the surface, but you already get the idea of how it all works.

Try changing the line with:

```Python
    return {"item_name": item.name, "item_id": item_id, "query": q}
```

...from:

```Python
        ... "item_name": item.name ...
```

...to:

```Python
        ... "item_price": item.price ...
```

...and see how your editor will auto-complete the attributes and know their types:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)


For a more complete example including more features, [see the tutorial - user guide](tutorial/intro/).

**Spoiler alert**: the tutorial - user guide includes:

* Declaration of **parameters** from other different places as: **headers**, **cookies**, **form fields** and **files**.
* How to set **validation constrains** as `maximum_length` or `regex`.
* A very powerful and easy to use **<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>** system.
* Security and authentication, including support for **OAuth2** with **JWT tokens** and **HTTP Basic** auth.
* More advanced (but equally easy) techniques for declaring **deeply nested JSON models** (thanks to Pydantic).
* Many extra features (thanks to Starlette) as:
    * **WebSockets**
    * **GraphQL**
    * extremely easy tests based on `requests` and `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...and more.



## Optional Dependencies

Used by Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - for faster JSON <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - for email validation.


Used by Starlette:

* <a href="http://docs.python-requests.org" target="_blank"><code>requests</code></a> - Required if you want to use the `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Required if you want to use `FileResponse` or `StaticFiles`.
* <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - Required if you want to use the default template configuration.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Required if you want to support form <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, with `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Required for `SessionMiddleware` support.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Required for `SchemaGenerator` support.
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Required for `GraphQLApp` support.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Required if you want to use `UJSONResponse`.

Used by FastAPI / Starlette:

* <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - for the server that loads and serves your application.

You can install all of these with `pip3 install fastapi[full]`.

## License

This project is licensed under the terms of the MIT license.
