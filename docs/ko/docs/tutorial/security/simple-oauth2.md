# 패스워드와 Bearer를 이용한 간단한 OAuth2

이제 이전 장에서 빌드하고 누락된 부분을 추가하여 완전한 보안 흐름을 갖도록 하겠습니다.

## `username`와 `password` 얻기

**FastAPI** 보안 유틸리티를 사용하여 `username` 및 `password`를 가져올 것입니다.

OAuth2는 (우리가 사용하고 있는) "패스워드 플로우"을 사용할 때 클라이언트/유저가 `username` 및 `password` 필드를 폼 데이터로 보내야 함을 지정합니다.

그리고 사양에는 필드의 이름을 그렇게 지정해야 한다고 나와 있습니다. 따라서 `user-name` 또는 `email`은 작동하지 않습니다.

하지만 걱정하지 않아도 됩니다. 프런트엔드에서 최종 사용자에게 원하는 대로 표시할 수 있습니다.

그리고 데이터베이스 모델은 원하는 다른 이름을 사용할 수 있습니다.

그러나 로그인 *경로 작동*의 경우 사양과 호환되도록 이러한 이름을 사용해야 합니다(예를 들어 통합 API 문서 시스템을 사용할 수 있어야 합니다).

사양에는 또한 `username`과 `password`가 폼 데이터로 전송되어야 한다고 명시되어 있습니다(따라서 여기에는 JSON이 없습니다).

### `scope`

사양에는 클라이언트가 다른 폼 필드 "`scope`"를 보낼 수 있다고 나와 있습니다.

폼 필드 이름은 `scope`(단수형)이지만 실제로는 공백으로 구분된 "범위"가 있는 긴 문자열입니다.

각 "범위"는 공백이 없는 문자열입니다.

일반적으로 특정 보안 권한을 선언하는 데 사용됩니다. 다음을 봅시다:

* `users:read` 또는 `users:write`는 일반적인 예시입니다.
* `instagram_basic`은 페이스북/인스타그램에서 사용합니다.
* `https://www.googleapis.com/auth/drive`는 Google에서 사용합니다.

/// info | 정보

OAuth2에서 "범위"는 필요한 특정 권한을 선언하는 문자열입니다.

`:`과 같은 다른 문자가 있는지 또는 URL인지는 중요하지 않습니다.

이러한 세부 사항은 구현에 따라 다릅니다.

OAuth2의 경우 문자열일 뿐입니다.

///

## `username`과 `password`를 가져오는 코드

이제 **FastAPI**에서 제공하는 유틸리티를 사용하여 이를 처리해 보겠습니다.

### `OAuth2PasswordRequestForm`

먼저 `OAuth2PasswordRequestForm`을 가져와 `/token`에 대한 *경로 작동*에서 `Depends`의 의존성으로 사용합니다.

{* ../../docs_src/security/tutorial003.py hl[4,76] *}

`OAuth2PasswordRequestForm`은 다음을 사용하여 폼 본문을 선언하는 클래스 의존성입니다:

* `username`.
* `password`.
* `scope`는 선택적인 필드로 공백으로 구분된 문자열로 구성된 큰 문자열입니다.
* `grant_type`(선택적으로 사용).

/// tip | 팁

OAuth2 사양은 실제로 `password`라는 고정 값이 있는 `grant_type` 필드를 *요구*하지만 `OAuth2PasswordRequestForm`은 이를 강요하지 않습니다.

사용해야 한다면 `OAuth2PasswordRequestForm` 대신 `OAuth2PasswordRequestFormStrict`를 사용하면 됩니다.

///

* `client_id`(선택적으로 사용) (예제에서는 필요하지 않습니다).
* `client_secret`(선택적으로 사용) (예제에서는 필요하지 않습니다).

/// info | 정보

`OAuth2PasswordRequestForm`은 `OAuth2PasswordBearer`와 같이 **FastAPI**에 대한 특수 클래스가 아닙니다.

