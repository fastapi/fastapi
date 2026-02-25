# OAuth2 스코프 { #oauth2-scopes }

**FastAPI**에서 OAuth2 스코프를 직접 사용할 수 있으며, 자연스럽게 동작하도록 통합되어 있습니다.

이를 통해 OAuth2 표준을 따르는 더 세밀한 권한 시스템을 OpenAPI 애플리케이션(및 API 문서)에 통합할 수 있습니다.

스코프를 사용하는 OAuth2는 Facebook, Google, GitHub, Microsoft, X(Twitter) 등 많은 대형 인증 제공자가 사용하는 메커니즘입니다. 이들은 이를 통해 사용자와 애플리케이션에 특정 권한을 제공합니다.

Facebook, Google, GitHub, Microsoft, X(Twitter)로 “로그인”할 때마다, 해당 애플리케이션은 스코프가 있는 OAuth2를 사용하고 있습니다.

이 섹션에서는 **FastAPI** 애플리케이션에서 동일한 “스코프가 있는 OAuth2”로 인증(Authentication)과 인가(Authorization)를 관리하는 방법을 확인합니다.

/// warning | 경고

이 섹션은 다소 고급 내용입니다. 이제 막 시작했다면 건너뛰어도 됩니다.

OAuth2 스코프가 반드시 필요한 것은 아니며, 인증과 인가는 원하는 방식으로 처리할 수 있습니다.

하지만 스코프가 있는 OAuth2는 (OpenAPI와 함께) API 및 API 문서에 깔끔하게 통합될 수 있습니다.

그럼에도 불구하고, 해당 스코프(또는 그 밖의 어떤 보안/인가 요구사항이든)는 코드에서 필요에 맞게 직접 강제해야 합니다.

많은 경우 스코프가 있는 OAuth2는 과한 선택일 수 있습니다.

하지만 필요하다고 알고 있거나 궁금하다면 계속 읽어보세요.

///

## OAuth2 스코프와 OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 사양은 “스코프(scopes)”를 공백으로 구분된 문자열 목록으로 정의합니다.

각 문자열의 내용은 어떤 형식이든 될 수 있지만, 공백을 포함하면 안 됩니다.

이 스코프들은 “권한”을 나타냅니다.

OpenAPI(예: API 문서)에서는 “security schemes”를 정의할 수 있습니다.

이 security scheme 중 하나가 OAuth2를 사용한다면, 스코프도 선언하고 사용할 수 있습니다.

각 “스코프”는 (공백 없는) 문자열일 뿐입니다.

보통 다음과 같이 특정 보안 권한을 선언하는 데 사용합니다:

* `users:read` 또는 `users:write` 는 흔한 예시입니다.
* `instagram_basic` 는 Facebook/Instagram에서 사용합니다.
* `https://www.googleapis.com/auth/drive` 는 Google에서 사용합니다.

/// info | 정보

OAuth2에서 “스코프”는 필요한 특정 권한을 선언하는 문자열일 뿐입니다.

`:` 같은 다른 문자가 있거나 URL이어도 상관없습니다.

그런 세부사항은 구현에 따라 달라집니다.

OAuth2 입장에서는 그저 문자열입니다.

///

## 전체 개요 { #global-view }

먼저, 메인 **튜토리얼 - 사용자 가이드**의 [비밀번호(및 해싱)를 사용하는 OAuth2, JWT 토큰을 사용하는 Bearer](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank} 예제에서 어떤 부분이 바뀌는지 빠르게 살펴보겠습니다. 이제 OAuth2 스코프를 사용합니다:

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

이제 변경 사항을 단계별로 살펴보겠습니다.

## OAuth2 보안 스킴 { #oauth2-security-scheme }

첫 번째 변경 사항은 이제 사용 가능한 스코프 2개(`me`, `items`)로 OAuth2 보안 스킴을 선언한다는 점입니다.

`scopes` 매개변수는 각 스코프를 키로 하고, 설명을 값으로 하는 `dict`를 받습니다:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

이제 스코프를 선언했기 때문에, 로그인/인가할 때 API 문서에 스코프가 표시됩니다.

그리고 접근을 허용할 스코프를 선택할 수 있게 됩니다: `me`와 `items`.

