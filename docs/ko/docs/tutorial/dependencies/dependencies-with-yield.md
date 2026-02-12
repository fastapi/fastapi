# `yield`를 사용하는 의존성 { #dependencies-with-yield }

FastAPI는 <abbr title='sometimes also called "exit code", "cleanup code", "teardown code", "closing code", "context manager exit code", etc. – 때로는 "exit code", "cleanup code", "teardown code", "closing code", "context manager exit code" 등으로도 불립니다'>작업 완료 후 추가 단계를 수행하는</abbr> 의존성을 지원합니다.

이를 구현하려면 `return` 대신 `yield`를 사용하고, 추가로 실행할 단계 (코드)를 그 뒤에 작성하세요.

/// tip | 팁

각 의존성마다 `yield`는 한 번만 사용해야 합니다.

///

/// note | 기술 세부사항

다음과 함께 사용할 수 있는 모든 함수:

* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager" class="external-link" target="_blank">`@contextlib.contextmanager`</a> 또는
* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager" class="external-link" target="_blank">`@contextlib.asynccontextmanager`</a>

는 **FastAPI**의 의존성으로 사용할 수 있습니다.

사실, FastAPI는 내부적으로 이 두 데코레이터를 사용합니다.

///

## `yield`를 사용하는 데이터베이스 의존성 { #a-database-dependency-with-yield }

예를 들어, 이 기능을 사용하면 데이터베이스 세션을 생성하고 작업이 끝난 후에 세션을 종료할 수 있습니다.

응답을 생성하기 전에는 `yield`문을 포함하여 그 이전의 코드만이 실행됩니다:

{* ../../docs_src/dependencies/tutorial007_py39.py hl[2:4] *}

yield된 값은 *경로 처리* 및 다른 의존성들에 주입되는 값 입니다:

{* ../../docs_src/dependencies/tutorial007_py39.py hl[4] *}

`yield`문 다음의 코드는 응답을 생성한 후 실행됩니다:

{* ../../docs_src/dependencies/tutorial007_py39.py hl[5:6] *}

/// tip | 팁

`async` 함수와 일반 함수 모두 사용할 수 있습니다.

**FastAPI**는 일반 의존성과 마찬가지로 각각의 함수를 올바르게 처리할 것입니다.

///

## `yield`와 `try`를 사용하는 의존성 { #a-dependency-with-yield-and-try }

`yield`를 사용하는 의존성에서 `try` 블록을 사용한다면, 의존성을 사용하는 도중 발생한 모든 예외를 받을 수 있습니다.

예를 들어, 다른 의존성이나 *경로 처리*의 중간에 데이터베이스 트랜잭션 "롤백"이 발생하거나 다른 오류가 발생한다면, 해당 예외를 의존성에서 받을 수 있습니다.

따라서, 의존성 내에서 `except SomeException`을 사용하여 특정 예외를 처리할 수 있습니다.

마찬가지로, `finally`를 사용하여 예외 발생 여부와 관계 없이 종료 단계까 실행되도록 할 수 있습니다.

{* ../../docs_src/dependencies/tutorial007_py39.py hl[3,5] *}

## `yield`를 사용하는 하위 의존성 { #sub-dependencies-with-yield }

모든 크기와 형태의 하위 의존성과 하위 의존성의 "트리"도 가질 수 있으며, 이들 모두가 `yield`를 사용할 수 있습니다.

**FastAPI**는 `yield`를 사용하는 각 의존성의 "종료 코드"가 올바른 순서로 실행되도록 보장합니다.

예를 들어, `dependency_c`는 `dependency_b`에 의존할 수 있고, `dependency_b`는 `dependency_a`에 의존할 수 있습니다.

{* ../../docs_src/dependencies/tutorial008_an_py39.py hl[6,14,22] *}

이들 모두는 `yield`를 사용할 수 있습니다.

이 경우 `dependency_c`는 종료 코드를 실행하기 위해, `dependency_b`의 값 (여기서는 `dep_b`로 명명)이 여전히 사용 가능해야 합니다.

