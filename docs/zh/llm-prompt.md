### Target language

Translate to Simplified Chinese (简体中文).

Language code: zh.

### Writing style

Write like a developer explaining something to a colleague over lunch — clear, direct, slightly casual. The reader is a Chinese-speaking programmer, not a professor or a manager.

**Core rules:**

1. One sentence, one idea. If a sentence has "并且" or "同时" or "并...并" connecting two independent thoughts, split it.
2. Prefer short sentences (under 30 characters) over long ones.
3. Use spoken Chinese word order, not English-influenced structure.
4. Technical terms can stay in English if they're more commonly used that way (e.g. API, JSON). See terminology tiers below.
5. Don't hedge. If something is true, say it. Don't write "可能" or "或许" unless the original text genuinely expresses uncertainty.
6. Do not drop meaning-carrying words for brevity. If the original says "you can choose to", keep the sense of choice — don't simplify it to "you can".
7. Distinguish between "can" (ability) and "may" (permission/option). "you can" = 你可以 (ability); "you may" = 你也可以 / 可以 (option).
8. Stay professional but friendly. Avoid slang or overly casual terms like "小老弟". Use "小兄弟" or "姊妹项目" instead.
9. Use "其他" (not "其它") in Simplified Chinese. "其它" is an older variant that should be avoided.
10. Do not repeat conjunctions. "并...并" is incorrect — split into separate sentences or rephrase.

**Patterns to avoid (AI-style Chinese):**

| ❌ Don't write | ✅ Write instead | Why |
|---|---|---|
| 将其复制到...文件中 | 复制到...里 | "将其" is literary, not spoken |
| 该行显示了...的URL地址 | 这行告诉你...的地址 | "该" as a pronoun is stiff; "地址" already implies URL |
| 你将会看到 | 你会看到 | "将会" is news-anchor tone |
| 它并非...而只是... | 不是...只是... | "并非...而只是" is essay-style; "不是...只是..." preserves the contrast |
| 可能像下面这样 | 长这样 / 像这样 | "可能" is unnecessary hedging |
| 由于路径首先匹配，因此始终会使用第一个定义的 | 路径优先匹配，永远走第一个 | Remove "由于...因此" scaffolding |
| 通过从 str 继承，API 文档就能... | 继承 str 后，API 文档会... | "通过从...继承" is English grammar mapped to Chinese |
| 能充分利用它的功能和优点 | 功能强还好用 | Don't inflate simple ideas |
| 在使用 GET 时，...的交互式文档不会显示... | GET 请求不显示... | Remove filler ("在使用...时") |
| 这并非偶然，整个框架都是围绕这种设计构建的 | 这不是巧合，整个框架就是这么设计的 | "围绕...构建" is a translation of "built around" |
| 导入 Enum 并创建继承自...的子类 | 导入 Enum，写个继承...的子类 | "并创建" is formal; "写个" is natural |
| 在路径操作函数内部直接访问模型对象的所有属性 | 在路径操作函数里直接访问模型的所有属性 | "内部" → "里"; "对象的" is redundant |
| 基于某内部开发团队 | 基于内部团队 | "某" adds unnecessary hedging |
| 依赖和基座 | 依赖项 | "基座" is not standard terminology |
| 小老弟 | 小兄弟 / 姊妹项目 | "小老弟" is too colloquial for docs |
| 剧透警告 | 剧透预警 | "剧透" alone loses the warning tone |
| 另一个自动生成的文档 | 另一套自动文档 | "另一个" is vague; "套" is more precise |
| 另一个 API 文档 | 另一套 API 文档 | Use "套" for document sets, not "个" |
| 模型对象的所有属性 | 模型的所有属性 | "对象的" is redundant |
| 并校验并在... | 先校验，再在... | Avoid "并...并" repetition |

**More patterns to watch for:**

- ❌ "你可以在...中找到..." → ✅ "在...里" or just state it directly
- ❌ "值得注意的是" → ✅ "注意" or just make the point
- ❌ "在这种情况下" → ✅ "这时" or "这种时候"
- ❌ "从...的角度来看" → ✅ Remove; just state the fact
- ❌ "对于...而言" → ✅ Remove; restructure the sentence
- ❌ "关于...的问题" → ✅ Remove; just name the topic
- ❌ Redundant "你的" (your) — English needs "your API", Chinese often drops it when context is clear. Examples:
  - ❌ "为你的 API 生成" → ✅ "为 API 生成"
  - ❌ "定义你的 API 的 schema" → ✅ "定义 API 的模式"
  - ❌ "按你的云厂商的文档部署" → ✅ "按云厂商的文档部署"
  - ❌ "它提供你的 API 所需的一切功能" → ✅ "它提供 API 所需的一切功能"

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
- Anchor IDs (the `{#...}` part) must stay in English. Never translate them.

### Quotes and punctuation

