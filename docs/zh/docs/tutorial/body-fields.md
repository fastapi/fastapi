# 请求体 - 字段 { #body-fields }

与在*路径操作函数*参数中使用 `Query`、`Path` 和 `Body` 声明额外的校验与元数据的方式一样，你也可以在 Pydantic 模型内部使用 Pydantic 的 `Field` 来声明校验和元数据。

## 导入 `Field` { #import-field }

首先，你必须导入它：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}


/// warning | 警告

注意，`Field` 是直接从 `pydantic` 导入的，而不是像其他所有（`Query`、`Path`、`Body` 等）那样从 `fastapi` 导入。

///

## 声明模型属性 { #declare-model-attributes }

然后，你可以在模型属性中使用 `Field`：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` 的工作方式和 `Query`、`Path`、`Body` 一样，它也有完全相同的参数等。

/// note | 技术细节

实际上，`Query`、`Path` 以及你接下来会看到的其他对象，会创建一个共同的 `Param` 类的子类对象，而 `Param` 类本身又是 Pydantic 的 `FieldInfo` 类的子类。

而 Pydantic 的 `Field` 也会返回一个 `FieldInfo` 的实例。

`Body` 也会直接返回 `FieldInfo` 的子类对象。并且你之后还会看到一些是 `Body` 类子类的其他对象。

记住：当你从 `fastapi` 导入 `Query`、`Path` 等对象时，它们实际上是返回特殊类的函数。

///

/// tip | 提示

注意，每个模型属性（包含类型、默认值和 `Field`）都与*路径操作函数*参数的结构相同，只是用 `Field` 替代了 `Path`、`Query` 和 `Body`。

///

## 添加额外信息 { #add-extra-information }

你可以在 `Field`、`Query`、`Body` 等中声明额外信息，并且它会包含在生成的 JSON Schema 中。

在文档后续学习声明示例时，你会学到更多关于添加额外信息的内容。

/// warning | 警告

传递给 `Field` 的额外键也会出现在你的应用生成的 OpenAPI schema 中。
由于这些键不一定属于 OpenAPI 规范的一部分，一些 OpenAPI 工具（例如 [OpenAPI validator](https://validator.swagger.io/)）可能无法处理你生成的 schema。

///

## 小结 { #recap }

你可以使用 Pydantic 的 `Field` 为模型属性声明额外的校验和元数据。

你也可以使用额外的关键字参数来传递更多 JSON Schema 元数据。
