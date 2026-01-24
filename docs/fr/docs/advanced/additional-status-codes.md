# Codes de statut supplémentaires { #additional-status-codes }

Par défaut, **FastAPI** renverra les réponses en utilisant une `JSONResponse`, en plaçant le contenu que vous renvoyez depuis votre *chemin d'accès* à l'intérieur de cette `JSONResponse`.

Il utilisera le code de statut par défaut ou celui que vous définissez dans votre *chemin d'accès*.

## Codes de statut supplémentaires { #additional-status-codes_1 }

Si vous souhaitez renvoyer des codes de statut supplémentaires en plus du code principal, vous pouvez le faire en renvoyant directement une `Response`, comme une `JSONResponse`, et en définissant directement le code de statut supplémentaire.

Par exemple, disons que vous voulez avoir un *chemin d'accès* qui permet de mettre à jour des éléments et renvoie des codes de statut HTTP 200 « OK » en cas de succès.

Mais vous voulez aussi qu'il accepte de nouveaux éléments. Et lorsque les éléments n'existaient pas auparavant, il les crée et renvoie un code de statut HTTP de 201 « Created ».

Pour y parvenir, importez `JSONResponse` et renvoyez-y directement votre contenu, en définissant le `status_code` que vous voulez :

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | Alertes

Lorsque vous renvoyez une `Response` directement, comme dans l'exemple ci-dessus, elle sera renvoyée directement.

Elle ne sera pas sérialisée avec un modèle, etc.

Vous devez vous assurer qu'elle contient les données que vous voulez qu'elle contienne, et que les valeurs sont du JSON valide (si vous utilisez `JSONResponse`).

///

/// note | Détails techniques

Vous pouvez également utiliser `from starlette.responses import JSONResponse`.

**FastAPI** fournit les mêmes `starlette.responses` que `fastapi.responses` uniquement par commodité pour vous, le développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette. De même pour `status`.

///

## Documents OpenAPI et API { #openapi-and-api-docs }

Si vous renvoyez directement des codes de statut et des réponses supplémentaires, ils ne seront pas inclus dans le schéma OpenAPI (les documents de l'API), car FastAPI n'a aucun moyen de savoir à l'avance ce que vous allez renvoyer.

Mais vous pouvez documenter cela dans votre code, en utilisant : [Réponses supplémentaires](additional-responses.md){.internal-link target=_blank}.
