# 패스워드(해싱 포함)를 사용하는 OAuth2, JWT 토큰을 사용하는 Bearer { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

모든 보안 흐름을 구성했으므로, 이제 <abbr title="JSON Web Tokens">JWT</abbr> 토큰과 안전한 패스워드 해싱을 사용해 애플리케이션을 실제로 안전하게 만들겠습니다.

이 코드는 실제로 애플리케이션에서 사용할 수 있으며, 패스워드 해시를 데이터베이스에 저장하는 등의 작업에 활용할 수 있습니다.

이전 장에서 멈춘 지점부터 시작해 내용을 확장해 나가겠습니다.

## JWT 알아보기 { #about-jwt }

JWT는 "JSON Web Tokens"를 의미합니다.

JSON 객체를 공백이 없는 길고 밀집된 문자열로 부호화하는 표준입니다. 다음과 같은 형태입니다:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

암호화된 것이 아니므로, 누구나 내용에서 정보를 복원할 수 있습니다.

하지만 서명되어 있습니다. 따라서 자신이 발급한 토큰을 받았을 때, 실제로 자신이 발급한 것이 맞는지 검증할 수 있습니다.

예를 들어 만료 기간이 1주일인 토큰을 생성할 수 있습니다. 그리고 사용자가 다음 날 토큰을 가지고 돌아오면, 그 사용자가 시스템에 여전히 로그인되어 있다는 것을 알 수 있습니다.

1주일 뒤에는 토큰이 만료되고 사용자는 인가되지 않으므로 새 토큰을 받기 위해 다시 로그인해야 합니다. 그리고 사용자(또는 제3자)가 만료 시간을 바꾸기 위해 토큰을 수정하려고 하면, 서명이 일치하지 않기 때문에 이를 알아챌 수 있습니다.

JWT 토큰을 직접 다뤄보고 동작 방식을 확인해보고 싶다면 <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>를 확인하십시오.

## `PyJWT` 설치 { #install-pyjwt }

Python에서 JWT 토큰을 생성하고 검증하려면 `PyJWT`를 설치해야 합니다.

[가상환경](../../virtual-environments.md){.internal-link target=_blank}을 만들고 활성화한 다음 `pyjwt`를 설치하십시오:

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info

RSA나 ECDSA 같은 전자 서명 알고리즘을 사용할 계획이라면, cryptography 라이브러리 의존성인 `pyjwt[crypto]`를 설치해야 합니다.

자세한 내용은 <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">PyJWT Installation docs</a>에서 확인할 수 있습니다.

///

## 패스워드 해싱 { #password-hashing }

"해싱(Hashing)"은 어떤 내용(여기서는 패스워드)을 알아볼 수 없는 바이트 시퀀스(그냥 문자열)로 변환하는 것을 의미합니다.

정확히 같은 내용(정확히 같은 패스워드)을 넣으면 정확히 같은 알아볼 수 없는 문자열이 나옵니다.

하지만 그 알아볼 수 없는 문자열에서 다시 패스워드로 되돌릴 수는 없습니다.

### 패스워드 해싱을 사용하는 이유 { #why-use-password-hashing }

데이터베이스를 탈취당하더라도, 침입자는 사용자의 평문 패스워드 대신 해시만 얻게 됩니다.

따라서 침입자는 그 패스워드를 다른 시스템에서 사용해 보려고 시도할 수 없습니다(많은 사용자가 어디서나 같은 패스워드를 사용하므로, 이는 위험합니다).

## `pwdlib` 설치 { #install-pwdlib }

pwdlib는 패스워드 해시를 다루기 위한 훌륭한 Python 패키지입니다.

많은 안전한 해싱 알고리즘과 이를 다루기 위한 유틸리티를 지원합니다.

추천 알고리즘은 "Argon2"입니다.

[가상환경](../../virtual-environments.md){.internal-link target=_blank}을 만들고 활성화한 다음 Argon2와 함께 pwdlib를 설치하십시오:

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip

`pwdlib`를 사용하면 **Django**, **Flask** 보안 플러그인 또는 다른 여러 도구로 생성한 패스워드를 읽을 수 있도록 설정할 수도 있습니다.

따라서 예를 들어, FastAPI 애플리케이션과 Django 애플리케이션이 같은 데이터베이스에서 동일한 데이터를 공유할 수 있습니다. 또는 같은 데이터베이스를 사용하면서 Django 애플리케이션을 점진적으로 마이그레이션할 수도 있습니다.

