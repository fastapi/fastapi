# 模板 { #templates }

**FastAPI** 支持多种模板引擎。

Flask 等工具使用的 Jinja2 是最用的模板引擎。

在 Starlette 的支持下，**FastAPI** 应用可以直接使用工具轻易地配置 Jinja2。

## 安装依赖项 { #install-dependencies }

确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，并安装 `jinja2`：

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## 使用 `Jinja2Templates` { #using-jinja2templates }

* 导入 `Jinja2Templates`
* 创建可复用的 `templates` 对象
* 在返回模板的*路径操作*中声明 `Request` 参数
* 使用 `templates` 渲染并返回 `TemplateResponse`，传递模板的名称、request 对象以及一个包含多个键值对（用于 Jinja2 模板）的 "context" 字典。

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note

在 FastAPI 0.108.0，Starlette 0.29.0 之前，`name` 是第一个参数。
并且，在此之前，`request` 对象是作为 context 的一部分以键值对的形式传递的。

///

/// tip

通过声明 `response_class=HTMLResponse`，API 文档就能识别响应的对象是 HTML。

///

/// note | 技术细节

您还可以使用 `from starlette.templating import Jinja2Templates`。

**FastAPI** 的 `fastapi.templating` 只是为开发者提供的快捷方式。实际上，绝大多数可用响应都直接继承自 Starlette。`Request` 与 `StaticFiles` 也一样。

///

## 编写模板 { #writing-templates }

编写模板 `templates/item.html`，代码如下：

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### 模板上下文值 { #template-context-values }

在包含如下语句的html中:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...这将显示你从 "context" 字典传递的 `id`:

```Python
{"id": id}
```

例如。当 ID 为 `42` 时, 会渲染成:

```html
Item ID: 42
```

### 模板 `url_for` 参数 { #template-url-for-arguments }

你还可以在模板内使用 `url_for()`，其参数与*路径操作函数*的参数相同。

所以，该部分:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...将生成一个与处理*路径操作函数* `read_item(id=id)`的 URL 相同的链接

例如。当 ID 为 `42` 时, 会渲染成:

```html
<a href="/items/42">
```

## 模板与静态文件 { #templates-and-static-files }

你还可以在模板内部将 `url_for()` 用于静态文件，例如你挂载的 `name="static"` 的 `StaticFiles`。

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

本例中，它将链接到 `static/styles.css` 中的 CSS 文件：

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

因为使用了 `StaticFiles`，**FastAPI** 应用会自动提供位于 URL `/static/styles.css` 的 CSS 文件。

## 更多说明 { #more-details }

包括测试模板等更多详情，请参阅 <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlette 官方文档 - 模板</a>。
