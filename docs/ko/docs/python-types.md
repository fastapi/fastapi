# 파이썬 타입 소개

파이썬은 선택적으로 "타입 힌트(type hints)"를 지원합니다.

이러한 **타입 힌트**들은 변수의 <abbr title="예를 들면: str, int, float, bool">타입</abbr>을 선언할 수 있게 해주는 특수한 구문입니다.

변수들의 타입을 선언함으로써, 편집기와 도구들이 당신에게 더 나은 지원을 제공할 수 있습니다.

이 문서는 단지 파이썬 타입 힌트에 대한 **빠른 자습서 / 복습**일 뿐입니다. 이것은 **FastAPI**에 사용하기 위한 최소한의 필요한 내용만을 다룹니다... 사실 굉장히 적은 내용입니다.

**FastAPI**는 모두 이런 타입 힌트에 기반해 있는데, 이는 많은 장점과 이익을 가져다 줍니다.

하지만 당신이 **FastAPI**를 사용할 일이 없다고 하더라도, 타입 힌트에 대해 살짝 공부하는 것은 도움이 될 것입니다.

!!! 참고
    만약 당신이 파이썬 전문가라면, 그리고 이미 타입 힌트에 대해 모든 것을 알고 있다면 다음 챕터로 바로 넘어가시면 됩니다.

## 동기부여

간단한 예시로 시작해봅시다:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

이런 프로그램 출력값을 불러와 봅시다:

```
John Doe
```

이 함수는 다음의 역할을 수행합니다: 

* `first_name`(이름)과 `last_name`(성)을 받습니다.
* `title()`을 이용해서 각각의 첫 글자를 대문자로 변환합니다.
* 사이에 공백 한 칸을 두고 둘을 <abbr title="하나로 붙입니다. 하나의 내용 다음에 다른 하나의 내용이 오도록.">연결</abbr> 합니다.


```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### 편집하기

이것은 굉장히 간단한 프로그램입니다.

하지만 이제 당신이 이것을 스크래치에서 작성하고 있다고 상상해봅시다.

어느 시점에서 당신은 함수의 정의를 시작했을 수 있습니다, 매개변수는 준비 되었고... 

그런데 이제 당신은 "첫 글자를 대문자로 변환하는 그 방법"이 무엇인지 불러내야 합니다.

그게 `upper`였나? `uppercase`였나? `first_uppercase`? `capitalize`?

그럼 당신은 오래된 프로그래머의 친구인, 편집기 자동완성으로 시도를 해봅니다.

당신은 함수의 첫 매개변수 `first_name`을 입력하고, 그리고 마침표(`.`)를 입력하고, `Ctrl+Space` 를 눌러서 자동완성을 시키려합니다.

애석하게도 쓸만한 것을 찾지 못합니다.

<img src="/img/python-types/image01.png">

### 타입 추가하기

기존 버전에서 한 줄을 수정해봅시다.

우리는 정확히 이 부분, 함수의 매개변수 부분을 바꿀 것입니다, 이렇게 되어있는 것에서:

```Python
    first_name, last_name
```

이렇게 되도록:

```Python
    first_name: str, last_name: str
```

그게 끝입니다.

이것들이 바로 "타입 힌트" 입니다:


```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

이는 다음과 같이 기본 값을 선언하는 것과는 같지 않습니다:


```Python
    first_name="john", last_name="doe"
```

이는 다른 것입니다.

우리는 콜론(`:`)을 사용하고 있지, 등호(`=`)를 사용하지 않습니다.

그리고 타입 힌트를 추가한다고 해서 대개 타입힌트가 없었을 때 일어났을 일과 다른 변화가 일어나지는 않습니다.

그렇지만 이제, 당신이 다시 함수를 생성하는 한가운데에 있다고 상상해봅시다, 다만 이번엔 타입 힌트가 있습니다.

같은 시점에서, 당신은 `Ctrl+Space`로 자동완성을 하려고 시도하고 다음을 보게 됩니다:

<img src="/img/python-types/image02.png">

이로써, 당신은 스크롤을 하여, 당신이 원하던 것을 찾을 때까지, 선택지들을 봅니다.

