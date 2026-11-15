# Développer avec l'IA { #develop-with-ai }

FastAPI inclut une **compétence d'agent (skill)** officielle, fournie avec le paquet Python, qui contient des recommandations pour la version installée dans votre projet.

## Installer la compétence { #install-the-skill }

Après avoir [installé FastAPI](tutorial/index.md#install-fastapi), exécutez [Library Skills](https://library-skills.io/use/) depuis le répertoire de votre projet :

```bash
uvx library-skills
```

Sélectionnez la compétence FastAPI et `.agents/skills` pour Codex et la plupart des agents, ou `.claude/skills` pour Claude Code. Vous pouvez sélectionner les deux.

Votre agent peut alors utiliser automatiquement la compétence lorsqu'il travaille sur du code FastAPI.

### Installer sans invites { #install-without-prompts }

Pour les agents et les scripts, sélectionnez la compétence FastAPI sans invites interactives :

```bash
uvx library-skills install --skill fastapi --yes
```

Pour Claude Code, ajoutez `--claude` pour l'installer également dans `.claude/skills` :

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Configurer votre application { #configure-your-app }

Configurez le [point d'entrée de l'application](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) dans `pyproject.toml` pour que les outils FastAPI puissent trouver votre application :

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Utilisez le nom du module et de la variable de votre application. Ici, `main:app` fait référence à l'objet `app` dans `main.py`.

## Exécuter votre application { #run-your-app }

Utilisez la [CLI FastAPI](fastapi-cli.md) pour le développement local :

```bash
uv run fastapi dev
```

En production, utilisez `uv run fastapi run`.

## Générer un SDK { #generate-an-sdk }

Pour le développement frontend et de clients d'API, consultez [Générer des SDK](advanced/generate-clients.md).

## Déployer votre application { #deploy-your-app }

Pour déployer sur [FastAPI Cloud](deployment/fastapicloud.md), la plateforme officielle de déploiement gérée par l'équipe FastAPI :

```bash
uv run fastapi deploy
```

Vous pouvez également [déployer manuellement](deployment/manually.md) chez un autre fournisseur cloud ou sur votre propre serveur.

## Plug-ins pour agents { #agent-plugins }

Les [plug-ins FastAPI Cloud pour Codex et Claude Code](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) incluent des instructions pour créer des projets et utiliser les compétences de bibliothèque fournies avec vos dépendances. Ils sont utiles même si vous n'utilisez pas FastAPI Cloud.

Ils couvrent également le déploiement sur FastAPI Cloud, les journaux et les variables d'environnement.
