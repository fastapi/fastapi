# 의존성으로서의 클래스

**의존성 주입** 시스템에 대해 자세히 살펴보기 전에 이전 예제를 업그레이드 해보겠습니다.

## 이전 예제의 `딕셔너리`

이전 예제에서, 우리는 의존성(의존 가능한) 함수에서 `딕셔너리`객체를 반환하고 있었습니다:

{* ../../docs_src/dependencies/tutorial001.py hl[9] *}

우리는 *경로 작동 함수*의 매개변수 `commons`에서 `딕셔너리` 객체를 얻습니다.

그리고 우리는 에디터들이 `딕셔너리` 객체의 키나 밸류의 자료형을 알 수 없기 때문에 자동 완성과 같은 기능을 제공해 줄 수 없다는 것을 알고 있습니다.

더 나은 방법이 있을 것 같습니다...

## 의존성으로 사용 가능한 것

지금까지 함수로 선언된 의존성을 봐왔습니다.

아마도 더 일반적이기는 하겠지만 의존성을 선언하는 유일한 방법은 아닙니다.

핵심 요소는 의존성이 "호출 가능"해야 한다는 것입니다

파이썬에서의 "**호출 가능**"은 파이썬이 함수처럼 "호출"할 수 있는 모든 것입니다.

따라서, 만약 당신이 `something`(함수가 아닐 수도 있음) 객체를 가지고 있고,

```Python
something()
```

또는

```Python
something(some_argument, some_keyword_argument="foo")
```

상기와 같은 방식으로 "호출(실행)" 할 수 있다면 "호출 가능"이 됩니다.

## 의존성으로서의 클래스

파이썬 클래스의 인스턴스를 생성하기 위해 사용하는 것과 동일한 문법을 사용한다는 걸 알 수 있습니다.

예를 들어:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

이 경우에 `fluffy`는 클래스 `Cat`의 인스턴스입니다. 그리고 우리는 `fluffy`를 만들기 위해서 `Cat`을 "호출"했습니다.

따라서, 파이썬 클래스는 **호출 가능**합니다.

그래서 **FastAPI**에서는 파이썬 클래스를 의존성으로 사용할 수 있습니다.

FastAPI가 실질적으로 확인하는 것은 "호출 가능성"(함수, 클래스 또는 다른 모든 것)과 정의된 매개변수들입니다.

"호출 가능"한 것을 의존성으로서 **FastAPI**에 전달하면, 그 "호출 가능"한 것의 매개변수들을 분석한 후 이를 *경로 작동 함수*를 위한 매개변수와 동일한 방식으로 처리합니다. 하위-의존성 또한 같은 방식으로 처리합니다.

매개변수가 없는 "호출 가능"한 것 역시 매개변수가 없는 *경로 작동 함수*와 동일한 방식으로 적용됩니다.

그래서, 우리는 위 예제에서의 `common_paramenters` 의존성을 클래스 `CommonQueryParams`로 바꿀 수 있습니다.

{* ../../docs_src/dependencies/tutorial002.py hl[11:15] *}

클래스의 인스턴스를 생성하는 데 사용되는 `__init__` 메서드에 주목하기 바랍니다:

{* ../../docs_src/dependencies/tutorial002.py hl[12] *}

...이전 `common_parameters`와 동일한 매개변수를 가집니다:

{* ../../docs_src/dependencies/tutorial001.py hl[9] *}

이 매개변수들은 **FastAPI**가 의존성을 "해결"하기 위해 사용할 것입니다

함수와 클래스 두 가지 방식 모두, 아래 요소를 갖습니다:

* `문자열`이면서 선택사항인 쿼리 매개변수 `q`.
* 기본값이 `0`이면서 `정수형`인 쿼리 매개변수 `skip`
* 기본값이 `100`이면서 `정수형`인 쿼리 매개변수 `limit`

두 가지 방식 모두, 데이터는 변환, 검증되고 OpenAPI 스키마에 문서화됩니다.

## 사용해봅시다!

이제 아래의 클래스를 이용해서 의존성을 정의할 수 있습니다.

{* ../../docs_src/dependencies/tutorial002.py hl[19] *}

**FastAPI**는 `CommonQueryParams` 클래스를 호출합니다. 이것은 해당 클래스의 "인스턴스"를 생성하고 그 인스턴스는 함수의 매개변수 `commons`로 전달됩니다.

## 타입 힌팅 vs `Depends`

위 코드에서 `CommonQueryParams`를 두 번 작성한 방식에 주목하십시오:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

마지막 `CommonQueryParams` 변수를 보면:

```Python
... = Depends(CommonQueryParams)
```

... **FastAPI**가 실제로 어떤 것이 의존성인지 알기 위해서 사용하는 방법입니다.
FastAPI는 선언된 매개변수들을 추출할 것이고 실제로 이 변수들을 호출할 것입니다.

---

이 경우에, 첫번째 `CommonQueryParams` 변수를 보면:

```Python
commons: CommonQueryParams ...
```

... **FastAPI**는 `CommonQueryParams` 변수에 어떠한 특별한 의미도 부여하지 않습니다. FastAPI는 이 변수를 데이터 변환, 검증 등에 활용하지 않습니다. (활용하려면 `= Depends(CommonQueryParams)`를 사용해야 합니다.)

사실 아래와 같이 작성해도 무관합니다:

```Python
commons = Depends(CommonQueryParams)
```

..전체적인 코드는 아래와 같습니다:

{* ../../docs_src/dependencies/tutorial003.py hl[19] *}

그러나 자료형을 선언하면 에디터가 매개변수 `commons`로 전달될 것이 무엇인지 알게 되고, 이를 통해 코드 완성, 자료형 확인 등에 도움이 될 수 있으므로 권장됩니다.

<!-- <img src="/img/tutorial/dependencies/image02.png"> -->

## 코드 단축

그러나 여기 `CommonQueryParams`를 두 번이나 작성하는, 코드 반복이 있다는 것을 알 수 있습니다:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

**FastAPI**는 *특히* 의존성이 **FastAPI**가 클래스 자체의 인스턴스를 생성하기 위해 "호출"하는 클래스인 경우, 조금 더 쉬운 방법을 제공합니다.

이러한 특정한 경우에는 아래처럼 사용할 수 있습니다:

이렇게 쓰는 것 대신:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...이렇게 쓸 수 있습니다.:

```Python
commons: CommonQueryParams = Depends()
```

의존성을 매개변수의 타입으로 선언하는 경우 `Depends(CommonQueryParams)`처럼 클래스 이름 전체를 *다시* 작성하는 대신, 매개변수를 넣지 않은 `Depends()`의 형태로 사용할 수 있습니다.

아래에 같은 예제가 있습니다:

{* ../../docs_src/dependencies/tutorial004.py hl[19] *}

...이렇게 코드를 단축하여도 **FastAPI**는 무엇을 해야하는지 알고 있습니다.

/// tip | 팁

만약 이것이 도움이 되기보다 더 헷갈리게 만든다면, 잊어버리십시오. 이것이 반드시 필요한 것은 아닙니다.

이것은 단지 손쉬운 방법일 뿐입니다. 왜냐하면 **FastAPI**는 코드 반복을 최소화할 수 있는 방법을 고민하기 때문입니다.

///
