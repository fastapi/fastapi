# 请求体 - 多个参数

至此，我们已经学习了如何使用 `Path` 和 `Query`，接下来，继续学习声明请求体的高级用法。

## 混用 `Path`、`Query` 和请求体参数

首先，声明中可以随意混用 `Path`、`Query` 和请求体参数，**FastAPI** 知道该如何处理。

默认值为 `None` 时，请求体参数是可选的：

```Python hl_lines="19-21"
{!../../../docs_src/body_multiple_params/tutorial001.py!}
```

!!! note "笔记"

    注意，本例中，从请求体获取的 `item` 是可选的，因为它的默认值是 `None`。

## 多个请求体参数

上例中，*路径操作*预期 JSON 请求体中的 `Item` 包含如下属性：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

但，也可以声明多个请求体参数，例如 `item` 和 `user`：

```Python hl_lines="22"
{!../../../docs_src/body_multiple_params/tutorial002.py!}
```

本例中，**FastAPI** 注意到函数中有多个请求体参数（两个 Pydantic 模型参数）。

因此，它使用参数名作为请求体中的键（字段名称），并预期如下请求体：

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

!!! note "笔记"

    注意，即使 `item` 的声明方式与之前相同，但现在它被嵌入到请求体的 `item` 键内。

**FastAPI** 会自动转换请求中的数据，因此 `item` 参数将接收指定的内容，`user` 参数也是如此。

FastAPI 不仅会校验复合数据，还会在 OpenAPI 概图和自动文档显示。

## 请求体中的单值

除了可以为查询参数与路径参数定义更多数据的 `Query` 和 `Path` 之外，**FastAPI** 还提供了等效的 `Body`。

接下来，扩展之前的模型。例如，添加 `item` 和 `user` 后，还要在同一请求体中，添加另一个键 `importance`。

直接声明该参数时，因为 `importance` 是单值，**FastAPI** 会把它识别为查询参数。

此时，使用 `Body` 可以让 **FastAPI** 把它视作请求体的键。


```Python hl_lines="23"
{!../../../docs_src/body_multiple_params/tutorial003.py!}
```

此时，**FastAPI** 预期如下请求体：


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

同样，FastAPI 会执行转换数据类型、校验、生成文档等操作。

## 多个请求体参数和查询参数

当然，除了请求体参数外，还可以声明更多查询参数。

默认情况下，单值会被解释为查询参数，因此不必显式添加 `Query`，只用以下代码就可以：

```Python
q: str = None
```

示例代码如下：

```Python hl_lines="27"
{!../../../docs_src/body_multiple_params/tutorial004.py!}
```

!!! info "说明"

    `Body` 也支持与 `Query`、`Path` 相同的校验和元数据参数。


## 嵌入单个请求体参数

假设只有一个使用 Pydantic 模型 `Item` 的请求体参数 `item`。

默认情况下，**FastAPI** 会直接调用请求体。

但是，如果希望 JSON 中包含 `item` 键，且模型内容都在该键之下，就要参照声明更多请求体参数的方式，使用 `Body` 的 `embed`参数：

```Python
item: Item = Body(..., embed=True)
```

代码如下：

```Python hl_lines="17"
{!../../../docs_src/body_multiple_params/tutorial005.py!}
```

本例中，**FastAPI** 预期如下请求体：

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

## 小结

即使一个请求只能有一个请求体，仍可以为*路径操作函数*添加多个请求体参数。

**FastAPI** 会进行处理，为函数提供并校验正确的数据，并在交互文档中显示正确的*路径操作*概图。

请求体还可以接收多个单值。

只声明单个请求体参数时，**FastAPI** 也可以把请求体嵌入到键里。

