# 模板 { #templates }

你可以在 **FastAPI** 中使用任何你想要的模板引擎。

一个常见的选择是 Jinja2，它也是 Flask 和其他工具使用的那个。

有一些工具可以让你轻松配置它，你可以在 **FastAPI** 应用中直接使用（由 Starlette 提供）。

## 安装依赖项 { #install-dependencies }

请确保你创建一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}，激活它，然后安装 `jinja2`：

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## 使用 `Jinja2Templates` { #using-jinja2templates }

* 导入 `Jinja2Templates`。
* 创建一个之后可以复用的 `templates` 对象。
* 在会返回模板的*路径操作*中声明一个 `Request` 参数。
* 使用你创建的 `templates` 渲染并返回 `TemplateResponse`，传入模板名称、request 对象，以及一个包含键值对的 "context" 字典，用于在 Jinja2 模板内部使用。

{* ../../docs_src/templates/tutorial001_py39.py hl[4,11,15:18] *}

/// note | 注意

在 FastAPI 0.108.0、Starlette 0.29.0 之前，`name` 是第一个参数。

并且，在之前的版本中，`request` 对象是作为 Jinja2 的 context 中键值对的一部分传递的。

///

/// tip | 提示

通过声明 `response_class=HTMLResponse`，文档 UI 就能知道响应将会是 HTML。

///

/// note | Technical Details

你也可以使用 `from starlette.templating import Jinja2Templates`。

**FastAPI** 提供的 `fastapi.templating` 与 `starlette.templating` 相同，只是为了方便你（开发者）使用。但大多数可用的响应都直接来自 Starlette。`Request` 和 `StaticFiles` 也是一样。

///

## 编写模板 { #writing-templates }

然后你可以编写一个模板，例如放在 `templates/item.html`：

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### 模板上下文值 { #template-context-values }

在包含如下内容的 HTML 中：

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...它会显示你传入的 "context" `dict` 中的 `id`：

```Python
{"id": id}
```

例如，当 ID 为 `42` 时，会渲染为：

```html
Item ID: 42
```

### 模板 `url_for` 参数 { #template-url-for-arguments }

你也可以在模板内部使用 `url_for()`，它接受的参数与*路径操作函数*使用的参数相同。

所以，包含以下内容的部分：

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...将生成一个指向同一 URL 的链接，该 URL 会由*路径操作函数* `read_item(id=id)` 处理。

例如，当 ID 为 `42` 时，会渲染为：

```html
<a href="/items/42">
```

## 模板与静态文件 { #templates-and-static-files }

你也可以在模板内部使用 `url_for()`，例如把它用于你以 `name="static"` 挂载的 `StaticFiles`。

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

在这个例子中，它会链接到 `static/styles.css` 这个 CSS 文件：

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

并且因为你使用了 `StaticFiles`，你的 **FastAPI** 应用会在 URL `/static/styles.css` 自动提供该 CSS 文件。

## 更多细节 { #more-details }

更多细节（包括如何测试模板），请查看 <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">Starlette 的模板文档</a>。
