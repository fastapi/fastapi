# 请求体 - 更新数据 { #body-updates }

## 用 `PUT` 替换式更新 { #update-replacing-with-put }

更新数据可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> 操作。

把输入数据转换为以 JSON 格式存储的数据（比如，使用 NoSQL 数据库时），可以使用 `jsonable_encoder`。例如，把 `datetime` 转换为 `str`。

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` 用于接收替换现有数据的数据。

### 关于替换的警告 { #warning-about-replacing }

用 `PUT` 把数据项 `bar` 更新为以下请求体时：

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

因为其中未包含已存储的属性 `"tax": 20.2`，输入模型会取 `"tax": 10.5` 的默认值。

因此，保存的数据会带有这个“新的” `tax` 值 `10.5`。

## 用 `PATCH` 进行部分更新 { #partial-updates-with-patch }

也可以使用 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> 操作对数据进行*部分*更新。

也就是说，你只需发送想要更新的数据，其余数据保持不变。

/// note | 注意

`PATCH` 没有 `PUT` 知名，也没那么常用。

很多团队甚至只用 `PUT` 实现部分更新。

你可以**随意**选择如何使用它们，**FastAPI** 不做任何限制。

但本指南会大致展示它们的预期用法。

///

### 使用 Pydantic 的 `exclude_unset` 参数 { #using-pydantics-exclude-unset-parameter }

如果要接收部分更新，建议在 Pydantic 模型的 `.model_dump()` 中使用 `exclude_unset` 参数。

比如，`item.model_dump(exclude_unset=True)`。

这会生成一个 `dict`，只包含创建 `item` 模型时显式设置的数据，不包含默认值。

然后再用它生成一个只含已设置（在请求中发送）数据、且省略默认值的 `dict`：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### 使用 Pydantic 的 `update` 参数 { #using-pydantics-update-parameter }

接下来，用 `.model_copy()` 为已有模型创建副本，并传入 `update` 参数，值为包含更新数据的 `dict`。

例如，`stored_item_model.model_copy(update=update_data)`：

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### 部分更新小结 { #partial-updates-recap }

简而言之，应用部分更新应当：

* （可选）使用 `PATCH` 而不是 `PUT`。
* 提取已存储的数据。
* 把该数据放入 Pydantic 模型。
* 生成不含输入模型默认值的 `dict`（使用 `exclude_unset`）。
    * 这样只会更新用户实际设置的值，而不会用模型中的默认值覆盖已存储的值。
* 为已存储的模型创建副本，用接收到的部分更新数据更新其属性（使用 `update` 参数）。
* 把模型副本转换为可存入数据库的形式（比如，使用 `jsonable_encoder`）。
    * 这类似于再次调用模型的 `.model_dump()` 方法，但会确保（并转换）值为可转换为 JSON 的数据类型，例如把 `datetime` 转换为 `str`。
* 把数据保存至数据库。
* 返回更新后的模型。

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | 提示

实际上，HTTP `PUT` 也可以使用同样的技巧。

但这里用 `PATCH` 举例，因为它就是为这种用例设计的。

///

/// note | 注意

注意，输入模型仍会被验证。

因此，如果希望接收的部分更新可以省略所有属性，则需要一个所有属性都标记为可选（带默认值或 `None`）的模型。

为了区分用于**更新**（全部可选）和用于**创建**（必填）的模型，可以参考[更多模型](extra-models.md){.internal-link target=_blank} 中介绍的思路。

///
