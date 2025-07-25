# Body - 업데이트

## `PUT`으로 교체 업데이트

항목을 업데이트하려면 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> 연산을 사용할 수 있습니다.

`jsonable_encoder`를 사용하여 입력 데이터를 JSON으로 저장할 수 있는 데이터로 변환할 수 있습니다(예: NoSQL 데이터베이스와 함께). 예를 들어, `datetime`을 `str`로 변환하는 것입니다.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT`은 기존 데이터를 교체해야 하는 데이터를 받는 데 사용됩니다.

### 교체에 대한 경고

즉, 다음을 포함하는 본문으로 `PUT`을 사용하여 항목 `bar`를 업데이트하려는 경우:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

입력 모델이 기본값을 가지고 있기 때문에, 포함되지 않은 값 `"tax": 10.5`는 기본값 `"tax": 10.5`로 "업데이트"되지 않고 설정됩니다.

데이터는 다음과 같이 `"tax": 10.5`로 저장됩니다:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
    "tax": 10.5,
}
```

## `PATCH`로 부분 업데이트

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> 연산을 사용하여 데이터를 *부분적으로* 업데이트할 수도 있습니다.

이는 업데이트하려는 데이터만 보내고, 나머지는 변경하지 않고 그대로 두는 것을 의미합니다.

/// note

`PATCH`는 `PUT`보다 덜 일반적으로 사용되고 알려져 있습니다.

그리고 많은 팀이 부분 업데이트에도 `PUT`만 사용합니다.

**어느 쪽을 사용하든 자유롭습니다**, FastAPI는 두 가지 모두에 제한을 두지 않습니다.

하지만 이 가이드는 어떻게 사용되도록 의도되었는지 어느 정도 보여줍니다.

///

### Pydantic의 `exclude_unset` 매개변수 사용

부분 업데이트를 받으려면, Pydantic 모델의 `.model_dump()`에서 `exclude_unset` 매개변수를 사용하는 것이 매우 유용합니다.

`item.model_dump(exclude_unset=True)`와 같이 사용합니다.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[34] *}

이렇게 하면 항목 모델을 생성할 때 설정된 데이터만 포함하는 `dict`이 생성되고, 기본값은 생략됩니다.

그런 다음 이를 사용하여 설정된(요청에서 보낸) 데이터만 포함하는 `dict`을 생성하고, 기본값은 생략할 수 있습니다:

{* ../../docs_src/body_updates/tutorial001_py310.py hl[35:37] *}

### Pydantic의 `update` 매개변수 사용

이제 기존 모델의 `.model_copy()`를 사용하여 업데이트를 생성할 수 있으며, 받은 데이터로 업데이트된 항목과 함께 `update` 매개변수를 `dict`으로 전달할 수 있습니다:

{* ../../docs_src/body_updates/tutorial001_py310.py hl[38:40] *}

### 부분 업데이트 요약

요약하면, 부분 업데이트를 적용하려면:

1. (선택적으로) `PATCH` 대신 `PUT`을 사용합니다.
2. 저장된 데이터를 검색합니다.
3. 해당 데이터를 Pydantic 모델에 넣습니다.
4. 입력 모델에서 기본값이 없는 `dict`을 생성합니다(`exclude_unset` 사용).
    * 이렇게 하면 모델에서 기본값 대신 사용자가 실제로 설정한 값만 업데이트할 수 있습니다.
5. 저장된 모델의 복사본을 생성하여, 받은 부분 업데이트로 해당 속성을 업데이트합니다(`update` 매개변수 사용).
6. 복사된 모델을 데이터베이스에 저장할 수 있는 것으로 변환합니다(예: `jsonable_encoder` 사용).
    * 이는 모델의 `.model_dump()` 메서드를 다시 사용하는 것과 비교할 수 있지만, 가능한 경우 기본값을 포함하여 직렬화됩니다.
7. 데이터를 데이터베이스에 저장합니다.
8. 업데이트된 모델을 반환합니다.
