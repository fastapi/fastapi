# Réponse personnalisée - HTML, flux, fichier, autres { #custom-response-html-stream-file-others }

Par défaut, **FastAPI** renverra les réponses en utilisant `JSONResponse`.

Vous pouvez le remplacer en renvoyant directement une `Response` comme expliqué dans [Renvoyer directement une Response](response-directly.md){.internal-link target=_blank}.

Mais si vous renvoyez directement une `Response` (ou n'importe quelle sous-classe, comme `JSONResponse`), les données ne seront pas automatiquement converties (même si vous déclarez un `response_model`), et la documentation ne sera pas générée automatiquement (par exemple, l'inclusion du « media type » dans l'en-tête HTTP `Content-Type` comme partie de l'OpenAPI généré).

Vous pouvez aussi déclarer la `Response` que vous voulez utiliser (par ex. toute sous-classe de `Response`), dans le décorateur de chemin d'accès en utilisant le paramètre `response_class`.

Le contenu que vous renvoyez depuis votre fonction de chemin d'accès sera placé à l'intérieur de cette `Response`.

Et si cette `Response` a un « media type » JSON (`application/json`), comme c'est le cas avec `JSONResponse` et `UJSONResponse`, les données que vous renvoyez seront automatiquement converties (et filtrées) avec tout `response_model` Pydantic que vous avez déclaré dans le décorateur de chemin d'accès.

/// note | Remarque

Si vous utilisez une classe de réponse sans « media type », FastAPI s'attendra à ce que votre réponse n'ait pas de contenu ; il ne documentera donc pas le format de la réponse dans les documents OpenAPI générés.

///

## Utiliser `ORJSONResponse` { #use-orjsonresponse }

Par exemple, si vous cherchez à maximiser la performance, vous pouvez installer et utiliser <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> et définir la réponse sur `ORJSONResponse`.

Importez la classe (sous-classe) `Response` que vous voulez utiliser et déclarez-la dans le décorateur de chemin d'accès.

Pour de grandes réponses, renvoyer directement une `Response` est bien plus rapide que de renvoyer un dictionnaire.

Cela vient du fait que, par défaut, FastAPI inspectera chaque élément et s'assurera qu'il est sérialisable en JSON, en utilisant le même [Encodeur compatible JSON](../tutorial/encoder.md){.internal-link target=_blank} expliqué dans le didacticiel. C'est ce qui vous permet de renvoyer des objets arbitraires, par exemple des modèles de base de données.

Mais si vous êtes certain que le contenu que vous renvoyez est sérialisable en JSON, vous pouvez le passer directement à la classe de réponse et éviter le surcoût supplémentaire qu'aurait FastAPI en faisant passer votre contenu de retour par le `jsonable_encoder` avant de le transmettre à la classe de réponse.

{* ../../docs_src/custom_response/tutorial001b_py310.py hl[2,7] *}

/// info

Le paramètre `response_class` sera aussi utilisé pour définir le « media type » de la réponse.

Dans ce cas, l'en-tête HTTP `Content-Type` sera défini à `application/json`.

Et il sera documenté comme tel dans OpenAPI.

///

/// tip | Astuce

`ORJSONResponse` est disponible uniquement dans FastAPI, pas dans Starlette.

///

## Réponse HTML { #html-response }

Pour renvoyer une réponse avec du HTML directement depuis **FastAPI**, utilisez `HTMLResponse`.

- Importez `HTMLResponse`.
- Passez `HTMLResponse` comme paramètre `response_class` de votre décorateur de chemin d'accès.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info

Le paramètre `response_class` sera aussi utilisé pour définir le « media type » de la réponse.

Dans ce cas, l'en-tête HTTP `Content-Type` sera défini à `text/html`.

Et il sera documenté comme tel dans OpenAPI.

///

### Renvoyer une `Response` { #return-a-response }

Comme vu dans [Renvoyer directement une Response](response-directly.md){.internal-link target=_blank}, vous pouvez aussi remplacer la réponse directement dans votre chemin d'accès, en la renvoyant.

Le même exemple ci-dessus, renvoyant une `HTMLResponse`, pourrait ressembler à :

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | Alertes

Une `Response` renvoyée directement par votre fonction de chemin d'accès ne sera pas documentée dans OpenAPI (par exemple, le `Content-Type` ne sera pas documenté) et ne sera pas visible dans les documents interactifs automatiques.

///

