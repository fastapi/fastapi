# Personnaliser les classes Request et APIRoute { #custom-request-and-apiroute-class }

Dans certains cas, vous pouvez vouloir surcharger la logique utilisée par les classes `Request` et `APIRoute`.

En particulier, cela peut être une bonne alternative à une logique dans un middleware.

Par exemple, si vous voulez lire ou manipuler le corps de la requête avant qu'il ne soit traité par votre application.

/// danger | Danger

Ceci est une fonctionnalité « avancée ».

Si vous débutez avec **FastAPI**, vous pouvez ignorer cette section.

///

## Cas d'utilisation { #use-cases }

Voici quelques cas d'utilisation :

* Convertir des corps de requête non JSON en JSON (par exemple <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* Décompresser des corps de requête compressés en gzip.
* Journaliser automatiquement tous les corps de requête.

## Gérer les encodages personnalisés du corps de la requête { #handling-custom-request-body-encodings }

Voyons comment utiliser une sous-classe personnalisée de `Request` pour décompresser des requêtes gzip.

Et une sous-classe d'`APIRoute` pour utiliser cette classe de requête personnalisée.

### Créer une classe `GzipRequest` personnalisée { #create-a-custom-gziprequest-class }

/// tip | Astuce

Il s'agit d'un exemple simplifié pour montrer le fonctionnement ; si vous avez besoin de la prise en charge de Gzip, vous pouvez utiliser le [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank} fourni.

///

Commencez par créer une classe `GzipRequest`, qui va surcharger la méthode `Request.body()` pour décompresser le corps en présence d'un en-tête approprié.

S'il n'y a pas `gzip` dans l'en-tête, elle n'essaiera pas de décompresser le corps.

De cette manière, la même classe de route peut gérer des requêtes gzip compressées ou non compressées.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### Créer une classe `GzipRoute` personnalisée { #create-a-custom-gziproute-class }

Ensuite, nous créons une sous-classe personnalisée de `fastapi.routing.APIRoute` qui utilisera `GzipRequest`.

Cette fois, elle va surcharger la méthode `APIRoute.get_route_handler()`.

Cette méthode renvoie une fonction. Et c'est cette fonction qui recevra une requête et retournera une réponse.

Ici, nous l'utilisons pour créer une `GzipRequest` à partir de la requête originale.

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | Détails techniques

Un `Request` possède un attribut `request.scope`, qui n'est qu'un `dict` Python contenant les métadonnées liées à la requête.

Un `Request` a également un `request.receive`, qui est une fonction pour « recevoir » le corps de la requête.

Le `dict` `scope` et la fonction `receive` font tous deux partie de la spécification ASGI.

Et ces deux éléments, `scope` et `receive`, sont ce dont on a besoin pour créer une nouvelle instance de `Request`.

Pour en savoir plus sur `Request`, consultez <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">la documentation de Starlette sur les requêtes</a>.

///

La seule chose que fait différemment la fonction renvoyée par `GzipRequest.get_route_handler`, c'est de convertir la `Request` en `GzipRequest`.

Ce faisant, notre `GzipRequest` se chargera de décompresser les données (si nécessaire) avant de les transmettre à nos *chemins d'accès*.

Après cela, toute la logique de traitement est identique.

Mais grâce à nos modifications dans `GzipRequest.body`, le corps de la requête sera automatiquement décompressé lorsque **FastAPI** le chargera, si nécessaire.

## Accéder au corps de la requête dans un gestionnaire d'exceptions { #accessing-the-request-body-in-an-exception-handler }

/// tip | Astuce

Pour résoudre ce même problème, il est probablement beaucoup plus simple d'utiliser `body` dans un gestionnaire personnalisé pour `RequestValidationError` ([Gérer les erreurs](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

Mais cet exemple reste valable et montre comment interagir avec les composants internes.

///

Nous pouvons également utiliser cette même approche pour accéder au corps de la requête dans un gestionnaire d'exceptions.

Il suffit de traiter la requête dans un bloc `try`/`except` :

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

Si une exception se produit, l'instance de `Request` sera toujours dans la portée, ce qui nous permet de lire et d'utiliser le corps de la requête lors du traitement de l'erreur :

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## Utiliser une classe `APIRoute` personnalisée dans un routeur { #custom-apiroute-class-in-a-router }

Vous pouvez également définir le paramètre `route_class` d'un `APIRouter` :

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

Dans cet exemple, les *chemins d'accès* sous le `router` utiliseront la classe personnalisée `TimedRoute`, et auront un en-tête supplémentaire `X-Response-Time` dans la réponse avec le temps nécessaire pour générer la réponse :

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
