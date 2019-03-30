!!! warning
    This is a rather advanced feature. You probably can skip it.

    If you are just following the tutorial - user guide, you can probably skip this section.

    If you already know that you need to modify the generated OpenAPI schema, continue reading.


There are some cases where you might need to modify the generated OpenAPI schema.

In this section you will see how.

## The normal process

The normal (default) process, is as follows.

A `FastAPI` application (instance) has an `.openapi()` method that is expected to return the OpenAPI schema.

As part of the application object creation, a *path operation* for `/openapi.json` (or for whatever you set your `openapi_url`) is registered.

It just returns a JSON response with the result of the application's `.openapi()` method.

By default, what the method `.openapi()` does is check the property `.openapi_schema` to see if it has contents and return them.

If it doesn't, it generates them using the utility function at `fastapi.openapi.utils.get_openapi`.

And that function `get_openapi()` receives as parameters:

* `title`: The OpenAPI title, shown in the docs.
* `version`: The version of your API, e.g. `2.5.0`.
* `openapi_version`: The version of the OpenAPI specification used. By default, the latest: `3.0.2`.
* `description`: The description of your API.
* `routes`: A list of routes, these are each of the registered *path operations*. They are taken from `app.routes`.
* `openapi_prefix`: The URL prefix to be used in your OpenAPI.

## Overriding the defaults

Using the information above, you can use the same utility function to generate the OpenAPI schema and override each part that you need.

For example, let's add <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" target="_blank">ReDoc's OpenAPI extension to include a custom logo</a>.

### Normal **FastAPI**

First, write all your **FastAPI** application as normally:

```Python hl_lines="1 4 7 8 9"
{!./src/extending_openapi/tutorial001.py!}
```

### Generate the OpenAPI schema

Then, use the same utility function to generate the OpenAPI schema, inside a `custom_openapi()` function:

```Python hl_lines="2 15 16 17 18 19 20"
{!./src/extending_openapi/tutorial001.py!}
```

### Modify the OpenAPI schema

Now you can add the ReDoc extension, adding a custom `x-logo` to the `info` "object" in the OpenAPI schema:

```Python hl_lines="21 22 23"
{!./src/extending_openapi/tutorial001.py!}
```

### Cache the OpenAPI schema

You can use the property `.openapi_schema` as a "cache", to store your generated schema.

That way, your application won't have to generate the schema every time a user opens your API docs.

It will be generated only once, and then the same cached schema will be used for the next requests.

```Python hl_lines="13 14 24 25"
{!./src/extending_openapi/tutorial001.py!}
```

### Override the method

Now you can replace the `.openapi()` method with your new function.

```Python hl_lines="28"
{!./src/extending_openapi/tutorial001.py!}
```

### Check it

Once you go to <a href="http://127.0.0.1:8000/redoc" target="_blank">http://127.0.0.1:8000/redoc</a> you will see that you are using your custom logo (in this example, **FastAPI**'s logo):

<img src="/img/tutorial/extending-openapi/image01.png">
