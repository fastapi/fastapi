# 백그라운드 작업

FastAPI에서는 응답을 반환한 후에 실행할 백그라운드 작업을 정의할 수 있습니다.

백그라운드 작업은 클라이언트가 응답을 받기 위해 작업이 완료될 때까지 기다릴 필요가 없기 때문에 요청 후에 발생해야하는 작업에 매우 유용합니다.

이러한 작업에는 다음이 포함됩니다.

* 작업을 수행한 후 전송되는 이메일 알림
    * 이메일 서버에 연결하고 이메일을 전송하는 것은 (몇 초 정도) "느린" 경향이 있으므로, 응답은 즉시 반환하고 이메일 알림은 백그라운드에서 전송하는 게 가능합니다.
* 데이터 처리:
    * 예를 들어 처리에 오랜 시간이 걸리는 데이터를 받았을 때 "Accepted" (HTTP 202)을 반환하고, 백그라운드에서 데이터를 처리할 수 있습니다.

## `백그라운드 작업` 사용

먼저 아래와 같이 `BackgroundTasks`를 임포트하고, `BackgroundTasks`를 _경로 작동 함수_ 에서 매개변수로 가져오고 정의합니다.

{* ../../docs_src/background_tasks/tutorial001.py hl[1,13] *}

**FastAPI** 는 `BackgroundTasks` 개체를 생성하고, 매개 변수로 전달합니다.

## 작업 함수 생성

백그라운드 작업으로 실행할 함수를 정의합니다.

이것은 단순히 매개변수를 받을 수 있는 표준 함수일 뿐입니다.

**FastAPI**는 이것이 `async def` 함수이든, 일반 `def` 함수이든 내부적으로 이를 올바르게 처리합니다.

이 경우, 아래 작업은 파일에 쓰는 함수입니다. (이메일 보내기 시물레이션)

그리고 이 작업은 `async`와 `await`를 사용하지 않으므로 일반 `def` 함수로 선언합니다.

{* ../../docs_src/background_tasks/tutorial001.py hl[6:9] *}

## 백그라운드 작업 추가

_경로 작동 함수_ 내에서 작업 함수를 `.add_task()` 함수 통해 _백그라운드 작업_ 개체에 전달합니다.

{* ../../docs_src/background_tasks/tutorial001.py hl[14] *}

`.add_task()` 함수는 다음과 같은 인자를 받습니다 :

- 백그라운드에서 실행되는 작업 함수 (`write_notification`).
- 작업 함수에 순서대로 전달되어야 하는 일련의 인자 (`email`).
- 작업 함수에 전달되어야하는 모든 키워드 인자 (`message="some notification"`).

## 의존성 주입

`BackgroundTasks`를 의존성 주입 시스템과 함께 사용하면 _경로 작동 함수_, 종속성, 하위 종속성 등 여러 수준에서 BackgroundTasks 유형의 매개변수를 선언할 수 있습니다.

**FastAPI**는 각 경우에 수행할 작업과 동일한 개체를 내부적으로 재사용하기에, 모든 백그라운드 작업이 함께 병합되고 나중에 백그라운드에서 실행됩니다.

{* ../../docs_src/background_tasks/tutorial002.py hl[13,15,22,25] *}

이 예제에서는 응답이 반환된 후에 `log.txt` 파일에 메시지가 기록됩니다.

요청에 쿼리가 있는 경우 백그라운드 작업의 로그에 기록됩니다.

그리고 _경로 작동 함수_ 에서 생성된 또 다른 백그라운드 작업은 경로 매개 변수를 활용하여 사용하여 메시지를 작성합니다.

## 기술적 세부사항

`BackgroundTasks` 클래스는 <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>에서 직접 가져옵니다.

`BackgroundTasks` 클래스는 FastAPI에서 직접 임포트하거나 포함하기 때문에 실수로 `BackgroundTask` (끝에 `s`가 없음)을 임포트하더라도 starlette.background에서 `BackgroundTask`를 가져오는 것을 방지할 수 있습니다.

(`BackgroundTask`가 아닌) `BackgroundTasks`를 사용하면, _경로 작동 함수_ 매개변수로 사용할 수 있게 되고 나머지는 **FastAPI**가 대신 처리하도록 할 수 있습니다. 이것은 `Request` 객체를 직접 사용하는 것과 같은 방식입니다.

FastAPI에서 `BackgroundTask`를 단독으로 사용하는 것은 여전히 가능합니다. 하지만 객체를 코드에서 생성하고, 이 객체를 포함하는 Starlette `Response`를 반환해야 합니다.

<a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`Starlette의 공식 문서`</a>에서 백그라운드 작업에 대한 자세한 내용을 확인할 수 있습니다.

## 경고

만약 무거운 백그라운드 작업을 수행해야하고 동일한 프로세스에서 실행할 필요가 없는 경우 (예: 메모리, 변수 등을 공유할 필요가 없음) <a href="https://docs.celeryq.dev" class="external-link" target="_blank">`Celery`</a>와 같은 큰 도구를 사용하면 도움이 될 수 있습니다.

RabbitMQ 또는 Redis와 같은 메시지/작업 큐 시스템 보다 복잡한 구성이 필요한 경향이 있지만, 여러 작업 프로세스를 특히 여러 서버의 백그라운드에서 실행할 수 있습니다.

그러나 동일한 FastAPI 앱에서 변수 및 개체에 접근해야햐는 작은 백그라운드 수행이 필요한 경우 (예 : 알림 이메일 보내기) 간단하게 `BackgroundTasks`를 사용해보세요.

## 요약

백그라운드 작업을 추가하기 위해 _경로 작동 함수_ 에 매개변수로 `BackgroundTasks`를 가져오고 사용합니다.
