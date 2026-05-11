# 서버 전송 이벤트(SSE) { #server-sent-events-sse }

브라우저 클라이언트로 데이터를 스트리밍하려면 **Server-Sent Events**(SSE)를 사용할 수 있습니다.

이는 [JSON Lines 스트리밍](stream-json-lines.md)과 비슷하지만, 브라우저가 기본적으로 [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)를 통해 지원하는 `text/event-stream` 형식을 사용합니다.

/// info | 정보

FastAPI 0.135.0에 추가되었습니다.

///

## Server-Sent Events란 { #what-are-server-sent-events }

SSE는 서버에서 클라이언트로 HTTP를 통해 데이터를 스트리밍하기 위한 표준입니다.

각 이벤트는 `data`, `event`, `id`, `retry`와 같은 "필드"를 가진 작은 텍스트 블록이며, 빈 줄로 구분됩니다.

다음과 같습니다:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE는 AI 채팅 스트리밍, 실시간 알림, 로그와 관측성, 그리고 서버가 클라이언트로 업데이트를 푸시하는 여러 경우에 흔히 사용됩니다.

/// tip | 팁

비디오나 오디오처럼 바이너리 데이터를 스트리밍하려면 고급 가이드: [데이터 스트리밍](../advanced/stream-data.md)을 확인하세요.

///

## FastAPI로 SSE 스트리밍 { #stream-sse-with-fastapi }

FastAPI에서 SSE를 스트리밍하려면, 경로 처리 함수에서 `yield`를 사용하고 `response_class=EventSourceResponse`를 설정하세요.

`EventSourceResponse`는 `fastapi.sse`에서 임포트합니다:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

각 `yield`된 항목은 JSON으로 인코딩되어 SSE 이벤트의 `data:` 필드로 전송됩니다.

반환 타입을 `AsyncIterable[Item]`으로 선언하면 FastAPI가 이를 사용해 데이터를 Pydantic으로 **검증**, **문서화**, **직렬화**합니다.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | 팁

Pydantic이 **Rust** 쪽에서 직렬화하므로, 반환 타입을 선언하지 않았을 때보다 훨씬 더 높은 **성능**을 얻을 수 있습니다.

///

### 비 async *경로 처리 함수* { #non-async-path-operation-functions }

`async`가 없는 일반 `def` 함수도 사용할 수 있으며, 동일하게 `yield`를 사용할 수 있습니다.

FastAPI가 이벤트 루프를 막지 않도록 올바르게 실행을 보장합니다.

이 경우 함수가 async가 아니므로 적절한 반환 타입은 `Iterable[Item]`입니다:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### 반환 타입 없음 { #no-return-type }

반환 타입을 생략할 수도 있습니다. FastAPI는 [`jsonable_encoder`](./encoder.md)를 사용해 데이터를 변환하고 전송합니다.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

`event`, `id`, `retry`, `comment` 같은 SSE 필드를 설정해야 한다면, 일반 데이터 대신 `ServerSentEvent` 객체를 `yield`할 수 있습니다.

`ServerSentEvent`는 `fastapi.sse`에서 임포트합니다:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` 필드는 항상 JSON으로 인코딩됩니다. Pydantic 모델을 포함해 JSON으로 직렬화할 수 있는 값을 모두 전달할 수 있습니다.

## 원시 데이터 { #raw-data }

JSON 인코딩 없이 데이터를 보내야 한다면, `data` 대신 `raw_data`를 사용하세요.

미리 포맷된 텍스트, 로그 라인, 또는 `[DONE]`과 같은 특수한 <dfn title="특수한 조건이나 상태를 나타내는 데 사용되는 값">"센티널"</dfn> 값을 보낼 때 유용합니다.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | 참고

`data`와 `raw_data`는 상호 배타적입니다. 각 `ServerSentEvent`에는 이 둘 중 하나만 설정할 수 있습니다.

///

## `Last-Event-ID`로 재개하기 { #resuming-with-last-event-id }

브라우저가 연결이 끊긴 후 재연결할 때, 마지막으로 받은 `id`를 `Last-Event-ID` 헤더에 담아 보냅니다.

헤더 파라미터로 이를 읽어와 클라이언트가 중단한 지점부터 스트림을 재개할 수 있습니다:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## POST로 SSE 사용하기 { #sse-with-post }

SSE는 `GET`뿐만 아니라 **모든 HTTP 메서드**와 함께 동작합니다.

이는 `POST`로 SSE를 스트리밍하는 [MCP](https://modelcontextprotocol.io) 같은 프로토콜에 유용합니다:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## 기술 세부사항 { #technical-details }

FastAPI는 일부 SSE 모범 사례를 기본으로 구현합니다.

- 메시지가 없을 때는 15초마다 **"keep alive" `ping` 주석**을 보내 일부 프록시가 연결을 종료하지 않도록 합니다. [HTML 사양: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes)에서 권장합니다.
- 스트림이 **캐시되지 않도록** `Cache-Control: no-cache` 헤더를 설정합니다.
- Nginx 같은 일부 프록시에서 **버퍼링을 방지**하기 위해 특수 헤더 `X-Accel-Buffering: no`를 설정합니다.

여러분이 따로 할 일은 없습니다. 기본값으로 동작합니다. 🤓
