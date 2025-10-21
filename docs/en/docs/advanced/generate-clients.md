# Generating SDKs { #generating-sdks }

Because **FastAPI** is based on the **OpenAPI** specification, its APIs can be described in a standard format that many tools understand.

This makes it easy to generate up-to-date **documentation**, client libraries (<abbr title="Software Development Kits">**SDKs**</abbr>) in multiple languages, and **testing** or **automation workflows** that stay in sync with your code.

In this guide, you'll learn how to generate a **TypeScript SDK** for your FastAPI backend.

## Open Source SDK Generators { #open-source-sdk-generators }

A versatile option is the <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>, which supports **many programming languages** and can generate SDKs from your OpenAPI specification.

For **TypeScript clients**, <a href="https://heyapi.dev/" class="external-link" target="_blank">Hey API</a> is a purpose-built solution, providing an optimized experience for the TypeScript ecosystem.

You can discover more SDK generators on <a href="https://openapi.tools/#sdk" class="external-link" target="_blank">OpenAPI.Tools</a>.

/// tip

FastAPI automatically generates **OpenAPI 3.1** specifications, so any tool you use must support this version.

///

## SDK Generators from FastAPI Sponsors { #sdk-generators-from-fastapi-sponsors }

This section highlights **venture-backed** and **company-supported** solutions from companies that sponsor FastAPI. These products provide **additional features** and **integrations** on top of high-quality generated SDKs.

