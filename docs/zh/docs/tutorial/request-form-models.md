# 表单模型 { #form-models }

你可以在 FastAPI 中使用 **Pydantic 模型**声明**表单字段**。

/// note | 注意

要使用表单，首先安装 [`python-multipart`](https://github.com/Kludex/python-multipart)。

将它添加到你的项目：

```console
$ uv add python-multipart
```

///

/// note | 注意

自 FastAPI 版本 `0.113.0` 起支持此功能。🤓

///

## 表单的 Pydantic 模型 { #pydantic-models-for-forms }

你只需声明一个 **Pydantic 模型**，其中包含你希望接收的**表单字段**，然后将参数声明为 `Form`：

{* ../../docs_src/request_form_models/tutorial001.py hl[9:11,15] *}

**FastAPI** 将从请求中的**表单数据**中**提取**出**每个字段**的数据，并提供你定义的 Pydantic 模型。

对于 [HTML 复选框](request-forms.md#boolean-form-fields)，请将布尔字段的默认值声明为 `False`。

## 检查文档 { #check-the-docs }

你可以在文档 UI 中验证它，地址为 `/docs`：

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 禁止额外的表单字段 { #forbid-extra-form-fields }

在某些特殊使用情况下（可能并不常见），你可能希望将表单字段**限制**为仅在 Pydantic 模型中声明过的字段，并**禁止**任何**额外**的字段。

/// note | 注意

自 FastAPI 版本 `0.114.0` 起支持此功能。🤓

///

你可以使用 Pydantic 的模型配置来 `forbid` 任何 `extra` 字段：

{* ../../docs_src/request_form_models/tutorial002.py hl[12] *}

如果客户端尝试发送一些额外的数据，他们将收到**错误**响应。

例如，客户端尝试发送如下表单字段：

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

他们将收到一条错误响应，表明字段 `extra` 不被允许：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## 组合表单模型 { #combine-form-models }

你可以将多个表单模型与单独的 `Form` 参数组合使用。

{* ../../docs_src/request_form_models/tutorial003.py hl[9:14,19:21] *}

客户端将 `name`、`tags` 和 `token` 作为表单字段发送。每个模型独立验证表单字段。

每个模型的 `extra` 配置都适用于所有表单字段，包括在其他参数或依赖项中声明的字段和文件。使用 `extra="forbid"` 时，该模型之外的任何字段都会被拒绝。使用 `extra="allow"` 时，这些字段会作为模型的额外数据被包含进来。

如果多个声明使用相同的表单字段名，每个声明都会验证该字段的值。请为共享字段使用兼容的类型和约束，以便 OpenAPI schema 能一致地描述它们。

## 可选表单模型 { #optional-form-models }

使用 `| None` 并将默认值设为 `None` 来声明表单模型，即可使这组字段变为可选。

{* ../../docs_src/request_form_models/tutorial005.py hl[17] *}

如果既未发送 `name` 也未发送 `age`，则 `profile` 为 `None`。如果发送了其中任意一个字段，FastAPI 就会验证模型，并要求提供这两个字段。提交空值也算作提供了字段。

使用 `| None` 但不设置默认值时，该参数仍然是必填的。

额外字段遵循模型的 `extra` 配置。被忽略的额外字段不会使模型被视为已提供。

仅包含未勾选复选框的可选模型会被省略。发送 `enabled=false` 这样的值可以显式提供该模型。

## 可选的表单模型联合类型 { #optional-unions-of-form-models }

你也可以使用可选的模型联合类型。

{* ../../docs_src/request_form_models/tutorial006.py hl[9:16,21] *}

如果未发送任何表单字段，则 `contact` 为 `None`。发送 `kind=person` 和 `name`，或发送 `kind=company` 和 `company_name`。判别器会选择要验证的模型。

## 组合表单模型联合类型 { #combine-unions-of-form-models }

你可以将联合类型与其他表单模型、单独的 `Form` 参数以及 `File` 参数组合使用。每个联合类型都会独立验证。

{* ../../docs_src/request_form_models/tutorial007.py hl[31:35] *}

在同一个表单中发送所有字段。例如，发送 `contact_type=person`、`name=Rick`、`notification_type=email`、`email=rick@example.com` 和 `token=secret`。

省略通知字段即可让 `notification` 保持为 `None`。

## 表单模型与文件 { #form-models-and-files }

你也可以将表单模型与[文件参数](request-files.md)组合使用。

{* ../../docs_src/request_form_models/tutorial004.py hl[14] *}

这里，客户端使用 `multipart/form-data` 发送 `name` 字段和 `avatar` 文件。

## 总结 { #summary }

你可以使用 Pydantic 模型在 FastAPI 中声明表单字段。😎
