# 响应状态码 { #response-status-code }

与指定响应模型的方式相同，在以下任意*路径操作*中，也可以使用 `status_code` 参数声明用于响应的 HTTP 状态码：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等。

{* ../../docs_src/response_status_code/tutorial001_py39.py hl[6] *}

/// note | 注意

注意，`status_code` 是（`get`、`post` 等）“装饰器”方法中的参数。与所有参数和请求体一样，它不是你的*路径操作函数*的参数。

///

`status_code` 参数接收一个包含 HTTP 状态码的数字。

/// info | 信息

`status_code` 也可以接收 `IntEnum`，例如 Python 的 <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>。

///

它会：

* 在响应中返回该状态码。
* 在 OpenAPI schema（因此也会在用户界面中）将其记录为该状态码：

<img src="/img/tutorial/response-status-code/image01.png">

/// note | 注意

某些响应码（参见下一节）表示响应没有响应体。

FastAPI 知道这一点，并会生成说明没有响应体的 OpenAPI 文档。

///

## 关于 HTTP 状态码 { #about-http-status-codes }

/// note | 注意

如果你已经知道 HTTP 状态码是什么，请跳到下一节。

///

在 HTTP 中，你会在响应中发送一个 3 位数的数字状态码。

这些状态码都有关联的名称用于识别，但重要的部分是数字。

简而言之：

* `100 - 199` 用于“信息”。你很少直接使用它们。具有这些状态码的响应不能包含响应体。
* **`200 - 299`** 用于“成功”的响应。这些是你最常用的。
    * `200` 是默认状态码，表示一切都“OK”。
    * 另一个例子是 `201`，“Created”。通常在数据库中创建新记录后使用。
    * 一个特殊情况是 `204`，“No Content”。当没有内容要返回给客户端时会使用该响应，因此响应不得包含响应体。
* **`300 - 399`** 用于“重定向”。具有这些状态码的响应可以包含或不包含响应体，但 `304`，“Not Modified” 除外，它不得包含响应体。
* **`400 - 499`** 用于“客户端错误”的响应。这可能是你第二常用的一类。
    * 例如 `404`，用于“Not Found”响应。
    * 对于来自客户端的通用错误，你可以直接使用 `400`。
* `500 - 599` 用于服务器错误。你几乎不会直接使用它们。当你的应用代码或服务器某个部分出问题时，会自动返回其中一个状态码。

/// tip | 提示

想了解每个状态码的更多信息，以及每个状态码分别用于什么场景，请查看 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> 关于 HTTP 状态码的文档</a>。

///

## 便于记住名称的快捷方式 { #shortcut-to-remember-the-names }

让我们再看一遍前面的例子：

{* ../../docs_src/response_status_code/tutorial001_py39.py hl[6] *}

`201` 是 “Created” 的状态码。

但你不必记住每个状态码的含义。

你可以使用 `fastapi.status` 中的便捷变量。

{* ../../docs_src/response_status_code/tutorial002_py39.py hl[1,6] *}

它们只是为了方便，保存的是相同的数字，但这样你可以使用编辑器的自动补全来找到它们：

<img src="/img/tutorial/response-status-code/image02.png">

/// note | 技术细节

你也可以使用 `from starlette import status`。

**FastAPI** 提供了与 `starlette.status` 相同的 `fastapi.status`，只是为了方便你（开发者）。但它直接来自 Starlette。

///

## 更改默认值 { #changing-the-default }

稍后，在[高级用户指南](../advanced/response-change-status-code.md){.internal-link target=_blank}中，你将看到如何返回一个不同于你在这里声明的默认状态码的状态码。
