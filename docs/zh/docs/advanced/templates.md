# 模板

**FastAPI** 支持多种模板引擎。

Flask 等工具使用的 Jinja2 是最用的模板引擎。

在 Starlette 的支持下，**FastAPI** 应用可以直接使用工具轻易地配置 Jinja2。

## 安装依赖项

安装 `jinja2`：

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

如需使用静态文件，还要安装 `aiofiles`：

<div class="termy">

```console
$ pip install aiofiles

---> 100%
```

</div>

## 使用 `Jinja2Templates`

* 导入 `Jinja2Templates`
* 创建可复用的 `templates` 对象
* 在返回模板的*路径操作*中声明 `Request` 参数
* 使用 `templates` 渲染并返回 `TemplateResponse`， 以键值对方式在 Jinja2 的 **context** 中传递 `request`

```Python hl_lines="4  11  15-16"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! note "笔记"

    注意，必须为 Jinja2 以键值对方式在上下文中传递 `request`。因此，还要在*路径操作*中声明。

!!! tip "提示"

    通过声明 `response_class=HTMLResponse`，API 文档就能识别响应的对象是 HTML。

!!! note "技术细节"

    您还可以使用 `from starlette.templating import Jinja2Templates`。

    **FastAPI** 的 `fastapi.templating` 只是为开发者提供的快捷方式。实际上，绝大多数可用响应都直接继承自 Starlette。 `Request` 与 `StaticFiles` 也一样。

## 编写模板

编写模板 `templates/item.html`，代码如下：

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

它会显示从 **context** 字典中提取的 `id`：

```Python
{"request": request, "id": id}
```

## 模板与静态文件

在模板内部使用 `url_for()`，例如，与挂载的 `StaticFiles` 一起使用。

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

本例中，使用 `url_for()` 为模板添加 CSS 文件 `static/styles.css` 链接：

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

因为使用了 `StaticFiles`， **FastAPI** 应用自动提供位于 URL `/static/styles.css`

的 CSS 文件。

## 更多说明

包括测试模板等更多详情，请参阅 <a href="https://www.starlette.io/templates/" class="external-link" target="_blank">Starlette 官档 - 模板</a>。
