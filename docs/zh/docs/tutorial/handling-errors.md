# 处理错误

许多情况下，您需要将错误通知使用您的API的客户端。

这个客户端可以是一个带有前端的浏览器、来自其他人的代码、物联网设备等。

你可能需要告诉客户:

* 客户端没有足够的权限进行该操作。
* 客户端无法访问该资源。
* 客户端试图访问的项目不存在
* 等。

在这些情况下，您通常会返回一个 **HTTP 状态码** 其范围为 **400** (从 400 到 499)。

这类似于200 HTTP状态码 (从 200 到 299)。这些 "200" 状态码意味着请求 "成功" 了。

在400范围内的状态码意味着来自客户端的错误。

还记得所有那些 **"404 Not Found"** 错误(和笑话)吗?

## 使用 `HTTPException`

要向客户端返回带有错误的HTTP响应，请使用 `HTTPException`.

### 导入 `HTTPException`

```Python hl_lines="1"
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### 在你的代码中抛出一个 `HTTPException`

`HTTPException` 是一个正常的Python异常，带有与 APIs 相关的额外数据。

因为它是一个Python异常，你不是 `return` 它，而是 `raise` 它。

这也意味着,如果你在你的 *路径操作函数* 中调用的一个应用函数中抛出 `HTTPException` ， *路径操作函数* 中的后续代码将不会被运行，它会立即终止请求并将来自 `HTTPException` 的HTTP错误发送给客户端。

在有关依赖关系和安全性的部分中，抛出异常而不是 `return` 值的好处将更加明显。

本例中，当客户端通过一个不存在的ID请求一个条目时，会抛出一个状态码为 `404` 的异常:

```Python hl_lines="11"
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### 产生的响应

如果客户端请求 `http://example.com/items/foo` (一个 `item_id` `"foo"`), 该客户端将收到一个HTTP状态码200和一个JSON响应:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

但如果客户端请求 `http://example.com/items/bar` (一个不存在的 `item_id` `"bar"`), 该客户端将收到一个HTTP状态码404 ("not found"错误)和一个JSON响应:

```JSON
{
  "detail": "Item not found"
}
```

!!! tip
    当抛出一个 `HTTPException` 时，你可以给 `detail` 参数传递任何可以转换为JSON的值, 不仅仅是 `str`.

    你可以传递一个 `dict`, 一个 `list`, 等等。

    它们由 **FastAPI** 自动处理并转换为JSON。

## 添加自定义消息头

在某些情况下，向HTTP错误添加自定义消息头是有用的。例如，对于某些类型的安全性。

您可能不需要在代码中直接使用它。

