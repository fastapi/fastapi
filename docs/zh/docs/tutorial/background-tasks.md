# 后台任务

**FastAPI** 可以定义返回响应后运行的后台任务。

如果要在请求后执行某些操作，但在接收响应之前不希望客户端等待操作执行完毕，就要使用后台任务。

包括如下场景：

* 执行操作后发送电子邮件通知：
    * 连接邮件服务器与发送邮件相对**较慢**（几秒），此时应直接返回响应，在后台发送邮件通知
* 处理数据：
    * 接收文件缓慢时，应先返回 `Accepted`（`HTTP 202`），在后台处理文件

## 使用 `BackgroundTasks`

首先，导入 `BackgroundTasks`，声明 `BackgroundTasks` 类型的*路径操作函数*参数：

```Python hl_lines="1  13"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

**FastAPI** 创建 `BackgroundTasks` 类型的对象参数。

## 创建任务函数

创建运行后台任务的函数。

任务函数是能接收参数的标准函数。

任务函数既可以是异步函数，也可以是普通函数，**FastAPI** 都能正确处理。

本例中，任务函数（模拟发送邮件）输出一个文件。

写入文件的操作无需使用 `async` 和 `await`， 所以使用 `def` 定义普通函数：

```Python hl_lines="6-9"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

## 添加后台任务

在*路径操作函数*中，使用 `.add_task()` 方法把任务函数传递给*后台任务*对象：

```Python hl_lines="14"
{!../../../docs_src/background_tasks/tutorial001.py!}
```

`.add_task()` 是实参（`Argument`）：

* 在后台运行的任务函数（`write_notification`）
* 按顺序传递给任务函数的实参序列（`email`）
* 传递给任务函数的关键字参数（`message="some notification"`）

## 依赖注入

依赖注入系统中也可以使用 `BackgroundTasks`，可以在不同层级声明 `BackgroundTasks` 类型的参数：*路径操作函数*、依赖项、子依赖项等。

**FastAPI** 知道怎样为不同情况执行不同的操作，以及如何复用相同对象，以便把所有后台任务合并为一体，并在后台运行：

```Python hl_lines="13  15  22  25"
{!../../../docs_src/background_tasks/tutorial002.py!}
```

本例中，响应发送后会把所有信息写入 `log.txt`。

如果请求中包含查询，该查询也会被后台任务写入日志。

然后，*路径操作函数*中生成的另一个后台任务会使用 `email` 路径参数写入信息。

## 技术细节

`BackgroundTasks` 类直接继承自 <a href="https://www.starlette.io/background/" class="external-link" target="_blank">`starlette.background`</a>。

FastAPI 中直接提供了 `BackgroundTasks` 类，这样就可以直接从 `fastapi` 中导入，避免不小心从 `starlette.background` 中导入备用的 `BackgroundTask`（结尾没有 `s`）。

*路径操作函数*中应当只使用 `BackgroundTasks` （不是 `BackgroundTask`），**FastAPI** 会处理其它操作，这点与直接使用 `Request` 一样。

FastAPI 中也可以使用 `BackgroundTask`，但必须要在代码中创建这个对象，并返回包含该对象的 Starlette `Response`。

详见  <a href="https://www.starlette.io/background/" class="external-link" target="_blank">Starlette 官档：后台任务</a>。

## 警告

如果需要执行繁重的后台计算，而且不需要由同一进程执行（例如，不需要共享内存、变量）时，可以使用 <a href="https://docs.celeryproject.org" class="external-link" target="_blank">Celery</a> 等工具。

这些工具需要更复杂的配置，还需要 RabbitMQ 或 Redis 等信息/工作队列管理器，但它们能使用多进程，尤其是可以在多个服务器上执行后台任务。

 [项目生成器](../project-generation.md){.internal-link target=_blank}一章中提供了包含所有配置好的 Celery 实例。

但如果只在 **FastAPI** 应用中访问变量或对象，或只是执行（发送邮件通知等）小型后台任务，只使用 `BackgroundTasks` 就够了。

## 小结

本章介绍了如何导入 `BackgroundTasks`，并在*路径操作函数*和依赖项的参数中使用 `BackgroundTasks` 添加后台任务。
