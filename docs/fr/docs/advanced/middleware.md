# Utiliser des middlewares avancés { #advanced-middleware }

Dans le tutoriel principal, vous avez vu comment ajouter des [middlewares personnalisés](../tutorial/middleware.md){.internal-link target=_blank} à votre application.

Vous avez également vu comment gérer [CORS avec le `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

Dans cette section, nous allons voir comment utiliser d'autres middlewares.

## Ajouter des middlewares ASGI { #adding-asgi-middlewares }

Comme **FastAPI** est basé sur Starlette et implémente la spécification <abbr title="Asynchronous Server Gateway Interface - Interface passerelle serveur asynchrone">ASGI</abbr>, vous pouvez utiliser n'importe quel middleware ASGI.

Un middleware n'a pas besoin d'être conçu pour FastAPI ou Starlette pour fonctionner, tant qu'il suit la spécification ASGI.

En général, les middlewares ASGI sont des classes qui s'attendent à recevoir une application ASGI en premier argument.

Ainsi, dans la documentation de middlewares ASGI tiers, on vous indiquera probablement de faire quelque chose comme :

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Mais FastAPI (en fait Starlette) fournit une manière plus simple de le faire, qui garantit que les middlewares internes gèrent les erreurs serveur et que les gestionnaires d'exceptions personnalisés fonctionnent correctement.

Pour cela, vous utilisez `app.add_middleware()` (comme dans l'exemple pour CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` reçoit une classe de middleware en premier argument, ainsi que tout argument supplémentaire à transmettre au middleware.

## Utiliser les middlewares intégrés { #integrated-middlewares }

**FastAPI** inclut plusieurs middlewares pour des cas d'usage courants ; voyons comment les utiliser.

/// note | Détails techniques

Pour les prochains exemples, vous pourriez aussi utiliser `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** fournit plusieurs middlewares dans `fastapi.middleware` simplement pour vous faciliter la vie, en tant que développeur. Mais la plupart des middlewares disponibles viennent directement de Starlette.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

Impose que toutes les requêtes entrantes soient soit `https`, soit `wss`.

Toute requête entrante en `http` ou `ws` sera redirigée vers le schéma sécurisé correspondant.

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

Impose que toutes les requêtes entrantes aient un en-tête `Host` correctement défini, afin de se prémunir contre les attaques de type HTTP Host Header.

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

Les arguments suivants sont pris en charge :

- `allowed_hosts` - Une liste de noms de domaine autorisés comme noms d'hôte. Les domaines génériques tels que `*.example.com` sont pris en charge pour faire correspondre les sous-domaines. Pour autoriser n'importe quel nom d'hôte, utilisez `allowed_hosts=["*"]` ou omettez le middleware.
- `www_redirect` - Si défini à `True`, les requêtes vers les versions sans www des hôtes autorisés seront redirigées vers leurs équivalents avec www. Valeur par défaut : `True`.

Si une requête entrante n'est pas valide, une réponse `400` sera envoyée.

## `GZipMiddleware` { #gzipmiddleware }

Gère les réponses GZip pour toute requête qui inclut « gzip » dans l'en-tête `Accept-Encoding`.

Le middleware gérera les réponses standard et en streaming.

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

Les arguments suivants sont pris en charge :

- `minimum_size` - Ne pas compresser en GZip les réponses dont la taille est inférieure à ce minimum en octets. Valeur par défaut : `500`.
- `compresslevel` - Utilisé pendant la compression GZip. Entier compris entre 1 et 9. Valeur par défaut : `9`. Une valeur plus faible entraîne une compression plus rapide mais des fichiers plus volumineux, tandis qu'une valeur plus élevée entraîne une compression plus lente mais des fichiers plus petits.

## Autres middlewares { #other-middlewares }

Il existe de nombreux autres middlewares ASGI.

Par exemple :

- <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Le `ProxyHeadersMiddleware` d'Uvicorn</a>
- <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Pour voir d'autres middlewares disponibles, consultez <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">la documentation des middlewares de Starlette</a> et la <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">liste ASGI Awesome</a>.
