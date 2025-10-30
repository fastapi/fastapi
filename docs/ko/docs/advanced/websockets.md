# WebSockets

여러분은 **FastAPI**에서 <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a>를 사용할 수 있습니다.

## `WebSockets` 설치

[가상 환경](../virtual-environments.md){.internal-link target=_blank)를 생성하고 활성화한 다음, `websockets`를 설치하세요:

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets 클라이언트

### 프로덕션 환경에서

여러분의 프로덕션 시스템에서는 React, Vue.js 또는 Angular와 같은 최신 프레임워크로 생성된 프런트엔드를 사용하고 있을 가능성이 높습니다.

백엔드와 WebSockets을 사용해 통신하려면 아마도 프런트엔드의 유틸리티를 사용할 것입니다.

또는 네이티브 코드로 WebSocket 백엔드와 직접 통신하는 네이티브 모바일 응용 프로그램을 가질 수도 있습니다.

혹은 WebSocket 엔드포인트와 통신할 수 있는 다른 방법이 있을 수도 있습니다.

---

하지만 이번 예제에서는 일부 자바스크립트를 포함한 간단한 HTML 문서를 사용하겠습니다. 모든 것을 긴 문자열 안에 넣습니다.

물론, 이는 최적의 방법이 아니며 프로덕션 환경에서는 사용하지 않을 것입니다.

프로덕션 환경에서는 위에서 설명한 옵션 중 하나를 사용하는 것이 좋습니다.

그러나 이는 WebSockets의 서버 측에 집중하고 동작하는 예제를 제공하는 가장 간단한 방법입니다:

{* ../../docs_src/websockets/tutorial001.py hl[2,6:38,41:43] *}

## `websocket` 생성하기

**FastAPI** 응용 프로그램에서 `websocket`을 생성합니다:

{* ../../docs_src/websockets/tutorial001.py hl[1,46:47] *}

/// note | 기술적 세부사항

`from starlette.websockets import WebSocket`을 사용할 수도 있습니다.

**FastAPI**는 개발자를 위한 편의를 위해 동일한 `WebSocket`을 직접 제공합니다. 하지만 이는 Starlette에서 가져옵니다.

///

## 메시지를 대기하고 전송하기

WebSocket 경로에서 메시지를 대기(`await`)하고 전송할 수 있습니다.

{* ../../docs_src/websockets/tutorial001.py hl[48:52] *}

여러분은 이진 데이터, 텍스트, JSON 데이터를 받을 수 있고 전송할 수 있습니다.

## 시도해보기

파일 이름이 `main.py`라고 가정하고 응용 프로그램을 실행합니다:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

브라우저에서 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>을 열어보세요.

간단한 페이지가 나타날 것입니다:

<img src="/img/tutorial/websockets/image01.png">

입력창에 메시지를 입력하고 전송할 수 있습니다:

<img src="/img/tutorial/websockets/image02.png">

**FastAPI** WebSocket 응용 프로그램이 응답을 돌려줄 것입니다:

<img src="/img/tutorial/websockets/image03.png">

여러 메시지를 전송(그리고 수신)할 수 있습니다:

<img src="/img/tutorial/websockets/image04.png">

모든 메시지는 동일한 WebSocket 연결을 사용합니다.

## `Depends` 및 기타 사용하기

WebSocket 엔드포인트에서 `fastapi`에서 다음을 가져와 사용할 수 있습니다:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

이들은 다른 FastAPI 엔드포인트/*경로 작동*과 동일하게 동작합니다:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | 정보

WebSocket에서는 `HTTPException`을 발생시키는 것이 적합하지 않습니다. 대신 `WebSocketException`을 발생시킵니다.

명세서에 정의된 <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">유효한 코드</a>를 사용하여 종료 코드를 설정할 수 있습니다.

///

### 종속성을 가진 WebSockets 테스트

파일 이름이 `main.py`라고 가정하고 응용 프로그램을 실행합니다:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

브라우저에서 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>을 열어보세요.

다음과 같은 값을 설정할 수 있습니다:

* 경로에 사용된 "Item ID".
* 쿼리 매개변수로 사용된 "Token".

/// tip | 팁

쿼리 `token`은 종속성에 의해 처리됩니다.

///

이제 WebSocket에 연결하고 메시지를 전송 및 수신할 수 있습니다:

<img src="/img/tutorial/websockets/image05.png">

## 연결 해제 및 다중 클라이언트 처리

WebSocket 연결이 닫히면, `await websocket.receive_text()`가 `WebSocketDisconnect` 예외를 발생시킵니다. 이를 잡아 처리할 수 있습니다:

{* ../../docs_src/websockets/tutorial003_py39.py hl[79:81] *}

테스트해보기:

* 여러 브라우저 탭에서 앱을 엽니다.
* 각 탭에서 메시지를 작성합니다.
* 한 탭을 닫아보세요.

`WebSocketDisconnect` 예외가 발생하며, 다른 모든 클라이언트가 다음과 같은 메시지를 수신합니다:

```
Client #1596980209979 left the chat
```

/// tip | 팁

위 응용 프로그램은 여러 WebSocket 연결에 메시지를 브로드캐스트하는 방법을 보여주는 간단한 예제입니다.

그러나 모든 것을 메모리의 단일 리스트로 처리하므로, 프로세스가 실행 중인 동안만 동작하며 단일 프로세스에서만 작동합니다.

FastAPI와 쉽게 통합할 수 있으면서 더 견고하고 Redis, PostgreSQL 등을 지원하는 도구를 찾고 있다면, <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>를 확인하세요.

///

## 추가 정보

다음 옵션에 대한 자세한 내용을 보려면 Starlette의 문서를 확인하세요:

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">`WebSocket` 클래스</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">클래스 기반 WebSocket 처리</a>.
