# 第一步

最简单的 FastAPI 文件所示如下：

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

复制代码到 `main.py`。

运行实时服务器：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

!!! note "笔记"

    `uvicorn main:app` 命令说明如下：
    
    * `main`：`main.py` 是 Python **模块**；
    * `app`：`main.py`  中 `app = FastAPI()` 创建的对象；
    * `--reload`：代码更新后，重启服务器。仅在开发时使用。

输出信息如下：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

这是 **FastAPI** 应用在本机提供服务的 URL。

### 查看文档

打开浏览器访问 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

JSON 响应如下：

```JSON
{"message": "Hello World"}
```

### API 文档

跳转到 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

查看自动生成的（<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>）API 文档：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 备选 API 文档

跳转到 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

查看自动生成的（<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>）备选文档 ：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** 使用 **OpenAPI** （定义 API 的标准 ）把所有 API 转换成**概图**。

#### 概图

**概图**是对事物的定义与描述，不是实现功能的代码，只是抽象的描述。

#### API 概图

本指南中，<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> 是定义 API 概图的规范。

这里的概图包括 API 路径、路径参数等。

#### 数据概图

**概图**这一术语也指 JSON 等数据的结构。

本指南中，数据概图是指 JSON 属性、数据类型等。

#### OpenAPI 和 JSON Schema

OpenAPI 用于定义 API 概图。该概图包含由 **JSON Schema** 为 API 发送与接收的数据所做的定义。**JSON Schema** 是 JSON 数据概图标准。

#### 查看 `openapi.json`

如果您对 OpenAPI 原始概图感兴趣，FastAPI 自动生成了描述所有 API 的 JSON （概图）。

直接查看：<a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>。

JSON 文件的开头如下：

```JSON
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### OpenAPI 是干什么用的

OpenAPI 概图用于驱动 FastAPI 内置的两个 API 文档。

基于 OpenAPI 的备选方案还有很多，为 **FastAPI** 应用添加其它备选方案很容易。

OpenAPI 还可以用于自动生成和 API 通信的客户端代码。例如前端、移动端、物联网应用等。

## 分步小结

### 第一步：导入 `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` 是为 API 提供所有功能的 Python 类。

!!! note "技术细节"

    `FastAPI` 是直接继承自 `Starlette` 的类。
    
    `FastAPI` 可以调用 Starlette 的所有功能。

### 第二步：创建 `FastAPI` 实例

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

变量 `app` 是 `FastAPI` 的**类实例**。

该实例是创建所有 API 的主要交互对象。

这个 `app` 就是如下命令中由 `uvicorn` 引用的变量：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

如果用下面的代码创建应用：

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

把代码存入 `main.py`，要以如下方式调用 `uvicorn`：

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### 第三步：创建*路径操作*

#### 路径

**路径**是指 URL 的第一个反斜杠（`/`）及它之后的内容。

下列 URL 中：

```
https://example.com/items/foo
```

……**路径**是：

```
/items/foo
```

!!! info "说明"

    **路径**通常也叫作**端点**或**路由**。

开发 API 时，**路径**是分离 **concerns** 和 **resources** 的主要方式。

#### 操作

**操作**是指 HTTP **方法**。

常用方法如下：

- `POST`
- `GET`
- `PUT`
- `DELETE`

罕见方法如下：

- `OPTIONS`
- `HEAD`
- `PATCH`
- `TRACE`

HTTP 协议支持使用上述任何一种（或多种）**方法**与路径通信。

---

开发 API 时，通常要使用特定 HTTP 方法执行特定操作。

常用方法：

- `POST`：创建数据
- `GET`：读取数据
- `PUT`：更新数据
- `DELETE`：删除数据

OpenAPI 把 HTTP 方法称为**操作**。

我们也称之为**操作**。

#### 定义*路径操作装饰器*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` 告诉 **FastAPI** 下方函数以如下方式处理访问请求：

- 请求路径为 `/`
- 使用 <abbr title="HTTP GET 方法"><code>get</code> 操作</abbr>

!!! info "`@decorator` 说明"

    `@something` 语法是 Python **装饰器**。
    
    就像一顶放在函数上面的装饰帽（估计这个术语的命名就是这么来的）。
    
    装饰器接收下方函数，并用它执行一些操作。
    
    本例中，这个装饰器告诉 **FastAPI** 下方函数对应的**路径**是 `/` 及 `get` **操作**。
    
    这就是***路径操作装饰器***。

其它常用操作如下：

- `@app.post()`
- `@app.put()`
- `@app.delete()`

及罕见的操作：

- `@app.options()`
- `@app.head()`
- `@app.patch()`
- `@app.trace()`

!!! tip "提示"

    您可以随意使用任何操作（HTTP方法）。
    
    **FastAPI** 不向操作强制附加任何特定含义。
    
    本章中的说明仅是指导，不是要求。
    
    例如，使用 GraphQL 时，通常所有操作都只使用 `post` 一种方法。

### 第四步：定义**路径操作函数**

**路径操作函数**由以下几部分组成：

- **路径**： `/`
- **操作**： `get`
- **函数**：**装饰器**下方的函数（位于 `@app.get("/")` 下方）

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

路径操作函数就是 Python 函数。

**FastAPI** 每次接收使用 `GET` 方法访问 URL**`/`**的请求时都会调用这个函数。

本例中的路径操作函数是异步函数（`async`）。

---

也可以不使用 `async def`，把路径操作函数定义为普通函数：

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note "笔记"

    如果不清楚普通函数与异步函数的区别，请参阅[异步：***急不可待？***](https://fastapi.tiangolo.com/async/#in-a-hurry){.internal-link target=_blank}一节中的内容。

### 第五步：返回内容

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

路径操作函数可以返回**字典**、**列表**，以及**字符串**、**整数**等单值。

还可以返回 Pydantic 模型（稍后介绍）。

还有很多能自动转换为 JSON 的对象与模型（比如 ORM 等）。您可以尝试使用最喜欢的对象，FastAPI 很可能已经为其提供支持了。

## 小结

- 导入 `FastAPI`
- 创建 `app` 实例
- 编写**路径操作装饰器**（如 `@app.get("/")`）
- 编写**路径操作函数**（如 `def root(): ...`）
- 运行开发服务器（如 `uvicorn main:app --reload`）

