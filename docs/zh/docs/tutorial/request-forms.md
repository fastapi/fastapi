# 表单数据 { #form-data }

接收的不是 JSON，而是表单字段时，要使用 `Form`。

/// info | 信息

要使用表单，需先安装 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后再安装它，例如：

```console
$ pip install python-multipart
```

///

## 导入 `Form` { #import-form }

从 `fastapi` 导入 `Form`：

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[3] *}

## 定义 `Form` 参数 { #define-form-parameters }

创建表单参数的方式与 `Body` 或 `Query` 一样：

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[9] *}

例如，在 OAuth2 规范的一种用法（称为“密码流”）中，要求通过表单字段发送 `username` 和 `password`。

<abbr title="specification">该规范</abbr>要求字段必须精确命名为 `username` 和 `password`，并通过表单字段发送，不能用 JSON。

使用 `Form` 可以声明与 `Body`（以及 `Query`、`Path`、`Cookie`）相同的配置，包括验证、示例、别名（例如用 `user-name` 替代 `username`）等。

/// info | 信息

`Form` 是直接继承自 `Body` 的类。

///

/// tip | 提示

声明表单体要显式使用 `Form`，否则参数会被解释为查询参数或请求体（JSON）参数。

///

## 关于“表单字段” { #about-form-fields }

与 JSON 不同，HTML 表单（`<form></form>`）向服务器发送数据通常使用「特殊」的编码。

**FastAPI** 会确保从正确的位置读取数据，而不是读取 JSON。

/// note | 技术细节

表单数据的「媒体类型」编码一般为 `application/x-www-form-urlencoded`。

但包含文件的表单编码为 `multipart/form-data`。你将在下一章了解如何处理文件。

如需进一步了解这些编码和表单字段，请参阅 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> Web 文档的 <code>POST</code></a>。

///

/// warning | 警告

可在一个*路径操作*中声明多个 `Form` 参数，但不能同时声明要接收 JSON 的 `Body` 字段，因为此时请求体的编码是 `application/x-www-form-urlencoded`，不是 `application/json`。

这不是 **FastAPI** 的限制，而是 HTTP 协议的一部分。

///

## 小结 { #recap }

使用 `Form` 声明表单数据输入参数。
