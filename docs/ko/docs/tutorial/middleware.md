# 미들웨어

미들웨어를 **FastAPI** 응용 프로그램에 추가할 수 있습니다.

"미들웨어"는 특정 *경로 작동*에 의해 처리되기 전, 모든 **요청**에 대해서 동작하는 함수입니다. 또한 모든 **응답**이 반환되기 전에도 동일하게 동작합니다.

* 미들웨어는 응용 프로그램으로 오는 **요청**를 가져옵니다.
* **요청** 또는 다른 필요한 코드를 실행 시킬 수 있습니다.
* **요청**을 응용 프로그램의 *경로 작동*으로 전달하여 처리합니다.
* 애플리케이션의 *경로 작업*에서 생성한 **응답**를 받습니다.
* **응답** 또는 다른 필요한 코드를 실행시키는 동작을 할 수 있습니다.
* **응답**를 반환합니다.

/// note | 기술 세부사항

만약 `yield`를 사용한 의존성을 가지고 있다면, 미들웨어가 실행되고 난 후에 exit이 실행됩니다.

만약 (나중에 문서에서 다룰) 백그라운드 작업이 있다면, 모든 미들웨어가 실행되고 *난 후에* 실행됩니다.

///

## 미들웨어 만들기

미들웨어를 작성하기 위해서 함수 상단에 `@app.middleware("http")` 데코레이터를 사용할 수 있습니다.

미들웨어 함수는 다음 항목들을 받습니다:

* `request`.
* `request`를 매개변수로 받는 `call_next` 함수.
    * 이 함수는 `request`를 해당하는 *경로 작업*으로 전달합니다.
    * 그런 다음, *경로 작업*에 의해 생성된 `response` 를 반환합니다.
* `response`를 반환하기 전에 추가로 `response`를 수정할 수 있습니다.

{* ../../docs_src/middleware/tutorial001.py hl[8:9,11,14] *}

/// tip | 팁

사용자 정의 헤더는 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">'X-' 접두사를 사용</a>하여 추가할 수 있습니다.

그러나 만약 클라이언트의 브라우저에서 볼 수 있는 사용자 정의 헤더를 가지고 있다면, 그것들을 CORS 설정([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank})에 <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette CORS 문서</a>에 명시된 `expose_headers` 매개변수를 이용하여 헤더들을 추가하여야합니다.

///

/// note | 기술적 세부사항

`from starlette.requests import request`를 사용할 수도 있습니다.

**FastAPI**는 개발자에게 편의를 위해 이를 제공합니다. 그러나 Starlette에서 직접 파생되었습니다.

///

### `response`의 전과 후

*경로 작동*을 받기 전 `request`와 함께 작동할 수 있는 코드를 추가할 수 있습니다.

그리고 `response` 또한 생성된 후 반환되기 전에 코드를 추가 할 수 있습니다.

예를 들어, 요청을 수행하고 응답을 생성하는데 까지 걸린 시간 값을 가지고 있는 `X-Process-Time` 같은 사용자 정의 헤더를 추가할 수 있습니다.

{* ../../docs_src/middleware/tutorial001.py hl[10,12:13] *}

## 다른 미들웨어

미들웨어에 대한 더 많은 정보는 [숙련된 사용자 안내서: 향상된 미들웨어](../advanced/middleware.md){.internal-link target=\_blank}에서 확인할 수 있습니다.

다음 부분에서 미들웨어와 함께 <abbr title="교차-출처 리소스 공유">CORS</abbr>를 어떻게 다루는지에 대해 확인할 것입니다.
