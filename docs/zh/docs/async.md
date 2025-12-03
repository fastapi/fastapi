# 并发 async / await

有关路径操作函数的 `async def` 语法以及异步代码、并发和并行的一些背景知识。

## 赶时间吗？

<abbr title="too long; didn't read(长文警告)"><strong>TL;DR:</strong></abbr>

如果你正在使用第三方库，它们会告诉你使用 `await` 关键字来调用它们，就像这样：

```Python
results = await some_library()
```

然后，通过 `async def` 声明你的 *路径操作函数*：

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note

你只能在被 `async def` 创建的函数内使用 `await`

///

---

如果你正在使用一个第三方库和某些组件（比如：数据库、API、文件系统...）进行通信，第三方库又不支持使用 `await` （目前大多数数据库三方库都是这样），这种情况你可以像平常那样使用 `def` 声明一个路径操作函数，就像这样：

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

如果你的应用程序不需要与其他任何东西通信而等待其响应，请使用 `async def`。

---

如果你不清楚，使用 `def` 就好.

---

**注意**：你可以根据需要在路径操作函数中混合使用 `def` 和 `async def`，并使用最适合你的方式去定义每个函数。FastAPI 将为他们做正确的事情。

无论如何，在上述任何情况下，FastAPI 仍将异步工作，速度也非常快。

但是，通过遵循上述步骤，它将能够进行一些性能优化。

## 技术细节

Python 的现代版本支持通过一种叫**"协程"**——使用 `async` 和 `await` 语法的东西来写**”异步代码“**。

让我们在下面的部分中逐一介绍：

* **异步代码**
* **`async` 和 `await`**
* **协程**

## 异步代码

异步代码仅仅意味着编程语言 💬 有办法告诉计算机/程序 🤖 在代码中的某个点，它 🤖 将不得不等待在某些地方完成一些事情。让我们假设一些事情被称为 "慢文件"📝.

所以，在等待"慢文件"📝完成的这段时间，计算机可以做一些其他工作。

然后计算机/程序 🤖 每次有机会都会回来，因为它又在等待，或者它 🤖 完成了当前所有的工作。而且它 🤖 将查看它等待的所有任务中是否有已经完成的，做它必须做的任何事情。

接下来，它 🤖 完成第一个任务（比如是我们的"慢文件"📝) 并继续与之相关的一切。

这个"等待其他事情"通常指的是一些相对较慢（与处理器和 RAM 存储器的速度相比）的 <abbr title="Input and Output">I/O</abbr> 操作，比如说：

* 通过网络发送来自客户端的数据
* 客户端接收来自网络中的数据
* 磁盘中要由系统读取并提供给程序的文件的内容
* 程序提供给系统的要写入磁盘的内容
* 一个 API 的远程调用
* 一个数据库操作，直到完成
* 一个数据库查询，直到返回结果
* 等等.

这个执行的时间大多是在等待 <abbr title="Input and Output">I/O</abbr> 操作，因此它们被叫做 "I/O 密集型" 操作。

它被称为"异步"的原因是因为计算机/程序不必与慢任务"同步"，去等待任务完成的确切时刻，而在此期间不做任何事情直到能够获取任务结果才继续工作。

相反，作为一个"异步"系统，一旦完成，任务就可以排队等待一段时间（几微秒），等待计算机程序完成它要做的任何事情，然后回来获取结果并继续处理它们。

对于"同步"（与"异步"相反），他们通常也使用"顺序"一词，因为计算机程序在切换到另一个任务之前是按顺序执行所有步骤，即使这些步骤涉及到等待。

### 并发与汉堡

上述异步代码的思想有时也被称为“并发”，它不同于“并行”。

并发和并行都与“不同的事情或多或少同时发生”有关。

但是并发和并行之间的细节是完全不同的。

要了解差异，请想象以下关于汉堡的故事：

### 并发汉堡

你和你的恋人一起去快餐店，你排队在后面，收银员从你前面的人接单。😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

然后轮到你了，你为你的恋人和你选了两个非常豪华的汉堡。🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

收银员对厨房里的厨师说了一些话，让他们知道他们必须为你准备汉堡（尽管他们目前正在为之前的顾客准备汉堡）。

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

你付钱了。 💸

收银员给你轮到的号码。

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

当你在等待的时候，你和你的恋人一起去挑选一张桌子，然后你们坐下来聊了很长时间（因为汉堡很豪华，需要一些时间来准备）。

当你和你的恋人坐在桌子旁，等待汉堡的时候，你可以用这段时间来欣赏你的恋人是多么的棒、可爱和聪明✨😍✨。

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

在等待中和你的恋人交谈时，你会不时地查看柜台上显示的号码，看看是否已经轮到你了。

然后在某个时刻，终于轮到你了。你去柜台拿汉堡然后回到桌子上。

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

