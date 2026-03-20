# 声明请求示例数据 { #declare-request-example-data }

你可以为你的应用将接收的数据声明示例。

这里有几种实现方式。

## Pydantic 模型中的额外 JSON Schema 数据 { #extra-json-schema-data-in-pydantic-models }

你可以为一个 Pydantic 模型声明 `examples`，它们会被添加到生成的 JSON Schema 中。

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

这些额外信息会原样添加到该模型输出的 JSON Schema 中，并会在 API 文档中使用。

你可以使用属性 `model_config`，它接收一个 `dict`，详见 <a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">Pydantic 文档：配置</a>。

你可以设置 `"json_schema_extra"`，其值为一个 `dict`，包含你希望出现在生成 JSON Schema 中的任意附加数据，包括 `examples`。

/// tip | 提示

你也可以用同样的技巧扩展 JSON Schema，添加你自己的自定义额外信息。

例如，你可以用它为前端用户界面添加元数据等。

///

/// info | 信息

OpenAPI 3.1.0（自 FastAPI 0.99.0 起使用）增加了对 `examples` 的支持，它是 JSON Schema 标准的一部分。

在此之前，只支持使用单个示例的关键字 `example`。OpenAPI 3.1.0 仍然支持它，但它已被弃用，并不属于 JSON Schema 标准。因此，建议你把 `example` 迁移到 `examples`。🤓

你可以在本页末尾阅读更多内容。

///

## `Field` 的附加参数 { #field-additional-arguments }

在 Pydantic 模型中使用 `Field()` 时，你也可以声明额外的 `examples`：

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## JSON Schema 中的 `examples` - OpenAPI { #examples-in-json-schema-openapi }

在以下任意场景中使用：

- `Path()`
- `Query()`
- `Header()`
- `Cookie()`
- `Body()`
- `Form()`
- `File()`

你也可以声明一组 `examples`，这些带有附加信息的示例将被添加到它们在 OpenAPI 中的 JSON Schema 里。

### 带有 `examples` 的 `Body` { #body-with-examples }

这里我们向 `Body()` 传入 `examples`，其中包含一个期望的数据示例：

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### 文档 UI 中的示例 { #example-in-the-docs-ui }

使用上述任一方法，在 `/docs` 中看起来会是这样：

<img src="/img/tutorial/body-fields/image01.png">

### 带有多个 `examples` 的 `Body` { #body-with-multiple-examples }

当然，你也可以传入多个 `examples`：

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

这样做时，这些示例会成为该请求体数据内部 JSON Schema 的一部分。

不过，在<dfn title="2023-08-26">撰写本文时</dfn>，用于展示文档 UI 的 Swagger UI 并不支持显示 JSON Schema 中数据的多个示例。但请继续阅读，下面有一种变通方法。

### OpenAPI 特定的 `examples` { #openapi-specific-examples }

在 JSON Schema 支持 `examples` 之前，OpenAPI 就已支持一个同名但不同的字段 `examples`。

这个面向 OpenAPI 的 `examples` 位于 OpenAPI 规范的另一处。它放在每个路径操作的详细信息中，而不是每个 JSON Schema 里。

而 Swagger UI 早就支持这个特定的 `examples` 字段。因此，你可以用它在文档 UI 中展示不同的示例。

这个 OpenAPI 特定字段 `examples` 的结构是一个包含多个示例的 `dict`（而不是一个 `list`），每个示例都包含会被添加到 OpenAPI 的额外信息。

这不放在 OpenAPI 内部包含的各个 JSON Schema 里，而是直接放在路径操作上。

### 使用 `openapi_examples` 参数 { #using-the-openapi-examples-parameter }

你可以在 FastAPI 中通过参数 `openapi_examples` 来声明这个 OpenAPI 特定的 `examples`，适用于：

- `Path()`
- `Query()`
- `Header()`
- `Cookie()`
- `Body()`
- `Form()`
- `File()`

这个 `dict` 的键用于标识每个示例，每个值是另一个 `dict`。

`examples` 中每个具体示例的 `dict` 可以包含：

- `summary`：该示例的简短描述。
- `description`：较长描述，可以包含 Markdown 文本。
- `value`：实际展示的示例，例如一个 `dict`。
- `externalValue`：`value` 的替代项，指向该示例的 URL。不过它的工具支持度可能不如 `value`。

你可以这样使用：

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### 文档 UI 中的 OpenAPI 示例 { #openapi-examples-in-the-docs-ui }

