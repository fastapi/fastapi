# 데이터 스트리밍 { #stream-data }

JSON으로 구조화할 수 있는 데이터를 스트리밍하려면 [JSON Lines 스트리밍](../tutorial/stream-json-lines.md)을 사용하세요.

하지만 순수 바이너리 데이터나 문자열을 스트리밍하려면 다음과 같이 하면 됩니다.

/// info | 정보

FastAPI 0.134.0에 추가되었습니다.

///

## 사용 예시 { #use-cases }

예를 들어 AI LLM 서비스의 출력에서 바로 순수 문자열을 스트리밍하고 싶다면 이를 사용할 수 있습니다.

또한 큰 바이너리 파일을 스트리밍하는 데 사용할 수 있습니다. 한 번에 모두 메모리로 읽지 않고, 읽는 즉시 데이터 청크를 순차적으로 스트리밍합니다.

이 방식으로 비디오나 오디오를 스트리밍할 수도 있으며, 처리하면서 생성된 데이터를 곧바로 전송할 수도 있습니다.

## `yield`와 함께 `StreamingResponse` 사용하기 { #a-streamingresponse-with-yield }

경로 처리 함수에서 `response_class=StreamingResponse`를 선언하면 `yield`를 사용해 데이터 청크를 순차적으로 보낼 수 있습니다.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI는 각 데이터 청크를 있는 그대로 `StreamingResponse`에 전달하며, JSON 등으로 변환하려고 하지 않습니다.

### async가 아닌 경로 처리 함수 { #non-async-path-operation-functions }

`async`가 없는 일반 `def` 함수에서도 동일하게 `yield`를 사용할 수 있습니다.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### 타입 애너테이션 생략하기 { #no-annotation }

바이너리 데이터를 스트리밍할 때는 반환 타입 애너테이션을 굳이 선언할 필요가 없습니다.

FastAPI는 데이터를 Pydantic으로 JSON으로 변환하거나 어떤 방식으로든 직렬화하지 않으므로, 이 경우 타입 애너테이션은 편집기나 도구를 위한 용도일 뿐이며 FastAPI에서는 사용되지 않습니다.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

이는 곧 `StreamingResponse`를 사용할 때 타입 애너테이션과 무관하게, 전송 기준에 맞춰 바이트 데이터를 생성하고 인코딩할 자유와 책임이 여러분에게 있음을 의미합니다. 🤓

### 바이트 스트리밍 { #stream-bytes }

주요 사용 사례 중 하나는 문자열 대신 `bytes`를 스트리밍하는 것입니다. 물론 그렇게 할 수 있습니다.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## 사용자 정의 `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

위 예시에서는 바이트 데이터를 스트리밍했지만, 응답에 `Content-Type` 헤더가 없어 클라이언트는 어떤 유형의 데이터를 받는지 알 수 없습니다.

스트리밍하는 데이터 유형에 맞춰 `Content-Type` 헤더를 설정하는 `StreamingResponse`의 하위 클래스를 직접 만들 수 있습니다.

예를 들어 `media_type` 속성을 사용해 `Content-Type` 헤더를 `image/png`로 설정하는 `PNGStreamingResponse`를 만들 수 있습니다:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

그런 다음 경로 처리 함수에서 `response_class=PNGStreamingResponse`로 이 새 클래스를 사용할 수 있습니다:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### 파일 시뮬레이션 { #simulate-a-file }

이 예시에서는 `io.BytesIO`로 파일을 시뮬레이션합니다. 이는 메모리에서만 존재하지만 파일과 동일한 인터페이스를 제공하는 파일 유사 객체입니다.

예를 들어 실제 파일처럼 내용을 소비하기 위해 순회(iterate)할 수 있습니다.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | 기술 세부사항

다른 두 변수 `image_base64`와 `binary_image`는 이미지를 Base64로 인코딩한 뒤 바이트로 변환한 것이며, 이를 `io.BytesIO`에 전달합니다.

이 예시에서 하나의 파일 안에 모두 담아, 그대로 복사해 실행할 수 있도록 하기 위한 목적입니다. 🥚

///

`with` 블록을 사용하면 제너레이터 함수(`yield`가 있는 함수)가 끝난 뒤, 즉 응답 전송이 완료된 후 파일 유사 객체가 닫히도록 보장합니다.

이 예시처럼 메모리 상의 가짜 파일(`io.BytesIO`)이라면 크게 중요하지 않지만, 실제 파일의 경우 작업이 끝난 뒤 파일을 닫는 것이 매우 중요합니다.

### 파일과 비동기 { #files-and-async }

대부분의 경우 파일 유사 객체는 기본적으로 async/await와 호환되지 않습니다.

예를 들어 `await file.read()`나 `async for chunk in file`과 같은 패턴을 지원하지 않습니다.

또한 디스크나 네트워크에서 읽기 때문에, 많은 경우 읽기 작업은 이벤트 루프를 막을 수 있는 블로킹 연산입니다.

/// info | 정보

위의 예시는 예외적인 경우입니다. `io.BytesIO` 객체는 이미 메모리에 있으므로 읽기가 아무 것도 차단하지 않습니다.

하지만 실제 파일이나 파일 유사 객체를 읽을 때는 블로킹되는 경우가 많습니다.

///

이벤트 루프가 블로킹되는 것을 피하려면 경로 처리 함수를 `async def` 대신 일반 `def`로 선언하세요. 그러면 FastAPI가 스레드풀 워커에서 실행하여 메인 루프가 막히지 않도록 합니다.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | 팁

비동기 함수 안에서 블로킹 코드를 호출해야 하거나, 반대로 블로킹 함수 안에서 비동기 함수를 호출해야 한다면 FastAPI의 형제 라이브러리인 [Asyncer](https://asyncer.tiangolo.com)를 사용할 수 있습니다.

///

### `yield from` { #yield-from }

파일 유사 객체처럼 어떤 것을 순회하면서 각 항목마다 `yield`를 하는 대신, `yield from`을 사용해 각 항목을 직접 전달하고 `for` 루프를 생략할 수 있습니다.

이는 FastAPI에 특화된 기능이 아니라 순수한 파이썬 기능이지만, 알아두면 유용한 트릭입니다. 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
