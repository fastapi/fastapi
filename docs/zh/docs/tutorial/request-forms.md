# 表单数据

接收的不是 JSON，而是表单字段时，要使用 `Form`。

!!! info "说明"

    要使用表单，需预先安装 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>。
    
    例如，`pip install python-multipart`。

## 导入 `Form`

从 `fastapi` 导入 `Form`：

```Python hl_lines="1"
{!../../../docs_src/request_forms/tutorial001.py!}
```

## 定义 `Form` 参数

创建表单（`Form`）参数的方式与 `Body` 和 `Query` 一样：

```Python hl_lines="7"
{!../../../docs_src/request_forms/tutorial001.py!}
```

例如，OAuth2 规范的 "密码流" 模式规定要通过表单字段发送 `username` 和 `password`。

<abbr title="specification">该规范</abbr>要求字段必须命名为 `username` 和 `password`，并通过表单字段发送，不能用 JSON。

使用 `Form` 可以声明与 `Body` （及 `Query`、`Path`、`Cookie`）相同的元数据和验证。

!!! info "说明"

    `Form` 是直接继承自 `Body` 的类。

!!! tip "提示"

    声明表单体要显式使用 `Form` ，否则，FastAPI 会把该参数当作查询参数或请求体（JSON）参数。

## 关于 "表单字段"

与 JSON 不同，HTML 表单（`<form></form>`）向服务器发送数据通常使用「特殊」的编码。

**FastAPI** 要确保从正确的位置读取数据，而不是读取 JSON。

!!! note "技术细节"

    表单数据的「媒体类型」编码一般为 `application/x-www-form-urlencoded`。
    
    但包含文件的表单编码为 `multipart/form-data`。文件处理详见下节。
    
    编码和表单字段详见 <a href="https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> Web 文档的 <code>POST</code></a>小节。

!!! warning "警告"

    可在一个*路径操作*中声明多个 `Form` 参数，但不能同时声明要接收 JSON 的 `Body` 字段。因为此时请求体的编码是 `application/x-www-form-urlencoded`，不是 `application/json`。
    
    这不是 **FastAPI** 的问题，而是 HTTP 协议的规定。

## 小结

本节介绍了如何使用 `Form` 声明表单数据输入参数。