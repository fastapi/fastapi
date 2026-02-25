# 表单数据 { #form-data }

当你需要接收表单字段而不是 JSON 时，可以使用 `Form`。

/// info

要使用表单，首先安装 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>。

请先创建并激活一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，然后再进行安装，例如：

```console
$ pip install python-multipart
```

///

## 导入 `Form` { #import-form }

从 `fastapi` 导入 `Form`：

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## 定义 `Form` 参数 { #define-form-parameters }

创建表单参数的方式与 `Body` 或 `Query` 相同：

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

例如，在 OAuth2 规范的一种使用方式（称为“密码流”）中，要求将 `username` 和 `password` 作为表单字段发送。

<dfn title="规范">规范</dfn> 要求这些字段必须精确命名为 `username` 和 `password`，并且作为表单字段发送，而不是 JSON。

使用 `Form` 可以像使用 `Body`（以及 `Query`、`Path`、`Cookie`）一样声明相同的配置，包括校验、示例、别名（例如将 `username` 写成 `user-name`）等。

/// info

`Form` 是直接继承自 `Body` 的类。

///

/// tip

要声明表单请求体，必须显式使用 `Form`，否则这些参数会被当作查询参数或请求体（JSON）参数。

///

## 关于 "表单字段" { #about-form-fields }

HTML 表单（`<form></form>`）向服务器发送数据时通常会对数据使用一种“特殊”的编码方式，这与 JSON 不同。

**FastAPI** 会确保从正确的位置读取这些数据，而不是从 JSON 中读取。

/// note | 技术细节

表单数据通常使用“媒体类型” `application/x-www-form-urlencoded` 进行编码。

但当表单包含文件时，会编码为 `multipart/form-data`。你将在下一章阅读如何处理文件。

如果你想了解更多关于这些编码和表单字段的信息，请参阅 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla 开发者网络">MDN</abbr> Web 文档的 <code>POST</code></a>。

///

/// warning

你可以在一个路径操作中声明多个 `Form` 参数，但不能同时再声明要接收为 JSON 的 `Body` 字段，因为此时请求体会使用 `application/x-www-form-urlencoded` 而不是 `application/json` 进行编码。

这不是 **FastAPI** 的限制，而是 HTTP 协议的一部分。

///

## 小结 { #recap }

使用 `Form` 来声明表单数据输入参数。
