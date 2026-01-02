# 비동기 테스트 { #async-tests }

제공된 `TestClient`를 사용하여 **FastAPI** 애플리케이션을 테스트하는 방법을 이미 살펴보았습니다. 지금까지는 `async` 함수를 사용하지 않고, 동기 테스트를 작성하는 방법만 보았습니다.

테스트에서 비동기 함수를 사용할 수 있으면 유용할 수 있습니다. 예를 들어 데이터베이스를 비동기로 쿼리하는 경우를 생각해 보세요. FastAPI 애플리케이션에 요청을 보낸 다음, async 데이터베이스 라이브러리를 사용하면서 백엔드가 데이터베이스에 올바른 데이터를 성공적으로 기록했는지 검증하고 싶을 수 있습니다.

어떻게 동작하게 만들 수 있는지 살펴보겠습니다.

## pytest.mark.anyio { #pytest-mark-anyio }

테스트에서 비동기 함수를 호출하려면, 테스트 함수도 비동기여야 합니다. AnyIO는 이를 위한 깔끔한 플러그인을 제공하며, 일부 테스트 함수를 비동기로 호출하도록 지정할 수 있습니다.

## HTTPX { #httpx }

**FastAPI** 애플리케이션이 `async def` 대신 일반 `def` 함수를 사용하더라도, 내부적으로는 여전히 `async` 애플리케이션입니다.

`TestClient`는 표준 pytest를 사용하여, 일반 `def` 테스트 함수 안에서 비동기 FastAPI 애플리케이션을 호출하도록 내부에서 마법 같은 처리를 합니다. 하지만 비동기 함수 안에서 이를 사용하면 그 마법은 더 이상 동작하지 않습니다. 테스트를 비동기로 실행하면, 테스트 함수 안에서 `TestClient`를 더 이상 사용할 수 없습니다.

`TestClient`는 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>를 기반으로 하며, 다행히 HTTPX를 직접 사용해 API를 테스트할 수 있습니다.

## 예시 { #example }

간단한 예시로, [더 큰 애플리케이션](../tutorial/bigger-applications.md){.internal-link target=_blank}과 [테스트](../tutorial/testing.md){.internal-link target=_blank}에서 설명한 것과 비슷한 파일 구조를 살펴보겠습니다:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

`main.py` 파일은 다음과 같습니다:

{* ../../docs_src/async_tests/app_a_py39/main.py *}

`test_main.py` 파일에는 `main.py`에 대한 테스트가 있으며, 이제 다음과 같이 보일 수 있습니다:

{* ../../docs_src/async_tests/app_a_py39/test_main.py *}

## 실행하기 { #run-it }

다음과 같이 평소처럼 테스트를 실행할 수 있습니다:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 자세히 보기 { #in-detail }

`@pytest.mark.anyio` 마커는 pytest에게 이 테스트 함수가 비동기로 호출되어야 한다고 알려줍니다:

{* ../../docs_src/async_tests/app_a_py39/test_main.py hl[7] *}

/// tip | 팁

`TestClient`를 사용할 때처럼 단순히 `def`가 아니라, 이제 테스트 함수가 `async def`라는 점에 주목하세요.

///

그 다음 앱으로 `AsyncClient`를 만들고, `await`를 사용해 비동기 요청을 보낼 수 있습니다.

{* ../../docs_src/async_tests/app_a_py39/test_main.py hl[9:12] *}

이는 다음과 동등합니다:

```Python
response = client.get('/')
```

`TestClient`로 요청을 보내기 위해 사용하던 코드입니다.

/// tip | 팁

새 `AsyncClient`와 함께 async/await를 사용하고 있다는 점에 주목하세요. 요청은 비동기입니다.

///

/// warning | 경고

애플리케이션이 lifespan 이벤트에 의존한다면, `AsyncClient`는 이러한 이벤트를 트리거하지 않습니다. 이벤트가 트리거되도록 하려면 <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>의 `LifespanManager`를 사용하세요.

///

## 기타 비동기 함수 호출 { #other-asynchronous-function-calls }

테스트 함수가 이제 비동기이므로, 테스트에서 FastAPI 애플리케이션에 요청을 보내는 것 외에도 다른 `async` 함수를 코드의 다른 곳에서 호출하듯이 동일하게 호출하고 (`await`) 사용할 수도 있습니다.

/// tip | 팁

테스트에 비동기 함수 호출을 통합할 때(예: <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB의 MotorClient</a>를 사용할 때) `RuntimeError: Task attached to a different loop`를 마주친다면, 이벤트 루프가 필요한 객체는 async 함수 안에서만 인스턴스화해야 한다는 점을 기억하세요. 예를 들어 `@app.on_event("startup")` 콜백에서 인스턴스화할 수 있습니다.

///
