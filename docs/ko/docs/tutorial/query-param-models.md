# 쿼리 매개변수 모델

연관된 쿼리 **매개변수** 그룹이 있다면 **Pydantic 모델** 을 사용해 선언할 수 있습니다.

이렇게 하면 **여러 곳**에서 **모델을 재사용**할 수 있을 뿐만 아니라, 매개변수에 대한 검증 및 메타데이터도 한 번에 선언할 수 있습니다. 😎

/// note | 참고

이 기능은 FastAPI 버전 `0.115.0`부터 제공됩니다. 🤓

///

## 쿼리 매개변수와 Pydantic 모델

필요한 **쿼리 매개변수**를 **Pydantic 모델** 안에 선언한 다음, 모델을 `Query`로 선언합니다.

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI**는 요청의 **쿼리 매개변수**에서 **각 필드**의 데이터를 **추출**해 정의한 Pydantic 모델로 제공합니다.

## 문서 확인하기

`/docs` 경로의 API 문서에서 매개변수를 확인할 수 있습니다.

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 추가 쿼리 매개변수 금지

몇몇의 특이한 경우에 (흔치 않지만), 허용할 쿼리 매개변수를 **제한**해야할 수 있습니다.

Pydantic 모델 설정에서 `extra` 필드를 `forbid` 로 설정할 수 있습니다.

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

만약 클라이언트가 쿼리 매개변수로 **추가적인** 데이터를 보내려고 하면, 클라이언트는 **에러** 응답을 받게 됩니다.

예를 들어, 아래와 같이 만약 클라이언트가 `tool` 쿼리 매개변수에 `plumbus` 라는 값을 추가해서 보내려고 하면,

```http
https://example.com/items/?limit=10&tool=plumbus
```

클라이언트는 쿼리 매개변수 `tool` 이 허용되지 않는다는 **에러** 응답을 받게 됩니다.

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

## 요약

**FastAPI** 에서 **쿼리 매개변수** 를 선언할 때 **Pydantic 모델** 을 사용할 수 있습니다. 😎

/// tip | 팁

스포일러 경고: Pydantic 모델을 쿠키와 헤더에도 적용할 수 있습니다. 이에 대해서는 이후 튜토리얼에서 다룰 예정입니다. 🤫

///
