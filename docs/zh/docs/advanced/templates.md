# 模板

你可以将 **FastAPI** 和任何你喜欢的模板引擎搭配使用。

最常见的选择是 Jinja2，该引擎同样使用在了 Flask 和其它的工具上。

Starlette 提供了一些工具，使你能快速将其配置其与 **FastAPI** 一同使用。

## 安装需求

安装 `jinja2`：

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## 使用 `Jinja2Templates`

* 导入 `Jinja2Templates`
* 创建一个可重用的 `templates` 对象
* 在 *路径操作* 中添加返回一个模板的 `Request` 参数
* 使用之前创建的 `templates` 来渲染并返回一个 `TemplateResponse`，将 `request` 作为 Jinja2 "上下文" 中的一个键值对传递

```Python hl_lines="4  11  15-16"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! note
    注意，此处你将 `request` 作为上下文键值对的一部分传递给了 Jinja2。因此，你还需要在 *路径操作* 中对其进行声明。

!!! tip
    通过声明 `response_class=HTMLResponse`，文档 UI 将得知函数返回类型为 HTML。

!!! note "技术细节"
    你也可以使用 `from starlette.templating import Jinja2Templates`。

    为了你，即开发者的便利，**FastAPI** 提供了与 `fastapi.templating` 一致的 `starlette.templating`。但大多数的响应值都直接来自于 Starlette，该情况同样适用于 `Request` 和 `StaticFiles`。

## 编写模板

接下来，你可以在 `templates/item.html` 中编写一个模板：

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

它会展示你在 "上下文" `字典` 中传递的 `id` 的值：

```Python
{"request": request, "id": id}
```

## 模板与静态文件

你也可以在模板内使用 `url_for()`，并可将其与你挂载的 `StaticFiles` 等使用。

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

在该示例中，它链接到了位于 `static/styles.css` 的 CSS 文件，其中包含如下内容：

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

因为你使用了 `StaticFiles`，**FastAPI** 可以自动通过 `/static/styles.css` URL 提供对应的 CSS 文件。

## 更多细节

关于如何测试模板等的更多细节，请查阅 <a href="https://www.starlette.io/templates/" class="external-link" target="_blank">Starlette 文档的模板章节</a>。