이는 Facebook, Google, GitHub 등으로 로그인하면서 권한을 부여할 때 사용되는 것과 동일한 메커니즘입니다:

<img src="/img/tutorial/security/image11.png">

## 스코프를 포함한 JWT 토큰 { #jwt-token-with-scopes }

이제 토큰 *경로 처리*를 수정해, 요청된 스코프를 반환하도록 합니다.

여전히 동일한 `OAuth2PasswordRequestForm`을 사용합니다. 여기에는 요청에서 받은 각 스코프를 담는 `scopes` 속성이 있으며, 타입은 `str`의 `list`입니다.

그리고 JWT 토큰의 일부로 스코프를 반환합니다.

/// danger | 위험

단순화를 위해, 여기서는 요청으로 받은 스코프를 그대로 토큰에 추가하고 있습니다.

하지만 실제 애플리케이션에서는 보안을 위해, 사용자가 실제로 가질 수 있는 스코프만(또는 미리 정의한 것만) 추가하도록 반드시 확인해야 합니다.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## *경로 처리*와 의존성에서 스코프 선언하기 { #declare-scopes-in-path-operations-and-dependencies }

이제 `/users/me/items/`에 대한 *경로 처리*가 스코프 `items`를 요구한다고 선언합니다.

이를 위해 `fastapi`에서 `Security`를 import하여 사용합니다.

`Security`는 (`Depends`처럼) 의존성을 선언하는 데 사용할 수 있지만, `Security`는 스코프(문자열) 목록을 받는 `scopes` 매개변수도 받습니다.

이 경우, 의존성 함수 `get_current_active_user`를 `Security`에 전달합니다(`Depends`로 할 때와 같은 방식).

하지만 스코프 `list`도 함께 전달합니다. 여기서는 스코프 하나만: `items`(더 많을 수도 있습니다).

또한 의존성 함수 `get_current_active_user`는 `Depends`뿐 아니라 `Security`로도 하위 의존성을 선언할 수 있습니다. 자체 하위 의존성 함수(`get_current_user`)와 추가 스코프 요구사항을 선언합니다.

이 경우에는 스코프 `me`를 요구합니다(여러 스코프를 요구할 수도 있습니다).

/// note | 참고

반드시 서로 다른 곳에 서로 다른 스코프를 추가해야 하는 것은 아닙니다.

여기서는 **FastAPI**가 서로 다른 레벨에서 선언된 스코프를 어떻게 처리하는지 보여주기 위해 이렇게 합니다.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | 기술 세부사항

`Security`는 실제로 `Depends`의 서브클래스이며, 나중에 보게 될 추가 매개변수 하나만 더 있습니다.

하지만 `Depends` 대신 `Security`를 사용하면, **FastAPI**는 보안 스코프를 선언할 수 있음을 알고 내부적으로 이를 사용하며, OpenAPI로 API를 문서화할 수 있습니다.

하지만 `fastapi`에서 `Query`, `Path`, `Depends`, `Security` 등을 import할 때, 이것들은 실제로 특수한 클래스를 반환하는 함수입니다.

///

## `SecurityScopes` 사용하기 { #use-securityscopes }

이제 의존성 `get_current_user`를 업데이트합니다.

이는 위의 의존성들이 사용하는 것입니다.

여기에서 앞서 만든 동일한 OAuth2 스킴을 의존성으로 선언하여 사용합니다: `oauth2_scheme`.

이 의존성 함수 자체에는 스코프 요구사항이 없기 때문에, `oauth2_scheme`와 함께 `Depends`를 사용할 수 있습니다. 보안 스코프를 지정할 필요가 없을 때는 `Security`를 쓸 필요가 없습니다.

또한 `fastapi.security`에서 import한 `SecurityScopes` 타입의 특별한 매개변수를 선언합니다.

이 `SecurityScopes` 클래스는 `Request`와 비슷합니다(`Request`는 요청 객체를 직접 얻기 위해 사용했습니다).

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## `scopes` 사용하기 { #use-the-scopes }

매개변수 `security_scopes`의 타입은 `SecurityScopes`입니다.

