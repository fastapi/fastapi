# 使用 yield 的依赖项 { #dependencies-with-yield }

FastAPI 支持在完成后执行一些<abbr title='有时也被称为"退出代码"（"exit code"）、"清理代码"（"cleanup code"）、"拆卸代码"（"teardown code"）、"关闭代码"（"closing code"）、"上下文管理器退出代码"（"context manager exit code"）等。'>完成后的额外步骤</abbr>的依赖项。

为此，使用 `yield` 而不是 `return`，并在后面编写这些额外的步骤（代码）。

/// tip | 提示

确保每个依赖只使用一次 `yield`。

///

/// note | 技术细节

任何一个可以与以下内容一起使用的函数：

* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager" class="external-link" target="_blank">`@contextlib.contextmanager`</a> 或者
* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager" class="external-link" target="_blank">`@contextlib.asynccontextmanager`</a>

都可以作为 **FastAPI** 的依赖项。

实际上，FastAPI 内部就使用了这两个装饰器。

///

## 使用 `yield` 的数据库依赖项 { #a-database-dependency-with-yield }

例如，你可以用它来创建一个数据库 session，并在完成后关闭它。

在创建响应之前，只会执行 `yield` 语句及之前的代码：

{* ../../docs_src/dependencies/tutorial007_py39.py hl[2:4] *}

`yield` 出来的值会注入到*路径操作*和其他依赖项中：

{* ../../docs_src/dependencies/tutorial007_py39.py hl[4] *}

`yield` 语句后面的代码会在响应之后执行：

{* ../../docs_src/dependencies/tutorial007_py39.py hl[5:6] *}

/// tip | 提示

你可以使用 `async` 或普通函数。

**FastAPI** 会像处理普通依赖一样，对每个依赖做正确的处理。

///

## 包含 `yield` 和 `try` 的依赖项 { #a-dependency-with-yield-and-try }

如果你在包含 `yield` 的依赖中使用 `try` 代码块，你会接收到在使用该依赖时抛出的任何异常。

例如，如果在中途某段代码（在另一个依赖中或在某个*路径操作*中）让数据库事务“回滚”，或创建了任何其他异常，你都会在你的依赖中接收到该异常。

因此，你可以在依赖中使用 `except SomeException` 来查找那个特定的异常。

同样，你也可以使用 `finally` 来确保退出步骤得到执行，无论是否存在异常。

{* ../../docs_src/dependencies/tutorial007_py39.py hl[3,5] *}

## 使用 `yield` 的子依赖项 { #sub-dependencies-with-yield }

你可以声明任意大小和形状的子依赖项以及子依赖树，它们中的任意一个或全部都可以使用 `yield`。

**FastAPI** 会确保每个带有 `yield` 的依赖中的“退出代码”按正确顺序运行。

例如，`dependency_c` 可以依赖于 `dependency_b`，而 `dependency_b` 则依赖于 `dependency_a`：

{* ../../docs_src/dependencies/tutorial008_an_py39.py hl[6,14,22] *}

并且它们都可以使用 `yield`。

在这种情况下，`dependency_c` 在执行其退出代码时，需要 `dependency_b`（此处名为 `dep_b`）的值仍然可用。

而 `dependency_b` 反过来则需要 `dependency_a`（此处名为 `dep_a`）的值在其退出代码中可用。

{* ../../docs_src/dependencies/tutorial008_an_py39.py hl[18:19,26:27] *}

同样，你可以让一些依赖使用 `yield`，另一些依赖使用 `return`，并让其中一些依赖于另一些。

你也可以声明一个依赖，它需要多个带有 `yield` 的依赖，等等。

你可以组合出任何你想要的依赖。

**FastAPI** 会确保所有内容都按正确的顺序运行。

/// note | 技术细节

这得益于 Python 的 <a href="https://docs.python.org/3/library/contextlib.html" class="external-link" target="_blank">Context Managers</a>。

**FastAPI** 在内部使用它们来实现这一点。

///

## 包含 `yield` 和 `HTTPException` 的依赖项 { #dependencies-with-yield-and-httpexception }

你已经看到，你可以使用带有 `yield` 的依赖，并在 `try` 代码块中尝试执行一些代码，然后在 `finally` 之后运行一些退出代码。

你也可以使用 `except` 来捕获被抛出的异常，并对其做一些处理。

例如，你可以抛出另一个异常，比如 `HTTPException`。

/// tip | 提示

这是一种相对高级的技巧，在大多数情况下你并不需要使用它，因为你可以在应用的其他代码中抛出异常（包括 `HTTPException`），例如在*路径操作函数*中。

但如果你需要，它就在这里。🤓

///

{* ../../docs_src/dependencies/tutorial008b_an_py39.py hl[18:22,31] *}

如果你想捕获异常并基于此创建一个自定义响应，请创建一个[自定义异常处理器](../handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank}。

## 包含 `yield` 和 `except` 的依赖项 { #dependencies-with-yield-and-except }

如果你在包含 `yield` 的依赖项中使用 `except` 捕获了一个异常，然后你没有再次抛出该异常（或抛出一个新异常），与普通的 Python 一样，FastAPI 将无法注意到发生了异常：

{* ../../docs_src/dependencies/tutorial008c_an_py39.py hl[15:16] *}

在这种情况下，客户端会看到一个 *HTTP 500 Internal Server Error* 响应（因为我们没有抛出 `HTTPException` 或类似异常），但服务器将**不会有任何日志**或其他提示来告诉我们错误是什么。😱

