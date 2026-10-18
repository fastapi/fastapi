# Tutoriel - Guide utilisateur { #tutorial-user-guide }


Ce tutoriel vous montre comment utiliser **FastAPI** avec la plupart de ses fonctionnalités, étape par étape.

Chaque section s'appuie progressivement sur les précédentes, mais elle est structurée de manière à séparer les sujets, afin que vous puissiez aller directement à l'un d'entre eux pour répondre à vos besoins spécifiques d'API.

Il est également conçu pour servir de référence ultérieure, afin que vous puissiez revenir voir exactement ce dont vous avez besoin.

## Exécuter le code { #run-the-code }

Tous les blocs de code peuvent être copiés et utilisés directement (il s'agit en fait de fichiers Python testés).

Pour exécuter l'un de ces exemples, copiez le code dans un fichier `main.py`, et démarrez `fastapi dev` avec `uv run` :

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Il est **FORTEMENT encouragé** que vous écriviez ou copiez le code, l'éditiez et l'exécutiez localement.

L'utiliser dans votre éditeur est ce qui vous montre vraiment les avantages de FastAPI, en voyant le peu de code que vous avez à écrire, toutes les vérifications de type, l'autocomplétion, etc.

---

## Installer FastAPI { #install-fastapi }

La première étape consiste à configurer votre projet et à ajouter FastAPI.

Installez [`uv`](https://docs.astral.sh/uv/getting-started/installation/), puis créez un projet et ajoutez FastAPI :

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` crée l'environnement virtuel du projet dans `.venv`, ajoute FastAPI à `pyproject.toml`, et crée `uv.lock` afin que les mêmes versions de packages puissent être installées plus tard.

/// details | Ce que font ces commandes

* `uv init` : crée un nouveau projet Python.
* `awesome-project` : crée le projet dans un nouveau répertoire portant ce nom.
* `--bare` : crée uniquement le fichier `pyproject.toml` minimal, sans générer d'exemple `main.py`, `README.md` ou d'autres fichiers. Vous créerez vous-même les fichiers de l'application dans les prochaines étapes de ce tutoriel.

Ensuite, `cd awesome-project` entre dans le nouveau répertoire du projet avant d'ajouter FastAPI.

`uv` utilisera une version compatible de Python déjà installée sur votre système, ou en téléchargera une si nécessaire.

Lorsque vous exécutez `uv add`, il sélectionne des versions compatibles de FastAPI et de tous les packages dont FastAPI dépend. Il enregistre les versions exactes dans `uv.lock`, ce qui permet d'installer les mêmes versions de packages plus tard sur un autre ordinateur ou lors du déploiement de l'application.

La création ou la mise à jour de ce fichier est appelée [**verrouillage** des dépendances du projet](https://docs.astral.sh/uv/concepts/projects/sync/). `uv` le fait automatiquement lorsque vous ajoutez un package.

///

/// details | Options d'installation de FastAPI

Lorsque vous installez avec `uv add "fastapi[standard]"`, cela inclut des dépendances standards optionnelles par défaut, y compris `fastapi-cloud-cli`, qui vous permet de déployer sur [FastAPI Cloud](https://fastapicloud.com).

Si vous ne souhaitez pas avoir ces dépendances optionnelles, vous pouvez à la place installer `uv add fastapi`.

Si vous souhaitez installer les dépendances standard mais sans `fastapi-cloud-cli`, vous pouvez installer avec `uv add "fastapi[standard-no-fastapi-cloud-cli]"`.

///

/// details | Utiliser `pip` à la place

Si vous préférez gérer manuellement un environnement virtuel et les packages, créez et activez un environnement virtuel, puis installez FastAPI avec `pip install "fastapi[standard]"`.

Lisez le [guide sur les environnements virtuels](https://tiangolo.com/guides/virtual-environments/) pour les étapes détaillées.

///

## Skills des agents IA { #ai-agent-skills }

FastAPI inclut une skill officielle pour les agents de codage IA. Elle est fournie avec le package, donc ses indications restent alignées avec la version de FastAPI installée dans votre projet et se mettent à jour lorsque vous mettez à niveau FastAPI.

Après avoir installé FastAPI dans votre projet, vous pouvez installer la skill avec <a href="https://library-skills.io">Library Skills</a> :

```bash
uvx library-skills
```

/// note | Remarque

`uvx` est un alias pour `uv tool run`. Il exécute Library Skills dans un environnement temporaire et isolé pendant que Library Skills analyse les packages installés dans votre projet.

///

La skill est compatible avec Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode, et la plupart des autres agents de codage. Pour Claude Code, sélectionnez `.claude/skills` lorsqu'il vous est demandé où installer la skill.

## Guide d'utilisation avancé { #advanced-user-guide }

Il existe également un **Guide d'utilisation avancé** que vous pouvez lire plus tard après ce **Tutoriel - Guide d'utilisation**.

Le **Guide d'utilisation avancé**, qui s'appuie sur cette base, utilise les mêmes concepts et vous apprend quelques fonctionnalités supplémentaires.

Mais vous devez d'abord lire le **Tutoriel - Guide d'utilisation** (ce que vous êtes en train de lire en ce moment).

Il est conçu pour que vous puissiez construire une application complète avec seulement le **Tutoriel - Guide d'utilisation**, puis l'étendre de différentes manières, en fonction de vos besoins, en utilisant certaines des idées supplémentaires du **Guide d'utilisation avancé**.
