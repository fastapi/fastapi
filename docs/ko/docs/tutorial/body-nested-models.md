# 본문 - 중첩 모델

**FastAPI**를 이용하면 (Pydantic 덕분에) 단독으로 깊이 중첩된 모델을 정의, 검증, 문서화하며 사용할 수 있습니다.
## 리스트 필드

어트리뷰트를 서브타입으로 정의할 수 있습니다. 예를 들어 파이썬 `list`는:

{* ../../docs_src/body_nested_models/tutorial001.py hl[14] *}

이는 `tags`를 항목 리스트로 만듭니다. 각 항목의 타입을 선언하지 않더라도요.

## 타입 매개변수가 있는 리스트 필드

하지만 파이썬은 내부의 타입이나 "타입 매개변수"를 선언할 수 있는 특정 방법이 있습니다:

### typing의 `List` 임포트

먼저, 파이썬 표준 `typing` 모듈에서 `List`를 임포트합니다:

{* ../../docs_src/body_nested_models/tutorial002.py hl[1] *}

### 타입 매개변수로 `List` 선언

`list`, `dict`, `tuple`과 같은 타입 매개변수(내부 타입)를 갖는 타입을 선언하려면:

* `typing` 모듈에서 임포트
* 대괄호를 사용하여 "타입 매개변수"로 내부 타입 전달: `[` 및 `]`

```Python
from typing import List

my_list: List[str]
```

이 모든 것은 타입 선언을 위한 표준 파이썬 문법입니다.

내부 타입을 갖는 모델 어트리뷰트에 대해 동일한 표준 문법을 사용하세요.

마찬가지로 예제에서 `tags`를 구체적으로 "문자열의 리스트"로 만들 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial002.py hl[14] *}

## 집합 타입

그런데 생각해보니 태그는 반복되면 안 되고, 고유한(Unique) 문자열이어야 할 것 같습니다.

그리고 파이썬은 집합을 위한 특별한 데이터 타입 `set`이 있습니다.

그렇다면 `Set`을 임포트 하고 `tags`를 `str`의 `set`으로 선언할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial003.py hl[1,14] *}

덕분에 중복 데이터가 있는 요청을 수신하더라도 고유한 항목들의 집합으로 변환됩니다.

그리고 해당 데이터를 출력 할 때마다 소스에 중복이 있더라도 고유한 항목들의 집합으로 출력됩니다.

또한 그에 따라 주석이 생기고 문서화됩니다.

## 중첩 모델

Pydantic 모델의 각 어트리뷰트는 타입을 갖습니다.

그런데 해당 타입 자체로 또다른 Pydantic 모델의 타입이 될 수 있습니다.

그러므로 특정한 어트리뷰트의 이름, 타입, 검증을 사용하여 깊게 중첩된 JSON "객체"를 선언할 수 있습니다.

모든 것이 단독으로 중첩됩니다.

### 서브모델 정의

예를 들어, `Image` 모델을 선언할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial004.py hl[9:11] *}

### 서브모듈을 타입으로 사용

그리고 어트리뷰트의 타입으로 사용할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial004.py hl[20] *}

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

다시 한번, **FastAPI**를 사용하여 해당 선언을 함으로써 얻는 것은:

* 중첩 모델도 편집기 지원(자동완성 등)
* 데이터 변환
* 데이터 검증
* 자동 문서화

## 특별한 타입과 검증

`str`, `int`, `float` 등과 같은 단일 타입과는 별개로, `str`을 상속하는 더 복잡한 단일 타입을 사용할 수 있습니다.

모든 옵션을 보려면, <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantic's exotic types</a> 문서를 확인하세요. 다음 장에서 몇가지 예제를 볼 수 있습니다.

예를 들어 `Image` 모델 안에 `url` 필드를 `str` 대신 Pydantic의 `HttpUrl`로 선언할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial005.py hl[4,10] *}

이 문자열이 유효한 URL인지 검사하고 JSON 스키마/OpenAPI로 문서화 됩니다.

## 서브모델 리스트를 갖는 어트리뷰트

`list`, `set` 등의 서브타입으로 Pydantic 모델을 사용할 수도 있습니다:

{* ../../docs_src/body_nested_models/tutorial006.py hl[20] *}

아래와 같은 JSON 본문으로 예상(변환, 검증, 문서화 등을)합니다:

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

`images` 키가 어떻게 이미지 객체 리스트를 갖는지 주목하세요.

///

## 깊게 중첩된 모델

단독으로 깊게 중첩된 모델을 정의할 수 있습니다:

{* ../../docs_src/body_nested_models/tutorial007.py hl[9,14,20,23,27] *}

/// info | 정보

`Offer`가 선택사항 `Image` 리스트를 차례로 갖는 `Item` 리스트를 어떻게 가지고 있는지 주목하세요

///

## 순수 리스트의 본문

예상되는 JSON 본문의 최상위 값이 JSON `array`(파이썬 `list`)면, Pydantic 모델에서와 마찬가지로 함수의 매개변수에서 타입을 선언할 수 있습니다:

```Python
images: List[Image]
```

이를 아래처럼:

{* ../../docs_src/body_nested_models/tutorial008.py hl[15] *}

## 어디서나 편집기 지원

그리고 어디서나 편집기 지원을 받을수 있습니다.

리스트 내부 항목의 경우에도:

<img src="/img/tutorial/body-nested-models/image01.png">

Pydantic 모델 대신에 `dict`를 직접 사용하여 작업할 경우, 이러한 편집기 지원을 받을수 없습니다.

하지만 수신한 딕셔너리가 자동으로 변환되고 출력도 자동으로 JSON으로 변환되므로 걱정할 필요는 없습니다.

## 단독 `dict`의 본문

일부 타입의 키와 다른 타입의 값을 사용하여 `dict`로 본문을 선언할 수 있습니다.

(Pydantic을 사용한 경우처럼) 유효한 필드/어트리뷰트 이름이 무엇인지 알 필요가 없습니다.

아직 모르는 키를 받으려는 경우 유용합니다.

---

다른 유용한 경우는 다른 타입의 키를 가질 때입니다. 예. `int`.

여기서 그 경우를 볼 것입니다.

이 경우, `float` 값을 가진 `int` 키가 있는 모든 `dict`를 받아들입니다:

{* ../../docs_src/body_nested_models/tutorial009.py hl[15] *}

/// tip | 팁

JSON은 오직 `str`형 키만 지원한다는 것을 염두에 두세요.

하지만 Pydantic은 자동 데이터 변환이 있습니다.

즉, API 클라이언트가 문자열을 키로 보내더라도 해당 문자열이 순수한 정수를 포함하는한 Pydantic은 이를 변환하고 검증합니다.

그러므로 `weights`로 받은 `dict`는 실제로 `int` 키와 `float` 값을 가집니다.

///

## 요약

**FastAPI**를 사용하면 Pydantic 모델이 제공하는 최대 유연성을 확보하면서 코드를 간단하고 짧게, 그리고 우아하게 유지할 수 있습니다.

물론 아래의 이점도 있습니다:

* 편집기 지원 (자동완성이 어디서나!)
* 데이터 변환 (일명 파싱/직렬화)
* 데이터 검증
* 스키마 문서화
* 자동 문서
