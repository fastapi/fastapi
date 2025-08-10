# Sous-application - Montage

Si vous avez besoin de deux applications **FastAPI** indépendantes, avec leur propre implémentation OpenAPI, leur propre documentation, ou autre, vous pouvez monter (mount) une ou plusieurs sous-applications à votre application principale.


## Monter une application **FastAPI**

Monter (mounting) une application signifie ajouter une nouvelle application complètement indépendante sur une URL spécifique, qui prendra en charge tout ce qui se trouve sous cette URL, avec les _opérations de chemin_ déclarées dans cette sous-application.

### Application principale

Premièrement, créez l'application **FastAPI** principale et ses *opérations de chemin* :


```Python hl_lines="3  6-8"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Sous-application

Ensuite, créez votre sous-application et ses *opérations de chemin*.

Cette sous-application est simplement une autre application **FastAPI** standard, mais c'est celle qui sera montée (mount) sur l'application principale :

```Python hl_lines="11  14-16"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Monter la sous-application

Dans votre application principale, `app`, montez la sous-application, `subapi`.

Dans ce cas, elle sera montée sur l'URL `/subapi` :

```Python hl_lines="11  19"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Vérifier la documentation API automatique

Maintenant, exécutez la commande `fastapi` avec votre fichier :

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Et ouvrez la documentation à l'adresse <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation automatique de l'API pour l'application principale, incluant seulement ses propres _opérations de chemin_ :

<img src="/img/tutorial/sub-applications/image01.png">

Et ensuite, ouvrez la documentation pour la sous-application, à l'adresse <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

Vous verrez la documentation API pour la sous-application, incluant uniquement ses propres _opérations de chemin_, toutes avec le préfixe `/subapi` :

<img src="/img/tutorial/sub-applications/image02.png">

Et si vous essayez d'interagir avec l'une des deux API, elles fonctionneront correctement, car le navigateur pourra communiquer avec chaque application ou sous-application spécifique.

### Détails techniques : `root_path`

Quand vous montez une sous-application comme décrit ci-dessus, **FastAPI** se chargera de communiquer le préfixe de la sous-application en utilisant un mécanisme de la spécification ASGI appelé `root_path`.

De cette manière, la sous-application saura utiliser ce préfixe pour la documentation.

Et la sous-application pourrait également avoir ses propres sous-applications montées, et tout fonctionnerait correctement, car FastAPI gère automatiquement tous ces `root_path`.

Vous en apprendrez plus sur le `root_path` et comment l'utiliser explicitement dans la section [Derrière un Proxy](behind-a-proxy.md){.internal-link target=_blank}.
