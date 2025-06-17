# 사용자 정의 응답 - HTML, Stream, 파일, 기타

기본적으로, **FastAPI** 응답을 `JSONResponse`를 사용하여 반환합니다.

이를 재정의 하려면 [응답을 직접 반환하기](response-directly.md){.internal-link target=_blank}에서 본 것처럼 `Response`를 직접 반환하면 됩니다.

그러나 `Response` (또는 `JSONResponse`와 같은 하위 클래스)를 직접 반환하면, 데이터가 자동으로 변환되지 않으며 (심지어 `response_model`을 선언했더라도), 문서화가 자동으로 생성되지 않습니다(예를 들어, 생성된 OpenAPI의 일부로 HTTP 헤더 `Content-Type`에 특정 "미디어 타입"을 포함하는 경우).

하지만 *경로 작업 데코레이터*에서 `response_class` 매개변수를 사용하여 원하는 `Response`(예: 모든 `Response` 하위 클래스)를 선언할 수도 있습니다.

*경로 작업 함수*에서 반환하는 내용은 해당 `Response`안에 포함됩니다.

그리고 만약 그 `Response`가 `JSONResponse`와 `UJSONResponse`의 경우 처럼 JSON 미디어 타입(`application/json`)을 가지고 있다면, *경로 작업 데코레이터*에서 선언한 Pydantic의 `response_model`을 사용해 자동으로 변환(및 필터링) 됩니다.

/// note | 참고

미디어 타입이 없는 응답 클래스를 사용하는 경우, FastAPI는 응답에 내용이 없을 것으로 예상하므로 생성된 OpenAPI 문서에서 응답 형식을 문서화하지 않습니다.

///

## `ORJSONResponse` 사용하기

예를 들어, 성능을 극대화하려는 경우, <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">orjson</a>을 설치하여 사용하고 응답을 `ORJSONResponse`로 설정할 수 있습니다.

사용하고자 하는 `Response` 클래스(하위 클래스)를 임포트한 후, **경로 작업 데코레이터*에서 선언하세요.

대규모 응답의 경우, 딕셔너리를 반환하는 것보다 `Response`를 반환하는 것이 훨씬 빠릅니다.

이유는 기본적으로, FastAPI가 내부의 모든 항목을 검사하고 JSON으로 직렬화할 수 있는지 확인하기 때문입니다. 이는 사용자 안내서에서 설명된 [JSON 호환 가능 인코더](../tutorial/encoder.md){.internal-link target=_blank}를 사용하는 방식과 동일합니다. 이를 통해 데이터베이스 모델과 같은 **임의의 객체**를 반환할 수 있습니다.

하지만 반환하는 내용이 **JSON으로 직렬화 가능**하다고 확신하는 경우, 해당 내용을 응답 클래스에 직접 전달할 수 있으며, FastAPI가 반환 내용을 `jsonable_encoder`를 통해 처리한 뒤 응답 클래스에 전달하는 오버헤드를 피할 수 있습니다.

{* ../../docs_src/custom_response/tutorial001b.py hl[2,7] *}

/// info | 정보

`response_class` 매개변수는 응답의 "미디어 타입"을 정의하는 데에도 사용됩니다.

이 경우, HTTP 헤더 `Content-Type`은 `application/json`으로 설정됩니다.

그리고 이는 OpenAPI에 그대로 문서화됩니다.

///

/// tip | 팁

`ORJSONResponse`는 FastAPI에서만 사용할 수 있고 Starlette에서는 사용할 수 없습니다.

///

## HTML 응답

**FastAPI**에서 HTML 응답을 직접 반환하려면 `HTMLResponse`를 사용하세요.

* `HTMLResponse`를 임포트 합니다.
* *경로 작업 데코레이터*의 `response_class` 매개변수로 `HTMLResponse`를 전달합니다.

{* ../../docs_src/custom_response/tutorial002.py hl[2,7] *}

/// info | 정보

`response_class` 매개변수는 응답의 "미디어 타입"을 정의하는 데에도 사용됩니다.

이 경우, HTTP 헤더 `Content-Type`은 `text/html`로 설정됩니다.

그리고 이는 OpenAPI에 그대로 문서화 됩니다.

///

### `Response` 반환하기

[응답을 직접 반환하기](response-directly.md){.internal-link target=_blank}에서 본 것 처럼, *경로 작업*에서 응답을 직접 반환하여 재정의할 수도 있습니다.

위의 예제와 동일하게 `HTMLResponse`를 반환하는 코드는 다음과 같을 수 있습니다:

{* ../../docs_src/custom_response/tutorial003.py hl[2,7,19] *}

/// warning | 경고

*경로 작업 함수*에서 직접 반환된 `Response`는 OpenAPI에 문서화되지 않습니다(예를들어, `Content-Type`이 문서화되지 않음) 자동 대화형 문서에서도 표시되지 않습니다.

///

/// info | 정보

물론 실제 `Content-Type` 헤더, 상태 코드 등은 반환된 `Response` 객체에서 가져옵니다.

