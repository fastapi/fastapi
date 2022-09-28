# 리퀘스트 바디

클라이언트(예를 들면, 브라우저)에서 당신의 API로 데이터를 전송할 때, 데이터는 **리퀘스트 바디**로써 전송되어야 합니다.

**리퀘스트** 바디는 클라이언트에서 당신의 API로 전송하는 데이터입니다. **리스폰스** 바디는 당신의 API가 클라이언트에게 전송하는 데이터입니다.

API는 거의 모든 경우 **리스폰스** 바디를 전송해야 합니다. 하지만 클라이언트들은 필수로 **리퀘스트** 바디를 전송해야 하는 건 아닙니다.

**리퀘스트** 바디를 정의하기 위해서 강력한 기능과 장점들을 가진 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> 모델을 사용합니다.

!!! info 정보
데이터를 전송하려면 다음 항목들 중 하나를 사용합니다: `POST` (가장 일반적), `PUT`, `DELETE` 혹은 `PATCH`.

    `GET` 리퀘스트에 바디를 전송하는 것은 정의되지 않은 행동이지만, FastAPI는 극히 복잡하거나 특수한 경우를 위해 해당 기능을 지원함
    위 방법이 권장되지 않는 방법이기 때문에, 스웨거 UI가 적용된 문서에서는 `GET` 을 사용할 경우 바디를 보여주지 않으며 프록시들도 위 방법을 지원하지 않을 수 있음

## Pydantic의 `BaseModel` 불러오기

먼저, `pydantic`의 `BaseModel`을 불러옵니다:

=== "파이썬 3.6 이상"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

=== "파이썬 3.10 이상"

    ```Python hl_lines="2"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

## 나만의 데이터 모델 만들기

이제 나만의 데이터 모델을 `BaseModel`을 상속한 클래스로 정의합니다.

클래스 항목들에 대해서는 파이썬 표준 타입들을 사용합니다:

=== "파이썬 3.6 이상"

    ```Python hl_lines="7-11"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

=== "파이썬 3.10 이상"

    ```Python hl_lines="5-9"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

모델 항목에 기본값이 정의되어 있을 경우, 쿼리 매개변수를 정의했을 때처럼 해당 항목은 필수로 값을 전달받지 않아도 됩니다. 반대로, 기본값이 없을 경우 값을 필수로 전달받아야 합니다. `None`을 사용하면 값 전달 여부를 조건부로 만들 수 있습니다.

예를 들어, 다음 모델은 JSON "`객체`" (혹은 파이썬의 `딕셔너리`)를 다음과 같이 정의합니다:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...`description`과 `tax`가 조건부이기 때문에 (기본값이 `None`으로 설정됨), 아래 JSON "`객체`" 도 허용됩니다:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 파라미터로 정의

데이터를 *path operation*으로 전송할 경우, 경로와 쿼리 매개변수를 정의하는 것과 동일하게 정의합니다:

=== "파이썬 3.6 이상"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

=== "파이썬 3.10 이상"

    ```Python hl_lines="16"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

...그리고 데이터의 타입을 당신이 정의한 타입인 `Item`과 동일하게 정의하면 됩니다.

## 결과

단순히 파이썬 타입을 이용한 정의만 하면, **FastAPI** 가

* 리퀘스트 바디를 JSON형식으로 읽어들입니다.
* 적절한 형 변환을 해 줍니다 (필요 시).
* 데이터를 검증합니다.
    * 만약 데이터가 유효하지 않으면, 데이터의 어느 부분에서 무엇이 잘못되었는지를 나타내는 깔끔하고 명확한 에러를 반환합니다.
* `Item`파라미터에 전달받은 데이터를 담아 반환합니다.
    * 함수에서 데이터 타입을 `Item`으로 정의했기 때문에, 데이터의 항목들과 타입에 대한 에디터 지원(자동 완성 등)을 받을 수 있습니다.
* 프로젝트에 필요하다면, 모델에 대한 <a href="https://json-schema.org" class="external-link" target="_blank">JSON 스키마</a>를 정의해 두고 어디서든지 사용할 수 있습니다.
* 위 스키마들은 생성된 OpenAPI 스키마에 포함되며, 자동 문서화 <abbr title="User Interfaces">UI</abbr>에서 사용됩니다.

## 자동 문서

직접 정의한 모델의 JSON 스키마는 OpenAPI가 자동 생성한 스키마에 포함되며, 인터렉티브 API 문서에서 확인할 수 있습니다:

