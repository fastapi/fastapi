# 파이썬 타입 소개 { #python-types-intro }

파이썬은 선택적으로 "타입 힌트(type hints)"(“type annotations”라고도 함)를 지원합니다.

이러한 **"타입 힌트"** 또는 애너테이션은 변수의 <dfn title="예: str, int, float, bool">타입</dfn>을 선언할 수 있게 해주는 특수한 구문입니다.

변수의 타입을 선언하면 에디터와 도구가 더 나은 지원을 제공할 수 있습니다.

이 문서는 파이썬 타입 힌트에 대한 **빠른 자습서 / 내용 환기**입니다. **FastAPI**와 함께 사용하기 위해 필요한 최소한만 다룹니다... 실제로는 아주 조금만 있으면 됩니다.

**FastAPI**는 모두 이러한 타입 힌트에 기반을 두고 있으며, 이는 많은 장점과 이점을 제공합니다.

하지만 **FastAPI**를 전혀 사용하지 않더라도, 타입 힌트를 조금만 배워도 도움이 됩니다.

/// note | 참고

파이썬에 능숙하고 타입 힌트에 대해 이미 모두 알고 있다면, 다음 장으로 건너뛰세요.

///

## 동기 부여 { #motivation }

간단한 예제로 시작해봅시다:

{* ../../docs_src/python_types/tutorial001_py310.py *}

이 프로그램을 호출하면 다음이 출력됩니다:

```
John Doe
```

이 함수는 다음을 수행합니다:

* `first_name`과 `last_name`를 받습니다.
* `title()`로 각각의 첫 글자를 대문자로 변환합니다.
* 가운데에 공백을 두고 <dfn title="서로를 하나로 합칩니다. 하나의 내용 뒤에 다른 것의 내용을 이어 붙입니다.">연결</dfn>합니다.

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### 수정하기 { #edit-it }

매우 간단한 프로그램입니다.

하지만 이제, 이것을 처음부터 작성한다고 상상해봅시다.

어느 시점엔 함수를 정의하기 시작했고, 매개변수도 준비해두었을 겁니다...

그런데 "첫 글자를 대문자로 변환하는 그 메서드"를 호출해야 합니다.

`upper`였나요? `uppercase`였나요? `first_uppercase`? `capitalize`?

그 다음, 개발자들의 오랜 친구인 에디터 자동완성을 시도합니다.

함수의 첫 번째 매개변수인 `first_name`을 입력하고, 점(`.`)을 찍은 다음, 완성을 트리거하기 위해 `Ctrl+Space`를 누릅니다.

하지만, 슬프게도 쓸만한 게 아무것도 없습니다:

<img src="/img/python-types/image01.png">

### 타입 추가하기 { #add-types }

이전 버전에서 한 줄만 수정해봅시다.

함수의 매개변수인 정확히 이 부분을:

```Python
    first_name, last_name
```

에서:

```Python
    first_name: str, last_name: str
```

로 바꾸겠습니다.

이게 다입니다.

이것들이 "타입 힌트"입니다:

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

이것은 다음처럼 기본값을 선언하는 것과는 다릅니다:

```Python
    first_name="john", last_name="doe"
```

다른 것입니다.

등호(`=`)가 아니라 콜론(`:`)을 사용합니다.

그리고 보통 타입 힌트를 추가해도, 타입 힌트 없이 일어나는 일과 비교해 특별히 달라지는 것은 없습니다.

하지만 이제, 타입 힌트를 포함해 그 함수를 다시 만드는 중이라고 상상해봅시다.

같은 지점에서 `Ctrl+Space`로 자동완성을 트리거하면 다음이 보입니다:

<img src="/img/python-types/image02.png">

그러면 스크롤하며 옵션을 보다가, "기억나는" 것을 찾을 수 있습니다:

<img src="/img/python-types/image03.png">

## 더 큰 동기부여 { #more-motivation }

이 함수를 확인해보세요. 이미 타입 힌트가 있습니다:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

에디터가 변수의 타입을 알고 있기 때문에, 자동완성만 되는 게 아니라 오류 검사도 할 수 있습니다:

<img src="/img/python-types/image04.png">

이제 고쳐야 한다는 것을 알고, `age`를 `str(age)`로 문자열로 바꿉니다:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## 타입 선언 { #declaring-types }

방금 타입 힌트를 선언하는 주요 위치를 보았습니다. 함수 매개변수입니다.

이것은 **FastAPI**와 함께 사용할 때도 주요 위치입니다.

