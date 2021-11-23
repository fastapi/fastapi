# 테스트

<a href="https://www.starlette.io/testclient/" class="external-link" target="_blank">Starlette</a> 덕분에 **FastAPI** 응용 프로그램을 쉽고 즐겁게 테스트할 수 있습니다. .

<a href="https://requests.readthedocs.io" class="external-link" target="_blank">요청</a>을 기반으로 하므로 매우 친숙하고 직관적입니다.

이를 통해 **FastAPI**와 함께 <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a>를 직접 사용할 수 있습니다.

## `TestClient` 사용

`TestClient`를 가져옵니다.

**FastAPI** 응용 프로그램에 전달하는 `TestClient`를 생성합니다.

`test_`로 시작하는 이름으로 함수를 생성합니다 (표준 `pytest` 규칙).

`requests`와 동일한 방식으로 `TestClient` 객체를 사용합니다.

확인해야 하는 표준 Python 표현식으로 간단한 `assert` 문을 작성합니다(표준 `pytest` 규칙).

```파이썬 hl_lines="2 12 15-18"
{!../../../docs_src/app_testing/tutorial001.py!}
```

!!! 팁  테스트 함수는 `async def`가 아닌 일반 `def`입니다.

    그리고 클라이언트에 대한 호출도 `await`를 사용하지 않는 일반 호출입니다.
    
    이렇게 하면 복잡함 없이 `pytest`를 직접 사용할 수 있습니다.

!!! 참고  "기술적 세부 사항"  `from starlette.testclient import TestClient`를 통해 사용할 수 있습니다.

    **FastAPI**는 개발자 여러분의 편의를 위해 `fastapi.testclient`와 동일한 `starlette.testclient`를 제공합니다. 그러나 그것은 Starlette에서 직접 제공됩니다.

!!! 팁  FastAPI 애플리케이션(예: 비동기 데이터베이스 함수)에 요청을 보내는 것과 별도로 테스트에서 `async` 함수를 호출하려면 고급 자습서의 [Async Tests](../advanced/async-tests.md){internal-link target=_blank} 를 살펴보세요.

## 테스트 분리

실제 응용 프로그램에서는 테스트가 다른 파일에 있을 수 있습니다.

그리고 **FastAPI** 애플리케이션은 여러 파일/모듈 등으로 구성될 수도 있습니다.

### **FastAPI** 앱 파일

**FastAPI** 앱에 `main.py` 파일이 있다고 가정해 보겠습니다.

```파이썬
{!../../../docs_src/app_testing/main.py!}
```

### 테스트 파일

그런 다음 테스트와 함께 `test_main.py` 파일을 만들고 `main` 모듈(`main.py`)에서 `app`을 가져올 수 있습니다.

```파이썬
{!../../../docs_src/app_testing/test_main.py!}
```

## 테스트: 확장된 예제

이제 이 예제를 확장하고 세부 사항을 추가하여 다른 부분을 테스트하는 방법을 살펴보겠습니다.

### 확장된 **FastAPI** 앱 파일

**FastAPI** 앱에 `main_b.py` 파일이 있다고 가정해 보겠습니다.

오류를 반환할 수 있는 `GET` 작업이 있습니다.

여러 오류를 반환할 수 있는 `POST` 작업이 있습니다.

두 *경로 작업* 모두 `X-Token` 헤더가 필요합니다.

```파이썬
{!../../../docs_src/app_testing/main_b.py!}
```

### 확장 테스트 파일

다음으로 확장 테스트를 통해 이전과 동일한 `test_main_b.py`를 가질 수 있습니다.

```파이썬
{!../../../docs_src/app_testing/test_main_b.py!}
```

클라이언트가 요청에 정보를 전달해야 하는데 방법을 모를 때마다 '요청'에서 방법을 검색할 수 있습니다(Google).

그런 다음 테스트에서 동일한 작업을 수행합니다.

예:

* *경로*  혹은 *쿼리*  매개변수를 전달하려면 URL 자체에 추가하십시오.
* JSON 본문을 전달하려면 파이썬 객체(예: `dict`)를 매개변수 `json`에 전달합니다.
* JSON 대신 *데이터에서*  보내야 한다면 `data` 매개변수를 대신 사용하세요.
* *headers*를 전달하려면 `headers` 매개변수에 `dict`를 사용하세요.
* *cookies*의 경우 `cookies` 매개변수의 `dict`.

데이터를 백엔드에 전달하는 방법(`requests` 또는 `TestClient` 사용)에 대한 자세한 내용은 <a href="https://requests.readthedocs.io" class="external-link" target="_blank를 확인하세요. ">문서 요청</a>을 확인하세요.

!!! 정보  `TestClient`는 Pydantic 모델이 아닌 JSON으로 변환할 수 있는 데이터를 수신합니다.

    테스트에 Pydantic 모델이 있고 테스트 중에 해당 데이터를 애플리케이션으로 보내려면 [JSON 호환 인코더](encoder.md){.internal-link target=_blank}에 설명된 `jsonable_encoder`를 사용할 수 있습니다. .

## 실행

그런 다음 `pytest`를 설치하기만 하면 됩니다.

<div class="termy">

```콘솔
$ pip install pytest

---> 100%
```

파일과 테스트를 자동으로 감지하고 실행하여 결과를 다시 보고합니다.

다음을 사용하여 테스트를 실행합니다.

<div class="termy">

```콘솔
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