그리고 사용자는 Django 앱 또는 **FastAPI** 앱에서 동시에 로그인할 수 있습니다.

///

## 패스워드 해시 및 검증 { #hash-and-verify-the-passwords }

`pwdlib`에서 필요한 도구를 임포트합니다.

권장 설정으로 PasswordHash 인스턴스를 생성합니다. 이는 패스워드를 해싱하고 검증하는 데 사용됩니다.

/// tip

pwdlib는 bcrypt 해싱 알고리즘도 지원하지만 레거시 알고리즘은 포함하지 않습니다. 오래된 해시로 작업해야 한다면 passlib 라이브러리를 사용하는 것을 권장합니다.

예를 들어, 다른 시스템(Django 같은)에서 생성한 패스워드를 읽고 검증하되, 새 패스워드는 Argon2나 Bcrypt 같은 다른 알고리즘으로 해싱하도록 할 수 있습니다.

그리고 동시에 그 모든 것과 호환되게 만들 수 있습니다.

///

사용자로부터 받은 패스워드를 해싱하는 유틸리티 함수를 생성합니다.

그리고 받은 패스워드가 저장된 해시와 일치하는지 검증하는 또 다른 유틸리티도 생성합니다.

그리고 사용자를 인증하고 반환하는 또 다른 함수도 생성합니다.

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,56:57,60:61,70:76] *}

/// note

새로운 (가짜) 데이터베이스 `fake_users_db`를 확인하면, 이제 해시 처리된 패스워드가 어떻게 생겼는지 볼 수 있습니다: `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`.

///

## JWT 토큰 처리 { #handle-jwt-tokens }

설치된 모듈을 임포트합니다.

JWT 토큰을 서명하는 데 사용할 임의의 비밀 키를 생성합니다.

안전한 임의의 비밀 키를 생성하려면 다음 명령을 사용하십시오:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

그리고 출력 결과를 변수 `SECRET_KEY`에 복사합니다(예제의 값을 사용하지 마십시오).

JWT 토큰을 서명하는 데 사용될 알고리즘을 위한 변수 `ALGORITHM`을 생성하고 `"HS256"`으로 설정합니다.

토큰 만료를 위한 변수를 생성합니다.

응답을 위해 토큰 엔드포인트에서 사용될 Pydantic 모델을 정의합니다.

새 액세스 토큰을 생성하기 위한 유틸리티 함수를 생성합니다.

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,79:87] *}

## 의존성 업데이트 { #update-the-dependencies }

`get_current_user`가 이전과 동일한 토큰을 받도록 업데이트하되, 이번에는 JWT 토큰을 사용하도록 합니다.

받은 토큰을 디코딩하고 검증한 뒤 현재 사용자를 반환합니다.

토큰이 유효하지 않다면 즉시 HTTP 오류를 반환합니다.

{* ../../docs_src/security/tutorial004_an_py310.py hl[90:107] *}

## `/token` *경로 처리* 업데이트 { #update-the-token-path-operation }

토큰의 만료 시간으로 `timedelta`를 생성합니다.

실제 JWT 액세스 토큰을 생성하여 반환합니다.

{* ../../docs_src/security/tutorial004_an_py310.py hl[118:133] *}

### JWT "주체(subject)" `sub`에 대한 기술 세부사항 { #technical-details-about-the-jwt-subject-sub }

JWT 명세에 따르면 토큰의 주체를 담는 `sub` 키가 있습니다.

선택적으로 사용할 수 있지만, 여기에 사용자 식별 정보를 넣게 되므로 여기서는 이를 사용합니다.

JWT는 사용자를 식별하고 사용자가 API에서 직접 작업을 수행할 수 있도록 허용하는 것 외에도 다른 용도로 사용될 수 있습니다.

예를 들어 "자동차"나 "블로그 게시물"을 식별할 수 있습니다.

그런 다음 해당 엔터티에 대한 권한(자동차의 경우 "drive", 블로그의 경우 "edit" 등)을 추가할 수 있습니다.

그리고 그 JWT 토큰을 사용자(또는 봇)에게 제공하면, 계정이 없어도 API가 생성한 JWT 토큰만으로 그 동작들(자동차 운전, 블로그 편집)을 수행할 수 있습니다.

이러한 아이디어를 활용하면 JWT는 훨씬 더 정교한 시나리오에도 사용될 수 있습니다.

