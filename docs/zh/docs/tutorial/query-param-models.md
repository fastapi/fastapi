# 查询参数模型 { #query-parameter-models }

如果你有一组具有相关性的**查询参数**，你可以创建一个 **Pydantic 模型**来声明它们。

这将允许你在**多个地方**去**复用模型**，并且一次性为所有参数声明验证和元数据。😎

/// note | 注意

FastAPI 从 `0.115.0` 版本开始支持这个特性。🤓

///

## 使用 Pydantic 模型的查询参数 { #query-parameters-with-a-pydantic-model }

在一个 **Pydantic 模型**中声明你需要的**查询参数**，然后将参数声明为 `Query`：

{* ../../docs_src/query_param_models/tutorial001.py hl[9:13,17] *}

**FastAPI** 将会从请求的**查询参数**中**提取**出**每个字段**的数据，并将你定义的 Pydantic 模型提供给你。

## 查看文档 { #check-the-docs }

你可以在 `/docs` 页面的 UI 中查看查询参数：

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 禁止额外的查询参数 { #forbid-extra-query-parameters }

在一些特殊的使用场景中（可能不是很常见），你可能希望**限制**你要接收的查询参数。

你可以使用 Pydantic 的模型配置来 `forbid` 任何 `extra` 字段：

{* ../../docs_src/query_param_models/tutorial002.py hl[10] *}

假设有一个客户端尝试在**查询参数**中发送一些**额外的**数据，它将会收到一个**错误**响应。

例如，如果客户端尝试发送一个值为 `plumbus` 的 `tool` 查询参数，如：

```http
https://example.com/items/?limit=10&tool=plumbus
```

他们将收到一个**错误**响应，告诉他们查询参数 `tool` 是不允许的：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## 组合参数模型 { #combine-parameter-models }

你可以声明多个查询参数模型，并将它们与单独的查询参数或依赖项组合使用。

{* ../../docs_src/query_param_models/tutorial003.py hl[9:15,20:22] *}

请求参数仍处于同一层级。

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

查询字符串中没有 `pagination` 或 `filters` 键。每个模型都使用自己的默认值、字段验证器和模型验证器独立验证查询参数。在依赖项中声明模型或单独的参数时也是如此。

如果模型共享参数名或别名，每个模型都会独立验证该请求参数。对于相互独立的值，请使用不同的名称或别名。OpenAPI 只会列出共享参数一次，就像处理与依赖项共享的参数一样，因此共享参数的声明应描述相同的类型和约束。

每个模型的 `extra` 配置都适用于所有查询参数，包括在其他模型或依赖项中声明的参数。使用 `extra="forbid"` 时，该模型之外的任何参数都会被拒绝。使用 `extra="allow"` 时，这些参数会作为模型的额外数据被包含在内。

这同样适用于 `Header` 和 `Cookie` 模型。

## 可选查询参数模型 { #optional-query-parameter-models }

声明查询参数模型时，使用 `| None` 并将默认值设为 `None`，即可使这组参数变为可选。

{* ../../docs_src/query_param_models/tutorial004.py hl[18] *}

如果既未发送 `start` 也未发送 `end`，则 `date_range` 为 `None`。如果发送了其中任意一个，FastAPI 就会验证模型，并要求提供两个字段。

使用 `| None` 但不设置默认值时，该参数仍然是必需的。

额外参数遵循模型的 `extra` 配置。被忽略的额外参数不会使模型被视为已提供。

OpenAPI 会逐一列出这组参数的字段，并将它们标记为可选。

你也可以声明可选的 [header 参数模型](header-param-models.md#optional-header-parameter-models)和 [cookie 参数模型](cookie-param-models.md#optional-cookie-parameter-models)。

## 总结 { #summary }

你可以使用 **Pydantic 模型**在 **FastAPI** 中声明**查询参数**。😎

/// tip | 提示

剧透警告：你也可以使用 Pydantic 模型来声明 cookie 和 headers，但你将在本教程的后面部分阅读到这部分内容。🤫

///
