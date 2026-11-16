# Desenvolva com IA { #develop-with-ai }

O FastAPI inclui uma **skill de agente** oficial, distribuída com o pacote Python, com orientações para a versão instalada no seu projeto.

## Instale a skill { #install-the-skill }

Após [instalar o FastAPI](tutorial/index.md#install-fastapi), execute [Library Skills](https://library-skills.io/use/) a partir do diretório do seu projeto:

```bash
uvx library-skills
```

Selecione a skill do FastAPI e `.agents/skills` para o Codex e a maioria dos agentes, ou `.claude/skills` para o Claude Code. Você pode selecionar ambos.

Seu agente poderá então usar a skill automaticamente ao trabalhar com código FastAPI.

### Instale sem prompts { #install-without-prompts }

Para agentes e scripts, selecione a skill do FastAPI sem prompts interativos:

```bash
uvx library-skills install --skill fastapi --yes
```

Para o Claude Code, adicione `--claude` para instalá-la também em `.claude/skills`:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Configure sua aplicação { #configure-your-app }

Configure o [ponto de entrada da aplicação](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) no `pyproject.toml` para que as ferramentas do FastAPI possam encontrar sua aplicação:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Use o módulo e o nome da variável da sua aplicação. Aqui, `main:app` refere-se ao objeto `app` em `main.py`.

## Execute sua aplicação { #run-your-app }

Use a [CLI do FastAPI](fastapi-cli.md) para desenvolvimento local:

```bash
uv run fastapi dev
```

Para produção, use `uv run fastapi run`.

## Gere um SDK { #generate-an-sdk }

Para desenvolvimento de frontend e clientes de API, consulte [Geração de SDKs](advanced/generate-clients.md).

## Implante sua aplicação { #deploy-your-app }

Para implantar no [FastAPI Cloud](deployment/fastapicloud.md), a plataforma oficial de implantação gerenciada da equipe do FastAPI:

```bash
uv run fastapi deploy
```

Você também pode [implantar manualmente](deployment/manually.md) em outro provedor de nuvem ou no seu próprio servidor.

## Plugins de agentes { #agent-plugins }

Os [plugins do FastAPI Cloud para Codex e Claude Code](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) incluem instruções para criar projetos e usar as skills de bibliotecas distribuídas com suas dependências. Eles são úteis mesmo que você não use o FastAPI Cloud.

Também abordam implantação no FastAPI Cloud, logs e variáveis de ambiente.
