# 路径操作的高级配置 { #path-operation-advanced-configuration }

## OpenAPI 的 operationId { #openapi-operationid }

/// warning

如果你并非 OpenAPI 的“专家”，你可能不需要这部分内容。

///

你可以在 *路径操作* 中通过参数 `operation_id` 设置要使用的 OpenAPI `operationId`。

务必确保每个操作的 `operation_id` 都是唯一的。

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### 使用 *路径操作函数* 的函数名作为 operationId { #using-the-path-operation-function-name-as-the-operationid }

如果你想用 API 的函数名作为 `operationId`，你可以遍历所有路径操作，并使用它们的 `APIRoute.name` 重写每个 *路径操作* 的 `operation_id`。

你应该在添加了所有 *路径操作* 之后执行此操作。

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2, 12:21, 24] *}

/// tip

如果你手动调用 `app.openapi()`，你应该在此之前更新 `operationId`。

///

/// warning

如果你这样做，务必确保你的每个 *路径操作函数* 的名字唯一。

即使它们在不同的模块中（Python 文件）。

///

## 从 OpenAPI 中排除 { #exclude-from-openapi }

使用参数 `include_in_schema` 并将其设置为 `False`，来从生成的 OpenAPI 方案中排除一个 *路径操作*（这样一来，就从自动化文档系统中排除掉了）：

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## 来自 docstring 的高级描述 { #advanced-description-from-docstring }

你可以限制 *路径操作函数* 的 `docstring` 中用于 OpenAPI 的行数。

添加一个 `\f`（一个“换页”的转义字符）可以使 **FastAPI** 在那一位置截断用于 OpenAPI 的输出。

剩余部分不会出现在文档中，但是其他工具（比如 Sphinx）可以使用剩余部分。

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## 附加响应 { #additional-responses }

你可能已经见过如何为一个 *路径操作* 声明 `response_model` 和 `status_code`。

这定义了该 *路径操作* 主响应的元数据。

你也可以为它声明带有各自模型、状态码等的附加响应。

文档中有一个完整章节，你可以阅读这里的[OpenAPI 中的附加响应](additional-responses.md){.internal-link target=_blank}。

## OpenAPI Extra { #openapi-extra }

当你在应用中声明一个 *路径操作* 时，**FastAPI** 会自动生成与该 *路径操作* 相关的元数据，以包含到 OpenAPI 方案中。

/// note | 技术细节

在 OpenAPI 规范中，这被称为 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operation 对象</a>。

///

它包含关于该 *路径操作* 的所有信息，并用于生成自动文档。

它包括 `tags`、`parameters`、`requestBody`、`responses` 等。

这个特定于 *路径操作* 的 OpenAPI 方案通常由 **FastAPI** 自动生成，但你也可以扩展它。

/// tip

这是一个较低层级的扩展点。

如果你只需要声明附加响应，更方便的方式是使用[OpenAPI 中的附加响应](additional-responses.md){.internal-link target=_blank}。

///

你可以使用参数 `openapi_extra` 扩展某个 *路径操作* 的 OpenAPI 方案。

### OpenAPI 扩展 { #openapi-extensions }

例如，这个 `openapi_extra` 可用于声明 [OpenAPI 扩展](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions)：

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

当你打开自动 API 文档时，你的扩展会显示在该 *路径操作* 的底部。

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

如果你查看最终生成的 OpenAPI（在你的 API 的 `/openapi.json`），你也会看到你的扩展作为该 *路径操作* 的一部分：

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

### 自定义 OpenAPI 路径操作方案 { #custom-openapi-path-operation-schema }

`openapi_extra` 中的字典会与该 *路径操作* 自动生成的 OpenAPI 方案进行深度合并。

因此，你可以在自动生成的方案上添加额外数据。

例如，你可以决定用自己的代码读取并验证请求，而不使用 FastAPI 与 Pydantic 的自动功能，但你仍然希望在 OpenAPI 方案中定义该请求。

你可以用 `openapi_extra` 来做到：

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

在这个示例中，我们没有声明任何 Pydantic 模型。事实上，请求体甚至没有被 <dfn title="从某种纯文本格式（如字节）转换为 Python 对象">解析</dfn> 为 JSON，而是直接以 `bytes` 读取，并由函数 `magic_data_reader()` 以某种方式负责解析。

尽管如此，我们仍然可以声明请求体的预期方案。

### 自定义 OpenAPI 内容类型 { #custom-openapi-content-type }

使用同样的技巧，你可以用一个 Pydantic 模型来定义 JSON Schema，然后把它包含到该 *路径操作* 的自定义 OpenAPI 方案部分中。

即使请求中的数据类型不是 JSON，你也可以这样做。

例如，在这个应用中我们不使用 FastAPI 集成的从 Pydantic 模型提取 JSON Schema 的功能，也不使用对 JSON 的自动校验。实际上，我们将请求的内容类型声明为 YAML，而不是 JSON：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

尽管我们没有使用默认的集成功能，我们仍然使用 Pydantic 模型手动生成我们想以 YAML 接收的数据的 JSON Schema。

然后我们直接使用请求并将请求体提取为 `bytes`。这意味着 FastAPI 甚至不会尝试将请求负载解析为 JSON。

接着在我们的代码中，我们直接解析该 YAML 内容，然后再次使用同一个 Pydantic 模型来验证该 YAML 内容：

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip

这里我们复用了同一个 Pydantic 模型。

但同样地，我们也可以用其他方式对其进行验证。

///
