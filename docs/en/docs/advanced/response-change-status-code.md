# Response - Change Status Code

You probably read before that you can set a default [Response Status Code](../tutorial/response-status-code.md){.internal-link target=_blank}.

But in some cases you need to return a different status code than the default.

## Use case

For example, imagine that you want to return an HTTP status code of "OK" `200` by default.

But if the data didn't exist, you want to create it, and return an HTTP status code of "CREATED" `201`.

But you still want to be able to filter and convert the data you return with a `response_model`.

For those cases, you can use a `Response` parameter.

## Use a `Response` parameter

You can declare a parameter of type `Response` in your *path operation function* (as you can do for cookies and headers).

And then you can set the `status_code` in that *temporal* response object.

```Python hl_lines="1  9  12"
{!../../../docs_src/response_change_status_code/tutorial001.py!}
```

And then you can return any object you need, as you normally would (a `dict`, a database model, etc).

And if you declared a `response_model`, it will still be used to filter and convert the object you returned.

**FastAPI** will use that *temporal* response to extract the status code (also cookies and headers), and will put them in the final response that contains the value you returned, filtered by any `response_model`.

You can also declare the `Response` parameter in dependencies, and set the status code in them. But have in mind that the last one to be set will win.