你们享用了汉堡，整个过程都很开心。✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// info

漂亮的插画来自 <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

///

---

在那个故事里，假设你是计算机程序 🤖 。

当你在排队时，你只是闲着😴， 轮到你前不做任何事情（仅排队）。但排队很快，因为收银员只接订单（不准备订单），所以这一切都还好。

然后，当轮到你时，需要你做一些实际性的工作，比如查看菜单，决定你想要什么，让你的恋人选择，支付，检查你是否提供了正确的账单或卡，检查你的收费是否正确，检查订单是否有正确的项目，等等。

此时，即使你仍然没有汉堡，你和收银员的工作也"暂停"了⏸， 因为你必须等待一段时间 🕙 让你的汉堡做好。

但是，当你离开柜台并坐在桌子旁，在轮到你的号码前的这段时间，你可以将焦点切换到 🔀 你的恋人上，并做一些"工作"⏯ 🤓。你可以做一些非常"有成效"的事情，比如和你的恋人调情😍.

之后，收银员 💁 把号码显示在显示屏上，并说到 "汉堡做好了"，而当显示的号码是你的号码时，你不会立刻疯狂地跳起来。因为你知道没有人会偷你的汉堡，因为你有你的号码，而其他人又有他们自己的号码。

所以你要等待你的恋人完成故事（完成当前的工作⏯ /正在做的事🤓)， 轻轻微笑，说你要吃汉堡⏸.

然后你去柜台🔀， 到现在初始任务已经完成⏯， 拿起汉堡，说声谢谢，然后把它们送到桌上。这就完成了与计数器交互的步骤/任务⏹. 这反过来又产生了一项新任务，即"吃汉堡"🔀 ⏯， 上一个"拿汉堡"的任务已经结束了⏹.

### 并行汉堡

现在让我们假设不是"并发汉堡"，而是"并行汉堡"。

你和你的恋人一起去吃并行快餐。

你站在队伍中，同时是厨师的几个收银员（比方说8个）从前面的人那里接单。

你之前的每个人都在等待他们的汉堡准备好后才离开柜台，因为8名收银员都会在下一份订单前马上准备好汉堡。

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

然后，终于轮到你了，你为你的恋人和你订购了两个非常精美的汉堡。

你付钱了 💸。

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

收银员去厨房。

你站在柜台前 🕙等待着，这样就不会有人在你之前抢走你的汉堡，因为没有轮流的号码。

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

当你和你的恋人忙于不让任何人出现在你面前，并且在他们到来的时候拿走你的汉堡时，你无法关注到你的恋人。😞

这是"同步"的工作，你被迫与服务员/厨师 👨‍🍳"同步"。你在此必须等待 🕙 ，在收银员/厨师 👨‍🍳 完成汉堡并将它们交给你的确切时间到达之前一直等待，否则其他人可能会拿走它们。

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

你经过长时间的等待 🕙 ，收银员/厨师 👨‍🍳终于带着汉堡回到了柜台。

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

你拿着汉堡，和你的情人一起上桌。

你们仅仅是吃了它们，就结束了。⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

没有太多的交谈或调情，因为大部分时间 🕙 都在柜台前等待😞。

/// info

漂亮的插画来自 <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

///

---

在这个并行汉堡的场景中，你是一个计算机程序 🤖 且有两个处理器（你和你的恋人），都在等待 🕙 ，并投入他们的注意力 ⏯ 在柜台上等待了很长一段时间。

这家快餐店有 8 个处理器（收银员/厨师）。而并发汉堡店可能只有 2 个（一个收银员和一个厨师）。

但最终的体验仍然不是最好的。😞

---

这将是与汉堡的类似故事。🍔

一种更"贴近生活"的例子，想象一家银行。

直到最近，大多数银行都有多个出纳员 👨‍💼👨‍💼👨‍💼👨‍💼 还有一条长长排队队伍🕙🕙🕙🕙🕙🕙🕙🕙。

所有收银员都是一个接一个的在客户面前做完所有的工作👨‍💼⏯.

你必须经过 🕙 较长时间排队，否则你就没机会了。

你可不会想带你的恋人 😍 和你一起去银行办事🏦.

### 汉堡结论

在"你与恋人一起吃汉堡"的这个场景中，因为有很多人在等待🕙， 使用并发系统更有意义⏸🔀⏯.

大多数 Web 应用都是这样的。

你的服务器正在等待很多很多用户通过他们不太好的网络发送来的请求。

然后再次等待 🕙 响应回来。

这个"等待" 🕙 是以微秒为单位测量的，但总的来说，最后还是等待很久。

这就是为什么使用异步对于 Web API 很有意义的原因 ⏸🔀⏯。

这种异步机制正是 NodeJS 受到欢迎的原因（尽管 NodeJS 不是并行的），以及 Go 作为编程语言的优势所在。

