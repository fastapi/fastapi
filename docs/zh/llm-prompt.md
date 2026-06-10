### Target language

Translate to Simplified Chinese (简体中文).

Language code: zh.

### Writing style

Write like a developer explaining something to a colleague — clear, direct, slightly casual. The reader is a Chinese-speaking programmer.

**Core rules:**

1. One sentence, one idea. Split sentences connected by "并且" or "同时" into separate sentences.
2. Prefer short sentences (under 30 characters) over long ones.
3. Use spoken Chinese word order, not English-influenced structure.
4. Technical terms can stay in English if they're more commonly used that way (e.g. API, JSON). See glossary below.
5. Don't hedge. "可能" / "或许" only when the original genuinely expresses uncertainty.
6. Distinguish "can" (ability → 你可以) from "may" (option → 你也可以 / 可以).
7. Use "其他" not "其它" in Simplified Chinese.
8. When a term appears in prose, translate it per glossary. In code, keep as-is.
9. Prefer omitting "会" for deterministic behavior: "FastAPI 自动生成" not "FastAPI 会自动生成".

### Anti-patterns

| ❌ Don't | ✅ Write instead | Why |
|---|---|---|
| 将其复制到... | 复制到... | "将其" is literary, not spoken |
| 该行显示了... | 这行告诉你... | "该" is stiff |
| 你将会看到 | 你会看到 | "将会" is news-anchor tone |
| 它并非...而只是... | 不是...只是... | essay-style → spoken |
| 由于...因此... | (remove scaffolding) | 由于/因此 is redundant |
| 在编辑器中，函数内部你会在各处得到... | 编辑器里函数各处都有... | 三重冗余 |
| 通过从 str 继承 | 继承 str 后 | English grammar mapped to Chinese |
| 并创建继承...的子类 | 写个继承...的子类 | "并创建" is formal |
| 模型对象的所有属性 | 模型的所有属性 | "对象的" is redundant |
| 值得注意的是 | 注意 / (just state it) | filler |
| 在这种情况下 | 这时 / 这种时候 | filler |
| 从...的角度来看 | (remove) | filler |
| 对于...而言 | (remove) | filler |
| 包含默认值的模型属性是可选的，否则就是必选的 | 模型属性有默认值就不是必填 | 太绕 |
| 发送数据应使用以下之一 | 发数据用这些方法之一 | 太正式 |
| 例如，上述模型声明如下 JSON | 比如，上面的模型对应的 JSON | 三重正式 |

### Terminology glossary

**FastAPI 核心概念（必须统一翻译）:**

| English | Chinese | NOT |
|---|---|---|
| path operation | 路径操作 | NOT 操作路径, NOT 路由操作 |
| path operation function | 路径操作函数 | NOT 路径操作功能 |
| path operation decorator | 路径操作装饰器 | NOT 路径操作修饰器 |
| dependency injection | 依赖注入 | NOT 依赖性注入 |
| request body | 请求体 | NOT 请求正文, NOT 请求体内容 |
| response body | 响应体 | NOT 响应正文 |
| response model | 响应模型 | NOT 回应模型 |
| query parameter | 查询参数 | NOT 查询变量 |
| path parameter | 路径参数 | NOT 路径变量 |
| background task | 后台任务 | NOT 后台线程 |
| schema | 模式 | NOT 架构, NOT 方案 (in JSON Schema context) |
| handler | 处理器 | NOT 句柄 |
| exception handler | 异常处理器 | NOT 例外处理器 |
| event handler | 事件处理器 | NOT 事件处理程序 |
| lifespan | 生命周期 | NOT 寿命, NOT 存活时间 |
| lifespan event | 生命周期事件 | NOT 寿命事件 |
| startup event | 启动事件 | NOT 启动事件监听器 |
| shutdown event | 关闭事件 | NOT 关闭事件监听器 |
| middleware | 中间件 | NOT 中间层 |
| endpoint | 端点 | NOT 终结点 |
| security scheme | 安全方案 | NOT 安全模式 |
| worker process | 工作进程 | NOT 工人进程 |
| deployment | 部署 | NOT 部属 |

**Web 开发通用:**

| English | Chinese | NOT |
|---|---|---|
| request | 请求 | NOT 要求 |
| response | 响应 | NOT 回复 (in HTTP context) |
| header | 请求头 / 响应头 | NOT 标题 (in HTTP context) |
| form | 表单 | NOT 格式 |
| status code | 状态码 | NOT 状态代码 |
| validation | 校验 | NOT 验证 (when referring to data validation) |
| error response | 错误响应 | NOT 错误回复 |
| frontend | 前端 | NOT 前台 |
| backend | 后端 | NOT 后台 (when referring to backend server) |
| authentication | 认证 | NOT 验证 (when referring to auth) |
| authorization | 授权 | NOT 鉴权 |
| Bearer Token | Bearer 令牌 | NOT 承载令牌 |
| password flow | 密码流程 | NOT 密码流 |
| deprecated | 已弃用 | NOT 已过时, NOT 已废弃 |