///

### OpenAPI에 문서화하고 `Response` 재정의 하기

함수 내부에서 응답을 재정의하면서 동시에 OpenAPI에서 "미디어 타입"을 문서화하고 싶다면, `response_class` 매게변수를 사용하면서 `Response` 객체를 반환할 수 있습니다.

이 경우 `response_class`는 OpenAPI *경로 작업*을 문서화하는 데만 사용되고, 실제로는 여러분이 반환한 `Response`가 그대로 사용됩니다.

### `HTMLResponse`직접 반환하기

예를 들어, 다음과 같이 작성할 수 있습니다:

{* ../../docs_src/custom_response/tutorial004.py hl[7,21,23] *}

이 예제에서, `generate_html_response()` 함수는 HTML을 `str`로 반환하는 대신 이미 `Response`를 생성하고 반환합니다.

`generate_html_response()`를 호출한 결과를 반환함으로써, 기본적인 **FastAPI** 기본 동작을 재정의 하는 `Response`를 이미 반환하고 있습니다.

하지만 `response_class`에 `HTMLResponse`를 함께 전달했기 때문에, FastAPI는 이를 OpenAPI 및 대화형 문서에서 `text/html`로 HTML을 문서화 하는 방법을 알 수 있습니다.

<img src="/img/tutorial/custom-response/image01.png">

## 사용 가능한 응답들

다음은 사용할 수 있는 몇가지 응답들 입니다.

`Response`를 사용하여 다른 어떤 것도 반환 할수 있으며, 직접 하위 클래스를 만들 수도 있습니다.

/// note | 기술 세부사항

`from starlette.responses import HTMLResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자인 여러분의 편의를 위해 `starlette.responses`를 `fastapi.responses`로 제공 하지만, 대부분의 사용 가능한 응답은 Starlette에서 직접 가져옵니다.

///

### `Response`

기본 `Response` 클래스는 다른 모든 응답 클래스의 부모 클래스 입니다.

이 클래스를 직접 반환할 수 있습니다.

다음 매개변수를 받을 수 있습니다:

* `content` - `str` 또는 `bytes`.
* `status_code` - HTTP 상태코드를 나타내는  `int`.
* `headers` - 문자열로 이루어진 `dict`.
* `media_type` - 미디어 타입을 나타내는 `str` 예: `"text/html"`.

FastAPI (실제로는 Starlette)가 자동으로 `Content-Length` 헤더를 포함시킵니다. 또한 `media_type`에 기반하여 `Content-Type` 헤더를 포함하며, 텍스트 타입의 경우 문자 집합을 추가 합니다.

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

### `HTMLResponse`

텍스트 또는 바이트를 받아 HTML 응답을 반환합니다. 위에서 설명한 내용과 같습니다.

### `PlainTextResponse`

텍스트 또는 바이트를 받아 일반 텍스트 응답을 반환합니다.

{* ../../docs_src/custom_response/tutorial005.py hl[2,7,9] *}

### `JSONResponse`

데이터를 받아 `application/json`으로 인코딩된 응답을 반환합니다.

이는 위에서 설명했듯이 **FastAPI**에서 기본적으로 사용되는 응답 형식입니다.

### `ORJSONResponse`

 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>을 사용하여 빠른 JSON 응답을 제공하는 대안입니다. 위에서 설명한 내용과 같습니다.

/// info | 정보

이를 사용하려면 `orjson`을 설치해야합니다. 예: `pip install orjson`.

///

### `UJSONResponse`

<a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>을 사용한 또 다른 JSON 응답 형식입니다.

/// info | 정보

이 응답을 사용하려면 `ujson`을 설치해야합니다. 예: 'pip install ujson`.

///

/// warning | 경고

`ujson` 은 일부 예외 경우를 처리하는 데 있어 Python 내장 구현보다 덜 엄격합니다.

///

{* ../../docs_src/custom_response/tutorial001.py hl[2,7] *}

/// tip | 팁

`ORJSONResponse`가 더 빠른 대안일 가능성이 있습니다.

///

### `RedirectResponse`

HTTP 리디렉션 응답을 반환합니다. 기본적으로 상태 코드는 307(임시 리디렉션)으로 설정됩니다.

`RedirectResponse`를 직접 반환할 수 있습니다.

{* ../../docs_src/custom_response/tutorial006.py hl[2,9] *}

---

또는 `response_class` 매개변수에서 사용할 수도 있습니다:


{* ../../docs_src/custom_response/tutorial006b.py hl[2,7,9] *}

이 경우, *경로 작업* 함수에서 URL을 직접 반환할 수 있습니다.

이 경우, 사용되는 `status_code`는 `RedirectResponse`의 기본값인 `307` 입니다.

---

`status_code` 매개변수를 `response_class` 매개변수와 함께 사용할 수도 있습니다:

{* ../../docs_src/custom_response/tutorial006c.py hl[2,7,9] *}

