# 处理错误 { #handling-errors }

某些情况下，需要向使用你的 API 的客户端返回错误提示。

这里所谓的客户端包括前端浏览器、他人的代码、物联网设备等。

你可能需要告诉客户端：

- 客户端没有执行该操作的权限
- 客户端没有访问该资源的权限
- 客户端要访问的项目不存在
- 等等

遇到这些情况时，通常要返回 **4XX**（400 至 499）**HTTP 状态码**。

这与表示请求成功的 **2XX**（200 至 299）HTTP 状态码类似。那些“200”状态码表示某种程度上的“成功”。

而 **4XX** 状态码表示客户端发生了错误。

大家都知道**「404 Not Found」**错误，还有调侃这个错误的笑话吧？

## 使用 `HTTPException` { #use-httpexception }

向客户端返回 HTTP 错误响应，可以使用 `HTTPException`。

### 导入 `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### 在代码中触发 `HTTPException` { #raise-an-httpexception-in-your-code }

`HTTPException` 是额外包含了和 API 有关数据的常规 Python 异常。

因为是 Python 异常，所以不能 `return`，只能 `raise`。

这也意味着，如果你在*路径操作函数*里调用的某个工具函数内部触发了 `HTTPException`，那么*路径操作函数*中后续的代码将不会继续执行，请求会立刻终止，并把 `HTTPException` 的 HTTP 错误发送给客户端。

在介绍依赖项与安全的章节中，你可以更直观地看到用 `raise` 异常代替 `return` 值的优势。

本例中，客户端用不存在的 `ID` 请求 `item` 时，触发状态码为 `404` 的异常：

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### 响应结果 { #the-resulting-response }

请求为 `http://example.com/items/foo`（`item_id` 为 `"foo"`）时，客户端会接收到 HTTP 状态码 200 及如下 JSON 响应结果：

```JSON
{
  "item": "The Foo Wrestlers"
}
```

但如果客户端请求 `http://example.com/items/bar`（不存在的 `item_id` `"bar"`），则会接收到 HTTP 状态码 404（“未找到”错误）及如下 JSON 响应结果：

```JSON
{
  "detail": "Item not found"
}
```

/// tip | 提示

触发 `HTTPException` 时，可以用参数 `detail` 传递任何能转换为 JSON 的值，不仅限于 `str`。

还支持传递 `dict`、`list` 等数据结构。

**FastAPI** 能自动处理这些数据，并将之转换为 JSON。

///

## 添加自定义响应头 { #add-custom-headers }

有些场景下要为 HTTP 错误添加自定义响应头。例如，出于某些类型的安全需要。

一般情况下你可能不会在代码中直接使用它。

但在某些高级场景中需要时，你可以添加自定义响应头：

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## 安装自定义异常处理器 { #install-custom-exception-handlers }

可以使用<a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">与 Starlette 相同的异常处理工具</a>添加自定义异常处理器。

假设有一个自定义异常 `UnicornException`（你自己或你使用的库可能会 `raise` 它）。

并且你希望用 FastAPI 在全局处理该异常。

此时，可以用 `@app.exception_handler()` 添加自定义异常处理器：

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

这里，请求 `/unicorns/yolo` 时，路径操作会触发 `UnicornException`。

但该异常将会被 `unicorn_exception_handler` 处理。

你会收到清晰的错误信息，HTTP 状态码为 `418`，JSON 内容如下：

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 技术细节

也可以使用 `from starlette.requests import Request` 和 `from starlette.responses import JSONResponse`。

**FastAPI** 提供了与 `starlette.responses` 相同的 `fastapi.responses` 作为便捷方式，但大多数可用的响应都直接来自 Starlette。`Request` 也是如此。

///

## 覆盖默认异常处理器 { #override-the-default-exception-handlers }

**FastAPI** 自带了一些默认异常处理器。

当你触发 `HTTPException`，或者请求中包含无效数据时，这些处理器负责返回默认的 JSON 响应。

你也可以用自己的处理器覆盖它们。

### 覆盖请求验证异常 { #override-request-validation-exceptions }

请求中包含无效数据时，**FastAPI** 内部会触发 `RequestValidationError`。

它也内置了该异常的默认处理器。

要覆盖它，导入 `RequestValidationError`，并用 `@app.exception_handler(RequestValidationError)` 装饰你的异常处理器。

异常处理器会接收 `Request` 和该异常。

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

现在，访问 `/items/foo` 时，默认的 JSON 错误为：

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

将得到如下文本内容：

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### 覆盖 `HTTPException` 错误处理器 { #override-the-httpexception-error-handler }

同理，也可以覆盖 `HTTPException` 的处理器。

例如，只为这些错误返回纯文本响应，而不是 JSON：

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | 技术细节

还可以使用 `from starlette.responses import PlainTextResponse`。

**FastAPI** 提供了与 `starlette.responses` 相同的 `fastapi.responses` 作为便捷方式，但大多数可用的响应都直接来自 Starlette。

///

/// warning | 警告

请注意，`RequestValidationError` 包含发生验证错误的文件名和行号信息，你可以在需要时将其记录到日志中以提供相关信息。

但这也意味着，如果你只是将其直接转换为字符串并返回，可能会泄露一些关于系统的细节信息。因此，这里的代码会提取并分别显示每个错误。

///

### 使用 `RequestValidationError` 的请求体 { #use-the-requestvalidationerror-body }

`RequestValidationError` 包含其接收到的带有无效数据的请求体 `body`。

开发时，你可以用它来记录请求体、调试错误，或返回给用户等。

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

现在试着发送一个无效的 `item`，例如：

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

收到的响应会告诉你数据无效，并包含收到的请求体：

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

**FastAPI** 也提供了自有的 `HTTPException`。

**FastAPI** 的 `HTTPException` 错误类继承自 Starlette 的 `HTTPException` 错误类。

它们之间的唯一区别是，**FastAPI** 的 `HTTPException` 在 `detail` 字段中接受任意可转换为 JSON 的数据，而 Starlette 的 `HTTPException` 只接受字符串。

因此，你可以继续像平常一样在代码中触发 **FastAPI** 的 `HTTPException`。

但注册异常处理器时，应该注册到来自 Starlette 的 `HTTPException`。

这样做是为了，当 Starlette 的内部代码、扩展或插件触发 Starlette `HTTPException` 时，你的处理器能够捕获并处理它。

本例中，为了在同一份代码中同时使用两个 `HTTPException`，将 Starlette 的异常重命名为 `StarletteHTTPException`：

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### 复用 **FastAPI** 的异常处理器 { #reuse-fastapis-exception-handlers }

如果你想在自定义处理后仍复用 **FastAPI** 的默认异常处理器，可以从 `fastapi.exception_handlers` 导入并复用这些默认处理器：

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

虽然本例只是用非常夸张的信息打印了错误，但足以说明：你可以先处理异常，然后再复用默认的异常处理器。
