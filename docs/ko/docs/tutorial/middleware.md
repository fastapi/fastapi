# 미들웨어

당신은 미들웨어를 **FastAPI** 어플리케이션에 추가할 수 있습니다.

"미들웨어"는 특정 *path operation*에 의해 처리되기 전, 모든 **request**에 대해서 동작하는 함수입니다. 또한 모든 **response**가 반환되기 전에도 동일하게 동작합니다.

* 미들웨어는 당신의 어플리케이션으로 오는 **request**를 가져옵니다.
* **request** 또는 다른 필요한 코드를 실행 시키는 동작을 할 수 있습니다.
* **reqeust**를 전달하여 일부 어플리케이션에서 처리합니다 (일부 *path 작업 *에 의해).
* 어플리케이션에서 생성한 **response**를 받습니다 (일부 *path 작업 *에 의해).
* **response** 또는 다른 필요한 코드를 실행시키는 동작을 할 수 있습니다.
* **response**를 반환합니다. 그런 다음 ** 요청 **을 전달하여 나머지 응용 프로그램에서 처리합니다 (일부 *path 작업 *에 의해).

!!! note "기술 세부사항"
    만약 당신이`yield`를 사용한 의존성을 가지고 있다면, 미들웨어가 실행되고 난 후에 exit이 실행될 것입니다.

    만약 백그라운드 작업이 있다면, 그것들은 모든 미들웨어가 실행되고 나서 실행될 것입니다.

## 미들웨어 작성하기

미들웨어를 작성하기 위해서 당신은 함수 상단에 `@app.middleware("http")` 데코레이터를 사용할 수 있습니다.

미들웨어 함수은 다음 항목들을 받습니다:

* `request`.
* `request`를 파라미터로 받는 `call_next` 함수.
  * 이 함수은 `request`를 해당하는 *path operation*으로 전달합니다.
  * 그런다음, *path operation*에 의해 생성된 `response` 를 반환합니다.
* 당신은 `response`를 반환하기 전에 추가로 `response`를 수정할 수 있습니다.

```Python hl_lines="8-9  11  14"
{!../../../docs_src/middleware/tutorial001.py!}
```

!!! 팁
    사용자 정의 헤더는 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">'X-' 접두사를 사용</a>하여 추가할 수 있습니다.

    그러나 만약 클라이언트의 브라우저에서 볼 수 있는 사용자 정의 헤더를 가지고 있다면, 그것들을 CORS 설정([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank})에 <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette CORS 문서</a>에 명시된 `expose_headers` 파라미터를 이용하여 헤더들을 추가하여야합니다.

!!! note "기술 세부사항"
    당신은 `from starlette.requests import Request`를 사용할 수도 있습니다.

    **FastAPI**는 개발자에게 편의성을 제공합니다. 그러나 Starlette에서 직접 제공됩니다.

### `response`의 전과 후

당신은 *path operation*을 받기 전 `request`와 함께 동작할 수 있는 코드를 추가할 수 있습니다.

그리고 `response` 또한 생성된 후 반환되기 전에 코드를 추가 할 수 있습니다.

예를 들어, 당신은 요청을 수행하고 응답을 생성하는데 까지 걸린 시간 값을 가지고 있는 `X-Process-Time` 같은 커스텀 헤더를 추가할 수 있습니다.

```Python hl_lines="10  12-13"
{!../../../docs_src/middleware/tutorial001.py!}
```

## 그 이외의 미들웨어

당신은 미들웨어 대한 더 많은 정보를 [숙련자 사용 가이드: 향상된 미들웨어](../advanced/middleware.md){.internal-link target=\_blank}에서 읽을 수 있습니다.

다음 섹션에서 당신은 미들웨어를 어떻게 다루는지에 대해 읽을 것입니다.
