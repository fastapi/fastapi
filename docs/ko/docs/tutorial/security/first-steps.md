# 보안 - 첫 단계 { #security-first-steps }

어떤 도메인에 **backend** API가 있다고 가정해 보겠습니다.

그리고 다른 도메인에 **frontend**가 있거나, 같은 도메인의 다른 경로에 있거나(또는 모바일 애플리케이션에 있을 수도 있습니다).

그리고 frontend가 **username**과 **password**를 사용해 backend에 인증할 수 있는 방법이 필요하다고 해봅시다.

**FastAPI**와 함께 **OAuth2**를 사용해서 이를 구현할 수 있습니다.

하지만 필요한 작은 정보 조각들을 찾기 위해 길고 긴 전체 스펙을 읽느라 시간을 쓰지 않도록 하겠습니다.

보안을 처리하기 위해 **FastAPI**가 제공하는 도구들을 사용해 봅시다.

## 어떻게 보이는지 { #how-it-looks }

먼저 코드를 그냥 사용해서 어떻게 동작하는지 보고, 그다음에 무슨 일이 일어나는지 이해하러 다시 돌아오겠습니다.

## `main.py` 만들기 { #create-main-py }

예제를 파일 `main.py`에 복사하세요:

{* ../../docs_src/security/tutorial001_an_py39.py *}

## 실행하기 { #run-it }

/// info | 정보

<a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> 패키지는 `pip install "fastapi[standard]"` 명령을 실행하면 **FastAPI**와 함께 자동으로 설치됩니다.

하지만 `pip install fastapi` 명령을 사용하면 `python-multipart` 패키지가 기본으로 포함되지 않습니다.

수동으로 설치하려면, [가상 환경](../../virtual-environments.md){.internal-link target=_blank}을 만들고 활성화한 다음, 아래로 설치하세요:

```console
$ pip install python-multipart
```

이는 **OAuth2**가 `username`과 `password`를 보내기 위해 "form data"를 사용하기 때문입니다.

///

