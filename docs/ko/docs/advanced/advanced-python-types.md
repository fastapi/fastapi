# 고급 Python 타입 { #advanced-python-types }

Python 타입을 다룰 때 유용할 수 있는 몇 가지 추가 아이디어를 소개합니다.

## `Union` 또는 `Optional` 사용 { #using-union-or-optional }

어떤 이유로 코드에서 `|`를 사용할 수 없다면, 예를 들어 타입 어노테이션이 아니라 `response_model=` 같은 곳이라면, 파이프 문자(`|`) 대신 `typing`의 `Union`을 사용할 수 있습니다.

예를 들어, 어떤 값이 `str` 또는 `None`이 될 수 있다고 선언할 수 있습니다:

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing`에는 `None`이 될 수 있음을 선언하는 축약형으로 `Optional`도 있습니다.

아주 개인적인 관점에서의 팁입니다:

- 🚨 `Optional[SomeType]` 사용은 피하세요
- 대신 ✨ **`Union[SomeType, None]`를 사용하세요** ✨.

둘은 동등하며 내부적으로도 같습니다. 하지만 단어 "optional"은 값이 선택 사항이라는 인상을 주는 반면, 실제 의미는 "값이 `None`이 될 수 있다"는 뜻입니다. 값이 선택 사항이 아니라 여전히 필수인 경우에도 그렇습니다.

`Union[SomeType, None]`가 의미를 더 명확하게 드러낸다고 생각합니다.

이는 단지 단어와 명칭의 문제입니다. 하지만 이런 단어가 여러분과 팀원이 코드를 어떻게 생각하는지에 영향을 줄 수 있습니다.

예를 들어, 다음 함수를 보세요:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

매개변수 `name`은 `Optional[str]`로 정의되어 있지만, 사실 선택적이지 않습니다. 이 매개변수 없이 함수를 호출할 수 없습니다:

```Python
say_hi()  # 이런, 에러가 발생합니다! 😱
```

`name` 매개변수는 기본값이 없기 때문에 여전히 필수입니다(선택적이 아님). 대신, `name`에는 `None`을 전달할 수 있습니다:

```Python
say_hi(name=None)  # 작동합니다. None은 유효합니다 🎉
```

좋은 소식은, 대부분의 경우 타입의 합집합을 정의할 때 그냥 `|`를 사용할 수 있다는 점입니다:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

그래서 보통은 `Optional`과 `Union` 같은 이름에 대해 걱정하지 않으셔도 됩니다. 😎
