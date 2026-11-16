# Mit KI entwickeln { #develop-with-ai }

FastAPI enthält einen offiziellen **Agent-Skill**, der mit dem Python-Paket ausgeliefert wird und Anleitungen für die in Ihrem Projekt installierte Version bietet.

## Den Skill installieren { #install-the-skill }

Führen Sie nach der [Installation von FastAPI](tutorial/index.md#install-fastapi) [Library Skills](https://library-skills.io/use/) in Ihrem Projektverzeichnis aus:

```bash
uvx library-skills
```

Wählen Sie den FastAPI-Skill und `.agents/skills` für Codex und die meisten Agenten oder `.claude/skills` für Claude Code aus. Sie können beide auswählen.

Ihr Agent kann den Skill dann automatisch verwenden, wenn er an FastAPI-Code arbeitet.

### Ohne Rückfragen installieren { #install-without-prompts }

Wählen Sie für Agenten und Skripte den FastAPI-Skill ohne interaktive Rückfragen aus:

```bash
uvx library-skills install --skill fastapi --yes
```

Fügen Sie für Claude Code `--claude` hinzu, um ihn auch in `.claude/skills` zu installieren:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Ihre Anwendung konfigurieren { #configure-your-app }

Konfigurieren Sie den [Einstiegspunkt der Anwendung](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) in `pyproject.toml`, damit FastAPI-Tools Ihre Anwendung finden können:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Verwenden Sie den Modul- und Variablennamen Ihrer Anwendung. Hier verweist `main:app` auf das Objekt `app` in `main.py`.

## Ihre Anwendung ausführen { #run-your-app }

Verwenden Sie das [FastAPI CLI](fastapi-cli.md) für die lokale Entwicklung:

```bash
uv run fastapi dev
```

Verwenden Sie für den Produktivbetrieb `uv run fastapi run`.

## Ein SDK generieren { #generate-an-sdk }

Informationen zur Entwicklung von Frontends und API-Clients finden Sie unter [SDKs generieren](advanced/generate-clients.md).

## Ihre Anwendung deployen { #deploy-your-app }

Um auf [FastAPI Cloud](deployment/fastapicloud.md), der offiziellen verwalteten Deployment-Plattform des FastAPI-Teams, zu deployen:

```bash
uv run fastapi deploy
```

Sie können auch bei einem anderen Cloudanbieter oder auf Ihrem eigenen Server [manuell deployen](deployment/manually.md).

## Agent-Plugins { #agent-plugins }

Die [FastAPI Cloud-Plugins für Codex und Claude Code](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) enthalten Anleitungen zum Erstellen von Projekten und zur Verwendung der Library Skills, die mit Ihren Abhängigkeiten ausgeliefert werden. Sie sind auch dann nützlich, wenn Sie FastAPI Cloud nicht verwenden.

Sie behandeln außerdem das Deployment auf FastAPI Cloud, Logs und Umgebungsvariablen.