/// info

Bien sûr, l'en-tête `Content-Type` réel, le code d'état, etc., proviendront de l'objet `Response` que vous avez renvoyé.

///

### Documenter dans OpenAPI et remplacer `Response` { #document-in-openapi-and-override-response }

Si vous voulez remplacer la réponse depuis l'intérieur de la fonction mais en même temps documenter le « media type » dans OpenAPI, vous pouvez utiliser le paramètre `response_class` ET renvoyer un objet `Response`.

`response_class` sera alors utilisé uniquement pour documenter l'opération de chemin d'accès OpenAPI, mais votre `Response` sera utilisée telle quelle.

#### Renvoyer directement une `HTMLResponse` { #return-an-htmlresponse-directly }

Par exemple, cela pourrait être quelque chose comme :

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

Dans cet exemple, la fonction `generate_html_response()` génère déjà et renvoie une `Response` au lieu de renvoyer le HTML dans une `str`.

En renvoyant le résultat de l'appel à `generate_html_response()`, vous renvoyez déjà une `Response` qui remplacera le comportement par défaut de **FastAPI**.

Mais comme vous avez aussi passé `HTMLResponse` dans `response_class`, **FastAPI** saura comment la documenter dans OpenAPI et les documents interactifs comme HTML avec `text/html` :

<img src="/img/tutorial/custom-response/image01.png">

## Réponses disponibles { #available-responses }

Voici certaines des réponses disponibles.

Gardez à l'esprit que vous pouvez utiliser `Response` pour renvoyer autre chose, ou même créer une sous-classe personnalisée.

/// note | Détails techniques

Vous pourriez aussi utiliser `from starlette.responses import HTMLResponse`.

**FastAPI** fournit les mêmes `starlette.responses` sous `fastapi.responses` simplement pour votre confort de développement. Mais la plupart des réponses disponibles viennent directement de Starlette.

///

### `Response` { #response }

La classe principale `Response`, toutes les autres réponses en héritent.

Vous pouvez la renvoyer directement.

Elle accepte les paramètres suivants :

- `content` - Une `str` ou des `bytes`.
- `status_code` - Un code d'état HTTP de type `int`.
- `headers` - Un `dict` de chaînes.
- `media_type` - Une `str` donnant le media type. Par exemple « text/html ».

FastAPI (en fait Starlette) inclura automatiquement un en-tête Content-Length. Il inclura aussi un en-tête Content-Type, basé sur `media_type` et en ajoutant un charset pour les types textuels.

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Prend du texte ou des octets et renvoie une réponse HTML, comme vous l'avez lu ci-dessus.

### `PlainTextResponse` { #plaintextresponse }

Prend du texte ou des octets et renvoie une réponse en texte brut.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Prend des données et renvoie une réponse encodée en `application/json`.

C'est la réponse par défaut utilisée dans **FastAPI**, comme vous l'avez lu ci-dessus.

### `ORJSONResponse` { #orjsonresponse }

Une réponse JSON alternative rapide utilisant <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, comme vous l'avez lu ci-dessus.

/// info

Cela nécessite l'installation de `orjson`, par exemple avec `pip install orjson`.

///

### `UJSONResponse` { #ujsonresponse }

Une réponse JSON alternative utilisant <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

/// info

Cela nécessite l'installation de `ujson`, par exemple avec `pip install ujson`.

///

/// warning | Alertes

`ujson` est moins rigoureux que l'implémentation intégrée de Python dans sa gestion de certains cas limites.

///

{* ../../docs_src/custom_response/tutorial001_py310.py hl[2,7] *}

/// tip | Astuce

Il est possible que `ORJSONResponse` soit une alternative plus rapide.

///

### `RedirectResponse` { #redirectresponse }

Renvoie une redirection HTTP. Utilise par défaut un code d'état 307 (Temporary Redirect).

Vous pouvez renvoyer directement une `RedirectResponse` :

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

Ou vous pouvez l'utiliser dans le paramètre `response_class` :

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

Si vous faites cela, vous pouvez alors renvoyer directement l'URL depuis votre fonction de chemin d'accès.

Dans ce cas, le `status_code` utilisé sera celui par défaut pour `RedirectResponse`, c'est-à-dire `307`.

---

Vous pouvez aussi utiliser le paramètre `status_code` combiné avec le paramètre `response_class` :

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Prend un générateur async ou un générateur/itérateur normal et diffuse le corps de la réponse.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[2,14] *}

