# LLM 测试文件 { #llm-test-file }

本文用于测试用于翻译文档的 <abbr title="Large Language Model - 大型语言模型">LLM</abbr> 是否理解 `scripts/translate.py` 中的 `general_prompt` 以及 `docs/{language code}/llm-prompt.md` 中的语言特定提示。语言特定提示会追加到 `general_prompt` 之后。

这里添加的测试会被所有语言特定提示的设计者看到。

用法如下：

* 准备语言特定提示——`docs/{language code}/llm-prompt.md`。
* 将本文重新翻译为你的目标语言（例如使用 `translate.py` 的 `translate-page` 命令）。这会在 `docs/{language code}/docs/_llm-test.md` 下创建翻译。
* 检查翻译是否正确。
* 如有需要，改进你的语言特定提示、通用提示，或英文文档。
* 然后手动修正翻译中剩余的问题，确保这是一个优秀的译文。
* 重新翻译，在已有的优秀译文基础上进行。理想情况是 LLM 不再对译文做任何更改。这意味着通用提示和你的语言特定提示已经尽可能完善（有时它仍会做一些看似随机的改动，原因是<a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLM 不是确定性算法</a>）。

测试如下：

## 代码片段 { #code-snippets }

//// tab | 测试

这是一个代码片段：`foo`。这是另一个代码片段：`bar`。还有一个：`baz quux`。

////

//// tab | 信息

代码片段的内容应保持不变。

参见 `scripts/translate.py` 中通用提示的 `### Content of code snippets` 部分。

////

## 引号 { #quotes }

//// tab | 测试

昨天，我的朋友写道："如果你把 incorrectly 拼对了，你就把它拼错了"。我回答："没错，但 'incorrectly' 错的不是 '"incorrectly"'"。

/// note | 注意

LLM 很可能会把这段翻错。我们只关心在重新翻译时它是否能保持修正后的译文。

///

////

//// tab | 信息

提示词设计者可以选择是否将中性引号转换为排版引号。也可以保持不变。

例如参见 `docs/de/llm-prompt.md` 中的 `### Quotes` 部分。

////

## 代码片段中的引号 { #quotes-in-code-snippets }

//// tab | 测试

`pip install "foo[bar]"`

代码片段中的字符串字面量示例：`"this"`，`'that'`。

一个较难的字符串字面量示例：`f"I like {'oranges' if orange else "apples"}"`

硬核：`Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | 信息

... 但是，代码片段内的引号必须保持不变。

////

## 代码块 { #code-blocks }

//// tab | 测试

一个 Bash 代码示例...

```bash
# 向宇宙打印问候
echo "Hello universe"
```

...以及一个控制台代码示例...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...以及另一个控制台代码示例...

```console
// 创建目录 "code"
$ mkdir code
// 切换到该目录
$ cd code
```

...以及一个 Python 代码示例...

```Python
wont_work()  # 这不会起作用 😱
works(foo="bar")  # 这可行 🎉
```

...就这些。

////

//// tab | 信息

代码块中的代码不应被修改，注释除外。

参见 `scripts/translate.py` 中通用提示的 `### Content of code blocks` 部分。

////

## 选项卡与彩色提示框 { #tabs-and-colored-boxes }

//// tab | 测试

/// info | 信息
Some text
///

/// note | 注意
Some text
///

/// note | 技术细节
Some text
///

/// check | 检查
Some text
///

/// tip | 提示
Some text
///

/// warning | 警告
Some text
///

/// danger | 危险
Some text
///

////

//// tab | 信息

选项卡以及 `Info`/`Note`/`Warning`/等提示块，应在竖线（`|`）后添加其标题的翻译。

参见 `scripts/translate.py` 中通用提示的 `### Special blocks` 与 `### Tab blocks` 部分。

////

## Web 与内部链接 { #web-and-internal-links }

//// tab | 测试

链接文本应被翻译，链接地址应保持不变：

