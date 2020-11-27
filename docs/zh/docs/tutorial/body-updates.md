# 请求体 - 更新

## 更新替换为 `PUT`

要更新一个项目，您可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> 操作。

你可以使用 `jsonable_encoder` 来将输入数据转换成可以存储为 JSON 的数据 (例如，使用NoSQL数据库). 例如，将 `datetime` 转换为 `str` 。

```Python hl_lines="30-35"
{!../../../docs_src/body_updates/tutorial001.py!}
```

`PUT` 用于接收应该替换现有数据的数据。

### 替换有关的警告

这意味着，如果你想使用 `PUT` 更新项目 `bar` 为以下内容：

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

因为它没有包含已经存储的属性 `"tax": 20.2`, 所以输入模型将带有默认值 `"tax": 10.5`.

这些数据将保存 `tax` 为 "新"的值 `10.5`。

## 使用 `PATCH` 进行部分更新

你也可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> 操作进行 *部分* 更新数据。

这意味着您只能发送您想要更新的数据，而其余数据保持不变。

!!! Note
    `PATCH` 比 `PUT` 更少被使用和熟知。

    许多团队只使用 `PUT`，甚至用于部分更新。

    您可以 **随心所欲** 地使用它们， **FastAPI** 没有任何限制。

    但本指南或多或少地向您展示了它们的用途。

### 使用 Pydantic 的 `exclude_unset` 参数

如果您想接收部分更新，在Pydantic模型的 `.dict()` 中使用参数 `exclude_unset` 将会十分有用。

就像 `item.dict(exclude_unset=True)`.

这将生成一个 `dict` 其中只包含创建 `item` 模型时设置的数据，不包括默认值。

然后，你可以使用这个生成一个 `dict` 只有被设置的数据(在请求中发送的)，省略默认值:

```Python hl_lines="34"
{!../../../docs_src/body_updates/tutorial002.py!}
```

### 使用 Pydantic 的 `update` 参数

现在，你可以通过使用 `.copy()` 创建已存在模型的一个副本，同时可以传递包含需要更新的数据 `dict` 给 `update` 参数。

就像 `stored_item_model.copy(update=update_data)`:

```Python hl_lines="35"
{!../../../docs_src/body_updates/tutorial002.py!}
```

### 部分更新回顾

总而言之，要应用部分更新，你需要:

* (可选的) 使用 `PATCH` 而不是 `PUT` 。
* 检索存储的数据。
* 把数据放在一个 Pydantic 模型中。
* 从输入模型中生成一个没有默认值的 `dict` (使用 `exclude_unset` )。
    * 这样你可以只更新用户实际设置的值，而不是覆盖模型中已经存储的默认值。
* 创建一个已存储模型的副本，用接收到的部分更新更新它的属性 (使用 `update` 参数)。
* 将复制的模型转换为可以存储在数据库中的东西 (例如，使用 `jsonable_encoder` )。
    * 这类似于使用模型的 `.dict()` 方法，但它确保(和转换)值的数据类型可以转换为JSON，例如， `datetime` 转换为 `str` 。
* 保存数据到您的数据库。
* 返回更新的模型。

```Python hl_lines="30-37"
{!../../../docs_src/body_updates/tutorial002.py!}
```

!!! tip
    实际上，您可以对 HTTP `PUT` 操作使用相同的技术。

    但是这里的示例使用 `PATCH` ，因为它是为这些用例创建的。

!!! note
    注意，输入模型仍然是经过验证的。

    因此，如果您希望接收可以省略所有属性的部分更新，则需要将所有属性标记为可选(使用默认值或 `None`)的模型。

    为了将用于 **updates** 的包含所有可选值的模型与用于**creation** 的包含所有必要值的模型进行区分，你可以使用在[Extra Models](extra-models.md){.internal-link target=_blank} 中描述的思路。
