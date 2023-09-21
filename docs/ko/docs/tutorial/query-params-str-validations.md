# 쿼리 매개변수 및 문자열 유효성 검사

**FastAPI**를 사용하면 매개변수에 대한 추가 정보와 유효성 검사를 선언할 수 있습니다.

예를 들어 보겠습니다:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial001.py!}
    ```

쿼리 매개변수 `q`는 `Union[str, None]` 유형 (Python 3.10에서는 `str | None`)입니다.
이것은 `str` 유형이지만 `None`이 될 수 있다는 것을 의미하며, 실제로 기본값은 `None`이므로
FastAPI 는 이것이 필수적이지 않다는 것을 알게됩니다.

!!! note
    기본값 `= None` 때문에 FastAPI는 `q`의 값이 필수적이지 않다는 것을 알게 됩니다.

    `Union`에서 `Union[str, None]`을 사용하면 편집기가 더 나은 지원과 오류 감지를 제공할 수 있습니다.

## 추가 유효성 검사

`q`가 선택 사항이지만 제공되는 경우 **길이가 50자를 초과하지 않도록** 강제하려고 합니다.

### `Query` 및 `Annotated` 가져오기

먼저 다음을 가져오세요.

* `fastapi`에서 `Query`
* `typing`에서 `Annotated` (Python 3.9 미만 : `typing_extensions`에서)

=== "Python 3.10+"

    Python 3.9 이상에서 `Annotated`가 표준 라이브러리이므로 `typing`에서 가져올 수 있습니다.

    ```Python hl_lines="1  3"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.6+"

    Python 3.9 미만에서는 `typing_extensions`에서 `Annotated`를 가져옵니다.

    FastAPI와 함께 이미 설치되어 있습니다.

    ```Python hl_lines="3-4"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

!!! info
    FastAPI 버전 0.95.0에서 `Annotated`를 지원에 추가하고 권장하기 시작했습니다.

    이전 버전을 사용하면 `Annotated`을 사용하려고 할 때 오류가 발생합니다.

    `Annotated`를 사용하기 전에 [FastAPI 버전을 업그레이드](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}하여 최소한 0.95.1로 업그레이드하세요.

## `q` 매개변수의 유형에 `Annotated` 사용하기

[Python Types Intro](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank}에서 `Annotated`를 사용하여 매개변수에 메타데이터를 추가할 수 있다고 했습니다.

이제 FastAPI 와 함께 사용해봅시다. 🚀

다음과 같은 type annotation 있습니다:

=== "Python 3.10+"

    ```Python
    q: str | None = None
    ```

=== "Python 3.6+"

    ```Python
    q: Union[str, None] = None
    ```

할 일은 `Annotated`로 묶으세요. 그러면 아래와 같이 됩니다:

=== "Python 3.10+"

    ```Python
    q: Annotated[str | None] = None
    ```

=== "Python 3.6+"

    ```Python
    q: Annotated[Union[str, None]] = None
    ```

이러한 두 버전은 같은 의미를 가집니다. `q`는 `str` 또는 `None`일 수 있는 매개변수이며 기본값은 `None`입니다.

이제 재미있는 부분으로 넘어갑니다. 🎉

## `Annotated`에서 `q` 매개변수로 `Query` 추가하기

이제 `Annotated`에 더 많은 메타데이터를 넣을 수 있고 `Query`를 추가하고 매개변수 `max_length`를 50으로 설정합니다.

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_an.py!}
    ```

기본값은 여전히 `None`이므로 매개변수는 여전히 선택사항 입니다.

그러나 이제 `Annotated` 내부에 `Query(max_length=50)`을 넣으면,
FastAPI 에게 쿼리 매개변수에서 이 값에 대한 **추가 유효성 검사**가 필요하다고 알려줄 수 있습니다
(추가 유효성 검사를 수행하기 위해 이렇게 하는 겁니다). 😎

FastAPI 는 이제 다음을 수행합니다.

