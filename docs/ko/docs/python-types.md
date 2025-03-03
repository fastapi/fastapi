# 파이썬 타입 소개

파이썬은 선택적으로 "타입 힌트(type hints)"를 지원합니다.

이러한 **타입 힌트**들은 변수의 <abbr title="예를 들면: str, int, float, bool">타입</abbr>을 선언할 수 있게 해주는 특수한 구문입니다.

변수의 타입을 지정하면 에디터와 툴이 더 많은 도움을 줄 수 있게 됩니다.

이 문서는 파이썬 타입 힌트에 대한 **빠른 자습서 / 내용환기** 수준의 문서입니다. 여기서는 **FastAPI**를 쓰기 위한 최소한의 내용만을 다룹니다.

**FastAPI**는 타입 힌트에 기반을 두고 있으며, 이는 많은 장점과 이익이 있습니다.

비록 **FastAPI**를 쓰지 않는다고 하더라도, 조금이라도 알아두면 도움이 될 것입니다.

/// note | 참고

파이썬에 능숙하셔서 타입 힌트에 대해 모두 아신다면, 다음 챕터로 건너뛰세요.

///

## 동기 부여

간단한 예제부터 시작해봅시다:

{* ../../docs_src/python_types/tutorial001.py *}


이 프로그램을 실행한 결과값:

```
John Doe
```

함수는 아래와 같이 실행됩니다:

* `first_name`과 `last_name`를 받습니다.
* `title()`로 각 첫 문자를 대문자로 변환시킵니다.
* 두 단어를 중간에 공백을 두고 <abbr title="두 개를 하나로 차례차례 이어지게 하다">연결</abbr>합니다.

{* ../../docs_src/python_types/tutorial001.py hl[2] *}


### 코드 수정

이건 매우 간단한 프로그램입니다.

그런데 처음부터 작성한다고 생각을 해봅시다.

여러분은 매개변수를 준비했고, 함수를 정의하기 시작했을 겁니다.

이때 "첫 글자를 대문자로 바꾸는 함수"를 호출해야 합니다.

`upper`였나? 아니면 `uppercase`? `first_uppercase`? `capitalize`?

그때 개발자들의 오랜 친구, 에디터 자동완성을 시도해봅니다.

당신은 `first_name`를 입력한 뒤 점(`.`)을 입력하고 자동완성을 켜기 위해서 `Ctrl+Space`를 눌렀습니다.

하지만 슬프게도 아무런 도움이 되지 않습니다:

<img src="/img/python-types/image01.png">

### 타입 추가하기

이전 버전에서 한 줄만 수정해봅시다.

저희는 이 함수의 매개변수 부분:

```Python
    first_name, last_name
```

을 아래와 같이 바꿀 겁니다:

```Python
    first_name: str, last_name: str
```

이게 다입니다.

이게 "타입 힌트"입니다:

{* ../../docs_src/python_types/tutorial002.py hl[1] *}


타입힌트는 다음과 같이 기본 값을 선언하는 것과는 다릅니다:

```Python
    first_name="john", last_name="doe"
```

이는 다른 것입니다.

등호(`=`) 대신 콜론(`:`)을 쓰고 있습니다.

일반적으로 타입힌트를 추가한다고 해서 특별하게 어떤 일이 일어나지도 않습니다.

그렇지만 이제, 다시 함수를 만드는 도중이라고 생각해봅시다. 다만 이번엔 타입 힌트가 있습니다.

같은 상황에서 `Ctrl+Space`로 자동완성을 작동시키면,

<img src="/img/python-types/image02.png">

아래와 같이 "그렇지!"하는 옵션이 나올때까지 스크롤을 내려서 볼 수 있습니다:

<img src="/img/python-types/image03.png">

## 더 큰 동기부여

아래 함수를 보면, 이미 타입 힌트가 적용되어 있는 걸 볼 수 있습니다:

{* ../../docs_src/python_types/tutorial003.py hl[1] *}


편집기가 변수의 타입을 알고 있기 때문에, 자동완성 뿐 아니라 에러도 확인할 수 있습니다:

<img src="/img/python-types/image04.png">

이제 고쳐야하는 걸 알기 때문에, `age`를 `str(age)`과 같이 문자열로 바꾸게 됩니다:

{* ../../docs_src/python_types/tutorial004.py hl[2] *}


## 타입 선언

방금 함수의 매개변수로써 타입 힌트를 선언하는 주요 장소를 보았습니다.

이 위치는 여러분이 **FastAPI**와 함께 이를 사용하는 주요 장소입니다.

### Simple 타입

`str`뿐 아니라 모든 파이썬 표준 타입을 선언할 수 있습니다.

예를 들면:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005.py hl[1] *}


### 타입 매개변수를 활용한 Generic(제네릭) 타입

`dict`, `list`, `set`, `tuple`과 같은 값을 저장할 수 있는 데이터 구조가 있고, 내부의 값은 각자의 타입을 가질 수도 있습니다.

타입과 내부 타입을 선언하기 위해서는 파이썬 표준 모듈인 `typing`을 이용해야 합니다.

구체적으로는 아래 타입 힌트를 지원합니다.

#### `List`

예를 들면, `str`의 `list`인 변수를 정의해봅시다.

`typing`에서  `List`(대문자 `L`)를 import 합니다.

{* ../../docs_src/python_types/tutorial006.py hl[1] *}


콜론(`:`) 문법을 이용하여 변수를 선언합니다.

타입으로는 `List`를 넣어줍니다.

이때 배열은 내부 타입을 포함하는 타입이기 때문에 대괄호 안에 넣어줍니다.

{* ../../docs_src/python_types/tutorial006.py hl[4] *}


