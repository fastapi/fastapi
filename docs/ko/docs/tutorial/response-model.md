# 응답 모델

어떤 *경로 작동*이든 매개변수 `response_model`를 사용하여 응답을 위한 모델을 선언할 수 있습니다:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 기타.

{* ../../docs_src/response_model/tutorial001.py hl[17] *}

/// note | 참고

`response_model`은 "데코레이터" 메소드(`get`, `post`, 등)의 매개변수입니다. 모든 매개변수들과 본문(body)처럼 *경로 작동 함수*가 아닙니다.

///

Pydantic 모델 어트리뷰트를 선언한 것과 동일한 타입을 수신하므로 Pydantic 모델이 될 수 있지만, `List[Item]`과 같이 Pydantic 모델들의 `list`일 수도 있습니다.

FastAPI는 이 `response_model`를 사용하여:

* 출력 데이터를 타입 선언으로 변환.
* 데이터 검증.
* OpenAPI *경로 작동*의 응답에 JSON 스키마 추가.
* 자동 생성 문서 시스템에 사용.

하지만 가장 중요한 것은:

* 해당 모델의 출력 데이터 제한. 이것이 얼마나 중요한지 아래에서 볼 것입니다.

/// note | 기술 세부사항

응답 모델은 함수의 타입 어노테이션 대신 이 매개변수로 선언하는데, 경로 함수가 실제 응답 모델을 반환하지 않고 `dict`, 데이터베이스 객체나 기타 다른 모델을 `response_model`을 사용하여 필드 제한과 직렬화를 수행하고 반환할 수 있기 때문입니다

///

## 동일한 입력 데이터 반환

여기서 우리는 평문 비밀번호를 포함하는 `UserIn` 모델을 선언합니다:

{* ../../docs_src/response_model/tutorial002.py hl[9,11] *}

그리고 이 모델을 사용하여 입력을 선언하고 같은 모델로 출력을 선언합니다:

{* ../../docs_src/response_model/tutorial002.py hl[17:18] *}

이제 브라우저가 비밀번호로 사용자를 만들 때마다 API는 응답으로 동일한 비밀번호를 반환합니다.

이 경우, 사용자가 스스로 비밀번호를 발신했기 때문에 문제가 되지 않을 수 있습니다.

그러나 동일한 모델을 다른 *경로 작동*에서 사용할 경우, 모든 클라이언트에게 사용자의 비밀번호를 발신할 수 있습니다.

/// danger | 위험

절대로 사용자의 평문 비밀번호를 저장하거나 응답으로 발신하지 마십시오.

///

## 출력 모델 추가

대신 평문 비밀번호로 입력 모델을 만들고 해당 비밀번호 없이 출력 모델을 만들 수 있습니다:

{* ../../docs_src/response_model/tutorial003.py hl[9,11,16] *}

여기서 *경로 작동 함수*가 비밀번호를 포함하는 동일한 입력 사용자를 반환할지라도:

{* ../../docs_src/response_model/tutorial003.py hl[24] *}

...`response_model`을 `UserOut` 모델로 선언했기 때문에 비밀번호를 포함하지 않습니다:

{* ../../docs_src/response_model/tutorial003.py hl[22] *}

따라서 **FastAPI**는 출력 모델에서 선언하지 않은 모든 데이터를 (Pydantic을 사용하여) 필터링합니다.

## 문서에서 보기

자동 생성 문서를 보면 입력 모델과 출력 모델이 각자의 JSON 스키마를 가지고 있음을 확인할 수 있습니다:

<img src="/img/tutorial/response-model/image01.png">

그리고 두 모델 모두 대화형 API 문서에 사용됩니다:

<img src="/img/tutorial/response-model/image02.png">

## 응답 모델 인코딩 매개변수

응답 모델은 아래와 같이 기본값을 가질 수 있습니다:

{* ../../docs_src/response_model/tutorial004.py hl[11,13:14] *}

* `description: Optional[str] = None`은 기본값으로 `None`을 갖습니다.
* `tax: float = 10.5`는 기본값으로 `10.5`를 갖습니다.
* `tags: List[str] = []` 빈 리스트의 기본값으로: `[]`.

그러나 실제로 저장되지 않았을 경우 결과에서 값을 생략하고 싶을 수 있습니다.

