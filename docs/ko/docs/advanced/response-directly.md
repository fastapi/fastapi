# 응답을 직접 반환하기

**FastAPI**에서 *경로 작업(path operation)*을 생성할 때, 일반적으로 `dict`, `list`, Pydantic 모델, 데이터베이스 모델 등의 데이터를 반환할 수 있습니다.

기본적으로 **FastAPI**는 [JSON 호환 가능 인코더](../tutorial/encoder.md){.internal-link target=_blank}에 설명된 `jsonable_encoder`를 사용해 해당 반환 값을 자동으로 `JSON`으로 변환합니다.

그런 다음, JSON 호환 데이터(예: `dict`)를 `JSONResponse`에 넣어 사용자의 응답을 전송하는 방식으로 처리됩니다.

그러나 *경로 작업*에서 `JSONResponse`를 직접 반환할 수도 있습니다.

예를 들어, 사용자 정의 헤더나 쿠키를 반환해야 하는 경우에 유용할 수 있습니다.

## `Response` 반환하기

사실, `Response` 또는 그 하위 클래스를 반환할 수 있습니다.

/// tip

`JSONResponse` 자체도 `Response`의 하위 클래스입니다.

///

그리고 `Response`를 반환하면 **FastAPI**가 이를 그대로 전달합니다.

Pydantic 모델로 데이터 변환을 수행하지 않으며, 내용을 다른 형식으로 변환하지 않습니다.

이로 인해 많은 유연성을 얻을 수 있습니다. 어떤 데이터 유형이든 반환할 수 있고, 데이터 선언이나 유효성 검사를 재정의할 수 있습니다.

## `Response`에서 `jsonable_encoder` 사용하기

**FastAPI**는 반환하는 `Response`에 아무런 변환을 하지 않으므로, 그 내용이 준비되어 있어야 합니다.

예를 들어, Pydantic 모델을 `dict`로 변환해 `JSONResponse`에 넣지 않으면 JSON 호환 유형으로 변환된 데이터 유형(예: `datetime`, `UUID` 등)이 사용되지 않습니다.

이러한 경우, 데이터를 응답에 전달하기 전에 `jsonable_encoder`를 사용하여 변환할 수 있습니다:

{* ../../docs_src/response_directly/tutorial001.py hl[6:7,21:22] *}

/// note | 기술적 세부 사항

`from starlette.responses import JSONResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자의 편의를 위해 `starlette.responses`를 `fastapi.responses`로 제공합니다. 그러나 대부분의 가능한 응답은 Starlette에서 직접 제공합니다.

///

## 사용자 정의 `Response` 반환하기
위 예제는 필요한 모든 부분을 보여주지만, 아직 유용하지는 않습니다. 사실 데이터를 직접 반환하면 **FastAPI**가 이를 `JSONResponse`에 넣고 `dict`로 변환하는 등 모든 작업을 자동으로 처리합니다.

이제, 사용자 정의 응답을 반환하는 방법을 알아보겠습니다.

예를 들어 <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a> 응답을 반환하고 싶다고 가정해보겠습니다.

XML 내용을 문자열에 넣고, 이를 `Response`에 넣어 반환할 수 있습니다:

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

## 참고 사항
`Response`를 직접 반환할 때, 그 데이터는 자동으로 유효성 검사되거나, 변환(직렬화)되거나, 문서화되지 않습니다.

그러나 [OpenAPI에서 추가 응답](additional-responses.md){.internal-link target=_blank}에서 설명된 대로 문서화할 수 있습니다.

이후 단락에서 자동 데이터 변환, 문서화 등을 사용하면서 사용자 정의 `Response`를 선언하는 방법을 확인할 수 있습니다.