그리고, `dependency_b`는 종료 코드를 위해 `dependency_a`의 값 (여기서는 `dep_a`로 명명) 이 사용 가능해야 합니다.

{* ../../docs_src/dependencies/tutorial008_an_py39.py hl[18:19,26:27] *}

같은 방식으로, `yield`를 사용하는 의존성과 `return`을 사용하는 의존성을 함께 사용할 수 있으며, 이들 중 일부가 다른 것들에 의존할 수 있습니다.

그리고 `yield`를 사용하는 다른 여러 의존성을 필요로 하는 단일 의존성을 가질 수도 있습니다.

원하는 의존성을 원하는 대로 조합할 수 있습니다.

**FastAPI**는 모든 것이 올바른 순서로 실행되도록 보장합니다.

/// note | 기술 세부사항

파이썬의 <a href="https://docs.python.org/3/library/contextlib.html" class="external-link" target="_blank">Context Managers</a> 덕분에 이 기능이 작동합니다.

**FastAPI**는 이를 내부적으로 사용하여 이를 달성합니다.

///

## `yield`와 `HTTPException`를 사용하는 의존성 { #dependencies-with-yield-and-httpexception }

`yield`를 사용하는 의존성에서 `try` 블록을 사용해 코드를 실행하고, 그 다음 `finally` 뒤에 종료 코드를 실행할 수 있다는 것을 보았습니다.

또한 `except`를 사용해 발생한 예외를 잡고 그에 대해 무언가를 할 수도 있습니다.

예를 들어, `HTTPException` 같은 다른 예외를 발생시킬 수 있습니다.

/// tip | 팁

이는 다소 고급 기술이며, 대부분의 경우 실제로는 필요하지 않을 것입니다. 예를 들어, *경로 처리 함수* 등 나머지 애플리케이션 코드 내부에서 예외 (`HTTPException` 포함)를 발생시킬 수 있기 때문입니다.

하지만 필요한 경우 사용할 수 있습니다. 🤓

///

{* ../../docs_src/dependencies/tutorial008b_an_py39.py hl[18:22,31] *}

예외를 잡고 그에 기반해 사용자 정의 응답을 생성하려면, [사용자 정의 예외 처리기](../handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank}를 생성하세요.

## `yield`와 `except`를 사용하는 의존성 { #dependencies-with-yield-and-except }

`yield`를 사용하는 의존성에서 `except`를 사용하여 예외를 포착하고 예외를 다시 발생시키지 않거나 (또는 새 예외를 발생시키지 않으면), FastAPI는 일반적인 Python에서와 마찬가지로 예외가 있었다는 것을 알아차릴 수 없습니다:

{* ../../docs_src/dependencies/tutorial008c_an_py39.py hl[15:16] *}

이 경우, `HTTPException`이나 유사한 예외를 발생시키지 않기 때문에 클라이언트는 마땅히 *HTTP 500 Internal Server Error* 응답을 보게 되지만, 서버에는 어떤 오류였는지에 대한 **로그**나 다른 표시가 **전혀 남지 않게 됩니다**. 😱

### `yield`와 `except`를 사용하는 의존성에서 항상 `raise` 하기 { #always-raise-in-dependencies-with-yield-and-except }

`yield`가 있는 의존성에서 예외를 잡았을 때, 다른 `HTTPException`이나 유사한 예외를 발생시키는 것이 아니라면, **원래 예외를 다시 발생시켜야 합니다**.

`raise`를 사용하여 동일한 예외를 다시 발생시킬 수 있습니다:

{* ../../docs_src/dependencies/tutorial008d_an_py39.py hl[17] *}

이제 클라이언트는 동일한 *HTTP 500 Internal Server Error* 응답을 받게 되지만, 서버 로그에는 사용자 정의 `InternalError`가 기록됩니다. 😎

## `yield`를 사용하는 의존성의 실행 순서 { #execution-of-dependencies-with-yield }

