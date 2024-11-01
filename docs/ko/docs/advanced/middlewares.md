# 고급 미들웨어

메인 튜토리얼에서 [Custom Middleware](../tutorial/middleware.md){.internal-link target=_blank}를 응용프로그램에 추가하는 방법을 읽으셨습니다.

그리고 [CORS with the `CORSMiddleware`](){.internal-link target=_blank}하는 방법도 보셨습니다.

이 섹션에서는 다른 미들웨어들을 사용하는 방법을 알아보겠습니다.

## ASGI 미들웨어 추가하기

**FastAPI**는 Starlette을 기반으로 하고 있으며, <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr> 사양을 구현하므로 ASGI 미들웨어를 사용할 수 있습니다.

미들웨어가 FastAPI나 Starlette용으로 만들어지지 않아도 ASGI 사양을 준수하는 한 동작할 수 있습니다.

일반적으로 ASGI 미들웨어는 첫 번째 인수로 ASGI 앱을 받는 클래스들입니다.

따라서 타사 ASGI 미들웨어 문서에서 일반적으로 다음과 같이 사용하도록 안내할 것입니다.

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

하지만 내부 미들웨어가 서버 오류를 처리하고 사용자 정의 예외 처리기가 제대로 작동하도록 하는 더 간단한 방법을 제공하는 FastAPI(실제로는 Starlette)가 있습니다.

이를 위해 `app.add_middleware()`를 사용합니다(CORS의 예에서와 같이).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()`는 첫 번째 인수로 미들웨어 클래스와 미들웨어에 전달할 추가 인수를 받습니다.

## 통합 미들웨어

**FastAPI**에는 일반적인 사용 사례를 위한 여러 미들웨어가 포함되어 있으며, 사용 방법은 다음에서 살펴보겠습니다.

/// note 참고 | “기술 세부 사항”

다음 예제에서는 `from starlette.middleware.something import SomethingMiddleware`를 사용할 수도 있습니다.

**FastAPI**는 개발자의 편의를 위해 `fastapi.middleware`에 여러 미들웨어를 제공합니다. 그러나 사용 가능한 대부분의 미들웨어는 Starlette에서 직접 제공합니다.

///

## `HTTPSRedirectMiddleware`

들어오는 모든 요청이 `https` 또는 `wss`여야 합니다.

http` 또는 `ws`로 들어오는 모든 요청은 대신 보안 체계로 리디렉션됩니다.