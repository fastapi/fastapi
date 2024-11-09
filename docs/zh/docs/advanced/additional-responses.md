# OPENAPI 中的其他响应

您可以声明附加响应，包括附加状态代码、媒体类型、描述等。

这些额外的响应将包含在OpenAPI模式中，因此它们也将出现在API文档中。

但是对于那些额外的响应，你必须确保你直接返回一个像 `JSONResponse` 一样的 `Response` ，并包含你的状态代码和内容。

## `model`附加响应
您可以向路径操作装饰器传递参数 `responses` 。

它接收一个 `dict`，键是每个响应的状态代码（如`200`），值是包含每个响应信息的其他 `dict`。

每个响应字典都可以有一个关键模型，其中包含一个 `Pydantic` 模型，就像 `response_model` 一样。

**FastAPI**将采用该模型，生成其`JSON Schema`并将其包含在`OpenAPI`中的正确位置。

例如，要声明另一个具有状态码 `404` 和`Pydantic`模型 `Message` 的响应，可以写：
{* ../../docs_src/additional_responses/tutorial001.py hl[18,22] *}

/// note

请记住，您必须直接返回 `JSONResponse` 。

///

/// info

`model` 密钥不是OpenAPI的一部分。
**FastAPI**将从那里获取`Pydantic`模型，生成` JSON Schema` ，并将其放在正确的位置。
- 正确的位置是：
    - 在键 `content` 中，其具有另一个`JSON`对象（ `dict` ）作为值，该`JSON`对象包含：
        - 媒体类型的密钥，例如 `application/json` ，它包含另一个`JSON`对象作为值，该对象包含：
            - 一个键` schema` ，它的值是来自模型的`JSON Schema`，正确的位置在这里。
                - **FastAPI**在这里添加了对OpenAPI中另一个地方的全局JSON模式的引用，而不是直接包含它。这样，其他应用程序和客户端可以直接使用这些JSON模式，提供更好的代码生成工具等。

///

**在OpenAPI中为该路径操作生成的响应将是：**

```json hl_lines="3-12"
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
**模式被引用到OpenAPI模式中的另一个位置：**
```json hl_lines="4-16"
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
## 主响应的其他媒体类型

您可以使用相同的 `responses` 参数为相同的主响应添加不同的媒体类型。

例如，您可以添加一个额外的媒体类型` image/png` ，声明您的路径操作可以返回JSON对象（媒体类型 `application/json` ）或PNG图像：

{* ../../docs_src/additional_responses/tutorial002.py hl[19:24,28] *}

/// note

- 请注意，您必须直接使用 `FileResponse` 返回图像。

///

/// info

- 除非在 `responses` 参数中明确指定不同的媒体类型，否则**FastAPI**将假定响应与主响应类具有相同的媒体类型（默认为` application/json` ）。
- 但是如果您指定了一个自定义响应类，并将 `None `作为其媒体类型，**FastAPI**将使用 `application/json` 作为具有关联模型的任何其他响应。

///

## 组合信息
您还可以联合接收来自多个位置的响应信息，包括 `response_model `、 `status_code` 和 `responses `参数。

您可以使用默认的状态码 `200` （或者您需要的自定义状态码）声明一个 `response_model `，然后直接在OpenAPI模式中在 `responses` 中声明相同响应的其他信息。

**FastAPI**将保留来自 `responses` 的附加信息，并将其与模型中的JSON Schema结合起来。

例如，您可以使用状态码 `404` 声明响应，该响应使用`Pydantic`模型并具有自定义的` description` 。

以及一个状态码为 `200` 的响应，它使用您的 `response_model` ，但包含自定义的 `example` ：

{* ../../docs_src/additional_responses/tutorial003.py hl[20:31] *}

所有这些都将被合并并包含在您的OpenAPI中，并在API文档中显示：

## 联合预定义响应和自定义响应

您可能希望有一些应用于许多路径操作的预定义响应，但是你想将不同的路径和自定义的相应组合在一块。
对于这些情况，你可以使用Python的技术，将 `dict` 与 `**dict_to_unpack` 解包：
```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

这里， new_dict 将包含来自 old_dict 的所有键值对加上新的键值对：
```python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```
您可以使用该技术在路径操作中重用一些预定义的响应，并将它们与其他自定义响应相结合。
**例如：**
{* ../../docs_src/additional_responses/tutorial004.py hl[13:17,26] *}
## 有关OpenAPI响应的更多信息

要了解您可以在响应中包含哪些内容，您可以查看OpenAPI规范中的以下部分：
	+ [OpenAPI响应对象](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responsesObject)，它包括 Response Object 。
	+ [OpenAPI响应对象](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responseObject)，您可以直接在 `responses` 参数中的每个响应中包含任何内容。包括 `description` 、 `headers` 、 `content` （其中是声明不同的媒体类型和JSON Schemas）和 `links` 。
