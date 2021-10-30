# 보안 - 첫 단계

어떤 도메인에 **백엔드** API가 있다고 상상해봅시다.

그리고 또다른 도메인 또는 동일한 도메인의 다른 경로에 (또는 모바일 애플리케이션에) **프론트엔드**가 있다고 해봅시다.

그리고 **사용자이름** 및 **비밀번호**를 사용하여, 프론트엔드가 백엔드로 인증하는 방법을 원합니다.

**OAuth2**를 사용하여 그것을 **FastAPI**로 구축할 수 있습니다.

그러나 필요한 작은 정보를 찾기 위해 긴 명세서 전체를 읽는 시간을 절약할 수 있습니다.

보안을 처리하기 위해 **FastAPI**가 제공하는 도구를 사용해봅시다.

## 생김새

우선 그냥 코드를 사용하여 이것이 어떻게 작동하는 지 보고, 어떤 일이 발생했는 지 이해하기 위해 나중에 돌아옵시다.

## `main.py` 생성

`main.py` 파일에 예시를 복사합니다:

```Python
{!../../../docs_src/security/tutorial001.py!}
```

## 실행

!!! info "정보"
    우선 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>를 설치합니다.

    예를 들어 `pip install python-multipart`와 같습니다.

    이것은 **OAuth2**가 `username` 및 `password`를 전송하는 데 "폼 데이터"를 사용하기 때문입니다.


아래의 방법을 사용하여 예시를 실행합니다:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## 확인

대화형 문서로 이동합니다: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

아래와 같은 것을 볼 수 있습니다:

<img src="/img/tutorial/security/image01.png">

!!! check "Authorize 버튼!"
    이미 반짝이는 새로운 "Authorize" 버튼이 있습니다.

    그리고 *경로 작동*에는 클릭할 수 있는 작은 자물쇠가 우측-상단 모서리에 있습니다.

그리고 만약 이것을 클릭하면, `username` 및 `password` (그리고 다른 선택적 필드) 를 입력하는 작은 인가 폼이 뜹니다:

<img src="/img/tutorial/security/image02.png">

!!! note "노트"
    폼에 무엇을 입력하든 지, 아직 작동하지 않습니다. 그러나 작동하게 할 것입니다.

이것은 당연히 최종 사용자를 위한 프론트엔드가 아니지만, 모든 API를 대화식으로 문서화하는 훌륭한 자동화 도구입니다.

이것은 (또한 본인일 수 있는) 프론트엔드 팀에 의해 사용될 수 있습니다.

써드 파티 애플리케이션 및 시스템에 의해 사용될 수 있습니다.

그리고 동일한 애플리케이션을 디버그, 확인, 테스트하기 위해 직접 사용할 수 있습니다.

## `password` 흐름

이제 조금 되돌아 가 이 모든 것이 무엇인 지 이해해봅시다.

`password` "흐름"은 보안 및 인증을 처리하기 위해, OAuth2에 정의된 방법 ("흐름들") 중 하나입니다.

OAuth2는 백엔드 또는 API가 사용자를 인증하는 서버와 독립적일 수 있게 설계 되었습니다.

그러나 이 예시에서, API 및 인증을 동일한 **FastAPI** 애플리케이션이 할 것입니다.

따라서, 단순화 된 관점에서 이를 되짚어 봅시다:

* 사용자가 프론트엔드에 `username` 및 `password`를 입력하고, `Enter`를 누릅니다.
* (사용자의 브라우저에서 실행 중인) 프론트엔드는 그 `username` 및 `password`를 (`tokenUrl="token"`을 사용하여 선언된) API의 특정 URL로 보냅니다.
* API는 그 `username` 및 `password`를 확인하고, (아직 구현하지 않은) "토큰"과 함께 응답합니다.
    * "토큰"은 단지 나중에 이 사용자를 검증하기 위해 사용할 수 있는 어떤 내용으로 이루어진 문자열입니다.
    * 일반적으로, 토큰은 일정 시간이 지나면 만료되도록 설정됩니다.
        * 따라서, 사용자는 어떤 부분이 지나면 다시 로그인해야 합니다.
        * 그리고 토큰을 도둑 맞으면, 위험이 적어집니다. 이것이 (대부분의 경우) 평생 작동하는 영구적인 키가 아니기 때문입니다.
* 프론트엔드는 그 토큰을 어딘가에 일시적으로 저장합니다.
* 사용자는 프론트엔드 내부에서 클릭을 통해 프론트엔드 웹 앱의 다른 부분으로 이동합니다.
* 프론트엔드는 API에서 더 많은 데이터를 가져와야 합니다.
    * 그러나 그 특정 엔드포인트에 대한 인증이 필요합니다.
    * 따라서, API로 인증하기 위해, `Bearer ` 값에 토큰을 추가한 `Authorization` 헤더를 보냅니다.
    * 만약 토큰에 `foobar`가 포함된 경우, `Authorization` 헤더의 내용은 다음과 같습니다: `Bearer foobar`.

## **FastAPI**의 `OAuth2PasswordBearer`

**FastAPI**는 이러한 보안 기능을 구현하기 위해, 다양한 추상화 수준에서, 여러 도구를 제공합니다.

이 예시에서, **Bearer** 토큰을 사용한, **비밀번호** 흐름과 함께, **OAuth2**를 사용할 것입니다. `OAuth2PasswordBearer` 클래스를 사용하여 그것을 작동시킬 것입니다.

