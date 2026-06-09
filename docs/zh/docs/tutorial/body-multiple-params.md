# Body - 多个参数 { #body-multiple-parameters }

前面看了 `Path` 和 `Query`。现在来看更高级的请求体声明用法。

## 混用 `Path`、`Query` 和请求体参数 { #mix-path-query-and-body-parameters }

先说结论。`Path`、`Query` 和请求体参数可以随意混用。**FastAPI** 会自己分辨。

Body 参数也能是可选的。把默认值设为 `None` 就行：

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | 注意

注意，这里从请求体取出的 `item` 是可选的。因为它的默认值是 `None`。

///

## 多个请求体参数 { #multiple-body-parameters }

上个例子里，*路径操作* 期望收到一个包含 `Item` 属性的 JSON：

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

也可以声明多个请求体参数，比如 `item` 和 `user`：

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

这时函数里有不止一个请求体参数（两个都是 Pydantic 模型）。**FastAPI** 会识别出来。

它会用参数名作为请求体里的键（字段名）。期望的请求体长这样：

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

注意，`item` 的声明和之前一样。现在它需要包在请求体的 `item` 键里。

///

**FastAPI** 会把请求自动转换。`item` 和 `user` 各拿到各自的内容。

它会校验组合数据。还会按这个结构生成 OpenAPI 模式和自动文档。

## 请求体里的单个值 { #singular-values-in-body }

就像有 `Query`、`Path` 用来给查询参数和路径参数加额外信息。**FastAPI** 也提供了等价的 `Body`。

比如，在上面的模型上再加一个同级的键 `importance`，和 `item`、`user` 并列。

如果直接这么声明。因为它是单个值，**FastAPI** 会把它当成查询参数。

但你可以用 `Body` 告诉 **FastAPI** 把它当成请求体里的另一个键：

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}

这时，**FastAPI** 期望的请求体是：

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

同样会做类型转换、校验和文档生成。

## 多个请求体参数配合查询参数 { #multiple-body-params-and-query }

当然，也可以在有请求体参数时再加查询参数。

默认单个值会被当成查询参数。你不必显式用 `Query`，直接写：

```Python
q: str | None = None
```

例如：

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}

/// note | 注意

`Body` 也支持和 `Query`、`Path` 一样的额外校验和元数据参数。后面会用到。

///

## 嵌套单个请求体参数 { #embed-a-single-body-parameter }

假设你只有一个 Pydantic 模型 `Item` 的 `item` 请求体参数。

默认会直接期望模型本身作为请求体。

但如果你想让它期望一个带 `item` 键的 JSON。模型内容放在这个键里。就像有额外请求体参数时那样。可以用 `Body` 的特殊参数 `embed`：

```Python
item: Annotated[Item, Body(embed=True)]
```

例如：

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}

这时 **FastAPI** 期望的请求体是：

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

## 小结 { #recap }

即使一个请求只有一个请求体。你也能在路径操作函数里声明多个请求体参数。

**FastAPI** 会处理好这些映射。把正确的数据传给函数。并校验并在路径操作里生成正确的模式文档。

你也能把单个值声明为请求体的一部分。

只有一个参数时。也可以让 **FastAPI** 把它嵌在某个键里。
