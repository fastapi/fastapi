# Renvoyer directement une réponse { #return-a-response-directly }

Lorsque vous créez un *chemin d'accès* **FastAPI**, vous pouvez normalement renvoyer n'importe quelle donnée : un `dict`, une `list`, un modèle Pydantic, un modèle de base de données, etc.

Si vous déclarez un [Modèle de réponse](../tutorial/response-model.md), FastAPI l'utilise pour sérialiser les données en JSON, en utilisant Pydantic.

Si vous ne déclarez pas de modèle de réponse, FastAPI utilise le `jsonable_encoder` expliqué dans [Encodeur compatible JSON](../tutorial/encoder.md) et le place dans une `JSONResponse`.

Vous pouvez également créer directement une `JSONResponse` et la renvoyer.

/// tip | Astuce

Vous aurez normalement une bien meilleure performance en utilisant un [Modèle de réponse](../tutorial/response-model.md) qu'en renvoyant directement une `JSONResponse`, car de cette façon la sérialisation des données est effectuée par Pydantic, en Rust.

///

## Renvoyer une `Response` { #return-a-response }

Vous pouvez renvoyer une `Response` ou n'importe laquelle de ses sous-classes.

/// info

`JSONResponse` est elle-même une sous-classe de `Response`.

///

Et lorsque vous renvoyez une `Response`, **FastAPI** la transmet directement.

Il n'effectue aucune conversion de données avec les modèles Pydantic, il ne convertit pas le contenu en un autre type, etc.

Cela vous donne beaucoup de flexibilité. Vous pouvez renvoyer n'importe quel type de données, surcharger toute déclaration ou validation de données, etc.

Cela vous donne aussi beaucoup de responsabilité. Vous devez vous assurer que les données que vous renvoyez sont correctes, dans le bon format, qu'elles peuvent être sérialisées, etc.

## Utiliser le `jsonable_encoder` dans une `Response` { #using-the-jsonable-encoder-in-a-response }

Comme **FastAPI** n'apporte aucune modification à une `Response` que vous renvoyez, vous devez vous assurer que son contenu est prêt pour cela.

Par exemple, vous ne pouvez pas mettre un modèle Pydantic dans une `JSONResponse` sans d'abord le convertir en un `dict` avec tous les types de données (comme `datetime`, `UUID`, etc.) convertis en types compatibles JSON.

Pour ces cas, vous pouvez utiliser le `jsonable_encoder` pour convertir vos données avant de les passer à une réponse :

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | Détails techniques

Vous pouvez aussi utiliser `from starlette.responses import JSONResponse`.

**FastAPI** fournit le même `starlette.responses` que `fastapi.responses` uniquement par commodité pour vous, développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette.

///

## Renvoyer une `Response` personnalisée { #returning-a-custom-response }

L'exemple ci-dessus montre toutes les parties dont vous avez besoin, mais il n'est pas encore très utile, car vous auriez pu renvoyer l'`item` directement, et **FastAPI** l'aurait placé dans une `JSONResponse` pour vous, en le convertissant en `dict`, etc. Tout cela par défaut.

Voyons maintenant comment vous pourriez utiliser cela pour renvoyer une réponse personnalisée.

Disons que vous voulez renvoyer une [réponse XML](https://en.wikipedia.org/wiki/XML).

Vous pouvez placer votre contenu XML dans une chaîne de caractères, le mettre dans une `Response` et le renvoyer :

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Comprendre le fonctionnement d'un Modèle de réponse { #how-a-response-model-works }

Lorsque vous déclarez un [Modèle de réponse - Type de retour](../tutorial/response-model.md) dans un chemin d'accès, **FastAPI** l'utilise pour sérialiser les données en JSON, en utilisant Pydantic.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

Comme cela se passe côté Rust, la performance sera bien meilleure que si cela était fait avec le Python classique et la classe `JSONResponse`.

Lorsque vous utilisez un `response_model` ou un type de retour, FastAPI n'utilise ni le `jsonable_encoder` pour convertir les données (ce qui serait plus lent) ni la classe `JSONResponse`.

À la place, il prend les octets JSON générés avec Pydantic en utilisant le modèle de réponse (ou le type de retour) et renvoie directement une `Response` avec le type de média approprié pour JSON (`application/json`).

## Notes { #notes }

Lorsque vous renvoyez une `Response` directement, ses données ne sont pas validées, converties (sérialisées), ni documentées automatiquement.

Mais vous pouvez toujours les documenter comme décrit dans [Réponses supplémentaires dans OpenAPI](additional-responses.md).

Vous pouvez voir dans les sections suivantes comment utiliser/déclarer ces `Response` personnalisées tout en conservant la conversion automatique des données, la documentation, etc.
