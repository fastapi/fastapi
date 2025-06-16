# 본문 - 다중 매개변수

지금부터 `Path`와 `Query`를 어떻게 사용하는지 확인하겠습니다.

요청 본문 선언에 대한 심화 사용법을 알아보겠습니다.

## `Path`, `Query` 및 본문 매개변수 혼합

당연하게 `Path`, `Query` 및 요청 본문 매개변수 선언을 자유롭게 혼합해서 사용할 수 있고, **FastAPI**는 어떤 동작을 할지 압니다.

또한, 기본 값을 `None`으로 설정해 본문 매개변수를 선택사항으로 선언할 수 있습니다.

{* ../../docs_src/body_multiple_params/tutorial001.py hl[19:21] *}

/// note | 참고

이 경우에는 본문으로 부터 가져온 `	item`은 기본값이 `None`이기 때문에, 선택사항이라는 점을 유의해야 합니다.

///

## 다중 본문 매개변수

이전 예제에서 보듯이, *경로 작동*은 아래와 같이 `Item` 속성을 가진 JSON 본문을 예상합니다:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

하지만, 다중 본문 매개변수 역시 선언할 수 있습니다. 예. `item`과 `user`:

{* ../../docs_src/body_multiple_params/tutorial002.py hl[22] *}

이 경우에, **FastAPI**는 이 함수 안에 한 개 이상의 본문 매개변수(Pydantic 모델인 두 매개변수)가 있다고 알 것입니다.

그래서, 본문의 매개변수 이름을 키(필드 명)로 사용할 수 있고, 다음과 같은 본문을 예측합니다:

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

이전과 같이 `item`이 선언 되었더라도, 본문 내의 `item` 키가 있을 것이라고 예측합니다.

///

FastAPI는 요청을 자동으로 변환해, 매개변수의 `item`과 `user`를 특별한 내용으로 받도록 할 것입니다.

복합 데이터의 검증을 수행하고 OpenAPI 스키마 및 자동 문서를 문서화합니다.

## 본문 내의 단일 값

쿼리 및 경로 매개변수에 대한 추가 데이터를 정의하는 `Query`와 `Path`와 같이, **FastAPI**는 동등한 `Body`를 제공합니다.

예를 들어 이전의 모델을 확장하면, `item`과 `user`와 동일한 본문에 또 다른 `importance`라는 키를 갖도록 할 수있습니다.

단일 값을 그대로 선언한다면, **FastAPI**는 쿼리 매개변수로 가정할 것입니다.

하지만, **FastAPI**의 `Body`를 사용해 다른 본문 키로 처리하도록 제어할 수 있습니다:


{* ../../docs_src/body_multiple_params/tutorial003.py hl[23] *}

이 경우에는 **FastAPI**는 본문을 이와 같이 예측할 것입니다:


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

다시 말해, 데이터 타입, 검증, 문서 등을 변환합니다.

## 다중 본문 매개변수와 쿼리

당연히, 필요할 때마다 추가적인 쿼리 매개변수를 선언할 수 있고, 이는 본문 매개변수에 추가됩니다.

기본적으로 단일 값은 쿼리 매개변수로 해석되므로, 명시적으로 `Query`를 추가할 필요가 없고, 아래처럼 할 수 있습니다:

{* ../../docs_src/body_multiple_params/tutorial004.py hl[27] *}

이렇게:

```Python
q: Optional[str] = None
```

/// info | 정보

`Body` 또한 `Query`, `Path` 그리고 이후에 볼 다른 것들처럼 동일한 추가 검증과 메타데이터 매개변수를 갖고 있습니다.

///

## 단일 본문 매개변수 삽입하기

Pydantic 모델 `Item`의 `item`을 본문 매개변수로 오직 한개만 갖고있다고 하겠습니다.

기본적으로 **FastAPI**는 직접 본문으로 예측할 것입니다.

하지만, 만약 모델 내용에 `item `키를 가진 JSON으로 예측하길 원한다면, 추가적인 본문 매개변수를 선언한 것처럼 `Body`의 특별한 매개변수인 `embed`를 사용할 수 있습니다:

{* ../../docs_src/body_multiple_params/tutorial005.py hl[17] *}

아래 처럼:

```Python
item: Item = Body(..., embed=True)
```

이 경우에 **FastAPI**는 본문을 아래 대신에:

```JSON hl_lines="2"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

아래 처럼 예측할 것 입니다:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

## 정리

요청이 단 한개의 본문을 가지고 있더라도, *경로 작동 함수*로 다중 본문 매개변수를 추가할 수 있습니다.

하지만, **FastAPI**는 이를 처리하고, 함수에 올바른 데이터를 제공하며, *경로 작동*으로 올바른 스키마를 검증하고 문서화 합니다.

또한, 단일 값을 본문의 일부로 받도록 선언할 수 있습니다.

그리고 **FastAPI**는 단 한개의 매개변수가 선언 되더라도, 본문 내의 키로 삽입 시킬 수 있습니다.
