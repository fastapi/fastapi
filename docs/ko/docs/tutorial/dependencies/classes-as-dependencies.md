# 의존성으로서의 클래스 { #classes-as-dependencies }

**의존성 주입** 시스템에 대해 더 깊이 살펴보기 전에, 이전 예제를 업그레이드해 보겠습니다.

## 이전 예제의 `dict` { #a-dict-from-the-previous-example }

이전 예제에서는 의존성("dependable")에서 `dict`를 반환하고 있었습니다:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

하지만 그러면 *경로 처리 함수*의 매개변수 `commons`에서 `dict`를 받게 됩니다.

그리고 에디터는 `dict`의 키와 값 타입을 알 수 없기 때문에 `dict`에 대해서는 (완성 기능 같은) 많은 지원을 제공할 수 없다는 것을 알고 있습니다.

더 나은 방법이 있습니다...

## 의존성이 되기 위한 조건 { #what-makes-a-dependency }

지금까지는 함수로 선언된 의존성을 봤습니다.

하지만 그것만이 의존성을 선언하는 유일한 방법은 아닙니다(아마도 더 일반적이긴 하겠지만요).

핵심 요소는 의존성이 "호출 가능(callable)"해야 한다는 것입니다.

파이썬에서 "**호출 가능(callable)**"이란 파이썬이 함수처럼 "호출"할 수 있는 모든 것입니다.

따라서 `something`(함수가 _아닐_ 수도 있습니다)이라는 객체가 있고, 다음처럼 "호출"(실행)할 수 있다면:

```Python
something()
```

또는

```Python
something(some_argument, some_keyword_argument="foo")
```

그것은 "호출 가능(callable)"입니다.

## 의존성으로서의 클래스 { #classes-as-dependencies_1 }

파이썬 클래스의 인스턴스를 만들 때도 같은 문법을 사용한다는 것을 알 수 있을 겁니다.

예를 들어:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

이 경우 `fluffy`는 클래스 `Cat`의 인스턴스입니다.

그리고 `fluffy`를 만들기 위해 `Cat`을 "호출"하고 있습니다.

따라서 파이썬 클래스도 **호출 가능(callable)**합니다.

그러면 **FastAPI**에서는 파이썬 클래스를 의존성으로 사용할 수 있습니다.

FastAPI가 실제로 확인하는 것은 그것이 "호출 가능(callable)"(함수, 클래스, 또는 다른 무엇이든)한지와 정의된 매개변수들입니다.

**FastAPI**에서 "호출 가능(callable)"한 것을 의존성으로 넘기면, 그 "호출 가능(callable)"한 것의 매개변수들을 분석하고 *경로 처리 함수*의 매개변수와 동일한 방식으로 처리합니다. 하위 의존성도 포함해서요.

이것은 매개변수가 전혀 없는 callable에도 적용됩니다. 매개변수가 없는 *경로 처리 함수*에 적용되는 것과 동일합니다.

그러면 위의 의존성("dependable") `common_parameters`를 클래스 `CommonQueryParams`로 바꿀 수 있습니다:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

클래스의 인스턴스를 만들 때 사용하는 `__init__` 메서드에 주목하세요:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...이전의 `common_parameters`와 동일한 매개변수를 가지고 있습니다:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

이 매개변수들이 **FastAPI**가 의존성을 "해결"하는 데 사용할 것들입니다.

두 경우 모두 다음을 갖게 됩니다:

* `str`인 선택적 쿼리 매개변수 `q`.
* 기본값이 `0`인 `int` 쿼리 매개변수 `skip`.
* 기본값이 `100`인 `int` 쿼리 매개변수 `limit`.

두 경우 모두 데이터는 변환되고, 검증되며, OpenAPI 스키마에 문서화되는 등 여러 처리가 적용됩니다.

## 사용하기 { #use-it }

이제 이 클래스를 사용해 의존성을 선언할 수 있습니다.

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI**는 `CommonQueryParams` 클래스를 호출합니다. 그러면 해당 클래스의 "인스턴스"가 생성되고, 그 인스턴스가 함수의 매개변수 `commons`로 전달됩니다.

## 타입 어노테이션 vs `Depends` { #type-annotation-vs-depends }

위 코드에서 `CommonQueryParams`를 두 번 작성하는 방식에 주목하세요:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

마지막 `CommonQueryParams`는, 다음에서:

```Python
... Depends(CommonQueryParams)
```

...**FastAPI**가 실제로 무엇이 의존성인지 알기 위해 사용하는 것입니다.

FastAPI는 여기에서 선언된 매개변수들을 추출하고, 실제로 이것을 호출합니다.

---

이 경우 첫 번째 `CommonQueryParams`는 다음에서:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
commons: CommonQueryParams ...
```

////

...**FastAPI**에 특별한 의미가 없습니다. FastAPI는 이를 데이터 변환, 검증 등에 사용하지 않습니다(그런 용도로는 `Depends(CommonQueryParams)`를 사용하고 있기 때문입니다).

실제로는 이렇게만 작성해도 됩니다:

//// tab | Python 3.9+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
commons = Depends(CommonQueryParams)
```

////

...다음과 같이요:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

하지만 타입을 선언하는 것을 권장합니다. 그러면 에디터가 매개변수 `commons`에 무엇이 전달되는지 알 수 있고, 코드 완성, 타입 체크 등에서 도움을 받을 수 있습니다:

<img src="/img/tutorial/dependencies/image02.png">

## 단축 { #shortcut }

하지만 `CommonQueryParams`를 두 번 작성하는 코드 반복이 있다는 것을 볼 수 있습니다:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI**는 이런 경우를 위한 단축 방법을 제공합니다. 이때 의존성은 *특히* **FastAPI**가 "호출"해서 클래스 자체의 인스턴스를 만들도록 하는 클래스입니다.

이 특정한 경우에는 다음과 같이 할 수 있습니다:

다음처럼 작성하는 대신:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...이렇게 작성합니다:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
commons: CommonQueryParams = Depends()
```

////

의존성을 매개변수의 타입으로 선언하고, `Depends(CommonQueryParams)` 안에 클래스 전체를 *다시* 작성하는 대신 매개변수 없이 `Depends()`를 사용합니다.

그러면 같은 예제는 다음처럼 보일 겁니다:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...그리고 **FastAPI**는 무엇을 해야 하는지 알게 됩니다.

/// tip | 팁

도움이 되기보다 더 헷갈린다면, 무시하세요. 이건 *필수*가 아닙니다.

그저 단축 방법일 뿐입니다. **FastAPI**는 코드 반복을 최소화하도록 도와주는 것을 중요하게 생각하기 때문입니다.

///
