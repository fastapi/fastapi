# 추가 상태 코드

기본적으로 **FastAPI**는 응답을 `JSONResponse`를 사용하여 반환하며, *경로 작업(path operation)*에서 반환한 내용을 해당 `JSONResponse` 안에 넣어 반환합니다.

기본 상태 코드 또는 *경로 작업*에서 설정한 상태 코드를 사용합니다.

## 추가 상태 코드

기본 상태 코드와 별도로 추가 상태 코드를 반환하려면 `JSONResponse`와 같이 `Response`를 직접 반환하고 추가 상태 코드를 직접 설정할 수 있습니다.

예를 들어 항목을 업데이트할 수 있는 *경로 작업*이 있고 성공 시 200 “OK”의 HTTP 상태 코드를 반환한다고 가정해 보겠습니다.

하지만 새로운 항목을 허용하기를 원할 것입니다. 항목이 이전에 존재하지 않았다면 이를 생성하고 HTTP 상태 코드 201 "Created"를 반환합니다.

이를 위해서는 `JSONResponse`를 가져와서 원하는 `status_code`를 설정하여 콘텐츠를 직접 반환합니다:

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | 경고

위의 예제처럼 `Response`를 직접 반환하면 바로 반환됩니다.

모델 등과 함께 직렬화되지 않습니다.

원하는 데이터가 있는지, 값이 유효한 JSON인지 확인합니다(`JSONResponse`를 사용하는 경우).

///

/// note | 기술적 세부 정보

`from starlette.responses import JSONResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자 여러분을 위한 편의성으로 `fastapi.responses`와 동일한 `starlette.responses`를 제공합니다. 그러나 사용 가능한 응답의 대부분은 Starlette에서 직접 제공됩니다. `status` 또한 마찬가지입니다.

///

## OpenAPI 및 API 문서

추가 상태 코드와 응답을 직접 반환하는 경우, FastAPI는 반환할 내용을 미리 알 수 있는 방법이 없기 때문에 OpenAPI 스키마(API 문서)에 포함되지 않습니다.

하지만 다음을 사용하여 코드에 이를 문서화할 수 있습니다: [추가 응답](additional-responses.md){.internal-link target=_blank}.
