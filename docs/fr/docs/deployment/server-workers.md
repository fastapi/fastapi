# Workers du serveur - Uvicorn avec workers { #server-workers-uvicorn-with-workers }

Reprenons ces concepts de déploiement vus précédemment :

* Sécurité - HTTPS
* Exécution au démarrage
* Redémarrages
* **Réplication (le nombre de processus en cours d'exécution)**
* Mémoire
* Étapes préalables avant le démarrage

Jusqu'à présent, avec tous les tutoriels dans les documents, vous avez probablement exécuté un programme serveur, par exemple avec la commande `fastapi`, qui lance Uvicorn en exécutant un seul processus.

Lors du déploiement d'applications, vous voudrez probablement avoir une réplication de processus pour tirer parti de plusieurs cœurs et pouvoir gérer davantage de requêtes.

Comme vous l'avez vu dans le chapitre précédent sur les [Concepts de déploiement](concepts.md), il existe plusieurs stratégies possibles.

Ici, je vais vous montrer comment utiliser Uvicorn avec des processus workers en utilisant la commande `fastapi` ou directement la commande `uvicorn`.

/// info | Info

Si vous utilisez des conteneurs, par exemple avec Docker ou Kubernetes, je vous en dirai plus à ce sujet dans le prochain chapitre : [FastAPI dans des conteneurs - Docker](docker.md).

En particulier, lorsque vous exécutez sur **Kubernetes**, vous ne voudrez probablement **pas** utiliser de workers et plutôt exécuter **un seul processus Uvicorn par conteneur**, mais je vous en parlerai plus en détail dans ce chapitre.

///

## Utiliser plusieurs workers { #multiple-workers }

Vous pouvez démarrer plusieurs workers avec l'option de ligne de commande `--workers` :

//// tab | `fastapi`

Si vous utilisez la commande `fastapi` :

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

Si vous préférez utiliser directement la commande `uvicorn` :

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

La seule option nouvelle ici est `--workers` qui indique à Uvicorn de démarrer 4 processus workers.

Vous pouvez aussi voir qu'il affiche le **PID** de chaque processus, `27365` pour le processus parent (c'est le **gestionnaire de processus**) et un pour chaque processus worker : `27368`, `27369`, `27370` et `27367`.

## Concepts de déploiement { #deployment-concepts }

Ici, vous avez vu comment utiliser plusieurs workers pour paralléliser l'exécution de l'application, tirer parti de plusieurs cœurs du CPU et être en mesure de servir davantage de requêtes.

Dans la liste des concepts de déploiement ci-dessus, l'utilisation de workers aide principalement à la partie réplication, et un peu aux redémarrages, mais vous devez toujours vous occuper des autres :

* **Sécurité - HTTPS**
* **Exécution au démarrage**
* ***Redémarrages***
* Réplication (le nombre de processus en cours d'exécution)
* **Mémoire**
* **Étapes préalables avant le démarrage**

## Conteneurs et Docker { #containers-and-docker }

Dans le prochain chapitre sur [FastAPI dans des conteneurs - Docker](docker.md), j'expliquerai quelques stratégies que vous pourriez utiliser pour gérer les autres **concepts de déploiement**.

Je vous montrerai comment créer votre propre image à partir de zéro pour exécuter un seul processus Uvicorn. C'est un processus simple et c'est probablement ce que vous voudrez faire lorsque vous utilisez un système distribué de gestion de conteneurs comme **Kubernetes**.

## Récapitulatif { #recap }

Vous pouvez utiliser plusieurs processus workers avec l'option CLI `--workers` des commandes `fastapi` ou `uvicorn` pour tirer parti des **CPU multicœurs**, et exécuter **plusieurs processus en parallèle**.

Vous pourriez utiliser ces outils et idées si vous mettez en place votre propre système de déploiement tout en prenant vous-même en charge les autres concepts de déploiement.

Consultez le prochain chapitre pour en savoir plus sur **FastAPI** avec des conteneurs (par exemple Docker et Kubernetes). Vous verrez que ces outils offrent aussi des moyens simples de résoudre les autres **concepts de déploiement**. ✨
