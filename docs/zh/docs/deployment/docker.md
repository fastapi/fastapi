# 容器中的 FastAPI - Docker { #fastapi-in-containers-docker }

部署 FastAPI 应用时，一个常见的方法是构建 **Linux 容器镜像**。这通常使用 <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> 来完成。然后，你可以通过几种可能的方式之一部署该容器镜像。

使用 Linux 容器有几个优点，包括**安全性**、**可复制性**、**简单性**等。

/// tip | 提示

赶时间并且已经知道这些东西了？跳转到下面的 [`Dockerfile` 👇](#build-a-docker-image-for-fastapi)。

///

<details>
<summary>Dockerfile Preview 👀</summary>

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## 什么是容器 { #what-is-a-container }

容器（主要是 Linux 容器）是一种非常**轻量级**的打包应用的方式：包含所有依赖和必要文件，同时与同一系统中的其他容器（其他应用或组件）保持隔离。

Linux 容器使用宿主机（物理机、虚拟机、云服务器等）的同一个 Linux 内核运行。这意味着它们非常轻量（与模拟整个操作系统的完整虚拟机相比）。

通过这种方式，容器消耗**很少的资源**，其数量与直接运行进程相当（虚拟机会消耗更多）。

容器还拥有各自**隔离的**运行进程（通常只有一个进程）、文件系统和网络，从而简化部署、安全、开发等。

## 什么是容器镜像 { #what-is-a-container-image }

**容器**是从**容器镜像**运行的。

容器镜像是容器中所有文件、环境变量，以及容器启动时应存在的默认命令/程序的**静态**版本。这里的 **静态** 意味着容器**镜像**并没有在运行，没有在执行，它只是打包好的文件和元数据。

与存储静态内容的“**容器镜像**”相反，“**容器**”通常指正在运行的实例，也就是正在被**执行**的东西。

当**容器**启动并运行（从**容器镜像**启动）时，它可以创建或更改文件、环境变量等。这些更改只会存在于该容器中，不会持久化到其底层的容器镜像中（不会保存到磁盘）。

容器镜像可类比为**程序**文件和内容，例如 `python` 以及某个文件 `main.py`。

而**容器**本身（与**容器镜像**相对）是镜像的实际运行实例，可类比为一个**进程**。事实上，容器只有在其中有**进程在运行**时才算运行（通常只有一个进程）。当其中没有进程运行时，容器就会停止。

## 容器镜像 { #container-images }

Docker 一直是创建和管理**容器镜像**与**容器**的主要工具之一。

同时还有一个公共的 <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a>，包含许多工具、环境、数据库和应用的预制**官方容器镜像**。

例如，有一个官方的 <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Python 镜像</a>。

还有许多用于不同用途（例如数据库）的镜像，例如：

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a>，等。

通过使用预制的容器镜像，可以非常轻松地**组合**并使用不同的工具。例如，试用一个新的数据库。在大多数情况下，你可以使用**官方镜像**，只需要通过环境变量进行配置即可。

这样，在很多情况下，你可以学习容器和 Docker，并把这些知识复用到许多不同的工具和组件上。

因此，你可以运行**多个容器**，分别放置不同的东西，比如数据库、Python 应用、带 React 前端应用的 Web 服务器，并通过内部网络把它们连接起来。

所有容器管理系统（如 Docker 或 Kubernetes）都内置了这些网络功能。

## 容器与进程 { #containers-and-processes }

**容器镜像**通常会在元数据中包含：启动**容器**时应运行的默认程序或命令，以及传递给该程序的参数。这和在命令行中运行的情况非常相似。

当**容器**启动时，它会运行该命令/程序（当然你也可以覆盖它，让它运行不同的命令/程序）。

只要**主进程**（命令或程序）在运行，容器就会保持运行。

容器通常只有一个**单进程**，但也可以由主进程启动子进程，从而在同一个容器中拥有**多个进程**。

但是，不可能在没有**至少一个正在运行的进程**的情况下运行容器。如果主进程停止，容器也会停止。

## 为 FastAPI 构建 Docker 镜像 { #build-a-docker-image-for-fastapi }

好，我们现在来构建点东西！🚀

我将向你展示如何基于**官方 Python** 镜像**从头开始**为 FastAPI 构建 **Docker 镜像**。

这是你在**大多数情况**下会想要做的，例如：

* 使用 **Kubernetes** 或类似工具
* 在 **Raspberry Pi** 上运行时
* 使用能为你运行容器镜像的云服务等。

### 包依赖 { #package-requirements }

你通常会把应用的**包依赖**放在某个文件中。

这主要取决于你用来**安装**这些依赖的工具。

最常见的做法是创建一个 `requirements.txt` 文件，每行包含一个包名及其版本。

当然，你也可以使用你在[关于 FastAPI 版本](versions.md){.internal-link target=_blank}中读到的相同思路来设置版本范围。

例如，你的 `requirements.txt` 可能如下所示：

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

然后你通常会用 `pip` 来安装这些包依赖，例如：

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | 信息

还有其他格式和工具可以用来定义并安装包依赖。

///

### 创建 **FastAPI** 代码 { #create-the-fastapi-code }

* 创建一个 `app` 目录并进入它。
* 创建一个空文件 `__init__.py`。
* 创建一个 `main.py` 文件，内容如下：

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

现在在同一个项目目录中创建一个文件 `Dockerfile`，内容如下：

```{ .dockerfile .annotate }
# (1)!
FROM python:3.9

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. 从官方 Python 基础镜像开始。

2. 将当前工作目录设置为 `/code`。

    这里将放置 `requirements.txt` 文件和 `app` 目录。

3. 将依赖文件复制到 `/code` 目录中。

    先**只**复制依赖文件，不复制其余代码。

    因为这个文件**不经常变更**，Docker 会检测到它并在这一步使用**缓存**，从而也为下一步启用缓存。

4. 安装依赖文件中的包依赖。

    `--no-cache-dir` 选项告诉 `pip` 不要在本地保存下载的包，因为那只有在 `pip` 之后还会再次运行并安装相同的包时才有用，但在容器场景中通常不是这样。

    /// note | 注意

    `--no-cache-dir` 只和 `pip` 有关，与 Docker 或容器无关。

    ///

    `--upgrade` 选项告诉 `pip`：如果包已经安装，则升级它们。

    因为上一步复制文件可能会被 **Docker 缓存**检测到，所以这一步在可用时也会**使用 Docker 缓存**。

    在开发过程中一次又一次构建镜像时，在这一步使用缓存会为你节省大量**时间**，而不是**每次**都去**下载和安装**所有依赖。

5. 将 `./app` 目录复制到 `/code` 目录中。

    因为这里包含所有代码，也是**最频繁变更**的部分，所以 Docker **缓存**不容易用于这一条或任何**后续步骤**。

    因此，把它放在 `Dockerfile` 的**靠近末尾**位置非常重要，以优化容器镜像构建时间。

6. 设置使用 `fastapi run` 的**命令**，它底层使用 Uvicorn。

    `CMD` 接收一个字符串列表，每个字符串对应命令行中用空格分隔的内容。

    该命令会从**当前工作目录**运行，也就是你在上面用 `WORKDIR /code` 设置的同一个 `/code` 目录。

/// tip | 提示

通过点击代码中的每个数字气泡来查看每行的作用。👆

///

/// warning | 警告

确保**始终**使用 `CMD` 指令的 **exec 形式**，如下所述。

///

#### 使用 `CMD` - Exec 形式 { #use-cmd-exec-form }

Docker 指令 <a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a> 有两种写法：

✅ **Exec** 形式：

```Dockerfile
# ✅ Do this
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** 形式：

```Dockerfile
# ⛔️ Don't do this
CMD fastapi run app/main.py --port 80
```

请确保始终使用 **exec** 形式，以保证 FastAPI 能够优雅关闭并触发 [lifespan 事件](../advanced/events.md){.internal-link target=_blank}。

你可以在 <a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">Docker 关于 shell 与 exec 形式的文档</a> 中阅读更多内容。

在使用 `docker compose` 时，这个差异会很明显。更多技术细节可参考 Docker Compose FAQ 的这一节：<a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">Why do my services take 10 seconds to recreate or stop?</a>。

#### 目录结构 { #directory-structure }

你现在应该有如下目录结构：

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### 在 TLS 终止代理后面 { #behind-a-tls-termination-proxy }

如果你在 Nginx 或 Traefik 等 TLS 终止代理（负载均衡器）后面运行容器，请添加选项 `--proxy-headers`。这会让 Uvicorn（通过 FastAPI CLI）信任该代理发送的头信息，从而知道应用运行在 HTTPS 后面等。

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker 缓存 { #docker-cache }

这个 `Dockerfile` 里有个重要技巧：我们先只复制**依赖文件本身**，而不是其余代码。我来告诉你为什么。

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker 和其他工具会以**增量**方式**构建**容器镜像：从 `Dockerfile` 顶部开始，把每条指令创建的文件作为一层，**一层叠一层**地加上去。

Docker 和类似工具在构建镜像时也会使用**内部缓存**：如果一个文件自上次构建容器镜像以来没有变化，它就会**复用上次创建的同一层**，而不是再次复制文件并从头创建新层。

仅仅避免复制文件不一定能提升太多，但因为这一步使用了缓存，它就能**在下一步使用缓存**。例如，它可以对安装依赖的指令使用缓存：

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

包依赖文件**不会频繁变更**。因此，只复制这个文件，Docker 就能在这一步**使用缓存**。

接着，Docker 就能**在下一步使用缓存**，也就是下载并安装那些依赖。这里就是我们**节省大量时间**的地方。✨ ...也能避免无聊的等待。😪😆

下载和安装包依赖**可能需要几分钟**，但使用**缓存**最多**只需要几秒钟**。

而你在开发过程中会一次又一次构建容器镜像来检查代码改动是否有效，这会累计节省大量时间。

然后在 `Dockerfile` 的靠近末尾位置，我们再复制所有代码。因为代码是**最频繁变更**的，所以把它放在末尾：因为通常这一步之后的任何步骤都无法再使用缓存。

```Dockerfile
COPY ./app /code/app
```

### 构建 Docker 镜像 { #build-the-docker-image }

现在所有文件都已就位，让我们构建容器镜像。

* 进入项目目录（`Dockerfile` 所在位置，包含 `app` 目录）。
* 构建你的 FastAPI 镜像：

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | 提示

注意最后的 `.`，它等价于 `./`，表示告诉 Docker：用哪个目录来构建容器镜像。

在本例中，它就是当前目录（`.`）。

///

### 启动 Docker 容器 { #start-the-docker-container }

* 根据你的镜像运行容器：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## 检查一下 { #check-it }

你应该能通过 Docker 容器的 URL 访问它，例如：<a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 或 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a>（或等价地址，使用你的 Docker host）。

你会看到类似内容：

```JSON
{"item_id": 5, "q": "somequery"}
```

## 交互式 API 文档 { #interactive-api-docs }

现在你可以访问 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 或 <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a>（或等价地址，使用你的 Docker host）。

你将看到自动生成的交互式 API 文档（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 备选的 API 文档 { #alternative-api-docs }

你也可以访问 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 或 <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a>（或等价地址，使用你的 Docker host）。

你将看到备选的自动文档（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 使用单文件 FastAPI 构建 Docker 镜像 { #build-a-docker-image-with-a-single-file-fastapi }

如果你的 FastAPI 是单文件形式，例如没有 `./app` 目录、只有 `main.py`，你的文件结构可能如下：

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

然后你只需要更改对应路径，把文件复制到 `Dockerfile` 中：

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. 直接把 `main.py` 文件复制到 `/code` 目录（不包含任何 `./app` 目录）。

2. 使用 `fastapi run` 来运行单文件 `main.py` 中的应用。

当你把文件传给 `fastapi run` 时，它会自动检测这是单文件而不是 package 的一部分，并知道如何导入并运行你的 FastAPI 应用。😎

## 部署概念 { #deployment-concepts }

我们再从容器的角度谈谈一些相同的[部署概念](concepts.md){.internal-link target=_blank}。

容器主要是用来简化**构建与部署**应用的过程，但它们并不强制你必须用某一种方式处理这些**部署概念**，而是有多种可选策略。

**好消息**是：无论你选择哪种策略，都有办法覆盖所有部署概念。🎉

我们从容器的角度回顾这些**部署概念**：

* HTTPS
* 启动时运行
* 重启
* 复制（运行的进程数）
* 内存
* 启动前的先前步骤

## HTTPS { #https }

如果我们只关注 FastAPI 应用的**容器镜像**（以及之后运行的**容器**），HTTPS 通常会由另一个工具在**外部**处理。

它可以是另一个容器，例如使用 <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a> 来处理 **HTTPS** 和**自动**获取**证书**。

/// tip | 提示

Traefik 集成了 Docker、Kubernetes 等，因此用它为容器设置和配置 HTTPS 非常容易。

///

或者，HTTPS 也可以由云服务商作为其服务之一来处理（同时仍在容器中运行应用）。

## 在启动时运行与重启 { #running-on-startup-and-restarts }

通常会有另一个工具负责**启动并运行**你的容器。

它可能是直接使用 **Docker**，或 **Docker Compose**、**Kubernetes**、**云服务**等。

在大多数（或所有）情况下，都会有一个简单选项用来启用：开机启动容器、在失败时自动重启。例如在 Docker 中，就是命令行选项 `--restart`。

如果不使用容器，让应用在启动时运行并支持重启可能会很麻烦且困难。但在大多数情况下，当**使用容器**时，这些功能默认就包含了。✨

## 复制 - 进程数 { #replication-number-of-processes }

如果你有一组机器组成的 <abbr title="A group of machines that are configured to be connected and work together in some way. - 一组配置为以某种方式连接并协同工作的机器。">cluster</abbr>，并使用 **Kubernetes**、Docker Swarm Mode、Nomad 或其他类似的复杂系统来管理多台机器上的分布式容器，那么你很可能希望在**集群级别**处理**复制**，而不是在每个容器中使用**进程管理器**（例如带 workers 的 Uvicorn）。

像 Kubernetes 这样的分布式容器管理系统通常有一些集成方式来处理**容器的复制**，同时仍然支持传入请求的**负载均衡**。全部都在**集群级别**完成。

在这些情况下，你很可能会希望像[上面所解释](#dockerfile)那样**从头构建 Docker 镜像**：安装依赖，并运行**单个 Uvicorn 进程**，而不是使用多个 Uvicorn workers。

### 负载均衡器 { #load-balancer }

使用容器时，通常会有某个组件在**主端口**上监听。它可能是另一个容器，同时也是一个用于处理 **HTTPS** 的 **TLS 终止代理**，或类似工具。

由于该组件会接收请求的**负载**并以（希望）**均衡**的方式把请求分发给各个 worker，因此它通常也被称为**负载均衡器**。

/// tip | 提示

用于 HTTPS 的 **TLS 终止代理**组件通常也会是**负载均衡器**。

///

当使用容器时，你用来启动和管理容器的同一系统，通常已经内置工具来把来自该**负载均衡器**（也可能是 **TLS 终止代理**）的**网络通信**（例如 HTTP 请求）传递到运行你应用的容器。

### 一个负载均衡器 - 多个 worker 容器 { #one-load-balancer-multiple-worker-containers }

在使用 **Kubernetes** 或类似的分布式容器管理系统时，它们的内部网络机制可以让单个在主**端口**上监听的**负载均衡器**把通信（请求）传递到可能**多个**运行你应用的容器。

每个运行你应用的容器通常**只有一个进程**（例如运行 FastAPI 应用的 Uvicorn 进程）。它们都是**相同的容器**，运行相同的内容，但每个容器都有自己的进程、内存等。这样你就能利用 CPU 的**不同核心**，甚至**不同机器**上的**并行化**能力。

带有**负载均衡器**的分布式容器系统会轮流把请求**分发**给运行你应用的各个容器。因此，每个请求都可以由多个运行你应用的**复制容器**之一来处理。

并且通常，这个**负载均衡器**也能处理发送到集群中*其他*应用的请求（例如不同域名，或不同 URL 路径前缀下），并把通信转发到集群中运行的*那个其他*应用对应的正确容器。

### 每个容器一个进程 { #one-process-per-container }

在这种场景下，你很可能希望**每个容器只运行一个（Uvicorn）进程**，因为你已经在集群级别处理复制了。

因此，在这种情况下，你**不会**希望在容器里运行多个 worker，例如使用 `--workers` 命令行选项。你希望每个容器只运行**一个 Uvicorn 进程**（但可能会有多个容器）。

在容器内再放一个进程管理器（例如多个 workers）只会增加你很可能已经由集群系统处理掉的**不必要复杂性**。

### 具有多个进程的容器与特殊情况 { #containers-with-multiple-processes-and-special-cases }

当然，也存在一些**特殊情况**，你可能希望在**一个容器**中运行多个 **Uvicorn worker 进程**。

这时，你可以使用 `--workers` 命令行选项来设置你想运行的 worker 数量：

```{ .dockerfile .annotate }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. 这里我们使用 `--workers` 命令行选项把 worker 数量设置为 4。

下面是一些可能合理的例子：

#### 一个简单的应用 { #a-simple-app }

如果你的应用**足够简单**，可以在**单台服务器**上运行（而不是集群），你可能希望在容器中使用进程管理器。

#### Docker Compose { #docker-compose }

你可能会用 **Docker Compose** 部署到**单台服务器**（不是集群），这样你就没有一种简单方式在保留共享网络和**负载均衡**的同时管理容器的复制（通过 Docker Compose）。

这时，你可能希望使用**一个容器**，其中的**进程管理器**启动**多个 worker 进程**。

---

关键点是：这些都**不是**你必须盲目遵循的**铁律**。你可以用这些思路来**评估你自己的场景**，并决定你的系统最合适的方法，同时检查如何管理下面这些概念：

* 安全性 - HTTPS
* 启动时运行
* 重启
* 复制（运行的进程数）
* 内存
* 启动前的先前步骤

## 内存 { #memory }

如果你**每个容器只运行一个进程**，那么每个容器的内存消耗会比较明确、稳定且有限（如果有复制，则不止一个容器）。

然后你就可以在容器管理系统的配置中设置相同的内存限制与需求（例如在 **Kubernetes** 中）。这样系统就能在**可用机器**上**复制容器**时，同时考虑它们所需的内存量，以及集群各机器的可用内存量。

如果你的应用很**简单**，这可能**不是问题**，你也许不需要指定硬性的内存限制。但如果你**使用大量内存**（例如使用**机器学习**模型），你应该检查实际内存消耗，并调整**每台机器**上运行的**容器数量**（也许还需要给集群增加更多机器）。

如果你**每个容器运行多个进程**，你就必须确保启动的进程数不会**消耗超过可用内存**。

## 启动前的先前步骤与容器 { #previous-steps-before-starting-and-containers }

如果你在使用容器（例如 Docker、Kubernetes），主要有两种方式可以选择。

### 多个容器 { #multiple-containers }

如果你有**多个容器**，很可能每个容器只运行**一个进程**（例如在 **Kubernetes** 集群中），那么你很可能希望有一个**单独的容器**来完成**启动前的先前步骤**：在单个容器里运行一个进程，并在运行复制的 worker 容器**之前**完成这些工作。

/// info | 信息

如果你在使用 Kubernetes，这很可能是一个 <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>。

///

如果在你的用例中，并行多次执行这些先前步骤**没有问题**（例如你不运行数据库迁移，只是检查数据库是否已就绪），那么你也可以把它们放到每个容器里，在启动主进程之前执行。

### 单容器 { #single-container }

如果你是一个简单设置：**单个容器**，然后在其中启动多个 **worker 进程**（或者只启动一个进程），那么你可以在同一个容器中，在启动应用进程之前运行这些先前步骤。

### 基础 Docker 镜像 { #base-docker-image }

过去曾经有一个官方的 FastAPI Docker 镜像：<a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>。但它现在已经废弃了。⛔️

你很可能**不应该**使用这个基础 Docker 镜像（或任何其他类似的镜像）。

如果你在使用 **Kubernetes**（或其他系统），并且已经在集群级别设置了**复制**，且有多个**容器**。在这些情况下，你更应该像上面描述的那样**从头构建镜像**：[为 FastAPI 构建 Docker 镜像](#build-a-docker-image-for-fastapi)。

如果你需要多个 worker，你可以直接使用 `--workers` 命令行选项。

/// note | 技术细节

这个 Docker 镜像创建于 Uvicorn 还不支持管理并重启挂掉的 worker 的时期，因此需要用 Gunicorn 配合 Uvicorn，这会增加不少复杂性，仅仅是为了让 Gunicorn 去管理并重启 Uvicorn worker 进程。

但现在 Uvicorn（以及 `fastapi` 命令）已经支持使用 `--workers`，所以没有理由用基础 Docker 镜像来替代自己构建（代码量基本一样 😅）。

///

## 部署容器镜像 { #deploy-the-container-image }

在拥有容器（Docker）镜像之后，有多种方式可以部署它。

例如：

* 在单台服务器上使用 **Docker Compose**
* 使用 **Kubernetes** 集群
* 使用 Docker Swarm Mode 集群
* 使用 Nomad 等其他工具
* 使用云服务获取你的容器镜像并部署它

## 使用 `uv` 的 Docker 镜像 { #docker-image-with-uv }

如果你使用 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a> 来安装并管理项目，可以参考它们的 <a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">uv Docker guide</a>。

## 回顾 { #recap }

使用容器系统（例如 **Docker** 和 **Kubernetes**）可以相当直接地处理所有**部署概念**：

* HTTPS
* 启动时运行
* 重启
* 复制（运行的进程数）
* 内存
* 启动前的先前步骤

在大多数情况下，你可能不想使用任何基础镜像，而是基于官方 Python Docker 镜像**从头构建容器镜像**。

注意 `Dockerfile` 中指令的**顺序**以及 **Docker 缓存**，你可以**最小化构建时间**，从而最大化你的生产力（并避免无聊）。😎
