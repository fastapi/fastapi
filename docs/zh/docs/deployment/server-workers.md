# 服务器工作进程（Workers） - 使用 Uvicorn 的多工作进程模式 { #server-workers-uvicorn-with-workers }

让我们回顾一下之前的部署概念：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* **复制（运行的进程数）**
* 内存
* 启动前的先前步骤

到目前为止，在文档中的所有教程中，您可能一直是在运行一个**服务器程序**，例如使用 `fastapi` 命令来启动 Uvicorn，而它默认运行的是**单进程模式**。

部署应用程序时，您可能希望进行一些**进程复制**，以利用**多核** CPU 并能够处理更多请求。

正如您在上一章有关[部署概念](concepts.md)中看到的，您可以使用多种策略。

在本章节中，我将向您展示如何使用 `fastapi` 命令或直接使用 `uvicorn` 命令以**多工作进程模式**运行 **Uvicorn**。

/// info | 信息

如果您正在使用容器，例如 Docker 或 Kubernetes，我将在下一章中告诉您更多相关信息：[容器中的 FastAPI - Docker](docker.md)。

比较特别的是，在 **Kubernetes** 环境中运行时，您通常**不需要**使用多个工作进程，而是**每个容器运行一个 Uvicorn 进程**。不过，我会在本章节的后续部分详细介绍这一点。

///

## 多个工作进程 { #multiple-workers }

您可以使用 `--workers` 命令行选项来启动多个工作进程：

//// tab | `fastapi`

如果您使用 `fastapi` 命令：

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

如果您更想要直接使用 `uvicorn` 命令：

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

这里唯一的新选项是 `--workers` 告诉 Uvicorn 启动 4 个工作进程。

您还可以看到它显示了每个进程的 **PID**，父进程（这是**进程管理器**）的 PID 为`27365`，每个工作进程的 PID 为：`27368`、`27369`， `27370`和`27367`。

## 部署概念 { #deployment-concepts }

在这里，您学习了如何使用多个**工作进程（workers）**来让应用程序的执行**并行化**，充分利用 CPU 的**多核性能**，并能够处理**更多的请求**。

从上面的部署概念列表来看，使用worker主要有助于**复制**部分，并对**重新启动**有一点帮助，但您仍然需要照顾其他部分：

* **安全 - HTTPS**
* **启动时运行**
* ***重新启动***
* 复制（运行的进程数）
* **内存**
* **启动之前的先前步骤**

## 容器和 Docker { #containers-and-docker }

在关于 [容器中的 FastAPI - Docker](docker.md) 的下一章中，我将介绍一些可用于处理其他**部署概念**的策略。

我将向您展示如何**从零开始构建自己的镜像**，以运行一个单独的 Uvicorn 进程。这个过程相对简单，并且在使用 **Kubernetes** 等分布式容器管理系统时，这通常是您需要采取的方法。

## 回顾 { #recap }

您可以在使用 `fastapi` 或 `uvicorn` 命令时，通过 `--workers` CLI 选项启用多个工作进程（workers），以充分利用**多核 CPU**，以**并行运行多个进程**。

如果您要设置**自己的部署系统**，同时自己处理其他部署概念，则可以使用这些工具和想法。

请查看下一章，了解带有容器（例如 Docker 和 Kubernetes）的 **FastAPI**。 您将看到这些工具也有简单的方法来解决其他**部署概念**。 ✨
