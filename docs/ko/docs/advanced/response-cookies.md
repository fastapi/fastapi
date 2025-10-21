# 응답 쿠키

## `Response` 매개변수 사용하기

*경로 작동 함수*에서 `Response` 타입의 매개변수를 선언할 수 있습니다.

그런 다음 해당 *임시* 응답 객체에서 쿠키를 설정할 수 있습니다.

{* ../../docs_src/response_cookies/tutorial002.py hl[1,8:9] *}

그런 다음 필요한 객체(`dict`, 데이터베이스 모델 등)를 반환할 수 있습니다.

그리고 `response_model`을 선언했다면 반환한 객체를 거르고 변환하는 데 여전히 사용됩니다.

**FastAPI**는 그 *임시* 응답에서 쿠키(또한 헤더 및 상태 코드)를 추출하고, 반환된 값이 포함된 최종 응답에 이를 넣습니다. 이 값은 `response_model`로 걸러지게 됩니다.

또한 의존관계에서 `Response` 매개변수를 선언하고, 해당 의존성에서 쿠키(및 헤더)를 설정할 수도 있습니다.

## `Response`를 직접 반환하기

코드에서 `Response`를 직접 반환할 때도 쿠키를 생성할 수 있습니다.

이를 위해 [Response를 직접 반환하기](response-directly.md){.internal-link target=_blank}에서 설명한 대로 응답을 생성할 수 있습니다.

그런 다음 쿠키를 설정하고 반환하면 됩니다:
{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}
/// tip

`Response` 매개변수를 사용하지 않고 응답을 직접 반환하는 경우, FastAPI는 이를 직접 반환한다는 점에 유의하세요.

따라서 데이터가 올바른 유형인지 확인해야 합니다. 예: `JSONResponse`를 반환하는 경우, JSON과 호환되는지 확인하세요.

또한 `response_model`로 걸러져야 할 데이터가 전달되지 않도록 확인하세요.

///

### 추가 정보

/// note | 기술적 세부사항

`from starlette.responses import Response` 또는 `from starlette.responses import JSONResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자의 편의를 위해 `fastapi.responses`로 동일한 `starlette.responses`를 제공합니다. 그러나 대부분의 응답은 Starlette에서 직접 제공됩니다.

또한 `Response`는 헤더와 쿠키를 설정하는 데 자주 사용되므로, **FastAPI**는 이를 `fastapi.Response`로도 제공합니다.

///

사용 가능한 모든 매개변수와 옵션은 <a href="https://www.starlette.dev/responses/#set-cookie" class="external-link" target="_blank">Starlette 문서</a>에서 확인할 수 있습니다.
