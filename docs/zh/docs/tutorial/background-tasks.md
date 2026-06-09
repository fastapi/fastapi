# 后台任务 { #background-tasks }

你可以定义后台任务。它会在返回响应之后运行。

这适合那些请求后需要做，但没必要让客户端等着的操作。

比如：

* 动作完成后发邮件通知：
    * 连接邮件服务器并发送邮件比较慢（要几秒）。可以先返回响应，把发邮件放到后台跑。
* 处理数据：
    * 比如你收到一个需要慢处理的文件。可以先返回 "Accepted"（HTTP 202），把文件在后台处理。

## 使用 `BackgroundTasks` { #using-backgroundtasks }

先导入 `BackgroundTasks`。在你的*路径操作函数*里声明一个类型为 `BackgroundTasks` 的参数：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI** 会帮你创建 `BackgroundTasks` 实例，并注入到这个参数里。

## 写任务函数 { #create-a-task-function }

写一个要在后台跑的函数。

就是普通函数。可以接收参数。

可以是 `async def`，也可以是普通 `def`。**FastAPI** 都能正确处理。

这个例子里，任务函数会写文件（模拟发邮件）。

写文件不需要 `async/await`，所以用普通 `def`：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## 添加后台任务 { #add-the-background-task }

在你的*路径操作函数*里，用 `.add_task()` 把任务函数加到 `BackgroundTasks` 对象里：

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` 的参数：

* 要在后台运行的任务函数（`write_notification`）。
* 按位置传给任务函数的参数序列（`email`）。
* 传给任务函数的关键字参数（`message="some notification"`）。

## 依赖注入 { #dependency-injection }

配合依赖注入也能用。你可以在多层级声明 `BackgroundTasks` 参数：在*路径操作函数*、依赖、子依赖等。

**FastAPI** 会复用同一个对象。把各处添加的后台任务合并。等响应发出后再统一执行：

{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}

这个示例里，响应发出后才把消息写进 `log.txt`。

如果请求里有 query，会由后台任务写入日志。

然后路径操作函数里再加一个后台任务。它会用 `email` 路径参数写一条消息。

## 技术细节 { #technical-details }

`BackgroundTasks` 类来自 [`starlette.background`](https://www.starlette.dev/background/)。

它在 FastAPI 里被直接导出。这样你可以从 `fastapi` 导入，避免不小心从 `starlette.background` 导入另一个 `BackgroundTask`（没有结尾的 s）。

只用 `BackgroundTasks`（不是 `BackgroundTask`）时，就能把它当作*路径操作函数*的参数。剩下的交给 **FastAPI**，跟直接用 `Request` 类似。

当然也能在 FastAPI 里单独用 `BackgroundTask`。但你要自己创建对象，并返回包含它的 Starlette `Response`。

更多细节看 [Starlette 的 Background Tasks 文档](https://www.starlette.dev/background/)。

## 注意事项 { #caveat }

如果后台计算很重，而且不需要在同一进程里跑（不需要共享内存、变量等），用更大的工具会更好，比如 [Celery](https://docs.celeryq.dev)。

它们配置更复杂。需要消息/任务队列管理器，比如 RabbitMQ 或 Redis。好处是能在多个进程，尤其是多台服务器上跑后台任务。

但如果你要访问同一个 **FastAPI** 应用里的变量和对象。或者任务很轻（比如发邮件通知）。用 `BackgroundTasks` 就够了。

## 回顾 { #recap }

在*路径操作函数*和依赖里导入并使用 `BackgroundTasks` 参数，给应用添加后台任务。
