# 模板

您可以在**FastAPI**使用任何您想用的模板引擎

与Flask和其他工具使用的相同，一种常见的选择是Jinja2，

有一些工具可以方便地配置它，你可以直接在你的**FastAPI**应用程序中使用（由Starlette提供）。

## 安装依赖

安装 `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## 使用 `Jinja2Templates`

* 导入 `Jinja2Templates`.
* 创建一个可以在以后重复使用的`templates`对象。
* 在 *路径操作* 中声明一个`Request`参数，该参数将返回一个模板。
* 使用你创建的`templates`来渲染并返回一个`TemplateResponse`，将`request`作为Jinja2 "context"中的一个键值对传递进去。

```Python hl_lines="4  11  15-16"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! note
    请注意，您需要将`request`作为Jinja2上下文中的键值对之一传递进去。因此，在 *路径操作* 中也需要声明它。

!!! tip
    通过声明`response_class=HTMLResponse` ，文档界面能知道响应是HTML格式的

!!! note "Technical Details"
    您还可以使用 `from starlette.templating import Jinja2Templates`。

    为了方便开发人员，**FastAPI** 提供与 `fastapi.template` 相同的 `starlette.template`。但大多数可用的回复直接来自 Starlette。`Request` 和 `StaticFiles`也是如此


## 编写模板

然后您可以在 `templates/item.html` 中编写一个模板：

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

它将会展示你从"context" `dict`中获取的`id`:

```Python
{"request": request, "id": id}
```

## 模板与静态文件

你还可以在模板中使用`url_for()`，并且可以与你挂载的`StaticFiles`一起使用。

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

在这个例子中，它将链接到一个位于`static/styles.css`的CSS文件。

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

由于您正在使用`StaticFiles`，该CSS文件将由您的**FastAPI**应用程序自动提供，URL为`/static/styles.css`。

## 更多细节

想了解更多详细信息，包括如何测试模板，请查看<a href="https://www.starlette.io/templates/" class="external-link" target="_blank">Starlette的模板文档</a>。
