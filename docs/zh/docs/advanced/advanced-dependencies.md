# 高级依赖项 { #advanced-dependencies }

## 参数化的依赖项 { #parameterized-dependencies }

我们之前看到的所有依赖项都是写死的函数或类。

但也可以在某些情况下为依赖项设置参数，而无需声明许多不同的函数或类。

假设要创建一个依赖项，用来检查查询参数 `q` 是否包含某些固定内容。

但我们希望能够对该固定内容进行参数化。

## **可调用**实例 { #a-callable-instance }

Python 可以把类实例变为“可调用项”。

这里说的不是类本身（类本就是可调用项），而是该类的实例。

为此，需要声明 `__call__` 方法：

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

在本例中，这个 `__call__` 将被 **FastAPI** 用来检查额外参数和子依赖项，并且稍后将被调用，把一个值传递给你的*路径操作函数*中的参数。

## 参数化实例 { #parameterize-the-instance }

接下来，我们可以使用 `__init__` 来声明实例的参数，用于“参数化”依赖项：

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

在这个例子中，**FastAPI** 不会触碰或关心 `__init__`，我们会在代码中直接使用它。

## 创建实例 { #create-an-instance }

我们可以用下面的方式创建该类的实例：

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

这样我们就能“参数化”依赖项，它现在包含 `"bar"`，作为属性 `checker.fixed_content`。

## 把实例作为依赖项 { #use-the-instance-as-a-dependency }

然后，我们可以在 `Depends(checker)` 中使用这个 `checker`，而不是 `Depends(FixedContentQueryChecker)`，因为依赖项是实例 `checker`，不是类本身。

处理依赖项时，**FastAPI** 会像这样调用 `checker`：

```Python
checker(q="somequery")
```

...并将其返回值作为依赖项的值，传递给我们的*路径操作函数*，对应参数 `fixed_content_included`：

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip | 提示

本章示例可能看起来有些刻意，而且目前还不太清楚有什么用处。

这些示例刻意保持简单，但展示了它是如何工作的。

在有关安全的章节中，有一些工具函数就是以同样的方式实现的。

如果你理解了这些内容，你就已经知道那些安全工具在底层是如何工作的。

///

## 带有 `yield`、`HTTPException`、`except` 以及 Background Tasks 的依赖项 { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | 警告

你很可能不需要这些技术细节。

这些细节主要在以下场景有用：如果你有一个早于 0.121.0 的 FastAPI 应用，并且你正遇到与带有 `yield` 的依赖项相关的问题。

///

带有 `yield` 的依赖项随着时间推移不断演进，以覆盖不同用例并修复一些问题。下面是变更总结。

### 带有 `yield` 和 `scope` 的依赖项 { #dependencies-with-yield-and-scope }

在 0.121.0 版本中，FastAPI 为带有 `yield` 的依赖项添加了对 `Depends(scope="function")` 的支持。

使用 `Depends(scope="function")` 时，`yield` 之后的退出代码会在*路径操作函数*结束后立刻执行，并且是在响应发送回客户端之前。

而当使用 `Depends(scope="request")`（默认值）时，`yield` 之后的退出代码会在响应发送之后执行。