当把 `openapi_examples` 添加到 `Body()` 后，`/docs` 会如下所示：

<img src="/img/tutorial/body-fields/image02.png">

## 技术细节 { #technical-details }

/// tip | 提示

如果你已经在使用 FastAPI 版本 0.99.0 或更高版本，你大概率可以跳过这些细节。

它们对更早版本（OpenAPI 3.1.0 尚不可用之前）更相关。

你可以把这当作一堂简短的 OpenAPI 和 JSON Schema 历史课。🤓

///

/// warning | 警告

以下是关于 JSON Schema 和 OpenAPI 标准的非常技术性的细节。

如果上面的思路对你已经足够可用，你可能不需要这些细节，可以直接跳过。

///

在 OpenAPI 3.1.0 之前，OpenAPI 使用的是一个更旧且经过修改的 JSON Schema 版本。

当时 JSON Schema 没有 `examples`，所以 OpenAPI 在它修改过的版本中添加了自己的 `example` 字段。

OpenAPI 还在规范的其他部分添加了 `example` 和 `examples` 字段：

- <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Parameter Object`（规范中）</a>，被 FastAPI 的以下内容使用：
    - `Path()`
    - `Query()`
    - `Header()`
    - `Cookie()`
- <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Request Body Object` 中的 `content` 字段里的 `Media Type Object`（规范中）</a>，被 FastAPI 的以下内容使用：
    - `Body()`
    - `File()`
    - `Form()`

/// info | 信息

这个旧的、OpenAPI 特定的 `examples` 参数，自 FastAPI `0.103.0` 起改名为 `openapi_examples`。

///

### JSON Schema 的 `examples` 字段 { #json-schemas-examples-field }

后来，JSON Schema 在新版本的规范中添加了 <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a> 字段。

随后新的 OpenAPI 3.1.0 基于最新版本（JSON Schema 2020-12），其中包含了这个新的 `examples` 字段。

现在，这个新的 `examples` 字段优先于旧的单个（且自定义的）`example` 字段，后者已被弃用。

JSON Schema 中这个新的 `examples` 字段只是一个由示例组成的 `list`，而不是像上面提到的 OpenAPI 其他位置那样带有额外元数据的 `dict`。

/// info | 信息

即使在 OpenAPI 3.1.0 发布、并与 JSON Schema 有了这种更简单的集成之后，有一段时间里，提供自动文档的 Swagger UI 并不支持 OpenAPI 3.1.0（它自 5.0.0 版本起已支持 🎉）。

因此，FastAPI 0.99.0 之前的版本仍然使用低于 3.1.0 的 OpenAPI 版本。

///

### Pydantic 与 FastAPI 的 `examples` { #pydantic-and-fastapi-examples }

当你在 Pydantic 模型中添加 `examples`，通过 `schema_extra` 或 `Field(examples=["something"])`，这些示例会被添加到该 Pydantic 模型的 JSON Schema 中。

这个 Pydantic 模型的 JSON Schema 会被包含到你的 API 的 OpenAPI 中，然后在文档 UI 中使用。

在 FastAPI 0.99.0 之前的版本（0.99.0 及以上使用更新的 OpenAPI 3.1.0），当你在其他工具（`Query()`、`Body()` 等）中使用 `example` 或 `examples` 时，这些示例不会被添加到描述该数据的 JSON Schema 中（甚至不会添加到 OpenAPI 自己的 JSON Schema 版本中），而是会直接添加到 OpenAPI 的路径操作声明中（在 OpenAPI 使用 JSON Schema 的部分之外）。

但现在 FastAPI 0.99.0 及以上使用 OpenAPI 3.1.0（其使用 JSON Schema 2020-12）以及 Swagger UI 5.0.0 及以上后，一切更加一致，示例会包含在 JSON Schema 中。

### Swagger UI 与 OpenAPI 特定的 `examples` { #swagger-ui-and-openapi-specific-examples }

此前，由于 Swagger UI 不支持多个 JSON Schema 示例（截至 2023-08-26），用户无法在文档中展示多个示例。

为了解决这个问题，FastAPI `0.103.0` 通过新增参数 `openapi_examples`，为声明同样的旧式 OpenAPI 特定 `examples` 字段提供了支持。🤓

### 总结 { #summary }

我曾经说我不太喜欢历史……结果现在在这儿上“技术史”课。😅

简而言之，升级到 FastAPI 0.99.0 或更高版本，一切会更简单、一致、直观，你也不必了解这些历史细节。😎
