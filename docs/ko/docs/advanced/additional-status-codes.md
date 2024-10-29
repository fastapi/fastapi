# 추가 상태 코드

기본적으로 **FastAPI**는 *경로 작업*에서 반환하는 내용을 `JSONResponse`로 응답하여 그 안에 콘텐츠를 포함해 반환합니다.

FastAPI는 기본 상태 코드 또는 *경로 작업*에서 설정한 상태 코드를 사용합니다.

## 추가 상태 코드

주요 상태 코드 외에 다른 상태 코드도 반환하고자 할 경우, `JSONResponse`와 같은 `Response`를 직접 반환하여 추가 상태 코드를 설정할 수 있습니다.

예를 들어, 항목을 업데이트할 수 있는 *경로 작업*을 설정하여 성공 시 `200 "OK"` 상태 코드를 반환하려고 합니다.

또한, 항목이 기존에 없을 때 새로운 항목을 생성하고, HTTP 상태 코드 `201 "Created"`를 반환하도록 할 수 있습니다.

이를 위해 `JSONResponse`를 임포트하고, 원하는 `status_code`를 설정하여 직접 콘텐츠를 반환합니다.

//// tab | Python 3.10+

```Python hl_lines="4  25"
{!> ../../docs_src/additional_status_codes/tutorial001_an_py310.py!}

////

//// tab | Python 3.9+

```Python hl_lines="4  25"
{!> ../../docs_src/additional_status_codes/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="4  26"
{!> ../../docs_src/additional_status_codes/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python hl_lines="2  23"
{!> ../../docs_src/additional_status_codes/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.
///

```Python hl_lines="4  25"
{!> ../../docs_src/additional_status_codes/tutorial001.py!}
```

////

/// 경고

위 예제와 같이 `Response` 를 직접 반환할 경우, 그대로 반환됩니다.

모델로 직렬화되지 않습니다.

응답 데이터가 JSON 형식이며 유효한 값이 포함되어 있는지 확인하십시오.
(`JSONResponse` 를 사용하는 경우)

///

/// note | "기술적 세부 사항"

`from starlette.responses import JSONResponse` 를 사용할 수도 있습니다.

**FastAPI** 편의를 위해 `starlette.responses` 의 같은 응답을 `fastapi.responses` 에서도 제공합니다. 그러나 대부분의 응답은 Starlette에서 직접 가져옵니다. `status` 도 동일합니다.

///

## OpenAPI 및 API 문서

추가 상태 코드와 응답을 직접 반환하면 OpenAPI (API 문서)에 포함되지 않습니다. FastAPI는 미리 반환할 내용을 파악할 방법이 없기 때문입니다.

그러나 코드에서 [추가응답](additional-responses.md){.internal-link target=_blank}을 사용해 문서화할 수 있습니다.
