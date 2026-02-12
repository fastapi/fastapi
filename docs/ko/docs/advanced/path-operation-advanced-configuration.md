# 경로 처리 고급 구성 { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | 경고

OpenAPI “전문가”가 아니라면, 아마 이 내용은 필요하지 않을 것입니다.

///

매개변수 `operation_id`를 사용해 *경로 처리*에 사용할 OpenAPI `operationId`를 설정할 수 있습니다.

각 작업마다 고유하도록 보장해야 합니다.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py39.py hl[6] *}

### *경로 처리 함수* 이름을 operationId로 사용하기 { #using-the-path-operation-function-name-as-the-operationid }

API의 함수 이름을 `operationId`로 사용하고 싶다면, 모든 API를 순회하면서 `APIRoute.name`을 사용해 각 *경로 처리*의 `operation_id`를 덮어쓸 수 있습니다.

모든 *경로 처리*를 추가한 뒤에 수행해야 합니다.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py39.py hl[2, 12:21, 24] *}

/// tip | 팁

`app.openapi()`를 수동으로 호출한다면, 그 전에 `operationId`들을 업데이트해야 합니다.

///

/// warning | 경고

이렇게 할 경우, 각 *경로 처리 함수*의 이름이 고유하도록 보장해야 합니다.

서로 다른 모듈(파이썬 파일)에 있어도 마찬가지입니다.

///

## OpenAPI에서 제외하기 { #exclude-from-openapi }

생성된 OpenAPI 스키마(따라서 자동 문서화 시스템)에서 특정 *경로 처리*를 제외하려면, `include_in_schema` 매개변수를 `False`로 설정하세요:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py39.py hl[6] *}

## docstring에서 고급 설명 가져오기 { #advanced-description-from-docstring }

OpenAPI에 사용할 *경로 처리 함수*의 docstring 줄 수를 제한할 수 있습니다.

`\f`(이스케이프된 "form feed" 문자)를 추가하면 **FastAPI**는 이 지점에서 OpenAPI에 사용할 출력 내용을 잘라냅니다.

문서에는 표시되지 않지만, Sphinx 같은 다른 도구는 나머지 부분을 사용할 수 있습니다.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## 추가 응답 { #additional-responses }

*경로 처리*에 대해 `response_model`과 `status_code`를 선언하는 방법을 이미 보셨을 것입니다.

이는 *경로 처리*의 기본 응답에 대한 메타데이터를 정의합니다.

모델, 상태 코드 등과 함께 추가 응답도 선언할 수 있습니다.

이에 대한 문서의 전체 장이 있으니, [OpenAPI의 추가 응답](additional-responses.md){.internal-link target=_blank}에서 읽어보세요.

## OpenAPI Extra { #openapi-extra }

애플리케이션에서 *경로 처리*를 선언하면, **FastAPI**는 OpenAPI 스키마에 포함될 해당 *경로 처리*의 관련 메타데이터를 자동으로 생성합니다.

/// note | 기술 세부사항

OpenAPI 명세에서는 이를 <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operation Object</a>라고 부릅니다.

///

여기에는 *경로 처리*에 대한 모든 정보가 있으며, 자동 문서를 생성하는 데 사용됩니다.

`tags`, `parameters`, `requestBody`, `responses` 등이 포함됩니다.

이 *경로 처리* 전용 OpenAPI 스키마는 보통 **FastAPI**가 자동으로 생성하지만, 확장할 수도 있습니다.

/// tip | 팁

이는 저수준 확장 지점입니다.

추가 응답만 선언하면 된다면, 더 편리한 방법은 [OpenAPI의 추가 응답](additional-responses.md){.internal-link target=_blank}을 사용하는 것입니다.

///

`openapi_extra` 매개변수를 사용해 *경로 처리*의 OpenAPI 스키마를 확장할 수 있습니다.

### OpenAPI 확장 { #openapi-extensions }

예를 들어 `openapi_extra`는 [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions)를 선언하는 데 도움이 될 수 있습니다:

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py39.py hl[6] *}

자동 API 문서를 열면, 해당 특정 *경로 처리*의 하단에 확장이 표시됩니다.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

또한 API의 `/openapi.json`에서 결과 OpenAPI를 보면, 특정 *경로 처리*의 일부로 확장이 포함된 것도 확인할 수 있습니다:

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

### 사용자 정의 OpenAPI *경로 처리* 스키마 { #custom-openapi-path-operation-schema }

`openapi_extra`의 딕셔너리는 *경로 처리*에 대해 자동으로 생성된 OpenAPI 스키마와 깊게 병합됩니다.

따라서 자동 생성된 스키마에 추가 데이터를 더할 수 있습니다.

예를 들어 Pydantic과 함께 FastAPI의 자동 기능을 사용하지 않고, 자체 코드로 요청을 읽고 검증하기로 결정할 수도 있지만, OpenAPI 스키마에는 여전히 그 요청을 정의하고 싶을 수 있습니다.

그럴 때 `openapi_extra`를 사용할 수 있습니다:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py39.py hl[19:36, 39:40] *}

이 예시에서는 어떤 Pydantic 모델도 선언하지 않았습니다. 사실 요청 바디는 JSON으로 <abbr title="converted from some plain format, like bytes, into Python objects - bytes 같은 일반 형식에서 Python 객체로 변환">parsed</abbr>되지도 않고, `bytes`로 직접 읽습니다. 그리고 함수 `magic_data_reader()`가 어떤 방식으로든 이를 파싱하는 역할을 담당합니다.

그럼에도 불구하고, 요청 바디에 대해 기대하는 스키마를 선언할 수 있습니다.

### 사용자 정의 OpenAPI 콘텐츠 타입 { #custom-openapi-content-type }

같은 트릭을 사용하면, Pydantic 모델을 이용해 JSON Schema를 정의하고 이를 *경로 처리*의 사용자 정의 OpenAPI 스키마 섹션에 포함시킬 수 있습니다.

요청의 데이터 타입이 JSON이 아니더라도 이렇게 할 수 있습니다.

예를 들어 이 애플리케이션에서는 Pydantic 모델에서 JSON Schema를 추출하는 FastAPI의 통합 기능도, JSON에 대한 자동 검증도 사용하지 않습니다. 실제로 요청 콘텐츠 타입을 JSON이 아니라 YAML로 선언합니다:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[15:20, 22] *}

그럼에도 기본 통합 기능을 사용하지 않더라도, YAML로 받고자 하는 데이터에 대한 JSON Schema를 수동으로 생성하기 위해 Pydantic 모델을 여전히 사용합니다.

그 다음 요청을 직접 사용하고, 바디를 `bytes`로 추출합니다. 이는 FastAPI가 요청 페이로드를 JSON으로 파싱하려고 시도조차 하지 않는다는 뜻입니다.

그리고 코드에서 YAML 콘텐츠를 직접 파싱한 뒤, 다시 같은 Pydantic 모델을 사용해 YAML 콘텐츠를 검증합니다:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[24:31] *}

/// tip | 팁

여기서는 같은 Pydantic 모델을 재사용합니다.

하지만 마찬가지로, 다른 방식으로 검증할 수도 있습니다.

///
