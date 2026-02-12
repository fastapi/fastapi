# 쿠키 매개변수 모델 { #cookie-parameter-models }

관련있는 **쿠키**들의 그룹이 있는 경우, **Pydantic 모델**을 생성하여 선언할 수 있습니다. 🍪

이를 통해 **여러 위치**에서 **모델을 재사용** 할 수 있고 모든 매개변수에 대한 유효성 검사 및 메타데이터를 한 번에 선언할 수도 있습니다. 😎

/// note | 참고

이 기능은 FastAPI 버전 `0.115.0` 이후부터 지원됩니다. 🤓

///

/// tip | 팁

동일한 기술이 `Query`, `Cookie`, 그리고 `Header`에 적용됩니다. 😎

///

## Pydantic 모델을 사용한 쿠키 { #cookies-with-a-pydantic-model }

**Pydantic 모델**에 필요한 **쿠키** 매개변수를 선언한 다음, 해당 매개변수를 `Cookie`로 선언합니다:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI**는 요청에서 받은 **쿠키**에서 **각 필드**에 대한 데이터를 **추출**하고 정의한 Pydantic 모델을 줍니다.

## 문서 확인하기 { #check-the-docs }

문서 UI `/docs`에서 정의한 쿠키를 볼 수 있습니다:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | 정보

명심하세요, 내부적으로 **브라우저는 쿠키를 특별한 방식으로 처리**하기 때문에 **자바스크립트**가 쉽게 쿠키를 건드릴 수 **없습니다**.

`/docs`에서 **API 문서 UI**로 이동하면 *경로 처리*에 대한 쿠키의 **문서**를 볼 수 있습니다.

하지만 아무리 **데이터를 입력**하고 "실행(Execute)"을 클릭해도, 문서 UI는 **자바스크립트**로 작동하기 때문에 쿠키는 전송되지 않고, 아무 값도 쓰지 않은 것처럼 **오류** 메시지를 보게 됩니다.

///

## 추가 쿠키 금지하기 { #forbid-extra-cookies }

일부 특별한 사용 사례(흔하지는 않겠지만)에서는 수신하려는 쿠키를 **제한**할 수 있습니다.

이제 API는 자신의 <abbr title="This is a joke, just in case. It has nothing to do with cookie consents, but it's funny that even the API can now reject the poor cookies. Have a cookie. 🍪">cookie consent</abbr>를 제어할 수 있는 권한을 갖게 되었습니다. 🤪🍪

Pydantic의 모델 구성을 사용하여 추가(`extra`) 필드를 금지(`forbid`)할 수 있습니다:

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

클라이언트가 **추가 쿠키**를 보내려고 시도하면, **오류** 응답을 받게 됩니다.

동의를 얻기 위해 애쓰는 불쌍한 쿠키 배너(팝업)들, <abbr title="This is another joke. Don't pay attention to me. Have some coffee for your cookie. ☕">API가 거부</abbr>하는데도. 🍪

예를 들어, 클라이언트가 `good-list-please` 값으로 `santa_tracker` 쿠키를 보내려고 하면 클라이언트는 `santa_tracker` <abbr title="Santa disapproves the lack of cookies. 🎅 Okay, no more cookie jokes.">쿠키가 허용되지 않는다</abbr>는 **오류** 응답을 받게 됩니다:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## 요약 { #summary }

**Pydantic 모델**을 사용하여 **FastAPI**에서 <abbr title="Have a last cookie before you go. 🍪">**쿠키**</abbr>를 선언할 수 있습니다. 😎