/// tip | 팁

대괄호 안의 내부 타입은 "타입 매개변수(type paramters)"라고 합니다.

이번 예제에서는 `str`이 `List`에 들어간 타입 매개변수 입니다.

///

이는 "`items`은 `list`인데, 배열에 들어있는 아이템 각각은 `str`이다"라는 뜻입니다.

이렇게 함으로써, 에디터는 배열에 들어있는 아이템을 처리할때도 도움을 줄 수 있게 됩니다:

<img src="/img/python-types/image05.png">

타입이 없으면 이건 거의 불가능이나 다름 없습니다.

변수 `item`은 `items`의 개별 요소라는 사실을 알아두세요.

그리고 에디터는 계속 `str`라는 사실을 알고 도와줍니다.

#### `Tuple`과 `Set`

`tuple`과 `set`도 동일하게 선언할 수 있습니다.

{* ../../docs_src/python_types/tutorial007.py hl[1,4] *}


이 뜻은 아래와 같습니다:

* 변수 `items_t`는, 차례대로 `int`, `int`, `str`인 `tuple`이다.
* 변수 `items_s`는, 각 아이템이 `bytes`인 `set`이다.

#### `Dict`

`dict`를 선언하려면 컴마로 구분된 2개의 파라미터가 필요합니다.

첫 번째 매개변수는 `dict`의 키(key)이고,

두 번째 매개변수는  `dict`의 값(value)입니다.

{* ../../docs_src/python_types/tutorial008.py hl[1,4] *}


이 뜻은 아래와 같습니다:

* 변수 `prices`는 `dict`이다:
    * `dict`의 키(key)는 `str`타입이다. (각 아이템의 이름(name))
    * `dict`의 값(value)는 `float`타입이다. (각 아이템의 가격(price))

#### `Optional`

`str`과 같이 타입을 선언할 때 `Optional`을 쓸 수도 있는데, "선택적(Optional)"이기때문에 `None`도 될 수 있습니다:

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009.py!}
```

`Optional[str]`을 `str` 대신 쓰게 되면, 특정 값이 실제로는 `None`이 될 수도 있는데 항상 `str`이라고 가정하는 상황에서 에디터가 에러를 찾게 도와줄 수 있습니다.

#### Generic(제네릭) 타입

이 타입은 대괄호 안에 매개변수를 가지며, 종류는:

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...등등

위와 같은 타입은 **Generic(제네릭) 타입** 혹은 **Generics(제네릭스)**라고 불립니다.

### 타입으로서의 클래스

변수의 타입으로 클래스를 선언할 수도 있습니다.

이름(name)을 가진 `Person` 클래스가 있다고 해봅시다.

{* ../../docs_src/python_types/tutorial010.py hl[1:3] *}


그렇게 하면 변수를 `Person`이라고 선언할 수 있게 됩니다.

{* ../../docs_src/python_types/tutorial010.py hl[6] *}


그리고 역시나 모든 에디터 도움을 받게 되겠죠.

<img src="/img/python-types/image06.png">

## Pydantic 모델

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>은 데이터 검증(Validation)을 위한 파이썬 라이브러리입니다.

당신은 속성들을 포함한 클래스 형태로 "모양(shape)"을 선언할 수 있습니다.

그리고 각 속성은 타입을 가지고 있습니다.

이 클래스를 활용하여서 값을 가지고 있는 인스턴스를 만들게 되면, 필요한 경우에는 적당한 타입으로 변환까지 시키기도 하여 데이터가 포함된 객체를 반환합니다.

그리고 결과 객체에 대해서는 에디터의 도움을 받을 수 있게 됩니다.

Pydantic 공식 문서 예시:

{* ../../docs_src/python_types/tutorial011.py *}


/// info | 정보

Pydantic<에 대해 더 배우고 싶다면 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">공식 문서</a>를 참고하세요.</a>

///

**FastAPI**는 모두 Pydantic을 기반으로 되어 있습니다.

이 모든 것이 실제로 어떻게 사용되는지에 대해서는 [자습서 - 사용자 안내서](tutorial/index.md){.internal-link target=_blank} 에서 더 많이 확인하실 수 있습니다.

## **FastAPI**에서의 타입 힌트

**FastAPI**는 여러 부분에서 타입 힌트의 장점을 취하고 있습니다.

**FastAPI**에서 타입 힌트와 함께 매개변수를 선언하면 장점은:

* **에디터 도움**.
* **타입 확인**.

...그리고 **FastAPI**는 같은 정의를 아래에도 적용합니다:

* **요구사항 정의**: 요청 경로 매개변수, 쿼리 매개변수, 헤더, 바디, 의존성 등.
* **데이터 변환**: 요청에서 요구한 타입으로.
* **데이터 검증**: 각 요청마다:
    * 데이터가 유효하지 않은 경우에는 **자동으로 에러**를 발생합니다.
* OpenAPI를 활용한 **API 문서화**:
    * 자동으로 상호작용하는 유저 인터페이스에 쓰이게 됩니다.

위 내용이 다소 추상적일 수도 있지만, 걱정마세요. [자습서 - 사용자 안내서](tutorial/index.md){.internal-link target=_blank}에서 전부 확인 가능합니다.

가장 중요한 건, 표준 파이썬 타입을 한 곳에서(클래스를 더하거나, 데코레이터 사용하는 대신) 사용함으로써 **FastAPI**가 당신을 위해 많은 일을 해준다는 사실이죠.

/// info | 정보

만약 모든 자습서를 다 보았음에도 타입에 대해서 더 보고자 방문한 경우에는 <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy`에서 제공하는 "cheat sheet"</a>이 좋은 자료가 될 겁니다.

///