这与 **FastAPI** 的性能水平相同。

你可以同时拥有并行性和异步性，你可以获得比大多数经过测试的 NodeJS 框架更高的性能，并且与 Go 不相上下， Go 是一种更接近于 C 的编译语言（<a href="https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">全部归功于 Starlette</a>）。

### 并发比并行好吗？

不！这不是故事的本意。

并发不同于并行。而是在需要大量等待的特定场景下效果更好。因此，在 Web 应用程序开发中，它通常比并行要好得多，但这并不意味着全部。

因此，为了平衡这一点，想象一下下面的短篇故事：

> 你必须打扫一个又大又脏的房子。

*是的，这就是完整的故事。*

---

在任何地方， 都不需要等待 🕙 ，只需要在房子的多个地方做着很多工作。

你可以像汉堡的例子那样轮流执行，先是客厅，然后是厨房，但因为你不需要等待 🕙 ，对于任何事情都是清洁，清洁，还是清洁，轮流不会影响任何事情。

无论是否轮流执行（并发），都需要相同的时间来完成，而你也会完成相同的工作量。

但在这种情况下，如果你能带上 8 名前收银员/厨师，现在是清洁工一起清扫，他们中的每一个人（加上你）都能占据房子的一个区域来清扫，你就可以在额外的帮助下并行的更快地完成所有工作。

在这个场景中，每个清洁工（包括你）都将是一个处理器，完成这个工作的一部分。

由于大多数执行时间是由实际工作（而不是等待）占用的，并且计算机中的工作是由 <abbr title="Central Processing Unit">CPU</abbr> 完成的，所以他们称这些问题为"CPU 密集型"。

---

CPU 密集型操作的常见示例是需要复杂的数学处理。

例如：

* **音频**或**图像**处理；
* **计算机视觉**: 一幅图像由数百万像素组成，每个像素有3种颜色值，处理通常需要同时对这些像素进行计算；
* **机器学习**: 它通常需要大量的"矩阵"和"向量"乘法。想象一个包含数字的巨大电子表格，并同时将所有数字相乘；
* **深度学习**: 这是机器学习的一个子领域，同样适用。只是没有一个数字的电子表格可以相乘，而是一个庞大的数字集合，在很多情况下，你需要使用一个特殊的处理器来构建和使用这些模型。

### 并发 + 并行: Web + 机器学习

使用 **FastAPI**，你可以利用 Web 开发中常见的并发机制的优势（NodeJS 的主要吸引力）。

并且，你也可以利用并行和多进程（让多个进程并行运行）的优点来处理与机器学习系统中类似的 **CPU 密集型** 工作。

这一点，再加上 Python 是**数据科学**、机器学习（尤其是深度学习）的主要语言这一简单事实，使得 **FastAPI** 与数据科学/机器学习 Web API 和应用程序（以及其他许多应用程序）非常匹配。

了解如何在生产环境中实现这种并行性，可查看此文 [Deployment](deployment/index.md){.internal-link target=_blank}。

## `async` 和 `await`

现代版本的 Python 有一种非常直观的方式来定义异步代码。这使它看起来就像正常的"顺序"代码，并在适当的时候"等待"。

当有一个操作需要等待才能给出结果，且支持这个新的 Python 特性时，你可以编写如下代码：

```Python
burgers = await get_burgers(2)
```

这里的关键是 `await`。它告诉 Python 它必须等待 ⏸ `get_burgers(2)` 完成它的工作 🕙 ，然后将结果存储在 `burgers` 中。这样，Python 就会知道此时它可以去做其他事情 🔀 ⏯ （比如接收另一个请求）。

要使 `await` 工作，它必须位于支持这种异步机制的函数内。因此，只需使用 `async def` 声明它：

```Python hl_lines="1"
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```

...而不是 `def`:

```Python hl_lines="2"
# This is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff to create the burgers
    return burgers
```

使用 `async def`，Python 就知道在该函数中，它将遇上 `await`，并且它可以"暂停" ⏸ 执行该函数，直至执行其他操作 🔀 后回来。

当你想调用一个 `async def` 函数时，你必须"等待"它。因此，这不会起作用：

```Python
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
```

---

因此，如果你使用的库告诉你可以使用 `await` 调用它，则需要使用 `async def` 创建路径操作函数 ，如：

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### 更多技术细节

你可能已经注意到，`await` 只能在 `async def` 定义的函数内部使用。

但与此同时，必须"等待"通过 `async def` 定义的函数。因此，带 `async def` 的函数也只能在 `async def` 定义的函数内部调用。

那么，这关于先有鸡还是先有蛋的问题，如何调用第一个 `async` 函数？

如果你使用 **FastAPI**，你不必担心这一点，因为"第一个"函数将是你的路径操作函数，FastAPI 将知道如何做正确的事情。

