# CORS (Partage des ressources entre origines) { #cors-cross-origin-resource-sharing }

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS ou « Cross-Origin Resource Sharing »</a> fait référence aux situations où un frontend exécuté dans un navigateur contient du code JavaScript qui communique avec un backend, et où le backend se trouve dans une « origine » différente de celle du frontend.

## Origine { #origin }

Une origine est la combinaison du protocole (`http`, `https`), du domaine (`myapp.com`, `localhost`, `localhost.tiangolo.com`) et du port (`80`, `443`, `8080`).

Ainsi, toutes celles-ci sont des origines différentes :

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Même si elles sont toutes sur `localhost`, elles utilisent des protocoles ou des ports différents, ce sont donc des « origines » différentes.

## Étapes { #steps }

Disons donc que vous avez un frontend exécuté dans votre navigateur à `http://localhost:8080`, et que son JavaScript essaie de communiquer avec un backend exécuté à `http://localhost` (comme nous ne spécifions pas de port, le navigateur supposera le port par défaut `80`).

Le navigateur enverra alors une requête HTTP `OPTIONS` au backend `:80`, et si le backend envoie les en-têtes appropriés autorisant la communication depuis cette origine différente (`http://localhost:8080`), alors le navigateur `:8080` permettra au JavaScript du frontend d’envoyer sa requête au backend `:80`.

Pour y parvenir, le backend `:80` doit disposer d’une liste « d’origines autorisées ».

Dans ce cas, la liste devrait inclure `http://localhost:8080` pour que le frontend `:8080` fonctionne correctement.

## Caractères génériques { #wildcards }

Il est également possible de déclarer la liste comme « * » (un « wildcard ») pour indiquer que toutes sont autorisées.

Mais cela n’autorisera que certains types de communication, en excluant tout ce qui implique des informations d’identification : cookies, en-têtes Authorization comme ceux utilisés avec les Bearer Tokens, etc.

Ainsi, pour que tout fonctionne correctement, il est préférable d’indiquer explicitement les origines autorisées.

## Utiliser `CORSMiddleware` { #use-corsmiddleware }

Vous pouvez le configurer dans votre application **FastAPI** à l’aide de `CORSMiddleware`.

* Importer `CORSMiddleware`.
* Créer une liste d’origines autorisées (sous forme de chaînes).
* L’ajouter comme « middleware » à votre application **FastAPI**.

Vous pouvez également spécifier si votre backend autorise :

* Les informations d’identification (en-têtes Authorization, cookies, etc.).
* Des méthodes HTTP spécifiques (`POST`, `PUT`) ou toutes avec le caractère générique « * ».
* Des en-têtes HTTP spécifiques ou tous avec le caractère générique « * ».

{* ../../docs_src/cors/tutorial001_py310.py hl[2,6:11,13:19] *}

Les paramètres utilisés par défaut par l’implémentation de `CORSMiddleware` sont restrictifs, vous devez donc activer explicitement des origines, méthodes ou en-têtes particuliers afin que les navigateurs soient autorisés à les utiliser dans un contexte inter‑domaine.

Les arguments suivants sont pris en charge :

* `allow_origins` - Une liste d’origines autorisées à effectuer des requêtes cross-origin. Par ex. `['https://example.org', 'https://www.example.org']`. Vous pouvez utiliser `['*']` pour autoriser n’importe quelle origine.
* `allow_origin_regex` - Une chaîne regex pour faire correspondre les origines autorisées à effectuer des requêtes cross-origin. Par ex. `'https://.*\.example\.org'`.
* `allow_methods` - Une liste de méthodes HTTP qui doivent être autorisées pour les requêtes cross-origin. Par défaut `['GET']`. Vous pouvez utiliser `['*']` pour autoriser toutes les méthodes standard.
* `allow_headers` - Une liste d’en-têtes HTTP de requête qui doivent être pris en charge pour les requêtes cross-origin. Par défaut `[]`. Vous pouvez utiliser `['*']` pour autoriser tous les en-têtes. Les en-têtes `Accept`, `Accept-Language`, `Content-Language` et `Content-Type` sont toujours autorisés pour les <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">requêtes CORS simples</a>.
* `allow_credentials` - Indique que les cookies doivent être pris en charge pour les requêtes cross-origin. Par défaut `False`.

    Aucun de `allow_origins`, `allow_methods` et `allow_headers` ne peut être défini à `['*']` si `allow_credentials` est défini à `True`. Ils doivent tous être <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards" class="external-link" rel="noopener" target="_blank">spécifiés explicitement</a>.

* `expose_headers` - Indique les en-têtes de réponse qui doivent être accessibles au navigateur. Par défaut `[]`.
* `max_age` - Définit un temps maximum (en secondes) pendant lequel les navigateurs peuvent mettre en cache les réponses CORS. Par défaut `600`.

Le middleware répond à deux types particuliers de requêtes HTTP ...

### Requêtes CORS de pré‑vérification { #cors-preflight-requests }

Il s’agit de toute requête `OPTIONS` avec les en-têtes `Origin` et `Access-Control-Request-Method`.

Dans ce cas, le middleware interceptera la requête entrante et répondra avec les en-têtes CORS appropriés, et soit une réponse `200`, soit `400` à titre informatif.

### Requêtes simples { #simple-requests }

Toute requête avec un en-tête `Origin`. Dans ce cas, le middleware laissera passer la requête normalement, mais inclura les en-têtes CORS appropriés dans la réponse.

## En savoir plus { #more-info }

Pour plus d’informations sur <abbr title="Cross-Origin Resource Sharing - Partage des ressources entre origines">CORS</abbr>, consultez la <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">documentation CORS de Mozilla</a>.

/// note | Détails techniques

Vous pouvez également utiliser `from starlette.middleware.cors import CORSMiddleware`.

**FastAPI** fournit plusieurs middlewares dans `fastapi.middleware` uniquement pour votre confort, en tant que développeur. Mais la plupart des middlewares disponibles proviennent directement de Starlette.

///
