# 테스팅

<a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a> 덕분에 **FastAPI** 를 테스트하는 일은 쉽고 즐거운 일이 되었습니다.

Starlette는 <a href="https://www.python-httpx.org\" class="external-link" target="_blank">HTTPX</a>를 기반으로 하며, 이는 Requests를 기반으로 설계되었기 때문에 매우 친숙하고 직관적입니다.

이를 사용하면 FastAPI에서 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a>를 직접 사용할 수 있습니다.

## `TestClient` 사용하기

/// info | 정보

`TestClient` 사용하려면, 우선 <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a> 를 설치해야 합니다.

[virtual environment](../virtual-environments.md){.internal-link target=_blank} 를 만들고, 활성화 시키고, 설치하는 것을 확실히 하세요. 예시:

```console
$ pip install httpx
```

///

`TestClient` 를 Import 하세요.

**FastAPI** 인스턴스를 인자로 넘겨서 `TestClient` 인스턴스를 만드세요.

이름이 `test_` 로 시작하는 함수를 만드세요. (`pytest` 의 표준적인 관례입니다.)

`httpx` 를 사용하는 것과 같이 `TestClient` 객체를 사용하세요.

표준적인 파이썬 문법을 이용하여 간단한 `assert` 문장을 작성하세요. (역시 표준적인 `pytest` 관례입니다).

```Python hl_lines="2  12  15-18"
{!../../docs_src/app_testing/tutorial001.py!}
```

/// tip | 팁

테스트를 위한 함수는 `async def` 가 아니라 `def` 로 작성됩니다.

그리고 `TestClient` 객체 호출 역시 `await` 을 사용하지 않는 일반적인 호출입니다.

이렇게 하여 복잡한 과정 없이 `pytest` 를 직접적으로 사용할 수 있습니다.

///

/// note | Technical Details | 기술 세부사항

`from starlette.testclient import TestClient` 역시 사용할 수 있습니다.

**FastAPI** 는 개발자의 편의를 위해 `starlette.testclient` 를 `fastapi.testclient` 로도 제공하는 것 뿐입니다. 차이는 오로지 `Starlette` 에서 직접 불러오느냐 아니냐 뿐입니다.

///

/// tip | 팁

FastAPI 애플리케이션에 요청을 보내는 것 외에도 테스트에서 `async` 함수를 호출하고 싶다면 (예: 비동기 데이터베이스 함수), 고급 튜토리얼의 [Async Tests](../advanced/async-tests.md){.internal-link target=_blank} 를 참조하세요.

///

## 분리된 테스트

실제 어플리케이션에서는 서로 다른 몇개의 테스트 파일을 만들게 될 것입니다.

**FastAPI** 어플리케이션 역시 여러개의 파일과 모듈 등으로 구성될 것입니다.

### **FastAPI** app 파일

[Bigger Applications](bigger-applications.md){.internal-link target=_blank} 에 묘사된 파일 구조를 가지고 있는 것으로 가정해봅시다.

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

`main.py` 파일에 아래와 같은  **FastAPI** 어플리케이션을 구성했습니다.

```Python
{!../../docs_src/app_testing/main.py!}
```

### 테스트 파일

테스트를 위해서 `test_main.py` 라는 파일도 가지고 있습니다. 이것은 동일한 파이썬 패키지에 위치해 있을 것입니다. (`__init__.py` 파일을 가진 동일한 디렉터리)

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

파일들이 동일한 패키지에 위치해 있기 때문에 상대 참조를 이용하여  **FastAPI** 인스턴스인 `app`을 `main` 에서 불러올 수 있습니다.

```Python hl_lines="3"
{!../../docs_src/app_testing/test_main.py!}
```

...그리고 직전 위에 묘사된것과 같은 테스트 코드를 작성할 수 있습니다.

## 테스트: 확장된 예시

이제는 위의 예시를 확장하고 더 많은 세부 사항을 추가해서 다른 부분들을 어떻게 테스트하는지 봅시다.

### 확장된 **FastAPI** 어플리케이션 파일

위의 예시와 동일한 파일 구조를 유지합니다.

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

이제는 **FastAPI** 인스턴스를 가진 `main.py` 파일에 몇몇의 다른 **경로 작동** 을 가진 경우를 생각해봅시다.

단일 에러를 반환할 수도 있는 `GET` 작동이 있습니다.

서로 다른 여러 에러를 반환할 수도 있는 `POST` 작동이 있습니다.

두 *경로 작동* 모두 `X-Token` 헤더를 요구합니다.

//// tab | Python 3.10+

```Python
{!> ../../docs_src/app_testing/app_b_an_py310/main.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/app_testing/app_b_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/app_testing/app_b_an/main.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | 팁

가능하면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | 팁

가능하면 `Annotated` 버전을 사용하는 것을 권장합니다.

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### 확장된 테스트 파일

이제는 `test_main.py` 를 확장된 테스트들로 수정할 수 있습니다.

```Python
{!> ../../docs_src/app_testing/app_b/test_main.py!}
```

요청의 설계가 `httpx` 의 설계에 기반하고 있기 때문에 클라이언트(TestClient) 에 정보를 어떻게 전달할지 모르겠으면  검색(Google) 을 통해 `httpx` 에서는 어떻게 하는지 찾아보면 알 수 있다.

그리고 테스트에 똑같이 적용하면 된다.

예시:

* *경로* 혹은 *쿼리* 매개변수를 전달하려면, URL 자체에 추가한다.
* JSON body 를 전달하려면, 파이썬 객체 (예를들면 `dict`) 를 `json` 파라미터로 전달한다.
* JSON 대신 *From Data* 를 보내야한다면, `data` 파라미터를 대신 전달한다.
* *headers* 를 전달하려면, `headers` 파라미터에 `dict` 를 전달한다.
* *cookies* 를 전달하려면, `cookies` 파라미터에 `dict` 를 전달한다.

백엔드로 데이터를 어떻게 보내는 정보를 더 얻으려면 (`httpx` 혹은 `TestClient` 를 이용해서)  <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX 문서</a> 를 확인하세요.

/// info | 정보

`TestClient` 는 Pydantic 모델이 아니라 JSON 으로 변환될 수 있는 데이터를 받습니다.

만약 테스트중 Pydantic 모델을 어플리케이션으로에 보내고 싶다면, [JSON Compatible Encoder](encoder.md){.internal-link target=_blank} 에 설명되어 있는 `jsonable_encoder` 를 사용할 수 있습니다.

///

## 실행하기

After that, you just need to install `pytest`.
테스트 코드를 작성하고, `pytest` 를 설치해야합니다.

[virtual environment](../virtual-environments.md){.internal-link target=_blank} 를 만들고, 활성화 시키고, 설치하는 것을 확실히 하세요. 예시:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

`pytest` 파일과 테스트를 자동으로 감지하고 실행한 다음, 결과를 보고할 것입니다.

test 를 다음과 같이 실행하세요.

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
