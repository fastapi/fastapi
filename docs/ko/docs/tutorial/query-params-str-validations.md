# 쿼리 매개변수와 문자열 검증

**FastAPI**를 사용하면 매개변수에 대한 추가 정보 및 검증을 선언할 수 있습니다.

이 응용 프로그램을 예로 들어보겠습니다:

{* ../../docs_src/query_params_str_validations/tutorial001.py hl[9] *}

쿼리 매개변수 `q`는 `Optional[str]` 자료형입니다. 즉, `str` 자료형이지만 `None` 역시 될 수 있음을 뜻하고, 실제로 기본값은 `None`이기 때문에 FastAPI는 이 매개변수가 필수가 아니라는 것을 압니다.

/// note | 참고

FastAPI는 `q`의 기본값이 `= None`이기 때문에 필수가 아님을 압니다.

`Optional[str]`에 있는 `Optional`은 FastAPI가 사용하는게 아니지만, 편집기에게 더 나은 지원과 오류 탐지를 제공하게 해줍니다.

///

## 추가 검증

`q`가 선택적이지만 값이 주어질 때마다 **값이 50 글자를 초과하지 않게** 강제하려 합니다.

### `Query` 임포트

이를 위해 먼저 `fastapi`에서 `Query`를 임포트합니다:

{* ../../docs_src/query_params_str_validations/tutorial002.py hl[3] *}

## 기본값으로 `Query` 사용

이제 `Query`를 매개변수의 기본값으로 사용하여 `max_length` 매개변수를 50으로 설정합니다:

{* ../../docs_src/query_params_str_validations/tutorial002.py hl[9] *}

기본값 `None`을 `Query(None)`으로 바꿔야 하므로, `Query`의 첫 번째 매개변수는 기본값을 정의하는 것과 같은 목적으로 사용됩니다.

그러므로:

```Python
q: Optional[str] = Query(None)
```

...위 코드는 아래와 동일하게 매개변수를 선택적으로 만듭니다:

```Python
q: Optional[str] = None
```

하지만 명시적으로 쿼리 매개변수를 선언합니다.

/// info | 정보

FastAPI는 다음 부분에 관심이 있습니다:

```Python
= None
```

또는:

```Python
= Query(None)
```

그리고 `None`을 사용하여 쿼라 매개변수가 필수적이지 않다는 것을 파악합니다.

`Optional` 부분은 편집기에게 더 나은 지원을 제공하기 위해서만 사용됩니다.

///

또한 `Query`로 더 많은 매개변수를 전달할 수 있습니다. 지금의 경우 문자열에 적용되는 `max_length` 매개변수입니다:

```Python
q: str = Query(None, max_length=50)
```

이는 데이터를 검증할 것이고, 데이터가 유효하지 않다면 명백한 오류를 보여주며, OpenAPI 스키마 *경로 작동*에 매개변수를 문서화 합니다.

## 검증 추가

매개변수 `min_length` 또한 추가할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial003.py hl[9] *}

## 정규식 추가

매개변수와 일치해야 하는 <abbr title="정규표현식(regular expression), regex 또는 regexp는 문자열 조회 패턴을 정의하는 문자들의 순열입니다">정규표현식</abbr>을 정의할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial004.py hl[10] *}

이 특정 정규표현식은 전달 받은 매개변수 값을 검사합니다:

* `^`: 이전에 문자가 없고 뒤따르는 문자로 시작합니다.
* `fixedquery`: 정확히 `fixedquery` 값을 갖습니다.
* `$`: 여기서 끝나고 `fixedquery` 이후로 아무 문자도 갖지 않습니다.

**"정규표현식"** 개념에 대해 상실감을 느꼈다면 걱정하지 않아도 됩니다. 많은 사람에게 어려운 주제입니다. 아직은 정규표현식 없이도 많은 작업들을 할 수 있습니다.

하지만 언제든지 가서 배울수 있고, **FastAPI**에서 직접 사용할 수 있다는 사실을 알고 있어야 합니다.

## 기본값

기본값으로 사용하는 첫 번째 인자로 `None`을 전달하듯이, 다른 값을 전달할 수 있습니다.

`min_length`가 `3`이고, 기본값이 `"fixedquery"`인 쿼리 매개변수 `q`를 선언해봅시다:

{* ../../docs_src/query_params_str_validations/tutorial005.py hl[7] *}

/// note | 참고

기본값을 갖는 것만으로 매개변수는 선택적이 됩니다.

///

## 필수로 만들기

더 많은 검증이나 메타데이터를 선언할 필요가 없는 경우, 다음과 같이 기본값을 선언하지 않고 쿼리 매개변수 `q`를 필수로 만들 수 있습니다:

```Python
q: str
```

아래 대신:

```Python
q: Optional[str] = None
```