여기에는 `scopes` 속성이 있으며, 자기 자신과 이 함수를 하위 의존성으로 사용하는 모든 의존성이 요구하는 스코프 전체를 담은 `list`를 가집니다. 즉, 모든 “dependants”... 다소 헷갈릴 수 있는데, 아래에서 다시 설명합니다.

`security_scopes` 객체(`SecurityScopes` 클래스)에는 또한 `scope_str` 속성이 있는데, 공백으로 구분된 단일 문자열로 스코프들을 담고 있습니다(이를 사용할 것입니다).

나중에 여러 지점에서 재사용(`raise`)할 수 있는 `HTTPException`을 생성합니다.

이 예외에는 필요한 스코프(있다면)를 공백으로 구분된 문자열(`scope_str`)로 포함합니다. 그리고 그 스코프 문자열을 `WWW-Authenticate` 헤더에 넣습니다(이는 사양의 일부입니다).

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## `username`과 데이터 형태 검증하기 { #verify-the-username-and-data-shape }

`username`을 얻었는지 확인하고, 스코프를 추출합니다.

그런 다음 Pydantic 모델로 데이터를 검증합니다(`ValidationError` 예외를 잡습니다). JWT 토큰을 읽거나 Pydantic으로 데이터를 검증하는 과정에서 오류가 나면, 앞에서 만든 `HTTPException`을 raise합니다.

이를 위해 Pydantic 모델 `TokenData`에 새 속성 `scopes`를 추가합니다.

Pydantic으로 데이터를 검증하면, 예를 들어 스코프가 정확히 `str`의 `list`이고 `username`이 `str`인지 등을 보장할 수 있습니다.

예를 들어 `dict`나 다른 형태라면, 나중에 애플리케이션이 어느 시점에 깨지면서 보안 위험이 될 수 있습니다.

또한 해당 username을 가진 사용자가 있는지 확인하고, 없다면 앞에서 만든 동일한 예외를 raise합니다.

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## `scopes` 검증하기 { #verify-the-scopes }

이제 이 의존성과 모든 dependant( *경로 처리* 포함)가 요구하는 모든 스코프가, 받은 토큰의 스코프에 포함되어 있는지 확인합니다. 그렇지 않으면 `HTTPException`을 raise합니다.

이를 위해, 모든 스코프를 `str`로 담고 있는 `security_scopes.scopes`를 사용합니다.

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## 의존성 트리와 스코프 { #dependency-tree-and-scopes }

이 의존성 트리와 스코프를 다시 살펴보겠습니다.

`get_current_active_user` 의존성은 `get_current_user`를 하위 의존성으로 가지므로, `get_current_active_user`에서 선언된 스코프 `"me"`는 `get_current_user`에 전달되는 `security_scopes.scopes`의 요구 스코프 목록에 포함됩니다.

*경로 처리* 자체도 스코프 `"items"`를 선언하므로, 이것 또한 `get_current_user`에 전달되는 `security_scopes.scopes` 목록에 포함됩니다.

의존성과 스코프의 계층 구조는 다음과 같습니다:

* *경로 처리* `read_own_items`는:
    * 의존성과 함께 요구 스코프 `["items"]`를 가집니다:
    * `get_current_active_user`:
        * 의존성 함수 `get_current_active_user`는:
            * 의존성과 함께 요구 스코프 `["me"]`를 가집니다:
            * `get_current_user`:
                * 의존성 함수 `get_current_user`는:
                    * 자체적으로는 요구 스코프가 없습니다.
                    * `oauth2_scheme`를 사용하는 의존성이 있습니다.
                    * `SecurityScopes` 타입의 `security_scopes` 매개변수가 있습니다:
                        * 이 `security_scopes` 매개변수는 위에서 선언된 모든 스코프를 담은 `list`인 `scopes` 속성을 가지므로:
                            * *경로 처리* `read_own_items`의 경우 `security_scopes.scopes`에는 `["me", "items"]`가 들어갑니다.
                            * *경로 처리* `read_users_me`의 경우 `security_scopes.scopes`에는 `["me"]`가 들어갑니다. 이는 의존성 `get_current_active_user`에서 선언되기 때문입니다.
                            * *경로 처리* `read_system_status`의 경우 `security_scopes.scopes`에는 `[]`(없음)가 들어갑니다. `scopes`가 있는 `Security`를 선언하지 않았고, 그 의존성인 `get_current_user`도 `scopes`를 선언하지 않았기 때문입니다.

