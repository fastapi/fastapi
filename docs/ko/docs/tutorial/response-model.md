# 응답 모델 - 반환 타입 { #response-model-return-type }

*경로 처리 함수*의 **반환 타입**을 어노테이션하여 응답에 사용될 타입을 선언할 수 있습니다.

함수 **매개변수**에서 입력 데이터를 위해 사용하는 것과 동일하게 **타입 어노테이션**을 사용할 수 있으며, Pydantic 모델, 리스트, 딕셔너리, 정수/불리언 같은 스칼라 값 등을 사용할 수 있습니다.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI는 이 반환 타입을 사용하여:

* 반환된 데이터를 **검증**합니다.
    * 데이터가 유효하지 않다면(예: 필드가 누락된 경우), 이는 *여러분의* 앱 코드가 깨져서 의도한 값을 반환하지 못한다는 의미이며, 잘못된 데이터를 반환하는 대신 서버 오류를 반환합니다. 이렇게 하면 여러분과 클라이언트는 기대한 데이터와 데이터 형태를 받는다는 것을 확실히 할 수 있습니다.
* OpenAPI *경로 처리*의 응답에 **JSON Schema**를 추가합니다.
    * 이는 **자동 문서**에서 사용됩니다.
    * 또한 자동 클라이언트 코드 생성 도구에서도 사용됩니다.
* 반환된 데이터를 Pydantic을 사용해 JSON으로 **직렬화**합니다. Pydantic은 **Rust**로 작성되어 있어 **훨씬 더 빠릅니다**.

하지만 가장 중요한 것은:

* 반환 타입에 정의된 내용으로 출력 데이터를 **제한하고 필터링**합니다.
    * 이는 특히 **보안**에 매우 중요합니다. 아래에서 더 자세히 살펴보겠습니다.

## `response_model` 매개변수 { #response-model-parameter }

타입 선언이 말하는 것과 정확히 일치하지 않는 데이터를 반환해야 하거나 반환하고 싶은 경우가 있습니다.

예를 들어, **딕셔너리**나 데이터베이스 객체를 **반환**하고 싶지만, **Pydantic 모델로 선언**하고 싶을 수 있습니다. 이렇게 하면 Pydantic 모델이 반환한 객체(예: 딕셔너리나 데이터베이스 객체)에 대해 데이터 문서화, 검증 등 모든 작업을 수행합니다.

반환 타입 어노테이션을 추가했다면, 도구와 에디터가 함수가 선언한 타입(예: Pydantic 모델)과 다른 타입(예: dict)을 반환하고 있다는 (올바른) 오류로 불평할 것입니다.

그런 경우에는 반환 타입 대신 *경로 처리 데코레이터*의 매개변수 `response_model`을 사용할 수 있습니다.

`response_model` 매개변수는 모든 *경로 처리*에서 사용할 수 있습니다:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* 등.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | 참고

`response_model`은 "데코레이터" 메서드(`get`, `post` 등)의 매개변수입니다. 모든 매개변수와 body처럼, *경로 처리 함수*의 매개변수가 아닙니다.

///

`response_model`은 Pydantic 모델 필드에 선언하는 것과 동일한 타입을 받습니다. 따라서 Pydantic 모델이 될 수도 있고, `List[Item]`처럼 Pydantic 모델의 `list`가 될 수도 있습니다.

FastAPI는 이 `response_model`을 사용해 데이터 문서화, 검증 등을 수행하고, 또한 출력 데이터를 타입 선언에 맞게 **변환하고 필터링**합니다.

/// tip | 팁

에디터, mypy 등에서 엄격한 타입 체크를 사용하고 있다면, 함수 반환 타입을 `Any`로 선언할 수 있습니다.

이렇게 하면 에디터에 의도적으로 어떤 값이든 반환한다고 알려줍니다. 하지만 FastAPI는 여전히 `response_model`을 사용하여 데이터 문서화, 검증, 필터링 등을 수행합니다.

///

### `response_model` 우선순위 { #response-model-priority }

반환 타입과 `response_model`을 둘 다 선언하면, `response_model`이 우선순위를 가지며 FastAPI에서 사용됩니다.

이렇게 하면 응답 모델과 다른 타입을 반환하는 경우에도 에디터와 mypy 같은 도구에서 사용할 올바른 타입 어노테이션을 함수에 추가할 수 있습니다. 그리고 동시에 FastAPI가 `response_model`을 사용하여 데이터 검증, 문서화 등을 수행하게 할 수도 있습니다.

