# 본문 - 중첩 모델 { #body-nested-models }

**FastAPI**를 사용하면 (Pydantic 덕분에) 임의로 깊게 중첩된 모델을 정의, 검증, 문서화하고 사용할 수 있습니다.

## 리스트 필드 { #list-fields }

어트리뷰트를 서브타입으로 정의할 수 있습니다. 예를 들어 파이썬 `list`는:

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

이는 `tags`를 리스트로 만들지만, 리스트 요소의 타입을 선언하지는 않습니다.

## 타입 매개변수가 있는 리스트 필드 { #list-fields-with-type-parameter }

하지만 파이썬에는 내부 타입, 즉 "타입 매개변수"를 사용해 리스트를 선언하는 특정한 방법이 있습니다:

### 타입 매개변수로 `list` 선언 { #declare-a-list-with-a-type-parameter }

`list`, `dict`, `tuple`처럼 타입 매개변수(내부 타입)를 갖는 타입을 선언하려면,
대괄호 `[` 및 `]`를 사용해 내부 타입(들)을 "타입 매개변수"로 전달하세요.

```Python
my_list: list[str]
```

이 모든 것은 타입 선언을 위한 표준 파이썬 문법입니다.

내부 타입을 갖는 모델 어트리뷰트에 대해 동일한 표준 문법을 사용하세요.

마찬가지로 예제에서 `tags`를 구체적으로 "문자열의 리스트"로 만들 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## 집합 타입 { #set-types }

그런데 생각해보니 태그는 반복되면 안 되고, 아마 고유한 문자열이어야 할 것입니다.

그리고 파이썬에는 고유한 항목들의 집합을 위한 특별한 데이터 타입 `set`이 있습니다.

그렇다면 `tags`를 문자열의 집합으로 선언할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

이렇게 하면 중복 데이터가 있는 요청을 받더라도 고유한 항목들의 집합으로 변환됩니다.

그리고 해당 데이터를 출력할 때마다, 소스에 중복이 있더라도 고유한 항목들의 집합으로 출력됩니다.

또한 그에 따라 주석이 생기고 문서화됩니다.

## 중첩 모델 { #nested-models }

Pydantic 모델의 각 어트리뷰트는 타입을 갖습니다.

그런데 그 타입 자체가 또 다른 Pydantic 모델일 수 있습니다.

따라서 특정한 어트리뷰트 이름, 타입, 검증을 사용하여 깊게 중첩된 JSON "객체"를 선언할 수 있습니다.

모든 것이 임의의 깊이로 중첩됩니다.

### 서브모델 정의 { #define-a-submodel }

예를 들어, `Image` 모델을 정의할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### 서브모델을 타입으로 사용 { #use-the-submodel-as-a-type }

그리고 이를 어트리뷰트의 타입으로 사용할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

이는 **FastAPI**가 다음과 유사한 본문을 기대한다는 것을 의미합니다:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

다시 한번, **FastAPI**로 그 선언만 해도 얻는 것은:

* 중첩 모델도 편집기 지원(자동완성 등)
* 데이터 변환
* 데이터 검증
* 자동 문서화

## 특별한 타입과 검증 { #special-types-and-validation }

`str`, `int`, `float` 등과 같은 일반적인 단일 타입과는 별개로, `str`을 상속하는 더 복잡한 단일 타입을 사용할 수 있습니다.

사용할 수 있는 모든 옵션을 보려면 <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantic의 Type Overview</a>를 확인하세요. 다음 장에서 몇 가지 예제를 볼 수 있습니다.

예를 들어 `Image` 모델에는 `url` 필드가 있으므로, 이를 `str` 대신 Pydantic의 `HttpUrl` 인스턴스로 선언할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

이 문자열은 유효한 URL인지 검사되며, JSON Schema / OpenAPI에도 그에 맞게 문서화됩니다.

## 서브모델 리스트를 갖는 어트리뷰트 { #attributes-with-lists-of-submodels }

`list`, `set` 등의 서브타입으로 Pydantic 모델을 사용할 수도 있습니다:

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

아래와 같은 JSON 본문을 예상(변환, 검증, 문서화 등)합니다:

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// info | 정보

`images` 키가 이제 이미지 객체 리스트를 갖는지 주목하세요.

///

## 깊게 중첩된 모델 { #deeply-nested-models }

임의로 깊게 중첩된 모델을 정의할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | 정보

`Offer`가 `Item`의 리스트를 가지고, 그 `Item`이 다시 선택 사항인 `Image` 리스트를 갖는지 주목하세요

///

## 순수 리스트의 본문 { #bodies-of-pure-lists }

예상되는 JSON 본문의 최상위 값이 JSON `array`(파이썬 `list`)라면, Pydantic 모델에서와 마찬가지로 함수의 매개변수에서 타입을 선언할 수 있습니다:

```Python
images: list[Image]
```

이를 아래처럼:

{* ../../docs_src/body_nested_models/tutorial008_py39.py hl[13] *}

## 어디서나 편집기 지원 { #editor-support-everywhere }

그리고 어디서나 편집기 지원을 받을 수 있습니다.

리스트 내부 항목의 경우에도:

<img src="/img/tutorial/body-nested-models/image01.png">

Pydantic 모델 대신 `dict`로 직접 작업한다면 이런 종류의 편집기 지원을 받을 수 없습니다.

하지만 그 부분에 대해서도 걱정할 필요는 없습니다. 들어오는 dict는 자동으로 변환되고, 출력도 자동으로 JSON으로 변환됩니다.

## 임의의 `dict` 본문 { #bodies-of-arbitrary-dicts }

또한 키는 어떤 타입이고 값은 다른 타입인 `dict`로 본문을 선언할 수 있습니다.

이렇게 하면 (Pydantic 모델을 사용하는 경우처럼) 유효한 필드/어트리뷰트 이름이 무엇인지 미리 알 필요가 없습니다.

아직 모르는 키를 받으려는 경우에 유용합니다.

---

또 다른 유용한 경우는 다른 타입(예: `int`)의 키를 갖고 싶을 때입니다.

여기서 그 경우를 볼 것입니다.

이 경우, `int` 키와 `float` 값을 가진 한 어떤 `dict`든 받아들입니다:

{* ../../docs_src/body_nested_models/tutorial009_py39.py hl[7] *}

/// tip | 팁

JSON은 키로 `str`만 지원한다는 것을 염두에 두세요.

하지만 Pydantic은 자동 데이터 변환 기능이 있습니다.

즉, API 클라이언트는 키로 문자열만 보낼 수 있더라도, 해당 문자열이 순수한 정수를 포함하기만 하면 Pydantic이 이를 변환하고 검증합니다.

그리고 `weights`로 받는 `dict`는 실제로 `int` 키와 `float` 값을 갖게 됩니다.

///

## 요약 { #recap }

**FastAPI**를 사용하면 Pydantic 모델이 제공하는 최대 유연성을 확보하면서 코드를 간단하고 짧고 우아하게 유지할 수 있습니다.

하지만 아래의 모든 이점도 있습니다:

* 편집기 지원(어디서나 자동완성!)
* 데이터 변환(일명 파싱/직렬화)
* 데이터 검증
* 스키마 문서화
* 자동 문서
