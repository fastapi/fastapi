# 보안 - 첫 걸음

어떤 도메인에 **백엔드** API가 있다고 가정해 보겠습니다.

그리고 다른 도메인이나 동일한 도메인의 다른 경로(또는 모바일 애플리케이션)에 **프론트엔드**가 있습니다.

그리고 **아이디**과 **패스워드**를 사용하여 프런트엔드가 백엔드로 인증하는 방법을 원합니다.

**OAuth2**를 사용하여 **FastAPI**로 빌드할 수 있습니다.

그러나 필요한 정보를 찾기 위해 긴 명세를 읽는 시간을 절약할 수 있습니다.

보안을 다루기 위해 **FastAPI**가 제공하는 도구들을 사용해 봅시다.

## 둘러보기

먼저 코드를 사용하고 어떻게 작동하는지 확인한 다음, 무슨 일이 일어나고 있는지 이해하기 위해 다시 돌아올 것입니다.

## `main.py` 생성

`main.py`의 예제를 복사합니다:

```Python
{!../../../docs_src/security/tutorial001.py!}
```

## 동작시키기

!!! 정보
    먼저 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>를 설치합니다.

    E.g. `pip install python-multipart`.

    **OAuth2**는 `아이디`와 `패스워드`를 보내기 위해 "폼 데이터"를 사용하기 때문입니다.

예제를 동작시킵니다:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 검토

대화형 문서에 가봅시다: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

다음과 같은 화면을 볼 것입니다:

<img src="/img/tutorial/security/image01.png">

!!! check "Authorize 버튼!"
    새 것처럼 반짝이는 "Authorize" 버튼이 있습니다.

    그리고 *경로 작업*에는 클릭할 수 있는 오른쪽 상단 모서리에 작은 자물쇠가 있습니다.

클릭하면 '아이디'와 '패스워드'(및 기타 선택적 필드)를 입력할 수 있는 작은 승인 양식이 있습니다.:

<img src="/img/tutorial/security/image02.png">

!!! note
    It doesn't matter what you type in the form, it won't work yet. But we'll get there.

이것은 물론 최종 사용자를 위한 프론트엔드는 아니지만 모든 API를 대화식으로 문서화하는 훌륭한 자동화 도구입니다.

프론트엔드 팀(자신일 수도 있음)에서 사용할 수 있습니다.

서드 파티 애플리케이션 및 시스템에서 사용할 수 있습니다.

또한 동일한 애플리케이션을 디버그, 확인 및 테스트하기 위해 직접 사용할 수도 있습니다.

## `패스워드` 흐름

이제 조금 돌아가서 그것이 무엇인지 이해합시다.

`패스워드` "흐름"은 보안 및 인증을 처리하기 위해 OAuth2에 정의된 방식("흐름") 중 하나입니다.

OAuth2는 백엔드 또는 API가 사용자를 인증하는 서버와 독립적일 수 있도록 설계되었습니다.

그러나 이 경우 동일한 **FastAPI** 애플리케이션이 API와 인증을 처리합니다.

그럼 관점을 단순화해서 검토해 보겠습니다:

* 사용자는 프론트엔드에 '아이디'과 '패스워드'를 입력하고 'Enter' 키를 누릅니다.
* 프론트엔드(사용자의 브라우저에서 실행)는 해당 `아이디`와 `패스워드`를 API의 특정 URL(`tokenUrl="token"`로 선언됨)로 보냅니다.
* API는 `아이디`과 `패스워드`를 확인하고 "토큰"으로 응답합니다(아직 구현하지 않았습니다).
    * "토큰"은 나중에 이 사용자를 확인하는 데 사용할 수 있는 일부 콘텐츠가 포함된 문자열입니다.
    * 일반적으로 토큰은 일정 시간이 지나면 만료되도록 설정됩니다.
        * 따라서 사용자는 후에 어느 시점에서 다시 로그인해야 합니다.
        * 그리고 토큰을 도난당하더라도 위험이 줄어듭니다. (대부분의 경우) 영원히 작동하는 영구 키와 다릅니다.
* 프론트엔드는 해당 토큰을 임시로 어딘가에 저장합니다.
* 사용자가 프런트엔드를 클릭하여 프런트엔드 웹 앱의 다른 섹션으로 이동합니다.
* 프론트엔드는 API에서 더 많은 데이터를 가져와야 합니다.
    * 그러나 특정 엔드포인트에 대한 인증이 필요합니다.
    * 따라서 API로 인증하기 위해 'Bearer' 값에 토큰을 더한 'Authorization' 헤더를 보냅니다.
    * 만약 토큰에 `foobar`가 포함된다면 `Authorization` 헤더의 내용은 `Bearer foobar`입니다.

## **FastAPI**의 `OAuth2PasswordBearer`

**FastAPI**는 이러한 보안 기능을 구현하기 위해 다양한 추상화 수준에서 여러 도구를 제공합니다.