* [链接到上面的标题](#code-snippets)
* [内部链接](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">外部链接</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">样式链接</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">脚本链接</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">图片链接</a>

链接文本应被翻译，且链接地址应指向对应的译文页面：

* <a href="https://fastapi.tiangolo.com/zh/" class="external-link" target="_blank">FastAPI 链接</a>

////

//// tab | 信息

链接的文本应被翻译，但地址保持不变。唯一的例外是指向 FastAPI 文档页面的绝对链接，此时应指向对应语言的译文。

参见 `scripts/translate.py` 中通用提示的 `### Links` 部分。

////

## HTML "abbr" 元素 { #html-abbr-elements }

//// tab | 测试

这里有一些包裹在 HTML "abbr" 元素中的内容（有些是虚构的）：

### abbr 提供了完整短语 { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - 尽管去做">GTD</abbr>
* <abbr title="less than - 小于"><code>lt</code></abbr>
* <abbr title="XML Web Token - XML Web 令牌">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - 并行服务器网关接口">PSGI</abbr>

### abbr 提供了完整短语与解释 { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mozilla 开发者网络: 为开发者编写的文档，由 Firefox 团队撰写">MDN</abbr>
* <abbr title="Input/Output - 输入/输出: 磁盘读写，网络通信。">I/O</abbr>.

////

//// tab | 信息

"abbr" 元素的 "title" 属性需要按照特定规则进行翻译。

译文可以自行添加 "abbr" 元素以解释英语单词，LLM 不应删除这些元素。

参见 `scripts/translate.py` 中通用提示的 `### HTML abbr elements` 部分。

////

## HTML "dfn" 元素 { #html-dfn-elements }

* <dfn title="配置为以某种方式连接并协同工作的机器组">集群</dfn>
* <dfn title="一种使用具有多个隐藏层的人工神经网络的机器学习方法，从输入层到输出层构建了完整的内部结构">深度学习</dfn>

## 标题 { #headings }

//// tab | 测试

### 开发 Web 应用——教程 { #develop-a-webapp-a-tutorial }

Hello.

### 类型提示与注解 { #type-hints-and-annotations }

Hello again.

### 超类与子类 { #super-and-subclasses }

Hello again.

////

//// tab | 信息

关于标题的唯一硬性规则是：LLM 必须保持花括号内的哈希部分不变，以确保链接不会失效。

参见 `scripts/translate.py` 中通用提示的 `### Headings` 部分。

语言特定的说明可参见例如 `docs/de/llm-prompt.md` 中的 `### Headings` 部分。

////

## 文档中使用的术语 { #terms-used-in-the-docs }

//// tab | 测试

* you
* your

* e.g.
* etc.

* `foo` as an `int`
* `bar` as a `str`
* `baz` as a `list`

* the Tutorial - User guide
* the Advanced User Guide
* the SQLModel docs
* the API docs
* the automatic docs

* Data Science
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic authentication
* HTTP Digest
* ISO format
* the JSON Schema standard
* the JSON schema
* the schema definition
* Password Flow
* Mobile

* deprecated
* designed
* invalid
* on the fly
* standard
* default
* case-sensitive
* case-insensitive

* to serve the application
* to serve the page

* the app
* the application

* the request
* the response
* the error response

* the path operation
* the path operation decorator
* the path operation function

* the body
* the request body
* the response body
* the JSON body
* the form body
* the file body
* the function body

* the parameter
* the body parameter
* the path parameter
* the query parameter
* the cookie parameter
* the header parameter
* the form parameter
* the function parameter

* the event
* the startup event
* the startup of the server
* the shutdown event
* the lifespan event

* the handler
* the event handler
* the exception handler
* to handle

* the model
* the Pydantic model
* the data model
* the database model
* the form model
* the model object

* the class
* the base class
* the parent class
* the subclass
* the child class
* the sibling class
* the class method

* the header
* the headers
* the authorization header
* the `Authorization` header
* the forwarded header

* the dependency injection system
* the dependency
* the dependable
* the dependant

* I/O bound
* CPU bound
* concurrency
* parallelism
* multiprocessing

* the env var
* the environment variable
* the `PATH`
* the `PATH` variable

* the authentication
* the authentication provider
* the authorization
* the authorization form
* the authorization provider
* the user authenticates
* the system authenticates the user

* the CLI
* the command line interface

* the server
* the client

* the cloud provider
* the cloud service

* the development
* the development stages

* the dict
* the dictionary
* the enumeration
* the enum
* the enum member

* the encoder
* the decoder
* to encode
* to decode

* the exception
* to raise

* the expression
* the statement

* the frontend
* the backend

* the GitHub discussion
* the GitHub issue

* the performance
* the performance optimization

* the return type
* the return value

* the security
* the security scheme

* the task
* the background task
* the task function

* the template
* the template engine

* the type annotation
* the type hint

* the server worker
* the Uvicorn worker
* the Gunicorn Worker
* the worker process
* the worker class
* the workload

* the deployment
* to deploy

* the SDK
* the software development kit

* the `APIRouter`
* the `requirements.txt`
* the Bearer Token
* the breaking change
* the bug
* the button
* the callable
* the code
* the commit
* the context manager
* the coroutine
* the database session
* the disk
* the domain
* the engine
* the fake X
* the HTTP GET method
* the item
* the library
* the lifespan
* the lock
* the middleware
* the mobile application
* the module
* the mounting
* the network
* the origin
* the override
* the payload
* the processor
* the property
* the proxy
* the pull request
* the query
* the RAM
* the remote machine
* the status code
* the string
* the tag
* the web framework
* the wildcard
* to return
* to validate

////

//// tab | 信息

这是一份不完整且非规范性的（主要是）技术术语清单，取自文档中常见的词汇。它可能有助于提示词设计者判断哪些术语需要对 LLM 提供额外指引。例如当它总是把一个好的译法改回次优译法，或在你的语言中对某个术语的词形变化有困难时。

参见例如 `docs/de/llm-prompt.md` 中的 `### List of English terms and their preferred German translations` 部分。

////

////

翻译（术语）对照：

//// tab | 测试（译文）

* 你
* 你的

* 例如
* 等等

* 将 `foo` 作为 `int`
* 将 `bar` 作为 `str`
* 将 `baz` 作为 `list`

* 教程 - 用户指南
* 高级用户指南
* SQLModel 文档
* API 文档
* 自动文档

* 数据科学
* 深度学习
* 机器学习
* 依赖注入
* HTTP 基本认证
* HTTP 摘要认证
* ISO 格式
* JSON Schema 标准
* JSON 模式
* 模式定义
* 密码流
* 移动端

* 已弃用
* 设计的
* 无效
* 即时
* 标准的
* 默认的
* 区分大小写
* 不区分大小写

* 为应用提供服务
* 为页面提供服务

* 应用
* 应用程序

* 请求
* 响应
* 错误响应

* 路径操作
* 路径操作装饰器
* 路径操作函数

* 主体
* 请求体
* 响应体
* JSON 体
* 表单体
* 文件体
* 函数体

* 参数
* 请求体参数
* 路径参数
* 查询参数
* Cookie 参数
* Header 参数
* 表单参数
* 函数参数

* 事件
* 启动事件
* 服务器的启动
* 关闭事件
* 生命周期事件

* 处理器
* 事件处理器
* 异常处理器
* 处理

* 模型
* Pydantic 模型
* 数据模型
* 数据库模型
* 表单模型
* 模型对象

* 类
* 基类
* 父类
* 子类
* 子类
* 兄弟类
* 类方法

* 请求头
* 请求头
* 授权头
* `Authorization` 头
* 转发头

* 依赖注入系统
* 依赖
* 可依赖对象
* 依赖项

* I/O 受限
* CPU 受限
* 并发
* 并行
* 多进程

* 环境变量
* 环境变量
* `PATH`
* `PATH` 变量

* 认证
* 认证提供方
* 授权
* 授权表单
* 授权提供方
* 用户进行认证
* 系统对用户进行认证

* CLI
* 命令行界面

* 服务器
* 客户端

* 云服务提供商
* 云服务

* 开发
* 开发阶段

* dict
* 字典
* 枚举
* 枚举
* 枚举成员

* 编码器
* 解码器
* 编码
* 解码

* 异常
* 抛出

* 表达式
* 语句

* 前端
* 后端

* GitHub 讨论
* GitHub Issue

* 性能
* 性能优化

* 返回类型
* 返回值

* 安全
* 安全方案

* 任务
* 后台任务
* 任务函数

* 模板
* 模板引擎

* 类型注解
* 类型提示

* 服务器 worker
* Uvicorn worker
* Gunicorn worker
* worker 进程
* worker 类
* 工作负载

* 部署
* 部署

* SDK
* 软件开发工具包

* `APIRouter`
* `requirements.txt`
* Bearer Token
* 破坏性变更
* Bug
* 按钮
* 可调用对象
* 代码
* 提交
* 上下文管理器
* 协程
* 数据库会话
* 磁盘
* 域名
* 引擎
* 假 X
* HTTP GET 方法
* 项
* 库
* 生命周期
* 锁
* 中间件
* 移动应用
* 模块
* 挂载
* 网络
* 源
* 覆盖
* 负载
* 处理器
* 属性
* 代理
* Pull Request
* 查询
* RAM
* 远程机器
* 状态码
* 字符串
* 标签
* Web 框架
* 通配符
* 返回
* 校验

////

//// tab | 信息（译文）

此清单是不完整且非规范性的，列出（主要是）文档中出现的技术术语。它有助于提示词设计者确定哪些术语需要额外的指引。例如当 LLM 总是把更好的译法改回次优译法，或在你的语言中难以正确变形时。

也可参见 `docs/de/llm-prompt.md` 中的 `### List of English terms and their preferred German translations` 部分。

////