* 최대 길이가 50자인지 확인하여 데이터 **유효성 검사**를 합니다.
* 데이터가 유효하지 않은 경우 클라이언트에게 **명확한 오류**를 표시합니다.
* OpenAPI 스키마 경로 작업에서 매개변수를 **문서화**합니다. (자동 문서 UI에 표시되도록)

## (예전방식) 'Query' 를 기본값으로 사용하기

FastAPI 의 이전 버전 (<abbr title="before 2023-03">0.95.0</abbr> 이전)에서는 매개변수의 기본값으로 'Query'를 사용해야 했습니다.

'Annotated' 방식이 아닌, 예전 코드를 많이 볼 수 있으므로 설명해 드리겠습니다.

!!! tip
    가능한 경우 앞에서 설명한 대로 'Annotated'를 사용하세요.
    여러 가지 이점이 있고 단점은 없습니다. 🍰

다음은 함수 매개변수의 기본 값으로 'Query()'를 사용하는 방법입니다.
매개변수 'max_length'를 50으로 설정합니다:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial002.py!}
    ```

이 경우 (Annotated를 사용하지 않고) 기본값 `None`을 함수에서 'Query()'로 바꿔야 하므로 기본값을 'Query(default=None)' 매개변수로 설정해야 합니다.
이렇게 하면 기본값을 정의하는 데 사용됩니다 (최소한 FastAPI 에서는).

따라서:

```Python
q: Union[str, None] = Query(default=None)
```

...매개변수를 선택 사항으로 만들고 기본값을 `None`으로 만듭니다. 다음과 동일합니다.

```Python
q: Union[str, None] = None
```

Python 3.10 이상에서는:

```Python
q: str | None = Query(default=None)
```

...매개변수를 선택 사항으로 만들고 기본값을 `None`으로 만듭니다. 다음과 동일합니다.

```Python
q: str | None = None
```

그러나 이것은 명시적으로 매개변수를 쿼리 매개변수로 선언하는 방법임을 나타냅니다.

!!! info
    매개변수를 선택 사항으로 만들기 위한 가장 중요한 부분은 다음 부분입니다.

    ```Python
    = None
    ```

    또는:

    ```Python
    = Query(default=None)
    ```

    `None`을 기본값으로 사용하므로 매개변수를 **필수로** 만들지 않는 것입니다.

    'Union[str, None]' 부분은 편집기가 더 나은 지원을 제공하도록 하는 데 사용되지만
    FastAPI 에게 이 매개변수가 필수가 아님을 알리는 것은 아닙니다.

그런 다음 'Query'에 더 많은 매개변수를 전달할 수 있습니다.
문자열에 적용되는 'max_length' 매개변수를 사용해봅시다:

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

이렇게 하면 데이터를 유효성 검사하고 데이터가 유효하지 않을 때 명확한 오류를 표시하며
OpenAPI 스키마 *경로 작업*에 매개변수를 문서화합니다.

### 기본값 또는 `Annotated` 안에 `Query`

`Annotated` 내에서 `Query`를 사용할 때 `Query`의 `default` 매개변수를 사용할 수 없다는 점에 유의하세요.

대신 함수 매개변수의 실제 기본값을 사용하십세요. 그렇지 않으면 일관성이 떨어집니다.

예를 들어, 다음은 허용되지 않습니다:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

... 왜냐하면 기본값이 `"rick"` 또는 `"morty"` 여야 하는지 명확하지 않기 때문입니다.

따라서 (가능한 경우) 다음을 사용해야 합니다:

```Python
q: Annotated[str, Query()] = "rick"
```

... 또는 오래된 코드 베이스라면:

```Python
q: str = Query(default="rick")
```

### 'Annotated' 의 장점

**함수 매개변수의 기본값 대신에 'Annotated'를 사용하는 것이 권장됩니다**. 이것은 여러 가지 이유로 **더 좋습니다**. 🤓

**함수 매개변수의 기본값**은 **실제 기본값**이며, 일반적으로 Python 에 더 직관적입니다. 😌

이 같은 함수를 **다른 위치**에서 FastAPI를 사용하지 않고 **호출**할 수 있으며, 예상대로 작동합니다.
**기본값이 없는 필수** 매개변수가 있으면 **편집기**에서 오류로 알려줄 것이며, 필수 매개변수를 전달하지 않고 실행하면 **Python**에서도 오류가 발생합니다.

'Annotated'를 사용하지 않고 **(옛 스타일) 기본값 스타일**을 사용하면, FastAPI 를 사용하지 않고 함수를 호출할 때 값이 예상과 다를 수 있습니다
(예: `str` 대신 `QueryInfo` 또는 유사한 값).
그리고 편집기나 Python 은 함수를 실행할 때가 아니면 오류를 바로 표시하지 않을 가능성이 있습니다.

'Annotated' 를 쓰면 여러 메타데이터 주석을 포함할 수 있기 때문에
이제는 <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>와 같은 도구에서도 함수를 사용할 수 있게 됩니다. 🚀

## 다양한 유효성 검사 추가하기

매개변수 `min_length`를 추가할 수 있습니다:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

!!! tip
    가능한 경우 'Annotated' 버전을 사용하세요.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial003_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

!!! tip
    가능한 경우 'Annotated' 버전을 사용하세요.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial003.py!}
    ```

