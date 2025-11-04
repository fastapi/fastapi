# 응답 헤더

## `Response` 매개변수 사용하기

여러분은 *경로 작동 함수*에서 `Response` 타입의 매개변수를 선언할 수 있습니다 (쿠키와 같이 사용할 수 있습니다).

그런 다음, 여러분은 해당 *임시* 응답 객체에서 헤더를 설정할 수 있습니다.

{* ../../docs_src/response_headers/tutorial002.py hl[1,7:8] *}

그 후, 일반적으로 사용하듯이 필요한 객체(`dict`, 데이터베이스 모델 등)를 반환할 수 있습니다.

`response_model`을 선언한 경우, 반환한 객체를 필터링하고 변환하는 데 여전히 사용됩니다.

**FastAPI**는 해당 *임시* 응답에서 헤더(쿠키와 상태 코드도 포함)를 추출하여, 여러분이 반환한 값을 포함하는 최종 응답에 `response_model`로 필터링된 값을 넣습니다.

또한, 종속성에서 `Response` 매개변수를 선언하고 그 안에서 헤더(및 쿠키)를 설정할 수 있습니다.

## `Response` 직접 반환하기

`Response`를 직접 반환할 때에도 헤더를 추가할 수 있습니다.

[응답을 직접 반환하기](response-directly.md){.internal-link target=_blank}에서 설명한 대로 응답을 생성하고, 헤더를 추가 매개변수로 전달하세요.

{* ../../docs_src/response_headers/tutorial001.py hl[10:12] *}

/// note | 기술적 세부사항

`from starlette.responses import Response`나 `from starlette.responses import JSONResponse`를 사용할 수도 있습니다.

**FastAPI**는 `starlette.responses`를 `fastapi.responses`로 개발자의 편의를 위해 직접 제공하지만, 대부분의 응답은 Starlette에서 직접 제공됩니다.

그리고 `Response`는 헤더와 쿠키를 설정하는 데 자주 사용될 수 있으므로, **FastAPI**는 `fastapi.Response`로도 이를 제공합니다.

///

## 커스텀 헤더

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">‘X-’ 접두어를 사용하여</a> 커스텀 사설 헤더를 추가할 수 있습니다.

하지만, 여러분이 브라우저에서 클라이언트가 볼 수 있기를 원하는 커스텀 헤더가 있는 경우, CORS 설정에 이를 추가해야 합니다([CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}에서 자세히 알아보세요). `expose_headers` 매개변수를 사용하여 <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette의 CORS 설명서</a>에 문서화된 대로 설정할 수 있습니다.
