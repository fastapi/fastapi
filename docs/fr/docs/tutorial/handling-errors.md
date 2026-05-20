# Gérer les erreurs { #handling-errors }

Il existe de nombreuses situations où vous devez signaler une erreur à un client qui utilise votre API.

Ce client peut être un navigateur avec un frontend, un code d'un tiers, un appareil IoT, etc.

Vous pourriez avoir besoin d'indiquer au client que :

* Le client n'a pas les privilèges suffisants pour cette opération.
* Le client n'a pas accès à cette ressource.
* L'élément auquel le client tentait d'accéder n'existe pas.
* etc.

Dans ces cas, vous retournez normalement un **code d'état HTTP** dans la plage de **400** (de 400 à 499).

C'est similaire aux codes d'état HTTP 200 (de 200 à 299). Ces codes « 200 » signifient que, d'une certaine manière, la requête a été un « succès ».

Les codes d'état dans la plage des 400 signifient qu'il y a eu une erreur côté client.

Vous souvenez-vous de toutes ces erreurs **« 404 Not Found »** (et des blagues) ?

## Utiliser `HTTPException` { #use-httpexception }

Pour renvoyer au client des réponses HTTP avec des erreurs, vous utilisez `HTTPException`.

### Importer `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### Lever une `HTTPException` dans votre code { #raise-an-httpexception-in-your-code }

`HTTPException` est une exception Python normale avec des données supplémentaires pertinentes pour les API.

Comme il s'agit d'une exception Python, vous ne la `return` pas, vous la `raise`.

Cela signifie aussi que si vous êtes dans une fonction utilitaire appelée depuis votre fonction de chemin d'accès, et que vous levez la `HTTPException` à l'intérieur de cette fonction utilitaire, le reste du code de la fonction de chemin d'accès ne s'exécutera pas : la requête sera immédiatement interrompue et l'erreur HTTP issue de la `HTTPException` sera envoyée au client.

L'avantage de lever une exception plutôt que de retourner une valeur apparaîtra plus clairement dans la section sur les Dépendances et la Sécurité.

Dans cet exemple, lorsque le client demande un élément par un ID qui n'existe pas, levez une exception avec un code d'état `404` :

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### Réponse résultante { #the-resulting-response }

Si le client demande `http://example.com/items/foo` (un `item_id` « foo »), il recevra un code d'état HTTP 200 et une réponse JSON :

```JSON
{
  "item": "The Foo Wrestlers"
}
```

Mais si le client demande `http://example.com/items/bar` (un `item_id` inexistant « bar »), il recevra un code d'état HTTP 404 (l'erreur « not found ») et une réponse JSON :

```JSON
{
  "detail": "Item not found"
}
```

/// tip | Astuce

Lorsque vous levez une `HTTPException`, vous pouvez passer n'importe quelle valeur convertible en JSON comme paramètre `detail`, pas uniquement un `str`.

Vous pouvez passer un `dict`, une `list`, etc.

Elles sont gérées automatiquement par **FastAPI** et converties en JSON.

///

## Ajouter des en-têtes personnalisés { #add-custom-headers }

Dans certaines situations, il est utile de pouvoir ajouter des en-têtes personnalisés à l'erreur HTTP. Par exemple, pour certains types de sécurité.

Vous n'aurez probablement pas besoin de l'utiliser directement dans votre code.

Mais si vous en aviez besoin pour un scénario avancé, vous pouvez ajouter des en-têtes personnalisés :

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## Installer des gestionnaires d'exception personnalisés { #install-custom-exception-handlers }

