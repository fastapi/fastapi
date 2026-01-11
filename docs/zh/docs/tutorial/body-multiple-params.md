# Body - 多个参数 { #body-multiple-parameters }

既然我们已经了解了如何使用 `Path` 和 `Query`，下面让我们来看看请求体声明的更高级用法。

## 混合使用 `Path`、`Query` 和请求体参数 { #mix-path-query-and-body-parameters }

首先，当然，你可以自由混合使用 `Path`、`Query` 和请求体参数声明，**FastAPI** 会知道该怎么做。

你还可以通过将默认值设置为 `None`，把请求体参数声明为可选参数：

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | 注意

请注意，在这种情况下，将从请求体中获取的 `item` 是可选的，因为它的默认值为 `None`。

///

## 多个请求体参数 { #multiple-body-parameters }

在上一个示例中，*路径操作*会期望一个 JSON 请求体，其中包含 `Item` 的属性，例如：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

但你也可以声明多个请求体参数，例如 `item` 和 `user`：

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}


在这种情况下，**FastAPI** 会注意到该函数中有多个请求体参数（有两个参数是 Pydantic 模型）。

因此，它会使用参数名作为请求体中的键（字段名），并期望一个类似于下面这样的请求体：

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | 注意

请注意，即使 `item` 的声明方式与之前相同，但现在它被期望位于请求体中，并在键 `item` 之下。

///

**FastAPI** 会从请求中自动完成转换，使得参数 `item` 接收到它对应的内容，`user` 也是一样。

它会对复合数据执行校验，并将其以这种方式记录到 OpenAPI schema 和自动化文档中。

## 请求体中的单一值 { #singular-values-in-body }

就像有 `Query` 和 `Path` 用于为查询参数和路径参数定义额外数据一样，**FastAPI** 提供了等价的 `Body`。

例如，扩展前面的模型，你可能决定除了 `item` 和 `user` 之外，还想在同一个请求体中增加另一个键 `importance`。

如果你按原样声明它，因为它是单一值，**FastAPI** 会认为它是一个查询参数。

但你可以使用 `Body` 指示 **FastAPI** 将它作为另一个请求体键来处理：

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}


在这种情况下，**FastAPI** 会期望一个类似于下面这样的请求体：

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

同样，它会转换数据类型、校验、生成文档等。

## 多个请求体参数和查询参数 { #multiple-body-params-and-query }

当然，除了任何请求体参数之外，你也可以在需要时声明额外的查询参数。

由于默认情况下单一值会被解释为查询参数，你不必显式添加 `Query`，你可以直接这样写：

```Python
q: Union[str, None] = None
```

或者在 Python 3.10 及以上版本：

```Python
q: str | None = None
```

例如：

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}


/// info | 信息

`Body` 也具备与 `Query`、`Path` 以及你后面会看到的其他类相同的额外校验与元数据参数。

///

## 嵌入单个请求体参数 { #embed-a-single-body-parameter }

假设你只有一个来自 Pydantic 模型 `Item` 的请求体参数 `item`。

默认情况下，**FastAPI** 会直接期望请求体本身。

但如果你希望它期望一个 JSON，包含键 `item`，并在其中放入模型内容（就像你声明额外请求体参数时那样），你可以使用特殊的 `Body` 参数 `embed`：

```Python
item: Item = Body(embed=True)
```

例如：

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}


在这种情况下，**FastAPI** 会期望一个类似于下面这样的请求体：

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

而不是：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## 总结 { #recap }

你可以在你的*路径操作函数*中添加多个请求体参数，即使一个请求只能有一个请求体。

但 **FastAPI** 会处理它，在你的函数中提供正确的数据，并在*路径操作*中校验并记录正确的 schema。

你还可以声明要作为请求体一部分接收的单一值。

并且即使只声明了一个参数，你也可以指示 **FastAPI** 将请求体嵌入到某个键中。
