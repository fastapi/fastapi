# OpenTelemetry { #opentelemetry }

API가 실행 중일 때 얼마나 많은 트래픽을 받는지, 어떤 요청이 느린지, 언제 오류가 발생하는지 알고 싶을 수 있습니다.

**텔레메트리**는 이러한 질문에 답하는 데 도움이 되는 애플리케이션 동작에 관한 데이터입니다. 일반적인 유형은 다음과 같습니다:

- **메트릭**: 응답 시간이나 처리 중인 요청 수처럼 시간에 따라 요약할 수 있는 측정값입니다.
- **트레이스**: 개별 요청과 해당 요청을 처리하기 위해 수행한 작업의 기록입니다. 소요 시간을 측정하는 각 작업을 **스팬**이라고 합니다.
- **로그**: 애플리케이션 시작이나 작업 실패와 같은 이벤트에 타임스탬프를 붙인 기록입니다.

[**OpenTelemetry**](https://opentelemetry.io/)는 텔레메트리를 수집하여 모니터링 서비스로 보내기 위한 표준과 도구 모음입니다. 모니터링 서비스에서는 대시보드를 통해 데이터를 살펴볼 수 있습니다.

**FastAPI는 기본적으로 OpenTelemetry를 지원**하며, HTTP 요청의 트레이스, 메트릭, 로그를 제공합니다. WebSocket 연결도 트레이스와 로그를 제공합니다. 이 데이터를 보려면 모니터링 서비스에서 데이터를 수신하도록 설정하세요.

## FastAPI 설치하기 { #install-fastapi }

텔레메트리 전송용 패키지가 포함된 `standard` 추가 옵션으로 FastAPI를 설치하세요:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## 애플리케이션 만들기 { #create-the-app }

`main.py` 파일을 만드세요:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

이 모든 기능은 기본적으로 작동하며, 텔레메트리를 사용하기 위해 별도의 코드를 작성할 필요가 없습니다.

## FastAPI Cloud { #fastapi-cloud }

`fastapi[standard]`를 사용하여 [FastAPI Cloud](https://fastapicloud.com)에 배포하면 메트릭이 자동으로 작동합니다. 다른 설정은 필요하지 않습니다.

Pro 요금제에서는 [메트릭 대시보드](https://fastapicloud.com/docs/monitoring-and-performance/metrics/)에서 요청 수, 오류율, 응답 시간을 확인할 수 있습니다.

<img src="/img/tutorial/opentelemetry/image01.png" alt="예제 데이터가 표시된 FastAPI Cloud Pro 메트릭 대시보드">

## 다른 모니터링 서비스 { #other-monitoring-services }

다른 모니터링 서비스로 텔레메트리를 보내려면 텔레메트리 전송을 위한 OpenTelemetry 프로토콜인 **OTLP**를 지원하는 엔드포인트를 설정하세요. 해당 서비스의 HTTP/protobuf 기본 엔드포인트를 사용하세요.

예제 URL을 사용할 엔드포인트로 바꾸고 다음 환경 변수를 설정하세요:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME`은 모니터링 서비스에서 애플리케이션을 식별합니다. 엔드포인트는 데이터를 수신하는 기본 URL입니다. 트레이스는 해당 URL 아래의 `/v1/traces`로, 메트릭은 `/v1/metrics`로, 로그는 `/v1/logs`로 전송됩니다.

서비스에서 인증을 요구하는 경우, `OTEL_EXPORTER_OTLP_HEADERS`를 해당 서비스에서 지정한 헤더로 설정하세요. 예를 들면 `api-key=YOUR_API_KEY`입니다.

## 애플리케이션 실행하기 { #run-the-app }

같은 터미널에서 애플리케이션을 시작하세요:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

다른 터미널에서 요청을 보내세요:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

모니터링 서비스를 열고 `my-api`를 찾으세요. 다음 내보내기가 이루어진 후, `GET /items/{item_id}` 스팬이 포함된 트레이스와 함께 요청 수, 응답 소요 시간, 활성 요청에 대한 메트릭을 확인할 수 있습니다.

## 텔레메트리 사용자 정의하기 { #customize-telemetry }

### 프로바이더와 익스포터 설정하기 { #configure-providers-and-exporters }

**프로바이더**는 트레이스, 메트릭 또는 로그를 기록하는 객체를 제공합니다. 프로바이더 설정은 해당 데이터의 처리 및 내보내기 방식을 제어합니다.

텔레메트리 라이브러리는 OpenTelemetry의 전역 프로바이더를 설정할 수 있습니다. 애플리케이션이 시작되기 전에 라이브러리를 설정하면 FastAPI가 해당 프로바이더를 자동으로 사용합니다.

환경 변수에 OTLP 엔드포인트가 설정되어 있으면, FastAPI는 활성화된 각 프로바이더에 해당 대상으로 데이터를 보내는 익스포터를 추가합니다. 기존 익스포터는 계속해서 각자의 대상으로 데이터를 보냅니다.

각 대상은 한 번만 설정하세요. 다른 라이브러리가 이미 환경 변수에 지정된 대상으로의 전송을 처리하고 있다면, 해당 라이브러리의 환경 변수 기반 내보내기를 비활성화하거나 FastAPI의 자동 설정을 끄세요:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

`telemetry` 딕셔너리에 프로바이더를 직접 전달할 수도 있습니다. 예를 들어, 다음 프로바이더는 OpenTelemetry의 콘솔 익스포터를 사용하여 터미널에 요청 스팬을 출력합니다:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**익스포터**는 스팬을 대상으로 보냅니다. `BatchSpanProcessor`는 스팬을 그룹으로 묶어 백그라운드에서 보냅니다. 모니터링 라이브러리의 대상으로 보내려면 콘솔 익스포터를 해당 라이브러리에서 제공하는 익스포터로 바꾸세요. 더 많은 설정 옵션은 [OpenTelemetry의 Python 계측 가이드](https://opentelemetry.io/docs/languages/python/instrumentation/)를 참고하세요.

같은 딕셔너리에서 `meter_provider` 또는 `logger_provider`를 사용하여 메트릭 또는 로그 프로바이더를 제공하세요. 프로바이더를 생성한 애플리케이션이나 라이브러리가 해당 프로바이더의 종료를 관리합니다. FastAPI는 자신이 추가한 내보내기 구성 요소를 관리합니다.

/// warning | 경고

OpenTelemetry는 기본적으로 전역 프로바이더를 사용합니다. [마운트된 하위 애플리케이션](sub-applications.md)에 대한 독립적인 텔레메트리 설정은 보장되지 않습니다.

///

### 요청 작업 추적하기 { #trace-request-operations }

기본적으로 요청 트레이스에는 의존성 해결, 경로 처리 함수 실행, 응답 직렬화, FastAPI의 `BackgroundTasks`에 있는 각 작업 실행에 대한 스팬이 포함됩니다. 이 스팬들은 동일한 프로바이더와 익스포터를 사용합니다.

백그라운드 작업의 스팬도 해당 요청의 트레이스에 포함됩니다. 백그라운드 작업은 HTTP 응답 스팬이 끝난 후에 실행되므로 측정된 응답 시간을 늘리지 않습니다.

HTTP 요청 스팬만 기록하려면 `operation_spans`를 `False`로 설정하세요:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket 연결 추적하기 { #trace-websocket-connections }

각 WebSocket 연결에는 `WS /ws/{room}`과 같은 스팬이 있으며, 핸들러 실행과 의존성 정리 작업을 포함합니다. 이 스팬은 동일한 프로바이더와 설정을 사용하며, 여기에는 의존성 해결과 엔드포인트 실행을 위한 `operation_spans`도 포함됩니다.

HTTP 요청 메트릭은 HTTP 요청만 다룹니다. 코드 `1000` 또는 `1001`로 정상 종료된 WebSocket 연결은 오류 로그를 생성하지 않습니다.

### 오류 확인하기 { #inspect-errors }

FastAPI는 처리되지 않은 예외를 OpenTelemetry 로그로 기록하고, 해당 요청이나 연결의 트레이스에 연결합니다. 트레이스가 샘플링되지 않은 경우에도 오류 로그는 기록됩니다.

예외 로그에는 예외 유형, 메시지, 스택 트레이스가 포함됩니다. 메시지와 스택 트레이스에는 민감한 정보가 포함될 수 있습니다. 프로바이더의 로그 프로세서를 사용하여 이를 필터링하거나 민감한 정보를 가리세요. 또는 `logs`를 `False`로 설정하여 이 로그를 비활성화하세요.

FastAPI는 요청 유효성 검사 실패도 경로와 오류 수가 포함된 경고 로그로 기록합니다. 이 로그에는 유효하지 않은 입력값이 포함되지 않습니다.

## 기록할 항목 선택하기 { #choose-what-to-record }

`telemetry` 딕셔너리는 다음 설정도 지원합니다:

| 설정 | 용도 | 기본값 |
| --- | --- | --- |
| `tracing` | HTTP 요청 및 WebSocket 연결 스팬 기록 | `True` |
| `metrics` | HTTP 요청 메트릭 기록 | `True` |
| `logs` | 유효성 검사 실패 및 처리되지 않은 예외 기록 | `True` |
| `operation_spans` | 요청 작업에 대한 스팬 추가 | `True` |
| `exclude` | ASGI 스코프를 전달받는 함수가 `True`를 반환하면 해당 요청 제외 | `None` |
| `auto_configure` | 환경 변수에 설정된 엔드포인트에 대한 익스포터 추가 | `True` |

예를 들어, 상태 확인 요청을 제외하고 메트릭을 수집하려면 다음과 같이 설정하세요:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

애플리케이션이 lifespan 함수 내부 등에서 프로바이더 설정을 직접 처리하는 경우 `auto_configure`를 `False`로 설정하세요.