By ✨ [**sponsoring FastAPI**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨, these companies help ensure the framework and its **ecosystem** remain healthy and **sustainable**.

Their sponsorship also demonstrates a strong commitment to the FastAPI **community** (you), showing that they care not only about offering a **great service** but also about supporting a **robust and thriving framework**, FastAPI. 🙇

For example, you might want to try:

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainless.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

Some of these solutions may also be open source or offer free tiers, so you can try them without a financial commitment. Other commercial SDK generators are available and can be found online. 🤓

## Create a TypeScript SDK { #create-a-typescript-sdk }

Let's start with a simple FastAPI application:

{* ../../docs_src/generate_clients/tutorial001_py39.py hl[7:9,12:13,16:17,21] *}

Notice that the *path operations* define the models they use for request payload and response payload, using the models `Item` and `ResponseMessage`.

### API Docs { #api-docs }

If you go to `/docs`, you will see that it has the **schemas** for the data to be sent in requests and received in responses:

<img src="/img/tutorial/generate-clients/image01.png">

You can see those schemas because they were declared with the models in the app.

That information is available in the app's **OpenAPI schema**, and then shown in the API docs.

That same information from the models that is included in OpenAPI is what can be used to **generate the client code**.

### Hey API { #hey-api }

Once we have a FastAPI app with the models, we can use Hey API to generate a TypeScript client. The fastest way to do that is via npx.

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

This will generate a TypeScript SDK in `./src/client`.

You can learn how to <a href="https://heyapi.dev/openapi-ts/get-started" class="external-link" target="_blank">install `@hey-api/openapi-ts`</a> and read about the <a href="https://heyapi.dev/openapi-ts/output" class="external-link" target="_blank">generated output</a> on their website.

### Using the SDK { #using-the-sdk }

Now you can import and use the client code. It could look like this, notice that you get autocompletion for the methods:

<img src="/img/tutorial/generate-clients/image02.png">

You will also get autocompletion for the payload to send:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip

Notice the autocompletion for `name` and `price`, that was defined in the FastAPI application, in the `Item` model.

///

You will have inline errors for the data that you send:

<img src="/img/tutorial/generate-clients/image04.png">

The response object will also have autocompletion:

<img src="/img/tutorial/generate-clients/image05.png">

## FastAPI App with Tags { #fastapi-app-with-tags }

In many cases, your FastAPI app will be bigger, and you will probably use tags to separate different groups of *path operations*.

For example, you could have a section for **items** and another section for **users**, and they could be separated by tags:

{* ../../docs_src/generate_clients/tutorial002_py39.py hl[21,26,34] *}

### Generate a TypeScript Client with Tags { #generate-a-typescript-client-with-tags }

If you generate a client for a FastAPI app using tags, it will normally also separate the client code based on the tags.

This way, you will be able to have things ordered and grouped correctly for the client code:

<img src="/img/tutorial/generate-clients/image06.png">

In this case, you have:

* `ItemsService`
* `UsersService`

### Client Method Names { #client-method-names }

Right now, the generated method names like `createItemItemsPost` don't look very clean:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...that's because the client generator uses the OpenAPI internal **operation ID** for each *path operation*.

OpenAPI requires that each operation ID is unique across all the *path operations*, so FastAPI uses the **function name**, the **path**, and the **HTTP method/operation** to generate that operation ID, because that way it can make sure that the operation IDs are unique.

But I'll show you how to improve that next. 🤓

## Custom Operation IDs and Better Method Names { #custom-operation-ids-and-better-method-names }

You can **modify** the way these operation IDs are **generated** to make them simpler and have **simpler method names** in the clients.

In this case, you will have to ensure that each operation ID is **unique** in some other way.

For example, you could make sure that each *path operation* has a tag, and then generate the operation ID based on the **tag** and the *path operation* **name** (the function name).

### Custom Generate Unique ID Function { #custom-generate-unique-id-function }

FastAPI uses a **unique ID** for each *path operation*, which is used for the **operation ID** and also for the names of any needed custom models, for requests or responses.

You can customize that function. It takes an `APIRoute` and outputs a string.

For example, here it is using the first tag (you will probably have only one tag) and the *path operation* name (the function name).

You can then pass that custom function to **FastAPI** as the `generate_unique_id_function` parameter:

{* ../../docs_src/generate_clients/tutorial003_py39.py hl[6:7,10] *}

### Generate a TypeScript Client with Custom Operation IDs { #generate-a-typescript-client-with-custom-operation-ids }

Now, if you generate the client again, you will see that it has the improved method names:

<img src="/img/tutorial/generate-clients/image07.png">

As you see, the method names now have the tag and then the function name, now they don't include information from the URL path and the HTTP operation.

### Preprocess the OpenAPI Specification for the Client Generator { #preprocess-the-openapi-specification-for-the-client-generator }

The generated code still has some **duplicated information**.

We already know that this method is related to the **items** because that word is in the `ItemsService` (taken from the tag), but we still have the tag name prefixed in the method name too. 😕

We will probably still want to keep it for OpenAPI in general, as that will ensure that the operation IDs are **unique**.

But for the generated client, we could **modify** the OpenAPI operation IDs right before generating the clients, just to make those method names nicer and **cleaner**.

We could download the OpenAPI JSON to a file `openapi.json` and then we could **remove that prefixed tag** with a script like this:

{* ../../docs_src/generate_clients/tutorial004.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

With that, the operation IDs would be renamed from things like `items-get_items` to just `get_items`, that way the client generator can generate simpler method names.

### Generate a TypeScript Client with the Preprocessed OpenAPI { #generate-a-typescript-client-with-the-preprocessed-openapi }

Since the end result is now in an `openapi.json` file, you need to update your input location:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

After generating the new client, you would now have **clean method names**, with all the **autocompletion**, **inline errors**, etc:

<img src="/img/tutorial/generate-clients/image08.png">

## Benefits { #benefits }

When using the automatically generated clients, you would get **autocompletion** for:

* Methods.
* Request payloads in the body, query parameters, etc.
* Response payloads.

You would also have **inline errors** for everything.

And whenever you update the backend code, and **regenerate** the frontend, it would have any new *path operations* available as methods, the old ones removed, and any other change would be reflected on the generated code. 🤓

This also means that if something changed, it will be **reflected** on the client code automatically. And if you **build** the client, it will error out if you have any **mismatch** in the data used.

So, you would **detect many errors** very early in the development cycle instead of having to wait for the errors to show up to your final users in production and then trying to debug where the problem is. ✨
