# 查询参数模型

如果你有一组具有相关性的**查询参数**，你可以创建一个 **Pydantic 模型**来声明它们。

这将允许你在**多个地方**去**复用模型**，并且一次性为所有参数声明验证和元数据。😎

/// note

FastAPI 从 `0.115.0` 版本开始支持这个特性。🤓

///

## 使用 Pydantic 模型的查询参数

在一个 **Pydantic 模型**中声明你需要的**查询参数**，然后将参数声明为 `Query`：

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** 将会从请求的**查询参数**中**提取**出**每个字段**的数据，并将其提供给你定义的 Pydantic 模型。

## 查看文档

你可以在 `/docs` 页面的 UI 中查看查询参数：

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 禁止额外的查询参数

在一些特殊的使用场景中（可能不是很常见），你可能希望**限制**你要接收的查询参数。

你可以使用 Pydantic 的模型配置来 `forbid`（意为禁止 —— 译者注）任何 `extra`（意为额外的 —— 译者注）字段：

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

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

## 总结

你可以使用 **Pydantic 模型**在 **FastAPI** 中声明**查询参数**。😎

/// tip

剧透警告：你也可以使用 Pydantic 模型来声明 cookie 和 headers，但你将在本教程的后面部分阅读到这部分内容。🤫

///
