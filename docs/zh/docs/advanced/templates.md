# 模板 { #templates }

你可以在 **FastAPI** 中使用任何你想用的模板引擎。

常见选择是 Jinja2，它也是 Flask 和其他工具使用的模板引擎。

有一些工具可以轻松配置它，你可以直接在 **FastAPI** 应用中使用（由 Starlette 提供）。

## 安装依赖项 { #install-dependencies }

将 `jinja2` 添加到你的项目中：

<div class="termy">

```console
$ uv add jinja2

---> 100%
```

</div>

## 使用 `Jinja2Templates` { #using-jinja2templates }

* 导入 `Jinja2Templates`。
* 创建可复用的 `templates` 对象。
* 在返回模板的*路径操作*中声明 `Request` 参数。
* 使用你创建的 `templates` 渲染并返回 `TemplateResponse`，传递模板的名称、请求对象以及一个包含多个键值对（用于 Jinja2 模板）的 "context" 字典。

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | 注意

在 FastAPI 0.108.0，Starlette 0.29.0 之前，`name` 是第一个参数。

并且，在此之前的旧版本中，`request` 对象是作为 Jinja2 的 context 中的键值对的一部分传递的。

///

/// tip | 提示

通过声明 `response_class=HTMLResponse`，文档 UI 就能知道响应会是 HTML。

///

/// note | 技术细节

你还可以使用 `from starlette.templating import Jinja2Templates`。

**FastAPI** 将同一个 `starlette.templating` 作为 `fastapi.templating` 提供，只是为了方便开发者使用。但绝大多数可用响应都直接来自 Starlette。`Request` 和 `StaticFiles` 也一样。

///

## 编写模板 { #writing-templates }

然后你可以在 `templates/item.html` 编写一个模板，例如：

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### 模板上下文值 { #template-context-values }

在包含如下语句的 HTML 中：

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...它会显示你传入的 "context" `dict` 中取得的 `id`：

```Python
{"id": id}
```

例如，当 ID 为 `42` 时，会渲染成：

```html
Item ID: 42
```

### 模板 `url_for` 参数 { #template-url-for-arguments }

你还可以在模板内使用 `url_for()`，其参数与*路径操作函数*使用的参数相同。

所以，该部分：

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...将生成一个链接，指向由*路径操作函数* `read_item(id=id)` 处理的同一个 URL。

例如，当 ID 为 `42` 时，会渲染成：

```html
<a href="/items/42">
```

## 模板与静态文件 { #templates-and-static-files }

你还可以在模板内部使用 `url_for()`，例如将它与你挂载的 `name="static"` 的 `StaticFiles` 一起使用。

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

在这个示例中，它会通过以下内容链接到 `static/styles.css` 中的 CSS 文件：

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

而且因为你使用了 `StaticFiles`，该 CSS 文件会由你的 **FastAPI** 应用在 URL `/static/styles.css` 自动提供。

## 更多说明 { #more-details }

包括如何测试模板在内的更多详情，请查看 [Starlette 的模板文档](https://starlette.dev/templates/)。
