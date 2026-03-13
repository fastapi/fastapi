# 静态文件 { #static-files }

你可以使用 `StaticFiles` 从目录中自动提供静态文件。

## 使用 `StaticFiles` { #use-staticfiles }

* 导入 `StaticFiles`。
* 将一个 `StaticFiles()` 实例“挂载”（Mount）到指定路径。

{* ../../docs_src/static_files/tutorial001_py310.py hl[2,6] *}

/// note | 技术细节

你也可以用 `from starlette.staticfiles import StaticFiles`。

**FastAPI** 提供了和 `starlette.staticfiles` 相同的 `fastapi.staticfiles`，只是为了方便你这个开发者。但它确实直接来自 Starlette。

///

### 什么是“挂载”（Mounting） { #what-is-mounting }

“挂载”表示在特定路径添加一个完全“独立”的应用，然后负责处理所有子路径。

这与使用 `APIRouter` 不同，因为挂载的应用是完全独立的。主应用的 OpenAPI 和文档不会包含已挂载应用的任何内容，等等。

你可以在[高级用户指南](../advanced/index.md){.internal-link target=_blank}中了解更多。

## 细节 { #details }

第一个 `"/static"` 指的是这个“子应用”将被“挂载”到的子路径。因此，任何以 `"/static"` 开头的路径都会由它处理。

`directory="static"` 指的是包含你的静态文件的目录名称。

`name="static"` 为它提供了一个可被 **FastAPI** 内部使用的名称。

这些参数都可以不是“`static`”，请根据你的应用需求和具体细节进行调整。

## 更多信息 { #more-info }

更多细节和选项请查阅 <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Starlette 的静态文件文档</a>。
