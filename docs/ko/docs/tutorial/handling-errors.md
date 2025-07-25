# 에러 처리

API를 사용하는 클라이언트에게 에러를 알려야 하는 상황은 많습니다.

이 클라이언트는 프론트엔드가 있는 브라우저, 다른 사람의 코드, IoT 장치 등일 수 있습니다.

다음과 같은 상황에서 클라이언트에게 알려야 할 수 있습니다:

* 클라이언트가 해당 작업에 대한 충분한 권한이 없는 경우
* 클라이언트가 해당 리소스에 접근할 수 없는 경우
* 클라이언트가 접근하려는 항목이 존재하지 않는 경우
* 등등

이런 경우에는 일반적으로 **400** 범위(400~499)의 **HTTP 상태 코드**를 반환합니다.

이는 200 HTTP 상태 코드(200~299)와 유사합니다. 이러한 "200" 상태 코드는 요청에 어떤 식으로든 "성공"이 있었다는 것을 의미합니다.

400 범위의 상태 코드는 클라이언트에서 에러가 있었다는 것을 의미합니다.

모든 **"404 Not Found"** 에러들(그리고 농담들)을 기억하시나요?

## `HTTPException` 사용하기

클라이언트에게 에러가 있는 HTTP 응답을 반환하려면 `HTTPException`을 사용합니다.

### `HTTPException` 임포트하기

{* ../../docs_src/handling_errors/tutorial001.py hl[1] *}

### 코드에서 `HTTPException` 발생시키기

`HTTPException`은 API와 관련된 추가 데이터가 있는 일반적인 Python 예외입니다.

Python 예외이기 때문에 `return`하지 않고 `raise`합니다.

이는 또한 *경로 동작 함수* 내부에서 호출하는 유틸리티 함수 내부에 있고, 해당 유틸리티 함수 내부에서 `HTTPException`을 발생시키면, *경로 동작 함수*의 나머지 코드를 실행하지 않고, 해당 요청을 즉시 종료하고 `HTTPException`의 HTTP 에러를 클라이언트에게 보낸다는 것을 의미합니다.

값을 반환하는 것보다 예외를 발생시키는 것의 이점은 의존성과 보안에 관한 섹션에서 더 명확해질 것입니다.

이 예제에서는 클라이언트가 존재하지 않는 ID로 항목을 요청할 때, 상태 코드 `404`의 예외를 발생시킵니다:

{* ../../docs_src/handling_errors/tutorial001.py hl[11] *}

### 결과 응답

클라이언트가 `http://example.com/items/foo`(`item_id` `"foo"`)를 요청하면, 해당 클라이언트는 HTTP 상태 코드 200과 다음과 같은 JSON 응답을 받을 것입니다:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

하지만 클라이언트가 `http://example.com/items/bar`(존재하지 않는 `item_id` `"bar"`)를 요청하면, 해당 클라이언트는 HTTP 상태 코드 404("not found" 에러)와 다음과 같은 JSON 응답을 받을 것입니다:

```JSON
{
  "detail": "Item not found"
}
```

/// tip

`HTTPException`을 발생시킬 때, `str`뿐만 아니라 JSON으로 변환할 수 있는 모든 값을 `detail` 매개변수로 전달할 수 있습니다.

`dict`, `list` 등을 전달할 수 있습니다.

이들은 **FastAPI**에 의해 자동으로 처리되어 JSON으로 변환됩니다.

///

## 커스텀 헤더 추가하기

HTTP 에러에 커스텀 헤더를 추가할 수 있는 것이 유용한 상황들이 있습니다. 예를 들어, 일부 유형의 보안을 위해서입니다.

아마도 코드에서 직접 사용할 필요는 없을 것입니다.

하지만 고급 시나리오에서 필요한 경우, 커스텀 헤더를 추가할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial002.py hl[14] *}

## 커스텀 예외 핸들러 설치하기

<a href="https://www.starlette.io/exceptions/" class="external-link" target="_blank">Starlette의 동일한 예외 유틸리티</a>를 사용하여 커스텀 예외 핸들러를 추가할 수 있습니다.

당신(또는 당신이 사용하는 라이브러리)이 `raise`할 수 있는 커스텀 예외 `UnicornException`이 있다고 가정해봅시다.

그리고 이 예외를 FastAPI로 전역적으로 처리하고 싶습니다.

`@app.exception_handler()`로 커스텀 예외 핸들러를 추가할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial003.py hl[5:7,13:18,24] *}

여기서 `/unicorns/yolo`를 요청하면, *경로 동작*이 `UnicornException`을 `raise`할 것입니다.

하지만 이는 `unicorn_exception_handler`에 의해 처리될 것입니다.

따라서 HTTP 상태 코드 `418`과 다음과 같은 JSON 내용으로 깔끔한 에러를 받을 것입니다:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 기술적 세부사항

`from starlette.requests import Request`와 `from starlette.responses import JSONResponse`도 사용할 수 있습니다.

**FastAPI**는 개발자인 당신의 편의를 위해 `starlette.responses`와 동일한 것을 `fastapi.responses`로 제공합니다. 하지만 사용 가능한 대부분의 응답은 Starlette에서 직접 제공됩니다. `Request`도 마찬가지입니다.

///

## 기본 예외 핸들러 오버라이드하기

**FastAPI**에는 몇 가지 기본 예외 핸들러가 있습니다.