### 在包含 `yield` 和 `except` 的依赖项中始终 `raise` { #always-raise-in-dependencies-with-yield-and-except }

如果你在带有 `yield` 的依赖项中捕获了异常，除非你要抛出另一个 `HTTPException` 或类似异常，**你应该重新抛出原始异常**。

你可以使用 `raise` 重新抛出同一个异常：

{* ../../docs_src/dependencies/tutorial008d_an_py39.py hl[17] *}

现在客户端会得到相同的 *HTTP 500 Internal Server Error* 响应，但服务器日志中会包含我们自定义的 `InternalError`。😎

## 使用 `yield` 的依赖项的执行 { #execution-of-dependencies-with-yield }

执行顺序大致如下图所示。时间从上到下流动，每一列代表交互的一部分或代码执行的一部分。

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

/// info | 信息

只会向客户端发送**一次响应**。它可能是某个错误响应，也可能是来自*路径操作*的响应。

在发送了其中一个响应之后，就无法再发送其他响应了。

///

/// tip | 提示

如果你在*路径操作函数*的代码中抛出任何异常，它都会被传递给带有 yield 的依赖项，包括 `HTTPException`。在大多数情况下，你会希望从带有 `yield` 的依赖项中重新抛出同一个异常或一个新异常，以确保它能被正确处理。

///

## 提前退出与 `scope` { #early-exit-and-scope }

通常，带有 `yield` 的依赖项的退出代码会在**响应**发送给客户端**之后**执行。

但如果你知道从*路径操作函数*返回后就不再需要使用该依赖，你可以使用 `Depends(scope="function")` 来告诉 FastAPI：应该在*路径操作函数*返回之后关闭该依赖，但要在**响应发送之前**关闭。

{* ../../docs_src/dependencies/tutorial008e_an_py39.py hl[12,16] *}

`Depends()` 接收一个 `scope` 参数，可以是：

* `"function"`：在处理请求的*路径操作函数*之前启动依赖，在*路径操作函数*结束后结束依赖，但要在响应发送回客户端**之前**结束。因此，依赖函数会在*路径操作函数*前后被执行。
* `"request"`：在处理请求的*路径操作函数*之前启动依赖（与使用 `"function"` 时类似），但在响应发送回客户端**之后**结束。因此，依赖函数会围绕整个**请求**与响应周期执行。

如果未指定，并且依赖使用了 `yield`，则其默认 `scope` 为 `"request"`。

### 子依赖项的 `scope` { #scope-for-sub-dependencies }

当你声明一个 `scope="request"`（默认）的依赖时，任何子依赖项也需要有 `"request"` 的 `scope`。

但 `scope` 为 `"function"` 的依赖可以依赖 `scope` 为 `"function"` 和 `"request"` 的依赖。

这是因为任何依赖都需要能够在子依赖项之前运行它的退出代码，因为它可能在退出代码中仍需要使用子依赖项。

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

## 包含 `yield`、`HTTPException`、`except` 和后台任务的依赖项 { #dependencies-with-yield-httpexception-except-and-background-tasks }

带有 `yield` 的依赖项随着时间推移不断演进，以覆盖不同的用例并修复一些问题。

如果你想了解 FastAPI 不同版本中有哪些变化，可以在高级指南中阅读更多内容：[高级依赖项 - 包含 `yield`、`HTTPException`、`except` 和后台任务的依赖项](../../advanced/advanced-dependencies.md#dependencies-with-yield-httpexception-except-and-background-tasks){.internal-link target=_blank}。

## 上下文管理器 { #context-managers }

### 什么是“上下文管理器” { #what-are-context-managers }

“上下文管理器”是你可以在 `with` 语句中使用的那些 Python 对象。

例如，<a href="https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files" class="external-link" target="_blank">你可以使用 `with` 来读取文件</a>：

```Python
with open("./somefile.txt") as f:
    contents = f.read()
    print(contents)
```

在底层，`open("./somefile.txt")` 会创建一个称为“上下文管理器”的对象。

当 `with` 代码块结束时，它会确保关闭文件，即使发生了异常也是如此。

当你使用 `yield` 创建一个依赖项时，**FastAPI** 会在内部为它创建一个上下文管理器，并与其他相关工具结合使用。

### 在使用 `yield` 的依赖项中使用上下文管理器 { #using-context-managers-in-dependencies-with-yield }

/// warning | 警告

这大概算是一个“高级”的想法。

如果你刚开始使用 **FastAPI**，你可能想先跳过它。

///

在 Python 中，你可以通过<a href="https://docs.python.org/3/reference/datamodel.html#context-managers" class="external-link" target="_blank">创建一个包含两个方法：`__enter__()` 和 `__exit__()` 的类</a>来创建上下文管理器。

你也可以在 **FastAPI** 的带有 `yield` 的依赖项中使用它们，在依赖函数内部使用
`with` 或 `async with` 语句：

{* ../../docs_src/dependencies/tutorial010_py39.py hl[1:9,13] *}

/// tip | 提示

另一种创建上下文管理器的方法是：

* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager" class="external-link" target="_blank">`@contextlib.contextmanager`</a> 或者
* <a href="https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager" class="external-link" target="_blank">`@contextlib.asynccontextmanager`</a>

用它们去装饰一个只包含单个 `yield` 的函数。

这正是 **FastAPI** 在内部对带有 `yield` 的依赖项所使用的方式。

但你不必（也不应该）为 FastAPI 的依赖项使用这些装饰器。

FastAPI 会在内部为你处理。

///