### Simple 타입 { #simple-types }

`str`뿐 아니라 모든 파이썬 표준 타입을 선언할 수 있습니다.

예를 들어 다음을 사용할 수 있습니다:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` 모듈 { #typing-module }

몇 가지 추가적인 사용 사례에서는 표준 라이브러리의 `typing` 모듈에서 무언가를 import해야 할 수 있습니다. 예를 들어 어떤 값이 "아무 타입"일 수 있다고 선언하려면, `typing`의 `Any`를 사용할 수 있습니다:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Generic(제네릭) 타입 { #generic-types }

일부 타입은 대괄호 안에 "타입 매개변수"를 받아 내부 타입을 정의할 수 있습니다. 예를 들어 "문자열의 리스트"는 `list[str]`로 선언합니다.

이렇게 타입 매개변수를 받을 수 있는 타입을 **Generic types** 또는 **Generics**라고 부릅니다.

대괄호와 내부 타입을 사용해 동일한 내장 타입들을 제네릭으로 사용할 수 있습니다:

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

예를 들어, `str`의 `list`인 변수를 정의해봅시다.

같은 콜론(`:`) 문법으로 변수를 선언합니다.

타입으로 `list`를 넣습니다.

`list`는 내부 타입을 포함하는 타입이므로, 그 타입들을 대괄호 안에 넣습니다:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | 정보

대괄호 안의 내부 타입은 "type parameters"라고 부릅니다.

이 경우 `str`이 `list`에 전달된 타입 매개변수입니다.

///

이는 "변수 `items`는 `list`이고, 이 `list`의 각 아이템은 `str`이다"라는 뜻입니다.

이렇게 하면, 에디터는 리스트의 아이템을 처리하는 동안에도 지원을 제공할 수 있습니다:

<img src="/img/python-types/image05.png">

타입이 없으면, 이는 거의 불가능합니다.

변수 `item`이 리스트 `items`의 요소 중 하나라는 점에 주목하세요.

그리고 에디터는 여전히 이것이 `str`임을 알고, 그에 대한 지원을 제공합니다.

#### Tuple과 Set { #tuple-and-set }

`tuple`과 `set`도 동일하게 선언할 수 있습니다:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

이는 다음을 의미합니다:

* 변수 `items_t`는 3개의 아이템을 가진 `tuple`이며, `int`, 또 다른 `int`, 그리고 `str`입니다.
* 변수 `items_s`는 `set`이며, 각 아이템의 타입은 `bytes`입니다.

#### Dict { #dict }

`dict`를 정의하려면, 쉼표로 구분된 2개의 타입 매개변수를 전달합니다.

첫 번째 타입 매개변수는 `dict`의 키를 위한 것입니다.

두 번째 타입 매개변수는 `dict`의 값을 위한 것입니다:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

이는 다음을 의미합니다:

* 변수 `prices`는 `dict`입니다:
    * 이 `dict`의 키는 `str` 타입입니다(예: 각 아이템의 이름).
    * 이 `dict`의 값은 `float` 타입입니다(예: 각 아이템의 가격).

#### Union { #union }

변수가 **여러 타입 중 어떤 것이든** 될 수 있다고 선언할 수 있습니다. 예를 들어 `int` 또는 `str`입니다.

이를 정의하려면 두 타입을 <dfn title='“비트 단위 OR 연산자”라고도 하지만, 여기서는 그 의미와 관련이 없습니다'>세로 막대(`|`)</dfn>로 구분해 사용합니다.

이는 두 타입 집합의 합집합(union) 안의 어느 것이든 될 수 있다는 뜻이므로 "유니온"이라고 부릅니다.

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

이는 `item`이 `int` 또는 `str`일 수 있다는 뜻입니다.

#### `None`일 수도 있음 { #possibly-none }

값이 `str` 같은 타입일 수도 있지만, `None`일 수도 있다고 선언할 수 있습니다.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

그냥 `str` 대신 `str | None`을 사용하면, 값이 항상 `str`이라고 가정하고 있지만 실제로는 `None`일 수도 있는 상황에서 에디터가 오류를 감지하도록 도와줍니다.

### 타입으로서의 클래스 { #classes-as-types }

변수의 타입으로 클래스를 선언할 수도 있습니다.

이름을 가진 `Person` 클래스가 있다고 해봅시다:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

그러면 `Person` 타입의 변수를 선언할 수 있습니다:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

그리고 다시, 에디터의 모든 지원을 받을 수 있습니다:

<img src="/img/python-types/image06.png">

이는 "`one_person`은 `Person` 클래스의 **인스턴스**"라는 뜻입니다.

"`one_person`은 `Person`이라는 **클래스**다"라는 뜻이 아닙니다.

## Pydantic 모델 { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>은 데이터 검증을 수행하는 파이썬 라이브러리입니다.

속성을 가진 클래스 형태로 데이터의 "모양(shape)"을 선언합니다.

그리고 각 속성은 타입을 가집니다.

그 다음 그 클래스의 인스턴스를 몇 가지 값으로 생성하면, 값들을 검증하고, (그런 경우라면) 적절한 타입으로 변환한 뒤, 모든 데이터를 가진 객체를 제공합니다.

그리고 그 결과 객체에 대해 에디터의 모든 지원을 받을 수 있습니다.

Pydantic 공식 문서의 예시:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | 정보

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic에 대해 더 알아보려면 문서를 확인하세요</a>.

///

**FastAPI**는 모두 Pydantic에 기반을 두고 있습니다.

이 모든 것은 [자습서 - 사용자 안내서](tutorial/index.md){.internal-link target=_blank}에서 실제로 많이 보게 될 것입니다.

## 메타데이터 애너테이션이 있는 타입 힌트 { #type-hints-with-metadata-annotations }

파이썬에는 `Annotated`를 사용해 이러한 타입 힌트에 **추가 <dfn title="데이터에 대한 데이터, 여기서는 타입에 대한 정보(예: 설명)">메타데이터</dfn>**를 넣을 수 있는 기능도 있습니다.

`Annotated`는 `typing`에서 import할 수 있습니다.

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

파이썬 자체는 이 `Annotated`로 아무것도 하지 않습니다. 그리고 에디터와 다른 도구들에게는 타입이 여전히 `str`입니다.

하지만 `Annotated`의 이 공간을 사용해, 애플리케이션이 어떻게 동작하길 원하는지에 대한 추가 메타데이터를 **FastAPI**에 제공할 수 있습니다.

기억해야 할 중요한 점은 `Annotated`에 전달하는 **첫 번째 *타입 매개변수***가 **실제 타입**이라는 것입니다. 나머지는 다른 도구를 위한 메타데이터일 뿐입니다.

지금은 `Annotated`가 존재하며, 표준 파이썬이라는 것만 알면 됩니다. 😎

나중에 이것이 얼마나 **강력**할 수 있는지 보게 될 것입니다.

/// tip | 팁

이것이 **표준 파이썬**이라는 사실은, 에디터에서 가능한 **최고의 개발자 경험**을 계속 얻을 수 있다는 뜻이기도 합니다. 사용하는 도구로 코드를 분석하고 리팩터링하는 등에서도요. ✨

또한 코드가 많은 다른 파이썬 도구 및 라이브러리와 매우 호환된다는 뜻이기도 합니다. 🚀

///

## **FastAPI**에서의 타입 힌트 { #type-hints-in-fastapi }

**FastAPI**는 이러한 타입 힌트를 활용해 여러 가지를 합니다.

**FastAPI**에서는 타입 힌트로 매개변수를 선언하면 다음을 얻습니다:

* **에디터 도움**.
* **타입 확인**.

...그리고 **FastAPI**는 같은 선언을 다음에도 사용합니다:

* **요구사항 정의**: 요청 경로 매개변수, 쿼리 매개변수, 헤더, 바디, 의존성 등에서.
* **데이터 변환**: 요청에서 필요한 타입으로.
* **데이터 검증**: 각 요청에서:
    * 데이터가 유효하지 않을 때 클라이언트에 반환되는 **자동 오류**를 생성합니다.
* OpenAPI를 사용해 API를 **문서화**:
    * 자동 상호작용 문서 UI에서 사용됩니다.

이 모든 것이 다소 추상적으로 들릴 수도 있습니다. 걱정하지 마세요. [자습서 - 사용자 안내서](tutorial/index.md){.internal-link target=_blank}에서 실제로 확인하게 될 것입니다.

가장 중요한 점은 표준 파이썬 타입을 한 곳에서 사용함으로써(더 많은 클래스, 데코레이터 등을 추가하는 대신) **FastAPI**가 여러분을 위해 많은 일을 해준다는 사실입니다.

/// info | 정보

자습서를 모두 끝내고 타입에 대해 더 알아보기 위해 다시 돌아왔다면, 좋은 자료로 <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy`의 "cheat sheet"</a>가 있습니다.

///
