# 헤더 매개변수 모델

관련 있는 **헤더 매개변수** 그룹이 있는 경우, **Pydantic 모델**을 생성하여 선언할 수 있습니다.

이를 통해 **여러 위치**에서 **모델을 재사용** 할 수 있고 모든 매개변수에 대한 유효성 검사 및 메타데이터를 한 번에 선언할 수도 있습니다. 😎

/// note | 참고

이 기능은 FastAPI 버전 `0.115.0` 이후부터 지원됩니다. 🤓

///

## Pydantic 모델을 사용한 헤더 매개변수

**Pydantic 모델**에 필요한 **헤더 매개변수**를 선언한 다음, 해당 매개변수를 `Header`로 선언합니다:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI**는 요청에서 받은 **헤더**에서 **각 필드**에 대한 데이터를 **추출**하고 정의한 Pydantic 모델을 줍니다.

## 문서 확인하기

문서 UI `/docs`에서 필요한 헤더를 볼 수 있습니다:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## 추가 헤더 금지하기

일부 특별한 사용 사례(흔하지는 않겠지만)에서는 수신하려는 헤더를 **제한**할 수 있습니다.

Pydantic의 모델 구성을 사용하여 추가(`extra`) 필드를 금지(`forbid`)할 수 있습니다:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

클라이언트가 **추가 헤더**를 보내려고 시도하면, **오류** 응답을 받게 됩니다.

예를 들어, 클라이언트가 `plumbus` 값으로 `tool` 헤더를 보내려고 하면, 클라이언트는 헤더 매개변수 `tool`이 허용 되지 않는다는 **오류** 응답을 받게 됩니다:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## 요약

**Pydantic 모델**을 사용하여 **FastAPI**에서 **헤더**를 선언할 수 있습니다. 😎