이 예시에서는 **Bearer** 토큰을 사용하여 **패스워드** 흐름과 함께 **OAuth2**를 사용할 것입니다. 우리는 `OAuth2PasswordBearer` 클래스를 사용하여 이를 수행합니다.

!!! 정보
    "bearer" 토큰이 유일한 선택지는 아닙니다.

    그러나 우리의 유스케이스에 가장 적합한 것입니다.

    그리고 OAuth2 전문가가 아니고 자신의 요구에 더 적합한 다른 옵션이 있는 이유를 정확히 알고 있지 않는 한 대부분의 사용 사례에 가장 적합할 수 있습니다.

    이 경우, **FastAPI**는 빌드 도구도 제공합니다.

`OAuth2PasswordBearer` 클래스의 인스턴스를 만들 때 `tokenUrl` 매개변수를 전달합니다. 이 매개변수에는 클라이언트(사용자의 브라우저에서 실행되는 프론트엔드)가 토큰을 얻기 위해 `아이디`와 `패스워드`를 보내는 데 사용할 URL이 포함됩니다.

```Python hl_lines="6"
{!../../../docs_src/security/tutorial001.py!}
```

!!! 팁
    여기서 `tokenUrl="token"`은 아직 생성하지 않은 상대 URL `token`을 나타냅니다. 상대 URL이므로 `./token`과 동일합니다.

    상대 URL을 사용하고 있기 때문에 API가 `https://example.com/`에 있는 경우 `https://example.com/token`을 참조합니다. 그러나 API가 `https://example.com/api/v1/`에 있는 경우 `https://example.com/api/v1/token`을 참조합니다.

    상대 URL을 사용하는 것은 [Behind a Proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank}와 같은 고급 사용 사례에서도 애플리케이션이 계속 작동하도록 하는 데 중요합니다.

이 매개변수는 해당 끝점 / *경로 작동*을 생성하지 않지만 URL `/token`이 클라이언트가 토큰을 가져오는 데 사용해야 하는 URL이 될 것이라고 선언합니다. 해당 정보는 OpenAPI에서 사용되며 다음 대화형 API 문서 시스템에서 사용됩니다.

곧 실제 경로 작업도 생성할 것입니다.

!!! 정보
    매우 엄격한 "Pythonista"인 경우 `token_url` 대신 `tokenUrl` 매개변수 이름의 스타일이 마음에 들지 않을 수 있습니다.

    그 이유는 OpenAPI 스펙과 동일한 이름을 사용하고 있기 때문입니다. 따라서 이러한 보안 체계에 대해 더 자세히 조사해야 하는 경우 복사하여 붙여넣으면 이에 대한 추가 정보를 찾을 수 있습니다.

`oauth2_scheme` 변수는 `OAuth2PasswordBearer`의 인스턴스이지만 "callable"하기도 합니다.

다음과 같이 부를 수 있습니다:

```Python
oauth2_scheme(some, parameters)
```

따라서 `Depends`와 함께 사용할 수 있습니다.

### 사용하기

이제 `Depends`를 사용하여 의존성에서 `oauth2_scheme`을 전달할 수 있습니다.

```Python hl_lines="10"
{!../../../docs_src/security/tutorial001.py!}
```

이 종속성은 *경로 작동 함수*의 'token' 매개변수에 할당된 'str'을 제공합니다.

**FastAPI**는 이 의존성을 사용하여 OpenAPI 스키마(및 자동 API 문서)에서 "보안 체계"를 정의할 수 있음을 알 수 있습니다.

!!! 기술적 세부사항
    **FastAPI**는 'fastapi.security.oauth2.OAuth2'에서 상속하기 때문에 'fastapi.security.base.SecurityBase'에서 차례로 상속되기에 'OAuth2PasswordBearer' 클래스(종속성에서 선언됨)를 사용하여 OpenAPI에서 보안 체계를 정의할 수 있음을 알 수 있습니다.

    OpenAPI(및 자동 API 문서)와 통합되는 모든 보안 유틸리티는 `SecurityBase`를 상속하므로 **FastAPI**가 OpenAPI에 통합하는 방법을 알 수 있습니다.

## What it does

해당 `Authorization` 헤더에 대한 요청을 살펴보고 값이 `Bearer`와 일부 토큰인지 확인하고 토큰을 `str`로 반환합니다.

'Authorization' 헤더가 표시되지 않거나 값에 'Bearer' 토큰이 없으면 401 상태 코드 오류('UNAUTHORIZED')로 직접 응답합니다.

오류를 반환하기 위해 토큰이 있는지 확인할 필요조차 없습니다. 함수가 실행되면 해당 토큰에 'str'이 있음을 확신할 수 있습니다.

대화형 문서에서 이미 시도해 볼 수 있습니다:

<img src="/img/tutorial/security/image03.png">

우리는 아직 토큰의 유효성을 확인하지 않았지만 이미 시작되었습니다.

## 요약

따라서 3~4줄만 추가하면 이미 원시적 형태의 보안을 갖추게 됩니다.