你可以在文档中阅读更多：[带有 `yield` 的依赖项 - 提前退出与 `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope)。

### 带有 `yield` 和 `StreamingResponse` 的依赖项，技术细节 { #dependencies-with-yield-and-streamingresponse-technical-details }

在 FastAPI 0.118.0 之前，如果你使用了带有 `yield` 的依赖项，它会在*路径操作函数*返回之后、但在发送响应之前运行退出代码。

其目的是避免在等待响应通过网络传输时，资源被持有超过必要的时间。

但这个改动也意味着：如果你返回的是 `StreamingResponse`，那么带有 `yield` 的依赖项的退出代码会已经执行过了。

例如，如果你在一个带有 `yield` 的依赖项中创建了数据库 session，那么在流式传输数据时，`StreamingResponse` 将无法使用该 session，因为该 session 已经在 `yield` 之后的退出代码中被关闭了。

在 0.118.0 中，这种行为被回滚，使得 `yield` 之后的退出代码在响应发送之后执行。

/// info | 信息

如你将在下文看到的，这与 0.106.0 之前的行为非常类似，但针对边界情况做了多项改进与 bug 修复。

///

#### 提前执行退出代码的用例 { #use-cases-with-early-exit-code }

对于某些特定条件下的用例，在发送响应之前运行带有 `yield` 的依赖项退出代码（旧行为）可能会有好处。

例如，设想你有一段代码，在带有 `yield` 的依赖项中使用数据库 session 仅用于验证用户，但在*路径操作函数*中不再使用该数据库 session，只在依赖项中使用；并且响应发送需要很长时间，比如一个慢速发送数据的 `StreamingResponse`，但由于某些原因并不使用数据库。

在这种情况下，数据库 session 会一直被持有，直到响应发送完毕。但如果你不再使用它，那么其实没必要一直持有它。

它可能长这样：

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

退出代码，也就是在这里自动关闭 `Session` 的部分：

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...会在响应把慢速数据发送完之后才运行：

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

但由于 `generate_stream()` 并不使用数据库 session，所以在发送响应期间保持 session 打开并不必要。

如果你在使用 SQLModel（或 SQLAlchemy）时遇到这种特定用例，你可以在不再需要 session 后显式关闭它：

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

这样 session 就会释放数据库连接，以便其他请求可以使用它。

如果你有其他用例需要从带有 `yield` 的依赖项中提前退出，请创建一个 <a href="https://github.com/fastapi/fastapi/discussions/new?category=questions" class="external-link" target="_blank">GitHub Discussion Question</a>，说明你的具体用例以及为何你会受益于对带有 `yield` 的依赖项进行提前关闭。

如果确实存在有说服力的用例需要在带有 `yield` 的依赖项中提前关闭，我会考虑添加一种新的方式来选择启用提前关闭。

### 带有 `yield` 和 `except` 的依赖项，技术细节 { #dependencies-with-yield-and-except-technical-details }

在 FastAPI 0.110.0 之前，如果你使用了带有 `yield` 的依赖项，并且在该依赖项中使用 `except` 捕获了异常，但没有再次抛出该异常，那么该异常会被自动抛出/转发到任何异常处理器或内部服务器错误处理器。

在 0.110.0 版本中，这一行为被更改，用于修复：在没有处理器（内部服务器错误）的情况下，转发异常会导致未处理的内存消耗；同时也使其与常规 Python 代码的行为保持一致。

### Background Tasks 与带有 `yield` 的依赖项，技术细节 { #background-tasks-and-dependencies-with-yield-technical-details }

在 FastAPI 0.106.0 之前，在 `yield` 之后抛出异常是不可能的，因为带有 `yield` 的依赖项的退出代码是在响应发送*之后*执行的，因此 [异常处理器](../tutorial/handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank} 早已运行完毕。

这样设计主要是为了允许在后台任务中使用依赖项“yield 出来”的同一个对象，因为退出代码会在后台任务完成之后才执行。

在 FastAPI 0.106.0 中，这一行为被更改，其意图是不在等待响应通过网络传输时持有资源。

/// tip | 提示

此外，后台任务通常是一套独立的逻辑，应该单独处理，并使用它自己的资源（例如它自己的数据库连接）。

因此，这样你通常会得到更干净的代码。

///

如果你过去依赖这种行为，那么现在你应该在后台任务内部创建资源，并且在内部只使用那些不依赖带有 `yield` 的依赖项资源的数据。

例如，不再使用同一个数据库 session，而是在后台任务内部创建一个新的数据库 session，并用这个新 session 从数据库中获取对象。然后，不再把数据库对象作为参数传递给后台任务函数，而是传递该对象的 ID，并在后台任务函数内部再次获取该对象。