그런 경우 여러 엔터티가 동일한 ID(예: `foo`)를 가질 수도 있습니다(사용자 `foo`, 자동차 `foo`, 블로그 게시물 `foo`).

따라서 ID 충돌을 방지하기 위해, 사용자에 대한 JWT 토큰을 생성할 때 `sub` 키의 값에 접두사를 붙일 수 있습니다. 예를 들어 `username:` 같은 것입니다. 그러면 이 예제에서 `sub` 값은 `username:johndoe`가 될 수 있습니다.

기억해야 할 중요한 점은 `sub` 키가 전체 애플리케이션에서 고유한 식별자여야 하고, 문자열이어야 한다는 것입니다.

## 확인하기 { #check-it }

서버를 실행하고 문서로 이동하십시오: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

다음과 같은 사용자 인터페이스가 보일 것입니다:

<img src="/img/tutorial/security/image07.png">

이전과 같은 방법으로 애플리케이션을 인가하십시오.

다음 인증 정보를 사용하십시오:

Username: `johndoe`
Password: `secret`

/// check

코드 어디에도 평문 패스워드 "`secret`"은 없고, 해시된 버전만 있다는 점에 유의하십시오.

///

<img src="/img/tutorial/security/image08.png">

엔드포인트 `/users/me/`를 호출하면 다음과 같은 응답을 받게 됩니다:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

개발자 도구를 열어보면 전송된 데이터에는 토큰만 포함되어 있고, 패스워드는 사용자를 인증하고 해당 액세스 토큰을 얻기 위한 첫 번째 요청에서만 전송되며 이후에는 전송되지 않는 것을 확인할 수 있습니다:

<img src="/img/tutorial/security/image10.png">

/// note

`Bearer `로 시작하는 값을 가진 `Authorization` 헤더에 주목하십시오.

///

## `scopes`의 고급 사용법 { #advanced-usage-with-scopes }

OAuth2에는 "scopes"라는 개념이 있습니다.

이를 사용해 JWT 토큰에 특정 권한 집합을 추가할 수 있습니다.

그런 다음 이 토큰을 사용자에게 직접 제공하거나 제3자에게 제공하여, 특정 제한사항 하에서 API와 상호작용하도록 할 수 있습니다.

어떻게 사용하는지, 그리고 **FastAPI**에 어떻게 통합되는지는 이후 **심화 사용자 안내서**에서 배울 수 있습니다.

## 요약 { #recap }

지금까지 살펴본 내용을 바탕으로, OAuth2와 JWT 같은 표준을 사용해 안전한 **FastAPI** 애플리케이션을 설정할 수 있습니다.

거의 모든 프레임워크에서 보안 처리는 꽤 빠르게 복잡한 주제가 됩니다.

이를 크게 단순화하는 많은 패키지들은 데이터 모델, 데이터베이스, 사용 가능한 기능들에 대해 많은 타협을 해야 합니다. 그리고 지나치게 단순화하는 일부 패키지들은 실제로 내부에 보안 결함이 있기도 합니다.

---

**FastAPI**는 어떤 데이터베이스, 데이터 모델, 도구에도 타협하지 않습니다.

프로젝트에 가장 잘 맞는 것들을 선택할 수 있는 모든 유연성을 제공합니다.

그리고 **FastAPI**는 외부 패키지를 통합하기 위해 복잡한 메커니즘을 요구하지 않기 때문에 `pwdlib`와 `PyJWT` 같은 잘 관리되고 널리 사용되는 패키지들을 바로 사용할 수 있습니다.

하지만 유연성, 견고성, 보안성을 해치지 않으면서 과정을 가능한 한 단순화할 수 있도록 도구들을 제공합니다.

또한 OAuth2 같은 안전한 표준 프로토콜을 비교적 간단한 방식으로 사용하고 구현할 수 있습니다.

더 세분화된 권한 시스템을 위해 OAuth2 "scopes"를 사용하는 방법은, 같은 표준을 따르는 방식으로 **심화 사용자 안내서**에서 더 자세히 배울 수 있습니다. 스코프를 사용하는 OAuth2는 Facebook, Google, GitHub, Microsoft, X (Twitter) 등 많은 대형 인증 제공업체들이 제3자 애플리케이션이 사용자 대신 그들의 API와 상호작용할 수 있도록 인가하는 데 사용하는 메커니즘입니다.
