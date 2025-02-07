# Server Workers - Gunicorn with Uvicorn

让我们回顾一下之前的部署概念：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* **复制（运行的进程数）**
* 内存
* 启动前的先前步骤

到目前为止，通过文档中的所有教程，您可能已经在**单个进程**上运行了像 Uvicorn 这样的**服务器程序**。

部署应用程序时，您可能希望进行一些**进程复制**，以利用**多核**并能够处理更多请求。

正如您在上一章有关[部署概念](concepts.md){.internal-link target=_blank}中看到的，您可以使用多种策略。

在这里我将向您展示如何将 <a href="https://gunicorn.org/" class="external-link" target="_blank">**Gunicorn**</a> 与 **Uvicorn worker 进程** 一起使用。

/// info

如果您正在使用容器，例如 Docker 或 Kubernetes，我将在下一章中告诉您更多相关信息：[容器中的 FastAPI - Docker](docker.md){.internal-link target=_blank}。

特别是，当在 **Kubernetes** 上运行时，您可能**不想**使用 Gunicorn，而是运行 **每个容器一个 Uvicorn 进程**，但我将在本章后面告诉您这一点。

///

## Gunicorn with Uvicorn Workers

**Gunicorn**主要是一个使用**WSGI标准**的应用服务器。 这意味着 Gunicorn 可以为 Flask 和 Django 等应用程序提供服务。 Gunicorn 本身与 **FastAPI** 不兼容，因为 FastAPI 使用最新的 **<a href="https://asgi.readthedocs.io/en/latest/" class="external-link" target=" _blank">ASGI 标准</a>**。

但 Gunicorn 支持充当 **进程管理器** 并允许用户告诉它要使用哪个特定的 **worker类**。 然后 Gunicorn 将使用该类启动一个或多个 **worker进程**。

**Uvicorn** 有一个 Gunicorn 兼容的worker类。

使用这种组合，Gunicorn 将充当 **进程管理器**，监听 **端口** 和 **IP**。 它会将通信**传输**到运行**Uvicorn类**的worker进程。

然后与Gunicorn兼容的**Uvicorn worker**类将负责将Gunicorn发送的数据转换为ASGI标准以供FastAPI使用。

## 安装 Gunicorn 和 Uvicorn

<div class="termy">

```console
$ pip install "uvicorn[standard]" gunicorn

---> 100%
```

</div>

这将安装带有`standard`扩展包（以获得高性能）的 Uvicorn 和 Gunicorn。

## Run Gunicorn with Uvicorn Workers

接下来你可以通过以下命令运行Gunicorn:

<div class="termy">

```console
$ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

[19499] [INFO] Starting gunicorn 20.1.0
[19499] [INFO] Listening at: http://0.0.0.0:80 (19499)
[19499] [INFO] Using worker: uvicorn.workers.UvicornWorker
[19511] [INFO] Booting worker with pid: 19511
[19513] [INFO] Booting worker with pid: 19513
[19514] [INFO] Booting worker with pid: 19514
[19515] [INFO] Booting worker with pid: 19515
[19511] [INFO] Started server process [19511]
[19511] [INFO] Waiting for application startup.
[19511] [INFO] Application startup complete.
[19513] [INFO] Started server process [19513]
[19513] [INFO] Waiting for application startup.
[19513] [INFO] Application startup complete.
[19514] [INFO] Started server process [19514]
[19514] [INFO] Waiting for application startup.
[19514] [INFO] Application startup complete.
[19515] [INFO] Started server process [19515]
[19515] [INFO] Waiting for application startup.
[19515] [INFO] Application startup complete.
```

</div>


让我们看看每个选项的含义：

* `main:app`：这与 Uvicorn 使用的语法相同，`main` 表示名为"`main`"的 Python 模块，因此是文件 `main.py`。 `app` 是 **FastAPI** 应用程序的变量名称。
     * 你可以想象 `main:app` 相当于一个 Python `import` 语句，例如：

        ```Python
        from main import app
        ```

     * 因此，`main:app` 中的冒号相当于 `from main import app` 中的 Python `import` 部分。

