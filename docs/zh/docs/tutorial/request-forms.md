# 表单数据

当您需要接收表单字段而不是JSON时，可以使用 `Form`。

!!! info
    为了使用表单，首先要安装 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

    如 `pip install python-multipart`.

## 导入 `Form`

从 `fastapi` 导入 `Form` :

```Python hl_lines="1"
{!../../../docs_src/request_forms/tutorial001.py!}
```

## Define `Form` parameters

Create form parameters the same way you would for `Body` or `Query`:

```Python hl_lines="7"
{!../../../docs_src/request_forms/tutorial001.py!}
```

例如，在使用OAuth2规范的一种方式(称为 "密码流" )中，需要将 `username` 和 `password` 作为表单字段发送。

<abbr title="specification">规范</abbr> 要求字段精确命名为 `username` 和 `password`，并以表单字段的形式发送，而不是JSON。

使用 `Form` 可以声明与 `Body` (以及`Query`, `Path`, `Cookie`)相同的元数据和验证。

!!! info
    `Form` 是一个直接继承自 `Body` 的类.

!!! tip
    要声明表单主体，您需要显式地使用`Form` ，因为如果没有它，参数将被解释为查询参数或主体(JSON)参数。

## 关于 "表单字段"

HTML表单向服务器发送数据的方式通常使用该数据的 "特殊" 编码，这与JSON不同。

**FastAPI** 将确保从正确的位置读取数据，而不是JSON。

!!! note "技术细节"
    表单中的数据通常使用 "媒体类型" 进行编码 `application/x-www-form-urlencoded`.

    但是当表单包含文件时，它被编码为 `multipart/form-data` 。你将在下一章读到如何处理文件。
    
    如果您想了解更多关于这些编码和表单字段的信息，请访问 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> 网络文档的 <code>POST</code></a>部分。

!!! warning
    你可以在一个 *路径操作* 中声明多个 `Form` 参数，但你不能同时声明 `Body` 字段，以希望收到内容是JSON格式，因为请求体将使用 `application/x-www-form-urlencoded` 编码而不是 `application/json` 。

    这不是 **FastAPI** 的限制，而是HTTP协议的一部分.

## 回顾

使用 `Form` 声明表单数据输入参数。
