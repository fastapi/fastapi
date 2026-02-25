# 高级依赖项 { #advanced-dependencies }

## 参数化的依赖项 { #parameterized-dependencies }

目前我们看到的依赖项都是固定的函数或类。

但有时你可能希望为依赖项设置参数，而不必声明许多不同的函数或类。

假设我们要有一个依赖项，用来检查查询参数 `q` 是否包含某个固定内容。

但我们希望能够把这个固定内容参数化。

## “可调用”的实例 { #a-callable-instance }

在 Python 中，可以让某个类的实例变成“可调用对象”（callable）。

这里指的是类的实例（类本身已经是可调用的），而不是类本身。

为此，声明一个 `__call__` 方法：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[12] *}

在这种情况下，**FastAPI** 会使用这个 `__call__` 来检查附加参数和子依赖，并且稍后会调用它，把返回值传递给你的*路径操作函数*中的参数。

## 参数化实例 { #parameterize-the-instance }

现在，我们可以用 `__init__` 声明实例的参数，用来“参数化”这个依赖项：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[9] *}

在本例中，**FastAPI** 不会接触或关心 `__init__`，我们会在自己的代码中直接使用它。

## 创建实例 { #create-an-instance }

我们可以这样创建该类的实例：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[18] *}

这样就把依赖项“参数化”了，现在它内部带有属性 `checker.fixed_content` 的值 `"bar"`。

## 把实例作为依赖项 { #use-the-instance-as-a-dependency }

然后，我们可以在 `Depends(checker)` 中使用这个 `checker`，而不是 `Depends(FixedContentQueryChecker)`，因为依赖项是实例 `checker`，不是类本身。

解析依赖项时，**FastAPI** 会像这样调用 `checker`：

```Python
checker(q="somequery")
```

...并将其返回值作为依赖项的值，传给我们的*路径操作函数*中的参数 `fixed_content_included`：

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[22] *}

/// tip | 提示

这些看起来可能有些牵强，目前它的用处也许还不太明显。

这些示例刻意保持简单，但展示了整体的工作方式。

在安全相关的章节里，有一些工具函数就是以相同的方式实现的。

如果你理解了这里的内容，你就已经知道那些安全工具在底层是如何工作的。

///

## 带 `yield` 的依赖项、`HTTPException`、`except` 与后台任务 { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | 警告

你很可能不需要了解这些技术细节。

这些细节主要在你的 FastAPI 应用版本低于 0.121.0 且你正遇到带 `yield` 的依赖项问题时才有用。

///

带 `yield` 的依赖项随着时间演进以覆盖不同用例并修复一些问题，下面是变更摘要。

### 带 `yield` 的依赖项与 `scope` { #dependencies-with-yield-and-scope }

在 0.121.0 版本中，FastAPI 为带 `yield` 的依赖项新增了 `Depends(scope="function")` 的支持。

使用 `Depends(scope="function")` 时，`yield` 之后的退出代码会在*路径操作函数*结束后、响应发送给客户端之前立即执行。

而当使用默认的 `Depends(scope="request")` 时，`yield` 之后的退出代码会在响应发送之后执行。

你可以在文档 [带 `yield` 的依赖项 - 提前退出与 `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) 中了解更多。

### 带 `yield` 的依赖项与 `StreamingResponse`（技术细节） { #dependencies-with-yield-and-streamingresponse-technical-details }

在 FastAPI 0.118.0 之前，如果你使用带 `yield` 的依赖项，它会在*路径操作函数*返回后、发送响应之前运行 `yield` 之后的退出代码。

这样做的目的是避免在等待响应通过网络传输期间不必要地占用资源。

这也意味着，如果你返回的是 `StreamingResponse`，那么该带 `yield` 的依赖项的退出代码会在开始发送响应前就已经执行完毕。

例如，如果你在带 `yield` 的依赖项中持有一个数据库会话，那么 `StreamingResponse` 在流式发送数据时将无法使用该会话，因为会话已经在 `yield` 之后的退出代码里被关闭了。

在 0.118.0 中，这一行为被回退为：让 `yield` 之后的退出代码在响应发送之后再执行。

/// info | 信息

如你在下文所见，这与 0.106.0 之前的行为非常相似，但对若干边界情况做了改进和修复。

///

#### 需要提前执行退出代码的用例 { #use-cases-with-early-exit-code }

在某些特定条件下，旧的行为（在发送响应之前执行带 `yield` 依赖项的退出代码）会更有利。

例如，设想你在带 `yield` 的依赖项中仅用数据库会话来校验用户，而在*路径操作函数*中并不会再次使用该会话；同时，响应需要很长时间才能发送完，比如一个缓慢发送数据的 `StreamingResponse`，且它出于某种原因并不使用数据库。

这种情况下，会一直持有数据库会话直到响应发送完毕；但如果并不再使用它，就没有必要一直占用。

代码可能如下：

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

退出代码（自动关闭 `Session`）位于：

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...会在响应把慢速数据发送完之后才运行：

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

但由于 `generate_stream()` 并不使用数据库会话，因此在发送响应期间保持会话打开并非必要。

如果你使用的是 SQLModel（或 SQLAlchemy）并碰到这种特定用例，你可以在不再需要时显式关闭会话：

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

这样会话会释放数据库连接，让其他请求可以使用。

如果你还有其他需要在 `yield` 依赖项中提前退出的用例，请创建一个 <a href="https://github.com/fastapi/fastapi/discussions/new?category=questions" class="external-link" target="_blank">GitHub 讨论问题</a>，说明你的具体用例以及为何提前关闭会对你有帮助。

如果确有有力的用例需要提前关闭，我会考虑新增一种选择性启用提前关闭的方式。

### 带 `yield` 的依赖项与 `except`（技术细节） { #dependencies-with-yield-and-except-technical-details }

在 FastAPI 0.110.0 之前，如果你在带 `yield` 的依赖项中用 `except` 捕获了一个异常，并且没有再次抛出它，那么该异常会被自动抛出/转发给任意异常处理器或内部服务器错误处理器。

在 0.110.0 中对此作出了变更，以修复将异常转发为未处理（内部服务器错误）时造成的内存消耗问题，并使其与常规 Python 代码的行为保持一致。

### 后台任务与带 `yield` 的依赖项（技术细节） { #background-tasks-and-dependencies-with-yield-technical-details }

在 FastAPI 0.106.0 之前，`yield` 之后抛出异常是不可行的，因为带 `yield` 的依赖项中的退出代码会在响应发送之后才执行，此时[异常处理器](../tutorial/handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank}已经运行完毕。

之所以这样设计，主要是为了允许在后台任务中继续使用依赖项通过 `yield`“产出”的对象，因为退出代码会在后台任务完成之后才执行。

在 FastAPI 0.106.0 中，这一行为被修改，目的是避免在等待响应通过网络传输时一直占用资源。

/// tip | 提示

另外，后台任务通常是一段独立的逻辑，应该单独处理，并使用它自己的资源（例如它自己的数据库连接）。

因此，这样做你的代码通常会更清晰。

///

如果你过去依赖于旧行为，现在应在后台任务内部自行创建所需资源，并且只在内部使用不依赖于带 `yield` 依赖项资源的数据。

例如，不要复用相同的数据库会话，而是在后台任务内部创建一个新的会话，并用这个新会话从数据库获取对象。然后，不是把数据库对象本身作为参数传给后台任务函数，而是传递该对象的 ID，并在后台任务函数内部再次获取该对象。
