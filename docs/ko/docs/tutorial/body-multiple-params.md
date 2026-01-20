# 본문 - 다중 매개변수 { #body-multiple-parameters }

이제 `Path`와 `Query`를 어떻게 사용하는지 확인했으니, 요청 본문 선언에 대한 더 고급 사용법을 살펴보겠습니다.

## `Path`, `Query` 및 본문 매개변수 혼합 { #mix-path-query-and-body-parameters }

먼저, 물론 `Path`, `Query` 및 요청 본문 매개변수 선언을 자유롭게 혼합해서 사용할 수 있고, **FastAPI**는 어떤 동작을 할지 압니다.

또한 기본 값을 `None`으로 설정해 본문 매개변수를 선택사항으로 선언할 수 있습니다:

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | 참고

이 경우에는 본문에서 가져올 `item`이 선택사항이라는 점을 유의하세요. 기본값이 `None`이기 때문입니다.

///

## 다중 본문 매개변수 { #multiple-body-parameters }

이전 예제에서, *경로 처리*는 아래처럼 `Item`의 속성을 가진 JSON 본문을 예상합니다:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

하지만, 다중 본문 매개변수 역시 선언할 수 있습니다. 예. `item`과 `user`:

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}


이 경우에, **FastAPI**는 이 함수에 본문 매개변수가 1개보다 많다는 것을 알아챌 것입니다(두 매개변수가 Pydantic 모델입니다).

그래서, 본문에서 매개변수 이름을 키(필드 이름)로 사용하고, 다음과 같은 본문을 예상합니다:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | 참고

`item`이 이전과 같은 방식으로 선언되었더라도, 이제는 본문에서 `item` 키 안에 있을 것으로 예상된다는 점을 유의하세요.

///

**FastAPI**는 요청에서 자동으로 변환을 수행하여, 매개변수 `item`이 해당하는 내용을 받고 `user`도 마찬가지로 받도록 합니다.

복합 데이터의 검증을 수행하고, OpenAPI 스키마 및 자동 문서에도 그에 맞게 문서화합니다.

## 본문 내의 단일 값 { #singular-values-in-body }

쿼리 및 경로 매개변수에 대한 추가 데이터를 정의하는 `Query`와 `Path`가 있는 것과 같은 방식으로, **FastAPI**는 동등한 `Body`를 제공합니다.

예를 들어 이전 모델을 확장해서, `item`과 `user` 외에도 같은 본문에 `importance`라는 다른 키를 두고 싶을 수 있습니다.

단일 값이므로 그대로 선언하면, **FastAPI**는 이를 쿼리 매개변수라고 가정할 것입니다.

하지만 `Body`를 사용하여 다른 본문 키로 처리하도록 **FastAPI**에 지시할 수 있습니다:

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}


이 경우에는 **FastAPI**가 다음과 같은 본문을 예상할 것입니다:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

다시 말해, 데이터 타입을 변환하고, 검증하고, 문서화하는 등의 작업을 수행합니다.

## 다중 본문 매개변수와 쿼리 { #multiple-body-params-and-query }

물론, 필요할 때마다 어떤 본문 매개변수에 추가로 쿼리 매개변수도 선언할 수 있습니다.

기본적으로 단일 값은 쿼리 매개변수로 해석되므로, 명시적으로 `Query`를 추가할 필요 없이 이렇게 하면 됩니다:

```Python
q: Union[str, None] = None
```

또는 Python 3.10 이상에서는:

```Python
q: str | None = None
```

예를 들어:

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}


/// info | 정보

`Body` 또한 `Query`, `Path` 그리고 이후에 볼 다른 것들과 마찬가지로 동일한 추가 검증과 메타데이터 매개변수를 모두 갖고 있습니다.

///

## 단일 본문 매개변수 삽입하기 { #embed-a-single-body-parameter }

Pydantic 모델 `Item`에서 가져온 단일 `item` 본문 매개변수만 있다고 하겠습니다.

기본적으로 **FastAPI**는 그 본문을 직접 예상합니다.

하지만 추가 본문 매개변수를 선언할 때처럼, `item` 키를 가지고 그 안에 모델 내용이 들어 있는 JSON을 예상하게 하려면, `Body`의 특별한 매개변수 `embed`를 사용할 수 있습니다:

```Python
item: Item = Body(embed=True)
```

다음과 같이요:

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}


이 경우 **FastAPI**는 다음과 같은 본문을 예상합니다:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

다음 대신에:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## 정리 { #recap }

요청은 본문을 하나만 가질 수 있지만, *경로 처리 함수*에 다중 본문 매개변수를 추가할 수 있습니다.

하지만 **FastAPI**는 이를 처리하고, 함수에 올바른 데이터를 제공하며, *경로 처리*에서 올바른 스키마를 검증하고 문서화합니다.

또한 단일 값을 본문의 일부로 받도록 선언할 수 있습니다.

그리고 단 하나의 매개변수만 선언되어 있더라도, **FastAPI**에 본문을 키 안에 삽입하도록 지시할 수 있습니다.