또한 `response_model=None`을 사용해 해당 *경로 처리*에 대한 응답 모델 생성을 비활성화할 수도 있습니다. 이는 유효한 Pydantic 필드가 아닌 것들에 대해 타입 어노테이션을 추가하는 경우에 필요할 수 있으며, 아래 섹션 중 하나에서 예시를 볼 수 있습니다.

## 동일한 입력 데이터 반환 { #return-the-same-input-data }

여기서는 평문 비밀번호를 포함하는 `UserIn` 모델을 선언합니다:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | 정보

`EmailStr`을 사용하려면 먼저 [`email-validator`](https://github.com/JoshData/python-email-validator)를 설치하세요.

[가상 환경](../virtual-environments.md)을 생성하고, 활성화한 다음 설치해야 합니다. 예를 들어:

```console
$ pip install email-validator
```

또는 다음과 같이:

```console
$ pip install "pydantic[email]"
```

///

그리고 이 모델을 사용하여 입력을 선언하고 같은 모델로 출력을 선언합니다:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

이제 브라우저가 비밀번호로 사용자를 만들 때마다 API는 응답으로 동일한 비밀번호를 반환합니다.

이 경우, 동일한 사용자가 비밀번호를 보내는 것이므로 문제가 되지 않을 수도 있습니다.

하지만 동일한 모델을 다른 *경로 처리*에서 사용하면, 모든 클라이언트에게 사용자의 비밀번호를 보내게 될 수도 있습니다.

/// danger | 위험

모든 주의사항을 알고 있으며 무엇을 하는지 정확히 알고 있지 않다면, 이런 방식으로 사용자의 평문 비밀번호를 저장하거나 응답으로 보내지 마세요.

///

## 출력 모델 추가 { #add-an-output-model }

대신 평문 비밀번호를 포함하는 입력 모델과, 비밀번호가 없는 출력 모델을 만들 수 있습니다:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

여기서 *경로 처리 함수*가 비밀번호를 포함하는 동일한 입력 사용자를 반환하더라도:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...비밀번호를 포함하지 않는 `UserOut` 모델로 `response_model`을 선언했습니다:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

따라서 **FastAPI**는 출력 모델에 선언되지 않은 모든 데이터를 (Pydantic을 사용하여) 필터링합니다.

### `response_model` 또는 반환 타입 { #response-model-or-return-type }

이 경우 두 모델이 서로 다르기 때문에, 함수 반환 타입을 `UserOut`으로 어노테이션하면 에디터와 도구는 서로 다른 클래스인데 잘못된 타입을 반환하고 있다고 불평할 것입니다.

그래서 이 예제에서는 `response_model` 매개변수로 선언해야 합니다.

...하지만 아래를 계속 읽으면 이를 극복하는 방법을 볼 수 있습니다.

## 반환 타입과 데이터 필터링 { #return-type-and-data-filtering }

이전 예제에서 계속해 봅시다. 함수에 **하나의 타입으로 어노테이션**을 하고 싶지만, 함수에서 실제로는 **더 많은 데이터**를 포함하는 것을 반환할 수 있길 원했습니다.

FastAPI가 응답 모델을 사용해 데이터를 계속 **필터링**하길 원합니다. 그래서 함수가 더 많은 데이터를 반환하더라도, 응답에는 응답 모델에 선언된 필드만 포함되게 합니다.

이전 예제에서는 클래스가 달랐기 때문에 `response_model` 매개변수를 써야 했습니다. 하지만 이는 에디터와 도구가 함수 반환 타입을 체크해 주는 지원을 받지 못한다는 뜻이기도 합니다.

하지만 대부분 이런 작업이 필요한 경우에는, 이 예제처럼 모델로 일부 데이터를 **필터링/제거**하길 원하는 경우가 많습니다.

그리고 그런 경우에는 클래스와 상속을 사용하여 함수 **타입 어노테이션**을 활용해 에디터/도구에서 더 나은 지원을 받으면서도 FastAPI의 **데이터 필터링**을 유지할 수 있습니다.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

이를 통해 이 코드는 타입 관점에서 올바르므로 에디터와 mypy 등의 도구 지원을 받을 수 있고, 동시에 FastAPI의 데이터 필터링도 받을 수 있습니다.

이게 어떻게 동작할까요? 확인해 봅시다. 🤓

### 타입 어노테이션과 도구 지원 { #type-annotations-and-tooling }

먼저 에디터, mypy 및 기타 도구가 이를 어떻게 보는지 살펴봅시다.

`BaseUser`는 기본 필드를 가집니다. 그리고 `UserIn`은 `BaseUser`를 상속하고 `password` 필드를 추가하므로, 두 모델의 모든 필드를 포함하게 됩니다.

함수 반환 타입을 `BaseUser`로 어노테이션하지만, 실제로는 `UserIn` 인스턴스를 반환합니다.

에디터, mypy 및 기타 도구는 이에 대해 불평하지 않습니다. 타이핑 관점에서 `UserIn`은 `BaseUser`의 서브클래스이므로, `BaseUser`인 어떤 것이 기대되는 곳에서는 *유효한* 타입이기 때문입니다.

### FastAPI 데이터 필터링 { #fastapi-data-filtering }

이제 FastAPI는 반환 타입을 보고, 여러분이 반환하는 값이 해당 타입에 선언된 필드 **만** 포함하도록 보장합니다.

FastAPI는 Pydantic을 내부적으로 여러 방식으로 사용하여, 클래스 상속의 동일한 규칙이 반환 데이터 필터링에는 적용되지 않도록 합니다. 그렇지 않으면 기대한 것보다 훨씬 더 많은 데이터를 반환하게 될 수도 있습니다.

이렇게 하면 **도구 지원**이 있는 타입 어노테이션과 **데이터 필터링**이라는 두 가지 장점을 모두 얻을 수 있습니다.

## 문서에서 보기 { #see-it-in-the-docs }

자동 생성 문서를 보면 입력 모델과 출력 모델이 각자의 JSON Schema를 가지고 있음을 확인할 수 있습니다:

<img src="/img/tutorial/response-model/image01.png">

그리고 두 모델 모두 대화형 API 문서에 사용됩니다:

<img src="/img/tutorial/response-model/image02.png">

## 기타 반환 타입 어노테이션 { #other-return-type-annotations }

유효한 Pydantic 필드가 아닌 것을 반환하면서도, 도구(에디터, mypy 등)가 제공하는 지원을 받기 위해 함수에 어노테이션을 달아두는 경우가 있을 수 있습니다.

### 응답을 직접 반환하기 { #return-a-response-directly }

가장 흔한 경우는 [고급 문서에서 나중에 설명하는 대로 Response를 직접 반환하는 것](../advanced/response-directly.md)입니다.

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

이 간단한 경우는 반환 타입 어노테이션이 `Response` 클래스(또는 그 서브클래스)이기 때문에 FastAPI에서 자동으로 처리됩니다.

그리고 `RedirectResponse`와 `JSONResponse`는 모두 `Response`의 서브클래스이므로, 타입 어노테이션이 올바르기 때문에 도구들도 만족합니다.

### Response 서브클래스 어노테이션 { #annotate-a-response-subclass }

타입 어노테이션에 `Response`의 서브클래스를 사용할 수도 있습니다:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

이는 `RedirectResponse`가 `Response`의 서브클래스이기 때문에 동작하며, FastAPI가 이 간단한 경우를 자동으로 처리합니다.

### 유효하지 않은 반환 타입 어노테이션 { #invalid-return-type-annotations }

하지만 유효한 Pydantic 타입이 아닌 다른 임의의 객체(예: 데이터베이스 객체)를 반환하고, 함수에서 그렇게 어노테이션하면, FastAPI는 그 타입 어노테이션으로부터 Pydantic 응답 모델을 만들려고 시도하다가 실패합니다.

또한, 유효한 Pydantic 타입이 아닌 타입이 하나 이상 포함된 여러 타입 간의 <dfn title="여러 타입 간의 union은 '이 타입들 중 아무거나'를 의미합니다.">union</dfn>이 있는 경우에도 동일합니다. 예를 들어, 아래는 실패합니다 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...이는 타입 어노테이션이 Pydantic 타입이 아니고, 단일 `Response` 클래스/서브클래스도 아니며, `Response`와 `dict` 간 union(둘 중 아무거나)이기 때문에 실패합니다.

### 응답 모델 비활성화 { #disable-response-model }

위 예제에서 이어서, FastAPI가 수행하는 기본 데이터 검증, 문서화, 필터링 등을 원하지 않을 수 있습니다.

하지만 에디터나 타입 체커(예: mypy) 같은 도구 지원을 받기 위해 함수에 반환 타입 어노테이션은 유지하고 싶을 수도 있습니다.

이 경우 `response_model=None`으로 설정하여 응답 모델 생성을 비활성화할 수 있습니다:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

그러면 FastAPI는 응답 모델 생성을 건너뛰며, FastAPI 애플리케이션에 영향을 주지 않고 필요한 반환 타입 어노테이션을 어떤 것이든 사용할 수 있습니다. 🤓

## 응답 모델 인코딩 매개변수 { #response-model-encoding-parameters }

응답 모델은 아래와 같이 기본값을 가질 수 있습니다:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (또는 Python 3.10에서 `str | None = None`)은 기본값으로 `None`을 갖습니다.
* `tax: float = 10.5`는 기본값으로 `10.5`를 갖습니다.
* `tags: List[str] = []`는 기본값으로 빈 리스트 `[]`를 갖습니다.

하지만 실제로 저장되지 않았을 경우 결과에서 이를 생략하고 싶을 수 있습니다.

예를 들어, NoSQL 데이터베이스에 많은 선택적 속성이 있는 모델이 있지만, 기본값으로 가득 찬 매우 긴 JSON 응답을 보내고 싶지 않습니다.

### `response_model_exclude_unset` 매개변수 사용 { #use-the-response-model-exclude-unset-parameter }

*경로 처리 데코레이터* 매개변수 `response_model_exclude_unset=True`로 설정할 수 있습니다:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

그러면 이러한 기본값은 응답에 포함되지 않고, 실제로 설정된 값만 포함됩니다.

따라서 ID가 `foo`인 항목에 대해 해당 *경로 처리*로 요청을 보내면, (기본값을 제외한) 응답은 다음과 같습니다:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | 정보

다음도 사용할 수 있습니다:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

`exclude_defaults` 및 `exclude_none`에 대해 [Pydantic 문서](https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict)에 설명된 대로 사용할 수 있습니다.

///

#### 기본값이 있는 필드에 값이 있는 데이터 { #data-with-values-for-fields-with-defaults }

하지만 ID가 `bar`인 항목처럼, 기본값이 있는 모델의 필드에 값이 있다면:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

응답에 포함됩니다.

#### 기본값과 동일한 값을 갖는 데이터 { #data-with-the-same-values-as-the-defaults }

데이터가 ID가 `baz`인 항목처럼 기본값과 동일한 값을 갖는다면:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI는 충분히 똑똑해서(사실, Pydantic이 충분히 똑똑합니다) `description`, `tax`, `tags`가 기본값과 동일하더라도, 기본값에서 가져온 것이 아니라 명시적으로 설정되었다는 것을 알아냅니다.

그래서 JSON 응답에 포함됩니다.

/// tip | 팁

기본값은 `None`뿐만 아니라 어떤 것이든 될 수 있습니다.

리스트(`[]`), `float`인 `10.5` 등이 될 수 있습니다.

///

### `response_model_include` 및 `response_model_exclude` { #response-model-include-and-response-model-exclude }

*경로 처리 데코레이터* 매개변수 `response_model_include` 및 `response_model_exclude`를 사용할 수도 있습니다.

이들은 포함(나머지 생략)하거나 제외(나머지 포함)할 어트리뷰트 이름을 담은 `str`의 `set`을 받습니다.

Pydantic 모델이 하나만 있고 출력에서 일부 데이터를 제거하려는 경우, 빠른 지름길로 사용할 수 있습니다.

/// tip | 팁

하지만 이러한 매개변수 대신, 위에서 설명한 것처럼 여러 클래스를 사용하는 것을 여전히 권장합니다.

이는 일부 어트리뷰트를 생략하기 위해 `response_model_include` 또는 `response_model_exclude`를 사용하더라도, 앱의 OpenAPI(및 문서)에 생성되는 JSON Schema가 여전히 전체 모델에 대한 스키마이기 때문입니다.

비슷하게 동작하는 `response_model_by_alias`에도 동일하게 적용됩니다.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | 팁

문법 `{"name", "description"}`은 두 값을 갖는 `set`을 만듭니다.

이는 `set(["name", "description"])`과 동일합니다.

///

#### `set` 대신 `list` 사용하기 { #using-lists-instead-of-sets }

`set`을 쓰는 것을 잊고 `list`나 `tuple`을 대신 사용하더라도, FastAPI는 이를 `set`으로 변환하므로 올바르게 동작합니다:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## 요약 { #recap }

응답 모델을 정의하고 특히 개인정보가 필터링되도록 보장하려면 *경로 처리 데코레이터*의 매개변수 `response_model`을 사용하세요.

명시적으로 설정된 값만 반환하려면 `response_model_exclude_unset`을 사용하세요.
