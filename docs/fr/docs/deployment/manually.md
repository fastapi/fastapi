# Exécuter un serveur manuellement { #run-a-server-manually }

## Utiliser la commande `fastapi run` { #use-the-fastapi-run-command }

En bref, utilisez `fastapi run` pour servir votre application FastAPI :

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

Cela fonctionnerait pour la plupart des cas. 😎

Vous pourriez utiliser cette commande par exemple pour démarrer votre application **FastAPI** dans un conteneur, sur un serveur, etc.

## Serveurs ASGI { #asgi-servers }

Allons un peu plus en détail.

FastAPI utilise un standard pour construire des frameworks web Python et des serveurs appelé <abbr title="Asynchronous Server Gateway Interface - Interface passerelle serveur asynchrone">ASGI</abbr>. FastAPI est un framework web ASGI.

La principale chose dont vous avez besoin pour exécuter une application **FastAPI** (ou toute autre application ASGI) sur une machine serveur distante est un programme serveur ASGI comme **Uvicorn**, c'est celui utilisé par défaut par la commande `fastapi`.

Il existe plusieurs alternatives, notamment :

* [Uvicorn](https://www.uvicorn.dev/) : un serveur ASGI haute performance.
* [Hypercorn](https://hypercorn.readthedocs.io/) : un serveur ASGI compatible avec HTTP/2 et Trio entre autres fonctionnalités.
* [Daphne](https://github.com/django/daphne) : le serveur ASGI conçu pour Django Channels.
* [Granian](https://github.com/emmett-framework/granian) : un serveur HTTP Rust pour les applications Python.
* [NGINX Unit](https://unit.nginx.org/howto/fastapi/) : NGINX Unit est un environnement d'exécution d'applications web léger et polyvalent.

## Machine serveur et programme serveur { #server-machine-and-server-program }

Il y a un petit détail sur les noms à garder à l'esprit. 💡

Le mot « serveur » est couramment utilisé pour désigner à la fois l'ordinateur distant/cloud (la machine physique ou virtuelle) et également le programme qui s'exécute sur cette machine (par exemple, Uvicorn).

Gardez cela à l'esprit lorsque vous lisez « serveur » en général, cela pourrait faire référence à l'une de ces deux choses.

Lorsqu'on se réfère à la machine distante, il est courant de l'appeler **serveur**, mais aussi **machine**, **VM** (machine virtuelle), **nœud**. Tout cela fait référence à un type de machine distante, exécutant normalement Linux, sur laquelle vous exécutez des programmes.

## Installer le programme serveur { #install-the-server-program }

Lorsque vous installez FastAPI, il est fourni avec un serveur de production, Uvicorn, et vous pouvez le démarrer avec la commande `fastapi run`.

Mais vous pouvez également installer un serveur ASGI manuellement.

Vous devez créer un [environnement virtuel](../virtual-environments.md), l'activer, puis vous pouvez installer l'application serveur.

Par exemple, pour installer Uvicorn :

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

Un processus similaire s'appliquerait à tout autre programme de serveur ASGI.

/// tip | Astuce

En ajoutant `standard`, Uvicorn va installer et utiliser quelques dépendances supplémentaires recommandées.

Cela inclut `uvloop`, le remplaçant hautes performances de `asyncio`, qui fournit le gros gain de performance en matière de concurrence.

Lorsque vous installez FastAPI avec quelque chose comme `pip install "fastapi[standard]"`, vous obtenez déjà `uvicorn[standard]` aussi.

///

## Exécuter le programme serveur { #run-the-server-program }

Si vous avez installé un serveur ASGI manuellement, vous devrez normalement passer une chaîne d'import dans un format spécial pour qu'il importe votre application FastAPI :

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | Remarque

La commande `uvicorn main:app` fait référence à :

* `main` : le fichier `main.py` (le « module » Python).
* `app` : l'objet créé dans `main.py` avec la ligne `app = FastAPI()`.

C'est équivalent à :

```Python
from main import app
```

///

Chaque programme de serveur ASGI alternatif aurait une commande similaire, vous pouvez en lire plus dans leur documentation respective.

/// warning | Alertes

Uvicorn et d'autres serveurs prennent en charge une option `--reload` utile pendant le développement.

L'option `--reload` consomme beaucoup plus de ressources, est plus instable, etc.

Cela aide beaucoup pendant le **développement**, mais vous **ne devriez pas** l'utiliser en **production**.

///

## Concepts de déploiement { #deployment-concepts }

Ces exemples exécutent le programme serveur (par exemple Uvicorn), en démarrant **un seul processus**, à l'écoute sur toutes les IP (`0.0.0.0`) sur un port prédéfini (par exemple `80`).

C'est l'idée de base. Mais vous voudrez probablement vous occuper de certaines choses supplémentaires, comme :

* Sécurité - HTTPS
* Exécution au démarrage
* Redémarrages
* Réplication (le nombre de processus en cours d'exécution)
* Mémoire
* Étapes précédant le démarrage

Je vous en dirai plus sur chacun de ces concepts, sur la manière d'y réfléchir, et donnerai quelques exemples concrets avec des stratégies pour les gérer dans les prochains chapitres. 🚀
