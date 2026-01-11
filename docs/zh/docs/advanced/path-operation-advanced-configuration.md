# 路径操作的高级配置 { #path-operation-advanced-configuration }

## OpenAPI 的 operationId { #openapi-operationid }

/// warning | 警告

如果你不是 OpenAPI 的“专家”，你可能不需要这部分内容。

///

你可以在*路径操作*中通过参数 `operation_id` 设置要使用的 OpenAPI `operationId`。

你必须确保每个操作的 `operation_id` 都是唯一的。

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py39.py hl[6] *}

### 使用*路径操作函数*的函数名作为 operationId { #using-the-path-operation-function-name-as-the-operationid }

如果你想用你的 API 的函数名作为 `operationId`，你可以遍历它们，然后使用它们的 `APIRoute.name` 覆盖每个*路径操作*的 `operation_id`。

你应该在添加了所有*路径操作*之后执行此操作。

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py39.py hl[2, 12:21, 24] *}

/// tip | 提示

如果你手动调用 `app.openapi()`，你应该在此之前更新 `operationId`。

///

/// warning | 警告

如果你这样做，你必须确保你的每个*路径操作函数*都有唯一的名字。

即使它们在不同的模块中（Python 文件）。

///

## 从 OpenAPI 中排除 { #exclude-from-openapi }

要从生成的 OpenAPI schema（因此也从自动化文档系统）中排除一个*路径操作*，使用参数 `include_in_schema` 并将其设置为 `False`：

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py39.py hl[6] *}

## 从 docstring 提供高级描述 { #advanced-description-from-docstring }

你可以限制用于 OpenAPI 的*路径操作函数*的 docstring 行数。

添加一个 `\f`（一个转义的“换页”字符）会让 **FastAPI** 在此处截断用于 OpenAPI 的输出。

它不会显示在文档中，但其他工具（例如 Sphinx）将能够使用剩余部分。

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## 额外响应 { #additional-responses }

你可能已经见过如何为一个*路径操作*声明 `response_model` 和 `status_code`。

这定义了一个*路径操作*的主响应的元数据。

你还可以声明额外的响应，包括它们的模型、状态码等。

文档中有一个完整的章节介绍它，你可以在[OpenAPI 中的额外响应](additional-responses.md){.internal-link target=_blank}阅读。

## OpenAPI Extra { #openapi-extra }

当你在应用中声明一个*路径操作*时，**FastAPI** 会自动生成该*路径操作*相关的元数据，并将其包含在 OpenAPI schema 中。

/// note | 注意

在 OpenAPI 规范中，它被称为 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operation Object</a>。

///

它包含关于*路径操作*的所有信息，并用于生成自动化文档。

它包括 `tags`、`parameters`、`requestBody`、`responses` 等。

这个针对特定*路径操作*的 OpenAPI schema 通常由 **FastAPI** 自动生成，但你也可以扩展它。

/// tip | 提示

这是一个较底层的扩展点。

如果你只需要声明额外的响应，更方便的方式是使用[OpenAPI 中的额外响应](additional-responses.md){.internal-link target=_blank}。

///

你可以使用参数 `openapi_extra` 来扩展一个*路径操作*的 OpenAPI schema。

### OpenAPI 扩展 { #openapi-extensions }

例如，这个 `openapi_extra` 可以用于声明 [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions)：

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py39.py hl[6] *}

如果你打开自动 API 文档，你的扩展会显示在对应*路径操作*的底部。

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

如果你查看生成的 OpenAPI（在你的 API 中的 `/openapi.json`），你也会看到你的扩展作为该特定*路径操作*的一部分：

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### 自定义 OpenAPI *路径操作* schema { #custom-openapi-path-operation-schema }

`openapi_extra` 中的字典会与为该*路径操作*自动生成的 OpenAPI schema 进行深度合并。

因此，你可以向自动生成的 schema 中添加额外数据。

例如，你可以决定用你自己的代码读取并校验请求，而不使用 FastAPI 基于 Pydantic 的自动特性，但你仍然希望在 OpenAPI schema 中定义该请求。

你可以用 `openapi_extra` 来实现：

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py39.py hl[19:36, 39:40] *}

在这个示例中，我们没有声明任何 Pydantic 模型。事实上，请求体甚至不会作为 JSON 被 <abbr title="converted from some plain format, like bytes, into Python objects - 从某种普通格式（例如 bytes）转换为 Python 对象">parsed</abbr>，而是直接以 `bytes` 读取，并且函数 `magic_data_reader()` 负责以某种方式解析它。

尽管如此，我们仍然可以为请求体声明预期的 schema。

### 自定义 OpenAPI 内容类型 { #custom-openapi-content-type }

使用同样的技巧，你可以用一个 Pydantic 模型来定义 JSON Schema，然后将其包含在该*路径操作*的自定义 OpenAPI schema 部分中。

而且即使请求中的数据类型不是 JSON，你也可以这样做。

例如，在这个应用中，我们不使用 FastAPI 的集成功能从 Pydantic 模型中提取 JSON Schema，也不使用针对 JSON 的自动校验。实际上，我们声明请求的内容类型为 YAML，而不是 JSON：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[15:20, 22] *}

尽管如此，虽然我们没有使用默认的集成功能，我们仍然使用一个 Pydantic 模型来手动生成我们希望以 YAML 接收的数据的 JSON Schema。

然后我们直接使用请求，并将 body 提取为 `bytes`。这意味着 FastAPI 甚至不会尝试将请求负载解析为 JSON。

然后在我们的代码中，我们直接解析该 YAML 内容，接着我们再次使用同一个 Pydantic 模型来校验 YAML 内容：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[24:31] *}

/// tip | 提示

这里我们复用了同一个 Pydantic 模型。

同样地，我们也可以用其他方式来校验它。

///
