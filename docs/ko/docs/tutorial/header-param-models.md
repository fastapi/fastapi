# 헤더 매개변수 모델 { #header-parameter-models }

관련 있는 **헤더 매개변수** 그룹이 있는 경우, **Pydantic 모델**을 생성하여 선언할 수 있습니다.

이를 통해 **여러 위치**에서 **모델을 재사용할** 수 있고 모든 매개변수에 대한 유효성 검사 및 메타데이터를 한 번에 선언할 수도 있습니다. 😎

/// note | 참고

이 기능은 FastAPI 버전 `0.115.0` 이후부터 지원됩니다. 🤓

///

## Pydantic 모델을 사용한 헤더 매개변수 { #header-parameters-with-a-pydantic-model }

**Pydantic 모델**에 필요한 **헤더 매개변수**를 선언한 다음, 해당 매개변수를 `Header`로 선언합니다:

{* ../../docs_src/header_param_models/tutorial001.py hl[9:14,18] *}

**FastAPI**는 요청에서 받은 **헤더**에서 **각 필드**에 대한 데이터를 **추출**하고 정의한 Pydantic 모델을 줍니다.

## 문서 확인하기 { #check-the-docs }

문서 UI `/docs`에서 필요한 헤더를 볼 수 있습니다:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## 추가 헤더 금지하기 { #forbid-extra-headers }

일부 특별한 사용 사례(흔하지는 않겠지만)에서는 수신하려는 헤더를 **제한**할 수 있습니다.

Pydantic의 모델 구성을 사용하여 추가(`extra`) 필드를 금지(`forbid`)할 수 있습니다:

{* ../../docs_src/header_param_models/tutorial002.py hl[10] *}

클라이언트가 **추가 헤더**를 보내려고 시도하면, **오류** 응답을 받게 됩니다.

예를 들어, 클라이언트가 `plumbus` 값으로 `tool` 헤더를 보내려고 하면, 클라이언트는 헤더 매개변수 `tool`이 허용되지 않는다는 **오류** 응답을 받게 됩니다:

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

## 밑줄 변환 비활성화하기 { #disable-convert-underscores }

일반적인 헤더 매개변수와 마찬가지로, 매개변수 이름에 밑줄 문자가 있으면 **자동으로 하이픈으로 변환**됩니다.

예를 들어, 코드에 `save_data` 헤더 매개변수가 있으면, 기대되는 HTTP 헤더는 `save-data`이고, 문서에서도 그렇게 표시됩니다.

어떤 이유로든 이 자동 변환을 비활성화해야 한다면, 헤더 매개변수용 Pydantic 모델에서도 비활성화할 수 있습니다.

{* ../../docs_src/header_param_models/tutorial003.py hl[19] *}

/// warning | 경고

`convert_underscores`를 `False`로 설정하기 전에, 일부 HTTP 프록시와 서버에서는 밑줄이 포함된 헤더 사용을 허용하지 않는다는 점을 염두에 두세요.

///

## 매개변수 모델 조합하기 { #combine-parameter-models }

여러 헤더 매개변수 모델을 개별 헤더 매개변수 및 의존성과 함께 사용할 수 있습니다. [쿼리 매개변수 모델](query-param-models.md#combine-parameter-models)에서 설명한 것처럼 각 모델은 독립적으로 추출되고 검증됩니다.

각 모델의 `extra` 설정은 다른 모델이나 의존성에 선언된 헤더를 포함하여 모든 헤더 매개변수에 적용됩니다. `extra="forbid"`이면 해당 모델에 없는 헤더는 모두 거부됩니다. `extra="allow"`이면 이러한 헤더는 모델의 추가 필드로 포함됩니다.

각 모델은 요청을 읽을 때와 OpenAPI를 생성할 때 모두 자체 `Header(convert_underscores=...)` 설정을 사용합니다. 명시적으로 지정한 필드 별칭은 그대로 헤더 이름으로 사용됩니다.

## 선택적 헤더 매개변수 모델 { #optional-header-parameter-models }

헤더 매개변수 그룹을 선택적으로 만들려면, 모델에 `| None`을 사용하고 기본값을 `None`으로 선언하세요.

{* ../../docs_src/header_param_models/tutorial004.py hl[15] *}

`x-client-name`과 `x-client-version`이 모두 전송되지 않으면 `client`는 `None`입니다. 둘 중 하나라도 전송되면 FastAPI는 모델을 검증하며 두 필드를 모두 요구합니다.

기본값, 추가 필드, OpenAPI에 대해서는 [선택적 쿼리 매개변수 모델](query-param-models.md#optional-query-parameter-models)과 같은 규칙이 적용됩니다.

`Host` 같은 헤더도 모델의 `extra` 설정을 따릅니다. `extra="allow"`이면 선언된 두 필드가 모두 제공되지 않아도 이러한 헤더로 인해 모델이 제공된 것으로 간주됩니다.

## 요약 { #summary }

**Pydantic 모델**을 사용하여 **FastAPI**에서 **헤더**를 선언할 수 있습니다. 😎
