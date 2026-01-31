# 生命周期事件 { #lifespan-events }

你可以定义在应用**启动**前应该执行的逻辑（代码）。这意味着这些代码将会被执行**一次**，并且在应用**开始接收请求之前**执行。

同样地，你可以定义在应用**关闭**时应该执行的逻辑（代码）。在这种情况下，这段代码将会被执行**一次**，在处理了可能的**许多请求之后**执行。

因为这段代码会在应用**开始**接收请求之前执行，并且在它**完成**处理请求后马上执行，它覆盖了整个应用程序的**生命周期**（“lifespan”这个词马上会很重要😉）。

这对于设置你需要在整个应用中使用的、在请求之间**共享**的**资源**，以及/或者你之后需要**清理**的资源，非常有用。例如：数据库连接池，或加载一个共享的机器学习模型。

## 用例 { #use-case }

让我们先从一个示例**用例**开始，然后看看如何用它来解决。

假设你有一些**机器学习模型**，你想用它们来处理请求。🤖

相同的模型在请求之间是共享的，所以并不是每个请求一个模型，或每个用户一个模型之类的。

假设加载模型可能**需要相当长的时间**，因为它必须从**磁盘读取大量数据**。所以你不希望每个请求都这么做。

你可以在模块/文件的顶层加载它，但那也意味着即使你只是运行一个简单的自动化测试，它也会**加载模型**，然后测试会很**慢**，因为它必须等待模型加载完成，才能运行代码中独立的部分。

这就是我们要解决的问题：在处理请求前加载模型，但只在应用开始接收请求之前加载，而不是在代码被加载时加载。

## 生命周期 { #lifespan }

你可以使用 `FastAPI` 应用的 `lifespan` 参数，以及一个“上下文管理器”（我马上会给你展示它是什么）来定义这些 *startup* 和 *shutdown* 逻辑。

让我们从一个例子开始，然后再详细看看。

我们用 `yield` 创建了一个异步函数 `lifespan()`，像这样：

{* ../../docs_src/events/tutorial003_py39.py hl[16,19] *}

这里我们通过在 `yield` 之前把（假的）模型函数放进机器学习模型的字典中，来模拟加载模型这种开销较大的 *startup* 操作。这段代码会在应用**开始接收请求之前**执行，也就是在 *startup* 期间。

然后，就在 `yield` 之后，我们卸载模型。这段代码会在应用**完成处理请求后**执行，也就是在 *shutdown* 之前。比如，这可以释放内存或 GPU 等资源。

/// tip | 提示

`shutdown` 会在你**停止**应用时发生。

也许你需要启动一个新版本，或者你只是你厌倦了运行它。 🤷

///

### 生命周期函数 { #lifespan-function }

首先要注意的是，我们定义了一个带有 `yield` 的异步函数。这与带有 `yield` 的依赖项非常相似。

{* ../../docs_src/events/tutorial003_py39.py hl[14:19] *}

函数在 `yield` 之前的第一部分，会在应用启动之前执行。

而 `yield` 之后的部分，会在应用完成后执行。

### 异步上下文管理器 { #async-context-manager }

如果你检查一下，会看到这个函数被 `@asynccontextmanager` 装饰器修饰。

它将函数转换成一种叫做“**异步上下文管理器**”的东西。

{* ../../docs_src/events/tutorial003_py39.py hl[1,13] *}

Python 中的**上下文管理器**是你可以在 `with` 语句中使用的东西，例如，`open()` 可以作为上下文管理器使用：

```Python
with open("file.txt") as file:
    file.read()
```

在 Python 的最近几个版本中，也有**异步上下文管理器**。你会用 `async with` 来使用它：

```Python
async with lifespan(app):
    await do_stuff()
```

当你像上面那样创建一个上下文管理器或异步上下文管理器时，它会在进入 `with` 块之前执行 `yield` 之前的代码，并在退出 `with` 块之后执行 `yield` 之后的代码。

在我们上面的代码示例中，我们没有直接使用它，而是把它传给 FastAPI，让 FastAPI 来使用它。

`FastAPI` 应用的 `lifespan` 参数接收一个**异步上下文管理器**，因此我们可以把我们新定义的 `lifespan` 异步上下文管理器传给它。

{* ../../docs_src/events/tutorial003_py39.py hl[22] *}

## 替代事件（已弃用） { #alternative-events-deprecated }

/// warning | 警告

处理 *startup* 和 *shutdown* 的推荐方式是像上面描述的那样使用 `FastAPI` 应用的 `lifespan` 参数。如果你提供了 `lifespan` 参数，`startup` 和 `shutdown` 事件处理器将不再被调用。要么全用 `lifespan`，要么全用事件，不能同时使用。

你大概可以跳过这一部分。

///

还有一种替代方法，用于定义在 *startup* 和 *shutdown* 期间执行的逻辑。

你可以定义事件处理器（函数），它们需要在应用启动前执行，或在应用正在关闭时执行。

这些函数可以用 `async def` 声明，也可以用普通的 `def` 声明。

### `startup` 事件 { #startup-event }

要添加一个应该在应用启动前运行的函数，用事件 `"startup"` 来声明它：

{* ../../docs_src/events/tutorial001_py39.py hl[8] *}

在这个例子中，`startup` 事件处理器函数会用一些值来初始化名为 “database” 的条目（只是一个 `dict`）。

你可以添加多个事件处理器函数。

并且，只有在所有 `startup` 事件处理器完成后，你的应用才会开始接收请求。

### `shutdown` 事件 { #shutdown-event }

要添加一个应该在应用关闭时运行的函数，用事件 `"shutdown"` 来声明它：

{* ../../docs_src/events/tutorial002_py39.py hl[6] *}

这里，`shutdown` 事件处理器函数会向文件 `log.txt` 写入一行文本 `"Application shutdown"`。

/// info | 信息

在 `open()` 函数中，`mode="a"` 表示“追加（append）”，因此这行文本会被添加到文件现有内容之后，而不会覆盖之前的内容。

///

/// tip | 提示

注意，在这种情况下我们使用了与文件交互的 Python 标准 `open()` 函数。

因此，这涉及 I/O（input/output）操作，需要“等待”内容写入磁盘。

但 `open()` 不使用 `async` 和 `await`。

所以，我们用标准的 `def` 而不是 `async def` 来声明事件处理器函数。

///

### `startup` 和 `shutdown` 一起使用 { #startup-and-shutdown-together }

你的 *startup* 和 *shutdown* 逻辑很可能是有关联的：你可能想启动某个东西然后结束它，获取一个资源然后释放它，等等。

在不共享逻辑或变量的分离函数中实现这些会更困难，因为你需要把值存储在全局变量中或使用类似的技巧。

正因为如此，现在推荐你像上面解释的那样改用 `lifespan`。

## 技术细节 { #technical-details }

只是为好奇的技术宅提供的技术细节。🤓

在底层，在 ASGI 技术规范中，这是 <a href="https://asgi.readthedocs.io/en/latest/specs/lifespan.html" class="external-link" target="_blank">Lifespan Protocol</a> 的一部分，它定义了名为 `startup` 和 `shutdown` 的事件。

/// info | 信息

你可以在 <a href="https://www.starlette.dev/lifespan/" class="external-link" target="_blank">Starlette's  Lifespan' docs</a> 中阅读更多关于 Starlette `lifespan` 处理器的内容。

包括如何处理可以在你代码其他区域使用的 lifespan state。

///

## 子应用 { #sub-applications }

🚨 请记住，这些生命周期事件（startup 和 shutdown）只会为主应用执行，不会为[子应用 - 挂载](sub-applications.md){.internal-link target=_blank}执行。
