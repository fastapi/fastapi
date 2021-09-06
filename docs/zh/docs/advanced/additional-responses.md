# OpenAPI 中的额外响应

!!! warning "警告"

    本章较难。
    
    **FastAPI** 新手可跳过本章。

本章学习为响应声明额外的状态码、媒体类型和描述。

这些响应会包含在 OpenAPI 概图里，并在 API 文档中显示。

但必须要确保这些响应与状态码和 `content` 一起直接以一个 `Response` 对象如 `JSONResponse` 返回。

## 以 `model` 声明额外响应

*路径操作装饰器*支持 `responses` 参数。

`responses` 参数可以接收以响应状态码为键，如 `200`，响应信息为值的字典。

响应字典可以包含 Pydantic 模型的键 `model`，如 `response_model`。

**FastAPI** 接收该模型，生成 JSON 概图，并保存在 OpenAPI 指定的位置。

例如，声明包含状态码 `404` 及 Pydantic 模型 `Message` 的响应，代码如下：

```Python hl_lines="18  23"
{!../../../docs_src/additional_responses/tutorial001.py!}
```

!!! note "笔记"

    注意，必须直接返回 `JSONResponse`。

!!! info "说明"

    `model` 键不是 OpenAPI 的组件。
    
    **FastAPI** 在此接收 Pydantic 模型，生成 `JSON Schema`，并把它置于正确的位置。
    
    正确的位置是：
    
    * `content` 键中的 JSON 对象（字典），该对象包含：
        * `application/json` 等媒体类型的键，此键中的 JSON 对象中包含：
            * `schema` 键，包含了模型中的 JSON 概图，这里就是正确的位置。
                * **FastAPI** 在此添加 OpenAPI 的其它位置要引用的全局 JSON 概图，而不是直接包含此概图。通过这种方式，其它应用和客户端可以直接使用这些 JSON 概图，为代码生成工具提供更好的支持。

OpenAPI 中，该*路径操作*生成的响应如下：

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

OpenAPI 概图在内部其它位置引用这个概图：

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

## 主响应的附加媒体类型

使用 `response` 参数还可以为主响应添加媒体类型。

例如，添加 `image/png` 媒体类型，声明返回 JSON 对象（使用 `application/json`）或 PNG 图像的*路径操作*：

```Python hl_lines="19-24  28"
{!../../../docs_src/additional_responses/tutorial002.py!}
```

!!! note "笔记"

    注意，必须直接使用 `FileResponse` 返回图像。

!!! info "说明"

    除非在 `response` 参数中显式指定其它媒体类型，否则，FastAPI 假设该响应和主响应类的媒体类型一样（默认为 `application/json`）。
    
    使用 `None` 指定自定义响应类的媒体类型时，FastAPI 会为包含关联模型的响应使用 `application/json`。

## 合并信息

**FastAPI** 支持合并 `response_model`、`status_code`、`responses` 参数等多个位置的响应信息。

使用默认状态码 `200`（或自定义状态码），声明 `response_model`。然后，直接在 OpenAPI 概图中，为 `responses` 中的同一响应声明更多信息。

**FastAPI** 保留 `responses` 中的信息，并把它与模型的 JSON 概图合并在一起。

例如，使用 Pydantic 模型声明包含状态码 `404` 的响应，并包含自定义 `description`。

带状态码 `200` 的响应不仅使用 `response_model`，还包含了自定义 `example`：

```Python hl_lines="20-31"
{!../../../docs_src/additional_responses/tutorial003.py!}
```

OpenAPI 中会合并、包含这些内容，然后显示在 API 文档中：

<img src="/img/tutorial/additional-responses/image01.png">

## 合并预定义响应与自定义响应

**FastAPI **还可以合并*路径操作*中的预定义响应和自定义响应。

此处使用 Python **字典解包**，即 `**dict_to_unpack`：

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

在此，`new_dict` 包含 `old_dict` 中的所有键值对，以及新的键值对：

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

这种技巧既可以复用*路径操作*中的预定义响应，还可以合并预定义响应和自定义响应。

例如：

```Python hl_lines="13-17  26"
{!../../../docs_src/additional_responses/tutorial004.py!}
```

## OpenAPI 响应的更多说明

要了解响应中都包含了哪些内容，请参阅 OpenAPI 规范的相关章节：

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responsesObject" class="external-link" target="_blank">OpenAPI 的 Responses 对象</a>，该对象包括 `Response` 对象；
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responseObject" class="external-link" target="_blank">OpenAPI 的 Response 对象</a>，为 `responses` 参数内的每个响应直接添加各种内容，包括 `description`、`headers`、`content`（此项下可声明媒体类型和 JSON 概图）、`links` 等。