`OAuth2PasswordBearer`는 **FastAPI**가 보안 체계임을 알도록 합니다. 그래서 OpenAPI에 그렇게 추가됩니다.

그러나 `OAuth2PasswordRequestForm`은 직접 작성하거나 `Form` 매개변수를 직접 선언할 수 있는 클래스 의존성일 뿐입니다.

그러나 일반적인 사용 사례이므로 더 쉽게 하기 위해 **FastAPI**에서 직접 제공합니다.

///

### 폼 데이터 사용하기

/// tip | 팁

종속성 클래스 `OAuth2PasswordRequestForm`의 인스턴스에는 공백으로 구분된 긴 문자열이 있는 `scope` 속성이 없고 대신 전송된 각 범위에 대한 실제 문자열 목록이 있는 `scopes` 속성이 있습니다.

이 예제에서는 `scopes`를 사용하지 않지만 필요한 경우, 기능이 있습니다.

///

이제 폼 필드의 `username`을 사용하여 (가짜) 데이터베이스에서 유저 데이터를 가져옵니다.

해당 사용자가 없으면 "잘못된 사용자 이름 또는 패스워드"라는 오류가 반환됩니다.

오류의 경우 `HTTPException` 예외를 사용합니다:

{* ../../docs_src/security/tutorial003.py hl[3,77:79] *}

### 패스워드 확인하기

이 시점에서 데이터베이스의 사용자 데이터 형식을 확인했지만 암호를 확인하지 않았습니다.

먼저 데이터를 Pydantic `UserInDB` 모델에 넣겠습니다.

일반 텍스트 암호를 저장하면 안 되니 (가짜) 암호 해싱 시스템을 사용합니다.

두 패스워드가 일치하지 않으면 동일한 오류가 반환됩니다.

#### 패스워드 해싱

"해싱"은 일부 콘텐츠(이 경우 패스워드)를 횡설수설하는 것처럼 보이는 일련의 바이트(문자열)로 변환하는 것을 의미합니다.

정확히 동일한 콘텐츠(정확히 동일한 패스워드)를 전달할 때마다 정확히 동일한 횡설수설이 발생합니다.

그러나 횡설수설에서 암호로 다시 변환할 수는 없습니다.

##### 패스워드 해싱을 사용해야 하는 이유

데이터베이스가 유출된 경우 해커는 사용자의 일반 텍스트 암호가 아니라 해시만 갖게 됩니다.

따라서 해커는 다른 시스템에서 동일한 암호를 사용하려고 시도할 수 없습니다(많은 사용자가 모든 곳에서 동일한 암호를 사용하므로 이는 위험할 수 있습니다).

//// tab | 파이썬 3.7 이상

{* ../../docs_src/security/tutorial003.py hl[80:83] *}

////

{* ../../docs_src/security/tutorial003_py310.py hl[78:81] *}

#### `**user_dict`에 대해

`UserInDB(**user_dict)`는 다음을 의미한다:

*`user_dict`의 키와 값을 다음과 같은 키-값 인수로 직접 전달합니다:*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | 정보

