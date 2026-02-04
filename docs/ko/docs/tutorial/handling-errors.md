# 오류 처리 { #handling-errors }

API를 사용하는 클라이언트에 오류를 알려야 하는 상황은 많이 있습니다.

이 클라이언트는 프론트엔드가 있는 브라우저일 수도 있고, 다른 사람이 작성한 코드일 수도 있고, IoT 장치일 수도 있습니다.

클라이언트에 다음과 같은 내용을 알려야 할 수도 있습니다:

* 클라이언트가 해당 작업을 수행할 충분한 권한이 없습니다.
* 클라이언트가 해당 리소스에 접근할 수 없습니다.
* 클라이언트가 접근하려고 한 항목이 존재하지 않습니다.
* 등등.

이런 경우 보통 **400**번대(400에서 499) 범위의 **HTTP 상태 코드**를 반환합니다.

이는 200번대 HTTP 상태 코드(200에서 299)와 비슷합니다. "200" 상태 코드는 어떤 형태로든 요청이 "성공"했음을 의미합니다.

400번대 상태 코드는 클라이언트 측에서 오류가 발생했음을 의미합니다.

**"404 Not Found"** 오류(그리고 농담들)도 다들 기억하시죠?

## `HTTPException` 사용하기 { #use-httpexception }

클라이언트에 오류가 포함된 HTTP 응답을 반환하려면 `HTTPException`을 사용합니다.

### `HTTPException` 가져오기 { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py39.py hl[1] *}

### 코드에서 `HTTPException` 발생시키기 { #raise-an-httpexception-in-your-code }

`HTTPException`은 API와 관련된 추가 데이터를 가진 일반적인 Python 예외입니다.

Python 예외이므로 `return` 하는 것이 아니라 `raise` 합니다.

이는 또한, *경로 처리 함수* 내부에서 호출하는 유틸리티 함수 안에서 `HTTPException`을 `raise`하면, *경로 처리 함수*의 나머지 코드는 실행되지 않고 즉시 해당 요청이 종료되며 `HTTPException`의 HTTP 오류가 클라이언트로 전송된다는 뜻입니다.

값을 반환하는 것보다 예외를 발생시키는 것의 이점은 의존성과 보안에 대한 섹션에서 더 분명해집니다.

이 예시에서는, 클라이언트가 존재하지 않는 ID로 항목을 요청하면 상태 코드 `404`로 예외를 발생시킵니다:

{* ../../docs_src/handling_errors/tutorial001_py39.py hl[11] *}

### 결과 응답 { #the-resulting-response }

클라이언트가 `http://example.com/items/foo`( `item_id` `"foo"`)를 요청하면, HTTP 상태 코드 200과 다음 JSON 응답을 받습니다:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

하지만 클라이언트가 `http://example.com/items/bar`(존재하지 않는 `item_id` `"bar"`)를 요청하면, HTTP 상태 코드 404("not found" 오류)와 다음 JSON 응답을 받습니다:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | 팁

`HTTPException`을 발생시킬 때 `detail` 파라미터로 `str`만 전달할 수 있는 것이 아니라, JSON으로 변환할 수 있는 어떤 값이든 전달할 수 있습니다.

`dict`, `list` 등을 전달할 수 있습니다.

이들은 **FastAPI**가 자동으로 처리해 JSON으로 변환합니다.

///

## 커스텀 헤더 추가하기 { #add-custom-headers }

HTTP 오류에 커스텀 헤더를 추가할 수 있으면 유용한 상황이 있습니다. 예를 들어 특정 보안 유형에서 그렇습니다.

아마 코드에서 직접 사용할 일은 거의 없을 것입니다.

하지만 고급 시나리오에서 필요하다면 커스텀 헤더를 추가할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial002_py39.py hl[14] *}

## 커스텀 예외 핸들러 설치하기 { #install-custom-exception-handlers }

<a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">Starlette의 동일한 예외 유틸리티</a>를 사용해 커스텀 예외 핸들러를 추가할 수 있습니다.

여러분(또는 사용하는 라이브러리)이 `raise`할 수 있는 커스텀 예외 `UnicornException`이 있다고 가정해 봅시다.

그리고 이 예외를 FastAPI에서 전역적으로 처리하고 싶다고 해봅시다.

`@app.exception_handler()`로 커스텀 예외 핸들러를 추가할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial003_py39.py hl[5:7,13:18,24] *}

여기서 `/unicorns/yolo`를 요청하면, *경로 처리*가 `UnicornException`을 `raise`합니다.

하지만 `unicorn_exception_handler`가 이를 처리합니다.

따라서 HTTP 상태 코드 `418`과 다음 JSON 내용을 가진 깔끔한 오류를 받게 됩니다:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 기술 세부사항