<img src="/img/python-types/image03.png">

## 더욱 동기부여

이 함수를 보십시오, 이미 타입 힌트가 있습니다: 

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

편집기가 변수들의 타입들을 알기 때문에, 당신은 자동완성을 받을 뿐 아니라 오류(error) 체크까지 받습니다:


<img src="/img/python-types/image04.png">

이제 당신은 이것을 수정해야 하는 것을 알고 있습니다, `age`를 `str(age)`을 통해 문자열로 변환합니다:


```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## 타입 선언하기 

방금 타입 힌트를 선언하는 주요 위치(main place)를 보셨습니다. 함수 매개 변수입니다.

이것은 마찬가지로 **FastAPI**와 함께 사용하는 주요 위치입니다.

### 간단한 타입들 Simple types
당신은 `str` 뿐만 아니라 모든 표준 파이썬 타입들을 다 선언할 수 있습니다.

당신은 예를 들어 이런 타입들을 사용할 수 있습니다:

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### 타입 매개변수가 있는 제네릭 타입
`dict`, `list`, `set` 그리고 `tuple`과 같이 다른 값을 포함할 수 있는 자료 구조들도 있습니다. 그리고 그 내부값들 역시 각자 고유의 타입을 가질 수 있습니다.

이들의 타입과 내부 타입을 선언하기 위해서, 당신은 표준 파이썬 모듈 `typing`을 사용할 수 있습니다.

이것은 특히 이러한 타입 힌트들을 지원하기 위해서 존재합니다.


#### `List`

예를 들어, 한 변수가 `str`의 `list`가 되도록 정의해 봅시다.

`typing`에서 `List`(대문자 `L`을 사용)를 가져옵니다:


```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial006.py!}
```

동일하게 콜론(`:`) 구문을 사용하여, 변수를 선언합니다.

타입으로는 `List`를 넣습니다.

리스트는 내부 타입(internal types)를 포함하는 타입이기 때문에, 이들을 대괄호 안에 넣습니다:


```Python hl_lines="4"
{!../../../docs_src/python_types/tutorial006.py!}
```

!!! 팁
    이렇게 대괄호 안에 있는 내부 타입(internal types)들은 "타입 매개변수"라고 부릅니다. 
    이런 경우에는 `str`이 `List`에 전달되는 매개변수입니다.

이는 "변수 `items`는 `list`이고, 이 리스트의 각 item들은 `str`임"을 의미합니다. 

이로써, 당신의 편집기는 리스트에서 아이템들을 프로세싱 하는 도중에도 지원을 제공할 수 있게 됩니다:

<img src="/img/python-types/image05.png">

타입이 없이는, 이것은 거의 달성하기 불가능합니다.

변수 `item`은 리스트 `items`의 원소 중 하나임을 유의하십시오.

그리고 여전히, 편집기는 이것이 `str`임을 알고 있으며, 그에 대한 지원을 제공합니다.


#### `Tuple` 과 `Set`
당신은 `tuple`과 `set`을 선언하기 위해서도 동일하게 합니다:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial007.py!}
```

이는 다음을 의미합니다:

* 변수 `items_t` 는 3개의 아이템을 가진 `tuple` 이며 각 아이템의 타입은 `int`, 또 다른 `int` 그리고 `str`입니다.
* 변수 `items_s` 는 `set`이며, 각각의 아이템은 `bytes`타입입니다.

#### `Dict`

`dict`을 정의하기 위해서는 당신은 쉼표로 구분된 2개의 타입의 매개변수를 pass합니다.

첫번째 타입 매개변수는 `dict`의 키를 위한 것입입니다.