다음으로 예제를 실행하세요:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 확인하기 { #check-it }

대화형 문서로 이동하세요: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

다음과 비슷한 화면이 보일 것입니다:

<img src="/img/tutorial/security/image01.png">

/// check | Authorize 버튼!

반짝이는 새 "Authorize" 버튼이 이미 있습니다.

그리고 *경로 처리*에는 오른쪽 상단에 클릭할 수 있는 작은 자물쇠가 있습니다.

///

그리고 이를 클릭하면 `username`과 `password`(그리고 다른 선택적 필드들)를 입력할 수 있는 작은 인증 폼이 나타납니다:

<img src="/img/tutorial/security/image02.png">

/// note | 참고

폼에 무엇을 입력하든 아직은 동작하지 않습니다. 하지만 곧 여기까지 구현할 것입니다.

///

물론 이것은 최종 사용자를 위한 frontend는 아니지만, 모든 API를 대화형으로 문서화하는 훌륭한 자동 도구입니다.

frontend 팀(그게 본인일 수도 있습니다)이 사용할 수 있습니다.

서드파티 애플리케이션과 시스템에서도 사용할 수 있습니다.

그리고 동일한 애플리케이션을 디버그하고, 확인하고, 테스트하기 위해 본인이 사용할 수도 있습니다.

## `password` 플로우 { #the-password-flow }

이제 조금 돌아가서 이것들이 무엇인지 이해해 봅시다.

`password` "flow"는 보안과 인증을 처리하기 위해 OAuth2에서 정의한 여러 방식("flows") 중 하나입니다.

OAuth2는 backend 또는 API가 사용자를 인증하는 서버와 독립적일 수 있도록 설계되었습니다.

하지만 이 경우에는 같은 **FastAPI** 애플리케이션이 API와 인증을 모두 처리합니다.

따라서, 단순화된 관점에서 다시 정리해보면:

* 사용자가 frontend에서 `username`과 `password`를 입력하고 `Enter`를 누릅니다.
* frontend(사용자의 브라우저에서 실행됨)는 해당 `username`과 `password`를 우리 API의 특정 URL로 보냅니다(`tokenUrl="token"`로 선언됨).
* API는 `username`과 `password`를 확인하고 "token"으로 응답합니다(아직 아무것도 구현하지 않았습니다).
    * "token"은 나중에 이 사용자를 검증하는 데 사용할 수 있는 어떤 내용이 담긴 문자열일 뿐입니다.
    * 보통 token은 일정 시간이 지나면 만료되도록 설정합니다.
        * 그래서 사용자는 나중에 어느 시점엔 다시 로그인해야 합니다.
        * 그리고 token이 도난당하더라도 위험이 더 낮습니다. 대부분의 경우 영구적으로 항상 동작하는 키와는 다릅니다.
* frontend는 그 token을 임시로 어딘가에 저장합니다.
* 사용자가 frontend에서 클릭해서 frontend 웹 앱의 다른 섹션으로 이동합니다.
* frontend는 API에서 더 많은 데이터를 가져와야 합니다.
    * 하지만 그 특정 endpoint에는 인증이 필요합니다.
    * 그래서 우리 API에 인증하기 위해 `Authorization` 헤더를, 값은 `Bearer `에 token을 더한 형태로 보냅니다.
    * token에 `foobar`가 들어 있다면 `Authorization` 헤더의 내용은 `Bearer foobar`가 됩니다.

## **FastAPI**의 `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

**FastAPI**는 이런 보안 기능을 구현하기 위해, 서로 다른 추상화 수준에서 여러 도구를 제공합니다.

이 예제에서는 **OAuth2**의 **Password** 플로우와 **Bearer** token을 사용합니다. 이를 위해 `OAuth2PasswordBearer` 클래스를 사용합니다.

/// info | 정보

"bearer" token만이 유일한 선택지는 아닙니다.

하지만 이 사용 사례에는 가장 적합한 선택입니다.

또한 OAuth2 전문가로서 왜 다른 옵션이 더 적합한지 정확히 아는 경우가 아니라면, 대부분의 사용 사례에도 가장 적합할 가능성이 큽니다.

그런 경우를 위해서도 **FastAPI**는 이를 구성할 수 있는 도구를 제공합니다.

///

`OAuth2PasswordBearer` 클래스의 인스턴스를 만들 때 `tokenUrl` 파라미터를 전달합니다. 이 파라미터에는 클라이언트(사용자의 브라우저에서 실행되는 frontend)가 token을 받기 위해 `username`과 `password`를 보낼 URL이 들어 있습니다.

{* ../../docs_src/security/tutorial001_an_py39.py hl[8] *}

/// tip | 팁

여기서 `tokenUrl="token"`은 아직 만들지 않은 상대 URL `token`을 가리킵니다. 상대 URL이므로 `./token`과 동일합니다.

상대 URL을 사용하므로, 예를 들어 API가 `https://example.com/`에 있다면 `https://example.com/token`을 가리킵니다. 하지만 API가 `https://example.com/api/v1/`에 있다면 `https://example.com/api/v1/token`을 가리킵니다.

상대 URL을 사용하는 것은 [프록시 뒤에서](../../advanced/behind-a-proxy.md){.internal-link target=_blank} 같은 고급 사용 사례에서도 애플리케이션이 계속 동작하도록 보장하는 데 중요합니다.

///

이 파라미터는 그 endpoint / *경로 처리*를 만들지는 않지만, URL `/token`이 클라이언트가 token을 얻기 위해 사용해야 할 URL이라고 선언합니다. 이 정보는 OpenAPI에 사용되고, 이어서 대화형 API 문서 시스템에서도 사용됩니다.

곧 실제 경로 처리를 만들 것입니다.

/// info | 정보

엄격한 "Pythonista"라면 `token_url` 대신 `tokenUrl` 같은 파라미터 이름 스타일이 마음에 들지 않을 수도 있습니다.

이는 OpenAPI 스펙에서 사용하는 이름과 동일하게 맞춘 것이기 때문입니다. 그래서 이런 보안 스킴에 대해 더 조사해야 할 때, 그대로 복사해서 붙여 넣어 더 많은 정보를 찾을 수 있습니다.

///

`oauth2_scheme` 변수는 `OAuth2PasswordBearer`의 인스턴스이지만, "callable"이기도 합니다.

다음처럼 호출될 수 있습니다:

```Python
oauth2_scheme(some, parameters)
```

따라서 `Depends`와 함께 사용할 수 있습니다.

### 사용하기 { #use-it }

이제 `Depends`로 `oauth2_scheme`를 의존성에 전달할 수 있습니다.

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

이 의존성은 `str`을 제공하고, 그 값은 *경로 처리 함수*의 파라미터 `token`에 할당됩니다.

**FastAPI**는 이 의존성을 사용해 OpenAPI 스키마(및 자동 API 문서)에 "security scheme"를 정의할 수 있다는 것을 알게 됩니다.

/// info | 기술 세부사항

**FastAPI**는 (의존성에 선언된) `OAuth2PasswordBearer` 클래스를 사용해 OpenAPI에서 보안 스킴을 정의할 수 있다는 것을 알고 있습니다. 이는 `OAuth2PasswordBearer`가 `fastapi.security.oauth2.OAuth2`를 상속하고, 이것이 다시 `fastapi.security.base.SecurityBase`를 상속하기 때문입니다.

OpenAPI(및 자동 API 문서)와 통합되는 모든 보안 유틸리티는 `SecurityBase`를 상속하며, 그래서 **FastAPI**가 이를 OpenAPI에 어떻게 통합할지 알 수 있습니다.

///

## 무엇을 하는지 { #what-it-does }

요청에서 `Authorization` 헤더를 찾아, 값이 `Bearer `에 어떤 token이 붙은 형태인지 확인한 뒤, 그 token을 `str`로 반환합니다.

`Authorization` 헤더가 없거나, 값에 `Bearer ` token이 없다면, 곧바로 401 상태 코드 오류(`UNAUTHORIZED`)로 응답합니다.

오류를 반환하기 위해 token이 존재하는지 직접 확인할 필요조차 없습니다. 함수가 실행되었다면 그 token에는 `str`이 들어 있다고 확신할 수 있습니다.

대화형 문서에서 이미 시도해 볼 수 있습니다:

<img src="/img/tutorial/security/image03.png">

아직 token의 유효성을 검증하진 않지만, 이것만으로도 시작은 된 셈입니다.

## 요약 { #recap }

즉, 추가로 3~4줄만으로도 이미 원시적인 형태의 보안을 갖추게 됩니다.
