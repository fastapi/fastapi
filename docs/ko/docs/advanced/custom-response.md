# 사용자 정의 응답 - HTML, Stream, 파일, 기타 { #custom-response-html-stream-file-others }

기본적으로 **FastAPI**는 JSON 응답을 반환합니다.

[응답을 직접 반환하기](response-directly.md)에서 본 것처럼 `Response`를 직접 반환하여 이를 재정의할 수 있습니다.

그러나 `Response`를 직접 반환하면(또는 `JSONResponse`와 같은 하위 클래스를 반환하면) 데이터가 자동으로 변환되지 않으며(비록 `response_model`을 선언했다 하더라도), 문서도 자동으로 생성되지 않습니다(예를 들어, 생성된 OpenAPI의 일부로 HTTP 헤더 `Content-Type`에 특정 "미디어 타입"을 포함하는 것 등).

하지만 *경로 처리 데코레이터*에서 `response_class` 매개변수를 사용하여 사용할 `Response`(예: 어떤 `Response` 하위 클래스든)를 선언할 수도 있습니다.

*경로 처리 함수*에서 반환하는 내용은 해당 `Response` 안에 담깁니다.

/// note | 참고

미디어 타입이 없는 응답 클래스를 사용하는 경우, FastAPI는 응답에 내용이 없을 것으로 예상하므로 생성된 OpenAPI 문서에서 응답 형식을 문서화하지 않습니다.

///

## JSON 응답 { #json-responses }

기본적으로 FastAPI는 JSON 응답을 반환합니다.

[응답 모델](../tutorial/response-model.md)을 선언하면 FastAPI는 Pydantic을 사용해 데이터를 JSON으로 직렬화합니다.

응답 모델을 선언하지 않으면 FastAPI는 [JSON 호환 가능 인코더](../tutorial/encoder.md)에서 설명한 `jsonable_encoder`를 사용해 데이터를 변환한 뒤 `JSONResponse`에 넣습니다.

`JSONResponse`처럼 JSON 미디어 타입(`application/json`)을 가진 `response_class`를 선언하면, 여러분이 *경로 처리 데코레이터*에서 선언한 Pydantic의 `response_model`로 데이터가 자동 변환(및 필터링)됩니다. 하지만 데이터의 JSON 바이트 직렬화 자체는 Pydantic이 수행하지 않고, `jsonable_encoder`로 변환한 후 `JSONResponse` 클래스에 전달하며, 그 클래스가 Python 표준 JSON 라이브러리를 사용해 바이트로 직렬화합니다.

### JSON 성능 { #json-performance }

