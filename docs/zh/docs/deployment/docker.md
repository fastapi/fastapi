# 容器中的 FastAPI - Docker { #fastapi-in-containers-docker }

部署 FastAPI 应用时，常见做法是构建一个**Linux 容器镜像**。通常使用 <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> 实现。然后你可以用几种方式之一部署该镜像。

使用 Linux 容器有多种优势，包括**安全性**、**可复制性**、**简单性**等。

/// tip | 提示

赶时间并且已经了解这些？直接跳到下面的 [`Dockerfile` 👇](#build-a-docker-image-for-fastapi)。

///

<details>
<summary>Dockerfile 预览 👀</summary>

```Dockerfile
FROM python:3.14

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

容器（主要是 Linux 容器）是一种非常**轻量**的方式，用来打包应用及其所有依赖和必要文件，并让它们与同一系统中的其他容器（其他应用或组件）相互隔离。

Linux 容器复用宿主机（物理机、虚拟机、云服务器等）的同一个 Linux 内核。这意味着它们非常轻量（相较于模拟整个操作系统的完整虚拟机）。

因此，容器消耗的**资源很少**，大致相当于直接运行进程（而虚拟机会多很多）。

容器还拥有各自**隔离**的运行进程（通常只有一个）、文件系统和网络，简化了部署、安全、开发等。

## 什么是容器镜像 { #what-is-a-container-image }

**容器**是从**容器镜像**运行的。

容器镜像是容器中所有文件、环境变量以及应该运行的默认命令/程序的一个**静态**版本。这里的**静态**指容器**镜像**本身并不在运行，仅仅是被打包的文件和元数据。

与存放静态内容的“**容器镜像**”相对，“**容器**”通常指一个正在运行的实例，即正在被**执行**的东西。

当**容器**启动并运行（从**容器镜像**启动）后，它可以创建或修改文件、环境变量等。这些更改只存在于该容器中，不会持久化到底层的容器镜像中（不会写回磁盘）。

容器镜像可类比为**程序**文件及其内容，例如 `python` 和某个文件 `main.py`。

而**容器**本身（相对**容器镜像**）就是该镜像的实际运行实例，可类比为**进程**。事实上，容器只有在有**进程在运行**时才处于运行状态（通常只有一个进程）。当容器中没有任何进程在运行时，容器就会停止。

## 容器镜像 { #container-images }

Docker 一直是创建和管理**容器镜像**与**容器**的主要工具之一。

还有一个公共的 <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a>，其中为许多工具、环境、数据库和应用提供了预制的**官方容器镜像**。

例如，有官方的 <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Python 镜像</a>。

还有许多用于不同目的（如数据库）的镜像，例如：

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a> 等。

通过使用预制的容器镜像，可以很容易地**组合**并使用不同工具。例如，试用一个新的数据库。在大多数情况下，你可以直接使用**官方镜像**，只需通过环境变量配置即可。

这样，在很多场景中你可以学习容器和 Docker，并将这些知识复用到许多不同的工具和组件中。

因此，你可以运行包含不同内容的**多个容器**，比如一个数据库、一个 Python 应用、一个带 React 前端的 Web 服务器，并通过它们的内部网络连接在一起。

所有容器管理系统（如 Docker 或 Kubernetes）都内置了这些网络功能。

## 容器与进程 { #containers-and-processes }

**容器镜像**通常在其元数据中包含在**容器**启动时应运行的默认程序或命令以及要传递给该程序的参数。这与命令行中做的事情非常相似。

当**容器**启动时，它将运行该命令/程序（尽管你可以覆盖它，让其运行不同的命令/程序）。

只要**主进程**（命令或程序）在运行，容器就在运行。

容器通常只有**一个进程**，但也可以由主进程启动子进程，这样同一个容器中就会有**多个进程**。

但不可能在没有**至少一个运行中的进程**的情况下让容器保持运行。如果主进程停止，容器也会停止。

## 为 FastAPI 构建 Docker 镜像 { #build-a-docker-image-for-fastapi }

好啦，现在动手构建点东西！🚀

我将演示如何基于**官方 Python** 镜像，**从零开始**为 FastAPI 构建一个**Docker 镜像**。

这在**大多数情况**下都适用，例如：

* 使用 **Kubernetes** 或类似工具
* 运行在 **Raspberry Pi**
* 使用某个为你运行容器镜像的云服务，等等

### 包依赖 { #package-requirements }

通常你会把应用的**包依赖**放在某个文件里。

这主要取决于你用来**安装**这些依赖的工具。

最常见的方式是使用 `requirements.txt` 文件，每行一个包名及其版本范围。

当然，你也可以参考你在[关于 FastAPI 版本](versions.md){.internal-link target=_blank}中读到的思路来设置版本范围。

例如，你的 `requirements.txt` 可能是：

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

通常你会用 `pip` 安装这些依赖，例如：

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | 信息

还有其他格式和工具可以定义并安装包依赖。

///

### 编写 **FastAPI** 代码 { #create-the-fastapi-code }

* 创建 `app` 目录并进入
* 创建空文件 `__init__.py`
* 创建 `main.py`，内容如下：

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

现在在同一个项目目录下创建 `Dockerfile` 文件：

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

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

    我们会把 `requirements.txt` 文件和 `app` 目录放在这里。

3. 将依赖文件复制到 `/code` 目录。

    首先**只**复制依赖文件，不要复制其他代码。

    因为这个文件**不常变化**，Docker 会检测并在此步骤使用**缓存**，从而也为下一步启用缓存。

4. 安装依赖文件中的包依赖。

    `--no-cache-dir` 选项告诉 `pip` 不要在本地保存下载的包，只有当以后还要再次用 `pip` 安装相同包时才需要，但在容器场景下不是这样。

    /// note | 注意

    `--no-cache-dir` 只和 `pip` 有关，与 Docker 或容器无关。

    ///

    `--upgrade` 选项告诉 `pip` 如果包已安装则进行升级。

    由于上一步复制文件可能被 **Docker 缓存**检测到，因此这一步在可用时也会**使用 Docker 缓存**。

    在开发过程中反复构建镜像时，此步骤使用缓存可以为你**节省大量时间**，而不必**每次**都**下载并安装**所有依赖。

5. 将 `./app` 目录复制到 `/code` 目录。

    这里包含了所有**最常变化**的代码，因此 Docker **缓存**很难用于这一步或**其后的步骤**。

    所以，把它放在 `Dockerfile` 的**靠后位置**，有助于优化容器镜像的构建时间。

6. 设置使用 `fastapi run` 的**命令**（底层使用 Uvicorn）。

    `CMD` 接受一个字符串列表，每个字符串相当于你在命令行中用空格分隔输入的内容。

    该命令会从**当前工作目录**运行，也就是你用 `WORKDIR /code` 设置的 `/code` 目录。

/// tip | 提示

点击代码中的每个编号气泡查看每行的作用。👆

///

/// warning | 警告

务必**始终**使用 `CMD` 指令的**exec 形式**，如下所述。

///

#### 使用 `CMD` - Exec 形式 { #use-cmd-exec-form }

<a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a> 指令有两种写法：

✅ **Exec** 形式：

```Dockerfile
# ✅ 推荐
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** 形式：

```Dockerfile
# ⛔️ 不要这样
CMD fastapi run app/main.py --port 80
```

务必使用**exec** 形式，以确保 FastAPI 可以优雅停机并触发[生命周期事件](../advanced/events.md){.internal-link target=_blank}。

你可以在 <a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">Docker 文档（Shell 与 Exec 形式）</a>中了解更多。

在使用 `docker compose` 时这一点尤为明显。更多技术细节参见该 FAQ：<a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">为什么我的服务需要 10 秒才能重新创建或停止？</a>

#### 目录结构 { #directory-structure }

此时你的目录结构应类似：

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### 在 TLS 终止代理后面 { #behind-a-tls-termination-proxy }

如果你在 Nginx 或 Traefik 等 TLS 终止代理（负载均衡器）后面运行容器，请添加 `--proxy-headers` 选项，这会通过 FastAPI CLI 告诉 Uvicorn 信任该代理发送的标头，表明应用运行在 HTTPS 后等。

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker 缓存 { #docker-cache }

这个 `Dockerfile` 里有个重要技巧：我们先**只复制依赖文件**，而不是其他代码。原因如下：

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker 等工具是**增量**地**构建**容器镜像的，从 `Dockerfile` 顶部开始，按顺序为每条指令创建**一层叠加层**，并把每步生成的文件加入。

构建镜像时，Docker 等工具也会使用**内部缓存**。如果自上次构建以来某个文件没有变更，它会**重用**上次创建的那一层，而不是再次复制文件并从头创建新层。

仅仅避免复制文件并不会带来太多改进，但因为该步骤使用了缓存，它就可以**在下一步中继续使用缓存**。例如，安装依赖的这条指令也能使用缓存：

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

包含包依赖的文件**不会频繁变更**。仅复制该文件，Docker 就能在这一步**使用缓存**。

随后，Docker 还能**对下一步**（下载并安装依赖）**使用缓存**。这正是我们**节省大量时间**的地方。✨ ...并避免无聊的等待。😪😆

下载并安装依赖**可能需要几分钟**，而使用**缓存**则**最多只需几秒**。

而且在开发中你会反复构建镜像来验证代码变更是否生效，累计节省的时间会很多。

接着，在 `Dockerfile` 的末尾附近我们再复制所有代码。因为这是**变化最频繁**的部分，把它放在后面，这样几乎所有在它之后的步骤都不会使用到缓存。

```Dockerfile
COPY ./app /code/app
```

### 构建 Docker 镜像 { #build-the-docker-image }

现在所有文件都就位了，开始构建容器镜像。

* 进入项目目录（`Dockerfile` 所在位置，包含 `app` 目录）
* 构建你的 FastAPI 镜像：

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | 提示

注意末尾的 `.`，它等价于 `./`，用于告诉 Docker 使用哪个目录来构建容器镜像。

此处就是当前目录（`.`）。

///

### 启动 Docker 容器 { #start-the-docker-container }

* 基于你的镜像运行一个容器：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## 检查一下 { #check-it }

你应该能在容器暴露的 URL 访问它，例如：<a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 或 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a>（或其他等价地址，取决于你的 Docker 主机）。

你会看到类似内容：

```JSON
{"item_id": 5, "q": "somequery"}
```

## 交互式 API 文档 { #interactive-api-docs }

现在你可以访问 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 或 <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a>（或其他等价地址，取决于你的 Docker 主机）。

你将看到自动生成的交互式 API 文档（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 提供）：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 备选 API 文档 { #alternative-api-docs }

你还可以访问 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 或 <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a>（或其他等价地址，取决于你的 Docker 主机）。

你将看到备选的自动文档（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 使用单文件 FastAPI 构建 Docker 镜像 { #build-a-docker-image-with-a-single-file-fastapi }

如果你的 FastAPI 是单个文件，例如没有 `./app` 目录、只有 `main.py`，你的文件结构可能如下：

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

然后你只需要在 `Dockerfile` 中修改相应路径来复制该文件：

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. 直接将 `main.py` 复制到 `/code`（没有 `./app` 目录）。

2. 使用 `fastapi run` 来运行单文件 `main.py` 中的应用。

当你把文件传给 `fastapi run` 时，它会自动检测这是一个单文件而不是包，并知道如何导入并服务你的 FastAPI 应用。😎

## 部署概念 { #deployment-concepts }

我们再从容器的角度讨论一些相同的[部署概念](concepts.md){.internal-link target=_blank}。

容器主要是简化应用**构建与部署**流程的工具，但它们并不强制采用某种特定方式来处理这些**部署概念**，可选策略有多种。

**好消息**是，不同策略下都有方式覆盖所有部署概念。🎉

让我们从容器角度回顾这些**部署概念**：

* HTTPS
* 启动时运行
* 失败重启
* 复制（运行的进程数）
* 内存
* 启动前的前置步骤

## HTTPS { #https }

如果我们只关注 FastAPI 应用的**容器镜像**（以及后续运行的**容器**），HTTPS 通常由**外部**的其他工具处理。

它可以是另一个容器，例如使用 <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>，处理 **HTTPS** 并**自动**获取**证书**。

/// tip | 提示

Traefik 与 Docker、Kubernetes 等都有集成，因此为容器设置和配置 HTTPS 非常容易。

///

或者，HTTPS 也可能由云服务商作为其服务之一提供（应用仍运行在容器中）。

## 启动时运行与重启 { #running-on-startup-and-restarts }

通常会有另一个工具负责**启动并运行**你的容器。

它可以是直接的 **Docker**、**Docker Compose**、**Kubernetes**、某个**云服务**等。

在大多数（或全部）情况下，都有简单选项可以在开机时运行容器并在失败时启用重启。例如，在 Docker 中是命令行选项 `--restart`。

如果不使用容器，要让应用开机自启并带重启可能繁琐且困难。但在**容器**场景下，这种功能通常默认就包含了。✨

## 复制 - 进程数 { #replication-number-of-processes }

如果你有一个由 **Kubernetes**、Docker Swarm Mode、Nomad 或其他类似的复杂系统管理的、在多台机器上运行的分布式容器<dfn title="被配置为以某种方式连接并协同工作的多台机器">集群</dfn>，那么你很可能会希望在**集群层面**来**处理复制**，而不是在每个容器中使用**进程管理**（比如让 Uvicorn 运行多个 workers）。

像 Kubernetes 这样的分布式容器管理系统通常都有某种内置方式来处理**容器复制**，同时对传入请求进行**负载均衡**。这一切都在**集群层面**完成。

在这些情况下，你可能希望如[上文所述](#dockerfile)那样**从头构建 Docker 镜像**，安装依赖，并仅运行**单个 Uvicorn 进程**，而不是使用多个 Uvicorn workers。

### 负载均衡器 { #load-balancer }

使用容器时，通常会有某个组件**监听主端口**。它可能是另一个同时充当 **TLS 终止代理**以处理 **HTTPS** 的容器，或类似工具。

由于该组件会承接请求的**负载**并以（期望）**均衡**的方式在 workers 间分发，它也常被称为**负载均衡器**。

/// tip | 提示

用于 HTTPS 的**TLS 终止代理**组件通常也会是**负载均衡器**。

///

使用容器时，你用来启动和管理容器的系统本身就已有内部工具，将来自该**负载均衡器**（也可能是**TLS 终止代理**）的**网络通信**（例如 HTTP 请求）传递到你的应用容器中。

### 一个负载均衡器 - 多个 worker 容器 { #one-load-balancer-multiple-worker-containers }

在 **Kubernetes** 等分布式容器管理系统中，使用其内部网络机制，允许在主**端口**上监听的单个**负载均衡器**将通信（请求）转发给可能**多个**运行你应用的容器。

这些运行你应用的容器通常每个只有**一个进程**（例如，一个运行 FastAPI 应用的 Uvicorn 进程）。它们都是**相同的容器**，运行相同的东西，但每个都有自己的进程、内存等。这样你就能在 CPU 的**不同核心**，甚至在**不同机器**上利用**并行化**。

分布式容器系统配合**负载均衡器**会把请求**轮流分配**到每个应用容器。因此，每个请求都可能由多个**副本容器**之一来处理。

通常，这个**负载均衡器**还能处理发往集群中*其他*应用的请求（例如不同域名，或不同的 URL 路径前缀），并将通信转发到运行*那个其他*应用的正确容器。

### 每个容器一个进程 { #one-process-per-container }

在这种场景下，你大概率希望**每个容器只有一个（Uvicorn）进程**，因为你已经在集群层面处理了复制。

因此，这种情况下你**不希望**在容器内再启多个 workers（例如通过 `--workers` 命令行选项）。你会希望每个容器仅有一个**单独的 Uvicorn 进程**（但可能会有多个容器）。

在容器内再放一个进程管理器（就像启多个 workers 一样）只会引入**不必要的复杂性**，而这些你很可能已经在集群系统中处理了。

### 具有多个进程和特殊情况的容器 { #containers-with-multiple-processes-and-special-cases }

当然，也有一些**特殊情况**，你可能希望让**一个容器**里运行多个 **Uvicorn worker 进程**。

在这些情况下，你可以使用 `--workers` 命令行选项来设置要运行的 worker 数量：

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. 这里我们使用 `--workers` 命令行选项将 worker 数量设置为 4。

以下是这种做法可能合理的一些示例：

#### 一个简单的应用 { #a-simple-app }

如果你的应用**足够简单**，可以在**单台服务器**（不是集群）上运行，你可能会希望在容器内有一个进程管理器。

#### Docker Compose { #docker-compose }

如果你使用 **Docker Compose** 部署到**单台服务器**（不是集群），那么你不会有一个简单的方法在保留共享网络与**负载均衡**的同时管理容器复制（通过 Docker Compose）。

这种情况下，你可能希望用**单个容器**，由**进程管理器**在容器内启动**多个 worker 进程**。

---

要点是，这些都**不是**你必须盲目遵循的**铁律**。你可以用这些思路来**评估你自己的场景**，并决定最适合你的系统的方法，看看如何管理以下概念：

* 安全 - HTTPS
* 启动时运行
* 重启
* 复制（运行的进程数）
* 内存
* 启动前的前置步骤

## 内存 { #memory }

如果你**每个容器只运行一个进程**，那么每个容器消耗的内存将更容易定义、较为稳定且有限（如果有复制则为多个容器）。

接着，你可以在容器管理系统（例如 **Kubernetes**）的配置中设置同样的内存限制与需求。这样它就能在**可用的机器**上**复制容器**，同时考虑容器所需的内存量以及集群中机器可用的内存量。

如果你的应用很**简单**，这可能**不成问题**，你也许不需要设置严格的内存上限。但如果你**使用大量内存**（例如使用**机器学习**模型），你应该检查自己的内存消耗，并调整**每台机器**上运行的**容器数量**（也许还需要为集群增加机器）。

如果你**每个容器运行多个进程**，你需要确保启动的进程数量不会**消耗超过可用的内存**。

## 启动前的前置步骤与容器 { #previous-steps-before-starting-and-containers }

如果你在使用容器（如 Docker、Kubernetes），你可以采用两种主要方式。

### 多个容器 { #multiple-containers }

如果你有**多个容器**，可能每个容器运行一个**单独进程**（例如在 **Kubernetes** 集群中），那么你可能希望使用一个**单独的容器**来执行**前置步骤**，在一个容器中运行一个进程，**在**启动那些复制的 worker 容器**之前**完成。

/// info | 信息

如果你使用 Kubernetes，这通常会是一个 <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>。

///

如果在你的用例中，**并行多次**运行这些前置步骤没有问题（例如你不是在跑数据库迁移，而只是检查数据库是否就绪），那么你也可以把这些步骤放在每个容器中，在启动主进程之前执行。

### 单个容器 { #single-container }

如果你的架构较为简单，使用一个**单个容器**，其后再启动多个**worker 进程**（或者也只有一个进程），那么你可以在同一个容器中，在启动应用进程之前执行这些前置步骤。

### 基础 Docker 镜像 { #base-docker-image }

曾经有一个官方的 FastAPI Docker 镜像：<a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>。但它现在已被弃用。⛔️

你大概率**不应该**使用这个基础镜像（或任何其它类似的镜像）。

如果你使用 **Kubernetes**（或其他）并且已经在集群层面设置**复制**、使用多个**容器**，那么在这些情况下，最好如上所述**从头构建镜像**：[为 FastAPI 构建 Docker 镜像](#build-a-docker-image-for-fastapi)。

如果你需要多个 workers，可以直接使用 `--workers` 命令行选项。

/// note | 技术细节

这个 Docker 镜像创建于 Uvicorn 还不支持管理与重启失效 workers 的时期，那时需要用 Gunicorn 搭配 Uvicorn，这引入了不少复杂度，只是为了让 Gunicorn 管理并重启 Uvicorn 的 worker 进程。

但现在 Uvicorn（以及 `fastapi` 命令）已经支持使用 `--workers`，因此没有理由不自己构建基础镜像（代码量几乎一样 😅）。

///

## 部署容器镜像 { #deploy-the-container-image }

得到容器（Docker）镜像后，有多种方式可以部署。

例如：

* 在单台服务器上使用 **Docker Compose**
* 使用 **Kubernetes** 集群
* 使用 Docker Swarm Mode 集群
* 使用 Nomad 等其他工具
* 使用云服务，接收你的容器镜像并部署

## 使用 `uv` 的 Docker 镜像 { #docker-image-with-uv }

如果你使用 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a> 来安装和管理项目，可以参考他们的 <a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">uv Docker 指南</a>。

## 回顾 { #recap }

使用容器系统（例如 **Docker** 与 **Kubernetes**）后，处理所有**部署概念**会变得相当直接：

* HTTPS
* 启动时运行
* 失败重启
* 复制（运行的进程数）
* 内存
* 启动前的前置步骤

在大多数情况下，你可能不想使用任何基础镜像，而是基于官方 Python Docker 镜像**从头构建容器镜像**。

注意 `Dockerfile` 中指令的**顺序**并利用好**Docker 缓存**，可以**最小化构建时间**，以最大化生产力（并避免无聊）。😎
