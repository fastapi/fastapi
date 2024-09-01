# 이벤트: startup과 shutdown

필요에 따라 응용 프로그램이 시작되기 전이나 종료될 때 실행되는 이벤트 핸들러(함수)를 정의할 수 있습니다.

이 함수들은 `async def` 또는 평범하게 `def`으로 선언할 수 있습니다.

/// warning | "경고"

이벤트 핸들러는 주 응용 프로그램에서만 작동합니다. [하위 응용 프로그램 - 마운트](./sub-applications.md){.internal-link target=_blank}에서는 작동하지 않습니다.

///

## `startup` 이벤트

응용 프로그램을 시작하기 전에 실행하려는 함수를 "startup" 이벤트로 선언합니다:

```Python hl_lines="8"
{!../../../docs_src/events/tutorial001.py!}
```

이 경우 `startup` 이벤트 핸들러 함수는 단순히 몇 가지 값으로 구성된 `dict` 형식의 "데이터베이스"를 초기화합니다.

하나 이상의 이벤트 핸들러 함수를 추가할 수도 있습니다.

그리고 응용 프로그램은 모든 `startup` 이벤트 핸들러가 완료될 때까지 요청을 받지 않습니다.

## `shutdown` 이벤트

응용 프로그램이 종료될 때 실행하려는 함수를 추가하려면 `"shutdown"` 이벤트로 선언합니다:

```Python hl_lines="6"
{!../../../docs_src/events/tutorial002.py!}
```

이 예제에서 `shutdown` 이벤트 핸들러 함수는 `"Application shutdown"`이라는 텍스트가 적힌 `log.txt` 파일을 추가할 것입니다.

/// info | "정보"

`open()` 함수에서 `mode="a"`는 "추가"를 의미합니다. 따라서 이미 존재하는 파일의 내용을 덮어쓰지 않고 새로운 줄을 추가합니다.

///

/// tip | "팁"

이 예제에서는 파일과 상호작용 하기 위해 파이썬 표준 함수인 `open()`을 사용하고 있습니다.

따라서 디스크에 데이터를 쓰기 위해 "대기"가 필요한 I/O (입력/출력) 작업을 수행합니다.

그러나 `open()`은 `async`와 `await`을 사용하지 않기 때문에 이벤트 핸들러 함수는 `async def`가 아닌 표준 `def`로 선언하고 있습니다.

///

/// info | "정보"

이벤트 핸들러에 관한 내용은 <a href="https://www.starlette.io/events/" class="external-link" target="_blank">Starlette 이벤트 문서</a>에서 추가로 확인할 수 있습니다.

///
