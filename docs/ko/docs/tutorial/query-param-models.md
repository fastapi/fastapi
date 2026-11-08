# 쿼리 매개변수 모델 { #query-parameter-models }

연관된 **쿼리 매개변수** 그룹이 있다면 이를 선언하기 위해 **Pydantic 모델**을 생성할 수 있습니다.

이렇게 하면 **여러 곳**에서 **모델을 재사용**할 수 있을 뿐만 아니라, 매개변수에 대한 검증 및 메타데이터도 한 번에 선언할 수 있습니다. 😎

/// note | 참고

이 기능은 FastAPI 버전 `0.115.0`부터 지원됩니다. 🤓

///

## Pydantic 모델과 쿼리 매개변수 { #query-parameters-with-a-pydantic-model }

필요한 **쿼리 매개변수**를 **Pydantic 모델** 안에 선언한 다음, 매개변수를 `Query`로 선언합니다:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI**는 요청의 **쿼리 매개변수**에서 **각 필드**의 데이터를 **추출**해 정의한 Pydantic 모델을 제공합니다.

## 문서 확인하기 { #check-the-docs }

`/docs`의 문서 UI에서 쿼리 매개변수를 확인할 수 있습니다:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 추가 쿼리 매개변수 금지 { #forbid-extra-query-parameters }

몇몇의 특이한 경우에 (흔치 않지만), 받으려는 쿼리 매개변수를 **제한**하고 싶을 수 있습니다.

Pydantic의 모델 설정을 사용해 어떤 `extra` 필드도 `forbid`할 수 있습니다:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

클라이언트가 **쿼리 매개변수**로 **추가적인** 데이터를 보내려고 하면 **에러** 응답을 받게 됩니다.

예를 들어, 아래와 같이 클라이언트가 `tool` 쿼리 매개변수에 `plumbus` 값을 보내려고 하면:

```http
https://example.com/items/?limit=10&tool=plumbus
```

쿼리 매개변수 `tool`이 허용되지 않는다는 **에러** 응답을 받게 됩니다:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## 매개변수 모델 조합하기 { #combine-parameter-models }

여러 쿼리 매개변수 모델을 선언하고, 개별 쿼리 매개변수나 의존성과 함께 사용할 수 있습니다.

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

요청 매개변수는 모두 같은 수준에 위치합니다.

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

쿼리 문자열에는 `pagination`이나 `filters` 키가 없습니다. 각 모델은 자체 기본값, 필드 검증기, 모델 검증기를 사용하여 쿼리 매개변수를 독립적으로 검증합니다. 모델이나 개별 매개변수를 의존성에 선언한 경우에도 동일하게 적용됩니다.

모델들이 같은 매개변수 이름이나 별칭을 공유하면, 각 모델은 해당 요청 매개변수를 독립적으로 검증합니다. 서로 독립적인 값에는 서로 다른 이름이나 별칭을 사용하세요. OpenAPI는 의존성과 공유하는 매개변수와 마찬가지로, 공유 매개변수를 한 번만 나열하므로 공유 선언은 같은 타입과 제약 조건을 나타내야 합니다.

각 모델의 `extra` 설정은 다른 모델이나 의존성에 선언된 매개변수를 포함하여 모든 쿼리 매개변수에 적용됩니다. `extra="forbid"`이면 해당 모델에 없는 매개변수는 모두 거부됩니다. `extra="allow"`이면 이러한 매개변수는 모델의 추가 필드로 포함됩니다.

`Header`와 `Cookie` 모델에서도 동일하게 동작합니다.

## 선택적 쿼리 매개변수 모델 { #optional-query-parameter-models }

쿼리 매개변수 그룹을 선택적으로 만들려면, 모델에 `| None`을 사용하고 기본값을 `None`으로 선언하세요.

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

`start`와 `end`가 모두 전송되지 않으면 `date_range`는 `None`입니다. 둘 중 하나라도 전송되면 FastAPI는 모델을 검증하며 두 필드를 모두 요구합니다.

기본값 없이 `| None`만 사용하면 매개변수는 여전히 필수입니다.

추가 매개변수는 모델의 `extra` 설정을 따릅니다. 무시되는 추가 매개변수만으로는 모델이 제공된 것으로 간주하지 않습니다.

OpenAPI는 그룹의 필드를 개별적으로 나열하고 선택 사항으로 표시합니다.

선택적 [헤더 매개변수 모델](header-param-models.md#optional-header-parameter-models)과 [쿠키 매개변수 모델](cookie-param-models.md#optional-cookie-parameter-models)도 선언할 수 있습니다.

## 요약 { #summary }

**FastAPI**에서 **쿼리 매개변수**를 선언할 때 **Pydantic 모델**을 사용할 수 있습니다. 😎

/// tip | 팁

스포일러 경고: Pydantic 모델을 쿠키와 헤더에도 사용할 수 있지만, 이에 대해서는 이후 튜토리얼에서 읽게 될 것입니다. 🤫

///
