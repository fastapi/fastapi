# 响应状态码

与指定响应模型的方式相同，在以下任意*路径操作*中，可以使用 `status_code` 参数声明用于响应的 HTTP 状态码：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等……

{* ../../docs_src/response_status_code/tutorial001.py hl[6] *}

/// note | 笔记

注意，`status_code` 是（`get`、`post` 等）**装饰器**方法中的参数。与之前的参数和请求体不同，不是*路径操作函数*的参数。

///

`status_code` 参数接收表示 HTTP 状态码的数字。

/// info | 说明

`status_code` 还能接收 `IntEnum` 类型，比如 Python 的 <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>。

///

它可以：

* 在响应中返回状态码
* 在 OpenAPI 概图（及用户界面）中存档：

<img src="/img/tutorial/response-status-code/image01.png">

/// note | 笔记

某些响应状态码表示响应没有响应体（参阅下一章）。

FastAPI 可以进行识别，并生成表明无响应体的 OpenAPI 文档。

///

## 关于 HTTP 状态码

/// note | 笔记

如果已经了解 HTTP 状态码，请跳到下一章。

///

在 HTTP 协议中，发送 3 位数的数字状态码是响应的一部分。

这些状态码都具有便于识别的关联名称，但是重要的还是数字。

简言之：

* `100` 及以上的状态码用于返回**信息**。这类状态码很少直接使用。具有这些状态码的响应不能包含响应体
* **`200`** 及以上的状态码用于表示**成功**。这些状态码是最常用的
    * `200` 是默认状态代码，表示一切**正常**
    * `201` 表示**已创建**，通常在数据库中创建新记录后使用
    * `204` 是一种特殊的例子，表示**无内容**。该响应在没有为客户端返回内容时使用，因此，该响应不能包含响应体
* **`300`** 及以上的状态码用于**重定向**。具有这些状态码的响应不一定包含响应体，但 `304`**未修改**是个例外，该响应不得包含响应体
* **`400`** 及以上的状态码用于表示**客户端错误**。这些可能是第二常用的类型
    * `404`，用于**未找到**响应
    * 对于来自客户端的一般错误，可以只使用 `400`
* `500` 及以上的状态码用于表示服务器端错误。几乎永远不会直接使用这些状态码。应用代码或服务器出现问题时，会自动返回这些状态代码

/// tip | 提示

状态码及适用场景的详情，请参阅 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN 的 HTTP 状态码</abbr>文档</a>。

///

## 状态码名称快捷方式

再看下之前的例子：

{* ../../docs_src/response_status_code/tutorial001.py hl[6] *}

`201` 表示**已创建**的状态码。

但我们没有必要记住所有代码的含义。

可以使用 `fastapi.status` 中的快捷变量。

{* ../../docs_src/response_status_code/tutorial002.py hl[1,6] *}

这只是一种快捷方式，具有相同的数字代码，但它可以使用编辑器的自动补全功能：

<img src="../../../../../../img/tutorial/response-status-code/image02.png">

/// note | 技术细节

也可以使用 `from starlette import status`。

为了让开发者更方便，**FastAPI** 提供了与 `starlette.status` 完全相同的 `fastapi.status`。但它直接来自于 Starlette。

///

## 更改默认状态码

[高级用户指南](../advanced/response-change-status-code.md){.internal-link target=_blank}中，将介绍如何返回与在此声明的默认状态码不同的状态码。
