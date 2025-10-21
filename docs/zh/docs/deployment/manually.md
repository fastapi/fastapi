# 手动运行服务器

## 使用 `fastapi run` 命令

简而言之，使用 `fastapi run` 来运行您的 FastAPI 应用程序：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

这在大多数情况下都能正常运行。😎

例如，您可以使用该命令在容器、服务器等环境中启动您的 **FastAPI** 应用。

## ASGI 服务器

让我们深入了解一些细节。

FastAPI 使用了一种用于构建 Python Web 框架和服务器的标准，称为 <abbr title="Asynchronous Server Gateway Interface，异步服务器网关接口">ASGI</abbr>。FastAPI 本质上是一个 ASGI Web 框架。

要在远程服务器上运行 **FastAPI** 应用（或任何其他 ASGI 应用），您需要一个 ASGI 服务器程序，例如 **Uvicorn**。它是 `fastapi` 命令默认使用的 ASGI 服务器。

除此之外，还有其他一些可选的 ASGI 服务器，例如：

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>：高性能 ASGI 服务器。
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>：与 HTTP/2 和 Trio 等兼容的 ASGI 服务器。
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>：为 Django Channels 构建的 ASGI 服务器。
* <a href="https://github.com/emmett-framework/granian" class="external-link" target="_blank">Granian</a>：基于 Rust 的 HTTP 服务器，专为 Python 应用设计。
* <a href="https://unit.nginx.org/howto/fastapi/" class="external-link" target="_blank">NGINX Unit</a>：NGINX Unit 是一个轻量级且灵活的 Web 应用运行时环境。

## 服务器主机和服务器程序

关于名称，有一个小细节需要记住。 💡

“**服务器**”一词通常用于指远程/云计算机（物理机或虚拟机）以及在该计算机上运行的程序（例如 Uvicorn）。

请记住，当您一般读到“服务器”这个名词时，它可能指的是这两者之一。

当提到远程主机时，通常将其称为**服务器**，但也称为**机器**(machine)、**VM**（虚拟机）、**节点**。 这些都是指某种类型的远程计算机，通常运行 Linux，您可以在其中运行程序。


## 安装服务器程序

当您安装 FastAPI 时，它自带一个生产环境服务器——Uvicorn，并且您可以使用 `fastapi run` 命令来启动它。

不过，您也可以手动安装 ASGI 服务器。

请确保您创建并激活一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，然后再安装服务器应用程序。

例如，要安装 Uvicorn，可以运行以下命令：

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

类似的流程也适用于任何其他 ASGI 服务器程序。

/// tip

通过添加 `standard` 选项，Uvicorn 将安装并使用一些推荐的额外依赖项。

其中包括 `uvloop`，这是 `asyncio` 的高性能替代方案，能够显著提升并发性能。

当您使用 `pip install "fastapi[standard]"` 安装 FastAPI 时，实际上也会安装 `uvicorn[standard]`。

///

## 运行服务器程序

如果您手动安装了 ASGI 服务器，通常需要以特定格式传递一个导入字符串，以便服务器能够正确导入您的 FastAPI 应用：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note

命令 `uvicorn main:app` 的含义如下：

* `main`：指的是 `main.py` 文件（即 Python “模块”）。
* `app`：指的是 `main.py` 文件中通过 `app = FastAPI()` 创建的对象。

它等价于以下导入语句：

```Python
from main import app
```

///

每种 ASGI 服务器程序通常都会有类似的命令，您可以在它们的官方文档中找到更多信息。

/// warning

Uvicorn 和其他服务器支持 `--reload` 选项，该选项在开发过程中非常有用。

但 `--reload` 选项会消耗更多资源，且相对不稳定。

它对于**开发阶段**非常有帮助，但在**生产环境**中**不应该**使用。

///

## 部署概念

这些示例运行服务器程序（例如 Uvicorn），启动**单个进程**，在所有 IP（`0.0.0.0`）上监听预定义端口（例如`80`）。

这是基本思路。 但您可能需要处理一些其他事情，例如：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* 复制（运行的进程数）
* 内存
* 开始前的步骤

在接下来的章节中，我将向您详细介绍每个概念、如何思考它们，以及一些具体示例以及处理它们的策略。 🚀