실행 순서는 아래 다이어그램과 거의 비슷합니다. 시간은 위에서 아래로 흐릅니다. 그리고 각 열은 상호 작용하거나 코드를 실행하는 부분 중 하나입니다.

```mermaid
sequenceDiagram

participant client as Client
participant handler as Exception handler
participant dep as Dep with yield
participant operation as Path Operation
participant tasks as Background tasks

    Note over client,operation: Can raise exceptions, including HTTPException
    client ->> dep: Start request
    Note over dep: Run code up to yield
    opt raise Exception
        dep -->> handler: Raise Exception
        handler -->> client: HTTP error response
    end
    dep ->> operation: Run dependency, e.g. DB session
    opt raise
        operation -->> dep: Raise Exception (e.g. HTTPException)
        opt handle
            dep -->> dep: Can catch exception, raise a new HTTPException, raise other exception
        end
        handler -->> client: HTTP error response
    end

    operation ->> client: Return response to client
    Note over client,operation: Response is already sent, can't change it anymore
    opt Tasks
        operation -->> tasks: Send background tasks
    end
    opt Raise other exception
        tasks -->> tasks: Handle exceptions in the background task code
    end
```

/// info | 정보

클라이언트에는 **하나의 응답**만 전송됩니다. 이는 오류 응답 중 하나일 수도 있고, *경로 처리*에서 생성된 응답일 수도 있습니다.

이러한 응답 중 하나가 전송된 후에는 다른 응답을 보낼 수 없습니다.

///

/// tip | 팁

*경로 처리 함수*의 코드에서 어떤 예외를 발생시키면 `HTTPException`을 포함해 `yield`를 사용하는 의존성으로 전달됩니다. 대부분의 경우 해당 예외(또는 새 예외)를 `yield`를 사용하는 의존성에서 다시 발생시켜, 제대로 처리되도록 해야 합니다.

///

## 조기 종료와 `scope` { #early-exit-and-scope }

일반적으로 `yield`를 사용하는 의존성의 종료 코드는 클라이언트로 **응답이 전송된 후에** 실행됩니다.

하지만 *경로 처리 함수*에서 반환한 뒤에는 더 이상 해당 의존성이 필요 없다는 것을 알고 있다면, `Depends(scope="function")`을 사용하여 FastAPI에 *경로 처리 함수*가 반환된 후, 하지만 **응답이 전송되기 전에** 의존성을 종료(닫기)해야 한다고 알려줄 수 있습니다.

{* ../../docs_src/dependencies/tutorial008e_an_py39.py hl[12,16] *}

`Depends()`는 다음이 될 수 있는 `scope` 매개변수를 받습니다:

* `"function"`: 요청을 처리하는 *경로 처리 함수* 전에 의존성을 시작하고, *경로 처리 함수*가 끝난 후, 하지만 응답이 클라이언트로 전송되기 **전에** 의존성을 종료합니다. 즉, 의존성 함수는 *경로 처리 **함수***를 **둘러싸며** 실행됩니다.
* `"request"`: 요청을 처리하는 *경로 처리 함수* 전에 의존성을 시작하고(`"function"`을 사용할 때와 유사), 응답이 클라이언트로 전송된 **후에** 종료합니다. 즉, 의존성 함수는 **요청**과 응답 사이클을 **둘러싸며** 실행됩니다.

지정하지 않고 의존성이 `yield`를 사용한다면, 기본 `scope`는 `"request"`입니다.

### 하위 의존성을 위한 `scope` { #scope-for-sub-dependencies }

`scope="request"`(기본값)로 의존성을 선언하면, 모든 하위 의존성도 `scope`가 `"request"`여야 합니다.

하지만 `scope`가 `"function"`인 의존성은 `scope`가 `"function"`인 의존성과 `"request"`인 의존성을 모두 의존성으로 가질 수 있습니다.

이는 어떤 의존성이든, 종료 코드에서 하위 의존성을 계속 사용해야 할 수도 있으므로, 하위 의존성보다 먼저 종료 코드를 실행할 수 있어야 하기 때문입니다.

