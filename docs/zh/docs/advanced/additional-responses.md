# OPENAPI 中的其他响应 { #additional-responses-in-openapi }

/// warning | 警告

这是一个相当高级的话题。

如果你刚开始使用 **FastAPI**，可能不需要这个。

///

你可以声明附加响应，包括附加状态码、媒体类型、描述等。

这些额外的响应将包含在 OpenAPI schema 中，因此它们也将出现在 API 文档中。

但是对于这些额外的响应，你必须确保你直接返回一个像 `JSONResponse` 一样的 `Response`，并包含你的状态码和内容。

## 使用 `model` 的附加响应 { #additional-response-with-model }

你可以向你的*路径操作装饰器*传递参数 `responses`。

它接收一个 `dict`：键是每个响应的状态码（如 `200`），值是包含每个响应信息的其他 `dict`。

这些响应 `dict` 中的每一个都可以有一个键 `model`，包含一个 Pydantic 模型，就像 `response_model` 一样。

**FastAPI** 将采用该模型，生成其 JSON Schema 并将其包含在 OpenAPI 的正确位置。

例如，要声明另一个具有状态码 `404` 和 Pydantic 模型 `Message` 的响应，你可以这样写：

{* ../../docs_src/additional_responses/tutorial001_py39.py hl[18,22] *}

/// note | 注意

请记住，你必须直接返回 `JSONResponse`。

///

/// info | 信息

`model` 键不是 OpenAPI 的一部分。

**FastAPI** 将从那里获取 Pydantic 模型，生成 JSON Schema，并将其放在正确的位置。

正确的位置是：

* 在键 `content` 中，其值是另一个 JSON 对象（`dict`），它包含：
    * 一个以媒体类型为键（例如 `application/json`）的条目，其值是另一个 JSON 对象，它包含：
        * 一个键 `schema`，其值是来自模型的 JSON Schema，这里就是正确的位置。
            * **FastAPI** 在这里添加了对 OpenAPI 中另一个地方的全局 JSON Schemas 的引用，而不是直接包含它。这样，其他应用程序和客户端可以直接使用这些 JSON Schemas，提供更好的代码生成工具等。

///

为该*路径操作*在 OpenAPI 中生成的响应将是：

```JSON hl_lines="3-12"
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

这些 schema 被引用到 OpenAPI schema 中的另一个位置：

```JSON hl_lines="4-16"
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## 为主响应添加其他媒体类型 { #additional-media-types-for-the-main-response }

你可以使用同一个 `responses` 参数，为同一个主响应添加不同的媒体类型。

例如，你可以添加一个额外的媒体类型 `image/png`，声明你的*路径操作*可以返回一个 JSON 对象（媒体类型 `application/json`）或一张 PNG 图片：

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | 注意

请注意，你必须直接使用 `FileResponse` 返回图片。

///

/// info | 信息

除非你在 `responses` 参数中显式指定不同的媒体类型，否则 FastAPI 会假定响应与主响应类具有相同的媒体类型（默认为 `application/json`）。

但是如果你指定了一个自定义响应类，并将 `None` 作为其媒体类型，FastAPI 将对任何带有关联模型的附加响应使用 `application/json`。

///

## 组合信息 { #combining-information }

你也可以组合来自多个位置的响应信息，包括 `response_model`、`status_code` 和 `responses` 参数。

你可以声明一个 `response_model`，使用默认状态码 `200`（或者如果你需要，也可以用自定义状态码），然后在 `responses` 中直接在 OpenAPI schema 里为同一个响应声明附加信息。

**FastAPI** 将保留来自 `responses` 的附加信息，并将其与模型的 JSON Schema 结合起来。

例如，你可以声明一个状态码 `404` 的响应，它使用 Pydantic 模型并具有自定义的 `description`。

以及一个状态码为 `200` 的响应，它使用你的 `response_model`，但包含自定义的 `example`：

{* ../../docs_src/additional_responses/tutorial003_py39.py hl[20:31] *}

这些将全部被合并并包含在你的 OpenAPI 中，并在 API 文档中显示：

<img src="/img/tutorial/additional-responses/image01.png">

## 组合预定义响应和自定义响应 { #combine-predefined-responses-and-custom-ones }

你可能希望有一些适用于许多*路径操作*的预定义响应，但你也想把它们与每个*路径操作*所需的自定义响应组合起来。

对于这些情况，你可以使用 Python 的“解包（unpacking）”技术，通过 `**dict_to_unpack` 解包一个 `dict`：

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

这里，`new_dict` 将包含来自 `old_dict` 的所有键值对，以及新的键值对：

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

你可以使用该技术在你的*路径操作*中复用一些预定义响应，并将它们与额外的自定义响应相结合。

例如：

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## 关于 OpenAPI 响应的更多信息 { #more-information-about-openapi-responses }

要查看你到底可以在响应中包含哪些内容，你可以查看 OpenAPI 规范中的这些部分：

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses Object</a>，它包含 `Response Object`。
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response Object</a>，你可以直接把这里的任何内容包含到 `responses` 参数中每个响应里。包括 `description`、`headers`、`content`（在这里声明不同媒体类型和 JSON Schemas）以及 `links`。