## 정규식 추가하기

매개변수가 일치해야 하는 <abbr title="정규식은 문자열 검색 패턴을 정의하는 문자 시퀀스입니다.">정규식</abbr> `pattern`을 정의할 수 있습니다:

=== "Python 3.10+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004.py!}
    ```

정규식 패턴은 다음과 같이 매개변수 값을 검사합니다:

* `^`: 다음 문자열로 시작하며, 앞에 문자가 없습니다.
* `fixedquery`: 정확한 문자 `fixedquery`를 가집니다.
* `$`: 여기서 끝나며, `fixedquery` 이후에 다른 문자가 없습니다.

이러한 **"정규식"** 로 인해 혼란스럽다면 걱정하지 마세요.
이것은 많은 사람들에게 어려운 주제입니다.
정규식을 사용하지 않고도 많은 것을 할 수 있습니다.

하지만 정규식을 학습한 뒤에, **FastAPI**에서 적용할 수 있다는 것을 기억하세요.

### `pattern` 대신 Pydantic v1 `regex` 사용하기

Pydantic 2 이전 및 FastAPI 0.100.0 이전에는 매개변수를 `pattern` 대신 `regex`로 호출했지만 이제는 폐기되었습니다.

아직 일부 코드에서 `regex`를 사용하는 것을 볼 수 있습니다:

=== "Python 3.10+ Pydantic v1"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial004_an_py310_regex.py!}
    ```

하지만 이것은 폐기되었으며 새 매개변수 `pattern`을 사용하도록 업데이트해야 합니다. 🤓

## 기본값

물론 `None` 이외의 기본값을 사용할 수 있습니다.

예를 들어 `q` 쿼리 매개변수를 `min_length`가 `3`이고
기본값이 `"fixedquery"`인 것으로 선언하려면 다음과 같이 할 수 있습니다:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial005_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial005.py!}
    ```

!!! note
    어떤 유형의 기본값이든 (None 포함) 매개변수를 선택사항(optional)으로 만듭니다.

## 필수로 만들기

추가적인 유효성 검사나 메타데이터를 선언할 필요가 없을 때는 `q` 쿼리 매개변수를 기본값을 선언하지 않고 필수로 만들 수 있습니다.

다음과 같이:

```Python
q: str
```

대신에:

```Python
q: Union[str, None] = None
```

하지만 이제 우리는 다음과 같이 `Query`로 선언합니다.

=== "Annotated"

    ```Python
    q: Annotated[Union[str, None], Query(min_length=3)] = None
    ```

=== "non-Annotated"

    ```Python
    q: Union[str, None] = Query(default=None, min_length=3)
    ```

따라서 `Query`를 사용하면서 값을 필수로 선언해야 하는 경우 기본값을 선언하지 않으면 됩니다.

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006.py!}
    ```

    !!! tip
        이 경우 `Query()`가 함수 매개변수 기본값으로 사용되더라도 `Query()`에 `default=None`를 전달하지 않는다는 것에 유의하세요.

        가능하면 'Annotated' 버전을 사용하는 것이 더 나을 것입니다. 😉

