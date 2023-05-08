# 테스트

<a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a> 덕분에 **FastAPI** 어플리케이션을 테스트 하는것은 쉽고 재미있습니다.

Requests를 바탕으로 설계된 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>를 기반으로 하기 때문에 매우 익숙하고 직관적 입니다.

이것을 토대로 여러분은 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a>를 **FastAPI**와 함께 직접 사용하실 수 있습니다.

## `TestClient` 사용하기

!!! info "정보"
    `TestClient`를 이용 하시려면 먼저 <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>를 설치 하셔야 합니다.

    예시) `pip install httpx`.

`TestClient`를 임포트 합니다.

당신의 **FastAPI** 어플리케이션을 전달 하셔서 `TestClient`를 생성 합니다.

Create functions with a name that starts with `test_`로 시작하는 함수를 생성 합니다. (이것은 `pytest`의 표준적인 관례 입니다).

`httpx`를 사용 하시는 것과 같은 방식으로 `TestClient` 객체를 사용합니다.

여러분이 확인하고 싶으신 항목을 표준 파이썬 수식을 이용해 간단하게 `assert` 문장으로 작성합니다. (다시 한번, `pytest`의 표준적인 관례 입니다).

```Python hl_lines="2  12  15-18"
{!../../../docs_src/app_testing/tutorial001.py!}
```

!!! tip "팁"
    테스트 함수들은 `async def`가 아닌 일반적인 `def`으로 시작 한다는 것에 주목하시기 바랍니다.

    클라이언트를 호출 할때도 `await`이 아닌 일반적인 호출 입니다..

    이것은 여러분이 복잡한 절차 없이 `pytest`를 바로 사용하실 수 있게 도와줍니다.

!!! note "기술 세부사항"
    여러분은 또한 `from starlette.testclient import TestClient`를 사용하실 수도 있습니다.

    개발자인 여러분의 편의를 위해 **FastAPI**는 `starlette.testclient`과 동일한 `fastapi.testclient`.  그러나 이것은 Starlette에서 직접 파생된 기능 입니다.

!!! tip "팁"
    여러분이 만약 FastAPI 어플리케이션에 요청을 보내는 것과는 별개로 (에를 들어 비동기적인 데이터베이스 함수) `async` 함수를 호출하고 싶으시다면 심화 자습서에 있는 [Async Tests](../advanced/async-tests.md){.internal-link target=_blank}를 참고하시기 바랍니다.

## 테스트 분리하기

실제 어플리케이션에서 여러분들은 아마 다른 파일에 테스트를 따로 작성 하실 것 입니다.

그리고 여러분의 **FastAPI** 어플리케이션은 여러개의 파일과 모듈 등으로 구성이 되어 있을 수도 있습니다.

### **FastAPI** app 파일

여러분이 [Bigger Applications](./bigger-applications.md){.internal-link target=_blank} 에 서술된 파일 구조를 가지고 있다고 가정 합니다:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

`main.py`파일 안에 여러분의 **FastAPI** app 이 있습니다:


```Python
{!../../../docs_src/app_testing/main.py!}
```

### 테스트 파일

그렇다면 여러분은 `test_main.py` 파일에 테스트를 작성 하실 수도 있습니다. 이 파일은 동일한 파이썬 패키지에 위치할 수도 있습니다 (`__init__.py` 파일과 동일한 디렉토리):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

이 파일이 동일한 패키지에 위치하고 있기 때문에 여러분은 상대적 임포트를 통해 `main`모듈 (`main.py`)에서 `app` 객체를 임포트 하실 수 있습니다.

```Python hl_lines="3"
{!../../../docs_src/app_testing/test_main.py!}
```

...그리고 전과 동일하게 테스트 코드를 포함 시킬 수 있습니다.

## 테스팅: 확장 예시

이제 이 예시를 확장 시키고 어떻게 다른 부분들을 테스트 하는지 살펴보기 위해 추가적인 세부사항을 더해 봅니다.

### 확장된 **FastAPI** app 파일

앞에서 다룬 파일 구조를 가지고 진행 합니다.

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

이제 여러분의 **FastAPI** 어플리케이션에 있는 `main.py` 파일에 다른 **path operations**이 있다고 가정해 봅니다.

파일에 에러를 리턴 할 소지가 있는 `GET` 연산이 있습니다.

파일에 여러가지 에러를 리턴 할 소지가 있는 `POST` 연산이 있습니다.

두 *path operations* 모두 `X-Token` 헤더를 필요로 합니다.

=== "Python 3.10+"

    ```Python
    {!> ../../../docs_src/app_testing/app_b_an_py310/main.py!}
    ```

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/app_testing/app_b_an_py39/main.py!}
    ```

=== "Python 3.6+"

    ```Python
    {!> ../../../docs_src/app_testing/app_b_an/main.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python
    {!> ../../../docs_src/app_testing/app_b_py310/main.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python
    {!> ../../../docs_src/app_testing/app_b/main.py!}
    ```

### 확장된 테스팅 파일

이제 여러분은 `test_main.py`에 확장된 테스트를 추가해 업데이트 하실 수 있습니다:

```Python
{!> ../../../docs_src/app_testing/app_b/test_main.py!}
```

여러분이 클라이언트가 정보를 요청에 포함시켜 보내야 하지만 어떻게 해야 하는지 모르실때 `httpx`에서는 어떻게 하는지 또는 HTTPX 디자인의 바탕이 된 `requests`서는 어떻게 하는지 검색(구글)을 통해 찾아 보실 수 있습니다.

그 다음에 여러분의 테스트에서 그대로 따라하시면 됩니다.

예시:

* *path* 또는 *query* 매개변수를 전달하시려면 URL에 직접 대입 하시면 됩니다.
* JSON 본문 (body)를 전달하시려면 파이썬 객체 (예시로 `dict`)를 매개변수 `json`에 대입 하시면 됩니다.
* JSON 다신 *Form Data* 를 보내시려면 `data` 매개변수를 사용하시면 됩니다.
* *headers*를 전달 하시려면 `headers` 매개변수에 `dict`를 대입해 하시면 됩니다.
* *cookies*는 `dict`를 `cookies`매개변수에 대입 하시면 됩니다.

`httpx`나 `TestClient`를 이용하여 백엔드로 데이터를 전송하는 방법에 관한 더 많은 정보는<a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX documentation</a>에서 찾아 보실 수 있습니다.

!!! info "정보"
    `TestClient`는 Pydantic 모델이 아니라 JSON으로 변경이 가능한 데이터를 받는다는 점을 숙지 하시기 바랍니다.

    만약 여러분의 테스트에 Pydantic 모델이 있고 테스팅 중에 여러분이 그것의 데이터를 어플리케이션으로 전송 하고자 하신다면 [JSON Compatible Encoder](encoder.md){.internal-link target=_blank}에 나와있는 `jsonable_encoder`를 사용하실 수 있습니다.

## 실행

이후 여러분은 `pytest`을 설치 하시면 됩니다:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

파일과 테스트들이 자동으로 감지되며 실행이 되고 여러분에게 결과를 보고 합니다.

테스트를 다음과 같이 실행하십시오:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
