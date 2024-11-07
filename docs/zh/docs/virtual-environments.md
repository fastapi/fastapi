# 虚拟环境

当你在 Python 项目中工作时，你可能会有必要用到一个**虚拟环境**（或类似的机制）来隔离你为每个项目安装的包。

/// info

如果你已经了解虚拟环境，知道如何创建和使用它们，你可以考虑跳过这一部分。🤓

///

/// tip

**虚拟环境**和**环境变量**是不同的。

**环境变量**是系统中的一个变量，可以被程序使用。

**虚拟环境**是一个包含一些文件的目录。

///

/// info

这个页面将教你如何使用**虚拟环境**以及了解它们的工作原理。

如果你计划使用一个**可以为你管理一切的工具**（包括安装 Python），试试 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a>。

///

## 创建一个工程

首先，为你的工程创建一个目录。

我 (指原作者 —— 译者注) 通常会在我的主目录下创建一个名为 `code` 的目录。

在这个目录下，我再为每个工程创建一个目录。

<div class="termy">

```console
// 进入主目录
$ cd
// 创建一个用于存放所有代码工程的目录
$ mkdir code
// 进入 code 目录
$ cd code
// 创建一个用于存放这个工程的目录
$ mkdir awesome-project
// 进入这个工程的目录
$ cd awesome-project
```

</div>

## 创建一个虚拟环境

在开始一个 Python 工程的**第一时间**，**<abbr title="还有其他做法，此处仅作一个简单的指南">在你的工程内部</abbr>**创建一个虚拟环境。

/// tip

你只需要 **在每个工程中操作一次**，而不是每次工作时都操作。

///

//// tab | `venv`

你可以使用 Python 自带的 `venv` 模块来创建一个虚拟环境。

<div class="termy">

```console
$ python -m venv .venv
```

</div>

/// details | 上述命令的含义

* `python`: 使用名为 `python` 的程序
* `-m`: 以脚本的方式调用一个模块，我们将告诉它接下来使用哪个模块
* `venv`: 使用名为 `venv` 的模块，这个模块通常随 Python 一起安装
* `.venv`: 在新目录 `.venv` 中创建虚拟环境

///

////

//// tab | `uv`

如果你安装了 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a>，你也可以使用它来创建一个虚拟环境。

<div class="termy">

```console
$ uv venv
```

</div>

/// tip

默认情况下，`uv` 会在一个名为 `.venv` 的目录中创建一个虚拟环境。

但你可以通过传递一个额外的参数来自定义它，指定目录的名称。

///

////

这个命令会在一个名为 `.venv` 的目录中创建一个新的虚拟环境。

/// details | `.venv`，或是其他名称

你可以在不同的目录下创建虚拟环境，但通常我们会把它命名为 `.venv`。

///

## 激活虚拟环境

激活新的虚拟环境来确保你运行的任何 Python 命令或安装的包都能使用到它。

/// tip

**每次**开始一个 **新的终端会话** 来工作在这个工程时，你都需要执行这个操作。

///

//// tab | Linux, macOS

<div class="termy">

```console
$ source .venv/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .venv\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

或者，如果你在 Windows 上使用 Bash（例如 <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>）：

<div class="termy">

```console
$ source .venv/Scripts/activate
```

</div>

////

/// tip

每次你在这个环境中安装一个 **新的包** 时，都需要 **重新激活** 这个环境。

这么做确保了当你使用一个由这个包安装的 **终端（<abbr title="命令行界面">CLI</abbr>）程序** 时，你使用的是你的虚拟环境中的程序，而不是全局安装、可能版本不同的程序。

///

## 检查虚拟环境是否激活

检查虚拟环境是否激活 (前面的命令是否生效)。

/// tip

这是 **可选的**，但这是一个很好的方法，可以 **检查** 一切是否按预期工作，以及你是否使用了你打算使用的虚拟环境。

///

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
$ which python

/home/user/code/awesome-project/.venv/bin/python
```

</div>

如果它显示了在你工程 (在这个例子中是 `awesome-project`) 的 `.venv/bin/python` 中的 `python` 二进制文件，那么它就生效了。🎉

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ Get-Command python

C:\Users\user\code\awesome-project\.venv\Scripts\python
```

</div>

如果它显示了在你工程 (在这个例子中是 `awesome-project`) 的 `.venv\Scripts\python` 中的 `python` 二进制文件，那么它就生效了。🎉

////

## 升级 `pip`

/// tip

如果你使用 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a> 来安装内容，而不是 `pip`，那么你就不需要升级 `pip`。😎

///

如果你使用 `pip` 来安装包（它是 Python 的默认组件），你应该将它 **升级** 到最新版本。

在安装包时出现的许多奇怪的错误都可以通过先升级 `pip` 来解决。

/// tip

通常你只需要在创建虚拟环境后 **执行一次** 这个操作。

///

确保虚拟环境是激活的 (使用上面的命令)，然后运行：

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

## 添加 `.gitignore`

如果你使用 **Git** (这是你应该使用的)，添加一个 `.gitignore` 文件来排除你的 `.venv` 中的所有内容。

/// tip

如果你使用 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a> 来创建虚拟环境，它会自动为你完成这个操作，你可以跳过这一步。😎

///

/// tip

通常你只需要在创建虚拟环境后 **执行一次** 这个操作。

///

<div class="termy">

```console
$ echo "*" > .venv/.gitignore
```

</div>

/// details | 上述命令的含义

* `echo "*"`: 将在终端中 "打印" 文本 `*`（接下来的部分会对这个操作进行一些修改）
* `>`: 使左边的命令打印到终端的任何内容实际上都不会被打印，而是会被写入到右边的文件中
* `.gitignore`: 被写入文本的文件的名称

而 `*` 对于 Git 来说意味着 "所有内容"。所以，它会忽略 `.venv` 目录中的所有内容。

该命令会创建一个名为 `.gitignore` 的文件，内容如下：

```gitignore
*
```
