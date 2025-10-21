# 后台任务

你可以定义在返回响应后运行的后台任务。

这对需要在请求之后执行的操作很有用，但客户端不必在接收响应之前等待操作完成。

包括这些例子：

* 执行操作后发送的电子邮件通知：
    * 由于连接到电子邮件服务器并发送电子邮件往往很“慢”（几秒钟），您可以立即返回响应并在后台发送电子邮件通知。
* 处理数据：
    * 例如，假设您收到的文件必须经过一个缓慢的过程，您可以返回一个"Accepted"(HTTP 202)响应并在后台处理它。

## 使用 `BackgroundTasks`

首先导入 `BackgroundTasks` 并在 *路径操作函数* 中使用类型声明 `BackgroundTasks` 定义一个参数：

{* ../../docs_src/background_tasks/tutorial001.py hl[1, 13] *}

**FastAPI** 会创建一个 `BackgroundTasks` 类型的对象并作为该参数传入。

## 创建一个任务函数

创建要作为后台任务运行的函数。

它只是一个可以接收参数的标准函数。

它可以是 `async def` 或普通的 `def` 函数，**FastAPI** 知道如何正确处理。

在这种情况下，任务函数将写入一个文件（模拟发送电子邮件）。

由于写操作不使用 `async` 和 `await`，我们用普通的 `def` 定义函数：

{* ../../docs_src/background_tasks/tutorial001.py hl[6:9] *}

## 添加后台任务

在你的 *路径操作函数* 里，用 `.add_task()` 方法将任务函数传到 *后台任务* 对象中：

{* ../../docs_src/background_tasks/tutorial001.py hl[14] *}

`.add_task()` 接收以下参数：

* 在后台运行的任务函数(`write_notification`)。
* 应按顺序传递给任务函数的任意参数序列(`email`)。
* 应传递给任务函数的任意关键字参数(`message="some notification"`)。

## 依赖注入

使用 `BackgroundTasks` 也适用于依赖注入系统，你可以在多个级别声明 `BackgroundTasks` 类型的参数：在 *路径操作函数* 里，在依赖中(可依赖)，在子依赖中，等等。

**FastAPI** 知道在每种情况下该做什么以及如何复用同一对象，因此所有后台任务被合并在一起并且随后在后台运行：

//// tab | Python 3.10+

{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13, 15, 22, 25] *}

////

//// tab | Python 3.9+

{* ../../docs_src/background_tasks/tutorial002_an_py39.py hl[13, 15, 22, 25] *}

////

//// tab | Python 3.8+

{* ../../docs_src/background_tasks/tutorial002_an.py hl[14, 16, 23, 26] *}

////

//// tab | Python 3.10+ 没Annotated

/// tip

尽可能选择使用 `Annotated` 的版本。

///

{* ../../docs_src/background_tasks/tutorial002_py310.py hl[11, 13, 20, 23] *}

////

//// tab | Python 3.8+ 没Annotated

/// tip

尽可能选择使用 `Annotated` 的版本。

///

{* ../../docs_src/background_tasks/tutorial002.py hl[13, 15, 22, 25] *}

////

该示例中，信息会在响应发出 *之后* 被写到 `log.txt` 文件。

如果请求中有查询，它将在后台任务中写入日志。

然后另一个在 *路径操作函数* 生成的后台任务会使用路径参数 `email` 写入一条信息。

## 技术细节

`BackgroundTasks` 类直接来自 <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>。

它被直接导入/包含到FastAPI以便你可以从 `fastapi` 导入，并避免意外从 `starlette.background` 导入备用的 `BackgroundTask` (后面没有 `s`)。

通过仅使用 `BackgroundTasks` (而不是 `BackgroundTask`)，使得能将它作为 *路径操作函数* 的参数 ，并让**FastAPI**为您处理其余部分, 就像直接使用 `Request` 对象。

在FastAPI中仍然可以单独使用 `BackgroundTask`，但您必须在代码中创建对象，并返回包含它的Starlette `Response`。

更多细节查看 <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">Starlette's official docs for Background Tasks</a>.

## 告诫

如果您需要执行繁重的后台计算，并且不一定需要由同一进程运行（例如，您不需要共享内存、变量等），那么使用其他更大的工具（如 <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>）可能更好。

它们往往需要更复杂的配置，即消息/作业队列管理器，如RabbitMQ或Redis，但它们允许您在多个进程中运行后台任务，甚至是在多个服务器中。

但是，如果您需要从同一个**FastAPI**应用程序访问变量和对象，或者您需要执行小型后台任务（如发送电子邮件通知），您只需使用 `BackgroundTasks` 即可。

## 回顾

导入并使用 `BackgroundTasks` 通过 *路径操作函数* 中的参数和依赖项来添加后台任务。