Vous pouvez ajouter des gestionnaires d'exception personnalisés avec [les mêmes utilitaires d'exception de Starlette](https://www.starlette.dev/exceptions/).

Supposons que vous ayez une exception personnalisée `UnicornException` que vous (ou une bibliothèque que vous utilisez) pourriez `raise`.

Et vous souhaitez gérer cette exception globalement avec FastAPI.

Vous pouvez ajouter un gestionnaire d'exception personnalisé avec `@app.exception_handler()` :

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

Ici, si vous appelez `/unicorns/yolo`, le chemin d'accès va `raise` une `UnicornException`.

Mais elle sera gérée par `unicorn_exception_handler`.

Ainsi, vous recevrez une erreur propre, avec un code d'état HTTP `418` et un contenu JSON :

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Détails techniques

Vous pourriez aussi utiliser `from starlette.requests import Request` et `from starlette.responses import JSONResponse`.

**FastAPI** fournit les mêmes `starlette.responses` sous `fastapi.responses` par simple commodité pour vous, développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette. Il en va de même pour `Request`.

///

## Remplacer les gestionnaires d'exception par défaut { #override-the-default-exception-handlers }

**FastAPI** fournit des gestionnaires d'exception par défaut.

Ces gestionnaires se chargent de renvoyer les réponses JSON par défaut lorsque vous `raise` une `HTTPException` et lorsque la requête contient des données invalides.

Vous pouvez remplacer ces gestionnaires d'exception par les vôtres.

### Remplacer les exceptions de validation de la requête { #override-request-validation-exceptions }

Lorsqu'une requête contient des données invalides, **FastAPI** lève en interne une `RequestValidationError`.

Et il inclut également un gestionnaire d'exception par défaut pour cela.

Pour la remplacer, importez `RequestValidationError` et utilisez-la avec `@app.exception_handler(RequestValidationError)` pour décorer le gestionnaire d'exception.

Le gestionnaire d'exception recevra une `Request` et l'exception.

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

À présent, si vous allez sur `/items/foo`, au lieu d'obtenir l'erreur JSON par défaut suivante :

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

vous obtiendrez une version texte, avec :

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### Remplacer le gestionnaire d'erreurs `HTTPException` { #override-the-httpexception-error-handler }

De la même manière, vous pouvez remplacer le gestionnaire de `HTTPException`.

Par exemple, vous pourriez vouloir renvoyer une réponse en texte brut au lieu de JSON pour ces erreurs :

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | Détails techniques

Vous pourriez aussi utiliser `from starlette.responses import PlainTextResponse`.

**FastAPI** fournit les mêmes `starlette.responses` sous `fastapi.responses` par simple commodité pour vous, le développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette.

///

/// warning | Alertes

Gardez à l'esprit que la `RequestValidationError` contient l'information du nom de fichier et de la ligne où l'erreur de validation se produit, afin que vous puissiez l'afficher dans vos journaux avec les informations pertinentes si vous le souhaitez.

Mais cela signifie que si vous vous contentez de la convertir en chaîne et de renvoyer cette information directement, vous pourriez divulguer un peu d'information sur votre système. C'est pourquoi, ici, le code extrait et affiche chaque erreur indépendamment.

///

### Utiliser le corps de `RequestValidationError` { #use-the-requestvalidationerror-body }

La `RequestValidationError` contient le `body` qu'elle a reçu avec des données invalides.

Vous pouvez l'utiliser pendant le développement de votre application pour journaliser le corps et le déboguer, le renvoyer à l'utilisateur, etc.

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

Essayez maintenant d'envoyer un élément invalide comme :

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

Vous recevrez une réponse vous indiquant que les données sont invalides et contenant le corps reçu :

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### `HTTPException` de FastAPI vs `HTTPException` de Starlette { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** a sa propre `HTTPException`.

Et la classe d'erreur `HTTPException` de **FastAPI** hérite de la classe d'erreur `HTTPException` de Starlette.

La seule différence est que la `HTTPException` de **FastAPI** accepte toute donnée sérialisable en JSON pour le champ `detail`, tandis que la `HTTPException` de Starlette n'accepte que des chaînes.

Ainsi, vous pouvez continuer à lever la `HTTPException` de **FastAPI** normalement dans votre code.

Mais lorsque vous enregistrez un gestionnaire d'exception, vous devez l'enregistrer pour la `HTTPException` de Starlette.

De cette façon, si une partie du code interne de Starlette, ou une extension ou un plug-in Starlette, lève une `HTTPException` de Starlette, votre gestionnaire pourra l'intercepter et la traiter.

Dans cet exemple, afin de pouvoir avoir les deux `HTTPException` dans le même code, les exceptions de Starlette sont renommées en `StarletteHTTPException` :

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### Réutiliser les gestionnaires d'exception de **FastAPI** { #reuse-fastapis-exception-handlers }

Si vous souhaitez utiliser l'exception avec les mêmes gestionnaires d'exception par défaut de **FastAPI**, vous pouvez importer et réutiliser les gestionnaires d'exception par défaut depuis `fastapi.exception_handlers` :

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

Dans cet exemple, vous vous contentez d'afficher l'erreur avec un message très expressif, mais vous voyez l'idée. Vous pouvez utiliser l'exception puis simplement réutiliser les gestionnaires d'exception par défaut.
