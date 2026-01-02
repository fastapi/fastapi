# 미들웨어 { #middleware }

미들웨어를 **FastAPI** 응용 프로그램에 추가할 수 있습니다.

"미들웨어"는 특정 *경로 처리*에 의해 처리되기 전, 모든 **요청**에 대해서 동작하는 함수입니다. 또한 모든 **응답**이 반환되기 전에도 동일하게 동작합니다.

* 미들웨어는 응용 프로그램으로 오는 각 **요청**을 가져옵니다.
* 그런 다음 해당 **요청**에 대해 무언가를 하거나 필요한 코드를 실행할 수 있습니다.
* 그런 다음 **요청**을 나머지 애플리케이션(어떤 *경로 처리*가)을 통해 처리되도록 전달합니다.
* 그런 다음 애플리케이션(어떤 *경로 처리*가)이 생성한 **응답**을 가져옵니다.
* 그런 다음 해당 **응답**에 대해 무언가를 하거나 필요한 코드를 실행할 수 있습니다.
* 그런 다음 **응답**을 반환합니다.

/// note | 기술 세부사항

`yield`를 사용하는 의존성이 있다면, exit 코드는 미들웨어 *후에* 실행됩니다.

백그라운드 작업(뒤에서 보게 될 [Background Tasks](background-tasks.md){.internal-link target=_blank} 섹션에서 다룹니다)이 있다면, 모든 미들웨어 *후에* 실행됩니다.

///

## 미들웨어 만들기 { #create-a-middleware }

미들웨어를 만들기 위해 함수 상단에 데코레이터 `@app.middleware("http")`를 사용합니다.

미들웨어 함수는 다음을 받습니다:

* `request`.
* `request`를 매개변수로 받는 `call_next` 함수.
    * 이 함수는 `request`를 해당하는 *경로 처리*로 전달합니다.
    * 그런 다음 해당 *경로 처리*가 생성한 `response`를 반환합니다.
* 그런 다음 반환하기 전에 `response`를 추가로 수정할 수 있습니다.

{* ../../docs_src/middleware/tutorial001_py39.py hl[8:9,11,14] *}

/// tip | 팁

사용자 정의 독점 헤더는 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">`X-` 접두사를 사용</a>하여 추가할 수 있다는 점을 기억하세요.

하지만 브라우저에서 클라이언트가 볼 수 있게 하려는 사용자 정의 헤더가 있다면, <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette의 CORS 문서</a>에 문서화된 `expose_headers` 매개변수를 사용해 CORS 설정([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank})에 추가해야 합니다.

///

/// note | 기술 세부사항

`from starlette.requests import Request`를 사용할 수도 있습니다.

**FastAPI**는 개발자인 여러분의 편의를 위해 이를 제공합니다. 하지만 이는 Starlette에서 직접 가져온 것입니다.

///

### `response`의 전과 후 { #before-and-after-the-response }

어떤 *경로 처리*가 받기 전에, `request`와 함께 실행될 코드를 추가할 수 있습니다.

또한 `response`가 생성된 후, 반환하기 전에 코드를 추가할 수도 있습니다.

예를 들어, 요청을 처리하고 응답을 생성하는 데 걸린 시간을 초 단위로 담는 사용자 정의 헤더 `X-Process-Time`을 추가할 수 있습니다:

{* ../../docs_src/middleware/tutorial001_py39.py hl[10,12:13] *}

/// tip | 팁

여기서는 이러한 사용 사례에서 더 정확할 수 있기 때문에 `time.time()` 대신 <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a>를 사용합니다. 🤓

///

## 여러 미들웨어 실행 순서 { #multiple-middleware-execution-order }

`@app.middleware()` 데코레이터 또는 `app.add_middleware()` 메서드를 사용해 여러 미들웨어를 추가하면, 새로 추가된 각 미들웨어가 애플리케이션을 감싸 스택을 형성합니다. 마지막에 추가된 미들웨어가 *가장 바깥쪽*이고, 처음에 추가된 미들웨어가 *가장 안쪽*입니다.

요청 경로에서는 *가장 바깥쪽* 미들웨어가 먼저 실행됩니다.

응답 경로에서는 마지막에 실행됩니다.

예를 들어:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

이 경우 실행 순서는 다음과 같습니다:

* **요청**: MiddlewareB → MiddlewareA → route

* **응답**: route → MiddlewareA → MiddlewareB

이러한 스태킹 동작은 미들웨어가 예측 가능하고 제어 가능한 순서로 실행되도록 보장합니다.

## 다른 미들웨어 { #other-middlewares }

다른 미들웨어에 대한 더 많은 정보는 나중에 [숙련된 사용자 안내서: 향상된 미들웨어](../advanced/middleware.md){.internal-link target=_blank}에서 확인할 수 있습니다.

다음 섹션에서 미들웨어로 <abbr title="Cross-Origin Resource Sharing">CORS</abbr>를 처리하는 방법을 보게 될 것입니다.
