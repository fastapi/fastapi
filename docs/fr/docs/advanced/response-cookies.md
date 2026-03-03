# Cookies de réponse { #response-cookies }

## Utiliser un paramètre `Response` { #use-a-response-parameter }

Vous pouvez déclarer un paramètre de type `Response` dans votre fonction de chemin d'accès.

Vous pouvez ensuite définir des cookies dans cet objet de réponse *temporaire*.

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

Vous pouvez ensuite renvoyer n'importe quel objet dont vous avez besoin, comme d'habitude (un `dict`, un modèle de base de données, etc.).

Et si vous avez déclaré un `response_model`, il sera toujours utilisé pour filtrer et convertir l'objet que vous avez renvoyé.

**FastAPI** utilisera cette réponse *temporaire* pour extraire les cookies (ainsi que les en-têtes et le code d'état), et les placera dans la réponse finale qui contient la valeur que vous avez renvoyée, filtrée par tout `response_model`.

Vous pouvez également déclarer le paramètre `Response` dans des dépendances, et y définir des cookies (et des en-têtes).

## Renvoyer une `Response` directement { #return-a-response-directly }

Vous pouvez également créer des cookies en renvoyant une `Response` directement dans votre code.

Pour ce faire, vous pouvez créer une réponse comme décrit dans [Renvoyer une Response directement](response-directly.md){.internal-link target=_blank}.

Définissez ensuite des cookies dessus, puis renvoyez-la :

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip | Astuce

Gardez à l'esprit que si vous renvoyez une réponse directement au lieu d'utiliser le paramètre `Response`, FastAPI la renverra telle quelle.

Vous devez donc vous assurer que vos données sont du type correct. Par exemple, qu'elles sont compatibles avec JSON si vous renvoyez une `JSONResponse`.

Et également que vous n'envoyez pas de données qui auraient dû être filtrées par un `response_model`.

///

### En savoir plus { #more-info }

/// note | Détails techniques

Vous pouvez également utiliser `from starlette.responses import Response` ou `from starlette.responses import JSONResponse`.

**FastAPI** fournit les mêmes `starlette.responses` que `fastapi.responses` simplement pour votre commodité, en tant que développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette.

Et comme `Response` peut être utilisé fréquemment pour définir des en-têtes et des cookies, **FastAPI** la met également à disposition via `fastapi.Response`.

///

Pour voir tous les paramètres et options disponibles, consultez la <a href="https://www.starlette.dev/responses/#set-cookie" class="external-link" target="_blank">documentation de Starlette</a>.
