# Request Body Limits { #request-body-limits }

Imagine your app receives small JSON requests, but you also want to let users upload larger files.

You can set `max_body_size` in bytes when you create your `FastAPI` app. Then you can set a different limit for an `APIRouter` or for a single *path operation*.

{* ../../docs_src/request_body_limits/tutorial001.py hl[3:4,17] *}

* `POST /items` uses the app's limit of 1 MiB (`1024 * 1024` bytes).
* `POST /uploads/` uses the router's limit of 100 MiB.
* `POST /uploads/small` has its own limit of 10 MiB.

## What counts toward the limit? { #what-counts-toward-the-limit }

The limit applies to the **whole request body**. If you upload two files in the same request, both files, any form fields, and the bytes used to encode the multipart form all count toward that one limit. The URL and request headers are outside the body.

**FastAPI** counts the bytes it reads, even if the client sends the body in chunks without a `Content-Length` header. If a read exceeds the limit, FastAPI stops reading and returns an HTTP **413 Content Too Large** response if the response hasn't started yet.

If your *path operation* reads the body itself, it can start running before FastAPI knows the total size. For example, if you're streaming an upload to a temporary file, finish reading it before you publish the file.

With [`UploadFile`](../tutorial/request-files.md#file-parameters-with-uploadfile), a file can move from memory to disk as it grows. Its contents still count toward the same limit.

## Set a default for a router { #set-a-default-for-a-router }

You can also pass `max_body_size` to `include_router()`. The included router uses that default unless it declares its own limit. A *path operation* can always declare a smaller or larger limit of its own.

If you leave `max_body_size` at its default of `None`, it inherits the limit from the router or app that contains it. Mounted apps inherit the parent app's limit in the same way. If you don't set a limit anywhere, FastAPI leaves the body size unlimited. Use a positive integer for the number of bytes, or `0` to allow only an empty body.

/// note | Middleware that reads the body

If your middleware reads the body before FastAPI selects a *path operation*, the app's limit applies to that read. In the example above, middleware that calls `await request.body()` would reject a 2 MiB upload before it reaches the router that allows 100 MiB.

If the middleware passes the request to a mounted app, the mounted app's limit also applies to the bytes already read.

If your middleware needs to read those uploads, set the app's limit large enough for them and set smaller limits on the *path operations* that need them.

///
