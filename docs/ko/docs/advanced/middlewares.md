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

/// note | 기술 세부 사항

다음 예제에서는 `from starlette.middleware.something import SomethingMiddleware`를 사용할 수도 있습니다.

**FastAPI**는 개발자의 편의를 위해 `fastapi.middleware`에 여러 미들웨어를 제공합니다. 그러나 사용 가능한 대부분의 미들웨어는 Starlette에서 직접 제공합니다.

///

## `HTTPSRedirectMiddleware`

들어오는 모든 요청이 `https` 또는 `wss`여야 합니다.

`http` 또는 `ws`로 들어오는 모든 요청은 대신 보안 체계로 리디렉션됩니다.

{* ../../docs_src/advanced_middleware/tutorial001.py hl[2,6] *}

## `TrustedHostMiddleware`

HTTP 호스트 헤더 공격을 방지하기 위해 모든 수신 요청에 올바르게 설정된 `Host` 헤더를 갖도록 강제합니다.

{* ../../docs_src/advanced_middleware/tutorial002.py hl[2,6:8] *}

다음 인수가 지원됩니다:

* `allowed_hosts` - 호스트 이름으로 허용해야 하는 도메인 이름 목록입니다. 일치하는 하위 도메인에 대해 `*.example.com`과 같은 와일드카드 도메인이 지원됩니다. 모든 호스트 이름을 허용하려면 `allowed_hosts=[“*”]`를 사용하거나 미들웨어를 생략하세요.

수신 요청의 유효성이 올바르게 확인되지 않으면 `400`이라는 응답이 전송됩니다.

## `GZipMiddleware`

`Accept-Encoding` 헤더에 `“gzip”`이 포함된 모든 요청에 대해 GZip 응답을 처리합니다.

미들웨어는 표준 응답과 스트리밍 응답을 모두 처리합니다.

{* ../../docs_src/advanced_middleware/tutorial003.py hl[2,6] *}

지원되는 인수는 다음과 같습니다:

* `minimum_size` - 이 최소 크기(바이트)보다 작은 응답은 GZip하지 않습니다. 기본값은 `500`입니다.
* `compresslevel` - GZip 압축 중에 사용됩니다. 1에서 9 사이의 정수입니다. 기본값은 `9`입니다. 값이 낮을수록 압축 속도는 빨라지지만 파일 크기는 커지고, 값이 높을수록 압축 속도는 느려지지만 파일 크기는 작아집니다.

## 기타 미들웨어

다른 많은 ASGI 미들웨어가 있습니다.

예를 들어:

<a href=“https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py” class=“external-link” target=“_blank”>유비콘의 `ProxyHeadersMiddleware`></a>
<a href=“https://github.com/florimondmanca/msgpack-asgi” class=“external-link” target=“_blank”>MessagePack</a>

사용 가능한 다른 미들웨어를 확인하려면 <a href=“https://www.starlette.dev/middleware/” class=“external-link” target=“_blank”>스타렛의 미들웨어 문서</a> 및 <a href=“https://github.com/florimondmanca/awesome-asgi” class=“external-link” target=“_blank”>ASGI Awesome List</a>를 참조하세요.
