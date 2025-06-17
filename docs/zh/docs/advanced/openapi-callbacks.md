# OpenAPI 回调

您可以创建触发外部 API 请求的*路径操作* API，这个外部 API 可以是别人创建的，也可以是由您自己创建的。

API 应用调用外部 API 时的流程叫做**回调**。因为外部开发者编写的软件发送请求至您的 API，然后您的 API 要进行回调，并把请求发送至外部 API。

此时，我们需要存档外部 API 的*信息*，比如应该有哪些*路径操作*，返回什么样的请求体，应该返回哪种响应等。

## 使用回调的应用

示例如下。

假设要开发一个创建发票的应用。

发票包括 `id`、`title`（可选）、`customer`、`total` 等属性。

API 的用户 （外部开发者）要在您的 API 内使用 POST 请求创建一条发票记录。

（假设）您的 API 将：

* 把发票发送至外部开发者的消费者
* 归集现金
* 把通知发送至 API 的用户（外部开发者）
    * 通过（从您的 API）发送 POST 请求至外部 API （即**回调**）来完成

## 常规 **FastAPI** 应用

添加回调前，首先看下常规 API 应用是什么样子。

常规 API 应用包含接收 `Invoice` 请求体的*路径操作*，还有包含回调 URL 的查询参数 `callback_url`。

这部分代码很常规，您对绝大多数代码应该都比较熟悉了：

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[10:14,37:54] *}

/// tip | 提示

`callback_url` 查询参数使用 Pydantic 的 <a href="https://pydantic-docs.helpmanual.io/usage/types/#urls" class="external-link" target="_blank">URL</a> 类型。

///

此处唯一比较新的内容是*路径操作装饰器*中的 `callbacks=invoices_callback_router.routes` 参数，下文介绍。

## 存档回调

实际的回调代码高度依赖于您自己的 API 应用。

并且可能每个应用都各不相同。

回调代码可能只有一两行，比如：

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
requests.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

但回调最重要的部分可能是，根据 API 要发送给回调请求体的数据等内容，确保您的 API 用户（外部开发者）正确地实现*外部 API*。

因此，我们下一步要做的就是添加代码，为从 API 接收回调的*外部 API*存档。

这部分文档在 `/docs` 下的 Swagger API 文档中显示，并且会告诉外部开发者如何构建*外部 API*。

本例没有实现回调本身（只是一行代码），只有文档部分。

/// tip | 提示

实际的回调只是 HTTP 请求。

实现回调时，要使用 <a href="https://www.encode.io/httpx/" class="external-link" target="_blank">HTTPX</a> 或 <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requests</a>。

///

## 编写回调文档代码

应用不执行这部分代码，只是用它来*记录 外部 API* 。

但，您已经知道用 **FastAPI** 创建自动 API 文档有多简单了。

我们要使用与存档*外部 API* 相同的知识……通过创建外部 API 要实现的*路径操作*（您的 API 要调用的）。

/// tip | 提示

编写存档回调的代码时，假设您是*外部开发者*可能会用的上。并且您当前正在实现的是*外部 API*，不是*您自己的 API*。

临时改变（为外部开发者的）视角能让您更清楚该如何放置*外部 API* 响应和请求体的参数与 Pydantic 模型等。

///

### 创建回调的 `APIRouter`

首先，新建包含一些用于回调的 `APIRouter`。

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[5,26] *}

### 创建回调*路径操作*

创建回调*路径操作*也使用之前创建的 `APIRouter`。

它看起来和常规 FastAPI *路径操作*差不多：

* 声明要接收的请求体，例如，`body: InvoiceEvent`
* 还要声明要返回的响应，例如，`response_model=InvoiceEventReceived`

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[17:19,22:23,29:33] *}

回调*路径操作*与常规*路径操作*有两点主要区别：

* 它不需要任何实际的代码，因为应用不会调用这段代码。它只是用于存档*外部 API*。因此，函数的内容只需要 `pass` 就可以了
* *路径*可以包含 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#key-expression" class="external-link" target="_blank">OpenAPI 3 表达式</a>（详见下文），可以使用带参数的变量，以及发送至您的 API 的原始请求的部分

### 回调路径表达式

回调*路径*支持包含发送给您的 API 的原始请求的部分的  <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#key-expression" class="external-link" target="_blank">OpenAPI 3 表达式</a>。

本例中是**字符串**：

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

因此，如果您的 API 用户（外部开发者）发送请求到您的 API：

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

使用如下 JSON 请求体：

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

然后，您的 API 就会处理发票，并在某个点之后，发送回调请求至 `callback_url`（外部 API）：

```
https://www.external.org/events/invoices/2expen51ve
```

JSON 请求体包含如下内容：

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

它会预期*外部 API* 的响应包含如下 JSON 请求体：

```JSON
{
    "ok": true
}
```

/// tip | 提示

注意，回调 URL包含 `callback_url` （`https://www.external.org/events`）中的查询参数，还有 JSON 请求体内部的发票 ID（`2expen51ve`）。

///

### 添加回调路由

至此，在上文创建的回调路由里就包含了*回调路径操作*（外部开发者要在外部 API 中实现）。

现在使用 API *路径操作装饰器*的参数 `callbacks`，从回调路由传递属性 `.routes`（实际上只是路由/路径操作的**列表**）：

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[36] *}

/// tip | 提示

注意，不能把路由本身（`invoices_callback_router`）传递给 `callback=`，要传递 `invoices_callback_router.routes` 中的 `.routes` 属性。

///

### 查看文档

现在，使用 Uvicorn 启动应用，打开 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs。</a>

就能看到文档的*路径操作*已经包含了**回调**的内容以及*外部 API*：

<img src="/img/tutorial/openapi-callbacks/image01.png">
