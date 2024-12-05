# Header 参数模型

如果您有一组相关的 **header 参数**，您可以创建一个 **Pydantic 模型**来声明它们。

这将允许您在**多个地方**能够**重用模型**，并且可以一次性声明所有参数的验证和元数据。😎

/// note

自 FastAPI 版本 `0.115.0` 起支持此功能。🤓

///

## 使用 Pydantic 模型的 Header 参数

在 **Pydantic 模型**中声明所需的 **header 参数**，然后将参数声明为 `Header` :

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** 将从请求中接收到的 **headers** 中**提取**出**每个字段**的数据，并提供您定义的 Pydantic 模型。

## 查看文档

您可以在文档 UI 的 `/docs` 中查看所需的 headers：

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## 禁止额外的 Headers

在某些特殊使用情况下（可能并不常见），您可能希望**限制**您想要接收的 headers。

您可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段：

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

如果客户尝试发送一些**额外的 headers**，他们将收到**错误**响应。

例如，如果客户端尝试发送一个值为 `plumbus` 的 `tool` header，客户端将收到一个**错误**响应，告知他们 header 参数 `tool` 是不允许的：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## 总结

您可以使用 **Pydantic 模型**在 **FastAPI** 中声明 **headers**。😎
