# 处理错误 { #handling-errors }

在很多情况下，你需要向使用你 API 的客户端通知错误。

这里的客户端可以是带前端的浏览器、其他人的代码、IoT 设备等。

你可能需要告诉客户端：

* 客户端没有足够的权限执行该操作。
* 客户端没有访问该资源的权限。
* 客户端试图访问的 item 不存在。
* 等等。

在这些情况下，你通常会返回一个 **HTTP 状态码**，范围在 **400**（从 400 到 499）。

这类似于 200 HTTP 状态码（从 200 到 299）。这些 “200” 状态码表示请求在某种意义上“成功”了。

400 范围内的状态码表示来自客户端的错误。

还记得那些 **"404 Not Found"** 错误（以及相关笑话）吗？

## 使用 `HTTPException` { #use-httpexception }

要向客户端返回包含错误的 HTTP 响应，你可以使用 `HTTPException`。

### 导入 `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py39.py hl[1] *}

### 在代码中 raise `HTTPException` { #raise-an-httpexception-in-your-code }

`HTTPException` 是一个普通的 Python 异常，但包含了与 API 相关的额外数据。

因为它是 Python 异常，所以你不是 `return` 它，而是 `raise` 它。

这也意味着：如果你在一个工具函数中（该工具函数是在你的*路径操作函数*内部调用的）从工具函数内部 `raise` 了 `HTTPException`，那么它不会继续执行*路径操作函数*里剩下的代码，而是会立即终止该请求，并将 `HTTPException` 中的 HTTP 错误发送给客户端。

相较于返回一个值，抛出异常的好处会在 Dependencies 和 Security 章节中更明显。

在这个例子中，当客户端通过一个不存在的 ID 请求 item 时，raise 一个状态码为 `404` 的异常：

{* ../../docs_src/handling_errors/tutorial001_py39.py hl[11] *}

### 最终的响应 { #the-resulting-response }

如果客户端请求 `http://example.com/items/foo`（`item_id` 为 `"foo"`），它会收到 HTTP 状态码 200，以及如下 JSON 响应：

```JSON
{
  "item": "The Foo Wrestlers"
}
```

但如果客户端请求 `http://example.com/items/bar`（一个不存在的 `item_id` `"bar"`），它会收到 HTTP 状态码 404（“not found” 错误），以及如下 JSON 响应：

```JSON
{
  "detail": "Item not found"
}
```

/// tip | 提示

raise `HTTPException` 时，你可以通过参数 `detail` 传入任何能被转换为 JSON 的值，而不仅仅是 `str`。

你可以传入 `dict`、`list` 等。

它们会被 **FastAPI** 自动处理并转换为 JSON。

///

## 添加自定义响应头 { #add-custom-headers }

在某些情况下，为 HTTP 错误添加自定义响应头会很有用。例如，用于某些类型的安全需求。

你可能不会需要在代码中直接使用它。

但如果你在高级场景中需要它，可以添加自定义响应头：

{* ../../docs_src/handling_errors/tutorial002_py39.py hl[14] *}

## 安装自定义异常处理器 { #install-custom-exception-handlers }

你可以使用 <a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">Starlette 的相同异常工具</a> 来添加自定义异常处理器。

假设你有一个自定义异常 `UnicornException`，你（或你使用的某个库）可能会 `raise` 它。

并且你想用 FastAPI 在全局处理这个异常。

你可以使用 `@app.exception_handler()` 添加一个自定义异常处理器：

{* ../../docs_src/handling_errors/tutorial003_py39.py hl[5:7,13:18,24] *}

这里，如果你请求 `/unicorns/yolo`，该*路径操作*会 `raise` 一个 `UnicornException`。

但它会被 `unicorn_exception_handler` 处理。

因此，你会收到一个清晰的错误，HTTP 状态码为 `418`，并带有如下 JSON 内容：

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 注意

你也可以使用 `from starlette.requests import Request` 和 `from starlette.responses import JSONResponse`。

