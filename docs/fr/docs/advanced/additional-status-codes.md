# Codes HTTP supplémentaires

Par défaut, **FastAPI** renverra les réponses à l'aide d'une structure de données `JSONResponse`, en plaçant la réponse de votre  *chemin d'accès* à l'intérieur de cette `JSONResponse`.

Il utilisera le code HTTP par défaut ou celui que vous avez défini dans votre *chemin d'accès*.

## Codes HTTP supplémentaires

Si vous souhaitez renvoyer des codes HTTP supplémentaires en plus du code principal, vous pouvez le faire en renvoyant directement une `Response`, comme une `JSONResponse`, et en définissant directement le code HTTP supplémentaire.

Par exemple, disons que vous voulez avoir un *chemin d'accès* qui permet de mettre à jour les éléments et renvoie les codes HTTP 200 "OK" en cas de succès.

Mais vous voulez aussi qu'il accepte de nouveaux éléments. Et lorsque les éléments n'existaient pas auparavant, il les crée et renvoie un code HTTP de 201 "Créé".

Pour y parvenir, importez `JSONResponse` et renvoyez-y directement votre contenu, en définissant le `status_code` que vous souhaitez :

```Python hl_lines="4 25"
{!../../../docs_src/additional_status_codes/tutorial001.py!}
```

!!! Attention
    Lorsque vous renvoyez une `Response` directement, comme dans l'exemple ci-dessus, elle sera renvoyée directement.

    Elle ne sera pas sérialisée avec un modèle.

    Assurez-vous qu'il contient les données souhaitées et que les valeurs soient dans un format JSON valides (si vous utilisez une `JSONResponse`).

!!! note "Détails techniques"
    Vous pouvez également utiliser `from starlette.responses import JSONResponse`.

    Pour plus de commodités, **FastAPI** fournit les objets `starlette.responses` sous forme d'un alias accessible par `fastapi.responses`. Mais la plupart des réponses disponibles proviennent directement de Starlette. Il en est de même avec l'objet `statut`.

## Documents OpenAPI et API

Si vous renvoyez directement des codes HTTP et des réponses supplémentaires, ils ne seront pas inclus dans le schéma OpenAPI (la documentation de l'API), car FastAPI n'a aucun moyen de savoir à l'avance ce que vous allez renvoyer.

Mais vous pouvez documenter cela dans votre code, en utilisant : [Réponses supplémentaires dans OpenAPI](additional-responses.md){.internal-link target=_blank}.
