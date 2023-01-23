# 본문 - 다중 매개변수

`Path` 와 `Query`를 지금까지 어떻게 사용하는지를 파악했고, 이제부터 요청 본문 선언에 대해 좀 더 진전된 사용법을 알아보겠습니다.

## `Path`, `Query`와 본문 매개변수의 혼합

당연하지만, 먼저 `Path`, `Query`와 요청 본문 매개변수 선언을 자유롭게 혼합할 수 있고, **FastAPI**는 무엇을 하려는지 알 것입니다.

그리고 본문 매개변수를 기본 값을 None으로 설정해서, 선택사항으로 선언할 수 있습니다:

=== "Python 3.6 그리고 그 이상"

    ```Python hl_lines="19-21"
    {!> ../../../docs_src/body_multiple_params/tutorial001.py!}
    ```

=== "Python 3.10 그리고 그 이상"

    ```Python hl_lines="17-19"
    {!> ../../../docs_src/body_multiple_params/tutorial001_py310.py!}
    ```

!!! 주의
    주의할 점으로, 이 경우 저 `item`의 경우 본문에서 선택사항으로 가져와질 것입니다. 왜냐하면 None이 기본 값으로 되어있기 때문입니다.

## 다중 본문 매개변수

이전 예제에서, *경로 매개변수*는 `Item`의 속성을 가진 JSON 본문를 기대할 것입니다, 마치:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

하지만 다중 본문 매개변수를 선언할 수 있습니다, 예시: `item` 그리고 `user`:

=== "Python 3.6 그리고 그 이상"

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial002.py!}
    ```

=== "Python 3.10 그리고 그 이상"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial002_py310.py!}
    ```

이러한 경우 **FastAPI**는 한 개 이상의 본문 매개변수가 함수에 있다는 것을 알게 됩니다. (Pydantic모델인 두개의 매개변수).

그렇기에, FastAPI는 매개변수의 이름들을 키(필드 이름)로서 사용하게 될것이며, 기대되는 본문는 다음과 같을 겁니다:

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

!!! 주의
    주의할 점으로, 비록 `item`이 이전과 같은 방식으로 선언되었지만, `item`은 이제 `item`이란 키와 함게 본문 안에 있는 것으로 기대되어 집니다.


**FastAPI**는 요청으로부터 자동 변환을 할 것이며, 이를 통해  매개변수 `item`은 `item`의 상세한 내용을 받을 것이며, 이는  `user`도 동일합니다.

그리고 복합적인 데이터에 대한 검증이 이루어질 것이며, 자동 문서화나 OpenAPI와 같은 것들을 위해 문서화를 하게 될 것입니다.

## 본문 속 단수형 값들

`Query`와 `Path`가 요청과 경로 매개변수를 위해 추가적인 데이터를 정의하도록 할 수 있던 것과 같은 방식으로, **FastAPI**는 동일한 것을 `Body`로 제공합니다.

예를 들어, 이전 모델을 확장시키기 위해, `item`과 `user`뿐만 아니라 같은 본문에 다른 키값인 `importance`를 넣기로 결정할 수 있습니다.

그것이 단수형 값이기에 그렇게 선언했다면, **FastAPI**는 쿼리 매개변수라고 추측할 것입니다.

하지만, **FastAPI**에게 그것을 다른 본문 키처럼 다루도록 `Body`를 사용하여 지시할 수 있습니다:

=== "Python 3.6 그리고 그 이상"

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial003.py!}
    ```

=== "Python 3.10 그리고 그 이상"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial003_py310.py!}
    ```

이 경우 **FastAPI**는 본문를 다음과 같이 예상합니다:

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

다시금 말하지만, **FastAPI**는 데이터 타입을 변경하고, 검증하고, 문서화 하고, 그 외 등등을 할 것입니다.

## 다중 본문 매개변수와 쿼리

물론 추가적인 쿼리 매개변수를 원하면, 원할 때에 어느 본문 매개변수에 추가적으로 선언할 수 있습니다.

기본적으로 단수형 값들은 쿼리 매개변수로 해석되기에, 명시적으로 `Query`를 추가할 필요가 없으며, 그저 다음과 같이:

```Python
q: Union[str, None] = None
```

또는 Python 3.10 그리고 그 이상에서:

```Python
q: str | None = None
```

예를 들어:

=== "Python 3.6 그리고 그 이상"

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004.py!}
    ```

=== "Python 3.10 그리고 그 이상"

    ```Python hl_lines="26"
    {!> ../../../docs_src/body_multiple_params/tutorial004_py310.py!}
    ```

!!! 정보
    `Body` 또한 `Query`,`Path`이나 나중에 보게될 것에서와 같은 추가적인 검증이나 메타데이터 매개변수를 모두 가지고 있습니다.

## 하나의 본문 매개변수 넣기

Pydantic 모델 `Item`에서 오직 하나의 `item` 본문 매개변수를 가지고 있다고 해봅시다.

기본적으로 **FastAPI**는 그 본문를 바로 기대할 것입니다.

하지만 만약 `item` 키를 JSON이 가지기를 기대하고, 모델 내용에 그것이 있기를 바란다면, 추가적인 본문 매개변수를 선언했을 때 처럼, 특별한 `Body` 매개변수 `embed`를 사용할 수 있습니다:

```Python
item: Item = Body(embed=True)
```

실제로:

=== "Python 3.6 그리고 그 이상"

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005.py!}
    ```

=== "Python 3.10 그리고 그 이상"

    ```Python hl_lines="15"
    {!> ../../../docs_src/body_multiple_params/tutorial005_py310.py!}
    ```

이러한 우 **FastAPI**는 본문를 다음과 같이 예상합니다:

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

다음과 같이는 아닙니다:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## 요약

요청이 오직 하나의 요청 본문를 가지고 있다해도, 여러개의 본문 매개변수를 당신의 *경로 실행 함수*에 추가할 수 있습니다.

하짐나 **FastAPI**그것을 처리할 것이며, 당신의 함수에 제대로 된 데이터를 줄 것이고, *경로 실행*속의 올바른 스키마를 검증하고 문서화할 것입니다.

또한 단수형 값들을 본문의 일부분으로서 받아들이게 선언할 수도 있습니다.

그리고 오직 하나의 매개변수가 선언되어 있으면 **FastAPI**에게 본문 속에 있는 키를 내포하도록 할 수 있습니다. 
