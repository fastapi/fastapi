# OpenAPI Webhooks { #openapi-webhooks }

有些情况下，你可能想告诉你的 API **用户**：你的应用可以携带一些数据调用*他们的*应用（发送一个请求），通常是为了**通知**某种类型的**事件**。

这意味着，与通常由你的用户向你的 API 发送请求的流程不同，这里是**你的 API**（或你的应用）可以向**他们的系统**（他们的 API、他们的应用）**发送请求**。

这通常被称为 **webhook**。

## Webhooks 步骤 { #webhooks-steps }

通常的流程是：**你在代码中定义**你将发送的消息，也就是**请求体**。

你还需要以某种方式定义你的应用会在**哪些时刻**发送这些请求或事件。

并且，**你的用户**会以某种方式（例如在某个 Web 仪表板上）定义你的应用应该将这些请求发送到的 **URL**。

关于如何注册 webhook 的 URL 的所有**逻辑**，以及实际发送这些请求的代码，都由你决定。你可以在**自己的代码**中按你想要的方式来编写。

## 使用 **FastAPI** 和 OpenAPI 文档化 webhooks { #documenting-webhooks-with-fastapi-and-openapi }

使用 **FastAPI**，通过 OpenAPI，你可以定义这些 webhook 的名称、你的应用可以发送的 HTTP 操作类型（例如 `POST`、`PUT` 等），以及你的应用将发送的请求**体**。

这能让你的用户更轻松地**实现他们的 API** 来接收你的 **webhook** 请求，他们甚至可能能够自动生成一些他们自己的 API 代码。

/// info | 信息

webhooks 在 OpenAPI 3.1.0 及以上版本中可用，FastAPI `0.99.0` 及以上版本支持。

///

## 带有 webhooks 的应用 { #an-app-with-webhooks }

当你创建一个 **FastAPI** 应用时，有一个 `webhooks` 属性可用于定义 *webhooks*，方式与你定义 *path operations* 相同，例如使用 `@app.webhooks.post()`。

{* ../../docs_src/openapi_webhooks/tutorial001_py39.py hl[9:13,36:53] *}

你定义的 webhooks 最终会出现在 **OpenAPI** schema 和自动生成的 **docs UI** 中。

/// info | 信息

`app.webhooks` 对象实际上只是一个 `APIRouter`，与你在使用多个文件来组织应用时会用到的类型相同。

///

注意：使用 webhooks 时，你实际上并没有声明一个 *path*（比如 `/items/`），你传入的文本只是该 webhook 的**标识符**（事件名称）。例如在 `@app.webhooks.post("new-subscription")` 中，webhook 的名称是 `new-subscription`。

这是因为我们预期**你的用户**会以其他方式（例如通过 Web 仪表板）来定义他们希望接收 webhook 请求的实际 **URL path**。

### 查看文档 { #check-the-docs }

现在你可以启动你的应用并访问 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

你会看到你的文档不仅有正常的 *path operations*，现在还多了一些 **webhooks**：

<img src="/img/tutorial/openapi-webhooks/image01.png">
