# OpenAPI에서 추가 응답 { #additional-responses-in-openapi }

/// warning | 경고

이는 꽤 고급 주제입니다.

**FastAPI**를 막 시작했다면, 이 내용이 필요 없을 수도 있습니다.

///

추가 상태 코드, 미디어 타입, 설명 등을 포함한 추가 응답을 선언할 수 있습니다.

이러한 추가 응답은 OpenAPI 스키마에 포함되므로 API 문서에도 표시됩니다.

하지만 이러한 추가 응답의 경우, 상태 코드와 콘텐츠를 포함하여 `JSONResponse` 같은 `Response`를 직접 반환하도록 반드시 처리해야 합니다.

## `model`을 사용한 추가 응답 { #additional-response-with-model }

*경로 처리 데코레이터*에 `responses` 파라미터를 전달할 수 있습니다.

이는 `dict`를 받습니다. 키는 각 응답의 상태 코드(예: `200`)이고, 값은 각 응답에 대한 정보를 담은 다른 `dict`입니다.

각 응답 `dict`에는 `response_model`처럼 Pydantic 모델을 담는 `model` 키가 있을 수 있습니다.

**FastAPI**는 그 모델을 사용해 JSON Schema를 생성하고, OpenAPI의 올바른 위치에 포함합니다.

예를 들어, 상태 코드 `404`와 Pydantic 모델 `Message`를 사용하는 다른 응답을 선언하려면 다음과 같이 작성할 수 있습니다:

{* ../../docs_src/additional_responses/tutorial001_py39.py hl[18,22] *}

/// note | 참고

`JSONResponse`를 직접 반환해야 한다는 점을 기억하세요.

///

/// info | 정보

`model` 키는 OpenAPI의 일부가 아닙니다.

**FastAPI**는 여기에서 Pydantic 모델을 가져와 JSON Schema를 생성하고 올바른 위치에 넣습니다.

올바른 위치는 다음과 같습니다:

* 값으로 또 다른 JSON 객체(`dict`)를 가지는 `content` 키 안에:
    * 미디어 타입(예: `application/json`)을 키로 가지며, 값으로 또 다른 JSON 객체를 포함하고:
        * `schema` 키가 있고, 그 값이 모델에서 생성된 JSON Schema입니다. 이것이 올바른 위치입니다.
            * **FastAPI**는 이를 직접 포함하는 대신, OpenAPI의 다른 위치에 있는 전역 JSON Schemas를 참조하도록 여기에서 reference를 추가합니다. 이렇게 하면 다른 애플리케이션과 클라이언트가 그 JSON Schema를 직접 사용할 수 있고, 더 나은 코드 생성 도구 등을 제공할 수 있습니다.

///

이 *경로 처리*에 대해 OpenAPI에 생성되는 응답은 다음과 같습니다:

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

스키마는 OpenAPI 스키마 내부의 다른 위치를 참조합니다:

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

## 주요 응답에 대한 추가 미디어 타입 { #additional-media-types-for-the-main-response }

같은 `responses` 파라미터를 사용해 동일한 주요 응답에 대해 다른 미디어 타입을 추가할 수도 있습니다.

예를 들어, *경로 처리*가 JSON 객체(미디어 타입 `application/json`) 또는 PNG 이미지(미디어 타입 `image/png`)를 반환할 수 있다고 선언하기 위해 `image/png`라는 추가 미디어 타입을 추가할 수 있습니다:

{* ../../docs_src/additional_responses/tutorial002_py310.py hl[17:22,26] *}

/// note | 참고

이미지는 `FileResponse`를 사용해 직접 반환해야 한다는 점에 유의하세요.

///

/// info | 정보

`responses` 파라미터에서 다른 미디어 타입을 명시적으로 지정하지 않는 한, FastAPI는 응답이 주요 응답 클래스와 동일한 미디어 타입(기본값 `application/json`)을 가진다고 가정합니다.

하지만 커스텀 응답 클래스를 지정하면서 미디어 타입을 `None`으로 설정했다면, FastAPI는 연결된 모델이 있는 모든 추가 응답에 대해 `application/json`을 사용합니다.

///

## 정보 결합하기 { #combining-information }

`response_model`, `status_code`, `responses` 파라미터를 포함해 여러 위치의 응답 정보를 결합할 수도 있습니다.

기본 상태 코드 `200`(또는 필요하다면 커스텀 코드)을 사용하여 `response_model`을 선언하고, 그와 동일한 응답에 대한 추가 정보를 `responses`에서 OpenAPI 스키마에 직접 선언할 수 있습니다.

**FastAPI**는 `responses`의 추가 정보를 유지하고, 모델의 JSON Schema와 결합합니다.

예를 들어, Pydantic 모델을 사용하고 커스텀 `description`을 가진 상태 코드 `404` 응답을 선언할 수 있습니다.

또한 `response_model`을 사용하는 상태 코드 `200` 응답을 선언하되, 커스텀 `example`을 포함할 수도 있습니다:

{* ../../docs_src/additional_responses/tutorial003_py39.py hl[20:31] *}

이 모든 내용은 OpenAPI에 결합되어 포함되고, API 문서에 표시됩니다:

<img src="/img/tutorial/additional-responses/image01.png">

## 미리 정의된 응답과 커스텀 응답 결합하기 { #combine-predefined-responses-and-custom-ones }

여러 *경로 처리*에 적용되는 미리 정의된 응답이 필요할 수도 있지만, 각 *경로 처리*마다 필요한 커스텀 응답과 결합하고 싶을 수도 있습니다.

그런 경우 Python의 `dict` “unpacking” 기법인 `**dict_to_unpack`을 사용할 수 있습니다:

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

여기서 `new_dict`는 `old_dict`의 모든 키-값 쌍에 더해 새 키-값 쌍까지 포함합니다:

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

이 기법을 사용해 *경로 처리*에서 일부 미리 정의된 응답을 재사용하고, 추가 커스텀 응답과 결합할 수 있습니다.

예를 들어:

{* ../../docs_src/additional_responses/tutorial004_py310.py hl[11:15,24] *}

## OpenAPI 응답에 대한 추가 정보 { #more-information-about-openapi-responses }

응답에 정확히 무엇을 포함할 수 있는지 보려면, OpenAPI 사양의 다음 섹션을 확인하세요:

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object" class="external-link" target="_blank">OpenAPI Responses Object</a>: `Response Object`를 포함합니다.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object" class="external-link" target="_blank">OpenAPI Response Object</a>: `responses` 파라미터 안의 각 응답에 이것의 어떤 항목이든 직접 포함할 수 있습니다. `description`, `headers`, `content`(여기에서 서로 다른 미디어 타입과 JSON Schema를 선언합니다), `links` 등을 포함할 수 있습니다.
