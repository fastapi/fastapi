# 使用 AI 開發 { #develop-with-ai }

FastAPI 在 Python 套件中隨附官方的 **AI 代理技能（agent skill）**，提供適用於你專案中所安裝版本的指引。

## 安裝技能 { #install-the-skill }

[安裝 FastAPI](tutorial/index.md#install-fastapi) 後，在你的專案目錄中執行 [Library Skills](https://library-skills.io/use/)：

```bash
uvx library-skills
```

選取 FastAPI 技能，並為 Codex 和大多數代理選擇 `.agents/skills`，或為 Claude Code 選擇 `.claude/skills`。你也可以兩者都選。

之後，你的代理在處理 FastAPI 程式碼時，就能自動使用這項技能。

### 不透過互動提示安裝 { #install-without-prompts }

供代理和腳本使用時，可以不透過互動提示直接選取 FastAPI 技能：

```bash
uvx library-skills install --skill fastapi --yes
```

若使用 Claude Code，加入 `--claude`，也將技能安裝到 `.claude/skills`：

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## 設定你的應用程式 { #configure-your-app }

在 `pyproject.toml` 中設定[應用程式進入點](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml)，讓 FastAPI 工具能找到你的應用程式：

```toml
[tool.fastapi]
entrypoint = "main:app"
```

請使用你的應用程式的模組和變數名稱。這裡的 `main:app` 指的是 `main.py` 中的 `app` 物件。

## 執行你的應用程式 { #run-your-app }

在本機開發時，使用 [FastAPI CLI](fastapi-cli.md)：

```bash
uv run fastapi dev
```

在正式環境中，使用 `uv run fastapi run`。

## 產生 SDK { #generate-an-sdk }

關於前端和 API 用戶端開發，請參閱[產生 SDK](advanced/generate-clients.md)。

## 部署你的應用程式 { #deploy-your-app }

若要部署到 FastAPI 團隊提供的官方代管部署平台 [FastAPI Cloud](deployment/fastapicloud.md)：

```bash
uv run fastapi deploy
```

你也可以[手動部署](deployment/manually.md)到其他雲端供應商的平台或自己的伺服器。

## 代理外掛 { #agent-plugins }

[適用於 Codex 和 Claude Code 的 FastAPI Cloud 外掛](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/)包含建立專案，以及使用相依套件隨附的程式庫技能的指引。即使你不使用 FastAPI Cloud，這些外掛也很有用。

它們也涵蓋 FastAPI Cloud 部署、日誌和環境變數。
