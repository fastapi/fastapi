# 概图的更多信息 - 示例

FastAPI 支持为应用中的数据声明示例。

以下是几种实现的方式。

## Pydantic 的 `schema_extra`

使用 `Config` 与 `schema_extra` 为 Pydantic 模型声明 `example`， 详见 <a href="https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization" class="external-link" target="_blank">Pydantic 文档：自定义概图</a>：

```Python hl_lines="15-23"
{!../../../docs_src/schema_extra_example/tutorial001.py!}
```

输出的 **JSON Schema** 中会为模型添加这些附加信息，并在 API 自动文档中显示。

!!! tip "提示"

    同样，可以扩展 JSON Schema，并添加更多自定义信息。
    
    例如，为前端用户界面添加元数据等信息。

## 更多 `Field` 参数

向 Pydantic 模型的 `Field()` 传递参数，可以为 **JSON Schema** 声明更多信息。

使用 `Field()` 为字段添加 `example`：

```Python hl_lines="4  10-13"
{!../../../docs_src/schema_extra_example/tutorial002.py!}
```

!!! warning "警告"

    注意，传递的这些参数不添加验证，只添加供存档使用的额外信息。

## OpenAPI 中的 `example` 与 `examples`

使用以下任意函数时：

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

还可以通过声明数据的 `example`，或一组 `examples` 向 **OpenAPI** 添加更多信息。

### 在 `Body` 中使用 `example`

下列代码向 `Body()`  传递`example` 数据：

```Python hl_lines="21-26"
{!../../../docs_src/schema_extra_example/tutorial003.py!}
```

### 文档中的示例

上述示例代码在文档 `/docs` 中的显示效果如下：

<img src="/img/tutorial/body-fields/image01.png">

### 在`Body` 中使用 `examples`

除了单个的 `example`，还可以使用 `dict` 传递 `examples`，以此来显示多个示例，这些示例信息也会被添加至 **OpenAPI**。

`dict` 通过*键*识别示例，这些示例的值也是 `dict`。

`examples` 的 `dict` 包含下列内容：

* `summary`：示例简述
* `description`：支持 Markdown 格式的较长描述
* `value`：实际显示的示例，可以是 `dict`
* `externalValue`：`value` 的备选项，指向示例的 URL。但可能有些工具不支持

```Python hl_lines="22-48"
{!../../../docs_src/schema_extra_example/tutorial004.py!}
```

### 文档中显示的多个示例

`Body()` 中包含 `examples` 时，在文档 `/docs` 中的显示如下图：

<img src="/img/tutorial/body-fields/image02.png">

## 技术细节

!!! warning "警告"

    与 **JSON Schema** 和 **OpenAPI** 相关的技术细节很多。
    
    一般情况下，理解上文中的代码就已经够用了，下面的技术细节不是必须的，跳过阅读也无所谓。

在 Pydantic 模型内部添加示例时， 使用 `schema_extra` 或 `Field(example="something")` ，就可以把 Pydantic 模型的示例添加至 **JSON Schema**。

Pydantic 模型的 **JSON Schema** 包含在 API 的 **OpenAPI** 中，并在文档中显示。

实际上，**JSON Schema** 标准中没有 `example`。新版 JSON Schema 中定义了 <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a> 字段，但  OpenAPI 3.0.3 基于的旧版 JSON Schema 没有`examples` 字段。

因此，OpenAPI 3.0.3 定义了自己的 <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-20" class="external-link" target="_blank">`example`</a>，供新版  **JSON Schema** 使用（但它用的只是 `example`，不是 `examples`）。同样，（使用 Swagger UI 的）API 文档中用的也是 `example`。

`example` 不是 JSON Schema 的组件，但它是 OpenAPI 为  JSON Schema 定制的组件，因此，文档中使用 `example`。

但在（`Query()`、`Body()` 等）其他工具中使用 `example` 或 `examples` 时，这些描述数据的示例不会被添加至 JSON Schema（包括 OpenAPI 自己的 JSON Schema），而是被直接添加至 OpenAPI 的*路径操作*声明里（OpenAPI 使用 JSON Schema 外部的组件）。

对于 `Path()`、`Query()`、`Header()`、`Cookie()`，`example` 或 `examples` 被添加至 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameter-object" class="external-link" target="_blank">OpenAPI 定义中的`Parameter Object`（规范）</a>。

对于 `Body()`、`File()`、`Form()`，`example` 或 `examples` 被添加至 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#mediaTypeObject" class="external-link" target="_blank">OpenAPI 定义中`content` 字段里的 `Request Body Object` 中的 `Media Type Object`（规范）</a>。

另一方面，新近发布的 OpenAPI **3.1.0** 版已经支持最新的 JSON Schema， 移除了绝大多数 OpenAPI 自定义的 JSON Schema，从而可以使用新版 JSON Schema 的功能，它们之间的细微区别也进一步减少。但 Swagger UI 现在还不支持 OpenAPI 3.1.0，因此，现在最好还是使用本章中的开发思路。
