# 백그라운드 작업 { #background-tasks }

FastAPI에서는 응답을 반환한 *후에* 실행할 백그라운드 작업을 정의할 수 있습니다.

백그라운드 작업은 요청 후에 발생해야 하지만, 클라이언트가 응답을 받기 전에 작업이 완료될 때까지 기다릴 필요가 없는 작업에 유용합니다.

예를 들면 다음과 같습니다.

* 작업을 수행한 후 전송되는 이메일 알림:
    * 이메일 서버에 연결하고 이메일을 전송하는 것은 (몇 초 정도) "느린" 경향이 있으므로, 응답은 즉시 반환하고 이메일 알림은 백그라운드에서 전송할 수 있습니다.
* 데이터 처리:
    * 예를 들어 처리에 오랜 시간이 걸리는 프로세스를 거쳐야 하는 파일을 받았다면, "Accepted"(HTTP 202) 응답을 반환하고 백그라운드에서 파일을 처리할 수 있습니다.

## `BackgroundTasks` 사용 { #using-backgroundtasks }

먼저 `BackgroundTasks`를 임포트하고, `BackgroundTasks` 타입 선언으로 *경로 처리 함수*에 매개변수를 정의합니다:

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[1,13] *}

**FastAPI**가 `BackgroundTasks` 타입의 객체를 생성하고 해당 매개변수로 전달합니다.

## 작업 함수 생성 { #create-a-task-function }

백그라운드 작업으로 실행할 함수를 생성합니다.

이는 매개변수를 받을 수 있는 표준 함수일 뿐입니다.

`async def` 함수일 수도, 일반 `def` 함수일 수도 있으며, **FastAPI**가 이를 올바르게 처리하는 방법을 알고 있습니다.

이 경우 작업 함수는 파일에 쓰기를 수행합니다(이메일 전송을 시뮬레이션).

그리고 쓰기 작업은 `async`와 `await`를 사용하지 않으므로, 일반 `def`로 함수를 정의합니다:

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[6:9] *}

## 백그라운드 작업 추가 { #add-the-background-task }

*경로 처리 함수* 내부에서 `.add_task()` 메서드로 작업 함수를 *백그라운드 작업* 객체에 전달합니다:

{* ../../docs_src/background_tasks/tutorial001_py39.py hl[14] *}

`.add_task()`는 다음 인자를 받습니다:

* 백그라운드에서 실행될 작업 함수(`write_notification`).
* 작업 함수에 순서대로 전달되어야 하는 인자 시퀀스(`email`).
* 작업 함수에 전달되어야 하는 키워드 인자(`message="some notification"`).

## 의존성 주입 { #dependency-injection }

`BackgroundTasks`는 의존성 주입 시스템에서도 동작하며, *경로 처리 함수*, 의존성(dependable), 하위 의존성 등 여러 수준에서 `BackgroundTasks` 타입의 매개변수를 선언할 수 있습니다.

**FastAPI**는 각 경우에 무엇을 해야 하는지와 동일한 객체를 어떻게 재사용해야 하는지를 알고 있으므로, 모든 백그라운드 작업이 함께 병합되어 이후 백그라운드에서 실행됩니다:


{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}


이 예제에서는 응답이 전송된 *후에* 메시지가 `log.txt` 파일에 작성됩니다.

요청에 쿼리가 있었다면, 백그라운드 작업으로 로그에 작성됩니다.

그 다음 *경로 처리 함수*에서 생성된 또 다른 백그라운드 작업이 `email` 경로 매개변수를 사용해 메시지를 작성합니다.

## 기술적 세부사항 { #technical-details }

`BackgroundTasks` 클래스는 <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>에서 직접 가져옵니다.

FastAPI에 직접 임포트/포함되어 있으므로 `fastapi`에서 임포트할 수 있고, 실수로 `starlette.background`에서 대안인 `BackgroundTask`(끝에 `s`가 없음)를 임포트하는 것을 피할 수 있습니다.

`BackgroundTask`가 아닌 `BackgroundTasks`만 사용하면, 이를 *경로 처리 함수*의 매개변수로 사용할 수 있고 나머지는 **FastAPI**가 `Request` 객체를 직접 사용할 때처럼 대신 처리해 줍니다.

FastAPI에서 `BackgroundTask`만 단독으로 사용하는 것도 가능하지만, 코드에서 객체를 생성하고 이를 포함하는 Starlette `Response`를 반환해야 합니다.

더 자세한 내용은 <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">Starlette의 Background Tasks 공식 문서</a>에서 확인할 수 있습니다.

## 주의사항 { #caveat }

무거운 백그라운드 계산을 수행해야 하고, 반드시 동일한 프로세스에서 실행할 필요가 없다면(예: 메모리, 변수 등을 공유할 필요가 없음) <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a> 같은 더 큰 도구를 사용하는 것이 도움이 될 수 있습니다.

이들은 RabbitMQ나 Redis 같은 메시지/작업 큐 관리자 등 더 복잡한 설정을 필요로 하는 경향이 있지만, 여러 프로세스에서, 특히 여러 서버에서 백그라운드 작업을 실행할 수 있습니다.

하지만 동일한 **FastAPI** 앱의 변수와 객체에 접근해야 하거나(또는 이메일 알림 전송처럼) 작은 백그라운드 작업을 수행해야 한다면, `BackgroundTasks`를 간단히 사용하면 됩니다.

## 요약 { #recap }

*경로 처리 함수*와 의존성에서 매개변수로 `BackgroundTasks`를 임포트해 사용하여 백그라운드 작업을 추가합니다.