### `StreamingResponse`

비동기 제너레이터 또는 일반 제너레이터/이터레이터를 받아 응답 본문을 스트리밍 합니다.

{* ../../docs_src/custom_response/tutorial007.py hl[2,14] *}

#### 파일과 같은 객체를 사용한 `StreamingResponse`

파일과 같은 객체(예: `open()`으로 반환된 객체)가 있는 경우, 해당 파일과 같은 객체를 반복(iterate)하는 제너레이터 함수를 만들 수 있습니다.

이 방식으로, 파일 전체를 메모리에 먼저 읽어들일 필요 없이, 제너레이터 함수를 `StreamingResponse`에 전달하여 반환할 수 있습니다.

이 방식은 클라우드 스토리지, 비디오 처리 등의 다양한 라이브러리와 함께 사용할 수 있습니다.

{* ../../docs_src/custom_response/tutorial008.py hl[2,10:12,14] *}

1. 이것이 제너레이터 함수입니다. `yield` 문을 포함하고 있으므로 "제너레이터 함수"입니다.
2. `with` 블록을 사용함으로써, 제너레이터 함수가 완료된 후 파일과 같은 객체가 닫히도록 합니다. 즉, 응답 전송이 끝난 후 닫힙니다.
3. 이 `yield from`은 함수가 `file_like`라는 객체를 반복(iterate)하도록 합니다. 반복된 각 부분은 이 제너레이터 함수(`iterfile`)에서 생성된 것처럼 `yield` 됩니다.

    이렇게 하면 "생성(generating)" 작업을 내부적으로 다른 무언가에 위임하는 제너레이터 함수가 됩니다.

   이 방식을 사용하면 `with` 블록 안에서 파일을 열 수 있어, 작업이 완료된 후 파일과 같은 객체가 닫히는 것을 보장할 수 있습니다.

/// tip | 팁

여기서 표준 `open()`을 사용하고 있기 때문에 `async`와 `await`를 지원하지 않습니다. 따라서 경로 작업은 일반 `def`로 선언합니다.

///

### `FileResponse`

파일을 비동기로 스트리밍하여 응답합니다.

다른 응답 유형과는 다른 인수를 사용하여 객체를 생성합니다:

* `path` - 스트리밍할 파일의 경로.
* `headers` - 딕셔너리 형식의 사용자 정의 헤더.
* `media_type` - 미디어 타입을 나타내는 문자열. 설정되지 않은 경우 파일 이름이나 경로를 사용하여 추론합니다.
* `filename` - 설정된 경우 응답의 `Content-Disposition`에 포함됩니다.

파일 응답에는 적절한 `Content-Length`, `Last-Modified`, 및 `ETag` 헤더가 포함됩니다.

{* ../../docs_src/custom_response/tutorial009.py hl[2,10] *}

또한 `response_class` 매개변수를 사용할 수도 있습니다:

{* ../../docs_src/custom_response/tutorial009b.py hl[2,8,10] *}

이 경우, 경로 작업 함수에서 파일 경로를 직접 반환할 수 있습니다.

## 사용자 정의 응답 클래스

`Response`를 상속받아 사용자 정의 응답 클래스를 생성하고 사용할 수 있습니다.

예를 들어, 포함된 `ORJSONResponse` 클래스에서 사용되지 않는 설정으로 <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">orjson</a>을 사용하고 싶다고 가정해봅시다.

만약 들여쓰기 및 포맷된 JSON을 반환하고 싶다면, `orjson.OPT_INDENT_2` 옵션을 사용할 수 있습니다.

`CustomORJSONResponse`를 생성할 수 있습니다. 여기서 핵심은 `Response.render(content)` 메서드를 생성하여 내용을 `bytes`로 반환하는 것입니다:

{* ../../docs_src/custom_response/tutorial009c.py hl[9:14,17] *}

이제 다음 대신:

```json
{"message": "Hello World"}
```

이 응답은 이렇게 반환됩니다:

```json
{
  "message": "Hello World"
}
```

물론 JSON 포맷팅보다 더 유용하게 활용할 방법을 찾을 수 있을 것입니다. 😉

## 기본 응답 클래스

**FastAPI** 클래스 객체 또는 `APIRouter`를 생성할 때 기본적으로 사용할 응답 클래스를 지정할 수 있습니다.

이를 정의하는 매개변수는 `default_response_class`입니다.

아래 예제에서 **FastAPI**는 모든 경로 작업에서 기본적으로 `JSONResponse` 대신 `ORJSONResponse`를 사용합니다.

{* ../../docs_src/custom_response/tutorial010.py hl[2,4] *}

/// tip | 팁

여전히 이전처럼 *경로 작업*에서 `response_class`를 재정의할 수 있습니다.

///

## 추가 문서화

OpenAPI에서 `responses`를 사용하여 미디어 타입 및 기타 세부 정보를 선언할 수도 있습니다: [OpenAPI에서 추가 응답](additional-responses.md){.internal-link target=_blank}.