이러한 핸들러는 `HTTPException`을 `raise`하고 요청에 유효하지 않은 데이터가 있을 때 기본 JSON 응답을 반환하는 역할을 합니다.

이러한 예외 핸들러를 자신만의 것으로 오버라이드할 수 있습니다.

### 요청 검증 예외 오버라이드하기

요청에 유효하지 않은 데이터가 포함되어 있으면, **FastAPI**는 내부적으로 `RequestValidationError`를 발생시킵니다.

그리고 이에 대한 기본 예외 핸들러도 포함되어 있습니다.

이를 오버라이드하려면 `RequestValidationError`를 임포트하고 `@app.exception_handler(RequestValidationError)`와 함께 사용하여 예외 핸들러를 장식합니다.

예외 핸들러는 `Request`와 예외를 받을 것입니다.

{* ../../docs_src/handling_errors/tutorial004.py hl[2,14:16] *}

이제 `/items/foo`로 이동하면, 다음과 같은 기본 JSON 에러를 받는 대신:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

다음과 같은 텍스트 버전을 받을 것입니다:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs `ValidationError`

/// warning

지금 당신에게 중요하지 않다면 건너뛸 수 있는 기술적 세부사항입니다.

///

`RequestValidationError`는 Pydantic의 <a href="https://docs.pydantic.dev/latest/concepts/models/#error-handling" class="external-link" target="_blank">`ValidationError`</a>의 하위 클래스입니다.

**FastAPI**는 이를 사용하므로, `response_model`에서 Pydantic 모델을 사용하고 데이터에 에러가 있으면 로그에서 에러를 볼 수 있습니다.

하지만 클라이언트/사용자는 이를 보지 못할 것입니다. 대신, 클라이언트는 HTTP 상태 코드 `500`과 함께 "Internal Server Error"를 받을 것입니다.

클라이언트의 *요청*이 아닌 *응답*이나 코드 어딘가에서 Pydantic `ValidationError`가 있다면, 실제로는 코드의 버그이기 때문에 이렇게 되어야 합니다.

그리고 당신이 이를 수정하는 동안, 클라이언트/사용자는 에러에 대한 내부 정보에 접근해서는 안 됩니다. 이는 보안 취약점을 노출할 수 있기 때문입니다.

### `HTTPException` 에러 핸들러 오버라이드하기

같은 방식으로 `HTTPException` 핸들러를 오버라이드할 수 있습니다.

예를 들어, 이러한 에러에 대해 JSON 대신 일반 텍스트 응답을 반환하고 싶을 수 있습니다:

{* ../../docs_src/handling_errors/tutorial004.py hl[3:4,9:11,22] *}

/// note | 기술적 세부사항

`from starlette.responses import PlainTextResponse`도 사용할 수 있습니다.

**FastAPI**는 개발자인 당신의 편의를 위해 `starlette.responses`와 동일한 것을 `fastapi.responses`로 제공합니다. 하지만 사용 가능한 대부분의 응답은 Starlette에서 직접 제공됩니다.

///

### `RequestValidationError` 본문 사용하기

`RequestValidationError`는 유효하지 않은 데이터와 함께 받은 `body`를 포함합니다.

앱을 개발하는 동안 본문을 로그하고 디버그하거나, 사용자에게 반환하는 등의 용도로 사용할 수 있습니다.

{* ../../docs_src/handling_errors/tutorial005.py hl[14] *}

이제 다음과 같은 유효하지 않은 항목을 보내보세요:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

받은 본문을 포함하여 데이터가 유효하지 않다고 알려주는 응답을 받을 것입니다:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI의 `HTTPException` vs Starlette의 `HTTPException`

**FastAPI**는 자체 `HTTPException`을 가지고 있습니다.

그리고 **FastAPI**의 `HTTPException` 에러 클래스는 Starlette의 `HTTPException` 에러 클래스에서 상속됩니다.

유일한 차이점은 **FastAPI**의 `HTTPException`은 `detail` 필드에 JSON으로 변환 가능한 모든 데이터를 허용하는 반면, Starlette의 `HTTPException`은 문자열만 허용한다는 것입니다.

따라서 코드에서 **FastAPI**의 `HTTPException`을 평소처럼 계속 발생시킬 수 있습니다.

하지만 예외 핸들러를 등록할 때는 Starlette의 `HTTPException`에 대해 등록해야 합니다.

이렇게 하면 Starlette의 내부 코드나 Starlette 확장 또는 플러그인의 어떤 부분이 Starlette `HTTPException`을 발생시키면, 핸들러가 이를 잡아 처리할 수 있습니다.

이 예제에서 같은 코드에서 두 `HTTPException`을 모두 사용할 수 있도록, Starlette의 예외는 `StarletteHTTPException`으로 이름이 변경되었습니다:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI**의 예외 핸들러 재사용하기

**FastAPI**의 동일한 기본 예외 핸들러와 함께 예외를 사용하고 싶다면, `fastapi.exception_handlers`에서 기본 예외 핸들러를 임포트하고 재사용할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial006.py hl[2:5,15,21] *}

이 예제에서는 매우 표현적인 메시지로 에러를 출력하고 있지만, 아이디어는 이해할 수 있을 것입니다. 예외를 사용한 다음 기본 예외 핸들러를 재사용할 수 있습니다.
