# Header 参数模型 { #header-parameter-models }

如果您有一组相关的 **header 参数**，您可以创建一个 **Pydantic 模型**来声明它们。

这将允许您在**多个地方**能够**重用模型**，并且可以一次性声明所有参数的验证和元数据。😎

/// note | 注意

自 FastAPI 版本 `0.115.0` 起支持此功能。🤓

///

## 使用 Pydantic 模型的 Header 参数 { #header-parameters-with-a-pydantic-model }

在 **Pydantic 模型**中声明所需的 **header 参数**，然后将参数声明为 `Header` :

{* ../../docs_src/header_param_models/tutorial001.py hl[9:14,18] *}

**FastAPI** 将从请求中接收到的 **headers** 中**提取**出**每个字段**的数据，并提供您定义的 Pydantic 模型。

## 查看文档 { #check-the-docs }

您可以在文档 UI 的 `/docs` 中查看所需的 headers：

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## 禁止额外的 Headers { #forbid-extra-headers }

在某些特殊使用情况下（可能并不常见），您可能希望**限制**您想要接收的 headers。

您可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段：

{* ../../docs_src/header_param_models/tutorial002.py hl[10] *}

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

## 禁用下划线转换 { #disable-convert-underscores }

与常规的 header 参数相同，当参数名中包含下划线时，会**自动转换为连字符**。

例如，如果你的代码中有一个名为 `save_data` 的 header 参数，那么预期的 HTTP 头将是 `save-data`，并且在文档中也会以这种形式显示。

如果由于某些原因你需要禁用这种自动转换，你也可以在用于 header 参数的 Pydantic 模型中进行设置。

{* ../../docs_src/header_param_models/tutorial003.py hl[19] *}

/// warning | 警告

在将 `convert_underscores` 设为 `False` 之前，请注意某些 HTTP 代理和服务器不允许使用带下划线的 headers。

///

## 组合参数模型 { #combine-parameter-models }

你可以将多个 header 参数模型与单独的 header 参数及依赖项组合使用。每个模型都会独立提取和验证，如[查询参数模型](query-param-models.md#combine-parameter-models)中所述。

每个模型的 `extra` 配置都适用于所有 header 参数，包括在其他模型或依赖项中声明的参数。使用 `extra="forbid"` 时，不属于该模型的任何 header 都会被拒绝。使用 `extra="allow"` 时，这些 headers 会作为模型的额外字段包含在内。

每个模型在读取请求和生成 OpenAPI 时，都会使用各自的 `Header(convert_underscores=...)` 设置。显式指定的字段别名会原样用作 header 名称。

## 可选的 Header 参数模型 { #optional-header-parameter-models }

使用 `| None` 声明 header 参数模型，并将默认值设为 `None`，即可将这组参数设为可选。

{* ../../docs_src/header_param_models/tutorial004.py hl[15] *}

如果既未发送 `x-client-name` 也未发送 `x-client-version`，则 `client` 为 `None`。如果发送了其中任意一个，FastAPI 就会验证模型，并要求提供这两个字段。

默认值、额外字段和 OpenAPI 的规则与[可选的查询参数模型](query-param-models.md#optional-query-parameter-models)相同。

`Host` 等 headers 也遵循模型的 `extra` 配置。使用 `extra="allow"` 时，即使未提供任何一个已声明的字段，这些 headers 也会使模型被视为已提供。

## 总结 { #summary }

您可以使用 **Pydantic 模型**在 **FastAPI** 中声明 **headers**。😎
