# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - interface en ligne de commande">CLI</abbr>** est un programme en ligne de commande que vous pouvez utiliser pour servir votre application FastAPI, gérer votre projet FastAPI, et plus encore.

Lorsque vous installez FastAPI (par exemple avec `pip install "fastapi[standard]"`), il est fourni avec un programme en ligne de commande que vous pouvez exécuter dans le terminal.

Pour exécuter votre application FastAPI en développement, vous pouvez utiliser la commande `fastapi dev` :

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | Astuce

Pour la production, utilisez `fastapi run` plutôt que `fastapi dev`. 🚀

///

En interne, **FastAPI CLI** utilise [Uvicorn](https://www.uvicorn.dev), un serveur ASGI haute performance, prêt pour la production. 😎

La CLI `fastapi` tentera de détecter automatiquement l’application FastAPI à exécuter, en supposant qu’il s’agit d’un objet nommé `app` dans un fichier `main.py` (ou quelques autres variantes).

Mais vous pouvez configurer explicitement l’application à utiliser.

## Configurer le `entrypoint` de l’application dans `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

Vous pouvez configurer l’endroit où se trouve votre application dans un fichier `pyproject.toml` comme suit :

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Cet `entrypoint` indiquera à la commande `fastapi` qu’elle doit importer l’application comme ceci :

```python
from main import app
```

Si votre code était structuré comme ceci :

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

Vous définiriez alors le `entrypoint` comme suit :

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

ce qui serait équivalent à :

```python
from backend.main import app
```

### `fastapi dev` avec un chemin { #fastapi-dev-with-path }

Vous pouvez également passer le chemin du fichier à la commande `fastapi dev`, et elle devinera l’objet d’application FastAPI à utiliser :

```console
$ fastapi dev main.py
```

Mais vous devez vous rappeler de passer le bon chemin à chaque fois que vous appelez la commande `fastapi`.

De plus, d’autres outils pourraient ne pas pouvoir le trouver, par exemple l’[extension VS Code](editor-support.md) ou [FastAPI Cloud](https://fastapicloud.com), il est donc recommandé d’utiliser le `entrypoint` dans `pyproject.toml`.

## `fastapi dev` { #fastapi-dev }

L’exécution de `fastapi dev` lance le mode développement.

Par défaut, l’**auto-reload** est activé et recharge automatiquement le serveur lorsque vous modifiez votre code. Cela consomme des ressources et peut être moins stable que lorsqu’il est désactivé. Vous devez l’utiliser uniquement pour le développement. Il écoute aussi sur l’adresse IP `127.0.0.1`, qui est l’adresse IP permettant à votre machine de communiquer uniquement avec elle‑même (`localhost`).

## `fastapi run` { #fastapi-run }

Exécuter `fastapi run` démarre FastAPI en mode production par défaut.

Par défaut, l’**auto-reload** est désactivé. Il écoute aussi sur l’adresse IP `0.0.0.0`, ce qui signifie toutes les adresses IP disponibles ; de cette manière, il sera accessible publiquement à toute personne pouvant communiquer avec la machine. C’est ainsi que vous l’exécutez normalement en production, par exemple dans un conteneur.

Dans la plupart des cas, vous avez (et devez avoir) un « termination proxy » au‑dessus qui gère le HTTPS pour vous ; cela dépend de la façon dont vous déployez votre application : votre fournisseur peut le faire pour vous, ou vous devrez le configurer vous‑même.

/// tip | Astuce

Vous pouvez en savoir plus à ce sujet dans la [documentation de déploiement](deployment/index.md).

///
