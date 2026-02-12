# CORS (교차-출처 리소스 공유) { #cors-cross-origin-resource-sharing }

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS 또는 "Cross-Origin Resource Sharing"</a>란, 브라우저에서 실행되는 프론트엔드에 백엔드와 통신하는 JavaScript 코드가 있고, 백엔드가 프론트엔드와 다른 "출처(origin)"에 있는 상황을 의미합니다.

## 출처 { #origin }

출처란 프로토콜(`http`, `https`), 도메인(`myapp.com`, `localhost`, `localhost.tiangolo.com`), 그리고 포트(`80`, `443`, `8080`)의 조합을 의미합니다.

따라서, 아래는 모두 상이한 출처입니다:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

모두 `localhost`에 있더라도, 서로 다른 프로토콜이나 포트를 사용하므로 서로 다른 "출처"입니다.

## 단계 { #steps }

그러면 브라우저에서 `http://localhost:8080`으로 실행되는 프론트엔드가 있고, 그 JavaScript가 `http://localhost`에서 실행되는 백엔드와 통신하려고 한다고 해봅시다(포트를 명시하지 않았기 때문에, 브라우저는 기본 포트 `80`을 가정합니다).

그러면 브라우저는 `:80`-백엔드에 HTTP `OPTIONS` 요청을 보내고, 백엔드가 이 다른 출처(`http://localhost:8080`)로부터의 통신을 허가하는 적절한 헤더를 보내면, `:8080`-브라우저는 프론트엔드의 JavaScript가 `:80`-백엔드에 요청을 보낼 수 있도록 합니다.

이를 위해, `:80`-백엔드는 "허용된 출처(allowed origins)" 목록을 가지고 있어야 합니다.

이 경우, `:8080`-프론트엔드가 올바르게 동작하려면 목록에 `http://localhost:8080`이 포함되어야 합니다.

## 와일드카드 { #wildcards }

또한 목록을 `"*"`("와일드카드")로 선언해 모두 허용된다고 말할 수도 있습니다.

하지만 그러면 자격 증명(credentials)이 포함된 모든 것을 제외하고 특정 유형의 통신만 허용하게 됩니다. 예: 쿠키, Bearer Token에 사용되는 것과 같은 Authorization 헤더 등.

따라서 모든 것이 올바르게 동작하게 하려면, 허용된 출처를 명시적으로 지정하는 것이 더 좋습니다.

## `CORSMiddleware` 사용 { #use-corsmiddleware }

`CORSMiddleware`를 사용하여 **FastAPI** 애플리케이션에서 이를 설정할 수 있습니다.

* `CORSMiddleware`를 임포트합니다.
* 허용된 출처(문자열)의 리스트를 생성합니다.
* **FastAPI** 애플리케이션에 "미들웨어(middleware)"로 추가합니다.

또한 백엔드가 다음을 허용할지 여부도 지정할 수 있습니다:

* 자격 증명(Authorization 헤더, 쿠키 등).
* 특정 HTTP 메서드(`POST`, `PUT`) 또는 와일드카드 `"*"`를 사용한 모든 메서드.
* 특정 HTTP 헤더 또는 와일드카드 `"*"`를 사용한 모든 헤더.

{* ../../docs_src/cors/tutorial001_py39.py hl[2,6:11,13:19] *}


`CORSMiddleware` 구현에서 사용하는 기본 매개변수는 기본적으로 제한적이므로, 브라우저가 Cross-Domain 컨텍스트에서 특정 출처, 메서드 또는 헤더를 사용할 수 있도록 하려면 이를 명시적으로 활성화해야 합니다.

다음 인자들이 지원됩니다:

* `allow_origins` - 교차-출처 요청을 보낼 수 있도록 허용해야 하는 출처의 리스트입니다. 예: `['https://example.org', 'https://www.example.org']`. 모든 출처를 허용하려면 `['*']`를 사용할 수 있습니다.
* `allow_origin_regex` - 교차-출처 요청을 보낼 수 있도록 허용해야 하는 출처와 매칭할 정규표현식 문자열입니다. 예: `'https://.*\.example\.org'`.
* `allow_methods` - 교차-출처 요청에 허용되어야 하는 HTTP 메서드의 리스트입니다. 기본값은 `['GET']`입니다. 모든 표준 메서드를 허용하려면 `['*']`를 사용할 수 있습니다.
* `allow_headers` - 교차-출처 요청에 대해 지원되어야 하는 HTTP 요청 헤더의 리스트입니다. 기본값은 `[]`입니다. 모든 헤더를 허용하려면 `['*']`를 사용할 수 있습니다. `Accept`, `Accept-Language`, `Content-Language`, `Content-Type` 헤더는 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">단순 CORS 요청</a>에 대해 항상 허용됩니다.
* `allow_credentials` - 교차-출처 요청에 대해 쿠키를 지원해야 함을 나타냅니다. 기본값은 `False`입니다.

    `allow_credentials`가 `True`로 설정된 경우 `allow_origins`, `allow_methods`, `allow_headers` 중 어느 것도 `['*']`로 설정할 수 없습니다. 모두 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards" class="external-link" rel="noopener" target="_blank">명시적으로 지정</a>되어야 합니다.

* `expose_headers` - 브라우저에서 접근 가능해야 하는 모든 응답 헤더를 나타냅니다. 기본값은 `[]`입니다.
* `max_age` - 브라우저가 CORS 응답을 캐시하는 최대 시간을 초 단위로 설정합니다. 기본값은 `600`입니다.

미들웨어는 두 가지 특정한 종류의 HTTP 요청에 응답합니다...

### CORS 사전 요청 { #cors-preflight-requests }

`Origin` 및 `Access-Control-Request-Method` 헤더가 있는 모든 `OPTIONS` 요청입니다.

이 경우 미들웨어는 들어오는 요청을 가로채 적절한 CORS 헤더와 함께, 정보 제공 목적으로 `200` 또는 `400` 응답을 반환합니다.

### 단순한 요청 { #simple-requests }

`Origin` 헤더가 있는 모든 요청입니다. 이 경우 미들웨어는 요청을 정상적으로 통과시키지만, 응답에 적절한 CORS 헤더를 포함합니다.

## 더 많은 정보 { #more-info }

<abbr title="Cross-Origin Resource Sharing – 교차-출처 리소스 공유">CORS</abbr>에 대한 더 많은 정보는 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS 문서</a>를 참고하세요.

/// note | 기술 세부사항

`from starlette.middleware.cors import CORSMiddleware`도 사용할 수 있습니다.

**FastAPI**는 개발자인 여러분의 편의를 위해 `fastapi.middleware`에 여러 미들웨어를 제공합니다. 하지만 사용 가능한 미들웨어 대부분은 Starlette에서 직접 제공됩니다.

///
