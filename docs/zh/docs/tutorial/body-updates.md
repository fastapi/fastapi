# 请求体 - 更新数据 { #body-updates }

## 用 `PUT` 替换更新 { #update-replacing-with-put }

要更新一个条目，你可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> 操作。

你可以使用 `jsonable_encoder` 将输入数据转换为可作为 JSON 存储的数据（例如在使用 NoSQL 数据库时）。例如，将 `datetime` 转换为 `str`。

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` 用于接收应该替换现有数据的数据。

### 关于替换更新的警告 { #warning-about-replacing }

这意味着，如果你想用 `PUT` 更新条目 `bar`，请求体包含：

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

因为其中不包含已存储的属性 `"tax": 20.2`，输入模型会采用 `"tax": 10.5` 的默认值。

并且数据会以这个“新”的 `tax` 值 `10.5` 保存。

## 用 `PATCH` 进行部分更新 { #partial-updates-with-patch }

你也可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> 操作来*部分*更新数据。

这意味着你可以只发送你想更新的数据，其余部分保持不变。

/// note | 注意

`PATCH` 不如 `PUT` 常用和知名。

并且很多团队即使是部分更新也只使用 `PUT`。

你可以**自由**地按你的需要使用它们，**FastAPI** 不施加任何限制。

但本指南会或多或少地展示它们按设计意图应该如何使用。

///

### 使用 Pydantic 的 `exclude_unset` 参数 { #using-pydantics-exclude-unset-parameter }

如果你想接收部分更新，在 Pydantic 模型的 `.model_dump()` 中使用参数 `exclude_unset` 非常有用。

例如 `item.model_dump(exclude_unset=True)`。

这会生成一个 `dict`，其中只包含创建 `item` 模型时设置过的数据，排除默认值。

然后你可以用它生成一个 `dict`，只包含已设置的数据（在请求中发送的数据），省略默认值：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### 使用 Pydantic 的 `update` 参数 { #using-pydantics-update-parameter }

现在，你可以使用 `.model_copy()` 创建现有模型的副本，并传入 `update` 参数，其值为包含要更新数据的 `dict`。

例如 `stored_item_model.model_copy(update=update_data)`：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### 部分更新小结 { #partial-updates-recap }

总结一下，要应用部分更新，你需要：

* （可选）使用 `PATCH` 而不是 `PUT`。
* 获取已存储的数据。
* 将这些数据放入一个 Pydantic 模型。
* 从输入模型生成一个不包含默认值的 `dict`（使用 `exclude_unset`）。
    * 这样你就可以只更新用户实际设置的值，而不是用模型中的默认值覆盖已存储的值。
* 创建存储模型的副本，用接收到的部分更新来更新其属性（使用 `update` 参数）。
* 将复制的模型转换为可存入 DB 的形式（例如使用 `jsonable_encoder`）。
    * 这类似于再次使用模型的 `.model_dump()` 方法，但它会确保（并转换）这些值是可转换为 JSON 的数据类型，例如将 `datetime` 转换为 `str`。
* 将数据保存到 DB。
* 返回更新后的模型。

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | 提示

实际上，你也可以在 HTTP `PUT` 操作中使用同样的技术。

但这里的示例使用了 `PATCH`，因为它就是为这些用例创建的。

///

/// note | 注意

注意，输入模型仍然会被校验。

所以，如果你希望接收的部分更新可以省略所有属性，你需要一个将所有属性都标记为可选的模型（带默认值或 `None`）。

为了区分用于**更新**的全可选值模型与用于**创建**的包含必填值模型，你可以使用 [更多模型](extra-models.md){.internal-link target=_blank} 中描述的思路。

///