**FastAPI** 为开发者提供了与 `starlette.responses` 相同的 `fastapi.responses` 作为便捷方式。但大多数可用的响应类型直接来自 Starlette。`Request` 也是一样。

///

## 覆盖默认异常处理器 { #override-the-default-exception-handlers }

**FastAPI** 内置了一些默认异常处理器。

当你 `raise` 一个 `HTTPException` 以及当请求包含无效数据时，这些处理器负责返回默认的 JSON 响应。

你可以用你自己的异常处理器覆盖它们。

### 覆盖请求验证异常 { #override-request-validation-exceptions }

当请求包含无效数据时，**FastAPI** 内部会 raise 一个 `RequestValidationError`。

并且它也包含一个默认的异常处理器。

要覆盖它，导入 `RequestValidationError`，并使用 `@app.exception_handler(RequestValidationError)` 来装饰异常处理器。

该异常处理器会接收一个 `Request` 和该异常。

{* ../../docs_src/handling_errors/tutorial004_py39.py hl[2,14:19] *}

现在，如果你访问 `/items/foo`，你将不会得到默认的 JSON 错误信息：

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

而会得到一个文本版本：

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### 覆盖 `HTTPException` 错误处理器 { #override-the-httpexception-error-handler }

同样地，你也可以覆盖 `HTTPException` 的处理器。

例如，你可能希望对这些错误返回纯文本响应，而不是 JSON：

{* ../../docs_src/handling_errors/tutorial004_py39.py hl[3:4,9:11,25] *}

/// note | 注意

你也可以使用 `from starlette.responses import PlainTextResponse`。

**FastAPI** 为开发者提供了与 `starlette.responses` 相同的 `fastapi.responses` 作为便捷方式。但大多数可用的响应类型直接来自 Starlette。

///

/// warning | 警告

请记住，`RequestValidationError` 包含了发生验证错误时的文件名和行号信息，因此如果你愿意，可以把它连同相关信息一起输出到日志中。

但这也意味着，如果你只是把它转换为字符串并直接返回这些信息，你可能会泄露一些关于你系统的信息，这也是为什么这里的代码会把每个错误独立提取并展示。

///

### 使用 `RequestValidationError` 的请求体 { #use-the-requestvalidationerror-body }

`RequestValidationError` 包含它接收到的、带有无效数据的 `body`。

在开发应用时，你可以用它来记录 body 并调试，返回给用户等。

{* ../../docs_src/handling_errors/tutorial005_py39.py hl[14] *}

现在尝试发送一个无效的 item，例如：

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

你会收到一个响应，告诉你数据无效，并包含收到的 body：

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

#### FastAPI 的 `HTTPException` vs Starlette 的 `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** 有它自己的 `HTTPException`。

并且 **FastAPI** 的 `HTTPException` 错误类继承自 Starlette 的 `HTTPException` 错误类。

唯一的区别是：**FastAPI** 的 `HTTPException` 的 `detail` 字段接受任何可 JSON 化的数据，而 Starlette 的 `HTTPException` 只接受字符串。

因此，你可以像往常一样在代码中继续 raise **FastAPI** 的 `HTTPException`。

但是当你注册异常处理器时，你应该为 Starlette 的 `HTTPException` 注册。

这样一来，如果 Starlette 的内部代码、某个 Starlette 扩展或插件 raise 了 Starlette 的 `HTTPException`，你的处理器就能够捕获并处理它。

在这个例子中，为了能在同一份代码里同时使用这两个 `HTTPException`，Starlette 的异常被重命名为 `StarletteHTTPException`：

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### 复用 **FastAPI** 的异常处理器 { #reuse-fastapis-exception-handlers }

如果你想结合异常一起使用 **FastAPI** 的默认异常处理器，你可以从 `fastapi.exception_handlers` 导入并复用默认异常处理器：

{* ../../docs_src/handling_errors/tutorial006_py39.py hl[2:5,15,21] *}

在这个例子中，你只是用一条非常“生动”的消息打印了错误，但你应该理解意思了：你可以使用异常，然后直接复用默认异常处理器。
