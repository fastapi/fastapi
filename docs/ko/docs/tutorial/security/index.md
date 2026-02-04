# 보안 { #security }

보안, 인증(authentication), 인가(authorization)를 처리하는 방법은 매우 다양합니다.

그리고 보통 복잡하고 "어려운" 주제이기도 합니다.

많은 프레임워크와 시스템에서 보안과 인증만 처리하는 데도 큰 노력과 코드가 필요합니다(많은 경우 작성된 전체 코드의 50% 이상이 될 수도 있습니다).

**FastAPI**는 모든 보안 명세를 전부 공부하고 배울 필요 없이, 표준적인 방식으로 쉽고 빠르게 **보안(Security)** 을 다룰 수 있도록 여러 도구를 제공합니다.

하지만 먼저, 몇 가지 작은 개념을 확인해 보겠습니다.

## 급하신가요? { #in-a-hurry }

이 용어들에 관심이 없고 사용자명과 비밀번호 기반 인증을 사용한 보안을 *지금 당장* 추가하기만 하면 된다면, 다음 장들로 넘어가세요.

## OAuth2 { #oauth2 }

OAuth2는 인증과 인가를 처리하는 여러 방법을 정의하는 명세입니다.

상당히 방대한 명세이며 여러 복잡한 사용 사례를 다룹니다.

"제3자"를 사용해 인증하는 방법도 포함합니다.

바로 `"Facebook, Google, X (Twitter), GitHub로 로그인"` 같은 시스템들이 내부적으로 사용하는 방식입니다.

### OAuth 1 { #oauth-1 }

OAuth 1도 있었는데, 이는 OAuth2와 매우 다르고 통신을 암호화하는 방법까지 직접 명세에 포함했기 때문에 더 복잡했습니다.

요즘에는 그다지 인기 있거나 사용되지는 않습니다.

OAuth2는 통신을 어떻게 암호화할지는 명세하지 않고, 애플리케이션이 HTTPS로 제공될 것을 기대합니다.

/// tip | 팁

**배포**에 대한 섹션에서 Traefik과 Let's Encrypt를 사용해 무료로 HTTPS를 설정하는 방법을 볼 수 있습니다.

///

## OpenID Connect { #openid-connect }

OpenID Connect는 **OAuth2**를 기반으로 한 또 다른 명세입니다.

OAuth2에서 비교적 모호한 부분을 일부 구체화하여 상호 운용성을 높이려는 확장입니다.

예를 들어, Google 로그인은 OpenID Connect를 사용합니다(내부적으로는 OAuth2를 사용).

하지만 Facebook 로그인은 OpenID Connect를 지원하지 않습니다. 자체적인 변형의 OAuth2를 사용합니다.

### OpenID("OpenID Connect"가 아님) { #openid-not-openid-connect }

"OpenID"라는 명세도 있었습니다. 이는 **OpenID Connect**와 같은 문제를 해결하려고 했지만, OAuth2를 기반으로 하지 않았습니다.

따라서 완전히 별도의 추가 시스템이었습니다.

요즘에는 그다지 인기 있거나 사용되지는 않습니다.

## OpenAPI { #openapi }

OpenAPI(이전에는 Swagger로 알려짐)는 API를 구축하기 위한 공개 명세입니다(현재 Linux Foundation의 일부).

**FastAPI**는 **OpenAPI**를 기반으로 합니다.

이 덕분에 여러 자동 대화형 문서 인터페이스, 코드 생성 등과 같은 기능을 사용할 수 있습니다.

OpenAPI에는 여러 보안 "scheme"을 정의하는 방법이 있습니다.

이를 사용하면 이러한 대화형 문서 시스템을 포함해, 표준 기반 도구들을 모두 활용할 수 있습니다.

OpenAPI는 다음 보안 scheme들을 정의합니다:

* `apiKey`: 다음에서 전달될 수 있는 애플리케이션 전용 키:
    * 쿼리 파라미터
    * 헤더
    * 쿠키
* `http`: 표준 HTTP 인증 시스템, 예:
    * `bearer`: `Authorization` 헤더에 `Bearer ` + 토큰 값을 넣는 방식. OAuth2에서 유래했습니다.
    * HTTP Basic 인증
    * HTTP Digest 등
* `oauth2`: 보안을 처리하는 모든 OAuth2 방식(이를 "flow"라고 부릅니다).
    * 이 flow들 중 여러 개는 OAuth 2.0 인증 제공자(예: Google, Facebook, X (Twitter), GitHub 등)를 구축하는 데 적합합니다:
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * 하지만 같은 애플리케이션에서 직접 인증을 처리하는 데 완벽하게 사용할 수 있는 특정 "flow"도 하나 있습니다:
        * `password`: 다음 장들에서 이에 대한 예시를 다룹니다.
* `openIdConnect`: OAuth2 인증 데이터를 자동으로 탐색(discover)하는 방법을 정의합니다.
    * 이 자동 탐색은 OpenID Connect 명세에서 정의됩니다.


/// tip | 팁

Google, Facebook, X (Twitter), GitHub 등 다른 인증/인가 제공자를 통합하는 것도 가능하며 비교적 쉽습니다.

가장 복잡한 문제는 그런 인증/인가 제공자 자체를 구축하는 것이지만, **FastAPI**는 어려운 작업을 대신 처리해 주면서 이를 쉽게 할 수 있는 도구를 제공합니다.

///

## **FastAPI** 유틸리티 { #fastapi-utilities }

FastAPI는 `fastapi.security` 모듈에서 각 보안 scheme에 대한 여러 도구를 제공하며, 이러한 보안 메커니즘을 더 쉽게 사용할 수 있게 해줍니다.

다음 장들에서는 **FastAPI**가 제공하는 도구를 사용해 API에 보안을 추가하는 방법을 보게 될 것입니다.

또한 대화형 문서 시스템에 어떻게 자동으로 통합되는지도 확인하게 됩니다.
