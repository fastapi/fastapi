# 에러 처리 { #handling-errors }

API를 사용하는 클라이언트에게 에러를 알려야 하는 상황이 많습니다.

클라이언트는 프론트엔드가 있는 브라우저일 수도 있고, 다른 사람의 코드일 수도 있고, IoT 장치일 수도 있습니다.

다음과 같은 상황을 클라이언트에게 알려야 할 수 있습니다:

* 해당 작업에 대한 권한이 없음
* 해당 리소스에 접근할 수 없음
* 접근하려는 항목이 존재하지 않음
* 기타 등등

이런 경우, 보통 **400**번대(400~499)의 **HTTP 상태 코드**를 반환합니다.

이는 200번대 HTTP 상태 코드(200~299)와 비슷합니다. "200"번대 상태 코드는 요청이 어떻게든 "성공"했다는 의미입니다.

400번대 상태 코드는 클라이언트에서 에러가 발생했다는 의미입니다.

**"404 Not Found"** 에러(그리고 농담들)를 기억하시나요?

## `HTTPException` 사용하기 { #use-httpexception }

에러가 있는 HTTP 응답을 클라이언트에 반환하려면 `HTTPException`을 사용합니다.

### `HTTPException` 임포트하기 { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001.py hl[1] *}

### 코드에서 `HTTPException` 발생시키기 { #raise-an-httpexception-in-your-code }

`HTTPException`은 API 관련 추가 데이터를 담은 일반 파이썬 예외입니다.

파이썬 예외이므로 `return`이 아닌 `raise`를 사용합니다.

*경로 작동 함수* 내에서 호출하는 유틸리티 함수가 있다면, 그 함수 안에서 `HTTPException`을 발생시켰을 때 *경로 작동 함수*의 나머지 코드는 실행되지 않고, 요청이 즉시 종료되며 `HTTPException`의 HTTP 에러가 클라이언트로 전송됩니다.

값을 반환하는 것보다 예외를 발생시키는 것의 이점은 의존성과 보안 섹션에서 더 명확해질 것입니다.

이 예제에서는 클라이언트가 존재하지 않는 ID로 항목을 요청하면 상태 코드 `404`의 예외를 발생시킵니다:

{* ../../docs_src/handling_errors/tutorial001.py hl[11] *}

### 결과 응답 { #the-resulting-response }

클라이언트가 `http://example.com/items/foo`(`item_id`가 `"foo"`)를 요청하면, HTTP 상태 코드 200과 다음 JSON 응답을 받습니다:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

하지만 클라이언트가 `http://example.com/items/bar`(존재하지 않는 `item_id` `"bar"`)를 요청하면, HTTP 상태 코드 404("not found" 에러)와 다음 JSON 응답을 받습니다:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | 팁

`HTTPException`을 발생시킬 때 `detail` 매개변수에 `str`뿐만 아니라 JSON으로 변환 가능한 모든 값을 전달할 수 있습니다.

`dict`, `list` 등을 전달할 수 있습니다.

이들은 **FastAPI**가 자동으로 처리하여 JSON으로 변환합니다.

///

## 커스텀 헤더 추가하기 { #add-custom-headers }

HTTP 에러에 커스텀 헤더를 추가하는 것이 유용할 때가 있습니다. 예를 들어, 일부 보안 시나리오에서 말이죠.

직접 사용할 필요는 거의 없습니다.

하지만 필요한 고급 시나리오를 위해 커스텀 헤더를 추가할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial002.py hl[14] *}

## 커스텀 예외 핸들러 설치하기 { #install-custom-exception-handlers }

<a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">Starlette의 예외 유틸리티</a>를 사용하여 커스텀 예외 핸들러를 추가할 수 있습니다.

여러분(또는 사용하는 라이브러리)이 `raise`할 수 있는 커스텀 예외 `UnicornException`이 있다고 가정해봅시다.

이 예외를 FastAPI에서 전역으로 처리하고 싶습니다.

`@app.exception_handler()`로 커스텀 예외 핸들러를 추가할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial003.py hl[5:7,13:18,24] *}

여기서 `/unicorns/yolo`를 요청하면 *경로 작동*이 `UnicornException`을 `raise`합니다.

하지만 `unicorn_exception_handler`가 이를 처리합니다.

따라서 HTTP 상태 코드 `418`과 다음 JSON 내용의 깔끔한 에러를 받습니다:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 기술적 세부사항

