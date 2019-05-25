You can declare the model used for the response with the parameter `response_model` in any of the path operations:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

```Python hl_lines="17"
{!./src/response_model/tutorial001.py!}
```

!!! note
    Notice that `response_model` is a parameter of the "decorator" method (`get`, `post`, etc). Not of your path operation function, like all the parameters and body.

It receives a standard Pydantic model and will:

* Convert the output data to the type declarations of the model
* Validate the data
* Add a JSON Schema for the response, in the OpenAPI path operation
* Will be used by the automatic documentation systems

But most importantly:

* Will limit the output data to that of the model. We'll see how that's important below.

!!! note "Technical Details"
    The response model is declared in this parameter instead of as a function return type annotation, because the path function may not actually return that response model but rather return a `dict`, database object or some other model, and then use the `response_model` to perform the field limiting and serialization.

## Return the same input data

Here we are declaring a `UserIn` model, it will contain a plaintext password:

```Python hl_lines="8 10"
{!./src/response_model/tutorial002.py!}
```

And we are using this model to declare our input and the same model to declare our output:

```Python hl_lines="16 17"
{!./src/response_model/tutorial002.py!}
```

Now, whenever a browser is creating a user with a password, the API will return the same password in the response.

In this case, it might not be a problem, because the user himself is sending the password.

But if we use the same model for another path operation, we could be sending the passwords of our users to every client.

!!! danger
    Never send the plain password of a user in a response.

## Add an output model

We can instead create an input model with the plaintext password and an output model without it:

```Python hl_lines="8 10 15"
{!./src/response_model/tutorial003.py!}
```

Here, even though our path operation function is returning the same input user that contains the password:

```Python hl_lines="23"
{!./src/response_model/tutorial003.py!}
```

...we declared the `response_model` to be our model `UserOut`, that doesn't include the password:

```Python hl_lines="21"
{!./src/response_model/tutorial003.py!}
```

So, **FastAPI** will take care of filtering out all the data that is not declared in the output model (using Pydantic).

## See it in the docs

When you see the automatic docs, you can check that the input model and output model will both have their own JSON Schema:

<img src="/img/tutorial/response-model/image01.png">

And both models will be used for the interactive API documentation:

<img src="/img/tutorial/response-model/image02.png">

## Response Model encoding parameters

If your response model has default values, like:

```Python hl_lines="11 13 14"
{!./src/response_model/tutorial004.py!}
```

* `description: str = None` has a default of `None`.
* `tax: float = None` has a default of `None`.
* `tags: List[str] = []` has a default of an empty list: `[]`.

You can set the *path operation decorator* parameter `response_model_skip_defaults=True`:

```Python hl_lines="24"
{!./src/response_model/tutorial004.py!}
```

and those default values won't be included in the response.

So, if you send a request to that *path operation* for the item with ID `foo`, the response (not including default values) will be:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

!!! info
    FastAPI uses Pydantic model's `.dict()` with <a href="https://pydantic-docs.helpmanual.io/#copying" target="_blank">its `skip_defaults` parameter</a> to achieve this.

### Data with values for fields with defaults

But if your data has values for the model's fields with default values, like the item with ID `bar`:

```Python hl_lines="3 5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

they will be included in the response.

### Data with the same values as the defaults

If the data has the same values as the default ones, like the item with ID `baz`:

```Python hl_lines="3 5 6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI is smart enough (actually, Pydantic is smart enough) to realize that, even though `description`, `tax`, and `tags` have the same values as the defaults, they were set explicitly (instead of taken from the defaults).

So, they will be included in the JSON response.

!!! tip
    Notice that the default values can be anything, not only `None`.

    They can be a list (`[]`), a `float` of `10.5`, etc.

### Use cases

This is very useful in several scenarios.

For example if you have models with many optional attributes in a NoSQL database, but you don't want to send very long JSON responses full of default values.

### Using Pydantic's `skip_defaults` directly

You can also use your model's `.dict(skip_defaults=True)` in your code.

For example, you could receive a model object as a body payload, and update your stored data using only the attributes set, not the default ones:

```Python hl_lines="31 32 33 34 35"
{!./src/response_model/tutorial004.py!}
```

!!! tip
    It's common to use the HTTP `PUT` operation to update data.

    In theory, `PUT` should be used to "replace" the entire contents.

    The less known HTTP `PATCH` operation is also used to update data.

    But `PATCH` is expected to be used when *partially* updating data. Instead of *replacing* the entire content.

    Still, this is just a small detail, and many teams and code bases use `PUT` instead of `PATCH` for all updates, including to *partially* update contents.

    You can use `PUT` or `PATCH` however you wish.

## Recap

Use the path operation decorator's parameter `response_model` to define response models and especially to ensure private data is filtered out.

Use `response_model_skip_defaults` to return only the values explicitly set.
