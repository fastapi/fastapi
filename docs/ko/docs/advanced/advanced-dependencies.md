# 고급 의존성 { #advanced-dependencies }

## 매개변수화된 의존성 { #parameterized-dependencies }

지금까지 본 모든 의존성은 고정된 함수 또는 클래스입니다.

하지만 여러 개의 함수나 클래스를 선언하지 않고도 의존성에 매개변수를 설정해야 하는 경우가 있을 수 있습니다.

예를 들어, `q` 쿼리 매개변수가 특정 고정된 내용을 포함하고 있는지 확인하는 의존성을 원한다고 가정해 봅시다.

이때 해당 고정된 내용을 매개변수화할 수 있길 바랍니다.

## "호출 가능한" 인스턴스 { #a-callable-instance }

Python에는 클래스의 인스턴스를 "호출 가능"하게 만드는 방법이 있습니다.

클래스 자체(이미 호출 가능함)가 아니라 해당 클래스의 인스턴스에 대해 호출 가능하게 하는 것입니다.

이를 위해 `__call__` 메서드를 선언합니다:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

이 경우, **FastAPI**는 추가 매개변수와 하위 의존성을 확인하기 위해 `__call__`을 사용하게 되며,
나중에 *경로 처리 함수*에서 매개변수에 값을 전달할 때 이를 호출하게 됩니다.

## 인스턴스 매개변수화하기 { #parameterize-the-instance }

이제 `__init__`을 사용하여 의존성을 "매개변수화"할 수 있는 인스턴스의 매개변수를 선언할 수 있습니다:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

이 경우, **FastAPI**는 `__init__`에 전혀 관여하지 않으며, 우리는 이 메서드를 코드에서 직접 사용하게 됩니다.

## 인스턴스 생성하기 { #create-an-instance }

다음과 같이 이 클래스의 인스턴스를 생성할 수 있습니다:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

이렇게 하면 `checker.fixed_content` 속성에 `"bar"`라는 값을 담아 의존성을 "매개변수화"할 수 있습니다.

## 인스턴스를 의존성으로 사용하기 { #use-the-instance-as-a-dependency }

그런 다음, 클래스 자체가 아닌 인스턴스 `checker`가 의존성이 되므로, `Depends(FixedContentQueryChecker)` 대신 `Depends(checker)`에서 이 `checker` 인스턴스를 사용할 수 있습니다.

의존성을 해결할 때 **FastAPI**는 이 `checker`를 다음과 같이 호출합니다:

```Python
checker(q="somequery")
```

...그리고 이때 반환되는 값을 *경로 처리 함수*의 의존성 값으로, `fixed_content_included` 매개변수에 전달합니다:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip | 팁

이 모든 과정이 복잡하게 느껴질 수 있습니다. 그리고 지금은 이 방법이 얼마나 유용한지 명확하지 않을 수도 있습니다.

이 예시는 의도적으로 간단하게 만들었지만, 전체 구조가 어떻게 작동하는지 보여줍니다.

보안 관련 장에서는 이와 같은 방식으로 구현된 유틸리티 함수들이 있습니다.

이 모든 과정을 이해했다면, 이러한 보안용 유틸리티 도구들이 내부적으로 어떻게 작동하는지 이미 파악한 것입니다.

///

## `yield`, `HTTPException`, `except`, 백그라운드 태스크가 있는 의존성 { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | 경고

대부분의 경우 이러한 기술 세부사항이 필요하지 않을 것입니다.

이 세부사항은 주로 0.121.0 이전의 FastAPI 애플리케이션이 있고 `yield`가 있는 의존성에서 문제가 발생하는 경우에 유용합니다.

///

`yield`가 있는 의존성은 여러 사용 사례를 수용하고 일부 문제를 해결하기 위해 시간이 지나며 발전해 왔습니다. 다음은 변경된 내용의 요약입니다.

### `yield`와 `scope`가 있는 의존성 { #dependencies-with-yield-and-scope }

0.121.0 버전에서 FastAPI는 `yield`가 있는 의존성에 대해 `Depends(scope="function")` 지원을 추가했습니다.

`Depends(scope="function")`를 사용하면, `yield` 이후의 종료 코드는 *경로 처리 함수*가 끝난 직후(클라이언트에 응답이 반환되기 전)에 실행됩니다.

그리고 `Depends(scope="request")`(기본값)를 사용하면, `yield` 이후의 종료 코드는 응답이 전송된 후에 실행됩니다.

