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

## Recap

Use the path operation decorator's parameter `response_model` to define response models and especially to ensure private data is filtered out.