`from starlette.requests import Request`와 `from starlette.responses import JSONResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자 편의를 위해 `starlette.responses`를 `fastapi.responses`로도 제공합니다. 하지만 사용 가능한 대부분의 응답은 Starlette에서 직접 가져옵니다. `Request`도 마찬가지입니다.

///

## 기본 예외 핸들러 오버라이드하기 { #override-the-default-exception-handlers }

**FastAPI**에는 몇 가지 기본 예외 핸들러가 있습니다.

이 핸들러들은 `HTTPException`을 `raise`하거나 요청에 유효하지 않은 데이터가 있을 때 기본 JSON 응답을 반환합니다.

이러한 예외 핸들러를 여러분만의 것으로 오버라이드할 수 있습니다.

### 요청 검증 예외 오버라이드하기 { #override-request-validation-exceptions }

요청에 유효하지 않은 데이터가 포함되면 **FastAPI**는 내부적으로 `RequestValidationError`를 발생시킵니다.

그리고 기본 예외 핸들러도 포함하고 있습니다.

이를 오버라이드하려면 `RequestValidationError`를 임포트하고 `@app.exception_handler(RequestValidationError)`로 예외 핸들러를 데코레이트합니다.

예외 핸들러는 `Request`와 예외를 받습니다.

{* ../../docs_src/handling_errors/tutorial004.py hl[2,14:16] *}

이제 `/items/foo`로 가면 다음과 같은 기본 JSON 에러 대신:

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

다음과 같은 텍스트 버전을 받습니다:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError` vs `ValidationError` { #requestvalidationerror-vs-validationerror }

/// warning | 주의

지금 당장 중요하지 않다면 건너뛸 수 있는 기술 세부사항입니다.

///

`RequestValidationError`는 Pydantic의 <a href="https://docs.pydantic.dev/latest/concepts/models/#error-handling" class="external-link" target="_blank">`ValidationError`</a>의 서브클래스입니다.

**FastAPI**는 이를 사용하여 `response_model`에서 Pydantic 모델을 사용하고 데이터에 에러가 있는 경우 로그에서 에러를 볼 수 있게 합니다.

하지만 클라이언트/사용자는 이를 보지 못합니다. 대신 HTTP 상태 코드 `500`과 함께 "Internal Server Error"를 받습니다.

*응답*이나 코드 어딘가에(클라이언트 *요청*이 아닌) Pydantic `ValidationError`가 있다면 실제로는 코드의 버그이므로 이렇게 되어야 합니다.

그리고 이를 수정하는 동안 클라이언트/사용자는 에러에 대한 내부 정보에 접근할 수 없어야 합니다. 보안 취약점을 노출할 수 있기 때문입니다.

### `HTTPException` 에러 핸들러 오버라이드하기 { #override-the-httpexception-error-handler }

같은 방식으로 `HTTPException` 핸들러를 오버라이드할 수 있습니다.

예를 들어 이런 에러들에 대해 JSON 대신 일반 텍스트 응답을 반환하고 싶을 수 있습니다:

{* ../../docs_src/handling_errors/tutorial004.py hl[3:4,9:11,22] *}

/// note | 기술적 세부사항

`from starlette.responses import PlainTextResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자 편의를 위해 `starlette.responses`를 `fastapi.responses`로도 제공합니다. 하지만 사용 가능한 대부분의 응답은 Starlette에서 직접 가져옵니다.

///

### `RequestValidationError` 본문 사용하기 { #use-the-requestvalidationerror-body }

`RequestValidationError`는 유효하지 않은 데이터와 함께 받은 `body`를 포함합니다.

앱 개발 중 이를 사용하여 본문을 로깅하고 디버그하거나 사용자에게 반환할 수 있습니다.

{* ../../docs_src/handling_errors/tutorial005.py hl[14] *}

이제 다음과 같이 유효하지 않은 항목을 보내보세요:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

데이터가 유효하지 않다는 내용과 받은 본문을 포함한 응답을 받습니다:

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

#### FastAPI의 `HTTPException` vs Starlette의 `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI**는 자체 `HTTPException`을 가지고 있습니다.

**FastAPI**의 `HTTPException` 에러 클래스는 Starlette의 `HTTPException` 에러 클래스를 상속받습니다.

유일한 차이점은 **FastAPI**의 `HTTPException`은 `detail` 필드에 JSON으로 변환 가능한 모든 데이터를 허용하는 반면, Starlette의 `HTTPException`은 문자열만 허용한다는 것입니다.

따라서 여러분의 코드에서 평소처럼 **FastAPI**의 `HTTPException`을 계속 발생시킬 수 있습니다.

하지만 예외 핸들러를 등록할 때는 Starlette의 `HTTPException`에 대해 등록해야 합니다.

이렇게 하면 Starlette 내부 코드나 Starlette 확장/플러그인에서 Starlette `HTTPException`을 발생시켰을 때 여러분의 핸들러가 이를 잡아서 처리할 수 있습니다.

이 예제에서는 같은 코드에서 두 `HTTPException`을 모두 사용하기 위해 Starlette의 예외를 `StarletteHTTPException`으로 이름을 바꿨습니다:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI**의 예외 핸들러 재사용하기 { #reuse-fastapis-exception-handlers }

예외와 함께 **FastAPI**의 기본 예외 핸들러를 사용하고 싶다면 `fastapi.exception_handlers`에서 기본 예외 핸들러를 임포트하여 재사용할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial006.py hl[2:5,15,21] *}

이 예제에서는 아주 설명적인 메시지로 에러를 출력하지만, 핵심은 이해할 수 있을 것입니다. 예외를 사용한 다음 기본 예외 핸들러를 재사용하면 됩니다.