```mermaid
sequenceDiagram

participant client as Client
participant dep_req as Dep scope="request"
participant dep_func as Dep scope="function"
participant operation as Path Operation

    client ->> dep_req: Start request
    Note over dep_req: Run code up to yield
    dep_req ->> dep_func: Pass dependency
    Note over dep_func: Run code up to yield
    dep_func ->> operation: Run path operation with dependency
    operation ->> dep_func: Return from path operation
    Note over dep_func: Run code after yield
    Note over dep_func: ✅ Dependency closed
    dep_func ->> client: Send response to client
    Note over client: Response sent
    Note over dep_req: Run code after yield
    Note over dep_req: ✅ Dependency closed
```

## `yield`, `HTTPException`, `except` 및 백그라운드 작업을 사용하는 의존성 { #dependencies-with-yield-httpexception-except-and-background-tasks }

`yield`를 사용하는 의존성은 시간이 지나면서 서로 다른 사용 사례를 다루고 일부 문제를 수정하기 위해 발전해 왔습니다.

FastAPI의 여러 버전에서 무엇이 바뀌었는지 보고 싶다면, 고급 가이드의 [고급 의존성 - `yield`, `HTTPException`, `except` 및 백그라운드 작업을 사용하는 의존성](../../advanced/advanced-dependencies.md#dependencies-with-yield-httpexception-except-and-background-tasks){.internal-link target=_blank}에서 더 자세히 읽을 수 있습니다.
## 컨텍스트 관리자 { #context-managers }

### "컨텍스트 관리자"란 { #what-are-context-managers }

"컨텍스트 관리자"는 Python에서 `with` 문에서 사용할 수 있는 모든 객체를 의미합니다.

예를 들어, <a href="https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files" class="external-link" target="_blank">`with`를 사용하여 파일을 읽을 수 있습니다</a>:

```Python
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
```

내부적으로 `open("./somefile.txt")` 는 "컨텍스트 관리자(Context Manager)"라고 불리는 객체를 생성합니다.

`with` 블록이 끝나면, 예외가 발생했더라도 파일을 닫도록 보장합니다.

`yield`가 있는 의존성을 생성하면 **FastAPI**는 내부적으로 이를 위한 컨텍스트 매니저를 생성하고 다른 관련 도구들과 결합합니다.

### `yield`를 사용하는 의존성에서 컨텍스트 관리자 사용하기 { #using-context-managers-in-dependencies-with-yield }

/// warning | 경고

이것은 어느 정도 "고급" 개념입니다.

**FastAPI**를 처음 시작하는 경우 지금은 이 부분을 건너뛰어도 좋습니다.

///

Python에서는 다음을 통해 컨텍스트 관리자를 생성할 수 있습니다. <a href="https://docs.python.org/3/reference/datamodel.html#context-managers" class="external-link" target="_blank"> 두 가지 메서드가 있는 클래스를 생성합니다: `__enter__()` and `__exit__()`</a>.

**FastAPI**의 `yield`가 있는 의존성 내에서
`with` 또는 `async with`문을 사용하여 이들을 활용할 수 있습니다:

{* ../../docs_src/dependencies/tutorial010_py39.py hl[1:9,13] *}

/// tip | 팁

컨텍스트 관리자를 생성하는 또 다른 방법은 다음과 같습니다:

* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager" class="external-link" target="_blank">`@contextlib.contextmanager`</a> 또는
* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager" class="external-link" target="_blank">`@contextlib.asynccontextmanager`</a>

이들은 단일 `yield`가 있는 함수를 꾸미는 데 사용합니다.

이것이 **FastAPI**가 `yield`가 있는 의존성을 위해 내부적으로 사용하는 방식입니다.

하지만 FastAPI 의존성에는 이러한 데코레이터를 사용할 필요가 없습니다(그리고 사용해서도 안됩니다).

FastAPI가 내부적으로 이를 처리해 줄 것입니다.

///
