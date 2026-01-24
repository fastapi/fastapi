# Tutoriel - Guide utilisateur { #tutorial-user-guide }

Ce tutoriel vous montre comment utiliser **FastAPI** avec la plupart de ses fonctionnalités, étape par étape.

Chaque section s'appuie progressivement sur les précédentes, mais elle est structurée de manière à séparer les sujets, afin que vous puissiez aller directement à l'un d'entre eux pour résoudre vos besoins spécifiques en matière d'API.

Il est également conçu pour fonctionner comme une référence future afin que vous puissiez revenir et voir exactement ce dont vous avez besoin.

## Exécuter le code { #run-the-code }

Tous les blocs de code peuvent être copiés et utilisés directement (il s'agit en fait de fichiers Python testés).

Pour exécuter l'un de ces exemples, copiez le code dans un fichier `main.py`, et démarrez `fastapi dev` avec :

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

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

Il est **FORTEMENT encouragé** que vous écriviez ou copiiez le code, l'éditiez et l'exécutiez localement.

L'utiliser dans votre éditeur est ce qui vous montre vraiment les avantages de FastAPI, en voyant le peu de code que vous avez à écrire, toutes les vérifications de type, l'autocomplétion, etc.

---

## Installer FastAPI { #install-fastapi }

La première étape consiste à installer FastAPI.

Vous devez vous assurer de créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis **d'installer FastAPI** :

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | Remarque

Lorsque vous installez avec `pip install "fastapi[standard]"`, cela inclut certaines dépendances standard optionnelles par défaut, notamment `fastapi-cloud-cli`, qui vous permet de déployer sur <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>.

Si vous ne voulez pas avoir ces dépendances optionnelles, vous pouvez installer `pip install fastapi` à la place.

Si vous voulez installer les dépendances standard mais sans le `fastapi-cloud-cli`, vous pouvez installer avec `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

///

## Guide utilisateur avancé { #advanced-user-guide }

Il existe également un **Guide utilisateur avancé** que vous pouvez lire plus tard après ce **Tutoriel - Guide utilisateur**.

Le **Guide utilisateur avancé** s'appuie sur celui-ci, utilise les mêmes concepts et vous apprend quelques fonctionnalités supplémentaires.

Mais vous devez d'abord lire le **Tutoriel - Guide utilisateur** (ce que vous êtes en train de lire en ce moment).

Il est conçu pour que vous puissiez construire une application complète avec seulement le **Tutoriel - Guide utilisateur**, puis l'étendre de différentes manières, en fonction de vos besoins, en utilisant certaines des idées supplémentaires du **Guide utilisateur avancé**.
