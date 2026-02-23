# Return a Response Directly { #return-a-response-directly }

When you create a **FastAPI** *path operation* you can normally return any data from it: a `dict`, a `list`, a Pydantic model, a database model, etc.

If you declare a [Response Model](../tutorial/response-model.md){.internal-link target=_blank} FastAPI will use it to serialize the data to JSON, using Pydantic.

If you don't declare a response model, FastAPI will use the `jsonable_encoder` explained in [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank} and put it in a `JSONResponse`.

You could also create a `JSONResponse` directly and return it.

/// tip

You will normally have much better performance using a [Response Model](../tutorial/response-model.md){.internal-link target=_blank} than returning a `JSONResponse` directly, as that way it serializes the data using Pydantic, in Rust.

///

## Return a `Response` { #return-a-response }

You can return any `Response` or any sub-class of it.

/// info

`JSONResponse` itself is a sub-class of `Response`.

///

And when you return a `Response`, **FastAPI** will pass it directly.

It won't do any data conversion with Pydantic models, it won't convert the contents to any type, etc.

This gives you a lot of flexibility. You can return any data type, override any data declaration or validation, etc.

## Using the `jsonable_encoder` in a `Response` { #using-the-jsonable-encoder-in-a-response }

Because **FastAPI** doesn't make any changes to a `Response` you return, you have to make sure its contents are ready for it.

For example, you cannot put a Pydantic model in a `JSONResponse` without first converting it to a `dict` with all the data types (like `datetime`, `UUID`, etc) converted to JSON-compatible types.

For those cases, you can use the `jsonable_encoder` to convert your data before passing it to a response:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | Technical Details

You could also use `from starlette.responses import JSONResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

///

## Returning a custom `Response` { #returning-a-custom-response }

The example above shows all the parts you need, but it's not very useful yet, as you could have just returned the `item` directly, and **FastAPI** would put it in a `JSONResponse` for you, converting it to a `dict`, etc. All that by default.

Now, let's see how you could use that to return a custom response.

Let's say that you want to return an <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a> response.

You could put your XML content in a string, put that in a `Response`, and return it:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## How a Response Model Works { #how-a-response-model-works }

When you declare a [Response Model](../tutorial/response-model.md){.internal-link target=_blank} in a path operation, **FastAPI** will use it to serialize the data to JSON, using Pydantic.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

As that will happen on the Rust side, the performance will be much better than if it was done with regular Python and the `JSONResponse` class.

When using a response model FastAPI won't use the `jsonable_encoder` to convert the data (which would be slower) nor the `JSONResponse` class.

Instead it takes the JSON bytes generated with Pydantic using the response model and returns a `Response` with the right media type for JSON directly (`application/json`).

## Notes { #notes }

When you return a `Response` directly its data is not validated, converted (serialized), or documented automatically.

But you can still document it as described in [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

You can see in later sections how to use/declare these custom `Response`s while still having automatic data conversion, documentation, etc.
