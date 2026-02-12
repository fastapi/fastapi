# 응답 상태 코드 { #response-status-code }

응답 모델을 지정하는 것과 같은 방법으로, 어떤 *경로 처리*에서든 `status_code` 매개변수를 사용하여 응답에 사용할 HTTP 상태 코드를 선언할 수도 있습니다:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 등

{* ../../docs_src/response_status_code/tutorial001_py39.py hl[6] *}

/// note | 참고

`status_code` 는 "데코레이터" 메소드(`get`, `post` 등)의 매개변수입니다. 모든 매개변수들과 본문처럼 *경로 처리 함수*가 아닙니다.

///

`status_code` 매개변수는 HTTP 상태 코드를 숫자로 입력받습니다.

/// info | 정보

`status_code` 는 파이썬의 <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a> 와 같은 `IntEnum` 을 입력받을 수도 있습니다.

///

`status_code` 매개변수는:

* 응답에서 해당 상태 코드를 반환합니다.
* 상태 코드를 OpenAPI 스키마(따라서, 사용자 인터페이스에도)에 문서화합니다:

<img src="/img/tutorial/response-status-code/image01.png">

/// note | 참고

일부 응답 코드(다음 섹션 참고)는 응답에 본문이 없다는 것을 나타냅니다.

FastAPI는 이를 알고 있으며, 응답 본문이 없다고 명시하는 OpenAPI 문서를 생성합니다.

///

## HTTP 상태 코드에 대하여 { #about-http-status-codes }

/// note | 참고

만약 HTTP 상태 코드가 무엇인지 이미 알고 있다면, 다음 섹션으로 넘어가세요.

///

HTTP에서는 응답의 일부로 3자리 숫자 상태 코드를 보냅니다.

이 상태 코드들은 이를 식별할 수 있도록 이름이 연결되어 있지만, 중요한 부분은 숫자입니다.

요약하자면:

* `100 - 199` 는 "정보"용입니다. 직접 사용할 일은 거의 없습니다. 이 상태 코드를 갖는 응답은 본문을 가질 수 없습니다.
* **`200 - 299`** 는 "성공적인" 응답을 위한 것입니다. 가장 많이 사용하게 될 유형입니다.
    * `200` 은 기본 상태 코드로, 모든 것이 "OK"임을 의미합니다.
    * 다른 예로는 `201` "생성됨"이 있습니다. 일반적으로 데이터베이스에 새 레코드를 생성한 후 사용합니다.
    * 특별한 경우로 `204` "내용 없음"이 있습니다. 이 응답은 클라이언트에게 반환할 내용이 없을 때 사용되며, 따라서 응답은 본문을 가지면 안 됩니다.
* **`300 - 399`** 는 "리다이렉션"용입니다. 이 상태 코드를 갖는 응답은 본문이 있을 수도 없을 수도 있으며, 본문이 없어야 하는 `304` "수정되지 않음"을 제외합니다.
* **`400 - 499`** 는 "클라이언트 오류" 응답을 위한 것입니다. 아마 두 번째로 가장 많이 사용하게 될 유형입니다.
    * 예를 들어 `404` 는 "찾을 수 없음" 응답을 위해 사용합니다.
    * 클라이언트의 일반적인 오류에는 `400` 을 그냥 사용할 수 있습니다.
* `500 - 599` 는 서버 오류에 사용됩니다. 직접 사용할 일은 거의 없습니다. 애플리케이션 코드의 일부나 서버에서 문제가 발생하면 자동으로 이들 상태 코드 중 하나를 반환합니다.

/// tip | 팁

각 상태 코드와 어떤 코드가 어떤 용도인지 더 알고 싶다면 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr>의 HTTP 상태 코드에 관한 문서</a>를 확인하세요.

///

## 이름을 기억하는 쉬운 방법 { #shortcut-to-remember-the-names }

이전 예시를 다시 확인해보겠습니다:

{* ../../docs_src/response_status_code/tutorial001_py39.py hl[6] *}

`201` 은 "생성됨"을 위한 상태 코드입니다.

하지만 각각의 코드가 무엇을 의미하는지 외울 필요는 없습니다.

`fastapi.status` 의 편의 변수를 사용할 수 있습니다.

{* ../../docs_src/response_status_code/tutorial002_py39.py hl[1,6] *}

이것들은 단지 편의를 위한 것으로, 동일한 숫자를 갖고 있지만, 이를 통해 편집기의 자동완성 기능으로 찾을 수 있습니다:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | 기술 세부사항

`from starlette import status` 역시 사용할 수 있습니다.

**FastAPI**는 개발자인 여러분의 편의를 위해 `fastapi.status` 와 동일한 `starlette.status` 도 제공합니다. 하지만 이것은 Starlette로부터 직접 제공됩니다.

///

## 기본값 변경 { #changing-the-default }

나중에 [고급 사용자 지침서](../advanced/response-change-status-code.md){.internal-link target=_blank}에서, 여기서 선언하는 기본값과 다른 상태 코드를 반환하는 방법을 확인할 수 있습니다.
