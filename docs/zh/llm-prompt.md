### Target language

Translate to Simplified Chinese (简体中文).

Language code: zh.

### Writing style

Write like a developer explaining something to a colleague over lunch — clear, direct, slightly casual. The reader is a Chinese-speaking programmer, not a professor or a manager.

**Core rules:**

1. One sentence, one idea. If a sentence has "并且" or "同时" connecting two independent thoughts, split it.
2. Prefer short sentences (under 30 characters) over long ones.
3. Use spoken Chinese word order, not English-influenced structure.
4. Technical terms can stay in English if they're more commonly used that way (e.g. API, JSON, decorator, endpoint).
5. Don't hedge. If something is true, say it. Don't write "可能" or "或许" unless the original text genuinely expresses uncertainty.

**Patterns to avoid (AI-style Chinese):**

| ❌ Don't write | ✅ Write instead | Why |
|---|---|---|
| 将其复制到...文件中 | 复制到...里 | "将其" is literary, not spoken |
| 该行显示了...的URL地址 | 这行告诉你...的地址 | "该" as a pronoun is stiff; "地址" already implies URL |
| 你将会看到 | 你会看到 | "将会" is news-anchor tone |
| 它并非...而只是... | 不是...就是... | "并非...而只是" is essay-style |
| 可能像下面这样 | 长这样 / 像这样 | "可能" is unnecessary hedging |
| 由于路径首先匹配，因此始终会使用第一个定义的 | 路径优先匹配，永远走第一个 | Remove "由于...因此" scaffolding |
| 通过从 str 继承，API 文档就能... | 继承 str 后，API 文档会... | "通过从...继承" is English grammar mapped to Chinese |
| 能充分利用它的功能和优点 | 功能强还好用 | Don't inflate simple ideas |
| 在使用 GET 时，...的交互式文档不会显示... | GET 请求不显示... | Remove filler ("在使用...时") |
| 这并非偶然，整个框架都是围绕这种设计构建的 | 这不是巧合，整个框架就是这么设计的 | "围绕...构建" is a translation of "built around" |
| 导入 Enum 并创建继承自...的子类 | 导入 Enum，写个继承...的子类 | "并创建" is formal; "写个" is natural |
| 在路径操作函数内部直接访问模型对象的所有属性 | 在路径操作函数里直接访问模型的所有属性 | "内部" → "里"; "对象的" is redundant |

**More patterns to watch for:**

- ❌ "你可以在...中找到..." → ✅ "在...里" or just state it directly
- ❌ "值得注意的是" → ✅ "注意" or just make the point
- ❌ "在这种情况下" → ✅ "这时" or "这种时候"
- ❌ "从...的角度来看" → ✅ Remove; just state the fact
- ❌ "对于...而言" → ✅ Remove; restructure the sentence
- ❌ "关于...的问题" → ✅ Remove; just name the topic
- ❌ Redundant "你的" (your) — English needs "your API", Chinese often drops it when context is clear

**Reference style:**

Think of how these write technical Chinese:
- Vue.js Chinese docs (vuejs.org/zh) — clean, direct, developer-friendly
- 阮一峰's blog — conversational but precise
- Go by Example Chinese (gobyexample-cn.github.io) — minimal, no fluff

### Grammar and tone

- Use "你" (not "您") to address the reader.
- Keep the tone helpful but not condescending. Don't over-explain things that are obvious to a developer.
- If the original English uses "you can..." or "you will see...", consider whether the Chinese version even needs the subject. Often you can drop "你" and just state the action.

### Headings

- Follow existing Simplified Chinese heading style (short and descriptive).
- Do not add trailing punctuation to headings.
- If a heading contains only the name of a FastAPI feature, do not translate it.

### Quotes and punctuation

- Keep punctuation style consistent with existing Simplified Chinese docs (they often mix English terms like "FastAPI" with Chinese text).
- Never change punctuation inside inline code, code blocks, URLs, or file paths.

### Ellipsis

- Keep ellipsis style consistent within each document, prefer `...` over `……`.
- Never change ellipsis in code, URLs, or CLI examples.

### Preferred translations / glossary

Use the following preferred translations when they apply in documentation prose:

- request (HTTP): 请求
- response (HTTP): 响应
- path operation: 路径操作
- path operation function: 路径操作函数
- dependency injection: 依赖注入
- middleware: 中间件
- schema: 模式
- validation: 校验
- endpoint: 端点
- decorator: 装饰器
- parameter: 参数
- argument: 参数（调用时传入的值）
- return: 返回
- raise: 抛出
- import: 导入
- module: 模块
- package: 包
- instance: 实例
- attribute: 属性
- method: 方法
- function: 函数
- class: 类
- type: 类型
- annotation: 标注
- declare: 声明
- async: 异步

### `///` admonitions

- Keep the admonition keyword in English (do not translate `note`, `tip`, etc.).
- If a title is present, prefer these canonical titles:

- `/// tip | 提示`
- `/// note | 注意`
- `/// warning | 警告`
- `/// info | 信息`
- `/// danger | 危险`
