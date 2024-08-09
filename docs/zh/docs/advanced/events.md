# 事件：启动 - 关闭

**FastAPI** 支持定义在应用启动前，或应用关闭后执行的事件处理器（函数）。

事件函数既可以声明为异步函数（`async def`），也可以声明为普通函数（`def`）。

/// warning | "警告"

**FastAPI** 只执行主应用中的事件处理器，不执行[子应用 - 挂载](sub-applications.md){.internal-link target=_blank}中的事件处理器。

///

## `startup` 事件

使用 `startup` 事件声明 `app` 启动前运行的函数：

```Python hl_lines="8"
{!../../../docs_src/events/tutorial001.py!}
```

本例中，`startup` 事件处理器函数为项目数据库（只是**字典**）提供了一些初始值。

**FastAPI** 支持多个事件处理器函数。

只有所有 `startup` 事件处理器运行完毕，**FastAPI** 应用才开始接收请求。

## `shutdown` 事件

使用 `shutdown` 事件声明 `app` 关闭时运行的函数：

```Python hl_lines="6"
{!../../../docs_src/events/tutorial002.py!}
```

此处，`shutdown` 事件处理器函数在 `log.txt` 中写入一行文本 `Application shutdown`。

/// info | "说明"

`open()` 函数中，`mode="a"` 指的是**追加**。因此这行文本会添加在文件已有内容之后，不会覆盖之前的内容。

///

/// tip | "提示"

注意，本例使用 Python `open()` 标准函数与文件交互。

这个函数执行 I/O（输入/输出）操作，需要等待内容写进磁盘。

但 `open()` 函数不支持使用 `async` 与 `await`。

因此，声明事件处理函数要使用 `def`，不能使用 `asnyc def`。

///

/// info | "说明"

有关事件处理器的详情，请参阅 <a href="https://www.starlette.io/events/" class="external-link" target="_blank">Starlette 官档 - 事件</a>。

///
