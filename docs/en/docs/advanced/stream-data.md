# Stream Data { #stream-data }

If you want to stream data that can be structured as JSON, you should [Stream JSON Lines](../tutorial/stream-json-lines.md){.internal-link target=_blank}.

But if you want to **stream pure binary data** or strings, here's how you can do it.

## Use Cases { #use-cases }

You could use this if you want to stream pure strings, for example directly from the output of an **AI LLM** service.

You could also use it to stream **large binary files**, where you stream each chunk of data as you read it, without having to read it all in memory at once.

You could also stream **video** or **audio** this way, it could even be generated as you process and send it.

## A `StreamingResponse` with `yield` { #a-streamingresponse-with-yield }

If you declare a `response_class=StreamingResponse` in your *path operation function*, you can use `yield` to send each chunk of data in turn.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI will give each chunk of data to the `StreamingResponse` as is, it won't try to convert it to JSON or anything similar.

### Non-async *path operation functions* { #non-async-path-operation-functions }

You can also use regular `def` functions (without `async`), and use `yield` the same way.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### No Annotation { #no-annotation }

You don't really need to declare the return type annotation for streaming binary data.

As FastAPI will not try to convert the data to JSON with Pydantic or serialize it in any way, in this case, the type annotation is only for your editor and tools to use, it won't be used by FastAPI.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

This also means that with `StreamingResponse` you have the **freedom** and **responsibility** to produce and encode the data bytes exactly as you need them to be sent, independent of the type annotations. 🤓

### Stream Bytes { #stream-bytes }

One of the main use cases would be to stream `bytes` instead of strings, you can of course do it.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## A Custom `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

In the examples above, the data bytes were streamed, but the response didn't have a `Content-Type` header, so the client didn't know what type of data it was receiving.

You can create a custom sub-class of `StreamingResponse` that sets the `Content-Type` header to the type of data you're streaming.

For example, you can create a `PNGStreamingResponse` that sets the `Content-Type` header to `image/png` using the `media_type` attribute:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,15:16] hl[16] *}

Then you can use this new class in `response_class=PNGStreamingResponse` in your *path operation function*:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[19:22] hl[19] *}

### Simulate a File { #simulate-a-file }

In this example, we are simulating a file with `io.BytesIO`, which is a file-like object that lives only in memory, but lets us use the same interface.

For example, we can iterate over it as we could with a file.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:22] hl[3,10,21] *}

/// note | Technical Details

The other two variables, `image_base64` and `binary_image`, are an image encoded in Base64, and then converted to bytes, to then pass it to `io.BytesIO`.

Only so that it can live in the same file for this example and you can copy it and run it as is. 🥚

///

### Files and Async { #files-and-async }

In most cases, file-like objects and interfaces are not compatible by default with async and await.

For example, they don't have an `await file.read()`, or `async for chunk in file`.

And in many cases, reading them would be a blocking operation (that could block the event loop), because they are read from disk or from the network.

/// info

The example above is actually an exception, because the `io.BytesIO` object is already in memory, so reading it won't block anything.

But in many cases reading a file or a file-like object would block.

///

To avoid blocking the event loop, you can simply declare the *path operation function* with regular `def` instead of `async def`, that way FastAPI will run it on a threadpool worker, to avoid blocking the main loop.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[25:28] hl[26] *}

/// tip

If you need to call blocking code from inside of an async function, or an async function from inside of a blocking function, you could use <a href="https://asyncer.tiangolo.com" class="external-link" target="_blank">Asyncer</a>, a sibling library to FastAPI.

///
