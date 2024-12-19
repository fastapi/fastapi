# 폼 데이터

JSON 대신 폼 필드를 받아야 하는 경우 `Form`을 사용할 수 있습니다.

/// info | 정보

폼을 사용하려면, 먼저 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>를 설치하세요.

[가상 환경](../virtual-environments.md){.internal-link target=_blank}을 생성하고 활성화한 다음, 아래와 같이 설치할 수 있습니다:

```console
$ pip install python-multipart
```

///

## `Form` 임포트하기

`fastapi`에서 `Form`을 임포트합니다:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[3] *}

## `Form` 매개변수 정의하기

`Body` 또는 `Query`와 동일한 방식으로 폼 매개변수를 만듭니다:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[9] *}

예를 들어, OAuth2 사양을 사용할 수 있는 방법 중 하나("패스워드 플로우"라고 함)로 `username`과 `password`를 폼 필드로 보내야 합니다.

<abbr title="specification">사양</abbr>에서는 필드 이름이 `username` 및 `password`로 정확하게 명명되어야 하고, JSON이 아닌 폼 필드로 전송해야 합니다.

`Form`을 사용하면 유효성 검사, 예제, 별칭(예: `username` 대신 `user-name`) 등을 포함하여 `Body`(및 `Query`, `Path`, `Cookie`)와 동일한 구성을 선언할 수 있습니다.

/// info | 정보

`Form`은 `Body`에서 직접 상속되는 클래스입니다.

///

/// tip | 팁

폼 본문을 선언할 때, 폼이 없으면 매개변수가 쿼리 매개변수나 본문(JSON) 매개변수로 해석(interpret)되기 때문에 `Form`을 명시적으로 사용해야 합니다.

///

## "폼 필드"에 대해

HTML 폼(`<form></form>`)이 데이터를 서버로 보내는 방식은 일반적으로 해당 데이터에 대해 "특수" 인코딩을 사용하며, 이는 JSON과 다릅니다.

**FastAPI**는 JSON 대신 올바른 위치에서 해당 데이터를 읽습니다.

/// note | 기술 세부사항

폼의 데이터는 일반적으로 "미디어 유형(media type)" `application/x-www-form-urlencoded`를 사용하여 인코딩합니다.

그러나 폼에 파일이 포함된 경우, `multipart/form-data`로 인코딩합니다. 다음 장에서 파일 처리에 대해 읽을 겁니다.


이러한 인코딩 및 폼 필드에 대해 더 읽고 싶다면, <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><code>POST</code>에 대한 <abbr title="Mozilla Developer Network">MDN</a> 웹 문서를 참조하세요.

///

/// warning | 경고

*경로 작업*에서 여러 `Form` 매개변수를 선언할 수 있지만, JSON으로 수신할 것으로 예상되는 `Body` 필드와 함께 선언할 수 없습니다. 요청 본문은 `application/json` 대신에 `application/x-www-form-urlencoded`를 사용하여 인코딩되기 때문입니다.

이는 **FastAPI**의 제한 사항이 아니며 HTTP 프로토콜의 일부입니다.

///

## 요약

폼 데이터 입력 매개변수를 선언하려면 `Form`을 사용하세요.
