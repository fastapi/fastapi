# 生命周期事件 { #lifespan-events }

你可以定义在应用**启动**前执行的逻辑（代码）。这意味着在应用**开始接收请求**之前，这些代码只会被执行**一次**。

同样地，你可以定义在应用**关闭**时应执行的逻辑。在这种情况下，这段代码将在**处理可能的多次请求后**执行**一次**。

因为这段代码在应用开始接收请求**之前**执行，也会在处理可能的若干请求**之后**执行，它覆盖了整个应用程序的**生命周期**（“生命周期”这个词很重要😉）。

这对于设置你需要在整个应用中使用的**资源**非常有用，这些资源在请求之间**共享**，你可能需要在之后进行**释放**。例如，数据库连接池，或加载一个共享的机器学习模型。

## 用例 { #use-case }

让我们从一个示例**用例**开始，看看如何用它来解决问题。

假设你有几个**机器学习的模型**，你想要用它们来处理请求。🤖

相同的模型在请求之间是共享的，因此并非每个请求或每个用户各自拥有一个模型。

假设加载模型可能**需要相当长的时间**，因为它必须从**磁盘**读取大量数据。因此你不希望每个请求都加载它。

你可以在模块/文件的顶部加载它，但这也意味着即使你只是在运行一个简单的自动化测试，它也会**加载模型**，这样测试将**变慢**，因为它必须在能够独立运行代码的其他部分之前等待模型加载完成。

这就是我们要解决的问题——在处理请求前加载模型，但只是在应用开始接收请求前，而不是在代码被加载时。

## Lifespan { #lifespan }

你可以使用 `FastAPI` 应用的 `lifespan` 参数和一个“上下文管理器”（稍后我将为你展示）来定义**启动**和**关闭**的逻辑。

让我们从一个例子开始，然后详细介绍。

我们使用 `yield` 创建了一个异步函数 `lifespan()` 像这样：

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

在这里，我们在 `yield` 之前将（虚拟的）模型函数放入机器学习模型的字典中，以此模拟加载模型的耗时**启动**操作。这段代码将在应用程序**开始处理请求之前**执行，即**启动**期间。

然后，在 `yield` 之后，我们卸载模型。这段代码将会在应用程序**完成处理请求后**执行，即在**关闭**之前。这可以释放诸如内存或 GPU 之类的资源。

/// tip | 提示

**关闭**事件会在你**停止**应用时发生。

可能你需要启动一个新版本，或者你只是厌倦了运行它。 🤷

///

### 生命周期函数 { #lifespan-function }

首先要注意的是，我们定义了一个带有 `yield` 的异步函数。这与带有 `yield` 的依赖项非常相似。

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

这个函数在 `yield` 之前的部分，会在应用启动前执行。

剩下的部分在 `yield` 之后，会在应用完成后执行。

### 异步上下文管理器 { #async-context-manager }

如你所见，这个函数有一个装饰器 `@asynccontextmanager`。

它将函数转化为所谓的“**异步上下文管理器**”。

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

在 Python 中，**上下文管理器**是一个你可以在 `with` 语句中使用的东西，例如，`open()` 可以作为上下文管理器使用。

```Python
with open("file.txt") as file:
    file.read()
```

Python 的最近几个版本也有了一个**异步上下文管理器**，你可以通过 `async with` 来使用：

```Python
async with lifespan(app):
    await do_stuff()
```

你可以像上面一样创建一个上下文管理器或者异步上下文管理器，它的作用是在进入 `with` 块时，执行 `yield` 之前的代码，并且在离开 `with` 块时，执行 `yield` 后面的代码。

但在我们上面的例子里，我们并不是直接使用，而是传递给 FastAPI 来供其使用。

`FastAPI` 的 `lifespan` 参数接受一个**异步上下文管理器**，所以我们可以把我们新定义的异步上下文管理器 `lifespan` 传给它。

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## 替代事件（弃用） { #alternative-events-deprecated }

/// warning | 警告

配置**启动**和**关闭**的推荐方法是使用 `FastAPI` 应用的 `lifespan` 参数，如前所示。如果你提供了一个 `lifespan` 参数，启动（`startup`）和关闭（`shutdown`）事件处理器将不再生效。要么使用 `lifespan`，要么配置所有事件，两者不能共用。

你可以跳过这一部分。

///

有一种替代方法可以定义在**启动**和**关闭**期间执行的逻辑。

你可以定义在应用启动前或应用关闭时需要执行的事件处理器（函数）。

事件函数既可以声明为异步函数（`async def`），也可以声明为普通函数（`def`）。

### `startup` 事件 { #startup-event }

使用事件 `"startup"` 声明一个在应用启动前运行的函数：

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

本例中，`startup` 事件处理器函数为项目“数据库”（只是一个 `dict`）提供了一些初始值。

**FastAPI** 支持多个事件处理器函数。

只有所有 `startup` 事件处理器运行完毕，**FastAPI** 应用才开始接收请求。

### `shutdown` 事件 { #shutdown-event }

使用事件 `"shutdown"` 声明一个在应用关闭时运行的函数：

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

此处，`shutdown` 事件处理器函数会向文件 `log.txt` 写入一行文本 `"Application shutdown"`。

/// info | 信息

在 `open()` 函数中，`mode="a"` 指的是“追加”。因此这行文本会添加在文件已有内容之后，不会覆盖之前的内容。

///

/// tip | 提示

注意，本例使用 Python 标准的 `open()` 函数与文件交互。

这个函数执行 I/O（输入/输出）操作，需要“等待”内容写进磁盘。

但 `open()` 不使用 `async` 和 `await`。

因此，声明事件处理函数要使用 `def`，而不是 `async def`。

///

### `startup` 和 `shutdown` 一起使用 { #startup-and-shutdown-together }

启动和关闭的逻辑很可能是连接在一起的，你可能希望启动某个东西然后结束它，获取一个资源然后释放它等等。

在不共享逻辑或变量的不同函数中处理这些逻辑比较困难，因为你需要在全局变量中存储值或使用类似的方式。

因此，推荐使用上面所述的 `lifespan`。

## 技术细节 { #technical-details }

只是为好奇者提供的技术细节。🤓

在底层，这部分是 ASGI 技术规范中的 <a href="https://asgi.readthedocs.io/en/latest/specs/lifespan.html" class="external-link" target="_blank">Lifespan 协议</a>的一部分，定义了称为 `startup` 和 `shutdown` 的事件。

/// info | 信息

你可以在 <a href="https://www.starlette.dev/lifespan/" class="external-link" target="_blank">Starlette 的 Lifespan 文档</a> 中阅读更多关于 `lifespan` 处理器的内容。

包括如何处理生命周期状态，以便在代码的其他部分使用。

///

## 子应用 { #sub-applications }

🚨 请注意，这些生命周期事件（startup 和 shutdown）只会在主应用上执行，不会在[子应用 - 挂载](sub-applications.md){.internal-link target=_blank}上执行。
