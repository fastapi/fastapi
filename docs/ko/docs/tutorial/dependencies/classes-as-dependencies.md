# 의존성으로서의 클래스

**의존성 주입**시스템을 더 깊이 알아보기 전에, 이전 예시를 개선해봅시다.

## 이전 예시에서의 `dict`

이전 예시에서, ("의존 가능한") 의존성으로부터 `dict`을 반환했습니다:

```Python hl_lines="9"
{!../../../docs_src/dependencies/tutorial001.py!}
```

그러나 *경로 동작 함수*의 매개변수 `commons` 내부에 `dict`을 받게 됩니다.

그리고 키와 값의 자료형을 모르기 때문에, 편집기가 `dict`에 대한 (완성 기능과 같은) 많은 지원을 제공할 수 없습니다.

이것을 더 개선할 수 있습니다...

## 의존성으로 만들어주는 것

지금까지 함수로 선언된 의존성을 보았습니다.

그러나 그것이 (더 일반적인 상황임에도 불구하고) 의존성을 선언하는 유일한 방법이 아닙니다.

주요한 사실은 의존성이 "호출 가능"해야 한다는 것입니다.

파이썬에서는 함수와 같이 파이썬이 "호출"할 수 있는 모든 것이 **"호출 가능"**합니다.

따라서, (함수가 _아닐_ 수도 있는) `something` 객체가 있다면 다음과 같이 "호출" (실행) 할 수 있습니다:

```Python
something()
```

또는

```Python
something(some_argument, some_keyword_argument="foo")
```

그러면 이것은 "호출 가능"합니다.

## 의존성으로서의 클래스

파이썬 클래스의 인스턴스를 생성하기 위해, 동일한 문법을 사용한다는 걸 알 수 있습니다.

예를 들어: 

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

이 사례에서, `fluffy`는 클래스 `Cat`의 인스턴스입니다.

그리고 `fluffly`를 생성하기 위해, `Cat`을 "호출"합니다.

따라서, 파이썬 클래스 또한 **호출 가능**합니다.

결국, **FastAPI**에서, 의존성으로서 파이썬 클래스를 사용할 수 있습니다.

FastAPI가 실질적으로 확인하는 것은 "호출 가능성" (함수, 클래스 또는 다른 모든 것) 및 정의된 매개변수입니다.

"호출 가능"한 것을 의존성으로서 **FastAPI**에 전달하면, 해당 "호출 가능"한 것에 대한 매개변수를 분석하고 하위-의존성을 포함하여 *경로 동작 함수*를 위한 매개변수와 동일한 방식으로 처리됩니다.

매개변수가 전혀 없는 호출 가능한 것에도 매개변수가 없는 *경로 동작 함수*와 동일한 방식으로 적용됩니다.

따라서, 위에 작성된 "의존 가능한" `common_parameters` 의존성을 클래스 `CommonQueryParams`로 바꿀 수 있습니다:

```Python hl_lines="11-15"
{!../../../docs_src/dependencies/tutorial002.py!}
```

클래스의 인스턴스를 생성하는 데 사용되는 `__init__` 메서드에 주목하기 바랍니다:

```Python hl_lines="12"
{!../../../docs_src/dependencies/tutorial002.py!}
```

...이전 `common_parameters`와 동일한 매개변수를 가집니다:

```Python hl_lines="8"
{!../../../docs_src/dependencies/tutorial001.py!}
```

이 매개변수들은 **FastAPI**가 의존성을 "해결"하기 위해 사용되는 것입니다.

함수와 클래스 두 가지 경우 모두, 아래 요소를 갖습니다:

* 선택적 `q` 쿼리 매개변수.
* 기본 값이 `0`인, `skip` 쿼리 매개변수.
* 기본 값이 `100`인, `limit` 쿼리 매개변수.

두 가지 경우 모두, 데이터는 변환, 검증되고 OpenAPI 스키마에 문서화됩니다.

## 사용

이제 클래스를 사용하여 의존성을 선언할 수 있습니다.

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial002.py!}
```

**FastAPI**는 `CommonQueryParams` 클래스를 호출합니다. 이것은 해당 클래스의 "인스턴스"를 생성하고 그 인스턴스는 함수의 매개변수 `commons`로 전달됩니다.

## 자료형 어노테이션 vs `Depends`

위 코드에서 어떻게 `CommonQueryParams`를 두 번이나 작성했는 지 주목하기 바랍니다:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

마지막 `CommonQueryParams`, 내부:

```Python
... = Depends(CommonQueryParams)
```

...는 **FastAPI**가 실제로 무엇이 의존성인지 알기 위해 사용하는 것입니다.

이를 통해 FastAPI는 선언된 매개변수를 추출하고 이것을 FastAPI가 실제로 호출합니다.

---

이 경우, 첫 번째 `CommonQueryParams`, 내부:

```Python
commons: CommonQueryParams ...
```

...는 **FastAPI**에 어떤 특별한 의미도 없습니다. FastAPI는 이것을 (`=Depends(CommonQueryParams)` 사용을 통해 할 수 있었던 작업인) 데이터 변환, 검증, 기타 등등 어떤 작업에도 사용하지 않습니다.

단지 다음과 같이 작성할 수 있습니다:

```Python
commons = Depends(CommonQueryParams)
```

...이것은 아래와 같습니다:

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial003.py!}
```

그러나 자료형을 선언하는 것은 편집기가 매개변수 `Commons`로 전달될 것이 무엇인지 알고, 코드 완성, 자료형 확인 등에 도움이 될 수 있으므로 권장됩니다.

<img src="/img/tutorial/dependencies/image02.png">

## 손쉬운 방법

그러나 여기 `CommonQueryParams`를 두 번이나 작성하는, 코드 반복이 있다는 걸 보았습니다:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**FastAPI**는 의존성이 *특히* **FastAPI**가 클래스 자체의 인스턴스를 생성하기 위해 "호출"하는 클래스인 경우, 손쉬운 방법을 제공합니다.

이러한 특정 사례를 위해, 다음과 같이 작업할 수 있습니다:

아래와 같이 작성하는 대신:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...아래와 같이 작성할 수 있습니다:

```Python
commons: CommonQueryParams = Depends()
```

의존성을 매개변수의 자료형으로 선언하고, `Depends(CommonQueryParams)`와 같이 내부 전체 클래스를 *다시* 작성해야 하는 대신, `Depends()`와 같이 내부에 어떤 매개변수도 없이, 함수의 매개변수에 (`=` 다음에 오는) 기본 값으로 `Depends()`를 사용합니다.

동일한 예제가 아래와 같습니다:

```Python hl_lines="19"
{!../../../docs_src/dependencies/tutorial004.py!}
```

...그리고 **FastAPI**는 무엇을 해야할 지 알게 됩니다.

!!! tip "팁"
    만약 이것이 도움이 되기보다 더 헷갈리게 만든다면, *필요* 없기 때문에, 잊어버리기 바랍니다.

    이것은 단지 손쉬운 방법일 뿐입니다. 왜냐하면 **FastAPI**는 코드 반복을 최소화할 수 있는 방법을 고민하기 때문입니다.
