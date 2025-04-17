# 본문 - 수정

## `PUT`을 이용한 수정

항목을 수정 하기 위해 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a>을 사용할 수 있습니다.

`jsonable_encoder`를 사용하여 입력 데이터를 (예를 들어, NoSQL 데이터베이스에서 사용 가능한) JSON으로 저장 가능하게 변환할 수 있습니다. 예를 들면, `datetime` 자료형을 `str`로 변환하게 됩니다.

```Python hl_lines="30-35"
{!../../../docs_src/body_updates/tutorial001.py!}
```

`PUT`은 기존 데이터를 대체하기 위한 항목을 수신하는 데 사용됩니다.

### 데이터 대체 경고

본문이 포함된 `PUT`을 사용하여 `bar` 항목을 수정하려면:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

이미 저장된 속성 `"tax": 20.2`를 포함하지 않기 때문에 기본값 `"tax": 10.5`를 사용합니다.
그리고 데이터는 `10.5`라는 "새로운" `tax`로 저장됩니다.

## `PATCH`를 이용한 부분 수정

데이터를 부분적으로 수정하기 위해 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> 를 사용할 수도 있습니다.

즉, 수정하려는 데이터만 보내고, 나머지는 그대로 둘 수 있습니다.

!!! note "참고"

    일반적으로 `PATCH`보다 `PUT`이 더 일반적으로 사용되고, 잘 알려져 있습니다.

    그리고 많은 팀이 부분 수정을 할 때도, `PUT`만 사용합니다.

    원하는 대로 **자유롭게** 사용할 수 있습니다, **FastAPI**는 이를 제한하지 않습니다.

    하지만 이 지침서는 각 메서드가 어떻게 사용되는 지를 보여줍니다.

### Pydantic의 `exclude_unset` 매개 변수 사용

Pydantic 모델의 `.dict()`에서 `exclude_unset` 매개변수를 사용하는 것은 부분 수정을 위해 매우 유용합니다.

이것은 `item.dict(exclude_unset=True)`와 같습니다.

이렇게 하면 기본값을 제외하고 `item` 모델을 만들 때 설정한 데이터만 있는 `dict`가 생성됩니다.

위 데이터를 사용하여 설정된 (요청에서 전송된) 데이터만으로 `dict`를 생성하고 기본값을 생략할 수 있습니다:

```Python hl_lines="34"
{!../../../docs_src/body_updates/tutorial002.py!}
```

### Pydantic의 `update` 매개 변수 사용

이제 `.copy()`를 이용하여 기존 모델의 복사본을 만들고 수정할 데이터가 포함된 `dict`와 함께 `update` 매개변수를 전달할 수 있습니다.

예시) `stored_item_model.copy(update=update_data)`:

```Python hl_lines="35"
{!../../../docs_src/body_updates/tutorial002.py!}
```

### 부분 수정 요약

부분 수정을 적용하는 방법을 요약하면:

-   (선택) `PUT` 대신 `PATCH`를 사용합니다.
-   저장된 데이터를 검색합니다.
-   위 데이터를 Pydantic 모델에 넣습니다.
-   위 모델에서 (`exclude_unset`을 사용하여) 기본값 없는 `dict`를 생성합니다.
    -   이렇게 하면 모델에 이미 기본값으로 저장된 값을 재정의하는 대신 클라이언트가 실제로 설정한 값만 수정할 수 있습니다.
-   저장된 모델의 복사본을 만들고, (`update` 매개변수를 사용하여) 수신된 부분 데이터로 속성을 수정합니다.
-   (예를 들면, `jsonable_encoder`를 사용한 것과 같이) 복사된 모델을 DB에 저장할 수 있는 형태로 변환합니다.
    -   이것은 모델의 `.dict()` 메서드를 다시 사용하는 것과 비슷하지만, 예를 들어, `datetime`을 `str`로 변환하듯, 값을 JSON으로 변환될 수 있는 데이터 자료형으로 확인 (및 변환) 합니다.
-   DB에 데이터를 저장합니다.
-   수정된 데이터 모델을 반환합니다.

```Python hl_lines="30-37"
{!../../../docs_src/body_updates/tutorial002.py!}
```

!!! tip "팁"

    실제로 HTTP `PUT` 메서드를 이용하여 이와 동일한 기술을 사용할 수 있습니다.

    그러나 이 예제는 이렇게 사용할 수 있다. 정도만 보여주기 위해 만들어졌으므로 `PATCH`를 이용하는 것이 바람직합니다.

!!! note "참고"

    입력 모델의 검증은 여전히 이뤄집니다.

    따라서, 모든 어트리뷰트를 생략할 수 있는 부분 수정을 위해서는 모든 어트리뷰트가 (기본값을 지정하거나 혹은 `None`을 사용하여) 선택사항으로 표시된 모델이 있어야 합니다.

    **수정**을 위해 모든 선택적 값이 있는 모델과 **생성**을 위해 필수적으로 요구되는 값이 있는 모델을 구별하기 위해서는, [추가 모델](extra-models.md){.internal-link target=_blank}에 있는 방법을 이용할 수 있습니다.
