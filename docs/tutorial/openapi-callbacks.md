You could create an API with a *path operation* that could trigger a request to an external API created by someone else, probably the same developer that would be *using* your API.

When your API app calls the external API, that is called a "callback". Because the software, that the external developer wrote, calls your API. And then your API *calls back* an external API, probably created by the same developer.

In this case, you could want to document how that external API *should* look like. What *path operation* should it have, what body it should expect, what responses to it should return, etc.

## An app with callbacks

Imagine you develop an app that allows creating invoices.

These invoices will have an `id`, optional `title`, `customer`, and `total`.

The user of your API (an external developer) will create an invoice in your API with a POST request.

Then your API will (let's imagine) send the invoice to the client, collect the money, and then finally, send a notification back to the API user (the external developer), by sending a POST request (from your API) to some external API provided by that external developer (this is the "callback").

## The normal **FastAPI** app

Let's first see how the normal API app would look like.

It will receive an `Invoice` body, and a query parameter of `callback_url` that will contain the URL to "call back".

This part is pretty normal, most of the parts are probably familiar to you already:

```Python hl_lines="8 9 10 11 12  35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54"
{!./src/openapi_callbacks/tutorial001.py!}
```

!!! tip
    The `callback_url` query parameter uses a Pydantic <a href="https://pydantic-docs.helpmanual.io/usage/types/#urls" target="_blank">URL</a> type.

The only new thing is the `callbacks=messages_callback_router.routes` as an argument to the *path operation decorator*. We'll see what that is next.

## Documenting the callback

The actual callback code will depend heavily on your own API app.

And it will probably vary a lot from one app to the next.

It could be just one or two lines of code, like:

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
requests.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

But possibly the most important thing is to make sure that your API user (the external developer) implements the *external API* correctly, according to the data that your API is going to send in the callback, etc.

So, what we will do next is add the code to document how that *external API* should be to receive the callback from your API.

That documentation will show up in the Swagger UI at `/docs` in your API, and it will let external developers know how to build it.

This example doesn't implement the callback itself (that could be just a line of code), only the documentation part.

!!! tip
    The actual callback is just an HTTP request.

    When implementing the callback yourself, you could use something like <a href="https://www.encode.io/httpx/" target="_blank">HTTPX</a> or <a href="https://requests.readthedocs.io/" target="_blank">Requests</a>.

## Write the callback documentation code

This code won't be executed in your app, we only need it to *document* how that *external API* should look like.

But you already know how to easily create automatic documentation for an API with **FastAPI**.

So we are going to use that same knowledge to document how the *external API* should look like... by creating the *path operation(s)* that the external API should implement (the ones your API will call).

### Create a callback `APIRouter`

To do this, create a new `APIRouter` that will contain one or more callbacks.

This router will never be added to an actual `FastAPI` app (i.e. it will never be passed to `app.include_router(...)`).

Because of that, you need to declare what will be the `default_response_class`, and set it to `JSONResponse`.

```Python hl_lines="3 24"
{!./src/openapi_callbacks/tutorial001.py!}
```

### Create the callback *path operation*

To create the callback *path operation* use the same `APIRouter` you created above.

It should look just like a normal FastAPI *path operation*:

* It probably should have a declaration of the body it should receive, e.g. `body: InvoiceEvent`.
* And it could also have a declaration of the response it should return, e.g. `response_model=InvoiceEventReceived`.

There are 2 main differences from a normal *path operation*:

* It doesn't need to have any actual code, because your app will never call this code. It's only used to document the *external API*. So, the function could just have `pass`.
* The *path* can contain an <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#key-expression" target="_blank">OpenAPI 3 expression</a> (see more below) where it can use variables with parameters and parts of the original request sent to *your API*.

```Python hl_lines="15 16 17  20 21  27 28 29 30 31 32"
{!./src/openapi_callbacks/tutorial001.py!}
```

### The callback path expression

The callback *path* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#key-expression" target="_blank">OpenAPI 3 expression</a> can contain parts of the original request sent to *your API*.

So, if your API user (the external developer) sends a request to *your API* to:

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

with a JSON body of:

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

Then *your API* will process the invoice, and at some point later, send a callback request to the `callback_url` (the *external API*):

```
https://www.external.org/events/invoices/2expen51ve
```

with a JSON body containing something like:

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

and it would expect a response from that *external API* like:

```JSON
{
    "ok": true
}
```

!!! tip
    Notice how the callback URL used contains the URL received as a query parameter in `callback_url` (`https://www.external.org/events`) and also the invoice `id` from inside of the JSON body (`2expen51ve`).

### Add the callback router

After having the *path operation(s)* needed to the callback router, add the *routes* from that callback router (that's actually just a `list` of routes/*path operations*) to the `callbacks` parameter of your *path operation decorator*:

```Python hl_lines="35"
{!./src/openapi_callbacks/tutorial001.py!}
```

!!! tip
    Notice that you are not passing the router itself to `callback=`, but the attribute `.routes`, as in `invoices_callback_router.routes`.
