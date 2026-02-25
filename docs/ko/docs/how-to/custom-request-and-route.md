# 커스텀 Request 및 APIRoute 클래스 { #custom-request-and-apiroute-class }

일부 경우에는 `Request`와 `APIRoute` 클래스에서 사용되는 로직을 오버라이드하고 싶을 수 있습니다.

특히, 이는 middleware에 있는 로직의 좋은 대안이 될 수 있습니다.

예를 들어, 애플리케이션에서 처리되기 전에 요청 바디를 읽거나 조작하고 싶을 때가 그렇습니다.

/// danger | 위험

이 기능은 "고급" 기능입니다.

**FastAPI**를 이제 막 시작했다면 이 섹션은 건너뛰는 것이 좋습니다.

///

## 사용 사례 { #use-cases }

사용 사례에는 다음이 포함됩니다:

* JSON이 아닌 요청 바디를 JSON으로 변환하기(예: <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* gzip으로 압축된 요청 바디 압축 해제하기.
* 모든 요청 바디를 자동으로 로깅하기.

## 커스텀 요청 바디 인코딩 처리하기 { #handling-custom-request-body-encodings }

커스텀 `Request` 서브클래스를 사용해 gzip 요청의 압축을 해제하는 방법을 살펴보겠습니다.

그리고 그 커스텀 요청 클래스를 사용하기 위한 `APIRoute` 서브클래스도 함께 보겠습니다.

### 커스텀 `GzipRequest` 클래스 만들기 { #create-a-custom-gziprequest-class }

/// tip | 팁

이 예시는 동작 방식 시연을 위한 장난감 예제입니다. Gzip 지원이 필요하다면 제공되는 [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank}를 사용할 수 있습니다.

///

먼저, `GzipRequest` 클래스를 만듭니다. 이 클래스는 `Request.body()` 메서드를 덮어써서, 적절한 헤더가 있는 경우 바디를 압축 해제합니다.

헤더에 `gzip`이 없으면 바디를 압축 해제하려고 시도하지 않습니다.

이렇게 하면 동일한 route 클래스가 gzip으로 압축된 요청과 압축되지 않은 요청을 모두 처리할 수 있습니다.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### 커스텀 `GzipRoute` 클래스 만들기 { #create-a-custom-gziproute-class }

다음으로, `GzipRequest`를 활용하는 `fastapi.routing.APIRoute`의 커스텀 서브클래스를 만듭니다.

이번에는 `APIRoute.get_route_handler()` 메서드를 오버라이드합니다.

이 메서드는 함수를 반환합니다. 그리고 그 함수가 요청을 받아 응답을 반환합니다.

여기서는 원본 요청으로부터 `GzipRequest`를 만들기 위해 이를 사용합니다.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | 기술 세부사항

`Request`에는 `request.scope` 속성이 있는데, 이는 요청과 관련된 메타데이터를 담고 있는 Python `dict`입니다.

`Request`에는 또한 `request.receive`가 있는데, 이는 요청의 바디를 "받기(receive)" 위한 함수입니다.

`scope` `dict`와 `receive` 함수는 모두 ASGI 명세의 일부입니다.

그리고 이 두 가지, `scope`와 `receive`가 새로운 `Request` 인스턴스를 만드는 데 필요한 것들입니다.

`Request`에 대해 더 알아보려면 <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette의 Requests 문서</a>를 확인하세요.

///

`GzipRequest.get_route_handler`가 반환하는 함수가 다르게 하는 유일한 것은 `Request`를 `GzipRequest`로 변환하는 것입니다.

이렇게 하면, 우리의 `GzipRequest`가 *경로 처리*로 전달하기 전에(필요하다면) 데이터의 압축 해제를 담당하게 됩니다.

그 이후의 모든 처리 로직은 동일합니다.

하지만 `GzipRequest.body`에서 변경을 했기 때문에, 필요할 때 **FastAPI**가 로드하는 시점에 요청 바디는 자동으로 압축 해제됩니다.

## 예외 핸들러에서 요청 바디 접근하기 { #accessing-the-request-body-in-an-exception-handler }

/// tip | 팁

같은 문제를 해결하려면 `RequestValidationError`에 대한 커스텀 핸들러에서 `body`를 사용하는 편이 아마 훨씬 더 쉽습니다([오류 처리하기](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

하지만 이 예시도 여전히 유효하며, 내부 컴포넌트와 상호작용하는 방법을 보여줍니다.

///

같은 접근 방식을 사용해 예외 핸들러에서 요청 바디에 접근할 수도 있습니다.

필요한 것은 `try`/`except` 블록 안에서 요청을 처리하는 것뿐입니다:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

예외가 발생하더라도 `Request` 인스턴스는 여전히 스코프 안에 남아 있으므로, 오류를 처리할 때 요청 바디를 읽고 활용할 수 있습니다:

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## 라우터에서의 커스텀 `APIRoute` 클래스 { #custom-apiroute-class-in-a-router }

`APIRouter`의 `route_class` 파라미터를 설정할 수도 있습니다:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

이 예시에서는 `router` 아래의 *경로 처리*들이 커스텀 `TimedRoute` 클래스를 사용하며, 응답을 생성하는 데 걸린 시간을 담은 추가 `X-Response-Time` 헤더가 응답에 포함됩니다:

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
