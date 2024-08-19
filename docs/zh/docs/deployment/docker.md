# 容器中的 FastAPI - Docker

部署 FastAPI 应用程序时，常见的方法是构建 **Linux 容器镜像**。 通常使用 <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> 完成。 然后，你可以通过几种可能的方式之一部署该容器镜像。

使用 Linux 容器有几个优点，包括**安全性**、**可复制性**、**简单性**等。

/// tip

赶时间并且已经知道这些东西了？ 跳转到下面的 [`Dockerfile` 👇](#fastapi-docker_1)。

///

<details>
<summary>Dockerfile Preview 👀</summary>

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
```

</details>

## 什么是容器

容器（主要是 Linux 容器）是一种非常**轻量级**的打包应用程序的方式，其包括所有依赖项和必要的文件，同时它们可以和同一系统中的其他容器（或者其他应用程序/组件）相互隔离。

Linux 容器使用宿主机（如物理服务器、虚拟机、云服务器等）的Linux 内核运行。 这意味着它们非常轻量（与模拟整个操作系统的完整虚拟机相比）。

通过这样的方式，容器消耗**很少的资源**，与直接运行进程相当（虚拟机会消耗更多）。

容器的进程（通常只有一个）、文件系统和网络都运行在隔离的环境，这简化了部署、安全、开发等。

## 什么是容器镜像

**容器**是从**容器镜像**运行的。

容器镜像是容器中文件、环境变量和默认命令/程序的**静态**版本。 **静态**这里的意思是容器**镜像**还没有运行，只是打包的文件和元数据。

与存储静态内容的“**容器镜像**”相反，“**容器**”通常指正在运行的实例，即正在**执行的**。

当**容器**启动并运行时（从**容器镜像**启动），它可以创建或更改文件、环境变量等。这些更改将仅存在于该容器中，而不会持久化到底层的容器镜像中（不会保存到磁盘）。

容器镜像相当于**程序**和文件，例如 `python`命令 和某些文件 如`main.py`。

而**容器**本身（与**容器镜像**相反）是镜像的实际运行实例，相当于**进程**。 事实上，容器仅在有**进程运行**时才运行（通常它只是一个单独的进程）。 当容器中没有进程运行时，容器就会停止。



## 容器镜像

Docker 一直是创建和管理**容器镜像**和**容器**的主要工具之一。

还有一个公共 <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a> ，其中包含预制的 **官方容器镜像**, 适用于许多工具、环境、数据库和应用程序。

例如，有一个官方的 <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Python 镜像</a>。

还有许多其他镜像用于不同的需要（例如数据库），例如：


* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a>, etc.


通过使用预制的容器镜像，可以非常轻松地**组合**并使用不同的工具。 例如，尝试一个新的数据库。 在大多数情况下，你可以使用**官方镜像**，只需为其配置环境变量即可。

这样，在许多情况下，你可以了解容器和 Docker，并通过许多不同的工具和组件重复使用这些知识。

因此，你可以运行带有不同内容的**多个容器**，例如数据库、Python 应用程序、带有 React 前端应用程序的 Web 服务器，并通过内部网络将它们连接在一起。

所有容器管理系统（如 Docker 或 Kubernetes）都集成了这些网络功能。

## 容器和进程

**容器镜像**通常在其元数据中包含启动**容器**时应运行的默认程序或命令以及要传递给该程序的参数。 与在命令行中的情况非常相似。

当 **容器** 启动时，它将运行该命令/程序（尽管你可以覆盖它并使其运行不同的命令/程序）。

只要**主进程**（命令或程序）在运行，容器就在运行。

容器通常有一个**单个进程**，但也可以从主进程启动子进程，这样你就可以在同一个容器中拥有**多个进程**。

但是，如果没有**至少一个正在运行的进程**，就不可能有一个正在运行的容器。 如果主进程停止，容器也会停止。


## 为 FastAPI 构建 Docker 镜像

好吧，让我们现在构建一些东西！ 🚀

我将向你展示如何基于 **官方 Python** 镜像 **从头开始** 为 FastAPI 构建 **Docker 镜像**。

这是你在**大多数情况**下想要做的，例如：

* 使用 **Kubernetes** 或类似工具
* 在 **Raspberry Pi** 上运行时
* 使用可为你运行容器镜像的云服务等。

### 依赖项

你通常会在某个文件中包含应用程序的**依赖项**。

具体做法取决于你**安装**这些依赖时所使用的工具。

最常见的方法是创建一个`requirements.txt`文件，其中每行包含一个包名称和它的版本。

你当然也可以使用在[关于 FastAPI 版本](versions.md){.internal-link target=_blank} 中讲到的方法来设置版本范围。

例如，你的`requirements.txt`可能如下所示：


```
fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
```

你通常会使用`pip`安装这些依赖项：

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic uvicorn
```

</div>

/// info

还有其他文件格式和工具来定义和安装依赖项。

 我将在下面的部分中向你展示一个使用 Poetry 的示例。 👇

///

### 创建 **FastAPI** 代码

* 创建`app`目录并进入。
* 创建一个空文件`__init__.py`。
* 创建一个 `main.py` 文件：



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

### Dockerfile

现在在相同的project目录创建一个名为`Dockerfile`的文件:

```{ .dockerfile .annotate }
# (1)
FROM python:3.9

# (2)
WORKDIR /code

# (3)
COPY ./requirements.txt /code/requirements.txt

# (4)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)
COPY ./app /code/app

# (6)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

1. 从官方Python基础镜像开始。

2. 将当前工作目录设置为`/code`。

     这是我们放置`requirements.txt`文件和`app`目录的位置。

3. 将符合要求的文件复制到`/code`目录中。

     首先仅复制requirements.txt文件，而不复制其余代码。

     由于此文件**不经常更改**，Docker 将检测到它并在这一步中使用**缓存**，从而为下一步启用缓存。

4. 安装需求文件中的包依赖项。

     `--no-cache-dir` 选项告诉 `pip` 不要在本地保存下载的包，因为只有当 `pip` 再次运行以安装相同的包时才会这样，但在与容器一起工作时情况并非如此。

     /// note | 笔记

     `--no-cache-dir` 仅与 `pip` 相关，与 Docker 或容器无关。

     ///

     `--upgrade` 选项告诉 `pip` 升级软件包（如果已经安装）。

     因为上一步复制文件可以被 **Docker 缓存** 检测到，所以此步骤也将 **使用 Docker 缓存**（如果可用）。

     在开发过程中一次又一次构建镜像时，在此步骤中使用缓存将为你节省大量**时间**，而不是**每次**都**下载和安装**所有依赖项。


5. 将“./app”目录复制到“/code”目录中。

     由于其中包含**更改最频繁**的所有代码，因此 Docker **缓存**不会轻易用于此操作或任何**后续步骤**。

     因此，将其放在`Dockerfile`**接近最后**的位置非常重要，以优化容器镜像的构建时间。

6. 设置**命令**来运行 `uvicorn` 服务器。

     `CMD` 接受一个字符串列表，每个字符串都是你在命令行中输入的内容，并用空格分隔。

     该命令将从 **当前工作目录** 运行，即你上面使用`WORKDIR /code`设置的同一`/code`目录。

     因为程序将从`/code`启动，并且其中包含你的代码的目录`./app`，所以**Uvicorn**将能够从`app.main`中查看并**import**`app`。

/// tip

通过单击代码中的每个数字气泡来查看每行的作用。 👆

///

你现在应该具有如下目录结构：
```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```


#### 在 TLS 终止代理后面

如果你在 Nginx 或 Traefik 等 TLS 终止代理（负载均衡器）后面运行容器，请添加选项 `--proxy-headers`，这将告诉 Uvicorn 信任该代理发送的标头，告诉它应用程序正在 HTTPS 后面运行等信息

```Dockerfile
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

#### Docker 缓存

这个`Dockerfile`中有一个重要的技巧，我们首先只单独复制**包含依赖项的文件**，而不是其余代码。 让我来告诉你这是为什么。

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker之类的构建工具是通过**增量**的方式来构建这些容器镜像的。具体做法是从`Dockerfile`顶部开始，每一条指令生成的文件都是镜像的“一层”，同过把这些“层”一层一层地叠加到基础镜像上，最后我们就得到了最终的镜像。

Docker 和类似工具在构建镜像时也会使用**内部缓存**，如果自上次构建容器镜像以来文件没有更改，那么它将**重新使用上次创建的同一层**，而不是再次复制文件并从头开始创建新层。

仅仅避免文件的复制不一定会有太多速度提升，但是如果在这一步使用了缓存，那么才可以**在下一步中使用缓存**。 例如，可以使用安装依赖项那条指令的缓存：

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```


包含包依赖项的文件**不会频繁更改**。 只复制该文件（不复制其他的应用代码），Docker 才能在这一步**使用缓存**。

Docker 进而能**使用缓存进行下一步**，即下载并安装这些依赖项。 这才是我们**节省大量时间**的地方。 ✨ ...可以避免无聊的等待。 😪😆

下载和安装依赖项**可能需要几分钟**，但使用**缓存**最多**只需要几秒钟**。

由于你在开发过程中会一次又一次地构建容器镜像以检查代码更改是否有效，因此可以累计节省大量时间。

在`Dockerfile`末尾附近，我们再添加复制代码的指令。 由于代码是**更改最频繁的**，所以将其放在最后，因为这一步之后的内容基本上都是无法使用缓存的。

```Dockerfile
COPY ./app /code/app
```

### 构建 Docker 镜像

现在所有文件都已就位，让我们构建容器镜像。

* 转到项目目录（在`Dockerfile`所在的位置，包含`app`目录）。
* 构建你的 FastAPI 镜像：


<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>


/// tip

注意最后的 `.`，它相当于`./`，它告诉 Docker 用于构建容器镜像的目录。

在本例中，它是相同的当前目录（`.`）。

///

### 启动 Docker 容器

* 根据你的镜像运行容器：

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## 检查一下


你应该能在Docker容器的URL中检查它，例如: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 或 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (或其他等价的，使用 Docker 主机).

你会看到类似内容：

```JSON
{"item_id": 5, "q": "somequery"}
```

## 交互式 API 文档

现在你可以转到 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 或 <a href ="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> （或其他等价的，使用 Docker 主机）。

你将看到自动交互式 API 文档（由 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a 提供） >):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 备选的 API 文档

你还可以访问 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 或 <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> （或其他等价的，使用 Docker 主机）。

你将看到备选的自动文档（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 提供）：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 使用单文件 FastAPI 构建 Docker 镜像

如果你的 FastAPI 是单个文件，例如没有`./app`目录的`main.py`，则你的文件结构可能如下所示：

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

然后你只需更改相应的路径即可将文件复制到`Dockerfile`中：

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)
COPY ./main.py /code/

# (2)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

1. 直接将`main.py`文件复制到`/code`目录中（不包含任何`./app`目录）。

2. 运行 Uvicorn 并告诉它从 `main` 导入 `app` 对象（而不是从 `app.main` 导入）。

然后调整Uvicorn命令使用新模块`main`而不是`app.main`来导入FastAPI 实例`app`。

## 部署概念

我们再谈谈容器方面的一些相同的[部署概念](concepts.md){.internal-link target=_blank}。

容器主要是一种简化**构建和部署**应用程序的过程的工具，但它们并不强制执行特定的方法来处理这些**部署概念**，并且有几种可能的策略。

**好消息**是，对于每种不同的策略，都有一种方法可以涵盖所有部署概念。 🎉

让我们从容器的角度回顾一下这些**部署概念**：

* HTTPS
* 启动时运行
* 重新启动
* 复制（运行的进程数）
* 内存
* 开始前的先前步骤


## HTTPS

如果我们只关注 FastAPI 应用程序的 **容器镜像**（以及稍后运行的 **容器**），HTTPS 通常会由另一个工具在 **外部** 处理。

它可以是另一个容器，例如使用 <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>，处理 **HTTPS** 和 **自动**获取**证书**。

/// tip

Traefik可以与 Docker、Kubernetes 等集成，因此使用它为容器设置和配置 HTTPS 非常容易。

///

或者，HTTPS 可以由云服务商作为其服务之一进行处理（同时仍在容器中运行应用程序）。

## 在启动和重新启动时运行

通常还有另一个工具负责**启动和运行**你的容器。

它可以直接是**Docker**, 或者**Docker Compose**、**Kubernetes**、**云服务**等。

在大多数（或所有）情况下，有一个简单的选项可以在启动时运行容器并在失败时重新启动。 例如，在 Docker 中，它是命令行选项 `--restart`。

如果不使用容器，让应用程序在启动时运行并重新启动可能会很麻烦且困难。 但在大多数情况下，当**使用容器**时，默认情况下会包含该功能。 ✨

## 复制 - 进程数

如果你有一个 <abbr title="一组配置为以某种方式连接并协同工作的计算机。">集群</abbr>, 比如 **Kubernetes**、Docker Swarm、Nomad 或其他类似的复杂系统来管理多台机器上的分布式容器，那么你可能希望在**集群级别**处理复制**，而不是在每个容器中使用**进程管理器**（如带有Worker的 Gunicorn） 。

像 Kubernetes 这样的分布式容器管理系统通常有一些集成的方法来处理**容器的复制**，同时仍然支持传入请求的**负载均衡**。 全部都在**集群级别**。

在这些情况下，你可能希望从头开始构建一个 **Docker 镜像**，如[上面所解释](#dockerfile)的那样，安装依赖项并运行 **单个 Uvicorn 进程**，而不是运行 Gunicorn 和 Uvicorn workers这种。


### 负载均衡器

使用容器时，通常会有一些组件**监听主端口**。 它可能是处理 **HTTPS** 的 **TLS 终止代理** 或一些类似的工具的另一个容器。

由于该组件将接受请求的**负载**并（希望）以**平衡**的方式在worker之间分配该请求，因此它通常也称为**负载均衡器**。

/// tip

用于 HTTPS **TLS 终止代理** 的相同组件也可能是 **负载均衡器**。

///

当使用容器时，你用来启动和管理容器的同一系统已经具有内部工具来传输来自该**负载均衡器**（也可以是**TLS 终止代理**) 的**网络通信**（例如HTTP请求）到你的应用程序容器。

### 一个负载均衡器 - 多个worker容器

当使用 **Kubernetes** 或类似的分布式容器管理系统时，使用其内部网络机制将允许单个在主 **端口** 上侦听的 **负载均衡器** 将通信（请求）传输到可能的 **多个** 运行你应用程序的容器。

运行你的应用程序的每个容器通常**只有一个进程**（例如，运行 FastAPI 应用程序的 Uvicorn 进程）。 它们都是**相同的容器**，运行相同的东西，但每个容器都有自己的进程、内存等。这样你就可以在 CPU 的**不同核心**， 甚至在**不同的机器**充分利用**并行化(parallelization)**。

具有**负载均衡器**的分布式容器系统将**将请求轮流分配**给你的应用程序的每个容器。 因此，每个请求都可以由运行你的应用程序的多个**复制容器**之一来处理。

通常，这个**负载均衡器**能够处理发送到集群中的*其他*应用程序的请求（例如发送到不同的域，或在不同的 URL 路径前缀下），并正确地将该通信传输到在集群中运行的*其他*应用程序的对应容器。






### 每个容器一个进程

在这种类型的场景中，你可能希望**每个容器有一个（Uvicorn）进程**，因为你已经在集群级别处理复制。

因此，在这种情况下，你**不会**希望拥有像 Gunicorn 和 Uvicorn worker一样的进程管理器，或者 Uvicorn 使用自己的 Uvicorn worker。 你可能希望每个容器（但可能有多个容器）只有一个**单独的 Uvicorn 进程**。

在容器内拥有另一个进程管理器（就像使用 Gunicorn 或 Uvicorn 管理 Uvicorn 工作线程一样）只会增加**不必要的复杂性**，而你很可能已经在集群系统中处理这些复杂性了。

### 具有多个进程的容器

当然，在某些**特殊情况**，你可能希望拥有 **一个容器**，其中包含 **Gunicorn 进程管理器**，并在其中启动多个 **Uvicorn worker进程**。

在这些情况下，你可以使用 **官方 Docker 镜像**，其中包含 **Gunicorn** 作为运行多个 **Uvicorn 工作进程** 的进程管理器，以及一些默认设置来根据当前情况调整工作进程数量 自动CPU核心。 我将在下面的 [Gunicorn - Uvicorn 官方 Docker 镜像](#official-docker-image-with-gunicorn-uvicorn) 中告诉你更多相关信息。

下面一些什么时候这种做法有意义的示例：


#### 一个简单的应用程序

如果你的应用程序**足够简单**，你不需要（至少现在不需要）过多地微调进程数量，并且你可以使用自动默认值，那么你可能需要容器中的进程管理器 （使用官方 Docker 镜像），并且你在**单个服务器**而不是集群上运行它。

#### Docker Compose

你可以使用 **Docker Compose** 部署到**单个服务器**（而不是集群），因此你没有一种简单的方法来管理容器的复制（使用 Docker Compose），同时保留共享网络和 **负载均衡**。

然后，你可能希望拥有一个**单个容器**，其中有一个**进程管理器**，在其中启动**多个worker进程**。

#### Prometheus和其他原因

你还可能有**其他原因**，这将使你更容易拥有一个带有**多个进程**的**单个容器**，而不是拥有每个容器中都有**单个进程**的**多个容器**。

例如（取决于你的设置）你可以在同一个容器中拥有一些工具，例如 Prometheus exporter，该工具应该有权访问**每个请求**。

在这种情况下，如果你有**多个容器**，默认情况下，当 Prometheus 来**读取metrics**时，它每次都会获取**单个容器**的metrics（对于处理该特定请求的容器），而不是获取所有复制容器的**累积metrics**。

在这种情况， 这种做法会更加简单：让**一个容器**具有**多个进程**，并在同一个容器上使用本地工具（例如 Prometheus exporter）收集所有内部进程的 Prometheus 指标并公开单个容器上的这些指标。

---

要点是，这些都**不是**你必须盲目遵循的**一成不变的规则**。 你可以根据这些思路**评估你自己的场景**并决定什么方法是最适合你的的系统，考虑如何管理以下概念：

* 安全性 - HTTPS
* 启动时运行
* 重新启动
* 复制（运行的进程数）
* 内存
* 开始前的先前步骤

## 内存

如果你**每个容器运行一个进程**，那么每个容器所消耗的内存或多或少是定义明确的、稳定的且有限的（如果它们是复制的，则不止一个）。

然后，你可以在容器管理系统的配置中设置相同的内存限制和要求（例如在 **Kubernetes** 中）。 这样，它将能够在**可用机器**中**复制容器**，同时考虑容器所需的内存量以及集群中机器中的可用内存量。

如果你的应用程序很**简单**，这可能**不是问题**，并且你可能不需要指定内存限制。 但是，如果你**使用大量内存**（例如使用**机器学习**模型），则应该检查你消耗了多少内存并调整**每台机器**中运行的**容器数量**（也许可以向集群添加更多机器）。

如果你**每个容器运行多个进程**（例如使用官方 Docker 镜像），你必须确保启动的进程数量不会消耗比可用内存**更多的内存**。

## 启动之前的步骤和容器

如果你使用容器（例如 Docker、Kubernetes），那么你可以使用两种主要方法。


### 多个容器

如果你有 **多个容器**，可能每个容器都运行一个 **单个进程**（例如，在 **Kubernetes** 集群中），那么你可能希望有一个 **单独的容器** 执行以下操作： 在单个容器中运行单个进程执行**先前步骤**，即运行复制的worker容器之前。

/// info

如果你使用 Kubernetes，这可能是 <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>。

///

如果在你的用例中，运行前面的步骤**并行多次**没有问题（例如，如果你没有运行数据库迁移，而只是检查数据库是否已准备好），那么你也可以将它们放在开始主进程之前在每个容器中。

### 单容器

如果你有一个简单的设置，使用一个**单个容器**，然后启动多个**工作进程**（或者也只是一个进程），那么你可以在启动进程之前在应用程序同一个容器中运行先前的步骤。 官方 Docker 镜像内部支持这一点。

## 带有 Gunicorn 的官方 Docker 镜像 - Uvicorn

有一个官方 Docker 镜像，其中包含与 Uvicorn worker一起运行的 Gunicorn，如上一章所述：[服务器工作线程 - Gunicorn 与 Uvicorn](server-workers.md){.internal-link target=_blank}。

该镜像主要在上述情况下有用：[具有多个进程和特殊情况的容器](#containers-with-multiple-processes-and-special-cases)。



* <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.


/// warning

你很有可能不需要此基础镜像或任何其他类似的镜像，最好从头开始构建镜像，如[上面所述：为 FastAPI 构建 Docker 镜像](#build-a-docker-image-for-fastapi)。

///

该镜像包含一个**自动调整**机制，用于根据可用的 CPU 核心设置**worker进程数**。

它具有**合理的默认值**，但你仍然可以使用**环境变量**或配置文件更改和更新所有配置。

它还支持通过一个脚本运行<a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#pre_start_path" class="external-link" target="_blank">**开始前的先前步骤** </a>。

/// tip

要查看所有配置和选项，请转到 Docker 镜像页面： <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank" >tiangolo/uvicorn-gunicorn-fastapi</a>。

///

### 官方 Docker 镜像上的进程数

此镜像上的**进程数**是根据可用的 CPU **核心**自动计算的。

这意味着它将尝试尽可能多地**榨取**CPU 的**性能**。

你还可以使用 **环境变量** 等配置来调整它。

但这也意味着，由于进程数量取决于容器运行的 CPU，因此**消耗的内存量**也将取决于该数量。

因此，如果你的应用程序消耗大量内存（例如机器学习模型），并且你的服务器有很多 CPU 核心**但内存很少**，那么你的容器最终可能会尝试使用比实际情况更多的内存 可用，并且性能会下降很多（甚至崩溃）。 🚨

### 创建一个`Dockerfile`

以下是如何根据此镜像创建`Dockerfile`：


```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

### 更大的应用程序

如果你按照有关创建[具有多个文件的更大应用程序](../tutorial/bigger-applications.md){.internal-link target=_blank}的部分进行操作，你的`Dockerfile`可能看起来这样：

```Dockerfile hl_lines="7"
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
```

### 何时使用

如果你使用 **Kubernetes** （或其他）并且你已经在集群级别设置 **复制**，并且具有多个 **容器**。 在这些情况下，你最好按照上面的描述 **从头开始构建镜像**：[为 FastAPI 构建 Docker 镜像](#build-a-docker-image-for-fastapi)。

该镜像主要在[具有多个进程的容器和特殊情况](#containers-with-multiple-processes-and-special-cases)中描述的特殊情况下有用。 例如，如果你的应用程序**足够简单**，基于 CPU 设置默认进程数效果很好，你不想在集群级别手动配置复制，并且不会运行更多进程,  或者你使用 **Docker Compose** 进行部署，在单个服务器上运行等。

## 部署容器镜像

拥有容器（Docker）镜像后，有多种方法可以部署它。

例如：

* 在单个服务器中使用 **Docker Compose**
* 使用 **Kubernetes** 集群
* 使用 Docker Swarm 模式集群
* 使用Nomad等其他工具
* 使用云服务获取容器镜像并部署它

## Docker 镜像与Poetry

如果你使用 <a href="https://python-poetry.org/" class="external-link" target="_blank">Poetry</a> 来管理项目的依赖项，你可以使用 Docker 多阶段构建：



```{ .dockerfile .annotate }
# (1)
FROM python:3.9 as requirements-stage

# (2)
WORKDIR /tmp

# (3)
RUN pip install poetry

# (4)
COPY ./pyproject.toml ./poetry.lock* /tmp/

# (5)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# (6)
FROM python:3.9

# (7)
WORKDIR /code

# (8)
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# (9)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (10)
COPY ./app /code/app

# (11)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

1. 这是第一阶段，称为`requirements-stage`。

2. 将 `/tmp` 设置为当前工作目录。

     这是我们生成文件`requirements.txt`的地方

3. 在此阶段安装Poetry。

4. 将`pyproject.toml`和`poetry.lock`文件复制到`/tmp`目录。

     因为它使用 `./poetry.lock*` （以 `*` 结尾），所以如果该文件尚不可用，它不会崩溃。

5. 生成`requirements.txt`文件。

6. 这是最后阶段，这里的任何内容都将保留在最终的容器镜像中。

7. 将当前工作目录设置为`/code`。

8. 将 `requirements.txt` 文件复制到 `/code` 目录。

     该文件仅存在于前一个阶段，这就是为什么我们使用 `--from-requirements-stage` 来复制它。

9. 安装生成的`requirements.txt`文件中的依赖项。

10. 将`app`目录复制到`/code`目录。

11. 运行`uvicorn`命令，告诉它使用从`app.main`导入的`app`对象。

/// tip

单击气泡数字可查看每行的作用。

///

**Docker stage** 是 `Dockerfile` 的一部分，用作 **临时容器镜像**，仅用于生成一些稍后使用的文件。

第一阶段仅用于 **安装 Poetry** 并使用 Poetry 的 `pyproject.toml` 文件中的项目依赖项 **生成 `requirements.txt`**。

此`requirements.txt`文件将在**下一阶段**与`pip`一起使用。

在最终的容器镜像中**仅保留最后阶段**。 之前的阶段将被丢弃。

使用 Poetry 时，使用 **Docker 多阶段构建** 是有意义的，因为你实际上并不需要在最终的容器镜像中安装 Poetry 及其依赖项，你 **只需要** 生成用于安装项目依赖项的`requirements.txt`文件。

然后，在下一个（也是最后一个）阶段，你将或多或少地以与前面描述的相同的方式构建镜像。

### 在TLS 终止代理后面 - Poetry

同样，如果你在 Nginx 或 Traefik 等 TLS 终止代理（负载均衡器）后面运行容器，请将选项`--proxy-headers`添加到命令中：


```Dockerfile
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

## 回顾

使用容器系统（例如使用**Docker**和**Kubernetes**），处理所有**部署概念**变得相当简单：

* HTTPS
* 启动时运行
* 重新启动
* 复制（运行的进程数）
* 内存
* 开始前的先前步骤

在大多数情况下，你可能不想使用任何基础镜像，而是基于官方 Python Docker 镜像 **从头开始构建容器镜像** 。

处理好`Dockerfile`和 **Docker 缓存**中指令的**顺序**，你可以**最小化构建时间**，从而最大限度地提高生产力（并避免无聊）。 😎

在某些特殊情况下，你可能需要使用 FastAPI 的官方 Docker 镜像。 🤓
