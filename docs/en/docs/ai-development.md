# Develop with AI { #develop-with-ai }

FastAPI includes an official **agent skill**, bundled with the Python package, with guidance for the version installed in your project.

## Install the skill { #install-the-skill }

After [installing FastAPI](tutorial/index.md#install-fastapi), run [Library Skills](https://library-skills.io/use/) from your project directory:

```bash
uvx library-skills
```

Select the FastAPI skill and `.agents/skills` for Codex and most agents, or `.claude/skills` for Claude Code. You can select both.

Your agent can then use the skill automatically when working on FastAPI code.

### Install without prompts { #install-without-prompts }

For agents and scripts, select the FastAPI skill without interactive prompts:

```bash
uvx library-skills install --skill fastapi --yes
```

For Claude Code, add `--claude` to also install it in `.claude/skills`:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Configure your app { #configure-your-app }

Configure the [app entrypoint](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) in `pyproject.toml` so FastAPI tools can find your app:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Use your app's module and variable name. Here, `main:app` refers to the `app` object in `main.py`.

## Run your app { #run-your-app }

Use the [FastAPI CLI](fastapi-cli.md) for local development:

```bash
uv run fastapi dev
```

For production, use `uv run fastapi run`.

## Generate an SDK { #generate-an-sdk }

For frontend and API client development, see [Generating SDKs](advanced/generate-clients.md).

## Deploy your app { #deploy-your-app }

To deploy to [FastAPI Cloud](deployment/fastapicloud.md), the official managed deployment platform from the FastAPI team:

```bash
uv run fastapi deploy
```

You can also [deploy manually](deployment/manually.md) to another cloud provider or your own server.

## Agent plugins { #agent-plugins }

The [FastAPI Cloud plugins for Codex and Claude Code](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) include instructions to create projects and use the library skills bundled with your dependencies. They are useful even if you don't use FastAPI Cloud.

They also cover FastAPI Cloud deployment, logs, and environment variables.
