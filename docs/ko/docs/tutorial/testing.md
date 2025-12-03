# 테스팅

<a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a> 덕분에 **FastAPI** 를 테스트하는 일은 쉽고 즐거운 일이 되었습니다.

Starlette는 <a href="https://www.python-httpx.org\" class="external-link" target="_blank">HTTPX</a>를 기반으로 하며, 이는 Requests를 기반으로 설계되었기 때문에 매우 친숙하고 직관적입니다.

이를 사용하면 FastAPI에서 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a>를 직접 사용할 수 있습니다.

## `TestClient` 사용하기

/// info | 정보

`TestClient` 사용하려면, 우선 <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a> 를 설치해야 합니다.

[virtual environment](../virtual-environments.md){.internal-link target=_blank} 를 만들고, 활성화 시킨 뒤에 설치하세요. 예시:

```console
$ pip install httpx
```

///

`TestClient` 를 임포트하세요.

**FastAPI** 어플리케이션을 전달하여 `TestClient` 를 만드세요.

이름이 `test_` 로 시작하는 함수를 만드세요(`pytest` 의 표준적인 관례입니다).

`httpx` 를 사용하는 것과 같은 방식으로 `TestClient` 객체를 사용하세요.

표준적인 파이썬 문법을 이용하여 확인이 필요한 곳에 간단한 `assert` 문장을 작성하세요(역시 표준적인 `pytest` 관례입니다).

{* ../../docs_src/app_testing/tutorial001.py hl[2,12,15:18] *}

/// tip | 팁

테스트를 위한 함수는 `async def` 가 아니라 `def` 로 작성됨에 주의하세요.

그리고 클라이언트에 대한 호출도 `await` 를 사용하지 않는 일반 호출입니다.

이렇게 하여 복잡한 과정 없이 `pytest` 를 직접적으로 사용할 수 있습니다.

///

/// note | 기술 세부사항

`from starlette.testclient import TestClient` 역시 사용할 수 있습니다.

**FastAPI** 는 개발자의 편의를 위해 `starlette.testclient` 를 `fastapi.testclient` 로도 제공할 뿐입니다. 이는 단지 `Starlette` 에서 직접 가져오는지의 차이일 뿐입니다.

///

/// tip | 팁

FastAPI 애플리케이션에 요청을 보내는 것 외에도 테스트에서 `async` 함수를 호출하고 싶다면 (예: 비동기 데이터베이스 함수), 심화 튜토리얼의 [Async Tests](../advanced/async-tests.md){.internal-link target=_blank} 를 참조하세요.

///

## 테스트 분리하기

실제 애플리케이션에서는 테스트를 별도의 파일로 나누는 경우가 많습니다.


그리고 **FastAPI** 애플리케이션도 여러 파일이나 모듈 등으로 구성될 수 있습니다.

### **FastAPI** app 파일

[Bigger Applications](bigger-applications.md){.internal-link target=_blank} 에 묘사된 파일 구조를 가지고 있는 것으로 가정해봅시다.

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

`main.py` 파일 안에 **FastAPI** app 을 만들었습니다:

{* ../../docs_src/app_testing/main.py *}

### 테스트 파일

테스트를 위해 `test_main.py` 라는 파일을 생성할 수 있습니다. 이 파일은 동일한 Python 패키지(즉, `__init__.py` 파일이 있는 동일한 디렉터리)에 위치할 수 있습니다.

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

파일들이 동일한 패키지에 위치해 있으므로, 상대 참조를 사용하여 `main` 에서 `app` 객체를 임포트 해올 수 있습니다.

{* ../../docs_src/app_testing/test_main.py hl[3] *}


...그리고 이전에 작성했던 것과 같은 테스트 코드를 작성할 수 있습니다.

## 테스트: 확장된 예시

이제 위의 예시를 확장하고 더 많은 세부 사항을 추가하여 다양한 부분을 어떻게 테스트하는지 살펴보겠습니다.

### 확장된 FastAPI 애플리케이션 파일

이전과 같은 파일 구조를 계속 사용해 보겠습니다.

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

이제 **FastAPI** 앱이 있는 `main.py` 파일에 몇 가지 다른 **경로 작업** 이 추가된 경우를 생각해봅시다.

단일 오류를 반환할 수 있는 `GET` 작업이 있습니다.

여러 다른 오류를 반환할 수 있는 `POST` 작업이 있습니다.

두 *경로 작업* 모두 `X-Token` 헤더를 요구합니다.

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

될 수 있으면 `Annotated` 버전 사용을 권장합나다.

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | 팁

될 수 있으면 `Annotated` 버전 사용을 권장합나다.

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### 확장된 테스트 파일

이제는 `test_main.py` 를 확장된 테스트들로 수정할 수 있습니다:

{* ../../docs_src/app_testing/app_b/test_main.py *}


클라이언트가 요청에 정보를 전달해야 하는데 방법을 모르겠다면, `httpx`에서 해당 작업을 수행하는 방법을 검색(Google)하거나, `requests`에서의 방법을 검색해보세요. HTTPX는 Requests의 디자인을 기반으로 설계되었습니다.

그 후, 테스트에서도 동일하게 적용하면 됩니다.

예시:

* *경로* 혹은 *쿼리* 매개변수를 전달하려면, URL 자체에 추가한다.
* JSON 본문을 전달하려면, 파이썬 객체 (예를들면 `dict`) 를 `json` 파라미터로 전달한다.
* JSON 대신 *폼 데이터* 를 보내야한다면, `data` 파라미터를 대신 전달한다.
* *헤더* 를 전달하려면, `headers` 파라미터에 `dict` 를 전달한다.
* *쿠키* 를 전달하려면, `cookies` 파라미터에 `dict` 를 전달한다.

백엔드로 데이터를 어떻게 보내는지 정보를 더 얻으려면 (`httpx` 혹은 `TestClient` 를 이용해서) <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX documentation</a> 를 확인하세요.

/// info | 정보

`TestClient` 는 Pydantic 모델이 아니라 JSON 으로 변환될 수 있는 데이터를 받습니다.

만약 테스트중 Pydantic 모델을 어플리케이션으로에 보내고 싶다면, [JSON 호환 가능 인코더](encoder.md){.internal-link target=_blank} 에 설명되어 있는 `jsonable_encoder` 를 사용할 수 있습니다.

///

## 실행하기

테스트 코드를 작성하고, `pytest` 를 설치해야합니다.

[virtual environment](../virtual-environments.md){.internal-link target=_blank} 를 만들고, 활성화 시킨 뒤에 설치하세요. 예시:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

`pytest` 파일과 테스트를 자동으로 감지하고 실행한 다음, 결과를 보고할 것입니다.

테스트를 다음 명령어로 실행하세요.

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
