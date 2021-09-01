# 特性

## FastAPI 特性

**FastAPI** 提供了以下内容：

### 基于开放标准

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> 用于创建 API，包括声明<abbr title="亦称为: endpoints, routes">路径</abbr><abbr title="也叫做HTTP方法, 例如 POST, GET, PUT, DELETE">操作</abbr>、参数、请求体、安全等
* 使用 <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> 的自动数据模型文档，（OpenAPI 就是基于 JSON Schema）
* 基于标准设计，历经缜密的研究，并非狗尾续貂
* 支持在多种语言中自动**生成客户端代码**

### 自动文档

API 文档和探索性 Web 用户界面。FastAPI 基于 OpenAPI，支持多种备选文档方案，目前默认自带 2 个 API 文档。

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>，可在浏览器中实现交互式探索，直接调用和测试 API

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 备选 API 文档：<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 现代 Python

借助 Pydantic，FastAPI 的功能全部基于标准的 **Python 3.6 类型**声明。无需学习新语法，只需要标准的现代 Python 。

就算不使用 FastAPI，最好也花几分钟学习一下 Python 类型，详见：[Python 类型](python-types.md){.internal-link target=\_blank}。

使用类型的标准 Python：

```Python
from types import List, Dict
from datetime import date

from pydantic import BaseModel


# 把变量声明为字符串
# 在函数内部获得编辑器支持
def main(user_id: str):
    return user_id


# Pydantic 模型
class User(BaseModel):
    id: int
    name: str
    joined: date
```

用法如下：

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info "说明"

    `**second_user_data` 是指：
    
    直接把 `second_user_data` 字典的键值作为关键字参数传递，等效于：`User(id=4, name="Mary", joined="2018-11-30")`

### 编辑器支持

FastAPI 设计的易用且直观，为了确保最佳的开发体验，所有设计方案在开发前就在多个编辑器上进行了测试。

最新的 Python 开发者调查报告显示<a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">使用最多的功能是**自动补全**</a>。

**FastAPI** 就是基于这一点，处处都有自动补全。

开发者几乎不需要翻阅文档。

编辑器会提供各种帮助：

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>：

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>：

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

即便在之前不敢想象的位置，也实现了代码自动补全。例如，自动补全 JSON 请求体（可能是嵌套的）中的键 `price`。

再也不会输错键名，也不用来回翻阅文档，更不用上下求索，确认最后使用的是 `username` 还是 `user_name`。

### 简洁

所有对象都有合理的**默认值**，处处都有可选配置。所有参数都可以微调，以满足您的需求，开发出理想的 API。

但默认的前提是，一切都能**正常运转**。

### 验证

* 验证绝大部分（所有？） Python **数据类型**，包括：
    * JSON 对象（`dict`）
    * JSON 数组（`list`），支持定义成员类型
    * 字符串（`str`）字段，支持定义最小或最大长度
    * 数字（`int`, `float`），支持定义最大值和最小值

* 校验外部类型， 比如：
    * URL
    * Email
    * UUID
    * 等……

所有的验证都由完善且稳定的 **Pydantic** 处理。

### 安全与身份验证

集成了安全和身份验证，杜绝数据库或数据模型的渗透风险。

OpenAPI 中定义的安全概图，包括：

* HTTP 基本验证
* **OAuth2**（使用 **JWT 令牌**）。详见 [OAuth2 与 JWT 令牌验证](tutorial/security/oauth2-jwt.md){.internal-link target=\_blank}
* 以下几种对象中的 API 密钥：
    * 请求头
    * 查询参数
    * Cookies 等

此外，还有 Starlette（包括 **session cookie**）的所有安全功能。

所有的工具和组件都可以复用，并能轻易地与您的系统、数据仓库、关系型数据库、 NoSQL 数据库集成。

### 依赖注入

FastAPI <abbr title='也叫作"组件"、"资源"、"服务"、"提供方"'><strong>依赖注入</strong></abbr>系统非常简单，但却十分强大。

* 支持子依赖项的依赖项，可创建多层依赖项或**图依赖项**
* FastAPI 会**自动处理**所有操作
* 所有依赖项都可以从请求获取数据，并且**增加了路径操作**约束和 API 文档
* 依赖项中定义的*路径操作*参数也可以**自动验证**
* 支持复杂的用户身份验证系统，**数据库连接**等
* **不依赖**数据库、前端，但是和它们集成很简单

### 无限的插件

其实，FastAPI 并不需要插件，可以直接导入和使用所需的代码。

依赖项可以把任意支持库轻易地整合进 FastAPI 应用，使用与*路径操作*相同的架构和语法，只要两行代码就可以为应用创建任意**插件**。

### 测试

* 100% <abbr title="自动测试的代码量">测试覆盖</abbr>
* 代码库 100% <abbr title="Python类型注解，有助于让编辑器和外部工具提供更好的支持">类型注释</abbr>
* 用于生产应用

## Starlette 特性

**FastAPI** 完全兼容并基于 <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>。所以，Starlette 代码能在 FastAPI 应用中正常运行。`FastAPI` 实际上是 `Starlette` 的子类。只要了解 Starlette，就可以使用它的绝大部分功能。

**FastAPI** 拥有 **Starlette** 的所有功能，可以说，它是 Starlette 的加强版：

* 令人惊叹的性能。<a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">Python 最快的框架之一，堪比 **NodeJS** 和 **Go**</a>
* **支持 WebSocket**
* **支持 GraphQL**
* 后台任务处理
* Startup 和 Shutdown 事件
* 基于 `requests` 测试客户端
* **CORS**、GZip、静态文件、流响应
* 支持 **Session 和 Cookie**
* 100% 测试覆盖率
* 代码库 100% 类型注释

## Pydantic 特性

**FastAPI** 完全兼容并基于 <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>。所以，Pydantic 代码能在 FastAPI 应用中正常运行。

FastAPI 还支持基于 Pydantic 的外部库，例如，数据库的 <abbr title="对象关系映射">ORM</abbr>、<abbr title="对象文档映射">ODM</abbr>。

也就是说，很多情况下，可以把从请求中获得的对象**直接传到数据库**，因为所有的验证都是自动的。

反之，也可以把从数据库中获取的对象**直接传到客户端**。

**FastAPI** 支持 **Pydantic** 的所有功能（基于 Pydantic 实现数据处理）：

* **不烧脑**：
    * 无需学习新的概图定义微语言
    * 只要了解 Python 类型，就能使用 Pydantic
* 适配 **<abbr title="集成开发环境，和编辑器类似">IDE</abbr>/<abbr title="检查代码错误的程序">linter</abbr>/brain**：
    * 因为 Pydantic 数据结构只是定义的类实例；自动补全、linting、mypy 都可以和验证数据一起正常运作，完全符合直觉
* **更快**：
    * 在<a href="https://pydantic-docs.helpmanual.io/#benchmarks-tag" class="external-link" target="_blank">基准测试</a>中，Pydantic 比其它参与测试的其它库都快
* 验证**复杂结构**：
    * 使用层级式 Pydantic 模型，Python `typing`的 `List` 和 `Dict` 等
    * 验证器可以清晰、简单地定义、校验复杂数据概图，并存档为 JSON Schema
    * 深度**嵌套 JSON** 对象，并可进行验证和注释
* **可扩展**：
    * Pydantic 支持自定义数据类型，使用验证装饰器扩展对模型的验证方法
* 100% 测试覆盖率
