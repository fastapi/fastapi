# 静态文件

您可以使用 `StaticFiles`从目录中自动提供静态文件。

## 使用`StaticFiles`

* 导入`StaticFiles`。
* "挂载"(Mount) 一个 `StaticFiles()` 实例到一个指定路径。

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "技术细节"
    你也可以用 `from starlette.staticfiles import StaticFiles`。

    **FastAPI** 提供了和 `starlette.staticfiles` 相同的 `fastapi.staticfiles` ，只是为了方便你，开发者。但它确实来自Starlette。

### 什么是"挂载"(Mounting)

"挂载" 表示在特定路径添加一个完全"独立的"应用，然后负责处理所有子路径。

这与使用`APIRouter`不同，因为安装的应用程序是完全独立的。OpenAPI和来自你主应用的文档不会包含已挂载应用的任何东西等等。

你可以在**高级用户指南**中了解更多。

## 细节

这个 "子应用" 会被 "挂载" 到第一个 `"/static"` 指向的子路径。因此，任何以`"/static"`开头的路径都会被它处理。

 `directory="static"` 指向包含你的静态文件的目录名字。

`name="static"` 提供了一个能被**FastAPI**内部使用的名字。

所有这些参数可以不同于"`static`"，根据你应用的需要和具体细节调整它们。

## 更多信息

更多细节和选择查阅 <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette's docs about Static Files</a>.
