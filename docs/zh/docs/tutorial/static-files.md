# 静态文件

使用 `StaticFiles` 可以指定文件夹自动提供静态文件服务。

## 安装 `aiofiles`

首先，安装 `aiofiles`：

<div class="termy">

```console
$ pip install aiofiles

---> 100%
```

</div>

## 使用 `StaticFiles`

* 导入 `StaticFiles`
* 在指定路径中**挂载** `StaticFiles()`

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "技术细节"

    您也可以直接使用 `from starlette.staticfiles import StaticFiles`。
    
    **FastAPI** 的 `fastapi.staticfiles` 与 `starlette.staticfiles` 相同，只是为了方便开发者调用。但实际上，`fastapi.staticfiles` 直接继承自 Starlette。

### 什么是**挂载**

**挂载**是指在路径中添加完全**独立**的应用，然后用它处理所有子路径。

与 `APIRouter` 不同，挂载的应用是完全独立的。主应用的 OpenAPI 与 API 文档不包含挂载应用中的内容。

**高级用户指南**中会介绍更多相关内容。

## 细节

第一个**`/static`**是要**挂载**的**子应用**的路径。因此，挂载子应用会处理所有以 `/static` 开头的路径。

`directory="static"` 是静态文件所在的文件夹。

`name="static"` 用于指定 **FastAPI **内部使用的名称。

这些参数都不必命名为 **`static`**，可以按需更改。

## 更多说明

更多细节与选项，详见 <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette 文档： 静态文件</a>。