* `--workers`：要使用的worker进程数量，每个进程将运行一个 Uvicorn worker进程，在本例中为 4 个worker进程。

* `--worker-class`：在worker进程中使用的与 Gunicorn 兼容的工作类。
     * 这里我们传递了 Gunicorn 可以导入和使用的类：

         ```Python
         import uvicorn.workers.UvicornWorker
         ```

* `--bind`：这告诉 Gunicorn 要监听的 IP 和端口，使用冒号 (`:`) 分隔 IP 和端口。
     * 如果您直接运行 Uvicorn，则可以使用`--host 0.0.0.0`和`--port 80`，而不是`--bind 0.0.0.0:80`（Gunicorn 选项）。


在输出中，您可以看到它显示了每个进程的 **PID**（进程 ID）（它只是一个数字）。

你可以看到：

* Gunicorn **进程管理器** 以 PID `19499` 开头（在您的情况下，它将是一个不同的数字）。
* 然后它开始`Listening at: http://0.0.0.0:80`。
* 然后它检测到它必须使用 `uvicorn.workers.UvicornWorker` 处的worker类。
* 然后它启动**4个worker**，每个都有自己的PID：`19511`、`19513`、`19514`和`19515`。

Gunicorn 还将负责管理**死进程**和**重新启动**新进程（如果需要保持worker数量）。 因此，这在一定程度上有助于上面列表中**重启**的概念。

尽管如此，您可能还希望有一些外部的东西，以确保在必要时**重新启动 Gunicorn**，并且**在启动时运行它**等。

## Uvicorn with Workers

Uvicorn 也有一个选项可以启动和运行多个 **worker进程**。

然而，到目前为止，Uvicorn 处理worker进程的能力比 Gunicorn 更有限。 因此，如果您想拥有这个级别（Python 级别）的进程管理器，那么最好尝试使用 Gunicorn 作为进程管理器。

无论如何，您都可以像这样运行它：

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

这里唯一的新选项是 `--workers` 告诉 Uvicorn 启动 4 个工作进程。

您还可以看到它显示了每个进程的 **PID**，父进程（这是 **进程管理器**）的 PID 为`27365`，每个工作进程的 PID 为：`27368`、`27369`， `27370`和`27367`。

## 部署概念

在这里，您了解了如何使用 **Gunicorn**（或 Uvicorn）管理 **Uvicorn 工作进程**来**并行**应用程序的执行，利用 CPU 中的 **多核**，并 能够满足**更多请求**。

从上面的部署概念列表来看，使用worker主要有助于**复制**部分，并对**重新启动**有一点帮助，但您仍然需要照顾其他部分：

* **安全 - HTTPS**
* **启动时运行**
* ***重新启动***
* 复制（运行的进程数）
* **内存**
* **启动之前的先前步骤**

## 容器和 Docker

在关于 [容器中的 FastAPI - Docker](docker.md){.internal-link target=_blank} 的下一章中，我将介绍一些可用于处理其他 **部署概念** 的策略。

我还将向您展示 **官方 Docker 镜像**，其中包括 **Gunicorn 和 Uvicorn worker** 以及一些对简单情况有用的默认配置。

在那里，我还将向您展示如何 **从头开始构建自己的镜像** 以运行单个 Uvicorn 进程（没有 Gunicorn）。 这是一个简单的过程，并且可能是您在使用像 **Kubernetes** 这样的分布式容器管理系统时想要做的事情。

## 回顾

您可以使用**Gunicorn**（或Uvicorn）作为Uvicorn工作进程的进程管理器，以利用**多核CPU**，**并行运行多个进程**。

如果您要设置**自己的部署系统**，同时自己处理其他部署概念，则可以使用这些工具和想法。

请查看下一章，了解带有容器（例如 Docker 和 Kubernetes）的 **FastAPI**。 您将看到这些工具也有简单的方法来解决其他**部署概念**。 ✨
