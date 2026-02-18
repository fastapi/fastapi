# Renvoyer directement une réponse { #return-a-response-directly }

Lorsque vous créez un *chemin d'accès* **FastAPI**, vous pouvez normalement retourner n'importe quelle donnée : un `dict`, une `list`, un modèle Pydantic, un modèle de base de données, etc.

Par défaut, **FastAPI** convertirait automatiquement cette valeur de retour en JSON en utilisant le `jsonable_encoder` expliqué dans [Encodeur compatible JSON](../tutorial/encoder.md){.internal-link target=_blank}.

Ensuite, en arrière-plan, il mettra ces données JSON-compatible (par exemple un `dict`) à l'intérieur d'un `JSONResponse` qui sera utilisé pour envoyer la réponse au client.

Mais vous pouvez retourner une `JSONResponse` directement à partir de vos *chemins d'accès*.

Cela peut être utile, par exemple, pour retourner des en-têtes personnalisés ou des cookies.

## Renvoyer une `Response` { #return-a-response }

En fait, vous pouvez retourner n'importe quelle `Response` ou n'importe quelle sous-classe de celle-ci.

/// tip | Astuce

`JSONResponse` est elle-même une sous-classe de `Response`.

///

Et quand vous retournez une `Response`, **FastAPI** la transmet directement.

Elle ne fera aucune conversion de données avec les modèles Pydantic, elle ne convertira pas le contenu en un type quelconque, etc.

Cela vous donne beaucoup de flexibilité. Vous pouvez retourner n'importe quel type de données, surcharger n'importe quelle déclaration ou validation de données, etc.

## Utiliser le `jsonable_encoder` dans une `Response` { #using-the-jsonable-encoder-in-a-response }

Parce que **FastAPI** n'apporte aucune modification à une `Response` que vous retournez, vous devez vous assurer que son contenu est prêt pour cela.

Par exemple, vous ne pouvez pas mettre un modèle Pydantic dans une `JSONResponse` sans d'abord le convertir en un `dict` avec tous les types de données (comme `datetime`, `UUID`, etc.) convertis en types compatibles avec JSON.

Pour ces cas, vous pouvez utiliser le `jsonable_encoder` pour convertir vos données avant de les passer à une réponse :

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | Détails techniques

Vous pouvez aussi utiliser `from starlette.responses import JSONResponse`.

**FastAPI** fournit le même `starlette.responses` que `fastapi.responses` juste par commodité pour vous, le développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette.

///

## Renvoyer une `Response` personnalisée { #returning-a-custom-response }

L'exemple ci-dessus montre toutes les parties dont vous avez besoin, mais il n'est pas encore très utile, car vous auriez pu retourner l'`item` directement, et **FastAPI** l'aurait mis dans une `JSONResponse` pour vous, en le convertissant en `dict`, etc. Tout cela par défaut.

Maintenant, voyons comment vous pourriez utiliser cela pour retourner une réponse personnalisée.

Disons que vous voulez retourner une réponse <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a>.

Vous pouvez mettre votre contenu XML dans une chaîne de caractères, la placer dans une `Response`, et la retourner :

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Notes { #notes }

Lorsque vous renvoyez une `Response` directement, ses données ne sont pas validées, converties (sérialisées), ni documentées automatiquement.

Mais vous pouvez toujours les documenter comme décrit dans [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

Vous pouvez voir dans les sections suivantes comment utiliser/déclarer ces `Response`s personnalisées tout en conservant la conversion automatique des données, la documentation, etc.
