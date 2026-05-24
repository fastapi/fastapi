# Middleware { #middleware }

Vous pouvez ajouter des middlewares aux applications **FastAPI**.

Un « middleware » est une fonction qui agit sur chaque **requête** avant qu’elle ne soit traitée par un *chemin d'accès* spécifique. Et aussi sur chaque **réponse** avant son renvoi.

* Il intercepte chaque **requête** qui parvient à votre application.
* Il peut alors faire quelque chose avec cette **requête** ou exécuter tout code nécessaire.
* Ensuite, il transmet la **requête** pour qu’elle soit traitée par le reste de l’application (par un *chemin d'accès*).
* Puis il récupère la **réponse** générée par l’application (par un *chemin d'accès*).
* Il peut faire quelque chose avec cette **réponse** ou exécuter tout code nécessaire.
* Enfin, il renvoie la **réponse**.

/// note | Détails techniques

Si vous avez des dépendances avec `yield`, le code de sortie s’exécutera après le middleware.

S’il y avait des tâches d’arrière-plan (présentées dans la section [Tâches d’arrière-plan](background-tasks.md), que vous verrez plus tard), elles s’exécuteront après tous les middlewares.

///

## Créer un middleware { #create-a-middleware }

Pour créer un middleware, utilisez le décorateur `@app.middleware("http")` au-dessus d’une fonction.

La fonction de middleware reçoit :

* La `request`.
* Une fonction `call_next` qui recevra la `request` en paramètre.
    * Cette fonction transmettra la `request` au *chemin d'accès* correspondant.
    * Puis elle renverra la `response` générée par le *chemin d'accès* correspondant.
* Vous pouvez ensuite modifier la `response` avant de la renvoyer.

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip | Astuce

Gardez à l’esprit que des en-têtes propriétaires personnalisés peuvent être ajoutés [en utilisant le préfixe `X-`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

Mais si vous avez des en-têtes personnalisés que vous voulez rendre visibles pour un client dans un navigateur, vous devez les ajouter à votre configuration CORS ([CORS (Partage des ressources entre origines)](cors.md)) en utilisant le paramètre `expose_headers` documenté dans [la documentation CORS de Starlette](https://www.starlette.dev/middleware/#corsmiddleware).

///

/// note | Détails techniques

Vous pourriez aussi utiliser `from starlette.requests import Request`.

**FastAPI** le fournit pour votre confort de développeur. Mais cela provient directement de Starlette.

///

### Avant et après la `response` { #before-and-after-the-response }

Vous pouvez ajouter du code à exécuter avec la `request`, avant que tout *chemin d'accès* ne la reçoive.

Et aussi après que la `response` a été générée, avant de la renvoyer.

Par exemple, vous pourriez ajouter un en-tête personnalisé `X-Process-Time` contenant le temps en secondes nécessaire pour traiter la requête et générer une réponse :

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip | Astuce

Ici, nous utilisons [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) au lieu de `time.time()` car cela peut être plus précis pour ces cas d’usage. 🤓

///

## Ordre d’exécution de plusieurs middlewares { #multiple-middleware-execution-order }

Quand vous ajoutez plusieurs middlewares en utilisant soit le décorateur `@app.middleware()`, soit la méthode `app.add_middleware()`, chaque nouveau middleware enveloppe l’application, formant une pile. Le dernier middleware ajouté est le plus externe, et le premier est le plus interne.

Sur le chemin de la requête, le plus externe s’exécute en premier.

Sur le chemin de la réponse, il s’exécute en dernier.

Par exemple :

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

Cela aboutit à l’ordre d’exécution suivant :

* **Requête** : MiddlewareB → MiddlewareA → route

* **Réponse** : route → MiddlewareA → MiddlewareB

Ce comportement d’empilement garantit que les middlewares s’exécutent dans un ordre prévisible et contrôlable.

## Autres middlewares { #other-middlewares }

Vous pouvez en lire davantage sur d’autres middlewares dans le [Guide de l’utilisateur avancé : Middleware avancé](../advanced/middleware.md).

Vous verrez comment gérer <abbr title="Cross-Origin Resource Sharing - Partage des ressources entre origines">CORS</abbr> avec un middleware dans la section suivante.
