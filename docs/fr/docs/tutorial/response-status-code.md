# Code d'état de la réponse { #response-status-code }

De la même manière que vous pouvez spécifier un modèle de réponse, vous pouvez également déclarer le code d'état HTTP utilisé pour la réponse avec le paramètre `status_code` dans n'importe lequel des chemins d'accès :

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | Remarque

Remarquez que `status_code` est un paramètre de la méthode « decorator » (`get`, `post`, etc.). Pas de votre fonction de chemin d'accès, comme tous les paramètres et le corps.

///

Le paramètre `status_code` reçoit un nombre correspondant au code d'état HTTP.

/// info

`status_code` peut aussi recevoir un `IntEnum`, comme le <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a> de Python.

///

Il va :

* Renvoyer ce code d'état dans la réponse.
* Le documenter comme tel dans le schéma OpenAPI (et donc dans les interfaces utilisateur) :

<img src="/img/tutorial/response-status-code/image01.png">

/// note | Remarque

Certains codes de réponse (voir la section suivante) indiquent que la réponse n'a pas de corps.

FastAPI le sait et produira une documentation OpenAPI indiquant qu'il n'y a pas de corps de réponse.

///

## À propos des codes d'état HTTP { #about-http-status-codes }

/// note | Remarque

Si vous savez déjà ce que sont les codes d'état HTTP, passez à la section suivante.

///

En HTTP, vous envoyez un code d'état numérique de 3 chiffres dans la réponse.

Ces codes d'état ont un nom associé pour les reconnaître, mais la partie importante est le nombre.

En bref :

* `100 - 199` sont pour « Information ». Vous les utilisez rarement directement. Les réponses avec ces codes d'état ne peuvent pas avoir de corps.
* **`200 - 299`** sont pour les réponses de « Succès ». Ce sont celles que vous utiliserez le plus.
    * `200` est le code d'état par défaut, ce qui signifie que tout était « OK ».
    * Un autre exemple est `201`, « Créé ». Il est couramment utilisé après la création d'un nouvel enregistrement dans la base de données.
    * Un cas particulier est `204`, « Aucun contenu ». Cette réponse est utilisée lorsqu'il n'y a aucun contenu à renvoyer au client ; la réponse ne doit donc pas avoir de corps.
* **`300 - 399`** sont pour la « Redirection ». Les réponses avec ces codes d'état peuvent avoir ou non un corps, sauf `304`, « Non modifié », qui ne doit pas en avoir.
* **`400 - 499`** sont pour les réponses d'« Erreur côté client ». C'est probablement le deuxième type que vous utiliserez le plus.
    * Un exemple est `404`, pour une réponse « Non trouvé ».
    * Pour des erreurs génériques du client, vous pouvez simplement utiliser `400`.
* `500 - 599` sont pour les erreurs côté serveur. Vous ne les utilisez presque jamais directement. Lorsqu'un problème survient quelque part dans le code de votre application ou sur le serveur, il renverra automatiquement l'un de ces codes d'état.

/// tip | Astuce

Pour en savoir plus sur chaque code d'état et à quoi il correspond, consultez la <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Réseau des développeurs Mozilla">MDN</abbr> documentation about HTTP status codes</a>.

///

## Raccourci pour se souvenir des noms { #shortcut-to-remember-the-names }

Reprenons l'exemple précédent :

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201` est le code d'état pour « Créé ».

Mais vous n'avez pas à mémoriser la signification de chacun de ces codes.

Vous pouvez utiliser les variables pratiques de `fastapi.status`.

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

Elles ne sont qu'une commodité, elles contiennent le même nombre, mais de cette façon vous pouvez utiliser l'autocomplétion de l'éditeur pour les trouver :

<img src="/img/tutorial/response-status-code/image02.png">

/// note | Détails techniques

Vous pourriez aussi utiliser `from starlette import status`.

FastAPI fournit le même `starlette.status` que `fastapi.status`, uniquement pour votre commodité de développeur. Mais cela vient directement de Starlette.

///

## Modifier la valeur par défaut { #changing-the-default }

Plus tard, dans le [Guide utilisateur avancé](../advanced/response-change-status-code.md){.internal-link target=_blank}, vous verrez comment renvoyer un code d'état différent de celui par défaut que vous déclarez ici.
