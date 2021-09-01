# 响应模型

使用 `response_model` 参数，即可在*路径操作*中声明响应模型：

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 等……

```Python hl_lines="17"
{!../../../docs_src/response_model/tutorial001.py!}
```

!!! note "笔记"

    注意，`response_model` 是（`get`、`post` 等）**装饰器**方法的参数。与之前的参数和请求体不同，不是*路径操作函数*的参数。

`response_model` 接收的类型与声明 Pydantic 模型属性的类型相同，可以是 Pydantic 模型，也可以是由 Pydantic 模型的 `list`，例如 `List[Item]`。

FastAPI 使用 `response_model`：

* 转换为类型声明的输出数据
* 校验数据
* 在 OpenAPI *路径操作*中，为响应添加 JSON Schema
* 生成 API 文档

但最重要的是：

* 把输出数据限制在该模型定义内。接下来，您就会知道这一点有多重要

!!! note "技术细节"

    响应模型是在装饰器参数中声明的，而不是返回类型注释的函数，因为路径函数没有真正返回该响应模型，而是返回 `dict`、数据库对象或其它模型，然后再使用 `response_model` 执行字段约束和序列化。

## 返回相同的输入数据

在此，声明包含明文密码的 `UserIn` 模型：

```Python hl_lines="9  11"
{!../../../docs_src/response_model/tutorial002.py!}
```

使用此模型声明输入对象，并使用同一个模型声明输出对象：

```Python hl_lines="17-18"
{!../../../docs_src/response_model/tutorial002.py!}
```

现在，只要在浏览器中使用密码创建用户，API 就会在响应中返回相同的密码。

本例中，因为是用户本人发送密码，这种操作没什么问题。

但如果在其它*路径操作*中使用同一个模型，就会把用户的密码发送给每一个客户端。

!!! danger "警告"

    永远不要存储用户的明文密码，也不要在响应中发送密码。

## 添加输出模型

相对于包含明文密码的输入模型，可以创建不含明文密码的输出模型：

```Python hl_lines="9  11  16"
{!../../../docs_src/response_model/tutorial003.py!}
```

这样，即便*路径操作函数*返回同样的输入用户：

```Python hl_lines="24"
{!../../../docs_src/response_model/tutorial003.py!}
```

……但因为`response_model` 中声明的 `UserOut` 模型没有包含密码：

```Python hl_lines="22"
{!../../../docs_src/response_model/tutorial003.py!}
```

因此，**FastAPI** 会（使用 Pydantic）过滤掉所有未在输出模型中声明的数据。

## 查看文档

在 API 文档中，可以看到输入模型和输出模型都有自己的 JSON Schema：

<img src="/img/tutorial/response-model/image01.png">

并且，API 文档可以使用这两个模型：

<img src="/img/tutorial/response-model/image02.png">

## 响应模型编码参数

响应模型支持默认值，例如：

```Python hl_lines="11  13-14"
{!../../../docs_src/response_model/tutorial004.py!}
```

* `description: Optional[str] = None` 的默认值是 `None`
* `tax: float = 10.5` 的默认值是 `10.5`
* `tags: List[str] = []` 的默认值是空列表： `[]`

但如果没有为含默认值的属性另赋新值，输出结果会省略含默认值的属性。

例如，NoSQL 数据库的模型中往往包含很多可选属性，如果输出含默认值的属性，输出的 JSON 响应会特别长，此时，可以省略只含默认值的属性。

### 使用 `response_model_exclude_unset` 参数

把*路径操作装饰器*的参数设置为 `response_model_exclude_unset=True`：

```Python hl_lines="24"
{!../../../docs_src/response_model/tutorial004.py!}
```

响应中就不会再包含未修改过默认值的属性，而是只包含设置过值的属性。

因此，向*路径操作*发送 ID 为 `foo` 的商品的请求，则（不包括默认值的）响应为：

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

!!! info "说明"

    FastAPI 使用 Pydantic 模型中 `.dict()` 的 <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank"> `exclude_unset` 参数</a> 实现此功能。

!!! info "说明"

    还可以使用：
    
    * `response_model_exclude_defaults=True`
    * `response_model_exclude_none=True`
    
    参阅 <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank">Pydantic 文档</a>中 `exclude_defaults` 和 `exclude_none` 的说明。

#### 默认值字段有实际值的数据

但如果为含默认值的模型字段赋予了新值，例如 ID 为 `bar` 的项：

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

这些值就会包含在返回的响应中。

#### 与默认值相同的数据

如果新的数据与默认值相同，例如 ID 为 `baz` 的项：

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

虽然 FastAPI （其实是 Pydantic）能够识别出 `description`、`tax` 和 `tags` 的值与默认值相同，这些值也会显式设置（而不是取自默认值）。

因此，这些值会包含在 JSON 响应里。

!!! tip "提示"

    注意，默认值可以是任何对象，不只是 None。
    
    还可以是列表 (`[]`)、`float`（10.5）等。

### `response_model_include` 和 `response_model_exclude`

路径操作装饰器参数还有 `response_model_include` 和 `response_model_exclude`。

这两个参数的值是由属性名 `str` 组成的 `set`，用于包含（忽略其它属性）或排除（包含其它属性）集合中的属性名。

如果只有一个 Pydantic 模型，但又想从中移除某些输出数据，则可以使用这种快捷方法。

!!! tip "提示"

    但我们依然建议使用多个类，而不是这些参数。
    
    因为就算使用 `response_model_include` 或 `response_model_exclude` 省略属性，但在 OpenAPI 生成的 JSON Schema （及文档）中仍会显示完整的模型。
    
    这种操作也适用于类似的 `response_model_by_alias`。

```Python hl_lines="31  37"
{!../../../docs_src/response_model/tutorial005.py!}
```

!!! tip "提示"

    `{"name", "description"}` 语法用于创建包含这两个值的 `set`。
    
    等效于 `set(["name", "description"])`。

#### 用 `list` 代替 `set`

不使用 `set`，而是使用 `list` 或 `tuple`，FastAPI 可以将其转换为 `set`，并仍能正常运行：

```Python hl_lines="31  37"
{!../../../docs_src/response_model/tutorial006.py!}
```

## 小结

使用*路径操作装饰器*的参数 `response_model` 定义响应模型，可以过滤数据，特别适合用来保护隐私数据。

如需只返回显式设置过的值，可以使用 `response_model_exclude_unset` 参数。
