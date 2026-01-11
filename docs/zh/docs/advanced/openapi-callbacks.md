# OpenAPI 回调 { #openapi-callbacks }

你可以创建一个 API，其中某个*路径操作*可以触发对某个由他人创建的*外部 API*的请求（很可能就是那个将会*使用*你 API 的开发者）。

当你的 API 应用调用*外部 API*时发生的流程称为“回调”。因为外部开发者编写的软件会向你的 API 发送请求，然后你的 API 会*回调*，向某个*外部 API*发送请求（这个外部 API 很可能也是同一个开发者创建的）。

在这种情况下，你可能想要记录这个外部 API *应该*是什么样的。它应该有哪些*路径操作*，期望什么请求体，应该返回什么响应，等等。

## 带回调的应用 { #an-app-with-callbacks }

我们来看一个例子。

想象你在开发一个允许创建发票的应用。

这些发票会有 `id`、`title`（可选）、`customer` 和 `total`。

你的 API 用户（外部开发者）会通过 POST 请求在你的 API 中创建一张发票。

然后你的 API 将会（我们假设）：

* 把发票发送给外部开发者的某个客户。
* 收款。
* 向 API 用户（外部开发者）发回一条通知。
    * 这将通过（从*你的 API*）向该外部开发者提供的某个*外部 API*发送一个 POST 请求来完成（这就是“回调”）。

## 常规 **FastAPI** 应用 { #the-normal-fastapi-app }

我们先看看在添加回调之前，常规 API 应用是什么样的。

它会有一个接收 `Invoice` 请求体的*路径操作*，以及一个包含回调 URL 的查询参数 `callback_url`。

这部分很常规，你对大多数代码可能都已经很熟悉了：

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[7:11,34:51] *}

/// tip | 提示

`callback_url` 查询参数使用 Pydantic 的 <a href="https://docs.pydantic.dev/latest/api/networks/" class="external-link" target="_blank">Url</a> 类型。

///

唯一的新内容是：*路径操作装饰器*的参数 `callbacks=invoices_callback_router.routes`。接下来我们会看到这是什么。

## 为回调编写文档 { #documenting-the-callback }

实际的回调代码会高度依赖于你自己的 API 应用。

并且它可能在不同应用之间差异很大。

它可能只有一两行代码，例如：

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

但回调可能最重要的部分，是确保你的 API 用户（外部开发者）根据*你的 API*在回调请求体中要发送的数据等内容，正确实现*外部 API*。

所以，我们接下来要做的是添加代码，用于记录那个*外部 API*为了接收来自*你的 API*的回调，*应该*是什么样的。

这份文档会显示在你的 API 的 `/docs`（Swagger UI）中，并让外部开发者知道如何构建这个*外部 API*。

这个示例不会实现回调本身（那可能只是一行代码），只实现文档部分。

/// tip | 提示

实际的回调只是一个 HTTP 请求。

当你自己实现回调时，可以使用类似 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> 或 <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requests</a> 的库。

///

## 编写回调文档代码 { #write-the-callback-documentation-code }

这段代码不会在你的应用中执行，我们只需要它来*记录*那个*外部 API*应该是什么样的。

但是，你已经知道用 **FastAPI** 为 API 轻松创建自动文档是多么简单了。

所以我们会用同样的知识来记录*外部 API*应该是什么样的……通过创建外部 API 应该实现的*路径操作*（你的 API 将会调用的那些）。

/// tip | 提示

在编写用于记录回调的代码时，把自己想象成那个*外部开发者*可能会很有帮助。并且你当前是在实现*外部 API*，而不是*你的 API*。

暂时采用这种（*外部开发者*的）视角，可以让你更直观地知道：在那个*外部 API*中，参数应该放在哪里，请求体和响应的 Pydantic 模型应该如何放置，等等。

///

### 创建回调 `APIRouter` { #create-a-callback-apirouter }

首先创建一个新的 `APIRouter`，它将包含一个或多个回调。

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[1,23] *}

### 创建回调*路径操作* { #create-the-callback-path-operation }

要创建回调*路径操作*，使用上面创建的同一个 `APIRouter`。

它看起来应该就像一个普通的 FastAPI *路径操作*：

* 它应该声明要接收的请求体，例如 `body: InvoiceEvent`。
* 并且它也可以声明要返回的响应，例如 `response_model=InvoiceEventReceived`。

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[14:16,19:20,26:30] *}

与普通*路径操作*相比，有 2 个主要区别：

* 它不需要任何实际代码，因为你的应用永远不会调用这段代码。它只用于记录*外部 API*。所以，这个函数可以只有 `pass`。
* *路径*可以包含一个 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">OpenAPI 3 表达式</a>（下面会详细介绍），它可以使用带参数的变量，以及发送到*你的 API*的原始请求的部分内容。

### 回调路径表达式 { #the-callback-path-expression }

回调*路径*可以包含一个 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">OpenAPI 3 表达式</a>，它可以包含发送到*你的 API*的原始请求的部分内容。

在这个例子中，它是 `str`：

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

所以，如果你的 API 用户（外部开发者）向*你的 API*发送请求到：

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

并使用如下 JSON 请求体：

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

那么*你的 API*会处理发票，并在之后的某个时间点，向 `callback_url`（*外部 API*）发送回调请求：

```
https://www.external.org/events/invoices/2expen51ve
```

其 JSON 请求体包含类似如下内容：

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

并且它会期望那个*外部 API*返回一个包含如下 JSON 请求体的响应：

```JSON
{
    "ok": true
}
```

/// tip | 提示

注意：回调 URL 同时包含了通过 `callback_url` 这个查询参数收到的 URL（`https://www.external.org/events`），以及 JSON 请求体中的发票 `id`（`2expen51ve`）。

///

### 添加回调路由 { #add-the-callback-router }

此时，你在上面创建的回调路由中已经有了所需的*回调路径操作*（即那个*外部开发者*应该在*外部 API*中实现的那些）。

现在在*你的 API 的路径操作装饰器*中使用参数 `callbacks`，从该回调路由中传入属性 `.routes`（它实际上只是一个路由/*路径操作*的 `list`）：

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[33] *}

/// tip | 提示

注意，你传给 `callback=` 的不是路由本身（`invoices_callback_router`），而是 `.routes` 属性，即 `invoices_callback_router.routes`。

///

### 查看文档 { #check-the-docs }

现在你可以启动应用并访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到文档中包含你的*路径操作*的 “Callbacks” 部分，展示*外部 API*应该是什么样的：

<img src="/img/tutorial/openapi-callbacks/image01.png">
