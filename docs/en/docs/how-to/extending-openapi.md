# Extending OpenAPI { #extending-openapi }

There are some cases where you might need to modify the generated OpenAPI schema.

In this section you will see how.

## The normal process { #the-normal-process }

The normal (default) process, is as follows.

A `FastAPI` application (instance) has an `.openapi()` method that is expected to return the OpenAPI schema.

As part of the application object creation, a *path operation* for `/openapi.json` (or for whatever you set your `openapi_url`) is registered.

It just returns a JSON response with the result of the application's `.openapi()` method.

By default, what the method `.openapi()` does is check the property `.openapi_schema` to see if it has contents and return them.

If it doesn't, it generates them using the utility function at `fastapi.openapi.utils.get_openapi`.

And that function `get_openapi()` receives as parameters:

* `title`: The OpenAPI title, shown in the docs.
* `version`: The version of your API, e.g. `2.5.0`.
* `openapi_version`: The version of the OpenAPI specification used. By default, the latest: `3.1.0`.
* `summary`: A short summary of the API.
* `description`: The description of your API, this can include markdown and will be shown in the docs.
* `routes`: A list of routes, these are each of the registered *path operations*. They are taken from `app.routes`.

/// info

The parameter `summary` is available in OpenAPI 3.1.0 and above, supported by FastAPI 0.99.0 and above.

///

## Overriding the defaults { #overriding-the-defaults }

Using the information above, you can use the same utility function to generate the OpenAPI schema and override each part that you need.

For example, let's add <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">ReDoc's OpenAPI extension to include a custom logo</a>.

### Normal **FastAPI** { #normal-fastapi }

First, write all your **FastAPI** application as normally:

{* ../../docs_src/extending_openapi/tutorial001.py hl[1,4,7:9] *}

### Generate the OpenAPI schema { #generate-the-openapi-schema }

Then, use the same utility function to generate the OpenAPI schema, inside a `custom_openapi()` function:

{* ../../docs_src/extending_openapi/tutorial001.py hl[2,15:21] *}

### Modify the OpenAPI schema { #modify-the-openapi-schema }

Now you can add the ReDoc extension, adding a custom `x-logo` to the `info` "object" in the OpenAPI schema:

{* ../../docs_src/extending_openapi/tutorial001.py hl[22:24] *}

### Cache the OpenAPI schema { #cache-the-openapi-schema }

You can use the property `.openapi_schema` as a "cache", to store your generated schema.

That way, your application won't have to generate the schema every time a user opens your API docs.

It will be generated only once, and then the same cached schema will be used for the next requests.

{* ../../docs_src/extending_openapi/tutorial001.py hl[13:14,25:26] *}

### Override the method { #override-the-method }

Now you can replace the `.openapi()` method with your new function.

{* ../../docs_src/extending_openapi/tutorial001.py hl[29] *}

### Check it { #check-it }

Once you go to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> you will see that you are using your custom logo (in this example, **FastAPI**'s logo):

<img src="/img/tutorial/extending-openapi/image01.png">