자세한 내용은 [Dependencies with `yield` - Early exit and `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) 문서를 참고하세요.

### `yield`가 있는 의존성과 `StreamingResponse`, 기술 세부사항 { #dependencies-with-yield-and-streamingresponse-technical-details }

FastAPI 0.118.0 이전에는 `yield`가 있는 의존성을 사용하면, *경로 처리 함수*가 반환된 뒤 응답을 보내기 직전에 `yield` 이후의 종료 코드가 실행되었습니다.

의도는 응답이 네트워크를 통해 전달되기를 기다리면서 필요한 것보다 더 오래 리소스를 점유하지 않도록 하는 것이었습니다.

이 변경은 `StreamingResponse`를 반환하는 경우에도 `yield`가 있는 의존성의 종료 코드가 이미 실행된다는 의미이기도 했습니다.

예를 들어, `yield`가 있는 의존성에 데이터베이스 세션이 있다면, `StreamingResponse`는 데이터를 스트리밍하는 동안 해당 세션을 사용할 수 없게 됩니다. `yield` 이후의 종료 코드에서 세션이 이미 닫혔기 때문입니다.

이 동작은 0.118.0에서 되돌려져, `yield` 이후의 종료 코드가 응답이 전송된 뒤 실행되도록 변경되었습니다.

/// info | 정보

아래에서 보시겠지만, 이는 0.106.0 버전 이전의 동작과 매우 비슷하지만, 여러 개선 사항과 코너 케이스에 대한 버그 수정이 포함되어 있습니다.

///

#### 종료 코드를 조기에 실행하는 사용 사례 { #use-cases-with-early-exit-code }

특정 조건의 일부 사용 사례에서는 응답을 보내기 전에 `yield`가 있는 의존성의 종료 코드를 실행하던 예전 동작이 도움이 될 수 있습니다.

예를 들어, `yield`가 있는 의존성에서 데이터베이스 세션을 사용해 사용자를 검증만 하고, *경로 처리 함수*에서는 그 데이터베이스 세션을 다시는 사용하지 않으며(의존성에서만 사용), **그리고** 응답을 전송하는 데 오랜 시간이 걸리는 경우를 생각해 봅시다. 예를 들어 데이터를 천천히 보내는 `StreamingResponse`인데, 어떤 이유로든 데이터베이스를 사용하지는 않는 경우입니다.

이 경우 데이터베이스 세션은 응답 전송이 끝날 때까지 유지되지만, 사용하지 않는다면 굳이 유지할 필요가 없습니다.

다음과 같이 보일 수 있습니다:

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

다음에서 `Session`을 자동으로 닫는 종료 코드는:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...응답이 느린 데이터 전송을 마친 뒤에 실행됩니다:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

하지만 `generate_stream()`는 데이터베이스 세션을 사용하지 않으므로, 응답을 전송하는 동안 세션을 열린 채로 유지할 필요는 없습니다.

SQLModel(또는 SQLAlchemy)을 사용하면서 이런 특정 사용 사례가 있다면, 더 이상 필요하지 않을 때 세션을 명시적으로 닫을 수 있습니다:

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

그러면 세션이 데이터베이스 연결을 해제하여, 다른 요청들이 이를 사용할 수 있게 됩니다.

`yield`가 있는 의존성에서 조기 종료가 필요한 다른 사용 사례가 있다면, 여러분의 구체적인 사용 사례와 `yield`가 있는 의존성에 대한 조기 종료가 어떤 점에서 이득이 되는지를 포함해 <a href="https://github.com/fastapi/fastapi/discussions/new?category=questions" class="external-link" target="_blank">GitHub Discussion Question</a>을 생성해 주세요.

`yield`가 있는 의존성에서 조기 종료에 대한 설득력 있는 사용 사례가 있다면, 조기 종료를 선택적으로 활성화할 수 있는 새로운 방법을 추가하는 것을 고려하겠습니다.

### `yield`가 있는 의존성과 `except`, 기술 세부사항 { #dependencies-with-yield-and-except-technical-details }

FastAPI 0.110.0 이전에는 `yield`가 있는 의존성을 사용한 다음 그 의존성에서 `except`로 예외를 잡고, 예외를 다시 발생시키지 않으면, 예외가 자동으로 어떤 예외 핸들러 또는 내부 서버 오류 핸들러로 raise/forward 되었습니다.

이는 핸들러 없이 전달된 예외(내부 서버 오류)로 인해 처리되지 않은 메모리 사용이 발생하는 문제를 수정하고, 일반적인 Python 코드의 동작과 일관되게 하기 위해 0.110.0 버전에서 변경되었습니다.

### 백그라운드 태스크와 `yield`가 있는 의존성, 기술 세부사항 { #background-tasks-and-dependencies-with-yield-technical-details }

FastAPI 0.106.0 이전에는 `yield` 이후에 예외를 발생시키는 것이 불가능했습니다. `yield`가 있는 의존성의 종료 코드는 응답이 전송된 *후에* 실행되었기 때문에, [Exception Handlers](../tutorial/handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank}가 이미 실행된 뒤였습니다.

이는 주로 백그라운드 태스크 안에서 의존성이 "yield"한 동일한 객체들을 사용할 수 있게 하기 위한 설계였습니다. 백그라운드 태스크가 끝난 뒤에 종료 코드가 실행되었기 때문입니다.

이는 응답이 네트워크를 통해 전달되기를 기다리는 동안 리소스를 점유하지 않기 위한 의도로 FastAPI 0.106.0에서 변경되었습니다.

/// tip | 팁

추가로, 백그라운드 태스크는 보통 별도의 리소스(예: 자체 데이터베이스 연결)를 가지고 따로 처리되어야 하는 독립적인 로직 집합입니다.

따라서 이 방식이 코드를 더 깔끔하게 만들어줄 가능성이 큽니다.

///

이 동작에 의존하던 경우라면, 이제는 백그라운드 태스크를 위한 리소스를 백그라운드 태스크 내부에서 생성하고, 내부적으로는 `yield`가 있는 의존성의 리소스에 의존하지 않는 데이터만 사용해야 합니다.

예를 들어, 동일한 데이터베이스 세션을 사용하는 대신, 백그라운드 태스크 내부에서 새 데이터베이스 세션을 생성하고, 이 새 세션을 사용해 데이터베이스에서 객체를 가져오면 됩니다. 그리고 데이터베이스에서 가져온 객체를 백그라운드 태스크 함수의 매개변수로 전달하는 대신, 해당 객체의 ID를 전달한 다음 백그라운드 태스크 함수 내부에서 객체를 다시 가져오면 됩니다.
