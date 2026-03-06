# Body - 업데이트 { #body-updates }

## `PUT`으로 교체 업데이트하기 { #update-replacing-with-put }

항목을 업데이트하려면 <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a> 작업을 사용할 수 있습니다.

`jsonable_encoder`를 사용해 입력 데이터를 JSON으로 저장할 수 있는 데이터로 변환할 수 있습니다(예: NoSQL 데이터베이스 사용 시). 예를 들어 `datetime`을 `str`로 변환하는 경우입니다.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT`은 기존 데이터를 **대체**해야 하는 데이터를 받는 데 사용합니다.

### 대체 시 주의사항 { #warning-about-replacing }

즉, `PUT`으로 항목 `bar`를 업데이트하면서 다음과 같은 body를 보낸다면:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

이미 저장된 속성 `"tax": 20.2`가 포함되어 있지 않기 때문에, 입력 모델은 `"tax": 10.5`라는 기본값을 사용하게 됩니다.

그리고 데이터는 그 “새로운” `tax` 값 `10.5`로 저장됩니다.

## `PATCH`로 부분 업데이트하기 { #partial-updates-with-patch }

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> 작업을 사용해 데이터를 *부분적으로* 업데이트할 수도 있습니다.

이는 업데이트하려는 데이터만 보내고, 나머지는 그대로 두는 것을 의미합니다.

/// note | 참고

`PATCH`는 `PUT`보다 덜 일반적으로 사용되고 덜 알려져 있습니다.

그리고 많은 팀이 부분 업데이트에도 `PUT`만 사용합니다.

여러분은 원하는 방식으로 **자유롭게** 사용할 수 있으며, **FastAPI**는 어떤 제한도 강제하지 않습니다.

다만 이 가이드는 의도된 사용 방식이 대략 어떻게 되는지를 보여줍니다.

///

### Pydantic의 `exclude_unset` 파라미터 사용하기 { #using-pydantics-exclude-unset-parameter }

부분 업데이트를 받으려면 Pydantic 모델의 `.model_dump()`에서 `exclude_unset` 파라미터를 사용하는 것이 매우 유용합니다.

예: `item.model_dump(exclude_unset=True)`.

이는 `item` 모델을 만들 때 실제로 설정된 데이터만 포함하는 `dict`를 생성하고, 기본값은 제외합니다.

그 다음 이를 사용해 (요청에서 전송되어) 설정된 데이터만 포함하고 기본값은 생략한 `dict`를 만들 수 있습니다:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### Pydantic의 `update` 파라미터 사용하기 { #using-pydantics-update-parameter }

이제 `.model_copy()`를 사용해 기존 모델의 복사본을 만들고, 업데이트할 데이터가 들어있는 `dict`를 `update` 파라미터로 전달할 수 있습니다.

예: `stored_item_model.model_copy(update=update_data)`:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### 부분 업데이트 요약 { #partial-updates-recap }

정리하면, 부분 업데이트를 적용하려면 다음을 수행합니다:

* (선택 사항) `PUT` 대신 `PATCH`를 사용합니다.
* 저장된 데이터를 조회합니다.
* 그 데이터를 Pydantic 모델에 넣습니다.
* 입력 모델에서 기본값이 제외된 `dict`를 생성합니다(`exclude_unset` 사용).
    * 이렇게 하면 모델의 기본값으로 이미 저장된 값을 덮어쓰지 않고, 사용자가 실제로 설정한 값만 업데이트할 수 있습니다.
* 저장된 모델의 복사본을 만들고, 받은 부분 업데이트로 해당 속성들을 갱신합니다(`update` 파라미터 사용).
* 복사한 모델을 DB에 저장할 수 있는 형태로 변환합니다(예: `jsonable_encoder` 사용).
    * 이는 모델의 `.model_dump()` 메서드를 다시 사용하는 것과 비슷하지만, JSON으로 변환 가능한 데이터 타입으로 값이 확실히 변환되도록 보장합니다(예: `datetime` → `str`).
* 데이터를 DB에 저장합니다.
* 업데이트된 모델을 반환합니다.

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | 팁

동일한 기법을 HTTP `PUT` 작업에서도 실제로 사용할 수 있습니다.

하지만 여기의 예시는 이런 사용 사례를 위해 만들어진 `PATCH`를 사용합니다.

///

/// note | 참고

입력 모델은 여전히 검증된다는 점에 유의하세요.

따라서 모든 속성을 생략할 수 있는 부분 업데이트를 받으려면, 모든 속성이 optional로 표시된(기본값을 가지거나 `None`을 기본값으로 가지는) 모델이 필요합니다.

**업데이트**를 위한 “모든 값이 optional인” 모델과, **생성**을 위한 “필수 값이 있는” 모델을 구분하려면 [추가 모델](extra-models.md){.internal-link target=_blank}에 설명된 아이디어를 사용할 수 있습니다.

///