그러나 이제 다음과 같이 `Query`로 선언합니다:

```Python
q: Optional[str] = Query(None, min_length=3)
```

그래서 `Query`를 필수값으로 만들어야 할 때면, 첫 번째 인자로 `...`를 사용할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial006.py hl[7] *}

/// info | 정보

이전에 `...`를 본적이 없다면: 특별한 단일값으로, <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">파이썬의 일부이며 "Ellipsis"라 부릅니다</a>.

///

이렇게 하면 **FastAPI**가 이 매개변수는 필수임을 알 수 있습니다.

## 쿼리 매개변수 리스트 / 다중값

쿼리 매개변수를 `Query`와 함께 명시적으로 선언할 때, 값들의 리스트나 다른 방법으로 여러 값을 받도록 선언 할 수도 있습니다.

예를 들어, URL에서 여러번 나오는  `q` 쿼리 매개변수를 선언하려면 다음과 같이 작성할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial011.py hl[9] *}

아래와 같은 URL을 사용합니다:

```
http://localhost:8000/items/?q=foo&q=bar
```

여러 `q` *쿼리 매개변수* 값들을 (`foo` 및 `bar`) 파이썬 `list`로 *경로 작동 함수* 내 *함수 매개변수* `q`로 전달 받습니다.

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

위의 예와 같이 `list` 자료형으로 쿼리 매개변수를 선언하려면 `Query`를 명시적으로 사용해야 합니다. 그렇지 않으면 요청 본문으로 해석됩니다.

///

대화형 API 문서는 여러 값을 허용하도록 수정 됩니다:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 쿼리 매개변수 리스트 / 기본값을 사용하는 다중값

그리고 제공된 값이 없으면 기본 `list` 값을 정의할 수도 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial012.py hl[9] *}

아래로 이동한다면:

```
http://localhost:8000/items/
```

`q`의 기본값은: `["foo", "bar"]`이며 응답은 다음이 됩니다:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### `list` 사용하기

`List[str]` 대신 `list`를 직접 사용할 수도 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial013.py hl[7] *}

/// note | 참고

이 경우 FastAPI는 리스트의 내용을 검사하지 않음을 명심하기 바랍니다.

예를 들어, `List[int]`는 리스트 내용이 정수인지 검사(및 문서화)합니다. 하지만 `list` 단독일 경우는 아닙니다.

///

## 더 많은 메타데이터 선언

매개변수에 대한 정보를 추가할 수 있습니다.

해당 정보는 생성된 OpenAPI에 포함되고 문서 사용자 인터페이스 및 외부 도구에서 사용됩니다.

/// note | 참고

도구에 따라 OpenAPI 지원 수준이 다를 수 있음을 명심하기 바랍니다.

일부는 아직 선언된 추가 정보를 모두 표시하지 않을 수 있지만, 대부분의 경우 누락된 기능은 이미 개발 계획이 있습니다.

///

`title`을 추가할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial007.py hl[10] *}

그리고 `description`도 추가할 수 있습니다:

{* ../../docs_src/query_params_str_validations/tutorial008.py hl[13] *}

## 별칭 매개변수

매개변수가 `item-query`이길 원한다고 가정해 봅시다.

마치 다음과 같습니다:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

그러나 `item-query`은 유효한 파이썬 변수 이름이 아닙니다.

가장 가까운 것은 `item_query`일 겁니다.

하지만 정확히`item-query`이길 원합니다...

이럴 경우 `alias`를 선언할 수 있으며, 해당 별칭은 매개변수 값을 찾는 데 사용됩니다:

{* ../../docs_src/query_params_str_validations/tutorial009.py hl[9] *}

## 매개변수 사용하지 않게 하기

이제는 더이상 이 매개변수를 마음에 들어하지 않는다고 가정해 봅시다.

이 매개변수를 사용하는 클라이언트가 있기 때문에 한동안은 남겨둬야 하지만, <abbr title="구식이며, 사용하지 않는 것을 추천">사용되지 않는다(deprecated)</abbr>고 확실하게 문서에서 보여주고 싶습니다.

그렇다면 `deprecated=True` 매개변수를 `Query`로 전달합니다:

{* ../../docs_src/query_params_str_validations/tutorial010.py hl[18] *}

문서가 아래와 같이 보일겁니다:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## 요약

매개변수에 검증과 메타데이터를 추가 선언할 수 있습니다.

제네릭 검증과 메타데이터:

* `alias`
* `title`
* `description`
* `deprecated`

특정 문자열 검증:

* `min_length`
* `max_length`
* `regex`

예제에서 `str` 값의 검증을 어떻게 추가하는지 살펴보았습니다.

숫자와 같은 다른 자료형에 대한 검증을 어떻게 선언하는지 확인하려면 다음 장을 확인하기 바랍니다.
