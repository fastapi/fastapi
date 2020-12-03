# 后台任务

您可以定义后台任务，在 *返回响应后* 运行。

这对于需要在请求之后执行的操作非常有用，但是客户端并不需要在接收响应之前等待操作完成。

这包括，例如:

* 执行操作后发送的电子邮件通知:
    * 由于连接到电子邮件服务器和发送电子邮件往往是 "慢" (几秒钟)的，你可以立即返回响应，并在后台发送电子邮件通知。
* 处理数据:
    * 例如，假设您接收一个必须经过缓慢进程的文件，您可以返回一个 "accept" 响应(HTTP 202)并在后台处理它。

## 使用 `BackgroundTasks`

首先，导入 `BackgroundTasks` 并且在 *路径操作函数* 中定义一个参数，类型声明为 `BackgroundTasks` 。

```Python hl_lines="1  13"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

**FastAPI** 将为您创建类型为 `BackgroundTasks` 的对象，并将其作为参数传递。

## 创建一个任务函数

创建一个作为后台任务运行的函数。

它只是一个可以接收参数的标准函数。

它可以是一个 `async def` 或普通的 `def` 函数，**FastAPI**将知道如何正确处理它。

在本例中，任务函数将写入文件(模拟发送电子邮件)。

并且由于写操作不使用 `async` 和 `await`，我们用普通的 `def` 定义函数:

```Python hl_lines="6-9"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

## 添加后台任务

在你的 *路径操作函数* 中，通过 `.add_task()` 方法将你的工作函数传递给 *后台任务* 对象:

```Python hl_lines="14"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

`.add_task()` 接收参数:

* 在后台运行的任务函数 (`write_notification`).
* 按顺序传递给任务函数的任何参数序列 (`email`).
* 应该传递给任务函数的任何关键字参数 (`message="some notification"`).

## 依赖注入

`BackgroundTasks` 也可以与依赖注入系统一起工作，你可以在多个级别上声明一个类型为 `BackgroundTasks` 的参数:在 *路径操作函数* 中，在依赖项(可依赖的)中，在子依赖项中，等等。

**FastAPI** 知道在每种情况下做什么，以及如何重用相同的对象，这样所有的后台任务合并在一起之后在后台运行:

```Python hl_lines="13  15  22  25"
{!../../../docs_src/background_tasks/tutorial002.py!}
```

在本例中，这些消息将在响应被发送 *之后* 被写入到 `log.txt` 文件。

如果请求中有查询，它将被写入后台任务的日志中。

然后，在 *路径操作函数* 生成的另一个后台任务将使用 `email` 路径参数写一条消息。

## 技术细节

`BackgroundTasks` 类直接来自于 <a href="https://www.starlette.io/background/" class="external-link" target="_blank">`starlette.background`</a>.

它被直接导入/包含到 FastAPI 中，这样你就可以从 FastAPI 中导入它，避免意外地从 `starlette.background` 中导入替代的 `BackgroundTask` (末尾没有 `s` )。

通过只使用 `BackgroundTasks` (而不是 `BackgroundTask` )，然后就可以使用它作为 *路径操作函数* 参数，并让 **FastAPI** 为您处理其余的，就像直接使用 `Request` 对象一样。

在 FastAPI 中仍然可以单独使用 `BackgroundTask` ，但你必须在代码中创建 `BackgroundTask` 对象并返回一个包含它的Starlette `Response` 。

你可以在<a href="https://www.starlette.io/background/" class="external-link" target="_blank">Starlette后台任务的官方文档</a>中看到更多细节。

## 警告

如果你需要执行较重的后台计算，且不一定需要由相同的进程执行(例如,你不需要共享内存变量,等等)，你可能会受益于使用其他更大的工具,像<a href="https://docs.celeryproject.org" class="external-link" target="_blank">Celery</a>。

它们往往需要更复杂的配置，一个消息/任务队列管理器，如 RabbitMQ 或 Redis ，但它们允许你在多个进程中运行后台任务，特别是在多个服务器中。

要查看示例，请检查[Project Generators](../project-generation.md){.internal-link target=_blank}，它们都包含已经配置好的Celery。

但是如果你需要从相同的 FastAPI 应用中访问变量和对象，或者你需要执行小的后台任务(比如发送邮件通知)，你可以简单地使用 `BackgroundTasks` 。

## 总结

导入，并在 *路径操作函数* 和依赖项的参数中使用 `BackgroundTasks` 来添加后台任务。
