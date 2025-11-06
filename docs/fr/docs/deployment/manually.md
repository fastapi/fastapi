# Exécuter un serveur manuellement - Uvicorn

La principale chose dont vous avez besoin pour exécuter une application **FastAPI** sur une machine serveur distante est un programme serveur ASGI tel que **Uvicorn**.

Il existe 3 principales alternatives :

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a> : un serveur ASGI haute performance.
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a> : un serveur
  ASGI compatible avec HTTP/2 et Trio entre autres fonctionnalités.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a> : le serveur ASGI
  conçu pour Django Channels.

## Machine serveur et programme serveur

Il y a un petit détail sur les noms à garder à l'esprit. 💡

Le mot "**serveur**" est couramment utilisé pour désigner à la fois l'ordinateur distant/cloud (la machine physique ou virtuelle) et également le programme qui s'exécute sur cette machine (par exemple, Uvicorn).

Gardez cela à l'esprit lorsque vous lisez "serveur" en général, cela pourrait faire référence à l'une de ces deux choses.

Lorsqu'on se réfère à la machine distante, il est courant de l'appeler **serveur**, mais aussi **machine**, **VM** (machine virtuelle), **nœud**. Tout cela fait référence à un type de machine distante, exécutant  Linux, en règle générale, sur laquelle vous exécutez des programmes.


## Installer le programme serveur

Vous pouvez installer un serveur compatible ASGI avec :

//// tab | Uvicorn

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>, un serveur ASGI rapide comme l'éclair, basé sur uvloop et httptools.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

/// tip | Astuce

En ajoutant `standard`, Uvicorn va installer et utiliser quelques dépendances supplémentaires recommandées.

Cela inclut `uvloop`, le remplaçant performant de `asyncio`, qui fournit le gros gain de performance en matière de concurrence.

///

////

//// tab | Hypercorn

* <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, un serveur ASGI également compatible avec HTTP/2.

<div class="termy">

```console
$ pip install hypercorn

---> 100%
```

</div>

...ou tout autre serveur ASGI.

////

## Exécutez le programme serveur

Vous pouvez ensuite exécuter votre application de la même manière que vous l'avez fait dans les tutoriels, mais sans l'option `--reload`, par exemple :

//// tab | Uvicorn

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

////

//// tab | Hypercorn

<div class="termy">

```console
$ hypercorn main:app --bind 0.0.0.0:80

Running on 0.0.0.0:8080 over http (CTRL + C to quit)
```

</div>

////

/// warning

N'oubliez pas de supprimer l'option `--reload` si vous l'utilisiez.

 L'option `--reload` consomme beaucoup plus de ressources, est plus instable, etc.

 Cela aide beaucoup pendant le **développement**, mais vous **ne devriez pas** l'utiliser en **production**.

///

## Hypercorn avec Trio

Starlette et **FastAPI** sont basés sur
<a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>, qui les rend
compatibles avec <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a>, de la bibliothèque standard Python et
<a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a>.

Néanmoins, Uvicorn n'est actuellement compatible qu'avec asyncio, et il utilise normalement <a href="https://github.
com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a >, le remplaçant hautes performances de `asyncio`.

Mais si vous souhaitez utiliser directement **Trio**, vous pouvez utiliser **Hypercorn** car il le prend en charge. ✨

### Installer Hypercorn avec Trio

Vous devez d'abord installer Hypercorn avec le support Trio :

<div class="termy">

```console
$ pip install "hypercorn[trio]"
---> 100%
```

</div>

### Exécuter avec Trio

Ensuite, vous pouvez passer l'option de ligne de commande `--worker-class` avec la valeur `trio` :

<div class="termy">

```console
$ hypercorn main:app --worker-class trio
```

</div>

Et cela démarrera Hypercorn avec votre application en utilisant Trio comme backend.

Vous pouvez désormais utiliser Trio en interne dans votre application. Ou mieux encore, vous pouvez utiliser AnyIO pour que votre code reste compatible avec Trio et asyncio. 🎉

## Concepts de déploiement

Ces exemples lancent le programme serveur (e.g. Uvicorn), démarrant **un seul processus**, sur toutes les IPs (`0.0.
0.0`) sur un port prédéfini (par example, `80`).

C'est l'idée de base. Mais vous vous préoccuperez probablement de certains concepts supplémentaires, tels que ... :

* la sécurité - HTTPS
* l'exécution au démarrage
* les redémarrages
* la réplication (le nombre de processus en cours d'exécution)
* la mémoire
* les étapes précédant le démarrage

Je vous en dirai plus sur chacun de ces concepts, sur la façon de les aborder, et donnerai quelques exemples concrets avec des stratégies pour les traiter dans les prochains chapitres. 🚀
