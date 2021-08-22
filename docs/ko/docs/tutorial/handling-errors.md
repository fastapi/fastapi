# 오류 처리

당신의 API를 사용하는 클라이언트에게 오류를 알려야하는 다양한 상황들이 있습니다.

여기서 클라이언트는 프론트엔드가 있는 브라우저, 다른 사람이 작성한 코드, IoT 기기 등이 될 수 있습니다.

클라이언트에게 다음의 사실을 전달하여야 합니다:

* 클라이언트가 해당 작업을 수행하기에 충분한 권한을 가지지 않았다는 사실
* 클라이언트가 자원에 접근할 수 없다는 사실
* 클라이언트가 접근하려고 하는 항목이 존재하지 않는다는 사실
* 기타 등등

이러한 경우 일반적으로 **4xx**(400에서 499까지)의 **HTTP 상태 코드**를 반환합니다.

이것은 2xx(200에서 299까지)의 HTTP 상태 코드와 유사합니다. "2xx" 상태 코드들은 요청이 "성공"적이었다는 것을 의미합니다.

400번대의 상태 코드들은 클라이언트로부터 오류가 발생했음을 의미합니다.

지금까지 본 **"404 Not Found"** 오류들을 떠올려보세요(그리고 그에 대한 농담들도요)!

## `HTTPException` 사용

클라이언트에게 HTTP 응답을 반환하기 위해 `HTTPException`을 사용합니다.

### `HTTPException` 임포트

```Python hl_lines="1" 
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### 코드에서 `HTTPException` 발생시키기

`HTTPException`은 API에 대한 추가적인 데이터를 포함한 일반적인 파이썬 예외입니다.

파이썬 예외이기 때문에, 반환(`return`)하지 않고 발생(`raise`)시킵니다.

이것은 만약 당신이 *경로 동작 함수*의 내부에서 호출하는 유틸리티 함수 내부에 있고, 해당 유틸리티 함수 내부에서 `HTTPException`을 발생시키는 경우, *경로 동작 함수*의 나머지 부분을 실행하는 대신 즉시 요청에 대한 작업을 중단하고 `HTTPException`에 따른 HTTP 오류를 클라이언트에게 전송한다는 것을 의미합니다.

예외 처리를 함에 있어 값을 반환(`return`)하는 것보다 발생시키는 것의 이점은 종속 및 보안(Dependencies and Security) 섹션에서 깊게 다룰 것입니다.

일례로, 클라이언트가 존재하지 않는 항목의 ID를 요청하는 경우,  다음과 같은 방법으로 상태 코드 `404`와 함께 예외 처리를 할 수 있습니다.

```Python hl_lines="11" 
{!../../../docs_src/handling_errors/tutorial001.py!}
```

### 결과 응답

클라이언트가 `http://example.com/items/foo`(`item_id`가 `"foo"`인 항목)로 요청을 보냈다면, 클라이언트는 HTTP 상태코드 200과 다음과 같은 JSON 응답을 받게 될 것입니다:

```JSON
{  
    "item": "The Foo Wrestlers"
}
```

하지만 클라이언트가 `http://example.com/items/bar` (`item_id`가 `"bar"`인 항목 없음)로 요청을 보낸다면, 클라이언트는 HTTP 상태코드 404("찾을 수 없음(not found)" 오류)와 다음의 JSON 응답을 받게 될 것입니다:

```JSON
{  
    "detail": "Item not found"
}
```

!!! tip "팁"
    `HTTPException`을 발생시킬 때, `str` 뿐 아니라 JSON으로 변환 가능한 모든 값을 `detail` 매개변수로 전달할 수 있습니다.

    `dict`, `list` 등을 전달할 수 있습니다.

    이들은 **FastAPI**에 의해 자동적으로 처리되고 JSON으로 변환됩니다.

## 사용자 정의 헤더 추가

HTTP 오류에 사용자 정의 헤더를 추가하는 것이 유용한 경우들이 있습니다. 예를들어, 몇몇 보안 문제의 경우 그러합니다.

코드에서 이것을 직접 사용할 필요는 없을 수 있습니다.