- Keep punctuation style consistent with existing Simplified Chinese docs (they often mix English terms like "FastAPI" with Chinese text).
- Never change punctuation inside inline code, code blocks, URLs, or file paths.

### Ellipsis

- Keep ellipsis style consistent within each document, prefer `...` over `……`.
- Never change ellipsis in code, URLs, or CLI examples.

### Code blocks

- Do not translate text inside code blocks.
- Do not translate code comments inside code blocks. Keep them in English.
- Do not translate variable names, function names, or class names inside code blocks.

### Spacing (中英文排版)

Follow W3C Chinese text formatting rules:

- Add a space between Chinese and English words:
  - ✅ "使用 FastAPI 构建"
  - ❌ "使用FastAPI构建"
- No space between English and punctuation:
  - ✅ "FastAPI，Django"
  - ❌ "FastAPI ， Django"
- No space between Chinese and Chinese punctuation:
  - ✅ "中文，中文。"
  - ❌ "中文 ， 中文 。"
- Add spaces around inline code and links when next to Chinese:
  - ✅ "使用 `FastAPI` 构建"
  - ✅ "查看 [文档](https://example.com) 了解更多"
  - ❌ "使用`FastAPI`构建"

### Admonitions

- Do NOT change the admonition type during translation:
  - If the source uses `info`, keep `info`. Do not change it to `note`.
  - If the source uses `tip`, keep `tip`. Do not change it to `note`.
  - If the source uses `warning`, keep `warning`. Do not change it to `danger`.
- You may translate the title text (e.g., `info | 信息`, `tip | 提示`).
- The admonition keyword must stay in English: `note`, `tip`, `warning`, `info`, `danger`.

### HTML attributes

- Keep alt text in Simplified Chinese. Do not translate alt text to English.
  - ✅ `alt="FastAPI 微纪录片"`
  - ❌ `alt="FastAPI Mini Documentary"`
  - ✅ `alt="FastAPI 大会 '26 - 2026 年 10 月 28 日 - 荷兰阿姆斯特丹"`
  - ❌ `alt="FastAPI Conf '26 - October 28, 2026 - Amsterdam, NL"`
- Keep title attributes in Chinese when they are user-facing.
- Do not change text inside `<abbr>` or `<dfn>` tags unless it's natural Chinese.

### Terminology tiers

**Tier 1 — Always translate (术语必须翻译):**

| English | Chinese |
|---|---|
| request (HTTP) | 请求 |
| response (HTTP) | 响应 |
| path operation | 路径操作 |
| path operation function | 路径操作函数 |
| dependency injection | 依赖注入 |
| middleware | 中间件 |
| validation | 校验 |
| request body | 请求体 |
| background task | 后台任务 |
| form | 表单 |
| file | 文件 |
| schema | 模式 |
| decorator | 装饰器 |
| parameter | 参数 |
| argument | 参数（调用时传入的值） |
| return | 返回 |
| raise | 抛出 |
| import | 导入 |
| module | 模块 |
| package | 包 |
| instance | 实例 |
| attribute | 属性 |
| method | 方法 |
| function | 函数 |
| class | 类 |
| type | 类型 |
| annotation | 标注 |
| declare | 声明 |
| async | 异步 |
| serialization | 序列化 |
| marshalling | 封送 |
| alternative | 另一套 |

**Tier 2 — Keep English (保留英文，不翻译):**

Protocols and standards: API, JSON, HTTP, REST, OAuth, JWT, Swagger, OpenAPI, GET, POST, PUT, DELETE, PATCH

Tools and frameworks: Pydantic, Starlette, Uvicorn, FastAPI, Typer, Celery, Redis, RabbitMQ, Visual Studio Code, PyCharm

Acronyms: CLI, SDK, IDE, URL, URI

Keywords in code: async, await

**Tier 3 — Translate in prose, keep English in code (正文翻译，代码/参数名保留英文):**

| English | Prose | Code |
|---|---|---|
| body | 请求体 | body |
| Body (FastAPI class) | — (keep as-is) | `Body` |
| schema | 模式 | Schema |
| annotation | 标注 | annotation |
| form | 表单 | form |
| file | 文件 | file |
| endpoint | 端点 | endpoint |
| decorator | 装饰器 | decorator |

Note: When "Body" refers to FastAPI's `Body` class or decorator, keep it in English even in prose. When "body" means the concept of request body, translate to "请求体".

### Consistency rules

- Pick one translation for each term and stick with it **throughout all documents**, not just within a single document.
- Do not switch between "请求体" and "body" in the same document. Choose one:
  - Recommended: use "请求体" in prose, keep "body" only in code and parameter names.
- Do not switch between "表单" and "Forms" in the same document. Choose one.
- Do not switch between "补全" and "自动补全" in the same document. Choose one (recommended: "自动补全").
- Do not switch between "另一个" and "另一套" for the same concept across documents. Choose one (recommended: "另一套" for document sets).
