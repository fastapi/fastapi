# 경로 작동 설정

*경로 작동 데코레이터*를 설정하기 위해서 전달할수 있는 몇 가지 매개변수가 있습니다.

/// warning | 경고

아래 매개변수들은 *경로 작동 함수*가 아닌 *경로 작동 데코레이터*에 직접 전달된다는 사실을 기억하십시오.

///

## 응답 상태 코드

*경로 작동*의 응답에 사용될 (HTTP) `status_code`를 정의할수 있습니다.

`404`와 같은 `int`형 코드를 직접 전달할수 있습니다.

하지만 각 코드의 의미를 모른다면, `status`에 있는 단축 상수들을 사용할수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial001.py hl[3,17] *}

각 상태 코드들은 응답에 사용되며, OpenAPI 스키마에 추가됩니다.

/// note | 기술적 세부사항

다음과 같이 임포트하셔도 좋습니다. `from starlette import status`.

**FastAPI**는 개발자 여러분의 편의를 위해서 `starlette.status`와 동일한 `fastapi.status`를 제공합니다. 하지만 Starlette에서 직접 온 것입니다.

///

## 태그

(보통 단일 `str`인) `str`로 구성된 `list`와 함께 매개변수 `tags`를 전달하여, `경로 작동`에 태그를 추가할 수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial002.py hl[17,22,27] *}

전달된 태그들은 OpenAPI의 스키마에 추가되며, 자동 문서 인터페이스에서 사용됩니다:

<img src="/img/tutorial/path-operation-configuration/image01.png">

## 요약과 기술

`summary`와 `description`을 추가할 수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial003.py hl[20:21] *}

## 독스트링으로 만든 기술

설명은 보통 길어지고 여러 줄에 걸쳐있기 때문에, *경로 작동* 기술을 함수 <abbr title="함수안에 있는 첫번째 표현식으로, 문서로 사용될 여러 줄에 걸친 (변수에 할당되지 않은) 문자열"> 독스트링</abbr> 에 선언할 수 있습니다, 이를 **FastAPI**가 독스트링으로부터 읽습니다.

<a href="https://ko.wikipedia.org/wiki/%EB%A7%88%ED%81%AC%EB%8B%A4%EC%9A%B4" class="external-link" target="_blank">마크다운</a> 문법으로 독스트링을 작성할 수 있습니다, 작성된 마크다운 형식의 독스트링은 (마크다운의 들여쓰기를 고려하여) 올바르게 화면에 출력됩니다.

{* ../../docs_src/path_operation_configuration/tutorial004.py hl[19:27] *}

이는 대화형 문서에서 사용됩니다:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## 응답 기술

`response_description` 매개변수로 응답에 관한 설명을 명시할 수 있습니다:

{* ../../docs_src/path_operation_configuration/tutorial005.py hl[21] *}

/// info | 정보

`response_description`은 구체적으로 응답을 지칭하며, `description`은 일반적인 *경로 작동*을 지칭합니다.

///

/// check | 확인

OpenAPI는 각 *경로 작동*이 응답에 관한 설명을 요구할 것을 명시합니다.

따라서, 응답에 관한 설명이 없을경우, **FastAPI**가 자동으로 "성공 응답" 중 하나를 생성합니다.

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## 단일 *경로 작동* 지원중단

단일 *경로 작동*을 없애지 않고 <abbr title="구식, 사용하지 않는것이 권장됨">지원중단</abbr>을 해야한다면, `deprecated` 매개변수를 전달하면 됩니다.

{* ../../docs_src/path_operation_configuration/tutorial006.py hl[16] *}

대화형 문서에 지원중단이라고 표시됩니다.

<img src="/img/tutorial/path-operation-configuration/image04.png">

지원중단된 경우와 지원중단 되지 않은 경우에 대한 *경로 작동*이 어떻게 보이는 지 확인하십시오.

<img src="/img/tutorial/path-operation-configuration/image05.png">

## 정리

*경로 작동 데코레이터*에 매개변수(들)를 전달함으로 *경로 작동*을 설정하고 메타데이터를 추가할수 있습니다.