### Ellipsis (`...`) 로 필수지정

값이 필수임을 명시적으로 선언하는 다른 방법이 있습니다.
기본값을 리터럴 값 `...` 으로 설정할 수 있습니다:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006b.py!}
    ```

!!! info
    이전에 '...' 을 보지 못했다면: 이것은 특별한 단일 값으로, <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">Python 의 일부이며 "Ellipsis"라고 합니다.</a>

    Pydantic 과 FastAPI 에서 값을 명시적으로 필수로 선언하기 위해 사용됩니다.

이렇게 하면 **FastAPI** 는 이 매개변수가 필수임을 알게 됩니다.

## `None`을 쓰면서 필수선언하기

매개변수가 `None`을 허용할 수 있지만 여전히 필수로 선언할 수 있습니다.
이렇게 하면 클라이언트가 값이 `None`이더라도 값을 보내도록 강제합니다.

이를 위해 `None`이 유효한 유형임을 선언하고 기본값으로 `...`을 사용할 수 있습니다.

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006c.py!}
    ```

!!! tip
    FastAPI 의 데이터 유효성 검사 및 직렬화를 담당하는 Pydantic은 기본값 없이 `Optional` 또는 `Union[Something, None]`을 사용할 때 특별한 동작을 합니다.
    이에 대한 자세한 내용은 Pydantic 문서의 <a href="https://pydantic-docs.helpmanual.io/usage/models/#required-optional-fields" class="external-link" target="_blank">필수 옵션 필드</a>에서 확인할 수 있습니다.

### `...` 대신 Pydantic의 `Required` 사용

`...` 사용에 불편함을 느낄 경우 Pydantic에서 `Required`를 가져와 사용할 수도 있습니다.

=== "Python 3.9+"

    ```Python hl_lines="4  10"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="2  9"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="2  8"
    {!> ../../../docs_src/query_params_str_validations/tutorial006d.py!}
    ```

!!! tip
    대부분의 경우 필수항목이라면 기본값을 생략하므로 `...` 또는 `Required`를 사용할 필요가 없습니다.

## 쿼리 매개변수 목록 / 다중 값

`Query`를 사용하여 명시적으로 쿼리 매개변수를 정의할 때 해당 매개변수가 여러 값을 수신하도록 선언할 수도 있습니다.
즉, 여러 값을 수신하도록 선언할 수도 있습니다.

예를 들어 URL 에 여러 번 나타날 수 있는 `q` 쿼리 매개변수를 선언하려면 다음과 같이 작성합니다.

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py310.py!}
    ```

=== "Python 3.9+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011_py39.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능한 경우 'Annotated' 버전을 사용하십시오.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial011.py!}
    ```

그런 다음 다음과 같은 URL 로 요청을 보내면:

```
http://localhost:8000/items/?q=foo&q=bar
```

*쿼리 매개변수* `q`의 값(`foo` 및 `bar`)을 Python `list` 로 수신하게 됩니다.

따라서 해당 URL 의 응답은 다음과 같습니다:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

!!! tip
    위의 예제와 같이 type `list` 인 쿼리 매개변수를 선언하려면 명시적으로 `Query`를 사용해야 합니다.
    그렇지 않으면 요청 본문으로 해석될 것입니다.

자동으로 API 문서는 다중 값을 허용하도록 업데이트되어 다음과 같이 표시됩니다:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### 기본값이 있는 쿼리 매개변수 list / 다중 값

