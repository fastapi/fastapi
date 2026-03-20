# 编辑器支持 { #editor-support }

官方的 [FastAPI 扩展](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode)为你的 FastAPI 开发流程带来增强，包括*路径操作*的发现与导航、部署到 FastAPI Cloud，以及实时日志流式传输。

有关该扩展的更多详情，请参阅其 [GitHub 仓库](https://github.com/fastapi/fastapi-vscode)中的 README。

## 安装与配置 { #setup-and-installation }

**FastAPI 扩展**同时适用于 [VS Code](https://code.visualstudio.com/) 和 [Cursor](https://www.cursor.com/)。你可以在各编辑器的扩展面板中直接搜索 “FastAPI”，并选择由 **FastAPI Labs** 发布的扩展进行安装。该扩展也适用于基于浏览器的编辑器，例如 [vscode.dev](https://vscode.dev) 和 [github.dev](https://github.dev)。

### 应用发现 { #application-discovery }

默认情况下，扩展会通过扫描实例化了 `FastAPI()` 的文件，自动发现工作区中的 FastAPI 应用。如果你的项目结构无法自动检测，你可以通过 `pyproject.toml` 中的 `[tool.fastapi]` 或 VS Code 设置项 `fastapi.entryPoint` 来指定入口点，使用模块表示法（例如 `myapp.main:app`）。

## 功能 { #features }

- **Path Operation 资源管理器** - 侧边栏树状视图展示应用中的所有 <dfn title="路由，端点">*路径操作*</dfn>。点击可跳转至任一路由或 APIRouter 的定义。
- **路由搜索** - 使用 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>（macOS 上为 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>）按路径、方法或名称进行搜索。
- **CodeLens 导航** - 测试客户端调用（例如 `client.get('/items')`）上方的可点击链接，可跳转到匹配的*路径操作*，在测试与实现之间快速往返。
- **部署到 FastAPI Cloud** - 一键将你的应用部署到 [FastAPI Cloud](https://fastapicloud.com/)。
- **应用日志流式传输** - 从部署在 FastAPI Cloud 的应用中实时流式获取日志，并支持按级别过滤与文本搜索。

如果你想先熟悉扩展功能，可以打开命令面板（<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>，macOS 上为 <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>），选择 “Welcome: Open walkthrough...”，然后选择 “Get started with FastAPI” 演练。
