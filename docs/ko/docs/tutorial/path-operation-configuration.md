# 경로 처리 설정 { #path-operation-configuration }

*경로 처리 데코레이터*를 설정하기 위해 전달할 수 있는 몇 가지 매개변수가 있습니다.

/// warning | 경고

아래 매개변수들은 *경로 처리 함수*가 아닌 *경로 처리 데코레이터*에 직접 전달된다는 사실을 기억하세요.

///

## 응답 상태 코드 { #response-status-code }

*경로 처리*의 응답에 사용될 (HTTP) `status_code`를 정의할 수 있습니다.

`404`와 같은 `int`형 코드를 직접 전달할 수 있습니다.

하지만 각 숫자 코드가 무엇을 의미하는지 기억하지 못한다면, `status`에 있는 단축 상수들을 사용할 수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

해당 상태 코드는 응답에 사용되며, OpenAPI 스키마에 추가됩니다.

/// note | 기술 세부사항

다음과 같이 임포트하셔도 좋습니다. `from starlette import status`.

**FastAPI**는 개발자 여러분의 편의를 위해 `starlette.status`와 동일한 `fastapi.status`를 제공합니다. 하지만 이는 Starlette에서 직접 온 것입니다.

///

## 태그 { #tags }

(보통 단일 `str`인) `str`로 구성된 `list`와 함께 매개변수 `tags`를 전달하여, *경로 처리*에 태그를 추가할 수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

전달된 태그들은 OpenAPI의 스키마에 추가되며, 자동 문서 인터페이스에서 사용됩니다:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Enum을 사용한 태그 { #tags-with-enums }

큰 애플리케이션이 있다면, **여러 태그**가 쌓이게 될 수 있고, 관련된 *경로 처리*에 항상 **같은 태그**를 사용하는지 확인하고 싶을 것입니다.

이런 경우에는 태그를 `Enum`에 저장하는 것이 합리적일 수 있습니다.

**FastAPI**는 일반 문자열과 동일한 방식으로 이를 지원합니다:

{* ../../docs_src/path_operation_configuration/tutorial002b_py39.py hl[1,8:10,13,18] *}

## 요약과 설명 { #summary-and-description }

`summary`와 `description`을 추가할 수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[18:19] *}

## 독스트링으로 만든 설명 { #description-from-docstring }

설명은 보통 길어지고 여러 줄에 걸쳐있기 때문에, *경로 처리* 설명을 함수 <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation – 문서화에 사용되는 함수 내부 첫 표현식의 여러 줄 문자열(어떤 변수에도 할당되지 않음)">docstring</abbr>에 선언할 수 있으며, **FastAPI**는 그곳에서 이를 읽습니다.

독스트링에는 <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a>을 작성할 수 있으며, (독스트링의 들여쓰기를 고려하여) 올바르게 해석되고 표시됩니다.

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

이는 대화형 문서에서 사용됩니다:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## 응답 설명 { #response-description }

`response_description` 매개변수로 응답에 관한 설명을 명시할 수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[19] *}

/// info | 정보

`response_description`은 구체적으로 응답을 지칭하며, `description`은 일반적인 *경로 처리*를 지칭합니다.

///

/// check | 확인

OpenAPI는 각 *경로 처리*가 응답에 관한 설명을 요구할 것을 명시합니다.

따라서, 응답에 관한 설명을 제공하지 않으면, **FastAPI**가 "Successful response" 중 하나를 자동으로 생성합니다.

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## *경로 처리* 지원중단하기 { #deprecate-a-path-operation }

*경로 처리*를 제거하지 않고 <abbr title="obsolete, recommended not to use it – 구식이며 사용하지 않는 것이 권장됨">deprecated</abbr>로 표시해야 한다면, `deprecated` 매개변수를 전달하면 됩니다:

{* ../../docs_src/path_operation_configuration/tutorial006_py39.py hl[16] *}

대화형 문서에서 지원중단으로 명확하게 표시됩니다:

<img src="/img/tutorial/path-operation-configuration/image04.png">

지원중단된 *경로 처리*와 지원중단되지 않은 *경로 처리*가 어떻게 보이는지 확인해 보세요:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## 정리 { #recap }

*경로 처리 데코레이터*에 매개변수(들)를 전달하여 *경로 처리*를 설정하고 메타데이터를 쉽게 추가할 수 있습니다.
