# 폼 데이터

JSON 대신에 폼 데이터 필드를 받을 필요가 있을 때, `폼`을 사용할 수 있습니다.

!!! info "정보"
    폼을 사용하기 위해서는 일단 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>를 설치해야 합니다.

    E.g. `pip install python-multipart`.

## `폼` 임포트

`fastapi`에서 `Form`을 임포트합니다:

```Python hl_lines="1"
{!../../../docs_src/request_forms/tutorial001.py!}
```

## `폼` 매개변수 정의하기

`본문`이나 `쿼리`와 같은 방법으로 폼 매개변수도 생성합니다:


```Python hl_lines="7"
{!../../../docs_src/request_forms/tutorial001.py!}
```

예를 들어, Oauth2 사양을 사용할 수 있는 ("비밀번호 흐름"이라고 불리는) 방법은 `username` 과 `password`를 폼데이터로 보내는 것이 필수입니다.


이 <abbr title="specification">사양</abbr>은 정확히 `username` 과 `password`라고 된 필드들이 필요하고 JSON이 아닌 폼 필드로 보내야 합니다.

`폼`만 있으면 `본문`(`쿼리`, `경로`, `쿠키`)와 마찬가지로 같은 메타데이터와 유효성 검사를 선언할 수 있습니다.

!!! info "정보"
    `폼`은 `본문`을 직접적으로 상속받은 클래스입니다.

!!! tip "팁"
    `Form` 없이는 매개변수가 쿼리 매개변수나 본문(JSON) 매개변수로 해석 되기 때문에 폼 본문을 선언하기 위해서는 `Form`을 명시적으로 상용하는 것이 필요합니다.


## "폼 필드"에 대해

HTML 폼(`<form></form>`)이 서버로 데이터를 보내는 방법은 일반적으로 그 데이터를 위해 JSON과는 다른 "특별한" 인코딩 방법을 사용합니다.

**FastAPI** JSON 대신에 정확한 곳에서 그 데이터를 읽을 수 있어야 합니다.

!!! note "기술적인 세부사항"
    폼으로부터 받은 데이터는 일반적으로 "media type" `application/x-www-form-urlencoded`을 이용해서 암호화 됩니다.

    폼이 파일을 포함하고 있을 때는 `multipart/form-data`로 암호화 됩니다. 다음 챕터에서 파일 다루기에 대해 읽을 수 있을 겁니다.

    이런 암호화와 폼필드에 대해 더 읽고싶다면, <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs for <code>POST</code></a>을 참고하세요.

!!! warning "주의"
    *경로 동작*에서 다양한 폼 파라미터를 선언할 수 있지만 요청은 `application/json` 대신에 `application/x-www-form-urlencoded`을 이용해 암호화 된 본문을 가지기 때문에 JSON으로 받기를 예상하는 `본문`필드 또한 선언할 수 없습니다.
    이는 **FastAPI**의 한계가 아니라 HTTP 통신의 일부입니다.

## 요약

입력 매개변수로 폼 데이터를 선언할 때에는 `Form`을 사용하세요.
