# 环境变量 { #environment-variables }

/// tip | 提示

如果你已经知道什么是“环境变量”以及如何使用它们，可以放心跳过这一部分。

///

环境变量（也称为“**env var**”）是一个存在于 Python 代码**之外**、位于**操作系统**中的变量，你的 Python 代码（或其他程序）都可以读取它。

环境变量可用于处理应用程序**设置**、作为 Python **安装**的一部分等。

## 创建和使用环境变量 { #create-and-use-env-vars }

你可以在 **shell（终端）**中**创建**和使用环境变量，而不需要用到 Python：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// You could create an env var MY_NAME with
$ export MY_NAME="Wade Wilson"

// Then you could use it with other programs, like
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Create an env var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Use it with other programs, like
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## 在 Python 中读取环境变量 { #read-env-vars-in-python }

你也可以在 Python **之外**的终端中创建环境变量（或使用任何其他方法），然后在 Python 中**读取**它们。

例如，你可以创建一个名为 `main.py` 的文件，其中包含以下内容：

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | 提示

<a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> 的第二个参数是默认返回值。

如果未提供，默认值是 `None`；这里我们提供 `"World"` 作为要使用的默认值。

///

然后你可以调用这个 Python 程序：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ export MY_NAME="Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ $Env:MY_NAME = "Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

由于环境变量可以在代码之外设置、但可以被代码读取，并且不必与其他文件一起存储（提交到 `git`），因此通常用于配置或**设置**。

你还可以为**特定的程序调用**创建仅对该程序可用、且只在其运行期间有效的环境变量。

要实现这一点，只需在同一行内、程序本身之前创建它：

<div class="termy">

```console
// Create an env var MY_NAME in line for this program call
$ MY_NAME="Wade Wilson" python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python

// The env var no longer exists afterwards
$ python main.py

Hello World from Python
```

</div>

/// tip | 提示

你可以在 <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a> 中了解更多信息。

///

## 类型和验证 { #types-and-validation }

这些环境变量只能处理**文本字符串**，因为它们存在于 Python 之外，并且必须与其他程序以及系统的其余部分兼容（甚至要与不同的操作系统兼容，例如 Linux、Windows、macOS）。

这意味着从环境变量中读取的**任何值**在 Python 中**都会是 `str`**，任何到其他类型的转换或任何验证都必须在代码中完成。

你将在[高级用户指南 - 设置和环境变量](./advanced/settings.md){.internal-link target=_blank}中了解更多关于使用环境变量处理**应用程序设置**的信息。

## `PATH` 环境变量 { #path-environment-variable }

有一个**特殊的**环境变量称为 **`PATH`**，操作系统（Linux、macOS、Windows）用它来查找要运行的程序。

`PATH` 变量的值是一个长字符串，由 Linux 和 macOS 上用冒号 `:` 分隔的目录组成，而在 Windows 上则是由分号 `;` 分隔的目录组成。

例如，`PATH` 环境变量可能如下所示：

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

这意味着系统应该在以下目录中查找程序：

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

这意味着系统应该在以下目录中查找程序：

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

当你在终端中输入一个**命令**时，操作系统会在 `PATH` 环境变量中列出的**每个目录**中**查找**该程序。

例如，当你在终端中输入 `python` 时，操作系统会在该列表中的**第一个目录**中查找名为 `python` 的程序。

如果找到了，它就会**使用它**；否则，它会继续在**其他目录**中查找。

### 安装 Python 并更新 `PATH` { #installing-python-and-updating-the-path }

安装 Python 时，可能会询问你是否要更新 `PATH` 环境变量。

//// tab | Linux, macOS

假设你安装 Python，并最终将其安装在目录 `/opt/custompython/bin` 中。

如果你同意更新 `PATH` 环境变量，那么安装程序将会把 `/opt/custompython/bin` 添加到 `PATH` 环境变量中。

它可能如下所示：

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

这样，当你在终端中输入 `python` 时，系统会在 `/opt/custompython/bin`（最后一个目录）中找到 Python 程序并使用它。

////

//// tab | Windows

假设你安装 Python，并最终将其安装在目录 `C:\opt\custompython\bin` 中。

如果你同意更新 `PATH` 环境变量，那么安装程序将会把 `C:\opt\custompython\bin` 添加到 `PATH` 环境变量中。

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

这样，当你在终端中输入 `python` 时，系统会在 `C:\opt\custompython\bin`（最后一个目录）中找到 Python 程序并使用它。

////

因此，如果你输入：

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

系统会在 `/opt/custompython/bin` 中**找到** `python` 程序并运行它。

这大致等价于输入：

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

系统会在 `C:\opt\custompython\bin\python` 中**找到** `python` 程序并运行它。

这大致等价于输入：

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

在学习[虚拟环境](virtual-environments.md){.internal-link target=_blank}时，这些信息会很有用。

## 结论 { #conclusion }

到这里，你应该对**环境变量**是什么以及如何在 Python 中使用它们有了基本的了解。

你也可以在 <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia for Environment Variable</a> 中了解更多相关信息。

在很多情况下，环境变量如何能立即派上用场、以及如何适用，并不是很明显。但在你进行开发时，它们会在许多不同的场景中不断出现，所以了解它们是很有必要的。

例如，你将在下一节关于[虚拟环境](virtual-environments.md)中需要这些信息。
