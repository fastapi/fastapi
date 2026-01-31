# 声明请求示例数据 { #declare-request-example-data }

你可以声明应用可以接收的数据示例。

下面是几种实现方式。

## 在 Pydantic 模型中添加额外的 JSON Schema 数据 { #extra-json-schema-data-in-pydantic-models }

你可以为 Pydantic 模型声明 `examples`，它们会被添加到生成的 JSON Schema 中。

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

这些额外信息会原样添加到该模型输出的 **JSON Schema** 中，并会在 API 文档中使用。

你可以使用属性 `model_config`，它接收一个 `dict`，如 <a href="https://docs.pydantic.dev/latest/api/config/" class="external-link" target="_blank">Pydantic 文档：Configuration</a> 中所述。

你可以设置 `"json_schema_extra"` 为一个 `dict`，其中包含你希望显示在生成的 JSON Schema 中的任何额外数据，包括 `examples`。

/// tip | 提示

你可以使用相同的技术来扩展 JSON Schema，并添加你自己的自定义额外信息。

例如，你可以用它来为前端用户界面添加元数据等。

///

/// info | 信息

OpenAPI 3.1.0（从 FastAPI 0.99.0 开始使用）新增了对 `examples` 的支持，它是 **JSON Schema** 标准的一部分。

在那之前，它只支持关键字 `example`，且只能有单个示例。OpenAPI 3.1.0 仍然支持它，但它已被弃用，并且不是 JSON Schema 标准的一部分。因此建议你将 `example` 迁移到 `examples`。🤓

你可以在本页末尾阅读更多内容。

///

## `Field` 的附加参数 { #field-additional-arguments }

在 Pydantic 模型中使用 `Field()` 时，你也可以声明额外的 `examples`：

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## JSON Schema - OpenAPI 中的 `examples` { #examples-in-json-schema-openapi }

当你使用以下任意一个：

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

你也可以声明一组带有附加信息的 `examples`，它们会被添加到 **OpenAPI** 内部的 **JSON Schemas** 中。

### 带 `examples` 的 `Body` { #body-with-examples }

这里我们传递 `examples`，其中包含一个在 `Body()` 中期望的数据示例：

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### 文档 UI 中的示例 { #example-in-the-docs-ui }

使用上面的任何方法，它在 `/docs` 中看起来都会是这样：

<img src="/img/tutorial/body-fields/image01.png">

### 带多个 `examples` 的 `Body` { #body-with-multiple-examples }

当然你也可以传递多个 `examples`：

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

这样做时，这些示例会成为该请求体数据内部 **JSON Schema** 的一部分。

不过，在 <abbr title="2023-08-26">本文撰写时</abbr>，负责展示文档 UI 的工具 Swagger UI 还不支持在 **JSON Schema** 中展示多个数据示例。但下面会介绍一种变通方案。

### OpenAPI 特有的 `examples` { #openapi-specific-examples }

在 **JSON Schema** 支持 `examples` 之前，OpenAPI 就已经支持另一个同样叫 `examples` 的字段。

这个 **OpenAPI 特有的** `examples` 位于 OpenAPI 规范中的另一个部分。它位于 **每个*路径操作*的详情**中，而不是在每个 JSON Schema 内部。

并且 Swagger UI 早就支持这个特定的 `examples` 字段。因此，你可以用它来在 **文档 UI 中展示**不同的**示例**。

这个 OpenAPI 特有字段 `examples` 的结构是一个 `dict`，包含**多个示例**（而不是 `list`），并且每个示例都带有额外信息，这些信息也会被添加到 **OpenAPI** 中。

它不会进入 OpenAPI 中包含的每个 JSON Schema 内部，而是放在 *路径操作* 本身的外部。

### 使用 `openapi_examples` 参数 { #using-the-openapi-examples-parameter }

你可以在 FastAPI 中使用参数 `openapi_examples` 来声明 OpenAPI 特有的 `examples`，适用于：

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

`dict` 的键用于标识每个示例，每个值则是另一个 `dict`。

`examples` 中每个具体示例的 `dict` 可以包含：

* `summary`：示例的简短描述。
* `description`：较长的描述，可包含 Markdown 文本。
* `value`：实际展示的示例，例如一个 `dict`。
* `externalValue`：`value` 的替代项，一个指向示例的 URL。尽管它可能不像 `value` 那样被许多工具支持。

你可以这样使用：

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### 文档 UI 中的 OpenAPI 示例 { #openapi-examples-in-the-docs-ui }

将 `openapi_examples` 添加到 `Body()` 后，`/docs` 会显示为：