但如果你想在没有 FastAPI 的情况下使用 `async` / `await`，则可以这样做。

### 编写自己的异步代码

Starlette （和 **FastAPI**） 是基于 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> 实现的，这使得它们可以兼容 Python 的标准库 <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a> 和 <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a>。

特别是，你可以直接使用 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> 来处理高级的并发用例，这些用例需要在自己的代码中使用更高级的模式。

即使你没有使用 **FastAPI**，你也可以使用 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> 编写自己的异步程序，使其拥有较高的兼容性并获得一些好处（例如， 结构化并发）。

我（指原作者 —— 译者注）基于 AnyIO 新建了一个库，作为一个轻量级的封装层，用来优化类型注解，同时提供了更好的**自动补全**、**内联错误提示**等功能。这个库还附带了一个友好的入门指南和教程，能帮助你**理解**并编写**自己的异步代码**：<a href="https://asyncer.tiangolo.com/" class="external-link" target="_blank">Asyncer</a>。如果你有**结合使用异步代码和常规**（阻塞/同步）代码的需求，这个库会特别有用。

### 其他形式的异步代码

这种使用 `async` 和 `await` 的风格在语言中相对较新。

但它使处理异步代码变得容易很多。

这种相同的语法（或几乎相同）最近也包含在现代版本的 JavaScript 中（在浏览器和 NodeJS 中）。

但在此之前，处理异步代码非常复杂和困难。

在以前版本的 Python，你可以使用多线程或者 <a href="https://www.gevent.org/" class="external-link" target="_blank">Gevent</a>。但代码的理解、调试和思考都要复杂许多。

在以前版本的 NodeJS / 浏览器 JavaScript 中，你会使用"回调"，因此也可能导致“回调地狱”。

## 协程

**协程**只是 `async def` 函数返回的一个非常奇特的东西的称呼。Python 知道它有点像一个函数，它可以启动，也会在某个时刻结束，而且它可能会在内部暂停 ⏸ ，只要内部有一个 `await`。

通过使用 `async` 和 `await` 的异步代码的所有功能大多数被概括为"协程"。它可以与 Go 的主要关键特性 "Goroutines" 相媲美。

## 结论

让我们再来回顾下上文所说的：

> Python 的现代版本可以通过使用 `async` 和 `await` 语法创建**协程**，并用于支持**异步代码**。

现在应该能明白其含义了。✨

所有这些使得 FastAPI（通过 Starlette）如此强大，也是它拥有如此令人印象深刻的性能的原因。

## 非常技术性的细节

/// warning

你可以跳过这里。

这些都是 FastAPI 如何在内部工作的技术细节。

如果你有相当多的技术知识（协程、线程、阻塞等），并且对 FastAPI 如何处理 `async def` 与常规 `def` 感到好奇，请继续。

///

### 路径操作函数

当你使用 `def` 而不是 `async def` 来声明一个*路径操作函数*时，它运行在外部的线程池中并等待其结果，而不是直接调用（因为它会阻塞服务器）。

如果你使用过另一个不以上述方式工作的异步框架，并且你习惯于用普通的 `def` 定义普通的仅计算路径操作函数，以获得微小的性能增益（大约100纳秒），请注意，在 FastAPI 中，效果将完全相反。在这些情况下，最好使用 `async def`，除非路径操作函数内使用执行阻塞 <abbr title="输入/输出：磁盘读写，网络通讯.">I/O</abbr> 的代码。

在这两种情况下，与你之前的框架相比，**FastAPI** 可能[仍然很快](index.md#_11){.internal-link target=_blank}。

### 依赖

这同样适用于[依赖](tutorial/dependencies/index.md){.internal-link target=_blank}。如果一个依赖是标准的 `def` 函数而不是 `async def`，它将被运行在外部线程池中。

### 子依赖

你可以拥有多个相互依赖的依赖以及[子依赖](tutorial/dependencies/sub-dependencies.md){.internal-link target=_blank} （作为函数的参数），它们中的一些可能是通过 `async def` 声明，也可能是通过 `def` 声明。它们仍然可以正常工作，这些通过 `def` 声明的函数将会在外部线程中调用（来自线程池），而不是"被等待"。

### 其他函数

你可直接调用通过 `def` 或 `async def` 创建的任何其他函数，FastAPI 不会影响你调用它们的方式。

这与 FastAPI 为你调用*路径操作函数*和依赖项的逻辑相反。

如果你的函数是通过 `def` 声明的，它将被直接调用（在代码中编写的地方），而不会在线程池中，如果这个函数通过 `async def` 声明，当在代码中调用时，你就应该使用 `await` 等待函数的结果。

---

再次提醒，这些是非常技术性的细节，如果你来搜索它可能对你有用。

否则，你最好应该遵守的指导原则<a href="#_1">赶时间吗？</a>.