그러나 고급 시나리오에서 필요한 경우, 사용자 정의 헤더를 추가하는 것이 가능합니다.

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial002.py!}
```

## 사용자 정의 예외 처리기(exception handler) 설치

<a href="https://www.starlette.io/exceptions/" class="external-link" target="_blank">Starlette과 동일한 예외 유틸리티</a>를 사용하여 사용자 정의 예외 처리기를 추가할 수 있습니다.

당신 또는 당신이 사용하는 라이브러리가 사용자 정의 예외인 `UnicornException`을  발생(`raise`) 시키고자 한다고 가정해봅시다. 

그리고 당신은 FastAPI를 사용하여 해당 예외를 전역적으로 처리하고자 합니다.

`@app.exception_handler()`를 사용하여 사용자 예외를 추가할 수 있습니다:

```Python hl_lines="5-7  13-18  24" 
{!../../../docs_src/handling_errors/tutorial003.py!}
```

여기서 `/unicorns/yolo`를 요청하면, *경로 동작*은 `UnicornException`을 발생(`raise`)시킬 것입니다.

하지만 이것은 `unicorn_exception_handler` 에 의해 처리됩니다.

따라서 당신은 HTTP 상태코드가 `418`이고, 다음과 같은 JSON 내용을 가진 오류를 받게됩니다:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

!!! note "기술 세부사항"
    `from starlette.requests import Request`와 `from starlette.responses import JSONResponse` 역시 사용할 수 있습니다.

    **FastAPI**는 개발자인 당신의 편의를 위해 `fastapi.responses` 와 동일한 `starlette.responses` 도 제공합니다. 하지만 대부분의 응답들은 Starlette로부터 직접 제공됩니다. 마찬가지로 `Request` 도 그러합니다.

## 기본 예외 처리기 재정의

**FastAPI** 에는 기본 예외 처리기들이 있습니다.

이 예외 처리기들은 당신이 `HTTPException`을 발생(`raise`)시키거나 요청에 유효하지 않은 데이터가 있을 때 기본 JSON 응답들을 반환하는 역할을 합니다.

이 예외 처리기들을 직접 재정의 할 수 있습니다.

### 요청 유효성 검사 예외 재정의

요청에 유효하지 않은 데이터가 있을 때, **FastAPI**는 내부적으로 `RequestValidationError`를 발생시킵니다.

또한 이에 대한 기본적인 예외 처리기도 포함하고 있습니다.

이를 재정의 하기 위해, `RequestValidationError`를 임포트한 후`@app.exception_handler(RequestValidationError)` 데코레이터와 함께 예외 처리기에 사용하세요.

예외 처리기는 `Request`와 예외를 전달받습니다.

```Python hl_lines="2  14-16" 
{!../../../docs_src/handling_errors/tutorial004.py!}
```

이제 `/items/foo`로 요청을 보내면, 기본 JSON 오류를 받는 대신:

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

다음과 같은 텍스트를 받게 될 것입니다:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs `ValidationError`

!!! warning "주의"
    이 부분은 당신에게 지금 중요하지 않다면 넘어가도 무관한 기술 세부사항입니다.

`RequestValidationError` 는 Pydantic의 <a href="https://pydantic-docs.helpmanual.io/#error-handling" class="external-link" target="_blank">`ValidationError`</a>의 하위 클래스입니다.

**FastAPI**가 이것을 사용하기 때문에 당신이 `response_model`에서 Pydantic 모델을 사용하고, 당신의 데이터에 오류가 있는 경우 로그에서 오류를 확인할 수 있습니다.

하지만 클라이언트와 사용자는 이를 볼 수 없습니다. 대신, 클라이언트는 HTTP 상태 코드 `500` 과 함께 "내부 서버 오류(Internal Server Error)"를 전달 받습니다.

만약 클라이언트의 *요청(request)*이 아닌 *응답(response)*이나 코드 어딘가에 Pydantic의 `ValidationError` 가 있는 경우, 이것은 코드 내에 버그가 있음을 의미하기 때문입니다.

당신이 해당 버그를 해결하는 동안 보안 취약점이 노출되는 것을 방지하기 위해 클라이언트와 사용자는 오류에 관한 내부 정보에 접근할 수 없습니다.

### `HTTPException` 예외 처리기 재정의

같은 방식으로 `HTTPException` 처리기를 재정의할 수 있습니다.

예를 들어, 이 오류들에 대해 JSON 대신 일반 텍스트를 반환하고자 할 수 있습니다:

```Python hl_lines="3-4  9-11  22" 
{!../../../docs_src/handling_errors/tutorial004.py!}
```

!!! note "기술 세부사항"
    `from starlette.responses import JSONResponse` 역시 사용할 수 있습니다.

    **FastAPI**는 개발자인 당신의 편의를 위해 `fastapi.responses`와 동일한 `starlette.responses`도 제공합니다. 하지만 대부분의 응답들은 Starlette로부터 직접 제공됩니다.

### `RequestValidationError` 본문 사용

`RequestValidationError` 는 유효하지 않은 데이터와 함께 받은 `body`를 포함합니다.

당신은 어플리케이션을 개발하는 동안 본문을 로그에 기록하고, 디버깅하고, 사용자에게 반환하는 작업 등을 수행하는 데에 이를 사용할 수 있습니다.

```Python hl_lines="14"
{!../../../docs_src/handling_errors/tutorial005.py!}
```

다음과 같이 유효하지 않은 항목을 전송하면:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

데이터가 유효하지 않음을 알려주는, 전달받은 본문을 포함한 응답을 받게 될 것입니다.

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

**FastAPI**에는 자체적인 `HTTPException` 이 있습니다.

그리고 **FastAPI**의 `HTTPException` 오류 클래스는 Starlette의 `HTTPException` 오류 클래스를 상속받습니다.

유일한 차이점은, **FastAPI**의 `HTTPException` 을 사용할 경우 응답에 헤더를 추가할 수 있다는 것입니다.

이것은 OAuth 2.0 및 몇몇 보안 유틸리티에 내부적으로 필요/사용됩니다.

따라서, 평소와 같이 코드에서 **FastAP**I의 `HTTPException` 을 계속 발생시킬 수 있습니다.

그러나 예외 처리기를 등록할 때에는, Starlette의 `HTTPException` 에 대하여 등록해야 합니다.

이렇게 하면 Starlette의 내부 코드 또는 Starlette 확장(extension) 또는 플러그인의 일부가 Starlette `HTTPException`을 발생시킬 때, 해당 예외 처리기가 이를 포착하고 처리할 수 있습니다.

아래 예시에서, 두 개의 `HTTPException` 을 같은 코드에서 사용하기 위해, Starlette의 예외는 `StarletteHTTPException` 로 이름을 변경하였습니다.

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI**의 예외 처리기 재사용

어떠한 방식으로든 예외를 사용하면서, **FastAPI**의 동일한 기본 예외 처리기를 사용할 수도 있습니다.

`fastapi.exception_handlers` 로부터 기본 예외 처리기를 임포트하고 재사용합니다:

```Python hl_lines="2-5  15  21"
{!../../../docs_src/handling_errors/tutorial006.py!}
```

상기 예시에서, 감정이 매우 많이 섞인 메시지와 함께 오류를 단순히 `print` 했습니다.

하지만 이를 통해 예외를 사용한 후, 기본 예외 처리기를 다시 사용하는 방법에 대해 알았을 것입니다.