<img src="/img/tutorial/body-fields/image02.png">

## 技术细节 { #technical-details }

/// tip | 提示

如果你已经在使用 **FastAPI** **0.99.0 或更高版本**，你大概可以**跳过**这些细节。

这些内容对更旧的版本更相关，也就是在 OpenAPI 3.1.0 尚不可用之前。

你可以把它当作一堂简短的 OpenAPI 和 JSON Schema **历史课**。🤓

///

/// warning | 警告

这里包含关于标准 **JSON Schema** 与 **OpenAPI** 的非常技术性的细节。

如果上面的思路已经适用于你，那可能就足够了，你大概不需要这些细节，可以随意跳过。

///

在 OpenAPI 3.1.0 之前，OpenAPI 使用的是更旧且经过修改的 **JSON Schema** 版本。

JSON Schema 没有 `examples`，因此 OpenAPI 在其修改后的版本中加入了自己的 `example` 字段。

OpenAPI 还在规范的其他部分加入了 `example` 和 `examples` 字段：

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object" class="external-link" target="_blank">`Parameter Object`（规范中）</a>，FastAPI 的以下工具使用了它：
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object" class="external-link" target="_blank">`Request Body Object`，在字段 `content` 中，对应 `Media Type Object`（规范中）</a>，FastAPI 的以下工具使用了它：
    * `Body()`
    * `File()`
    * `Form()`

/// info | 信息

这个旧的 OpenAPI 特有 `examples` 参数从 FastAPI `0.103.0` 起改名为 `openapi_examples`。

///

### JSON Schema 的 `examples` 字段 { #json-schemas-examples-field }

但随后 JSON Schema 在新版本规范中加入了 <a href="https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5" class="external-link" target="_blank">`examples`</a> 字段。

接着新的 OpenAPI 3.1.0 基于最新版本（JSON Schema 2020-12），其中包含了这个新字段 `examples`。

现在，这个新的 `examples` 字段优先于旧的单个（且自定义的）`example` 字段，而后者现在已被弃用。

JSON Schema 中这个新的 `examples` 字段**只是一个示例的 `list`**，不像 OpenAPI 其他位置（上面描述的）那样是带额外元数据的 `dict`。

/// info | 信息

即使 OpenAPI 3.1.0 已发布，并实现了这种与 JSON Schema 更简单的新集成方式，但在一段时间里，提供自动文档的工具 Swagger UI 仍不支持 OpenAPI 3.1.0（从 5.0.0 版本开始支持 🎉）。

因此，FastAPI 0.99.0 之前的版本仍使用低于 3.1.0 的 OpenAPI 版本。

///

### Pydantic 和 FastAPI 的 `examples` { #pydantic-and-fastapi-examples }

当你在 Pydantic 模型中添加 `examples`（使用 `schema_extra` 或 `Field(examples=["something"])`）时，该示例会被添加到这个 Pydantic 模型的 **JSON Schema** 中。

而该 Pydantic 模型的 **JSON Schema** 会被包含进你的 API 的 **OpenAPI** 中，然后用于文档 UI。

在 FastAPI 0.99.0 之前的版本（0.99.0 及以上使用更新的 OpenAPI 3.1.0），当你在其他工具（`Query()`、`Body()` 等）中使用 `example` 或 `examples` 时，这些示例不会被添加到描述该数据的 JSON Schema 中（甚至不会添加到 OpenAPI 自己那套 JSON Schema 版本中），而是直接添加到 OpenAPI 中的 *路径操作* 声明里（在 OpenAPI 中使用 JSON Schema 的部分之外）。

但现在 FastAPI 0.99.0 及以上使用 OpenAPI 3.1.0（它使用 JSON Schema 2020-12），并配合 Swagger UI 5.0.0 及以上，一切都更一致了，示例也会被包含在 JSON Schema 中。

### Swagger UI 与 OpenAPI 特有的 `examples` { #swagger-ui-and-openapi-specific-examples }

现在，由于 Swagger UI（截至 2023-08-26）不支持多个 JSON Schema 示例，用户无法在文档中展示多个示例。

为了解决这个问题，FastAPI `0.103.0` **新增了对**使用新参数 `openapi_examples` 来声明同一个旧的 **OpenAPI 特有** `examples` 字段的支持。🤓

### 总结 { #summary }

我以前总说我不太喜欢历史……结果现在在这里讲“技术史”课。😅

简而言之，**升级到 FastAPI 0.99.0 或更高版本**，事情会更**简单、一致、直观**，你也不需要了解这些历史细节。😎
