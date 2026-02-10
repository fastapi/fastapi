# 고급 Middleware { #advanced-middleware }

메인 튜토리얼에서 애플리케이션에 [커스텀 Middleware](../tutorial/middleware.md){.internal-link target=_blank}를 추가하는 방법을 읽었습니다.

그리고 [`CORSMiddleware`로 CORS 처리하기](../tutorial/cors.md){.internal-link target=_blank}도 읽었습니다.

이 섹션에서는 다른 middleware들을 사용하는 방법을 살펴보겠습니다.

## ASGI middleware 추가하기 { #adding-asgi-middlewares }

**FastAPI**는 Starlette를 기반으로 하고 <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr> 사양을 구현하므로, 어떤 ASGI middleware든 사용할 수 있습니다.

ASGI 사양을 따르기만 하면, FastAPI나 Starlette를 위해 만들어진 middleware가 아니어도 동작합니다.

일반적으로 ASGI middleware는 첫 번째 인자로 ASGI 앱을 받도록 기대하는 클래스입니다.

그래서 서드파티 ASGI middleware 문서에서는 아마 다음과 같이 하라고 안내할 것입니다:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

하지만 FastAPI(정확히는 Starlette)는 더 간단한 방법을 제공하며, 이를 통해 내부 middleware가 서버 오류를 처리하고 커스텀 예외 핸들러가 올바르게 동작하도록 보장합니다.

이를 위해(그리고 CORS 예제에서처럼) `app.add_middleware()`를 사용합니다.

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()`는 첫 번째 인자로 middleware 클래스를 받고, 그 뒤에는 middleware에 전달할 추가 인자들을 받습니다.

## 통합 middleware { #integrated-middlewares }

**FastAPI**에는 일반적인 사용 사례를 위한 여러 middleware가 포함되어 있습니다. 다음에서 이를 사용하는 방법을 살펴보겠습니다.

/// note | 기술 세부사항

다음 예제에서는 `from starlette.middleware.something import SomethingMiddleware`를 사용해도 됩니다.

**FastAPI**는 개발자 편의를 위해 `fastapi.middleware`에 여러 middleware를 제공하지만, 사용 가능한 대부분의 middleware는 Starlette에서 직접 제공됩니다.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

들어오는 모든 요청이 `https` 또는 `wss`여야 하도록 강제합니다.

`http` 또는 `ws`로 들어오는 모든 요청은 대신 보안 스킴으로 리디렉션됩니다.

{* ../../docs_src/advanced_middleware/tutorial001_py39.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

HTTP Host Header 공격을 방어하기 위해, 들어오는 모든 요청에 올바르게 설정된 `Host` 헤더가 있어야 하도록 강제합니다.

{* ../../docs_src/advanced_middleware/tutorial002_py39.py hl[2,6:8] *}

다음 인자들을 지원합니다:

* `allowed_hosts` - 호스트명으로 허용할 도메인 이름 목록입니다. `*.example.com` 같은 와일드카드 도메인으로 서브도메인을 매칭하는 것도 지원합니다. 어떤 호스트명이든 허용하려면 `allowed_hosts=["*"]`를 사용하거나 middleware를 생략하세요.
* `www_redirect` - True로 설정하면, 허용된 호스트의 non-www 버전으로 들어오는 요청을 www 버전으로 리디렉션합니다. 기본값은 `True`입니다.

들어오는 요청이 올바르게 검증되지 않으면 `400` 응답이 전송됩니다.

## `GZipMiddleware` { #gzipmiddleware }

`Accept-Encoding` 헤더에 `"gzip"`이 포함된 어떤 요청이든 GZip 응답을 처리합니다.

이 middleware는 일반 응답과 스트리밍 응답을 모두 처리합니다.

{* ../../docs_src/advanced_middleware/tutorial003_py39.py hl[2,6] *}

다음 인자들을 지원합니다:

* `minimum_size` - 바이트 단위로 지정한 최소 크기보다 작은 응답은 GZip으로 압축하지 않습니다. 기본값은 `500`입니다.
* `compresslevel` - GZip 압축 중에 사용됩니다. 1부터 9까지의 정수입니다. 기본값은 `9`입니다. 값이 낮을수록 압축은 더 빠르지만 파일 크기는 더 커지고, 값이 높을수록 압축은 더 느리지만 파일 크기는 더 작아집니다.

## 다른 middleware { #other-middlewares }

다른 ASGI middleware도 많이 있습니다.

예를 들어:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn의 `ProxyHeadersMiddleware`</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

사용 가능한 다른 middleware를 보려면 <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">Starlette의 Middleware 문서</a>와 <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI Awesome List</a>를 확인하세요.
