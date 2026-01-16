# 하위 의존성 { #sub-dependencies }

**하위 의존성**을 가지는 의존성을 만들 수 있습니다.

필요한 만큼 **깊게** 중첩할 수도 있습니다.

이것을 해결하는 일은 **FastAPI**가 알아서 처리합니다.

## 첫 번째 의존성 "dependable" { #first-dependency-dependable }

다음과 같이 첫 번째 의존성("dependable")을 만들 수 있습니다:

{* ../../docs_src/dependencies/tutorial005_an_py310.py hl[8:9] *}

이 의존성은 선택적 쿼리 파라미터 `q`를 `str`로 선언하고, 그대로 반환합니다.

매우 단순한 예시(그다지 유용하진 않음)이지만, 하위 의존성이 어떻게 동작하는지에 집중하는 데 도움이 됩니다.

## 두 번째 의존성 "dependable"과 "dependant" { #second-dependency-dependable-and-dependant }

그다음, 또 다른 의존성 함수("dependable")를 만들 수 있는데, 이 함수는 동시에 자기 자신의 의존성도 선언합니다(그래서 "dependant"이기도 합니다):

{* ../../docs_src/dependencies/tutorial005_an_py310.py hl[13] *}

선언된 파라미터를 살펴보겠습니다:

* 이 함수 자체가 의존성("dependable")이지만, 다른 의존성도 하나 선언합니다(즉, 다른 무언가에 "의존"합니다).
    * `query_extractor`에 의존하며, 그 반환값을 파라미터 `q`에 할당합니다.
* 또한 선택적 `last_query` 쿠키를 `str`로 선언합니다.
    * 사용자가 쿼리 `q`를 제공하지 않았다면, 이전에 쿠키에 저장해 둔 마지막 쿼리를 사용합니다.

## 의존성 사용하기 { #use-the-dependency }

그다음 다음과 같이 의존성을 사용할 수 있습니다:

{* ../../docs_src/dependencies/tutorial005_an_py310.py hl[23] *}

/// info | 정보

*경로 처리 함수*에서는 `query_or_cookie_extractor`라는 의존성 하나만 선언하고 있다는 점에 주목하세요.

하지만 **FastAPI**는 `query_or_cookie_extractor`를 호출하는 동안 그 결과를 전달하기 위해, 먼저 `query_extractor`를 해결해야 한다는 것을 알고 있습니다.

///

```mermaid
graph TB

query_extractor(["query_extractor"])
query_or_cookie_extractor(["query_or_cookie_extractor"])

read_query["/items/"]

query_extractor --> query_or_cookie_extractor --> read_query
```

## 같은 의존성을 여러 번 사용하기 { #using-the-same-dependency-multiple-times }

같은 *경로 처리*에 대해 의존성 중 하나가 여러 번 선언되는 경우(예: 여러 의존성이 공통 하위 의존성을 갖는 경우), **FastAPI**는 그 하위 의존성을 요청당 한 번만 호출해야 한다는 것을 알고 있습니다.

그리고 같은 요청에 대해 동일한 의존성을 여러 번 호출하는 대신, 반환값을 <abbr title="계산/생성된 값을 저장해 두었다가, 다시 계산하지 않고 재사용하기 위한 유틸리티/시스템.">"cache"</abbr>에 저장하고, 그 요청에서 해당 값이 필요한 모든 "dependants"에 전달합니다.

고급 시나리오로, 같은 요청에서 "cached" 값을 쓰는 대신 매 단계마다(아마도 여러 번) 의존성이 호출되어야 한다는 것을 알고 있다면, `Depends`를 사용할 때 `use_cache=False` 파라미터를 설정할 수 있습니다:

//// tab | Python 3.9+

```Python hl_lines="1"
async def needy_dependency(fresh_value: Annotated[str, Depends(get_value, use_cache=False)]):
    return {"fresh_value": fresh_value}
```

////

//// tab | Python 3.9+ 비 Annotated

/// tip | 팁

가능하다면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python hl_lines="1"
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
```

////

## 정리 { #recap }

여기서 사용한 그럴듯한 용어들을 제외하면, **Dependency Injection** 시스템은 꽤 단순합니다.

*경로 처리 함수*와 같은 형태의 함수들일 뿐입니다.

하지만 여전히 매우 강력하며, 임의로 깊게 중첩된 의존성 "그래프"(트리)를 선언할 수 있습니다.

/// tip | 팁

이 단순한 예시만 보면 그다지 유용해 보이지 않을 수도 있습니다.

하지만 **보안**에 관한 챕터에서 이것이 얼마나 유용한지 보게 될 것입니다.

또한 얼마나 많은 코드를 아껴주는지도 보게 될 것입니다.

///