#### Utiliser `StreamingResponse` avec des objets de type fichier { #using-streamingresponse-with-file-like-objects }

Si vous avez un objet <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">de type fichier</a> (par ex. l'objet renvoyé par `open()`), vous pouvez créer une fonction génératrice pour itérer sur cet objet de type fichier.

De cette façon, vous n'avez pas à tout lire en mémoire au préalable, et vous pouvez passer cette fonction génératrice à `StreamingResponse`, puis la renvoyer.

Cela inclut de nombreuses bibliothèques pour interagir avec du stockage cloud, du traitement vidéo, et autres.

{* ../../docs_src/custom_response/tutorial008_py310.py hl[2,10:12,14] *}

1. C'est la fonction génératrice. C'est une « fonction génératrice » parce qu'elle contient des instructions `yield` à l'intérieur.
2. En utilisant un bloc `with`, nous nous assurons que l'objet de type fichier est fermé après l'exécution de la fonction génératrice. Donc, après qu'elle a fini d'envoyer la réponse.
3. Ce `yield from` indique à la fonction d'itérer sur l'objet nommé `file_like`. Puis, pour chaque partie itérée, de produire cette partie comme provenant de cette fonction génératrice (`iterfile`).

    Ainsi, c'est une fonction génératrice qui transfère le travail de « génération » à autre chose en interne.

    En procédant ainsi, nous pouvons la placer dans un bloc `with` et, de cette façon, garantir que l'objet de type fichier est fermé après la fin.

/// tip | Astuce

Remarquez qu'ici, comme nous utilisons le `open()` standard qui ne prend pas en charge `async` et `await`, nous déclarons le chemin d'accès avec un `def` normal.

///

### `FileResponse` { #fileresponse }

Diffuse de façon asynchrone un fichier comme réponse.

Prend un ensemble de paramètres différent à l'instanciation par rapport aux autres types de réponse :

- `path` - Le chemin du fichier à diffuser.
- `headers` - D'éventuels en-têtes personnalisés à inclure, sous forme de dictionnaire.
- `media_type` - Une chaîne donnant le media type. Si non défini, le nom du fichier ou le chemin sera utilisé pour en déduire un media type.
- `filename` - Si défini, sera inclus dans l'en-tête `Content-Disposition` de la réponse.

Les réponses de type fichier incluront les en-têtes appropriés `Content-Length`, `Last-Modified` et `ETag`.

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

Vous pouvez aussi utiliser le paramètre `response_class` :

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

Dans ce cas, vous pouvez renvoyer directement le chemin du fichier depuis votre fonction de chemin d'accès.

## Classe de réponse personnalisée { #custom-response-class }

Vous pouvez créer votre propre classe de réponse personnalisée, héritant de `Response`, et l'utiliser.

Par exemple, disons que vous voulez utiliser <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, mais avec certains réglages personnalisés non utilisés dans la classe `ORJSONResponse` incluse.

Disons que vous voulez renvoyer du JSON indenté et formaté, donc vous voulez utiliser l'option orjson `orjson.OPT_INDENT_2`.

Vous pourriez créer une `CustomORJSONResponse`. L'essentiel est de créer une méthode `Response.render(content)` qui renvoie le contenu en `bytes` :

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

Maintenant, au lieu de renvoyer :

```json
{"message": "Hello World"}
```

... cette réponse renverra :

```json
{
  "message": "Hello World"
}
```

Bien sûr, vous trouverez probablement des moyens bien meilleurs de tirer parti de cela que de formater du JSON. 😉

## Classe de réponse par défaut { #default-response-class }

Lors de la création d'une instance de classe **FastAPI** ou d'un `APIRouter`, vous pouvez spécifier quelle classe de réponse utiliser par défaut.

Le paramètre qui le définit est `default_response_class`.

Dans l'exemple ci-dessous, **FastAPI** utilisera `ORJSONResponse` par défaut, dans tous les chemins d'accès, au lieu de `JSONResponse`.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | Astuce

Vous pouvez toujours remplacer `response_class` dans les chemins d'accès comme auparavant.

///

## Documentation supplémentaire { #additional-documentation }

Vous pouvez aussi déclarer le media type et de nombreux autres détails dans OpenAPI en utilisant `responses` : [Réponses supplémentaires dans OpenAPI](additional-responses.md){.internal-link target=_blank}.
