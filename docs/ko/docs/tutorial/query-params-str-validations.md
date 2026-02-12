# 쿼리 매개변수와 문자열 검증 { #query-parameters-and-string-validations }

**FastAPI**를 사용하면 매개변수에 대한 추가 정보 및 검증을 선언할 수 있습니다.

이 응용 프로그램을 예로 들어보겠습니다:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

쿼리 매개변수 `q`는 `str | None` 자료형입니다. 즉, `str` 자료형이지만 `None` 역시 될 수 있음을 뜻하고, 실제로 기본값은 `None`이기 때문에 FastAPI는 이 매개변수가 필수가 아니라는 것을 압니다.

/// note | 참고

FastAPI는 `q`의 기본값이 `= None`이기 때문에 필수가 아님을 압니다.

`str | None`을 사용하면 편집기가 더 나은 지원과 오류 탐지를 제공하게 해줍니다.

///

## 추가 검증 { #additional-validation }

`q`가 선택적이지만 값이 주어질 때마다 **길이가 50자를 초과하지 않게** 강제하려 합니다.

### `Query`와 `Annotated` 임포트 { #import-query-and-annotated }

이를 위해 먼저 다음을 임포트합니다:

* `fastapi`에서 `Query`
* `typing`에서 `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info | 정보

FastAPI는 0.95.0 버전에서 `Annotated` 지원을 추가했고(그리고 이를 권장하기 시작했습니다).

이전 버전을 사용하면 `Annotated`를 사용하려고 할 때 오류가 발생합니다.

`Annotated`를 사용하기 전에 최소 0.95.1 버전으로 [FastAPI 버전 업그레이드](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}를 진행하세요.

///

## `q` 매개변수의 타입에 `Annotated` 사용하기 { #use-annotated-in-the-type-for-the-q-parameter }

이전에 [Python Types Intro](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank}에서 `Annotated`를 사용해 매개변수에 메타데이터를 추가할 수 있다고 말씀드린 것을 기억하시나요?

이제 FastAPI에서 사용할 차례입니다. 🚀

다음과 같은 타입 어노테이션이 있었습니다:

//// tab | Python 3.10+

```Python
q: str | None = None
```

////

//// tab | Python 3.9+

```Python
q: Union[str, None] = None
```

////

여기서 `Annotated`로 감싸서 다음과 같이 만듭니다:

//// tab | Python 3.10+

```Python
q: Annotated[str | None] = None
```

////

//// tab | Python 3.9+

```Python
q: Annotated[Union[str, None]] = None
```

////

두 버전 모두 같은 의미로, `q`는 `str` 또는 `None`이 될 수 있는 매개변수이며 기본값은 `None`입니다.

이제 재미있는 부분으로 넘어가 봅시다. 🎉

## `q` 매개변수의 `Annotated`에 `Query` 추가하기 { #add-query-to-annotated-in-the-q-parameter }

이제 이 `Annotated`에 더 많은 정보를 넣을 수 있으므로(이 경우에는 추가 검증), `Annotated` 안에 `Query`를 추가하고 `max_length` 매개변수를 `50`으로 설정합니다:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

기본값은 여전히 `None`이므로, 매개변수는 여전히 선택적입니다.

하지만 `Annotated` 안에 `Query(max_length=50)`를 넣음으로써, 이 값에 대해 **추가 검증**을 적용하고 최대 50자까지만 허용하도록 FastAPI에 알려줍니다. 😎

/// tip | 팁

여기서는 **쿼리 매개변수**이기 때문에 `Query()`를 사용합니다. 나중에 `Path()`, `Body()`, `Header()`, `Cookie()`와 같이 `Query()`와 동일한 인자를 받는 것들도 보게 될 것입니다.

///

이제 FastAPI는 다음을 수행합니다:

* 최대 길이가 50자인지 확인하도록 데이터를 **검증**합니다
* 데이터가 유효하지 않을 때 클라이언트에게 **명확한 오류**를 보여줍니다
* OpenAPI 스키마 *경로 처리*에 매개변수를 **문서화**합니다(따라서 **자동 문서 UI**에 표시됩니다)

## 대안(이전 방식): 기본값으로 `Query` 사용 { #alternative-old-query-as-the-default-value }

이전 FastAPI 버전(<abbr title="before 2023-03">0.95.0</abbr> 이전)에서는 `Annotated`에 넣는 대신, 매개변수의 기본값으로 `Query`를 사용해야 했습니다. 주변에서 이 방식을 사용하는 코드를 볼 가능성이 높기 때문에 설명해 드리겠습니다.

/// tip | 팁

새 코드를 작성할 때와 가능할 때는 위에서 설명한 대로 `Annotated`를 사용하세요. 여러 장점이 있고(아래에서 설명합니다) 단점은 없습니다. 🍰

///

다음은 함수 매개변수의 기본값으로 `Query()`를 사용하면서 `max_length`를 50으로 설정하는 방법입니다:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

이 경우(`Annotated`를 사용하지 않는 경우) 함수에서 기본값 `None`을 `Query()`로 바꿔야 하므로, 이제 `Query(default=None)`로 기본값을 설정해야 합니다. (최소한 FastAPI 입장에서는) 이 인자는 해당 기본값을 정의하는 것과 같은 목적을 수행합니다.

그러므로:

```Python
q: str | None = Query(default=None)
```

...위 코드는 기본값이 `None`인 선택적 매개변수를 만들며, 아래와 동일합니다:


```Python
q: str | None = None
```

하지만 `Query` 버전은 이것이 쿼리 매개변수임을 명시적으로 선언합니다.

그 다음, `Query`로 더 많은 매개변수를 전달할 수 있습니다. 지금의 경우 문자열에 적용되는 `max_length` 매개변수입니다:

```Python
q: str | None = Query(default=None, max_length=50)
```

이는 데이터를 검증할 것이고, 데이터가 유효하지 않다면 명백한 오류를 보여주며, OpenAPI 스키마 *경로 처리*에 매개변수를 문서화 합니다.

### 기본값으로 `Query` 사용 또는 `Annotated`에 넣기 { #query-as-the-default-value-or-in-annotated }

`Annotated` 안에서 `Query`를 사용할 때는 `Query`에 `default` 매개변수를 사용할 수 없다는 점을 기억하세요.

대신 함수 매개변수의 실제 기본값을 사용하세요. 그렇지 않으면 일관성이 깨집니다.

예를 들어, 다음은 허용되지 않습니다:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...왜냐하면 기본값이 `"rick"`인지 `"morty"`인지 명확하지 않기 때문입니다.

따라서 (가능하면) 다음과 같이 사용합니다:

```Python
q: Annotated[str, Query()] = "rick"
```

...또는 오래된 코드베이스에서는 다음과 같은 코드를 찾게 될 것입니다:

```Python
q: str = Query(default="rick")
```

### `Annotated`의 장점 { #advantages-of-annotated }

함수 매개변수의 기본값 방식 대신 **`Annotated`를 사용하는 것을 권장**합니다. 여러 이유로 **더 좋기** 때문입니다. 🤓

**함수 매개변수**의 **기본값**이 **실제 기본값**이 되므로, 전반적으로 Python에 더 직관적입니다. 😌

FastAPI 없이도 **다른 곳에서** 같은 함수를 **호출**할 수 있고, **예상대로 동작**합니다. **필수** 매개변수(기본값이 없는 경우)가 있다면 **편집기**가 오류로 알려줄 것이고, 필수 매개변수를 전달하지 않고 실행하면 **Python**도 오류를 냅니다.

`Annotated`를 사용하지 않고 **(이전) 기본값 스타일**을 사용하면, FastAPI 없이 **다른 곳에서** 함수를 호출할 때도 제대로 동작하도록 함수에 인자를 전달해야 한다는 것을 **기억**해야 합니다. 그렇지 않으면 값이 기대와 다르게 됩니다(예: `str` 대신 `QueryInfo` 같은 것). 그리고 편집기도 경고하지 않고 Python도 그 함수를 실행할 때는 불평하지 않으며, 오직 내부 동작에서 오류가 발생할 때만 문제가 드러납니다.

`Annotated`는 하나 이상의 메타데이터 어노테이션을 가질 수 있기 때문에, 이제 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a> 같은 다른 도구에서도 같은 함수를 사용할 수 있습니다. 🚀

## 검증 더 추가하기 { #add-more-validations }

`min_length` 매개변수도 추가할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## 정규식 추가 { #add-regular-expressions }

매개변수와 일치해야 하는 <abbr title="문자열에 대한 검색 패턴을 정의하는 문자들의 순열인 정규 표현식(regular expression), regex 또는 regexp입니다.">정규 표현식</abbr> `pattern`을 정의할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

이 특정 정규표현식 패턴은 전달 받은 매개변수 값이 다음을 만족하는지 검사합니다:

* `^`: 뒤따르는 문자로 시작하며, 앞에는 문자가 없습니다.
* `fixedquery`: 정확히 `fixedquery` 값을 가집니다.
* `$`: 여기서 끝나며, `fixedquery` 이후로 더 이상 문자가 없습니다.

**"정규 표현식"** 개념에 대해 상실감을 느꼈다면 걱정하지 않아도 됩니다. 많은 사람에게 어려운 주제입니다. 아직은 정규 표현식 없이도 많은 작업들을 할 수 있습니다.

이제 필요할 때 언제든지 **FastAPI**에서 직접 사용할 수 있다는 사실을 알게 되었습니다.

## 기본값 { #default-values }

물론 `None`이 아닌 다른 기본값을 사용할 수도 있습니다.

`q` 쿼리 매개변수에 `min_length`를 `3`으로 설정하고, 기본값을 `"fixedquery"`로 선언하고 싶다고 해봅시다:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py39.py hl[9] *}

/// note | 참고

`None`을 포함해 어떤 타입이든 기본값을 가지면 매개변수는 선택적(필수 아님)이 됩니다.

///

## 필수 매개변수 { #required-parameters }

더 많은 검증이나 메타데이터를 선언할 필요가 없는 경우, 다음과 같이 기본값을 선언하지 않고 쿼리 매개변수 `q`를 필수로 만들 수 있습니다:

```Python
q: str
```

아래 대신:

```Python
q: str | None = None
```

하지만 이제는 예를 들어 다음과 같이 `Query`로 선언합니다:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

따라서 `Query`를 사용하면서 값을 필수로 선언해야 할 때는, 기본값을 선언하지 않으면 됩니다:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py39.py hl[9] *}

### 필수지만 `None` 가능 { #required-can-be-none }

매개변수가 `None`을 허용하지만 여전히 필수라고 선언할 수 있습니다. 이렇게 하면 값이 `None`이더라도 클라이언트는 값을 반드시 전송해야 합니다.

이를 위해 `None`이 유효한 타입이라고 선언하되, 기본값은 선언하지 않으면 됩니다:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## 쿼리 매개변수 리스트 / 다중값 { #query-parameter-list-multiple-values }

`Query`로 쿼리 매개변수를 명시적으로 정의할 때 값들의 리스트를 받도록 선언할 수도 있고, 다른 말로 하면 여러 값을 받도록 선언할 수도 있습니다.

예를 들어, URL에서 여러 번 나타날 수 있는 `q` 쿼리 매개변수를 선언하려면 다음과 같이 작성할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

그 다음, 아래와 같은 URL로:

```
http://localhost:8000/items/?q=foo&q=bar
```

여러 `q` *쿼리 매개변수* 값들(`foo` 및 `bar`)을 파이썬 `list`로 *경로 처리 함수*의 *함수 매개변수* `q`에서 받게 됩니다.

따라서 해당 URL에 대한 응답은 다음과 같습니다:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | 팁

위의 예와 같이 `list` 타입으로 쿼리 매개변수를 선언하려면 `Query`를 명시적으로 사용해야 합니다. 그렇지 않으면 요청 본문으로 해석됩니다.

///

대화형 API 문서는 여러 값을 허용하도록 수정 됩니다:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 쿼리 매개변수 리스트 / 기본값이 있는 다중값 { #query-parameter-list-multiple-values-with-defaults }

제공된 값이 없으면 기본 `list` 값을 정의할 수도 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py39.py hl[9] *}

다음으로 이동하면:

```
http://localhost:8000/items/
```

`q`의 기본값은 `["foo", "bar"]`가 되고, 응답은 다음이 됩니다:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### `list`만 사용하기 { #using-just-list }

`list[str]` 대신 `list`를 직접 사용할 수도 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py39.py hl[9] *}

/// note | 참고

이 경우 FastAPI는 리스트의 내용을 검사하지 않음을 명심하세요.

예를 들어, `list[int]`는 리스트 내용이 정수인지 검사(및 문서화)합니다. 하지만 `list` 단독일 경우는 아닙니다.

///

## 더 많은 메타데이터 선언 { #declare-more-metadata }

매개변수에 대한 정보를 추가할 수 있습니다.

해당 정보는 생성된 OpenAPI에 포함되고 문서 사용자 인터페이스 및 외부 도구에서 사용됩니다.

/// note | 참고

도구에 따라 OpenAPI 지원 수준이 다를 수 있음을 명심하세요.

일부는 아직 선언된 추가 정보를 모두 표시하지 않을 수 있지만, 대부분의 경우 누락된 기능은 이미 개발 계획이 있습니다.

///

`title`을 추가할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

그리고 `description`도 추가할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## 별칭 매개변수 { #alias-parameters }

매개변수가 `item-query`이길 원한다고 가정해 봅시다.

마치 다음과 같습니다:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

그러나 `item-query`는 유효한 파이썬 변수 이름이 아닙니다.

가장 가까운 것은 `item_query`일 겁니다.

하지만 정확히 `item-query`이길 원합니다...

이럴 경우 `alias`를 선언할 수 있으며, 해당 별칭은 매개변수 값을 찾는 데 사용됩니다:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## 매개변수 사용 중단하기 { #deprecating-parameters }

이제는 더 이상 이 매개변수를 마음에 들어하지 않는다고 가정해 봅시다.

이 매개변수를 사용하는 클라이언트가 있기 때문에 한동안은 남겨둬야 하지만, 문서에서 <abbr title="obsolete, recommended not to use it – 구식이며, 사용하지 않는 것을 추천">deprecated</abbr>로 명확하게 보여주고 싶습니다.

그렇다면 `deprecated=True` 매개변수를 `Query`로 전달합니다:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

문서가 아래와 같이 보일겁니다:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## OpenAPI에서 매개변수 제외 { #exclude-parameters-from-openapi }

생성된 OpenAPI 스키마(따라서 자동 문서화 시스템)에서 쿼리 매개변수를 제외하려면 `Query`의 `include_in_schema` 매개변수를 `False`로 설정하세요:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## 커스텀 검증 { #custom-validation }

위에 나온 매개변수들로는 할 수 없는 **커스텀 검증**이 필요한 경우가 있을 수 있습니다.

그런 경우에는 일반적인 검증(예: 값이 `str`인지 검증한 뒤) 이후에 적용되는 **커스텀 검증 함수**를 사용할 수 있습니다.

`Annotated` 안에서 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">Pydantic의 `AfterValidator`</a>를 사용하면 이를 구현할 수 있습니다.

/// tip | 팁

Pydantic에는 <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a>와 같은 다른 것들도 있습니다. 🤓

///

예를 들어, 이 커스텀 validator는 <abbr title="ISBN means International Standard Book Number – 국제 표준 도서 번호">ISBN</abbr> 도서 번호의 경우 아이템 ID가 `isbn-`으로 시작하고, <abbr title="IMDB (Internet Movie Database) is a website with information about movies – 영화에 대한 정보를 제공하는 웹사이트">IMDB</abbr> 영화 URL ID의 경우 `imdb-`로 시작하는지 확인합니다:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info | 정보

이는 Pydantic 2 이상 버전에서 사용할 수 있습니다. 😎

///

/// tip | 팁

데이터베이스나 다른 API 같은 **외부 구성요소**와 통신이 필요한 어떤 종류의 검증이든 해야 한다면, 대신 **FastAPI Dependencies**를 사용해야 합니다. 이에 대해서는 나중에 배우게 됩니다.

이 커스텀 validator는 요청에서 제공된 **같은 데이터만**으로 확인할 수 있는 것들을 위한 것입니다.

///

### 코드 이해하기 { #understand-that-code }

중요한 부분은 **`Annotated` 안에서 함수와 함께 `AfterValidator`를 사용한다는 것**뿐입니다. 이 부분은 건너뛰셔도 됩니다. 🤸

---

하지만 이 특정 코드 예제가 궁금하고 계속 보고 싶다면, 추가 세부사항은 다음과 같습니다.

#### `value.startswith()`를 사용한 문자열 { #string-with-value-startswith }

알고 계셨나요? `value.startswith()`를 사용하는 문자열은 튜플을 받을 수 있으며, 튜플에 있는 각 값을 확인합니다:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### 임의의 항목 { #a-random-item }

`data.items()`를 사용하면 각 딕셔너리 항목의 키와 값을 담은 튜플로 구성된 <abbr title="리스트, 세트 등처럼 for 루프로 순회할 수 있는 것">iterable object</abbr>를 얻습니다.

이 iterable object를 `list(data.items())`로 적절한 `list`로 변환합니다.

그 다음 `random.choice()`로 리스트에서 **무작위 값**을 얻어 `(id, name)` 형태의 튜플을 얻습니다. 예를 들어 `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")` 같은 값이 될 것입니다.

그 다음 이 튜플의 **두 값을** 변수 `id`와 `name`에 **할당**합니다.

따라서 사용자가 아이템 ID를 제공하지 않더라도, 무작위 추천을 받게 됩니다.

...이 모든 것을 **단 하나의 간단한 줄**로 합니다. 🤯 Python 정말 좋지 않나요? 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## 요약 { #recap }

매개변수에 검증과 메타데이터를 추가 선언할 수 있습니다.

제네릭 검증과 메타데이터:

* `alias`
* `title`
* `description`
* `deprecated`

문자열에 특화된 검증:

* `min_length`
* `max_length`
* `pattern`

`AfterValidator`를 사용하는 커스텀 검증.

예제에서 `str` 값의 검증을 어떻게 추가하는지 살펴보았습니다.

숫자와 같은 다른 타입에 대한 검증을 어떻게 선언하는지 확인하려면 다음 장을 확인하기 바랍니다.
