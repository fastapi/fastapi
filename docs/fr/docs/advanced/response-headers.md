# En-têtes de réponse { #response-headers }

## Utiliser un paramètre `Response` { #use-a-response-parameter }

Vous pouvez déclarer un paramètre de type `Response` dans votre fonction de chemin d'accès (comme vous pouvez le faire pour les cookies).

Vous pouvez ensuite définir des en-têtes dans cet objet de réponse temporaire.

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

Ensuite, vous pouvez renvoyer n'importe quel objet dont vous avez besoin, comme d'habitude (un `dict`, un modèle de base de données, etc.).

Et si vous avez déclaré un `response_model`, il sera toujours utilisé pour filtrer et convertir l'objet que vous avez renvoyé.

**FastAPI** utilisera cette réponse temporaire pour extraire les en-têtes (ainsi que les cookies et le code de statut), et les placera dans la réponse finale qui contient la valeur que vous avez renvoyée, filtrée par tout `response_model`.

Vous pouvez également déclarer le paramètre `Response` dans des dépendances, et y définir des en-têtes (et des cookies).

## Renvoyer une `Response` directement { #return-a-response-directly }

Vous pouvez également ajouter des en-têtes lorsque vous renvoyez une `Response` directement.

Créez une réponse comme décrit dans [Renvoyer une Response directement](response-directly.md){.internal-link target=_blank} et passez les en-têtes comme paramètre supplémentaire :

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | Détails techniques

Vous pouvez également utiliser `from starlette.responses import Response` ou `from starlette.responses import JSONResponse`.

**FastAPI** fournit les mêmes `starlette.responses` sous `fastapi.responses` simplement pour votre commodité, en tant que développeur. Mais la plupart des réponses disponibles viennent directement de Starlette.

Et comme `Response` peut être utilisée fréquemment pour définir des en-têtes et des cookies, **FastAPI** la fournit aussi via `fastapi.Response`.

///

## En-têtes personnalisés { #custom-headers }

Gardez à l'esprit que des en-têtes propriétaires personnalisés peuvent être ajoutés <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">en utilisant le préfixe `X-`</a>.

Mais si vous avez des en-têtes personnalisés que vous voulez qu'un client dans un navigateur puisse voir, vous devez les ajouter à vos configurations CORS (en savoir plus dans [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), en utilisant le paramètre `expose_headers` documenté dans <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">la documentation CORS de Starlette</a>.
