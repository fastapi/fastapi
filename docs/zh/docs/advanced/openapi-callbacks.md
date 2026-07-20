# OpenAPI 回调 { #openapi-callbacks }

你可以创建一个包含*路径操作*的 API，该*路径操作*可以触发对其他人创建的*外部 API*的请求（很可能就是那个会*使用*你的 API 的同一个开发者）。

当你的 API 应用调用*外部 API*时，这个过程被称为“回调”。因为外部开发者编写的软件会先向你的 API 发送请求，然后你的 API 再*回调*，向*外部 API*发送请求（很可能也是该开发者创建的）。

在这种情况下，你可能希望记录该外部 API *应该*是什么样子。它应该有哪些*路径操作*，应该接收什么请求体，应该返回什么响应等。

## 使用回调的应用 { #an-app-with-callbacks }

让我们通过一个例子来看这一切。

假设你开发一个可以创建发票的应用。

这些发票会有 `id`、`title`（可选）、`customer` 和 `total`。

你的 API 用户（外部开发者）会通过 POST 请求在你的 API 中创建一张发票。

然后你的 API 会（假设）：

* 将发票发送给外部开发者的某个客户。
* 收款。
* 向 API 用户（外部开发者）发回通知。
    * 这会通过（从*你的 API*）向该外部开发者提供的某个*外部 API*发送 POST 请求来完成（这就是“回调”）。

## 常规 **FastAPI** 应用 { #the-normal-fastapi-app }

我们先看看在添加回调之前，常规 API 应用会是什么样子。

它会有一个接收 `Invoice` 请求体的*路径操作*，以及一个包含回调 URL 的查询参数 `callback_url`。

这部分很常规，大部分代码你应该已经很熟悉了：

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[7:11,34:51] *}

/// tip | 提示

`callback_url` 查询参数使用 Pydantic 的 [Url](https://docs.pydantic.dev/latest/api/networks/) 类型。

///

唯一的新内容是*路径操作装饰器*中的参数 `callbacks=invoices_callback_router.routes`。接下来我们会看看它是什么。

## 为回调编写文档 { #documenting-the-callback }

实际的回调代码会高度依赖你自己的 API 应用。

而且很可能在不同应用之间差异很大。

它可能只有一两行代码，例如：

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

但回调最重要的部分可能是确保你的 API 用户（外部开发者）正确实现*外部 API*，与*你的 API*将在回调请求体中发送的数据等相匹配。

因此，接下来我们要做的是添加代码，用来记录该*外部 API*应该是什么样子，才能接收来自*你的 API*的回调。

这份文档会显示在你的 API 的 `/docs` 下的 Swagger UI 中，并且会让外部开发者知道如何构建*外部 API*。

本例不实现回调本身（那可能只是一行代码），只实现文档部分。

/// tip | 提示

实际的回调只是一个 HTTP 请求。

自己实现回调时，你可以使用类似 [HTTPX](https://www.python-httpx.org) 或 [Requests](https://requests.readthedocs.io/) 的工具。

///

## 编写回调文档代码 { #write-the-callback-documentation-code }

这段代码不会在你的应用中执行，我们只需要用它来*记录*该*外部 API*应该是什么样子。

不过，你已经知道如何使用 **FastAPI** 轻松为 API 创建自动文档了。

因此，我们会使用相同的知识来记录该*外部 API*应该是什么样子...通过创建外部 API 应该实现的*路径操作*（也就是你的 API 将调用的那些）。

/// tip | 提示

在编写用于记录回调的代码时，可以想象你就是那个*外部开发者*。而且你现在正在实现的是*外部 API*，不是*你的 API*。

临时采用这个（*外部开发者*的）视角，可以帮助你更清楚地判断该把参数、请求体的 Pydantic 模型、响应等放在该*外部 API*的什么位置。

///

### 创建回调 `APIRouter` { #create-a-callback-apirouter }

首先创建一个新的 `APIRouter`，它将包含一个或多个回调。

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[1,23] *}

### 创建回调*路径操作* { #create-the-callback-path-operation }

要创建回调*路径操作*，请使用你在上面创建的同一个 `APIRouter`。

它看起来应该就像普通的 FastAPI *路径操作*：

* 它可能应该声明要接收的请求体，例如 `body: InvoiceEvent`。
* 它也可以声明要返回的响应，例如 `response_model=InvoiceEventReceived`。

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[14:16,19:20,26:30] *}

它与普通*路径操作*有 2 个主要区别：

* 它不需要任何实际代码，因为你的应用永远不会调用这段代码。它只用于记录*外部 API*。因此，函数可以只有 `pass`。
* *路径*可以包含 [OpenAPI 3 表达式](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression)（见下文），其中可以使用带参数的变量，以及发送到*你的 API*的原始请求的部分内容。

### 回调路径表达式 { #the-callback-path-expression }

回调*路径*可以有一个 [OpenAPI 3 表达式](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression)，其中可以包含发送到*你的 API*的原始请求的部分内容。

在这个例子中，它是这个 `str`：

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

所以，如果你的 API 用户（外部开发者）向*你的 API*发送请求到：

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

并带有如下 JSON 请求体：

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

那么*你的 API*会处理该发票，并在稍后的某个时间点，向 `callback_url`（*外部 API*）发送回调请求：

```
https://www.external.org/events/invoices/2expen51ve
```

并带有类似如下内容的 JSON 请求体：

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

它会预期该*外部 API*返回类似如下 JSON 请求体的响应：

```JSON
{
    "ok": true
}
```

/// tip | 提示

请注意，使用的回调 URL 包含在 `callback_url` 中作为查询参数接收到的 URL（`https://www.external.org/events`），也包含 JSON 请求体内部的发票 `id`（`2expen51ve`）。

///

### 添加回调路由 { #add-the-callback-router }

此时，你已经在上面创建的回调路由中拥有了所需的*回调路径操作*（即*外部开发者*应该在*外部 API*中实现的那些）。

现在，在*你的 API 的路径操作装饰器*中使用参数 `callbacks`，传入该回调路由的 `.routes` 属性：

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[33] *}

/// tip | 提示

请注意，你不是把路由本身（`invoices_callback_router`）传给 `callbacks=`，而是传它的 `.routes`，也就是 `invoices_callback_router.routes`。FastAPI 会使用这些路由来生成回调的 OpenAPI 文档。

///

### 查看文档 { #check-the-docs }

现在你可以启动应用并访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)。

你会看到文档中为你的*路径操作*包含了一个 "Callbacks" 部分，展示了*外部 API*应该是什么样子：

<img src="/img/tutorial/openapi-callbacks/image01.png">
