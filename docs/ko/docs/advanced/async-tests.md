# 비동기 테스트 코드 작성

이전 장에서  `TestClient` 를 이용해 **FastAPI** 어플리케이션 테스트를 작성하는 법을 배우셨을텐데요.
지금까지는 `async` 키워드 사용없이 동기 함수의 테스트 코드를 작성하는 법만 익혔습니다.

하지만 비동기 함수를 사용하여 테스트 코드를 작성하는 것은 매우 유용할 수 있습니다.
예를 들면 데이터베이스에 비동기로 쿼리하는 경우를 생각해봅시다.
FastAPI 애플리케이션에 요청을 보내고, 비동기 데이터베이스 라이브러리를 사용하여 백엔드가 데이터베이스에 올바르게 데이터를 기록했는지 확인하고 싶을 때가 있을 겁니다.

이런 경우의 테스트 코드를 어떻게 비동기로 작성하는지 알아봅시다.

## pytest.mark.anyio

앞에서 작성한 테스트 함수에서 비동기 함수를 호출하고 싶다면, 테스트 코드도 비동기 함수여야합니다.
AnyIO는 특정 테스트 함수를 비동기 함수로 호출 할 수 있는 깔끔한 플러그인을 제공합니다.


## HTTPX

**FastAPI** 애플리케이션이  `async def` 대신 `def` 키워드로 선언된 함수를 사용하더라도, 내부적으로는 여전히 `비동기` 애플리케이션입니다.

`TestClient`는 pytest 표준을 사용하여 비동기 FastAPI 애플리케이션을 일반적인 `def` 테스트 함수 내에서 호출할 수 있도록 내부에서 마술을 부립니다. 하지만 이 마술은 비동기 함수 내부에서 사용할 때는 더 이상 작동하지 않습니다. 테스트를 비동기로 실행하면, 더 이상 테스트 함수 내부에서 `TestClient`를 사용할 수 없습니다.

`TestClient`는 <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>를 기반으로 하고 있으며, 다행히 이를 직접 사용하여 API를 테스트할 수 있습니다.

## 예시

간단한 예시를 위해 [더 큰 어플리케이션 만들기](../ko/tutorial/bigger-applications.md){.internal-link target=_blank} 와 [테스트](../ko/tutorial/testing.md){.internal-link target=_blank}:에서 다룬 파일 구조와 비슷한 형태를 확인해봅시다:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

 `main.py`는 아래와 같아야 합니다:

{* ../../docs_src/async_tests/main.py *}

`test_main.py` 파일은 `main.py`에 대한 테스트가 있을 텐데, 다음과 같을 수 있습니다:

{* ../../docs_src/async_tests/test_main.py *}

## 실행하기

아래의 명령어로 테스트 코드를 실행합니다:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 자세히 보기

`@pytest.mark.anyio` 마커는 pytest에게 이 테스트 함수가 비동기로 호출되어야 함을 알려줍니다:

{* ../../docs_src/async_tests/test_main.py hl[7] *}

/// tip | 팁

테스트 함수가 이제 `TestClient`를 사용할 때처럼 단순히 `def`가 아니라 `async def`로 작성된 점에 주목해주세요.

///

그 다음에  `AsyncClient` 로 앱을 만들고 비동기 요청을 `await` 키워드로 보낼 수 있습니다:

{* ../../docs_src/async_tests/test_main.py hl[9:12] *}

위의 코드는:

```Python
response = client.get('/')
```

`TestClient` 에 요청을 보내던 것과 동일합니다.

/// tip | 팁

새로운 `AsyncClient`를 사용할 때 async/await를 사용하고 있다는 점에 주목하세요. 이 요청은 비동기적으로 처리됩니다.

///

/// warning | 경고

만약의 어플리케이션이 Lifespan 이벤트에 의존성을 갖고 있다면 `AsyncClient` 가 이러한 이벤트를 실행시키지 않습니다.
`AsyncClient` 가 테스트를 실행시켰다는 것을 확인하기 위해
`LifespanManager` from <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>.확인해주세요.


///

## 그 외의 비동기 함수 호출

테스트 함수가 이제 비동기 함수이므로, FastAPI 애플리케이션에 요청을 보내는 것 외에도 다른 `async` 함수를 호출하고 `await` 키워드를 사용 할 수 있습니다.

/// tip | 팁

테스트에 비동기 함수 호출을 통합할 때 (예: <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB의 MotorClient</a>를 사용할 때) `RuntimeError: Task attached to a different loop` 오류가 발생한다면, 이벤트 루프가 필요한 객체는 반드시 비동기 함수 내에서만 인스턴스화해야 한다는 점을 주의하세요!
예를 들어 `@app.on_event("startup")` 콜백 내에서 인스턴스화하는 것이 좋습니다.

///