/// tip | 팁

여기서 중요한 “마법 같은” 점은 `get_current_user`가 각 *경로 처리*마다 검사해야 하는 `scopes` 목록이 달라진다는 것입니다.

이는 특정 *경로 처리*에 대한 의존성 트리에서, 각 *경로 처리*와 각 의존성에 선언된 `scopes`에 따라 달라집니다.

///

## `SecurityScopes`에 대한 추가 설명 { #more-details-about-securityscopes }

`SecurityScopes`는 어느 지점에서든, 그리고 여러 곳에서 사용할 수 있으며, “루트” 의존성에만 있어야 하는 것은 아닙니다.

`SecurityScopes`는 **해당 특정** *경로 처리*와 **해당 특정** 의존성 트리에 대해, 현재 `Security` 의존성과 모든 dependant에 선언된 보안 스코프를 항상 갖고 있습니다.

`SecurityScopes`에는 dependant가 선언한 모든 스코프가 포함되므로, 중앙의 의존성 함수에서 토큰이 필요한 스코프를 가지고 있는지 검증한 다음, 서로 다른 *경로 처리*에서 서로 다른 스코프 요구사항을 선언할 수 있습니다.

이들은 각 *경로 처리*마다 독립적으로 검사됩니다.

## 확인하기 { #check-it }

API 문서를 열면, 인증하고 인가할 스코프를 지정할 수 있습니다.

<img src="/img/tutorial/security/image11.png">

어떤 스코프도 선택하지 않으면 “인증”은 되지만, `/users/me/` 또는 `/users/me/items/`에 접근하려고 하면 권한이 충분하지 않다는 오류가 발생합니다. `/status/`에는 여전히 접근할 수 있습니다.

그리고 스코프 `me`는 선택했지만 스코프 `items`는 선택하지 않았다면, `/users/me/`에는 접근할 수 있지만 `/users/me/items/`에는 접근할 수 없습니다.

이는 사용자가 애플리케이션에 얼마나 많은 권한을 부여했는지에 따라, 제3자 애플리케이션이 사용자로부터 제공받은 토큰으로 이 *경로 처리*들 중 하나에 접근하려고 할 때 발생하는 상황과 같습니다.

## 제3자 통합에 대해 { #about-third-party-integrations }

이 예제에서는 OAuth2 “password” 플로우를 사용하고 있습니다.

이는 보통 자체 프론트엔드가 있는 우리 애플리케이션에 로그인할 때 적합합니다.

우리가 이를 통제하므로 `username`과 `password`를 받는 것을 신뢰할 수 있기 때문입니다.

하지만 다른 사람들이 연결할 OAuth2 애플리케이션(즉, Facebook, Google, GitHub 등과 동등한 인증 제공자를 만들고 있다면)을 구축한다면, 다른 플로우 중 하나를 사용해야 합니다.

가장 흔한 것은 implicit 플로우입니다.

가장 안전한 것은 code 플로우이지만, 더 많은 단계가 필요해 구현이 더 복잡합니다. 복잡하기 때문에 많은 제공자는 implicit 플로우를 권장하게 됩니다.

/// note | 참고

인증 제공자마다 자신들의 브랜드의 일부로 만들기 위해, 각 플로우를 서로 다른 방식으로 이름 붙이는 경우가 흔합니다.

하지만 결국, 동일한 OAuth2 표준을 구현하고 있는 것입니다.

///

**FastAPI**는 `fastapi.security.oauth2`에 이러한 모든 OAuth2 인증 플로우를 위한 유틸리티를 포함합니다.

## 데코레이터 `dependencies`에서의 `Security` { #security-in-decorator-dependencies }

[경로 처리 데코레이터의 의존성](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}에서 설명한 것처럼 데코레이터의 `dependencies` 매개변수에 `Depends`의 `list`를 정의할 수 있는 것과 같은 방식으로, 거기에서 `scopes`와 함께 `Security`를 사용할 수도 있습니다.