또한 기본 `list` 값을 정의할 수 있습니다:

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_an.py!}
    ```

=== "Python 3.9+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial012_py39.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial012.py!}
    ```

다음으로 이동하면:

```
http://localhost:8000/items/
```

`q`의 기본값은 `["foo", "bar"]`가 되며 응답은 다음과 같습니다:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### `list` 사용

`List[str]` 대신 (또는 Python 3.9+에서 `list[str]` 대신) `list`를 직접 사용할 수도 있습니다.

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial013_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial013.py!}
    ```

!!! note
    이 경우 FastAPI 는 `list` 의 내용을 확인하지 않습니다.

    예를 들어 `List[int]`는 목록의 내용이 정수인지 확인할 것입니다.
    그러나 `list`만 사용하는 경우 `list` 의 내용을 확인하지 않습니다.

## 추가 메타데이터 선언

파라미터에 대한 더 많은 정보를 추가할 수 있습니다.

이 정보는 생성된 OpenAPI 에 포함되며 UI문서 및 외부 도구에서 사용됩니다.

!!! note
    서로 다른 도구들은 다양한 수준의 OpenAPI 지원을 가질 수 있습니다.

    일부 도구는 아직 선언된 모든 추가 정보를 표시하지 않을 수 있으며, 대부분의 경우 누락된 기능은 이미 개발이 계획되어 있습니다.

`title`을 추가할 수 있습니다:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial007_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial007.py!}
    ```

그리고 `description`을 추가할 수 있습니다:

=== "Python 3.10+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="14"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="15"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="12"
    {!> ../../../docs_src/query_params_str_validations/tutorial008_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="13"
    {!> ../../../docs_src/query_params_str_validations/tutorial008.py!}
    ```

## 별칭 매개변수

매개변수를 `item-query`로 지정하려고 상상해보십시오.

다음과 같이:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

그러나 `item-query`는 관습적인 Python 변수 이름이 아닙니다.

관습적인 변수이름은 `item_query`일 것입니다.

그러나 여전히 `item-query` 로 작동합니다.

이런 경우 `alias`를 선언할 수 있으며, 이 별칭이 매개변수 값을 찾는 데 사용됩니다:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params_str_validations/tutorial009_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params_str_validations/tutorial009.py!}
    ```

## 매개변수 폐기

이제 이 매개변수를 더 이상 사용하지 않는다고 가정해 봅시다.

클라이언트가 여전히 사용 중이기 때문에 한동안 그대로 두어야 합니다.
문서에서는 이를 명확하게 <abbr title="사용하지 않는 것이 권장됨">폐기(deprecated)</abbr>로 표시하고 싶습니다.

그런 경우 `Query` 에 매개변수 `deprecated=True` 를 전달하세요:

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="20"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="17"
    {!> ../../../docs_src/query_params_str_validations/tutorial010_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="18"
    {!> ../../../docs_src/query_params_str_validations/tutorial010.py!}
    ```

문서에서는 다음과 같이 표시됩니다:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## OpenAPI 에서 제외하기

생성된 OpenAPI 스키마(자동 문서화 시스템에서도)에서 쿼리 매개변수를 제외하려면 `Query`의 매개변수 `include_in_schema`를 `False`로 설정하세요:

=== "Python 3.10+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params_str_validations/tutorial014_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        가능하면 `Annotated` 버전을 사용하는 것이 좋습니다.

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params_str_validations/tutorial014.py!}
    ```

## 요약

매개변수에 대한 추가적인 유효성 검증과 메타데이터를 선언할 수 있습니다.

일반적인 검증 및 메타데이터:

* `alias`
* `title`
* `description`
* `deprecated`

문자열에 대한 검증:

* `min_length`
* `max_length`
* `pattern`

이 예에서는 `str` 값에 대한 검증을 선언하는 방법을 보았습니다.

숫자와 같은 다른 유형에 대한 검증을 선언하는 방법을 보려면 다음 장을 참조하십시오.
