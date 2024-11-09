# 环境变量

/// tip

如果你已经知道什么是“环境变量”并且知道如何使用它们，你可以放心跳过这一部分。

///

环境变量（也称为“**env var**”）是一个独立于 Python 代码**之外**的变量，它存在于**操作系统**中，可以被你的 Python 代码（或其他程序）读取。

环境变量对于处理应用程序**设置**、作为 Python **安装**的一部分等方面非常有用。

## 创建和使用环境变量

你在 **shell（终端）**中就可以**创建**和使用环境变量，并不需要用到 Python：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 你可以使用以下命令创建一个名为 MY_NAME 的环境变量
$ export MY_NAME="Wade Wilson"

// 然后，你可以在其他程序中使用它，例如
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 创建一个名为 MY_NAME 的环境变量
$ $Env:MY_NAME = "Wade Wilson"

// 在其他程序中使用它，例如
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## 在 Python 中读取环境变量

你也可以在 Python **之外**的终端中创建环境变量（或使用任何其他方法），然后在 Python 中**读取**它们。

例如，你可以创建一个名为 `main.py` 的文件，其中包含以下内容：

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

第二个参数是 <a href="https://docs.python.org/zh-cn/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> 的默认返回值。

如果没有提供，默认值为 `None`，这里我们提供 `"World"` 作为默认值。

///

然后你可以调用这个 Python 程序：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 这里我们还没有设置环境变量
$ python main.py

// 因为我们没有设置环境变量，所以我们得到的是默认值

Hello World from Python

// 但是如果我们事先创建过一个环境变量
$ export MY_NAME="Wade Wilson"

// 然后再次调用程序
$ python main.py

// 现在就可以读取到环境变量了

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 这里我们还没有设置环境变量
$ python main.py

// 因为我们没有设置环境变量，所以我们得到的是默认值

Hello World from Python

// 但是如果我们事先创建过一个环境变量
$ $Env:MY_NAME = "Wade Wilson"

// 然后再次调用程序
$ python main.py

// 现在就可以读取到环境变量了

Hello Wade Wilson from Python
```

</div>

////

由于环境变量可以在代码之外设置、但可以被代码读取，并且不必与其他文件一起存储（提交到 `git`），因此通常用于配置或**设置**。

你还可以为**特定的程序调用**创建特定的环境变量，该环境变量仅对该程序可用，且仅在其运行期间有效。

要实现这一点，只需在同一行内、程序本身之前创建它：

<div class="termy">

```console
// 在这个程序调用的同一行中创建一个名为 MY_NAME 的环境变量
$ MY_NAME="Wade Wilson" python main.py

// 现在就可以读取到环境变量了

Hello Wade Wilson from Python

// 在此之后这个环境变量将不会依然存在
$ python main.py

Hello World from Python
```

</div>

/// tip

你可以在 <a href="https://12factor.net/zh_cn/config" class="external-link" target="_blank">The Twelve-Factor App: 配置</a>中了解更多信息。

///

## 类型和验证

这些环境变量只能处理**文本字符串**，因为它们是处于 Python 范畴之外的，必须与其他程序和操作系统的其余部分兼容（甚至与不同的操作系统兼容，如 Linux、Windows、macOS）。

这意味着从环境变量中读取的**任何值**在 Python 中都将是一个 `str`，任何类型转换或验证都必须在代码中完成。

你将在[高级用户指南 - 设置和环境变量](./advanced/settings.md)中了解更多关于使用环境变量处理**应用程序设置**的信息。

## `PATH` 环境变量

有一个**特殊的**环境变量称为 **`PATH`**，操作系统（Linux、macOS、Windows）用它来查找要运行的程序。

`PATH` 变量的值是一个长字符串，由 Linux 和 macOS 上的冒号 `:` 分隔的目录组成，而在 Windows 上则是由分号 `;` 分隔的。

例如，`PATH` 环境变量可能如下所示：

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

这意味着系统应该在以下目录中查找程序：

-   `/usr/local/bin`
-   `/usr/bin`
-   `/bin`
-   `/usr/sbin`
-   `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

这意味着系统应该在以下目录中查找程序：

-   `C:\Program Files\Python312\Scripts`
-   `C:\Program Files\Python312`
-   `C:\Windows\System32`

////

当你在终端中输入一个**命令**时，操作系统会在 `PATH` 环境变量中列出的**每个目录**中**查找**程序。

例如，当你在终端中输入 `python` 时，操作系统会在该列表中的**第一个目录**中查找名为 `python` 的程序。

如果找到了，那么操作系统将**使用它**；否则，操作系统会继续在**其他目录**中查找。

### 安装 Python 和更新 `PATH`

安装 Python 时，可能会询问你是否要更新 `PATH` 环境变量。

//// tab | Linux, macOS

假设你安装 Python 并最终将其安装在了目录 `/opt/custompython/bin` 中。

如果你同意更新 `PATH` 环境变量，那么安装程序将会将 `/opt/custompython/bin` 添加到 `PATH` 环境变量中。

它看起来大概会像这样：

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

如此一来，当你在终端中输入 `python` 时，系统会在 `/opt/custompython/bin` 中找到 Python 程序（最后一个目录）并使用它。

////

//// tab | Windows

假设你安装 Python 并最终将其安装在了目录 `C:\opt\custompython\bin` 中。

如果你同意更新 `PATH` 环境变量 (在 Python 安装程序中，这个操作是名为 `Add Python x.xx to PATH` 的复选框 —— 译者注)，那么安装程序将会将 `C:\opt\custompython\bin` 添加到 `PATH` 环境变量中。

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

如此一来，当你在终端中输入 `python` 时，系统会在 `C:\opt\custompython\bin` 中找到 Python 程序（最后一个目录）并使用它。

////

因此，如果你输入：

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

系统会在 `/opt/custompython/bin` 中**找到** `python` 程序并运行它。

这和输入以下命令大致等价：

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

系统会在 `C:\opt\custompython\bin\python` 中**找到** `python` 程序并运行它。

这和输入以下命令大致等价：

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

当学习[虚拟环境](virtual-environments.md)时，这些信息将会很有用。

## 结论

通过这个教程，你应该对**环境变量**是什么以及如何在 Python 中使用它们有了基本的了解。

你也可以在<a href="https://zh.wikipedia.org/wiki/%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F" class="external-link" target="_blank">环境变量 - 维基百科</a> (<a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia for Environment Variable</a>) 中了解更多关于它们的信息。

在许多情况下，环境变量的用途和适用性并不是很明显。但是在开发过程中，它们会在许多不同的场景中出现，因此了解它们是很有必要的。

例如，你将在下一节关于[虚拟环境](virtual-environments.md)中需要这些信息。
