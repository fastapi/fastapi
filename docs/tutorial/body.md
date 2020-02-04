When you need to send data from a client (let's say, a browser) to your API, you send it as a **request body**.

A **request** body is data sent by the client to your API. A **response** body is the data your API sends to the client.

Your API almost always has to send a **response** body. But clients don't necessarily need to send **request** bodies all the time.

To declare a **request** body, you use <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> models with all their power and benefits.

!!! info
    You cannot send a request body using a `GET` operation (HTTP method).

    To send data, you have to use one of: `POST` (the more common), `PUT`, `DELETE` or `PATCH`.

## Import Pydantic's `BaseModel`

First, you need to import `BaseModel` from `pydantic`:

```Python hl_lines="2"
{!./src/body/tutorial001.py!}
```

## Create your data model

Then you declare your data model as a class that inherits from `BaseModel`.

Use standard Python types for all the attributes:

```Python hl_lines="5 6 7 8 9"
{!./src/body/tutorial001.py!}
```

The same as when declaring query parameters, when a model attribute has a default value, it is not required. Otherwise, it is required. Use `None` to make it just optional.

For example, this model above declares a JSON "`object`" (or Python `dict`) like:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...as `description` and `tax` are optional (with a default value of `None`), this JSON "`object`" would also be valid:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Declare it as a parameter

To add it to your *path operation*, declare it the same way you declared path and query parameters:

```Python hl_lines="16"
{!./src/body/tutorial001.py!}
```

...and declare its type as the model you created, `Item`.

## Results

With just that Python type declaration, **FastAPI** will:

* Read the body of the request as JSON.
* Convert the corresponding types (if needed).
* Validate the data.
    * If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
* Give you the received data in the parameter `item`.
    * As you declared it in the function to be of type `Item`, you will also have all the editor support (completion, etc) for all of the attributes and their types.
* Generate <a href="http://json-schema.org" class="external-link" target="_blank">JSON Schema</a> definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
* Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation <abbr title="User Interfaces">UIs</abbr>.

## Automatic docs

The JSON Schemas of your models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs:

<img src="/img/tutorial/body/image01.png">

And will be also used in the API docs inside each *path operation* that needs them:

<img src="/img/tutorial/body/image02.png">

## Editor support

In your editor, inside your function you will get type hints and completion everywhere (this wouldn't happen if you received a `dict` instead of a Pydantic model):

<img src="/img/tutorial/body/image03.png">

You also get error checks for incorrect type operations:

<img src="/img/tutorial/body/image04.png">

This is not by chance, the whole framework was built around that design.

And it was thoroughly tested at the design phase, before any implementation, to ensure it would work with all the editors.

There were even some changes to Pydantic itself to support this.

The previous screenshots were taken with <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

But you would get the same editor support with <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> and most of the other Python editors:

<img src="/img/tutorial/body/image05.png">

## Use the model

Inside of the function, you can access all the attributes of the model object directly:

```Python hl_lines="19"
{!./src/body/tutorial002.py!}
```

## Request body + path parameters

You can declare path parameters and body requests at the same time.

**FastAPI** will recognize that the function parameters that match path parameters should be **taken from the path**, and that function parameters that are declared to be Pydantic models should be **taken from the request body**.

```Python hl_lines="15 16"
{!./src/body/tutorial003.py!}
```

## Request body + path + query parameters

You can also declare **body**, **path** and **query** parameters, all at the same time.

**FastAPI** will recognize each of them and take the data from the correct place.

```Python hl_lines="16"
{!./src/body/tutorial004.py!}
```

The function parameters will be recognized as follows:

* If the parameter is also declared in the **path**, it will be used as a path parameter.
* If the parameter is of a **singular type** (like `int`, `float`, `str`, `bool`, etc) it will be interpreted as a **query** parameter.
* If the parameter is declared to be of the type of a **Pydantic model**, it will be interpreted as a request **body**.

## Without Pydantic

If you don't want to use Pydantic models, you can also use **Body** parameters. See the docs for [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
