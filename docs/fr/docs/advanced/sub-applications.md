# Sous-applications - Montage { #sub-applications-mounts }

Si vous avez besoin de deux applications FastAPI indépendantes, avec leur propre OpenAPI et leurs propres interfaces de la documentation, vous pouvez avoir une application principale et « monter » une (ou plusieurs) sous‑application(s).

## Monter une application **FastAPI** { #mounting-a-fastapi-application }

« Monter » signifie ajouter une application entièrement « indépendante » à un chemin spécifique, qui se chargera ensuite de tout gérer sous ce chemin, avec les _chemins d'accès_ déclarés dans cette sous‑application.

### Application de premier niveau { #top-level-application }

Créez d'abord l'application **FastAPI** principale (de premier niveau) et ses *chemins d'accès* :

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[3, 6:8] *}

### Sous-application { #sub-application }

Ensuite, créez votre sous‑application et ses *chemins d'accès*.

Cette sous‑application est simplement une autre application FastAPI standard, mais c'est celle qui sera « montée » :

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 14:16] *}

### Monter la sous-application { #mount-the-sub-application }

Dans votre application de premier niveau, `app`, montez la sous‑application, `subapi`.

Dans ce cas, elle sera montée au chemin `/subapi` :

{* ../../docs_src/sub_applications/tutorial001_py310.py hl[11, 19] *}

### Vérifier la documentation API automatique { #check-the-automatic-api-docs }

Exécutez maintenant la commande `fastapi` avec votre fichier :

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Puis ouvrez la documentation à <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation API automatique pour l'application principale, n'incluant que ses propres _chemins d'accès_ :

<img src="/img/tutorial/sub-applications/image01.png">

Ensuite, ouvrez la documentation de la sous‑application à <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

Vous verrez la documentation API automatique pour la sous‑application, n'incluant que ses propres _chemins d'accès_, tous sous le préfixe de sous‑chemin correct `/subapi` :

<img src="/img/tutorial/sub-applications/image02.png">

Si vous essayez d'interagir avec l'une ou l'autre des deux interfaces, elles fonctionneront correctement, car le navigateur pourra communiquer avec chaque application ou sous‑application spécifique.

### Détails techniques : `root_path` { #technical-details-root-path }

Lorsque vous montez une sous‑application comme ci‑dessus, FastAPI se charge de communiquer le chemin de montage à la sous‑application au moyen d'un mécanisme de la spécification ASGI appelé `root_path`.

De cette manière, la sous‑application saura utiliser ce préfixe de chemin pour l'interface de documentation.

La sous‑application peut également avoir ses propres sous‑applications montées et tout fonctionnera correctement, car FastAPI gère automatiquement tous ces `root_path`.

Vous en apprendrez davantage sur `root_path` et sur la façon de l'utiliser explicitement dans la section [Derrière un proxy](behind-a-proxy.md){.internal-link target=_blank}.