`from starlette.requests import Request`와 `from starlette.responses import JSONResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자의 편의를 위해 `starlette.responses`를 `fastapi.responses`로도 동일하게 제공합니다. 하지만 사용 가능한 대부분의 응답은 Starlette에서 직접 옵니다. `Request`도 마찬가지입니다.

///

## 기본 예외 핸들러 오버라이드하기 { #override-the-default-exception-handlers }

**FastAPI**에는 몇 가지 기본 예외 핸들러가 있습니다.

이 핸들러들은 `HTTPException`을 `raise`했을 때, 그리고 요청에 유효하지 않은 데이터가 있을 때 기본 JSON 응답을 반환하는 역할을 합니다.

이 예외 핸들러들을 여러분의 것으로 오버라이드할 수 있습니다.

### 요청 검증 예외 오버라이드하기 { #override-request-validation-exceptions }

요청에 유효하지 않은 데이터가 포함되면, **FastAPI**는 내부적으로 `RequestValidationError`를 `raise`합니다.

그리고 이에 대한 기본 예외 핸들러도 포함되어 있습니다.

이를 오버라이드하려면 `RequestValidationError`를 가져오고, `@app.exception_handler(RequestValidationError)`로 예외 핸들러를 데코레이트해 사용하세요.

예외 핸들러는 `Request`와 예외를 받습니다.

{* ../../docs_src/handling_errors/tutorial004_py39.py hl[2,14:19] *}

이제 `/items/foo`로 이동하면, 다음과 같은 기본 JSON 오류 대신:

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

다음과 같은 텍스트 버전을 받게 됩니다:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### `HTTPException` 오류 핸들러 오버라이드하기 { #override-the-httpexception-error-handler }

같은 방식으로 `HTTPException` 핸들러도 오버라이드할 수 있습니다.

예를 들어, 이런 오류들에 대해 JSON 대신 일반 텍스트 응답을 반환하고 싶을 수 있습니다:

{* ../../docs_src/handling_errors/tutorial004_py39.py hl[3:4,9:11,25] *}

/// note | 기술 세부사항

`from starlette.responses import PlainTextResponse`를 사용할 수도 있습니다.

**FastAPI**는 개발자의 편의를 위해 `starlette.responses`를 `fastapi.responses`로도 동일하게 제공합니다. 하지만 사용 가능한 대부분의 응답은 Starlette에서 직접 옵니다.

///

/// warning | 경고

`RequestValidationError`에는 검증 오류가 발생한 파일 이름과 줄 정보가 포함되어 있어, 원한다면 관련 정보와 함께 로그에 표시할 수 있다는 점을 유념하세요.

하지만 이는 단순히 문자열로 변환해 그 정보를 그대로 반환하면 시스템에 대한 일부 정보를 누설할 수 있다는 뜻이기도 합니다. 그래서 여기의 코드는 각 오류를 독립적으로 추출해 보여줍니다.

///

### `RequestValidationError`의 body 사용하기 { #use-the-requestvalidationerror-body }

`RequestValidationError`에는 유효하지 않은 데이터와 함께 받은 `body`가 포함됩니다.

앱을 개발하는 동안 body를 로그로 남기고 디버그하거나, 사용자에게 반환하는 등으로 사용할 수 있습니다.

{* ../../docs_src/handling_errors/tutorial005_py39.py hl[14] *}

이제 다음처럼 유효하지 않은 item을 보내보세요:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

받은 body를 포함해 데이터가 유효하지 않다고 알려주는 응답을 받게 됩니다:

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

**FastAPI**에는 자체 `HTTPException`이 있습니다.

그리고 **FastAPI**의 `HTTPException` 오류 클래스는 Starlette의 `HTTPException` 오류 클래스를 상속합니다.

유일한 차이는 **FastAPI**의 `HTTPException`은 `detail` 필드에 JSON으로 변환 가능한 어떤 데이터든 받을 수 있는 반면, Starlette의 `HTTPException`은 문자열만 받을 수 있다는 점입니다.

따라서 코드에서는 평소처럼 **FastAPI**의 `HTTPException`을 계속 `raise`하면 됩니다.

하지만 예외 핸들러를 등록할 때는 Starlette의 `HTTPException`에 대해 등록해야 합니다.

이렇게 하면 Starlette 내부 코드의 어떤 부분, 또는 Starlette 확장/플러그인이 Starlette `HTTPException`을 `raise`하더라도, 여러분의 핸들러가 이를 잡아서 처리할 수 있습니다.

이 예시에서는 동일한 코드에서 두 `HTTPException`을 모두 사용할 수 있도록, Starlette의 예외를 `StarletteHTTPException`으로 이름을 바꿉니다:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI**의 예외 핸들러 재사용하기 { #reuse-fastapis-exception-handlers }

예외를 사용하면서 **FastAPI**의 동일한 기본 예외 핸들러도 함께 사용하고 싶다면, `fastapi.exception_handlers`에서 기본 예외 핸들러를 가져와 재사용할 수 있습니다:

{* ../../docs_src/handling_errors/tutorial006_py39.py hl[2:5,15,21] *}

이 예시에서는 매우 표현력 있는 메시지로 오류를 출력만 하고 있지만, 요지는 이해하셨을 겁니다. 예외를 사용한 뒤 기본 예외 핸들러를 그대로 재사용할 수 있습니다.
