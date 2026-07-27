# 请求体 - 字段 { #body-fields }

与在*路径操作函数*中使用 `Query`、`Path` 、`Body` 声明校验与元数据的方式一样，可以使用 Pydantic 的 `Field` 在 Pydantic 模型内部声明校验和元数据。

## 导入 `Field` { #import-field }

首先，从 Pydantic 中导入 `Field`：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}

/// warning | 警告

注意，与从 `fastapi` 导入 `Query`，`Path`、`Body` 不同，要直接从 `pydantic` 导入 `Field` 。

///

## 声明模型属性 { #declare-model-attributes }

然后，使用 `Field` 定义模型的属性：

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` 的工作方式和 `Query`、`Path`、`Body` 相同，参数也相同。

/// note | 技术细节

实际上，`Query`、`Path` 以及你接下来会看到的其它对象，会创建公共 `Param` 类的子类的对象，而 `Param` 本身是 Pydantic 中 `FieldInfo` 的子类。

Pydantic 的 `Field` 返回也是 `FieldInfo` 的类实例。

`Body` 直接返回的也是 `FieldInfo` 的子类的对象。后文还会介绍一些 `Body` 的子类。

注意，从 `fastapi` 导入的 `Query`、`Path` 等对象实际上都是返回特殊类的函数。

///

/// tip | 提示

注意，模型属性的类型、默认值及 `Field` 的代码结构与*路径操作函数*的参数相同，只不过是用 `Field` 替换了`Path`、`Query`、`Body`。

///

## 添加更多信息 { #add-extra-information }

`Field`、`Query`、`Body` 等对象里可以声明更多信息，并且 JSON Schema 中也会集成这些信息。

*声明示例*一章中将详细介绍添加更多信息的知识。

/// warning | 警告

传递给 `Field` 的额外键也会出现在你的应用生成的 OpenAPI 架构中。
由于这些键不一定属于 OpenAPI 规范的一部分，某些 OpenAPI 工具（例如 [OpenAPI 验证器](https://validator.swagger.io/)）可能无法处理你生成的架构。

///

## 小结 { #recap }

Pydantic 的 `Field` 可以为模型属性声明更多校验和元数据。

传递 JSON Schema 元数据还可以使用更多关键字参数。