<img src="/img/tutorial/body/image01.png">

또한 API 문서 내에서 스키마를 필요로 하는 각 *path operation* 문서 내에서도 사용됩니다:

<img src="/img/tutorial/body/image02.png">

## 에디터 지원

에디터에서, 함수 내의 모든 곳에서 타입 힌트와 자동 완성 지원을 받을 수 있습니다 (만약 Pydantic모델 대신 `딕셔너리`형식의 데이터의 경우 지원되지 않음):

<img src="/img/tutorial/body/image03.png">

잘못된 타입 명령어 사용 시 에러를 표시해 줍니다:

<img src="/img/tutorial/body/image04.png">

이는 우연이 아니라, 전체 프레임워크가 그러한 디자인에 기반해서 만들어졌습니다.

또한, 위 기능은 모든 에디터에서 동일한 동작을 보장하기 위해 구현 전의 디자인 단계에서부터 철저히 테스트 되었습니다.

심지어 이를 지원하기 위해서 Pydantic에서 몇 차례 수정이 있었을 정도였습니다.

위 화면들은 <a href="https://code.visualstudio.com" class="external-link" target="_blank">비주얼 스튜디오 코드</a>에서의 화면입니다.

하지만 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>을 포함한 모든 파이썬 에디터에서 동일한 지원을 받을 수 있습니다.

<img src="/img/tutorial/body/image05.png">

!!! tip "팁"
만약 에디터로 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>을 사용한다면, <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>을 사용해도 됩니다.

    다음 항목들에 대해, Pydantic 모델들에 대한 에디터 지원을 도와줍니다:
    * 자동 완성
    * 타입 체크
    * 리팩토링
    * 검색
    * 검사

## 모델 사용

함수 내에서, 모델의 모든 항목에 대해 직접 접근이 가능합니다:

=== "파이썬 3.6 이상"

    ```Python hl_lines="21"
    {!> ../../../docs_src/body/tutorial002.py!}
    ```

=== "파이썬 3.10 이상"

    ```Python hl_lines="19"
    {!> ../../../docs_src/body/tutorial002_py310.py!}
    ```

## 리퀘스트 바디 + 경로 매개변수

경로 매개변수와 리퀘스트 바디를 동시에 정의할 수 있습니다.

**FastAPI** 는 함수 매개변수들 중, 경로 매개변수에서 값을 가져올 변수와, 리퀘스트 바디에서 가져올(Pydantic 모델로 정의된) 변수를 구분해서 매칭합니다.

=== "파이썬 3.6 이상"

    ```Python hl_lines="17-18"
    {!> ../../../docs_src/body/tutorial003.py!}
    ```

=== "파이썬 3.10 이상"

    ```Python hl_lines="15-16"
    {!> ../../../docs_src/body/tutorial003_py310.py!}
    ```

## 리퀘스트 바디 + 경로 + 쿼리 매개변수

**바디**, **경로** 그리고 **쿼리** 매개변수를, 한번에 정의할 수도 있습니다.

**FastAPI** 는 각각을 구분해서, 변수들의 값을 알맞은 위치에서 가져옵니다.

=== "파이썬 3.6 이상"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body/tutorial004.py!}
    ```

=== "파이썬 3.10 이상"

    ```Python hl_lines="16"
    {!> ../../../docs_src/body/tutorial004_py310.py!}
    ```

함수 매개변수는 다음과 같이 구분됩니다:

* **경로**에 동일한 변수가 정의되어 있다면, 해당 변수를 경로 매개변수로 해석합니다.
* 변수가 **단일 타입** (`int`, `float`, `str`, `bool` 등) 이라면 변수를 **쿼리** 매개변수로 해석합니다.
* 변수가 **Pydantic model**로 정의되어 있다면, 변수를 리퀘스트 **바디**로 해석합니다.

!!! note "참고"
FastAPI 는 변수 `q` 의 기본값이 `= None` 이라서, 필수값이 필요하지 않다는 것을 알고 있습니다.

    `Union[str, None]`안의 `Union` 은 FastAPI가 사용하진 않지만, 당신의 에디터가 더 나은 지원과 에러 검출을 할 수 있도록 합니다.

## Pydantic 이 없을 경우

Pydantic 모델을 사용하고 싶지 않다면, **Body** 매개변수를 사용해도 됩니다. 해당 내용은 다음 문서 [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}. 를 참조하세요.
