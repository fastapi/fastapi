![FastAPI](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-114916.png)

<center>FastAPI框架，高性能，易于学习，快速编码，为生产环境而准备</center>



![Build Status](https://travis-ci.com/tiangolo/fastapi.svg?branch=master)![Coverage](https://codecov.io/gh/tiangolo/fastapi/branch/master/graph/badge.svg)![Join the chat at https://gitter.im/tiangolo/fastapi](https://badges.gitter.im/tiangolo/fastapi.svg)![Package version](https://badge.fury.io/py/fastapi.svg)

---

**官方文档地址：**[https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

**源码地址：**[https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)

---

FastAPI是一种现代的，快速的（高性能）的Web框架，基于标准Python类型提示构建的API，使用的Python的版本应该3.6+。

主要有以下几个功能：

- **快：** 与NodeJS和Go相当的高性能（感谢Starlette和Pydantic）。 [最快的Python框架之一](https://github.com/tiangolo/fastapi/blob/master/docs/index.md#performance)
- **快速编码：** 开发速度提升2到3倍
- **更少的bug：** 减少约40％的人为原因导致的bug
- **直观：** 强大的编辑器支持，更快完成，调试时间更少
- **简单：** 易于使用和学习，减少阅读文档的时间
- **简短：** 减少代码重复。每个参数代表多个功能。 更少的错误
- **健壮：** 获得可用于生产的代码。具有自动交互式文档
- **基于标准：** 基于（并且完全兼容）API的开放标准：OpenAPI（以前称为Swagger）和JSON模式

## 关于FastAPI的评价

这些天，我大量使用FastAPI。...我实际上正在计划将其用于Microsoft团队的所有ML服务。 其中一些已集成到核心Windows产品和某些Office产品中。

<p align='right'>——Kabir Khan - Microsoft</p>

---

我对FastAPI感到欣喜若狂。太有趣了！

<p align='right'>——Brian Okken - Python Bytes podcast host</p>

---

老实说，你做的东西看起来很可靠和漂亮。从很多方面来说，这就是我希望**Hug**成为的样子。看到有人这么做，真的很鼓舞人心。

<p align='right'>Timothy Crosley - Hug creator</p>

---

如果您想学习一种构建REST API的现代框架，请查看FastAPI，它既快速，易于使用又易于学习。

我们已将我们的API切换到为FastAPI了，我认为您也会喜欢它。

<p align='right'>Ines Montani - Matthew Honnibal - Explosion AIfounders - spaCycreators</p>

---

我们采用了FastAPI库来生成一个REST服务器，可以查询该服务器以获得预期效果。（对于Ludwig）

<p align='right'>——Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - Uber</p>

## 基本要求

1.  Python 3.6+

2.  FastAPI 基于：
    -   web部分：[Starlette](https://www.starlette.io/)
    -   data部分：[Pydantic](https://pydantic-docs.helpmanual.io/)

## 安装方式

```shell
pip install fastapi
```

您还需要一个ASGI服务器，用于[Uvicorn](http://www.uvicorn.org/)或[Hypercorn](https://gitlab.com/pgjones/hypercorn)等都可以

```shell
pip install uvicorn
```

## 简单示例

### 创建

-   创建文件 `main.py`

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

如果您的代码使用了`async` / `await`，请使用 `async def` ：

```shell
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### 运行服务

使用以下命令运行服务

```shell
uvicorn main:app --reload
```

关于这条命令的说明：

-   `main` : 指文件 `main.py` 
-   `app` ：在 `main.py` 文件内部创建的对象，其中包含 `app = FastAPI()`
-   `--reload` ：重新加载，指在代码更改后重新启动服务（仅在开发时使用）

### 检查运行效果

在浏览器中输入[http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)，您将看到JSON响应

```json
{"item_id": 5, "q": "somequery"}
```

现在，您已经创建好了一个API：

-   在路径 `/` 和`/items/{item_id}` 接收HTTP请求
-   这两个路径都是`GET`请求方式
-   在路径`/items/{item_id}`有一个参数`item_id`，并且这个参数应该是`int`类型的
-   路径`/items/{item_id}`有一个可选的`str`类型参数`q`

### 交互式API文档

现在进入到[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)路径，您将看到自动交互式API文档（由[Swagger UI](https://github.com/swagger-api/swagger-ui)提供）：

![Swagger UI](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-134300.png)

### 另一个API文档

现在，切换到[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)路径，您将看到另一个自动文档(由[ReDoc](https://github.com/Rebilly/ReDoc)提供)

![ReDoc](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-135552.png)

## 升级示例

现在，修改文件`main.py`，用来接收来自`PUT`请求的`body`

使用标准的Python类型声明`body`，得益于Pydantic

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

此时，服务应该进行了自动重新加载（因为前边的 `uvicorn`命令，添加了`--reload`参数）

### 升级示例的交互式API文档

现在进入到[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)路径

-   交互式API文档也会自动更新，包括新的`body`：

![Swagger UI](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-140325.png)

-   单击`Try it out`按钮 ，它允许您填充参数并直接与API交互：

![Swagger UI interaction](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-140712.png)

-   然后单击`Execute`按钮，将与您的API通信，发送参数，获取结果并将其显示在屏幕上：

![Swagger UI interaction](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-142225.png)

### 升级示例的另一个API文档

现在切换到[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) 路径

-   另一个文档将展示新的查询参数和正文，如下：

![ReDoc](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-143634.png)

### 总结

综上所述，您可以**一次性**将`params`、`body`等的类型，声明为函数的参数，并且使用标准的Python类型就可以做到这一点。

您不必学习新的语法，特定库的方法或类等，而只是标准的**Python 3.6+**。

例如，对于一个`int 类型：`

```python
item_id: int
```

或者更复杂的`Item`：

```python
item: Item
```

你还可以得到：

-   编译器的支持，比如：
    -   代码提示
    -   类型检查
-   数据验证
    -   数据无效时自动清除错误
    -   甚至对深度嵌套的JSON对象也能进行验证
-   输入数据转换：来自网络的以下数据类型到Python数据类型的转换
    -   JSON
    -   路径参数
    -   查询参数
    -   Cookies
    -   Headers
    -   Forms
    -   Files
-   输出数据的转换：从Python数据类型转换为网络数据（比如JSON）：
    -   转换Python数据类型（`str`,`int`,`float`,`bool`,`list`等）
    -   `datetime`对象
    -   `UUID`对象
    -   Database models
    -   ...
-   自动交互API文档，包括两个备选的用户界面:
    -   Swagger UI
    -   ReDoc。

---

现在回到前面的代码，示例中，**FastAPI** 将完成：

-   验证`GET`和`PUT`请求的路径中是否有`item_id`
-   验证`GET`和`PUT`请求中`item_id`是否为`int`类型
    -   如果不是，客户端将清楚看到一个有用的错误提示
-   检查`GET`请求中是否有一个名为`q`的可选查询参数（如：`http://127.0.0.1:8000/items/foo?q=somequery`）
    -   由于`q`参数用`= None`声明，因此它是可选的
    -   如果没有`None`，则`q`参数是必需的（与PUT的情况一样）
-   对`/items/{item_id}`的`PUT`请求，将以JSON格式读取`body`：
    -   检查它是否具有必需的参数`name`，类型应该是`str`
    -   检查它是否具有必需的参数`price`，类型必须是`float`
    -   检查它是否具有非必需的参数`is_offer`，如果这个参数存在，类应该是`bool`
    -   以上对深度嵌套的JSON对象也适用
-   自动将其转换为JSON
-   使用OpenAPI记录所有可以被下面使用的内容：
    -   交互式文档系统
    -   适用于多种语言的客户端代码自动生成系统
-   直接提供2个交互式文档Web界面

---

虽然文档才刚刚开始，但是您已经了解了FastAPI究竟能够干些什么

试着按照下面的内容更改代码：

```python
    return {"item_name": item.name, "item_id": item_id}
```

原来是：

```python
        ... "item_name": item.name ...
```

修改成：

```python
        ... "item_price": item.price ...
```

查看编辑器如何自动提示它们的属性名称和类型：

![editor support](http://linupyoos.oss-cn-beijing.aliyuncs.com/blogs/2020-02-29-151804.png)

有关包含更多特性的完整示例，请参见[Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)

**提前剧透：** `tutorial - user guide` 包括以下内容：

-   来自不同地方的**参数**声明，比如： **headers**，**cookies**， **form 字段** ，**files**
-   如何将**验证约束**设置为`最大长度`或`正则表达式`
-   一个非常强大且易于使用的**依赖注入**系统
-   安全性和身份验证，包括对具有**JWT tokens**和**HTTP Basic**身份验证的**OAuth2**的支持
-   更高级（但同样简单）的声明 **深度嵌套JSON models**的方法（感谢Pydantic）
-   许多额外的功能（多亏了Starlette），比如：
    -   **WebSockets**
    -   **GraphQL**
    -   基于`requests`和`pytest`的极其简单的测试
    -   **CORS**
    -   **Cookie Sessions**
    -   ...

## 性能

独立的TechEmpower基准测试显示，在Uvicorn下运行的**FastAPI**应用程序是可用的[最快的Python框架之一](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)，仅低于Starlette和Uvicorn本身（由FastAPI内部使用）

要了解更多信息，请参阅[Benchmarks](https://fastapi.tiangolo.com/benchmarks/)部分。

## 可选依赖项

由Pydantic使用：

-   [`ujson`](https://github.com/esnme/ultrajson) - 更快的JSON解析
-   [`email_validator`](https://github.com/JoshData/python-email-validator) - 电子邮件验证

由Starlette使用：

-   [`requests`](http://docs.python-requests.org/) - 如果要使用`TestClient`，则需要`requests`
-   [`aiofiles`](https://github.com/Tinche/aiofiles) - 如果要使用`FileResponse`或`StaticFiles`，需要`aiofiles`
-   [`jinja2`](http://jinja.pocoo.org/) - 如果您想使用默认模板配置，则需要
-   [`python-multipart`](https://andrew-d.github.io/python-multipart/) - 如果要使用`request.form()`支持form解析，则为必需
-   [`itsdangerous`](https://pythonhosted.org/itsdangerous/) - 对于`SessionMiddleware`支持是必需的
-   [`pyyaml`](https://pyyaml.org/wiki/PyYAMLDocumentation) - 对于`Starlette`的`SchemaGenerator`支持是必需的（`FastAPI`可能不需要它）
-   [`graphene`](https://graphene-python.org/) - 对于`GraphQLApp`支持是必需的
-   [`ujson`](https://github.com/esnme/ultrajson) - 如果您想使用`UJSONResponse`，则是必需的

由FastAPI/Starlette使用：

-   [`uvicorn`](http://www.uvicorn.org/) - 用于加载和启动应用程序服务器

您可以使用`pip install fastapi `安装以上所有工具

## 许可

该项目根据MIT许可条款获得许可。