但如果你在某个高级场景需要它，你可以添加自定义头:

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial002.py!}
```

## 安装自定义异常处理程序

您可以使用 <a href="https://www.starlette.io/exceptions/" class="external-link" target="_blank">与 Starlette 中的异常实用程序相同</a> 方法添加自定义异常处理程序。

假设你有一个自定义的异常 `UnicornException` 你(或者你使用的库)将会 `raise`。

你想用FastAPI全局地处理这个异常。

您可以添加一个自定义异常处理程序 `@app.exception_handler()`:

```Python hl_lines="5-7  13-18  24"
{!../../../docs_src/handling_errors/tutorial003.py!}
```

在这里，如果您请求 `/unicorns/yolo`, *路径操作* 将会 `raise` 一个 `UnicornException` 。

但它将由 `unicorn_exception_handler` 处理。

因此，你将收到一个干净的错误, 包括一个HTTP状态码' `418` '和一个JSON内容：

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

!!! note "技术细节"
    你也可以使用 `from starlette.requests import Request` 和 `from starlette.responses import JSONResponse`。

    **FastAPI** 提供的 `fastapi.responses` 与 `starlette.responses` 相同，只是为了方便开发人员。但大多数可用的响应都直接来自Starlette。和 `Request` 相同。

## 重载默认的异常处理程序

**FastAPI** 有一些默认的异常处理程序。

These handlers are in charge of returning the default JSON responses when you `raise` an `HTTPException` and when the request has invalid data.当你 `raise` 一个 `HTTPException` 或请求具有无效数据时，这些处理程序负责返回默认的JSON响应。

您可以用自己的异常处理程序覆盖这些异常处理程序。

### 重载请求异常验证

当一个请求包含无效数据时，**FastAPI** 在内部抛出一个 `RequestValidationError`.

它还包括一个默认的异常处理程序。

要重载它，导入 `RequestValidationError` 并在 `@app.exception_handler(RequestValidationError)` 中使用来装饰异常处理程序。

异常处理程序将接收一个 `Request` 和异常.

```Python hl_lines="2  14-16"
{!../../../docs_src/handling_errors/tutorial004.py!}
```

现在，如果你访问 `/items/foo`, 你将不会得到一个默认的 JSON 错误信息：

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

您将得到一个文本版本:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs `ValidationError`

!!! warning
    如果这些技术细节现在对你不重要的话，你可以跳过。

`RequestValidationError` 是 Pydantic 的 <a href="https://pydantic-docs.helpmanual.io/#error-handling" class="external-link" target="_blank">`ValidationError`</a>的一个子类。

**FastAPI** 使用它，所以当你在 `response_model` 中一个 Pydantic 模型，并且你的数据有一个错误，你将会在你的日志汇总看到这个错误。 

但是客户端/用户不会看到它。相反，客户端将收到一个带有HTTP状态码 `500` 的 "内部服务器错误" 。

它应该这样子做，因为如果你在你的 *响应* 或者其他代码(不是客户的 *请求* )中有一个Pydantic `ValidationError`， 它实际上是你代码中的一个错误。

当您修复它时，您的客户端/用户不应该访问关于错误的内部信息，因为这可能会暴露一个安全漏洞。

### 重载 `HTTPException` 错误处理程序

同样，您可以重载 `HTTPException` 处理程序。

例如，对于这些错误，你可能想要返回一个纯文本的响应而不是JSON:

```Python hl_lines="3-4  9-11  22"
{!../../../docs_src/handling_errors/tutorial004.py!}
```

!!! note "技术细节"
    你也可以使用 `from starlette.responses import PlainTextResponse`.

    **FastAPI** 提供了`fastapi.responses` 和 `starlette.responses` 是一样的，只是为了方便开发者。但是大多数可用的响应都直接来自 Starlette。

### 使用 `RequestValidationError` 主体

`RequestValidationError` 包含它接收到的带有无效数据的 `body` 。

你可以在开发你的应用程序时使用它来记录主体并调试它，返回给用户等等。

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial005.py!}
```

现在尝试发送一个无效的项目，如:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

您将收到一个响应，告诉您的数据是无效的，包含接收到的主体:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI 的 `HTTPException` 和 Starlette 的 `HTTPException`

**FastAPI** 拥有自己的 `HTTPException`.

并且 **FastAPI** 的 `HTTPException` 错误类继承自 Starlette 的 `HTTPException` 错误类。

唯一的区别是 **FastAPI** 的 `HTTPException` 允许你在响应中添加消息头。

这是 OAuth 2.0 和一些其它安全工具在内部需要/使用的。

你可以像往常一样在代码中抛出 **FastAPI** 的 `HTTPException` 。

但是当你注册一个异常处理程序时，你应该为 Starlette 的 `HTTPException` 注册。

这样，如果 Starlette 的任何内部代码，或 Starlette 扩展或插件引发Starlette `HTTPException` ，您的处理程序将能够捕获并处理它。

在这个例子中，为了能够在相同的代码中同时拥有两个 `HTTPException`，Starlette 的异常被重命名为`StarletteHTTPException` ：

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### 重用 **FastAPI** 的异常处理程序

您也可以只是想以某种方式使用异常，然后使用 **FastAPI** 中相同的缺省异常处理程序。

你可以从 `fastapi.exception_handlers` 导入和重用默认的异常处理程序:

```Python hl_lines="2-5  15  21"
{!../../../docs_src/handling_errors/tutorial006.py!}
```

在这个例子中，你只是用一个非常有表现力的信息来 `打印` 错误。

但你应该明白，你可以使用异常然后重用默认的异常处理程序。
