# 교차 출처 리소스 공유

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS 또는 "교차-출처 리소스 공유"</a>란, 브라우저에서 동작하는 프론트엔드가 자바스크립트로 코드로 백엔드와 통신하고, 백엔드는 해당 프론트엔드와 다른 "출처"에 존재하는 상황을 의미합니다.

## 출처

출처란 프로토콜(`http` , `https`), 도메인(`myapp.com`, `localhost`, `localhost.tiangolo.com` ), 그리고 포트(`80`, `443`, `8080` )의 조합을 의미합니다.

따라서, 아래는 모두 상이한 출처입니다:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

모두 `localhost` 에 있지만, 서로 다른 프로토콜과 포트를 사용하고 있으므로 다른 "출처"입니다.

## 단계

브라우저 내 `http://localhost:8080`에서 동작하는 프론트엔드가 있고, 자바스크립트는 `http://localhost`를 통해 백엔드와 통신한다고 가정해봅시다(포트를 명시하지 않는 경우, 브라우저는 `80` 을 기본 포트로 간주합니다).

그러면 브라우저는 백엔드에 HTTP `OPTIONS` 요청을 보내고, 백엔드에서 이 다른 출처(`http://localhost:8080`)와의 통신을 허가하는 적절한 헤더를 보내면, 브라우저는 프론트엔드의 자바스크립트가 백엔드에 요청을 보낼 수 있도록 합니다.

이를 위해, 백엔드는 "허용된 출처(allowed origins)" 목록을 가지고 있어야만 합니다.

이 경우, 프론트엔드가 제대로 동작하기 위해 `http://localhost:8080`을 목록에 포함해야 합니다.

## 와일드카드

모든 출처를 허용하기 위해 목록을 `"*"` ("와일드카드")로 선언하는 것도 가능합니다.

하지만 이것은 특정한 유형의 통신만을 허용하며, 쿠키 및 액세스 토큰과 사용되는 인증 헤더(Authoriztion header) 등이 포함된 경우와 같이 자격 증명(credentials)이 포함된 통신은 허용되지 않습니다.

따라서 모든 작업을 의도한대로 실행하기 위해, 허용되는 출처를 명시적으로 지정하는 것이 좋습니다.

## `CORSMiddleware` 사용

`CORSMiddleware` 을 사용하여 **FastAPI** 응용 프로그램의 교차 출처 리소스 공유 환경을 설정할 수 있습니다.

* `CORSMiddleware` 임포트.
* 허용되는 출처(문자열 형식)의 리스트 생성.
* FastAPI 응용 프로그램에 "미들웨어(middleware)"로 추가.

백엔드에서 다음의 사항을 허용할지에 대해 설정할 수도 있습니다:

* 자격증명 (인증 헤더, 쿠키 등).
* 특정한 HTTP 메소드(`POST`, `PUT`) 또는 와일드카드 `"*"` 를 사용한 모든 HTTP 메소드.
* 특정한 HTTP 헤더 또는 와일드카드 `"*"` 를 사용한 모든 HTTP 헤더.

```Python hl_lines="2  6-11  13-19"
{!../../../docs_src/cors/tutorial001.py!}
```

`CORSMiddleware` 에서 사용하는 기본 매개변수는 제한적이므로, 브라우저가 교차-도메인 상황에서 특정한 출처, 메소드, 헤더 등을 사용할 수 있도록 하려면 이들을 명시적으로 허용해야 합니다.

다음의 인자들이 지원됩니다:

* `allow_origins` - 교차-출처 요청을 보낼 수 있는 출처의 리스트입니다. 예) `['https://example.org', 'https://www.example.org']`. 모든 출처를 허용하기 위해 `['*']` 를 사용할 수 있습니다.
* `allow_origin_regex` - 교차-출처 요청을 보낼 수 있는 출처를 정규표현식 문자열로 나타냅니다.  `'https://.*\.example\.org'`.
* `allow_methods` - 교차-출처 요청을 허용하는 HTTP 메소드의 리스트입니다. 기본값은 `['GET']` 입니다. `['*']` 을 사용하여 모든 표준 메소드들을 허용할 수 있습니다.
* `allow_headers` - 교차-출처를 지원하는 HTTP 요청 헤더의 리스트입니다. 기본값은 `[]` 입니다. 모든 헤더들을 허용하기 위해 `['*']` 를 사용할 수 있습니다. `Accept`, `Accept-Language`, `Content-Language` 그리고 `Content-Type` 헤더는 CORS 요청시 언제나 허용됩니다.
* `allow_credentials` - 교차-출처 요청시 쿠키 지원 여부를 설정합니다. 기본값은 `False` 입니다. 또한 해당 항목을 허용할 경우 `allow_origins` 는 `['*']` 로 설정할 수 없으며, 출처를 반드시 특정해야 합니다.
* `expose_headers` - 브라우저에 접근할 수 있어야 하는 모든 응답 헤더를 가리킵니다. 기본값은 `[]` 입니다.
* `max_age` - 브라우저가 CORS 응답을 캐시에 저장하는 최대 시간을 초 단위로 설정합니다. 기본값은 `600` 입니다.

미들웨어는 두가지 특정한 종류의 HTTP 요청에 응답합니다...

### CORS 사전 요청

`Origin` 및 `Access-Control-Request-Method` 헤더와 함께 전송하는 모든 `OPTIONS` 요청입니다.

이 경우 미들웨어는 들어오는 요청을 가로채 적절한 CORS 헤더와, 정보 제공을 위한 `200` 또는 `400` 응답으로 응답합니다.

### 단순한 요청

`Origin` 헤더를 가진 모든 요청. 이 경우 미들웨어는 요청을 정상적으로 전달하지만, 적절한 CORS 헤더를 응답에 포함시킵니다.

## 더 많은 정보

<abbr title="교차-출처 리소스 공유">CORS</abbr>에 대한 더 많은 정보를 알고싶다면, <a href="https://developer.mozilla.org/ko/docs/Web/HTTP/CORS" class="external-link" target="_blank">Mozilla CORS 문서</a>를 참고하기 바랍니다.

!!! note "기술적 세부 사항"
    `from starlette.middleware.cors import CORSMiddleware` 역시 사용할 수 있습니다.

    **FastAPI**는 개발자인 당신의 편의를 위해 `fastapi.middleware` 에서 몇가지의 미들웨어를 제공합니다. 하지만 대부분의 미들웨어가 Stralette으로부터 직접 제공됩니다.