**Python / 编程通用:**

| English | Chinese | NOT |
|---|---|---|
| class | 类 | NOT 类别 |
| function | 函数 | NOT 功能 |
| method | 方法 | NOT 方式 |
| parameter | 参数 | NOT 变量 (when referring to function params) |
| attribute | 属性 | NOT 特性 |
| module | 模块 | NOT 模组 |
| import | 导入 | NOT 引入 |
| return | 返回 | NOT 回传 |
| return type | 返回类型 | NOT 回传类型 |
| return value | 返回值 | NOT 回传值 |
| raise | 抛出 | NOT 抛掷, NOT 引发 |
| exception | 异常 | NOT 例外 |
| decorator | 装饰器 | NOT 修饰器 |
| annotation | 注解 | NOT 标注 |
| type hint | 类型提示 | NOT 类型线索 |
| type annotation | 类型注解 | NOT 类型标注 |
| instance | 实例 | NOT 例子 |
| serialization | 序列化 | NOT 串行化 |
| inheritance | 继承 | NOT 继派 |
| concurrency | 并发 | NOT 共行 |
| parallelism | 并行 | NOT 平行 |
| multiprocessing | 多进程 | NOT 多处理器 |
| template | 模板 | NOT 范本 |
| performance | 性能 | NOT 效能 |

**开发环境与工具:**

| English | Chinese | NOT |
|---|---|---|
| virtual environment | 虚拟环境 | NOT 虚拟目录 |
| environment variable | 环境变量 | NOT 环境参量 |
| command line | 命令行 | NOT 指令行 |
| editor support | 编辑器支持 | NOT 编辑器辅助 |
| code completion | 代码补全 | NOT 代码自动完成 |
| data validation | 数据校验 | NOT 数据验证 |
| data conversion | 数据转换 | NOT 数据格式转换 |
| interactive docs | 交互式文档 | NOT 互动文档 |
| automatic docs | 自动文档 | NOT 自动化文档 |
| error message | 错误信息 | NOT 错误消息 |

**保留英文（不翻译）:**

- 框架/工具: FastAPI, Pydantic, Starlette, Uvicorn, Typer, Celery, Redis
- 协议/标准: JSON, HTTP, REST, OAuth, JWT, Swagger, OpenAPI
- HTTP 方法: GET, POST, PUT, DELETE, PATCH
- 缩写: CLI, SDK, IDE, URL, URI, API, CSS, HTML
- 代码关键字: async, await
- 常见编程术语（保留英文更自然时）: framework, plugin, payload, callback, endpoint (in code)
- 安全相关（保留英文）: OAuth2, Bearer, Basic, Digest, CORS, CSRF, TLS, SSL
- FastAPI 类名（保留英文）: Depends, Query, Body, Form, File, Header, Cookie, Annotated

### Consistency rules

- Pick one translation per term and stick with it **across all documents**.
- Do not switch between "请求体" and "body" in the same document.
- Do not switch between "表单" and "Forms" in the same document.
- Do not switch between "另一个" and "另一套" for document sets (use "另一套").

### Headings

*(Supplements the general prompt's heading rules with Chinese-specific guidance.)*

- Follow existing Simplified Chinese heading style (short, descriptive).
- Do not add trailing punctuation to headings.
- If a heading contains only a FastAPI feature name, do not translate it.

### Admonitions

*(Supplements the general prompt's admonition rules with Chinese-specific titles.)*

- Do NOT change the admonition type during translation (e.g. `info` → keep `info`, not `note`).
- Chinese title mappings: `tip | 提示`, `note | 注意`, `warning | 警告`, `info | 信息`.

### Spacing (中英文排版)

- Add a space between Chinese and English words: ✅ `使用 FastAPI 构建` / ❌ `使用FastAPI构建`
- No space between English and punctuation: ✅ `FastAPI，Django`
- Add spaces around inline code next to Chinese: ✅ `使用 `FastAPI` 构建`

### Good translation examples

When in doubt, prefer the concise, spoken style over formal writing:

| English | ✅ Good Chinese | ❌ Avoid |
|---|---|---|
| The simplest FastAPI file could look like this | 最简单的 FastAPI 文件长这样 | 最简单的 FastAPI 文件可能像下面这样 |
| Copy that to a file `main.py` | 复制到 `main.py` 里 | 将其复制到 `main.py` 文件中 |
| That line shows the URL... | 这行告诉你...的地址 | 该行显示了...的URL地址 |
| model attribute has a default value, it is not required | 模型属性有默认值就不是必填 | 包含默认值的模型属性是可选的，否则就是必选的 |
| declare it the same way you declared path and query parameters | 和声明路径参数、查询参数的方式一样 | 使用与声明路径和查询参数相同的方式 |
| That's it. **2 lines**. | 大功告成。**2 行**。 | 就这样。**2 行代码**。 |
| Let's first just use the code and see how it works | 先直接运行代码看看效果 | 让我们先直接使用代码看看它是如何工作的 |
