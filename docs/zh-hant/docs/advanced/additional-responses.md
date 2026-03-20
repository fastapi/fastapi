# OpenAPI 中的額外回應 { #additional-responses-in-openapi }

/// warning | 警告

這是一個偏進階的主題。

如果你剛開始使用 **FastAPI**，大多情況下不需要用到它。

///

你可以宣告額外的回應，包含額外的狀態碼、媒體型別、描述等。

這些額外回應會被包含在 OpenAPI 中，因此也會顯示在 API 文件裡。

但對於這些額外回應，你必須直接回傳像 `JSONResponse` 這樣的 `Response`，並包含你的狀態碼與內容。

## 使用 `model` 的額外回應 { #additional-response-with-model }

你可以在你的「路徑操作裝飾器」中傳入參數 `responses`。

它接收一個 `dict`：鍵是各回應的狀態碼（例如 `200`），值是另一個 `dict`，其中包含每個回應的資訊。

每個回應的 `dict` 都可以有一個鍵 `model`，包含一個 Pydantic 模型，與 `response_model` 類似。

**FastAPI** 會取用該模型、產生其 JSON Schema，並把它放到 OpenAPI 中正確的位置。

例如，要宣告一個狀態碼為 `404` 的額外回應，並使用 Pydantic 模型 `Message`，你可以這樣寫：

{* ../../docs_src/additional_responses/tutorial001_py310.py hl[18,22] *}

/// note | 注意

請記住你必須直接回傳 `JSONResponse`。

///

/// info | 說明

`model` 這個鍵不屬於 OpenAPI。

**FastAPI** 會從這裡取出 Pydantic 模型，產生 JSON Schema，並放到正確位置。

正確的位置是：

* 在 `content` 這個鍵中，其值是一個 JSON 物件（`dict`），包含：
    * 一個媒體型別作為鍵，例如 `application/json`，其值是另一個 JSON 物件，當中包含：
        * 鍵 `schema`，其值是該模型的 JSON Schema，這裡就是正確的位置。
            * **FastAPI** 會在這裡加入一個指向你 OpenAPI 中全域 JSON Schemas 的參照，而不是直接把它嵌入。如此一來，其他應用與用戶端可以直接使用那些 JSON Schemas，提供更好的程式碼產生工具等。

///

這個路徑操作在 OpenAPI 中產生的回應將會是：

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

這些 Schemas 會在 OpenAPI 中以參照的方式指向其他位置：

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

## 主回應的其他媒體型別 { #additional-media-types-for-the-main-response }

你可以用同一個 `responses` 參數，替相同的主回應新增不同的媒體型別。

例如，你可以新增 `image/png` 這種媒體型別，宣告你的「路徑操作」可以回傳 JSON 物件（媒體型別為 `application/json`）或一張 PNG 圖片：

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | 注意

請注意你必須直接用 `FileResponse` 回傳圖片。

///

/// info | 說明

除非你在 `responses` 參數中明確指定不同的媒體型別，否則 FastAPI 會假設回應的媒體型別與主回應類別相同（預設為 `application/json`）。

但如果你指定了一個自訂的回應類別，且其媒體型別為 `None`，那麼對於任何具關聯模型的額外回應，FastAPI 會使用 `application/json`。

///

## 結合資訊 { #combining-information }

你也可以從多個地方結合回應資訊，包括 `response_model`、`status_code` 與 `responses` 參數。

你可以宣告一個 `response_model`，使用預設狀態碼 `200`（或你需要的自訂狀態碼），然後在 `responses` 中直接於 OpenAPI Schema 為相同的回應宣告額外資訊。

**FastAPI** 會保留 `responses` 提供的額外資訊，並把它和你模型的 JSON Schema 結合。

例如，你可以宣告一個狀態碼為 `404` 的回應，使用一個 Pydantic 模型，並帶有自訂的 `description`。

以及一個狀態碼為 `200` 的回應，使用你的 `response_model`，但包含自訂的 `example`：

{* ../../docs_src/additional_responses/tutorial003_py310.py hl[20:31] *}

以上都會被結合並包含在你的 OpenAPI 中，並顯示在 API 文件：

<img src="/img/tutorial/additional-responses/image01.png">

## 結合預先定義與自訂的回應 { #combine-predefined-responses-and-custom-ones }

你可能想要有一些適用於多個「路徑操作」的預先定義回應，但也想與每個「路徑操作」所需的自訂回應結合。

在這些情況下，你可以使用 Python 的「解包」`dict` 技巧，透過 `**dict_to_unpack`：

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

此處，`new_dict` 會包含 `old_dict` 的所有鍵值配對，再加上新的鍵值配對：

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

你可以用這個技巧在「路徑操作」中重用一些預先定義的回應，並與其他自訂回應結合。

例如：

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## 關於 OpenAPI 回應的更多資訊 { #more-information-about-openapi-responses }

若要查看回應中究竟可以包含哪些內容，你可以參考 OpenAPI 規範中的這些章節：

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses 物件</a>，其中包含 `Response Object`。
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response 物件</a>，你可以把這裡的任何內容直接放到 `responses` 參數內各個回應中。包含 `description`、`headers`、`content`（在其中宣告不同的媒體型別與 JSON Schemas）、以及 `links`。