요약하면, 최대 성능이 필요하다면 [응답 모델](../tutorial/response-model.md)을 사용하고, *경로 처리 데코레이터*에 `response_class`를 선언하지 마세요.

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTML 응답 { #html-response }

**FastAPI**에서 HTML 응답을 직접 반환하려면 `HTMLResponse`를 사용하세요.

* `HTMLResponse`를 임포트합니다.
* *경로 처리 데코레이터*의 `response_class` 매개변수로 `HTMLResponse`를 전달합니다.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | 정보

`response_class` 매개변수는 응답의 "미디어 타입"을 정의하는 데에도 사용됩니다.

이 경우, HTTP 헤더 `Content-Type`은 `text/html`로 설정됩니다.

그리고 이는 OpenAPI에 그대로 문서화됩니다.

///

### `Response` 반환하기 { #return-a-response }

[응답을 직접 반환하기](response-directly.md)에서 본 것처럼, *경로 처리*에서 응답을 직접 반환하여 재정의할 수도 있습니다.

위의 예제와 동일하게 `HTMLResponse`를 반환하는 코드는 다음과 같을 수 있습니다:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | 경고

*경로 처리 함수*에서 직접 반환된 `Response`는 OpenAPI에 문서화되지 않습니다(예를 들어, `Content-Type`이 문서화되지 않음) 그리고 자동 대화형 문서에도 표시되지 않습니다.

///

/// info | 정보

물론 실제 `Content-Type` 헤더, 상태 코드 등은 반환된 `Response` 객체에서 가져옵니다.

///

### OpenAPI에 문서화하고 `Response` 재정의하기 { #document-in-openapi-and-override-response }

함수 내부에서 응답을 재정의하면서 동시에 OpenAPI에서 "미디어 타입"을 문서화하고 싶다면, `response_class` 매개변수를 사용하면서 `Response` 객체를 반환할 수 있습니다.

이 경우 `response_class`는 OpenAPI *경로 처리*를 문서화하는 데만 사용되고, 실제로는 여러분이 반환한 `Response`가 그대로 사용됩니다.

#### `HTMLResponse` 직접 반환하기 { #return-an-htmlresponse-directly }

예를 들어, 다음과 같이 작성할 수 있습니다:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

이 예제에서 `generate_html_response()` 함수는 HTML을 `str`로 반환하는 대신 이미 `Response`를 생성하고 반환합니다.

`generate_html_response()`를 호출한 결과를 반환함으로써, 기본적인 **FastAPI** 동작을 재정의하는 `Response`를 이미 반환하고 있습니다.

하지만 `response_class`에 `HTMLResponse`를 함께 전달했기 때문에, **FastAPI**는 이를 OpenAPI 및 대화형 문서에서 `text/html`의 HTML로 문서화하는 방법을 알 수 있습니다:

<img src="/img/tutorial/custom-response/image01.png">

## 사용 가능한 응답들 { #available-responses }

다음은 사용할 수 있는 몇 가지 응답들입니다.

`Response`를 사용하여 다른 어떤 것도 반환할 수 있으며, 직접 하위 클래스를 만들 수도 있습니다.

/// note | 기술 세부사항

`from starlette.responses import HTMLResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자인 여러분의 편의를 위해 `starlette.responses`를 `fastapi.responses`로 동일하게 제공하지만, 대부분의 사용 가능한 응답은 Starlette에서 직접 가져옵니다.

///

### `Response` { #response }

기본 `Response` 클래스이며, 다른 모든 응답 클래스가 이를 상속합니다.

이 클래스를 직접 반환할 수 있습니다.

다음 매개변수를 받을 수 있습니다:

* `content` - `str` 또는 `bytes`.
* `status_code` - HTTP 상태 코드를 나타내는 `int`.
* `headers` - 문자열로 이루어진 `dict`.
* `media_type` - 미디어 타입을 나타내는 `str` 예: `"text/html"`.

FastAPI(정확히는 Starlette)가 자동으로 Content-Length 헤더를 포함시킵니다. 또한 `media_type`에 기반하여 Content-Type 헤더를 포함하며, 텍스트 타입의 경우 문자 집합을 추가합니다.

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

텍스트 또는 바이트를 받아 HTML 응답을 반환합니다. 위에서 설명한 내용과 같습니다.

### `PlainTextResponse` { #plaintextresponse }

텍스트 또는 바이트를 받아 일반 텍스트 응답을 반환합니다.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

데이터를 받아 `application/json`으로 인코딩된 응답을 반환합니다.

이는 위에서 설명했듯이 **FastAPI**에서 기본적으로 사용되는 응답 형식입니다.

/// note | 기술 세부사항

하지만 응답 모델 또는 반환 타입을 선언한 경우, 해당 모델이 데이터를 JSON으로 직렬화하는 데 직접 사용되며, 올바른 JSON 미디어 타입의 응답이 `JSONResponse` 클래스를 사용하지 않고 바로 반환됩니다.

이 방식이 최상의 성능을 얻는 이상적인 방법입니다.

///

### `RedirectResponse` { #redirectresponse }

HTTP 리디렉션 응답을 반환합니다. 기본적으로 상태 코드는 307(임시 리디렉션)으로 설정됩니다.

`RedirectResponse`를 직접 반환할 수 있습니다:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

또는 `response_class` 매개변수에서 사용할 수도 있습니다:


{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

이 경우, *경로 처리* 함수에서 URL을 직접 반환할 수 있습니다.

이 경우, 사용되는 `status_code`는 `RedirectResponse`의 기본값인 `307`입니다.

---

`status_code` 매개변수를 `response_class` 매개변수와 함께 사용할 수도 있습니다:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

비동기 제너레이터 또는 일반 제너레이터/이터레이터(`yield`가 있는 함수)를 받아 응답 본문을 스트리밍합니다.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | 기술 세부사항

`async` 작업은 `await`에 도달했을 때만 취소될 수 있습니다. `await`가 없으면 제너레이터(`yield`가 있는 함수)는 제대로 취소될 수 없고, 취소가 요청된 후에도 계속 실행될 수 있습니다.

이 작은 예제는 어떤 `await`도 필요하지 않으므로, 이벤트 루프가 취소를 처리할 기회를 주기 위해 `await anyio.sleep(0)`를 추가합니다.

대규모 또는 무한 스트림에서는 더욱 중요합니다.

///

/// tip | 팁

`StreamingResponse`를 직접 반환하는 대신, [데이터 스트리밍](./stream-data.md)에서의 스타일을 따르는 것이 더 편리하며 백그라운드에서 취소 처리를 해줍니다.

JSON Lines를 스트리밍한다면, [JSON Lines 스트리밍](../tutorial/stream-json-lines.md) 튜토리얼을 확인하세요.

///

### `FileResponse` { #fileresponse }

파일을 비동기로 스트리밍하여 응답합니다.

다른 응답 유형과는 다른 인수를 사용하여 객체를 생성합니다:

* `path` - 스트리밍할 파일의 경로.
* `headers` - 딕셔너리 형식의 사용자 정의 헤더.
* `media_type` - 미디어 타입을 나타내는 문자열. 설정되지 않은 경우 파일 이름이나 경로를 사용하여 추론합니다.
* `filename` - 설정된 경우 응답의 `Content-Disposition`에 포함됩니다.

파일 응답에는 적절한 `Content-Length`, `Last-Modified`, 및 `ETag` 헤더가 포함됩니다.

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

또한 `response_class` 매개변수를 사용할 수도 있습니다:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

이 경우, 경로 처리 함수에서 파일 경로를 직접 반환할 수 있습니다.

## 사용자 정의 응답 클래스 { #custom-response-class }

`Response`를 상속받아 사용자 정의 응답 클래스를 생성하고 사용할 수 있습니다.

예를 들어, [`orjson`](https://github.com/ijl/orjson)을 일부 설정과 함께 사용하고 싶다고 가정해봅시다.

들여쓰기 및 포맷된 JSON을 반환하고 싶다면, orjson 옵션 `orjson.OPT_INDENT_2`를 사용할 수 있습니다.

`CustomORJSONResponse`를 생성할 수 있습니다. 여기서 핵심은 `Response.render(content)` 메서드를 생성하여 내용을 `bytes`로 반환하는 것입니다:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

이제 다음 대신:

```json
{"message": "Hello World"}
```

...이 응답은 이렇게 반환됩니다:

```json
{
  "message": "Hello World"
}
```

물론 JSON 포맷팅보다 더 유용하게 활용할 방법을 찾을 수 있을 것입니다. 😉

### `orjson` 또는 응답 모델 { #orjson-or-response-model }

성능이 목적이라면, `orjson` 응답을 사용하는 것보다 [응답 모델](../tutorial/response-model.md)을 사용하는 편이 더 나을 가능성이 큽니다.

응답 모델을 사용하면 FastAPI는 중간 단계(예: `jsonable_encoder`로의 변환) 없이 Pydantic을 사용해 데이터를 JSON으로 직렬화합니다. 이런 중간 단계는 다른 경우에 발생합니다.

그리고 내부적으로 Pydantic은 JSON 직렬화를 위해 `orjson`과 동일한 Rust 기반 메커니즘을 사용하므로, 응답 모델만으로도 이미 최상의 성능을 얻게 됩니다.

## 기본 응답 클래스 { #default-response-class }

**FastAPI** 클래스 인스턴스 또는 `APIRouter`를 생성할 때 기본으로 사용할 응답 클래스를 지정할 수 있습니다.

이를 정의하는 매개변수는 `default_response_class`입니다.

아래 예제에서 **FastAPI**는 모든 *경로 처리*에서 JSON 대신 기본적으로 `HTMLResponse`를 사용합니다.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | 팁

여전히 이전처럼 *경로 처리*에서 `response_class`를 재정의할 수 있습니다.

///

## 추가 문서화 { #additional-documentation }

OpenAPI에서 `responses`를 사용하여 미디어 타입 및 기타 세부 정보를 선언할 수도 있습니다: [OpenAPI에서 추가 응답](additional-responses.md).