예를 들어, NoSQL 데이터베이스에 많은 선택적 속성이 있는 모델이 있지만, 기본값으로 가득 찬 매우 긴 JSON 응답을 보내고 싶지 않습니다.

### `response_model_exclude_unset` 매개변수 사용

*경로 작동 데코레이터* 매개변수를 `response_model_exclude_unset=True`로 설정 할 수 있습니다:

{* ../../docs_src/response_model/tutorial004.py hl[24] *}

이러한 기본값은 응답에 포함되지 않고 실제로 설정된 값만 포함됩니다.

따라서 해당 *경로 작동*에 ID가 `foo`인 항목(items)을 요청으로 보내면 (기본값을 제외한) 응답은 다음과 같습니다:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | 정보

FastAPI는 이를 위해 Pydantic 모델의 `.dict()`의 <a href="https://docs.pydantic.dev/latest/concepts/serialization/#modeldict" class="external-link" target="_blank"> `exclude_unset` 매개변수</a>를 사용합니다.

///

/// info | 정보

아래 또한 사용할 수 있습니다:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

<a href="https://docs.pydantic.dev/latest/concepts/serialization/#modeldict" class="external-link" target="_blank">Pydantic 문서</a>에서 `exclude_defaults` 및 `exclude_none`에 대해 설명한 대로 사용할 수 있습니다.

///

#### 기본값이 있는 필드를 갖는 값의 데이터

하지만 모델의 필드가 기본값이 있어도 ID가 `bar`인 항목(items)처럼 데이터가 값을 갖는다면:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

응답에 해당 값들이 포함됩니다.

#### 기본값과 동일한 값을 갖는 데이터

If the data has the same values as the default ones, like the item with ID `baz`:
ID가 `baz`인 항목(items)처럼 기본값과 동일한 값을 갖는다면:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

`description`, `tax` 그리고 `tags`가 기본값과 같더라도 (기본값에서 가져오는 대신) 값들이 명시적으로 설정되었다는 것을 인지할 정도로 FastAPI는 충분히 똑똑합니다(사실, Pydantic이 충분히 똑똑합니다).

따라서 JSON 스키마에 포함됩니다.

/// tip | 팁

`None` 뿐만 아니라 다른 어떤 것도 기본값이 될 수 있습니다.

리스트(`[]`), `float`인 `10.5` 등이 될 수 있습니다.

///

### `response_model_include` 및 `response_model_exclude`

*경로 작동 데코레이터* 매개변수 `response_model_include` 및 `response_model_exclude`를 사용할 수 있습니다.

이들은 포함(나머지 생략)하거나 제외(나머지 포함) 할 어트리뷰트의 이름과 `str`의 `set`을 받습니다.

Pydantic 모델이 하나만 있고 출력에서 ​​일부 데이터를 제거하려는 경우 빠른 지름길로 사용할 수 있습니다.

/// tip | 팁

하지만 이러한 매개변수 대신 여러 클래스를 사용하여 위 아이디어를 사용하는 것을 추천합니다.

이는 일부 어트리뷰트를 생략하기 위해 `response_model_include` 또는 `response_model_exclude`를 사용하더라도 앱의 OpenAPI(및 문서)가 생성한 JSON 스키마가 여전히 전체 모델에 대한 스키마이기 때문입니다.

비슷하게 작동하는 `response_model_by_alias` 역시 마찬가지로 적용됩니다.

///

{* ../../docs_src/response_model/tutorial005.py hl[31,37] *}

/// tip | 팁

문법 `{"name", "description"}`은 두 값을 갖는 `set`을 만듭니다.

이는 `set(["name", "description"])`과 동일합니다.

///

#### `set` 대신 `list` 사용하기

`list` 또는 `tuple` 대신 `set`을 사용하는 법을 잊었더라도, FastAPI는 `set`으로 변환하고 정상적으로 작동합니다:

{* ../../docs_src/response_model/tutorial006.py hl[31,37] *}

## 요약

응답 모델을 정의하고 개인정보가 필터되는 것을 보장하기 위해 *경로 작동 데코레이터*의 매개변수 `response_model`을 사용하세요.

명시적으로 설정된 값만 반환하려면 `response_model_exclude_unset`을 사용하세요.