`**user_dict`에 대한 자세한 설명은 [**추가 모델** 문서](../extra-models.md#about-user_indict){.internal-link target=_blank}를 다시 읽어봅시다.

///

## 토큰 반환하기

`token` 엔드포인트의 응답은 JSON 객체여야 합니다.

`token_type`이 있어야 합니다. 여기서는 "Bearer" 토큰을 사용하므로 토큰 유형은 "`bearer`"여야 합니다.

그리고 액세스 토큰을 포함하는 문자열과 함께 `access_token`이 있어야 합니다.

이 간단한 예제에서는 완전히 안전하지 않고, 동일한 `username`을 토큰으로 반환합니다.

/// tip | 팁

다음 장에서는 패스워드 해싱 및 <abbr title="JSON Web Tokens">JWT</abbr> 토큰을 사용하여 실제 보안 구현을 볼 수 있습니다.

하지만 지금은 필요한 세부 정보에 집중하겠습니다.

///

{* ../../docs_src/security/tutorial003.py hl[85] *}

/// tip | 팁

사양에 따라 이 예제와 동일하게 `access_token` 및 `token_type`이 포함된 JSON을 반환해야 합니다.

이는 코드에서 직접 수행해야 하며 해당 JSON 키를 사용해야 합니다.

사양을 준수하기 위해 스스로 올바르게 수행하기 위해 거의 유일하게 기억해야 하는 것입니다.

나머지는 **FastAPI**가 처리합니다.

///

## 의존성 업데이트하기

이제 의존성을 업데이트를 할 겁니다.

이 사용자가 활성화되어 있는 *경우에만* `current_user`를 가져올 겁니다.

따라서 `get_current_user`를 의존성으로 사용하는 추가 종속성 `get_current_active_user`를 만듭니다.

이러한 의존성 모두, 사용자가 존재하지 않거나 비활성인 경우 HTTP 오류를 반환합니다.

따라서 엔드포인트에서는 사용자가 존재하고 올바르게 인증되었으며 활성 상태인 경우에만 사용자를 얻습니다:

{* ../../docs_src/security/tutorial003.py hl[58:66,69:72,90] *}

/// info | 정보

여기서 반환하는 값이 `Bearer`인 추가 헤더 `WWW-Authenticate`도 사양의 일부입니다.

모든 HTTP(오류) 상태 코드 401 "UNAUTHORIZED"는 `WWW-Authenticate` 헤더도 반환해야 합니다.

베어러 토큰의 경우(지금의 경우) 해당 헤더의 값은 `Bearer`여야 합니다.

실제로 추가 헤더를 건너뛸 수 있으며 여전히 작동합니다.

그러나 여기에서는 사양을 준수하도록 제공됩니다.

또한 이를 예상하고 (현재 또는 미래에) 사용하는 도구가 있을 수 있으며, 현재 또는 미래에 자신 혹은 자신의 유저들에게 유용할 것입니다.

그것이 표준의 이점입니다 ...

///

## 확인하기

대화형 문서 열기: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

### 인증하기

"Authorize" 버튼을 눌러봅시다.

자격 증명을 사용합니다.

유저명: `johndoe`

패스워드: `secret`

<img src="/img/tutorial/security/image04.png">

시스템에서 인증하면 다음과 같이 표시됩니다:

<img src="/img/tutorial/security/image05.png">

### 자신의 유저 데이터 가져오기

이제 `/users/me` 경로에 `GET` 작업을 진행합시다.

다음과 같은 사용자 데이터를 얻을 수 있습니다:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

잠금 아이콘을 클릭하고 로그아웃한 다음 동일한 작업을 다시 시도하면 다음과 같은 HTTP 401 오류가 발생합니다.

```JSON
{
  "detail": "Not authenticated"
}
```

### 비활성된 유저

이제 비활성된 사용자로 시도하고, 인증해봅시다:

유저명: `alice`

패스워드: `secret2`

그리고 `/users/me` 경로와 함께 `GET` 작업을 사용해 봅시다.

다음과 같은 "Inactive user" 오류가 발생합니다:

```JSON
{
  "detail": "Inactive user"
}
```

## 요약

이제 API에 대한 `username` 및 `password`를 기반으로 완전한 보안 시스템을 구현할 수 있는 도구가 있습니다.

이러한 도구를 사용하여 보안 시스템을 모든 데이터베이스 및 모든 사용자 또는 데이터 모델과 호환되도록 만들 수 있습니다.

유일한 오점은 아직 실제로 "안전"하지 않다는 것입니다.

다음 장에서는 안전한 패스워드 해싱 라이브러리와 <abbr title="JSON Web Tokens">JWT</abbr> 토큰을 사용하는 방법을 살펴보겠습니다.