두번째 타입 매개변수는 `dict`의 값을 위한 것입니다:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial008.py!}
```

이는 다음을 의미합니다:

* 변수 `prices`는 `dict`입니다:
    * 이 `dict`의 키(key)들은 `str` 타입입니다 (각 아이템의 이름이라고 해봅시다).
    * 이 `dict`의 값(value)들은 `float` 타입입니다 (각 아이템의 가격이라고 해봅시다).

#### `Optional`

당신은 어떤 변수가 `str`과 같이 타입을 가지고 있다고 선언하고 싶을 때에도 `Optional`을 사용할 수 있습니다. 다만 이 타입이 "선택적(optional)"이라는 것입니다. 이는 `None`도 될 수 있음을 의미합니다 :


```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```
그냥 `str`이 아닌 `Optional[str]`을 사용하는 것은, 당신이 어떤 값이 항상 `str`일 것이라고 가정했는데, 사실은 `None`도 될 수 있는 경우에, 편집기가 오류를 감지할 수 있도록 해줍니다.


#### 제네릭 타입 
대괄호 안에 타입 매개변수를 가지는 타입들, 예를 들어:

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...등등.

이들을 **제네릭 타입** 또는 **제네릭스**라고 부릅니다.

### 타입으로서의 클래스

당신은 클래스도 변수의 타입으로서 선언할 수 있습니다.

다음과 같은 이름을 가진 `Person` 이라는 클래스가 있다고 생각해봅시다 :

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

그러면 당신은 `Person` 타입의 변수를 선언할 수 있습니다 :


```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

그 다음엔, 다시, 당신은 편집기의 모든 도움을 받습니다:

<img src="/img/python-types/image06.png">

## Pydantic 모델들

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>은 데이터 검증을 수행하기 위한 파이썬 라이브러리입니다.


당신은 어트리뷰트가 있는 클래스로서 데이터의 "형상(shape)"을 선언합니다.

그리고 각각의 어트리뷰트들은 타입을 가지고 있습니다.

그다음 어떤 값들을 가진 그 클래스의 인스턴스를 생성하면, 그것이 값을 검증하고 (필요한 경우) 올바른 타입으로 변환해주고 당신에게 모든 데이터를 포함한 객체를 제공해줄 것입니다.


그리고 당신은 그 결과로서의 객체로 편집기의 모든 지원을 받습니다.

Pydantic 공식 문서에서 가져왔습니다:

```Python
{!../../../docs_src/python_types/tutorial011.py!}
```

!!! 정보
    Pydantic에 대해 더 알아보고 싶다면 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic 문서</a>를 확인해보십시오.


**FastAPI**는 모두 Pydantic에 기반을 두고 있습니다.

이 모든 것이 실제로 어떻게 사용되는지에 대해서는 [자습서 - 사용자 안내서](tutorial/index.md){.internal-link target=_blank} 에서 더 많이 확인하실 수 있습니다.

## **FastAPI** 에서의 타입 힌트

**FastAPI**는 몇가지를 하기 위해 이런 타입 힌트의 이점을 취합니다.

**FastAPI**로 당신은 타입 힌트가 있는 변수를 선언하고 다음을 얻습니다:

* **편집기 지원(Editor support)**.
* **타입 검사(Type checks)**.


...그리고 **FastAPI**는 다음을 하기 위해 동일한 선언을 사용합니다:

* **요구사항을 정의하기**: 요청 경로, 경로 매개변수, 쿼리 매개변수, 헤더, 바디, 의존성 등으로부터.
* **데이터를 변환하기**: 요청에서 요구되는 타입으로.
* **데이터를 검증하기**: 각 요청으로부터 오는:
    * 데이터가 유효하지 않을 경우 클라이언트에 반환되는 **자동 오류**를 생성하는 것
* 오픈API를 이용하여 API를 **문서화하기 Document** :
    * 이는 다음에 자동 대화형 문서 사용자 인터페이스에 의해 사용됩니다. 

이것이 모두 추상적으로 들릴 수 있습니다. 걱정하지 마십시오. 당신은 이 모든 것의 실제 사용을 [자습서 - 사용자 안내서](tutorial/index.md){.internal-link target=_blank}에서 보게 될 것입니다. 


중요한것은 표준 파이썬 타입을 사용함으로써, 한 자리에서 (클래스, decorator 등을 추가하는 대신에) **FastAPI**가 당신을 위해 많은 일을 해줄 것이라는 점입니다.

!!! 정보
    만약 당신이 이미 자습서를 모두 보고나서 타입에 대해 더 알아보고자 여기로 돌아왔다면, 좋은 참고자료가 여기 있습니다 - <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">컨닝페이퍼, 출처 `mypy`</a>.