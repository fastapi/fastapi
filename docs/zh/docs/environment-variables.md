# 环境变量

/// tip

如果您已经知道什么是“环境变量”以及如何使用它们，请随意跳过此部分。

///

环境变量（有时也被称为" **env var** "）是在种存在于Python代码 **外面** 的变量, 例如在 **操作系统** 中。它可以被Python代码读取，当然也可以被其他程序读取。

环境变量在处理应用 **设置** 时非常有用，例如在 **安装** Python时。

## 创建和使用环境变量

你可以在 **终端或命令行** 中 **创建** 和使用环境变量，而不需要打开Python。

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 你可以使用以下命令创建环境变量 MY_NAME
$ export MY_NAME="Wade Wilson"

// 然后你可以将它与其他程序一起使用，例如
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 创建一个环境变量 MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// 与其他程序一起使用，例如
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## 在 Python 中读取环境变量

您还可以在 Python **外部**、在终端中（或使用任何其他方法）创建环境变量，然后 **在Python中读取它们** 。

例如，你可以有一个文件“main.py”，其中包含：

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

第二个参数 <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> 是一个默认返回的参数。

如果没有提供，默认为 `None`，这里我们提供 `"World"` 作为默认值。

///

然后你可以调用该 Python 程序：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// 这里我们还没有设置环境变量
$ python main.py

// 由于我们没有设置环境变量，因此我们获得默认值

Hello World from Python

// 但是如果我们先创建一个环境变量
$ export MY_NAME="Wade Wilson"

// 然后再次调用程序
$ python main.py

// 现在它可以读取环境变量

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// 这里我们还没有设置环境变量
$ python main.py

// 由于我们没有设置环境变量，因此我们获得默认值

Hello World from Python

// 但是如果我们先创建一个环境变量
$ $Env:MY_NAME = "Wade Wilson"

// 然后再次调用程序
$ python main.py

// 现在它可以读取环境变量

Hello Wade Wilson from Python
```

</div>

////

由于环境变量可以在代码之外设置，同时可以由代码读取。它不必与其余文件一起存储（例如，提交给“git”时）。因此常被用于配置或 **设置** 。

您还可以仅为 **特定程序调用** 创建环境变量，该变量仅对该程序可用。同时，它仅在其设定的时间内可用。

因此，请在程序编写之前创建。请参看以下例子：

<div class="termy">

```console
// 为`main.py`的程序创建一个可调用的环境变量 MY_NAME
$ MY_NAME="Wade Wilson" python main.py

// 现在它可以读取环境变量

Hello Wade Wilson from Python

// 调用一次后环境变量就失效了
$ python main.py

Hello World from Python
```

</div>

/// tip

你可以在这里了解更多 <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## 类型和变量

这些环境变量只能处理 **文本字符串** ，因为它们是 Python 外部的。同时，它必须与其他程序和系统的其余部分兼容（甚至与不同的操作系统，如 Linux、Windows、macOS）。

这意味着使用 Python 读取的环境变量，其所包含的 **任何值** 都将是 **`str`** 类型。并且它在 Python 中执行的任何类型转换或任何验证都必须在您编写的代码中完成。

您可以在[Advanced User Guide - Settings and Environment Variables](./advanced/settings.md){.internal-link target=_blank}了解更多为**应用设置**提供环境变量的信息。

## `PATH` 环境变量

这是一个被称为**`PATH`**的**特殊**环境变量。它被操作系统（如 Linux、macOS、Windows）用来查找要运行的程序。

变量 `PATH` 的值是一个长字符串。它是一个路径列表，在 Linux 和 macOS 上用冒号 `:` ，在 Windows 上用分号 `;` 分隔。

例如，`PATH`环境变量可以写成以下形式:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

这表示系统应该在以下路径中寻找程序：

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

这表示系统应该在以下路径中寻找程序：

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

当你在终端中输入一个**命令**时，操作系统会在`PATH`**环境变量中列出的**每个路径中**查找**程序。

例如，当你在命令行中输入`python`时，操作系统会在列出的**第一个路径**中查找叫`python`的程序。

如果找到了，它就会**执行**它。否则它会继续在**其他路径**中查找。

### 安装Python及更新`PATH`

当你安装Python时，你可能被要求是否要更新`PATH`环境变量。

//// tab | Linux, macOS

假设您安装了 Python 并且它最终位于路径`/opt/custompython/bin`中。

如果您同意更新`PATH`环境变量，那么安装程序将把`/opt/custompython/bin`添加到`PATH`环境变量中。

它显示为这样：

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

现在，当你在终端中输入`python`，系统将在`/opt/custompython/bin`路径中查找`python`程序，并调用它。

////

//// tab | Windows

假设您安装了 Python 并且它最终位于路径`C:\opt\custompython\bin`中。

如果您同意更新`PATH`环境变量，那么安装程序将把`C:\opt\custompython\bin`添加到`PATH`环境变量中。

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

现在，当你在终端中输入`python`，系统将在`C:\opt\custompython\bin`路径中查找`python`程序，并调用它。

////

现在，当你在终端中输入`python`，系统将在`/opt/custompython/bin`（最后一个路径）路径中查找`python`程序，并调用它。

那么，您输入：

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

系统将在`/opt/custompython/bin`**查找**`python`并运行它。

这相当于输入：

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

系统将在`C:\opt\custompython\bin\python`**查找**`python`并运行它。

这相当于输入：

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

当您想学习更多关于[Virtual Environments](virtual-environments.md){.internal-link target=_blank}的知识，请继续阅读。

## 结论

通过上面的内容，您应该对什么是**环境变量**以及如何在 Python 中使用它们有一个基本的了解。

您可以在<a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia for Environment Variable</a>了解更多信息。

在多数情况下，环境变量如何发挥作用，以及如何被应用在程序中并不明显。但在开发过程中，它们会不断出现在许多不同的场景中，因此了解它们是有益的。

例如，在下一节中，您将会学习到 [Virtual Environments](virtual-environments.md)。