!!! info "정보"
    "bearer" 토큰은 유일한 선택지가 아닙니다.
    
    그러나 이것은 우리 사용 사례에 가장 적합합니다.

    그리고 이것은 OAuth2 전문가이거나 본인의 필요에 더 적합한 또다른 선택지가 있는 이유를 정확히 알지 않는 이상, 대부분의 사용 사례에 가장 적합할 것입니다

    그 경우, **FastAPI**는 물론 그것을 구축할 도구를 제공합니다.

`OAuth2PasswordBearer` 클래스의 인스턴스를 생성할 때 `tokenUrl` 매개변수를 전달합니다. 이 매개변수는 (사용자의 브라우저에서 실행 중인 프론트엔드) 클라이언트가 토큰을 얻기 위해 `username` 및 `password`를 보내는 데 사용할 URL을 포함합니다.

```Python hl_lines="6"
{!../../../docs_src/security/tutorial001.py!}
```

!!! tip "팁"
    여기서 `tokenUrl="token"`은 아직 생성하지 않은 상대적 URL `token`을 가리킵니다. 상대적 URL이기 때문에, 이것은 `./token`과 동일합니다.

    왜냐하면 상대적 URL을 사용하기 때문에, 만약 API가 `https://example.com/` 위치한다면, 이것은 `https://example.com/token`을 가리킵니다. 그러나 만약 API가 `https://example.com/api/v1/`에 위치한다면, 이것은 `https://example.com/api/v1/token`을 가리킵니다.

    상대적 URL을 사용하는 건 [비하인드 프록시](../../advanced/behind-a-proxy.md){.internal-link target=_blank}와 같은 숙련된 사용 사례에서도 애플리케이션이 계속 작동하는 지 확인하기 위해 중요합니다.

이 매개변수는 엔드포인트 / *경로 작동*을 생성하지 않지만, 클라이언트가 토큰을 얻기 위해 사용해야 할 `/token` URL을 선언합니다. 그 정보는 OpenAPI에 사용되며, 대화형 API 문서 시스템에도 보여집니다.

곧 실제 경로 작동을 생성할 것입니다.

!!! info "정보"
    만약 고지식한 "파이써니스타"라면 `token_url` 대신 `tokenUrl`로 사용된 매개변수 이름의 형태를 싫어할 수 있습니다.

    그것은 왜냐하면 OpenAPI 스펙에도 동일한 이름으로 사용되기 때문입니다. 따라서 만약 이러한 보안 스킴에 대해 더 자세히 조사해봐야 한다면 추가적인 정보를 얻기 위해 단지 이것을 복사 및 붙여넣으면 됩니다.

`oauth2_scheme` 변수는 `OAuth2PasswordBearer`의 인스턴스이지만, 이것은 또한 "호출 가능"합니다.

다음과 같이 호출될 수 있습니다:

```Python
oauth2_scheme(some, parameters)
```

따라서, `Depends`와 함께 사용될 수 있습니다.

### 사용

이제 `Depends`를 사용하여 `oauth2_scheme`을 의존성 내부에 전달할 수 있습니다.

```Python hl_lines="10"
{!../../../docs_src/security/tutorial001.py!}
```

이 의존성은 *경로 작동 함수*의 매개변수 `token`에 할당된 `str`을 제공합니다.

**FastAPI**는 OpenAPI 스키마 내부 (그리고 자동 API 문서) 에 "보안 스킴"을 정의하기 위해서 이 의존성을 사용할 수 있다는 걸 알게 됩니다.

!!! info "기술적 세부사항"
    **FastAPI**는 차례로 `fastapi.security.base.SecurityBase`로부터 상속되는, `fastapi.security.oauth2.OAuth2`로부터 상속을 받기 때문에 OpenAPI 내부 보안 스킴을 정의하기 위해 (의존성 내부에 선언된) `OAuth2PasswordBearer` 클래스를 사용할 수 있다는 걸 알게 됩니다.

    모든 OpenAPI (그리고 자동 API 문서) 와 통합되는 보안 유틸리티는 `SecurityBase`를 상속 받고, 이것이 어떻게 **FastAPI**가 그것들이 OpenAPI에 어떻게 통합되는 지 알 수 있는 이유입니다.

## 그것이 하는 일

`Authorization` 헤더에 대한 요청을 살펴보고, 값이 일부 토큰이 합쳐진 `Bearer `인지 확인하고, 토큰을 `str`로 반환합니다.

만약 `Authorization`을 발견하지 못하거나, 값이 `Bearer ` 토큰을 갖고 있지 않다면, 401 상태 코드 오류 (`UNAUTHORIZED`)로 바로 응답합니다.

심지어 오류를 반환하기 위해 토큰이 존재하는 지 확인하지 않아도 됩니다. 만약 함수가 실행된다면, 그 토큰 내부에 `str`이 있다는 걸 확신할 수 있습니다.

대화형 문서에서 시도해 볼 수 있습니다:

<img src="/img/tutorial/security/image03.png">

아직 토큰의 유효성을 검증하지 않았지만, 이미 그것이 시작되었습니다.

## 요약

결국, 단지 추가적인 3 또는 4 줄 내로, 이미 보안의 근본적인 형태를 갖추게 된 것입니다.
