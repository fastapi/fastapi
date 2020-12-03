# 静态文件

你可以通过使用 `StaticFiles` 从一个目录中自动提供静态文件。

## 安装 `aiofiles`

首先需要安装 `aiofiles`:

<div class="termy">

```console
$ pip install aiofiles

---> 100%
```

</div>

## 使用 `StaticFiles`

* 导入 `StaticFiles`.
* 在特定路径中 "挂载" StaticFiles()实例。

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "技术细节"
    你也可以使用 `from starlette.staticfiles import StaticFiles`.

    **FastAPI** 提供和 `starlette.staticfiles` 相同的 `fastapi.staticfiles`，只是为了方便开发人员。但它实际上直接来自于 Starlette。

### 什么是 "挂载"

"挂载" 意味着在特定路径中添加一个完整的 "独立的" 应用程序，然后由它来处理所有的子路径。

这不同于使用 `APIRouter` 作为一个挂载的应用程序是完全独立的。主应用程序的 OpenAPI 和文档不会包含挂载的应用程序中的任何内容，等。

你可以在 **高级用户指南** 中了解更多。

## 细节

第一个 `"/static"` 指的是将 "挂载" 此 "子应用程序" 的子路径。因此，任何以 `"/static"` 开头的路径都将由它处理。

`directory="static"` 是指包含静态文件的目录的名称。

`name="static"` 给了它一个可以被 **FastAPI** 内部使用的名称。

所有这些参数都可以不同于 "`static`" ，根据您自己的应用程序的需要和具体细节来调整它们。

## 更多信息

更多细节和选项请检查<a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette 关于静态文件的文档</a>。
