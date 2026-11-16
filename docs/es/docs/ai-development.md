# Desarrolla con IA { #develop-with-ai }

FastAPI incluye una **skill de agente** oficial, distribuida con el paquete de Python, con orientación para la versión instalada en tu proyecto.

## Instala la skill { #install-the-skill }

Después de [instalar FastAPI](tutorial/index.md#install-fastapi), ejecuta [Library Skills](https://library-skills.io/use/) desde el directorio de tu proyecto:

```bash
uvx library-skills
```

Selecciona la skill de FastAPI y `.agents/skills` para Codex y la mayoría de los agentes, o `.claude/skills` para Claude Code. Puedes seleccionar ambos.

Tu agente podrá entonces usar la skill automáticamente al trabajar en código de FastAPI.

### Instala sin preguntas interactivas { #install-without-prompts }

Para agentes y scripts, selecciona la skill de FastAPI sin preguntas interactivas:

```bash
uvx library-skills install --skill fastapi --yes
```

Para Claude Code, añade `--claude` para instalarla también en `.claude/skills`:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Configura tu aplicación { #configure-your-app }

Configura el [punto de entrada de la aplicación](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) en `pyproject.toml` para que las herramientas de FastAPI puedan encontrar tu aplicación:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Usa el módulo y el nombre de la variable de tu aplicación. Aquí, `main:app` hace referencia al objeto `app` en `main.py`.

## Ejecuta tu aplicación { #run-your-app }

Usa la [CLI de FastAPI](fastapi-cli.md) para el desarrollo local:

```bash
uv run fastapi dev
```

Para producción, usa `uv run fastapi run`.

## Genera un SDK { #generate-an-sdk }

Para el desarrollo de frontend y clientes de API, consulta [Generación de SDKs](advanced/generate-clients.md).

## Despliega tu aplicación { #deploy-your-app }

Para desplegar en [FastAPI Cloud](deployment/fastapicloud.md), la plataforma oficial de despliegue gestionado del equipo de FastAPI:

```bash
uv run fastapi deploy
```

También puedes [desplegar manualmente](deployment/manually.md) en otro proveedor de la nube o en tu propio servidor.

## Plugins para agentes { #agent-plugins }

Los [plugins de FastAPI Cloud para Codex y Claude Code](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) incluyen instrucciones para crear proyectos y usar las skills de paquetes distribuidas con tus dependencias. Son útiles incluso si no usas FastAPI Cloud.

También cubren el despliegue en FastAPI Cloud, los logs y las variables de entorno.
