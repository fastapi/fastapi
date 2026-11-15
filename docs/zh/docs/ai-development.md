# 使用 AI 开发 { #develop-with-ai }

FastAPI 的 Python 包内附带官方的 **智能体技能（agent skill）**，为你的项目中安装的版本提供指导。

## 安装技能 { #install-the-skill }

[安装 FastAPI](tutorial/index.md#install-fastapi) 后，在项目目录中运行 [Library Skills](https://library-skills.io/use/)：

```bash
uvx library-skills
```

选择 FastAPI 技能，并为 Codex 和大多数智能体选择 `.agents/skills`，或为 Claude Code 选择 `.claude/skills`。你也可以同时选择两者。

之后，你的智能体在处理 FastAPI 代码时就能自动使用该技能。

### 非交互式安装 { #install-without-prompts }

对于智能体和脚本，可以使用以下命令，无需交互式提示即可选择 FastAPI 技能：

```bash
uvx library-skills install --skill fastapi --yes
```

对于 Claude Code，添加 `--claude`，将技能同时安装到 `.claude/skills`：

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## 配置应用 { #configure-your-app }

在 `pyproject.toml` 中配置[应用入口点](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml)，以便 FastAPI 工具找到你的应用：

```toml
[tool.fastapi]
entrypoint = "main:app"
```

请使用你的应用的模块名和变量名。这里，`main:app` 指的是 `main.py` 中的 `app` 对象。

## 运行应用 { #run-your-app }

使用 [FastAPI CLI](fastapi-cli.md) 进行本地开发：

```bash
uv run fastapi dev
```

在生产环境中，使用 `uv run fastapi run`。

## 生成 SDK { #generate-an-sdk }

有关前端和 API 客户端开发，请参阅[生成 SDK](advanced/generate-clients.md)。

## 部署应用 { #deploy-your-app }

要部署到 FastAPI 团队提供的官方托管部署平台 [FastAPI Cloud](deployment/fastapicloud.md)，请运行：

```bash
uv run fastapi deploy
```

你也可以[手动部署](deployment/manually.md)到其他云服务提供商或你自己的服务器。

## 智能体插件 { #agent-plugins }

[适用于 Codex 和 Claude Code 的 FastAPI Cloud 插件](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/)包含创建项目以及使用依赖项附带的库技能的指导。即使你不使用 FastAPI Cloud，这些插件也很有用。

它们还涵盖 FastAPI Cloud 部署、日志和环境变量。
