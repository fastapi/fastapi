# 第一步

下述代码是最简单的 FastAPI 文件：

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

把代码复制到 `main.py`。

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

    `uvicorn main:app` 命令含义如下：
    
    * `main`：`main.py` 是 Python「模块」
    * `app`：`main.py`  中用 `app = FastAPI()` 创建的对象
    * `--reload`：代码更新后，重启服务器。仅在开发时使用

输出内容包含如下信息：

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

显示了应用在本机提供服务的 URL 地址。

### 查看

打开浏览器访问 <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>。

可以看到如下 JSON 响应：

```JSON
{"message": "Hello World"}
```

### API 交互文档

跳转到 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>。

可以看到（ <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">由 Swagger UI</a> ）自动生成的 API 交互文档：

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 备选 API 文档

转到 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>。

这是（由 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> ）自动生成的备选文档 ：

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** 使用 **OpenAPI** 把所有 API 转换成「概图」。

#### 「概图」

「概图」是对事物的定义或描述，不是实现真正的功能，只是抽象的描述。

#### API「概图」

此处，OpenAPI 是定义 API 概图的规范。

OpenAPI 定义的概图包括 API 路径及使用的参数等对象。

#### 数据「概图」

「概图」这一术语也表示 JSON 等数据的结构。

此处，表示 JSON 属性及数据类型等。

#### OpenAPI 和 JSON Schema

OpenAPI 用于定义 API 概图。在该概图中，API 发送和接收的数据是由 JSON 数据概图标准（**JSON Schema**）定义的 。

#### 查看 `openapi.json`

如需查看原始 OpenAPI 概图，FastAPI 可以自动生成描述所有 API 的 JSON 对象。

直接输入：<a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a> 即可查看。

显示的 JSON 以如下内容开头：

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

#### OpenAPI 的用途

OpenAPI 概图负责驱动 FastAPI 内置的两个交互文档。

基于 OpenAPI 替代方案还有很多。您可以轻易地向 **FastAPI** 应用添加任意替代方案。

甚至还可以用 OpenAPI 自动生成与 API 通信的客户端代码。例如，前端、移动端、物联网应用等。

## 分步小结

### 第一步：导入 `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` 是为 API 提供所有功能的 Python 类。

!!! note "技术细节"

    `FastAPI` 是直接从 `Starlette` 继承的类。
    
    通过 `FastAPI` 可以使用 Starlette 的所有功能。

### 第二步：创建 `FastAPI`「实例」

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

这里的变量 `app` 是 `FastAPI` 的类「实例」。

该实例是创建所有 API 的主要交互对象。

在下面的命令中， `uvicorn` 也要引用这个 `app`：

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

如果以下述方式创建应用：

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

把代码存入 `main.py`，要以如下方式运行 `uvicorn`：

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### 第三步：创建*路径操作*

#### 路径

这里的「路径」是指 URL 中第一个 `/` 之后的内容。

因此，在下面的 URL 中：

```
https://example.com/items/foo
```

…… 其路径是：

```
/items/foo
```

!!! info "说明"

    「路径」通常也称为「端点」或「路由」。

开发 API 时，「路径」是分离「关注点」和「资源」的主要手段。

#### 操作

这里的「操作」是指 HTTP「方法」。

下面是常用的 HTTP 方法：

- `POST`
- `GET`
- `PUT`
- `DELETE`

…… 还有以下几种罕见的方法：

- `OPTIONS`
- `HEAD`
- `PATCH`
- `TRACE`

在 HTTP 协议中，可以使用以上任意一种或多种「方法」与路径通信。

---

开发 API 时，通常使用特定的 HTTP 方法执行特定的操作。

通常使用：

- `POST`：创建数据
- `GET`：读取数据
- `PUT`：更新数据
- `DELETE`：删除数据

因此，OpenAPI 把 HTTP 方法称为「操作」。

我们也称之为「操作」。

#### 定义*路径操作装饰器*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` 告诉 **FastAPI** 在它下方的函数负责处理如下访问请求：

- 请求路径为 `/`
- 使用 <abbr title="HTTP GET 方法"><code>get</code> 操作</abbr>

!!! info "`@decorator` 说明"

    `@something` 语法是 Python「装饰器」。
    
    就像一顶放在函数上面的装饰帽（估计这个术语的命名就是这么来的）。
    
    装饰器接收下方函数，并用它执行一些操作。
    
    本例中，这个装饰器告诉 **FastAPI** 下方函数对应的**路径**是 `/` 及 `get` **操作**。
    
    这就是「**路径操作装饰器**」。

还可以使用其他操作：

- `@app.post()`
- `@app.put()`
- `@app.delete()`

及罕见的：

- `@app.options()`
- `@app.head()`
- `@app.patch()`
- `@app.trace()`

!!! tip "提示"

    您可以随意使用任意操作（HTTP方法）。
    
    **FastAPI** 不为操作强制附加任何特定含义。
    
    本章中的说明仅是指导，不是要求。
    
    例如，使用 GraphQL 时，通常所有操作都用 `post` 一种方法执行。

### 第四步：定义**路径操作函数**

这就是「**路径操作函数**」：

- **路径**： `/`
- **操作**： `get`
- **函数**：「装饰器」下方的函数（位于 `@app.get("/")` 下方）

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

路径操作函数其实就是 Python 函数。

**FastAPI** 每次接收使用 `GET` 方法访问 URL「`/`」的请求时，都会调用这个函数。

本例中，它是 `async` 函数。

---

也可以不使用 `async def`，把路径操作函数定义为常规函数：

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note "笔记"

    如果不清楚常规函数与异步函数的区别，请参阅[异步：*「着急了？」*](https://fastapi.tiangolo.com/async/#in-a-hurry){.internal-link target=_blank}。

### 第五步：返回内容

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

返回的内容可以是 `dict`、`list`、 `str`、`int` 等单值。

也可以是 Pydantic 模型（稍后介绍）。

甚至可以是 ORM 对象等能自动转换为 JSON 的对象或模型。试着使用您最喜欢的对象，FastAPI 很有可能已经为其提供支持了。

## 小结

- 导入 `FastAPI`
- 创建 `app` 实例
- 编写**路径操作装饰器**（如，`@app.get("/")`）
- 编写**路径操作函数**（如，`def root(): ...`）
- 运行开发服务器（如，`uvicorn main:app --reload`）
