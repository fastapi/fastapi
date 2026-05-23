# Réponse personnalisée - HTML, flux, fichier, autres { #custom-response-html-stream-file-others }

Par défaut, **FastAPI** renvoie des réponses JSON.

Vous pouvez le remplacer en renvoyant une `Response` directement comme vu dans [Renvoyer une Response directement](response-directly.md).

Mais si vous renvoyez directement une `Response` (ou n'importe quelle sous-classe, comme `JSONResponse`), les données ne seront pas automatiquement converties (même si vous déclarez un `response_model`), et la documentation ne sera pas générée automatiquement (par exemple, l'inclusion du « media type », dans l'en-tête HTTP `Content-Type` comme partie de l'OpenAPI généré).

Vous pouvez aussi déclarer la `Response` que vous voulez utiliser (par ex. toute sous-classe de `Response`), dans le décorateur de *chemin d'accès* en utilisant le paramètre `response_class`.

Le contenu que vous renvoyez depuis votre *fonction de chemin d'accès* sera placé à l'intérieur de cette `Response`.

/// note | Remarque

Si vous utilisez une classe de réponse sans media type, FastAPI s'attendra à ce que votre réponse n'ait pas de contenu ; il ne documentera donc pas le format de la réponse dans la documentation OpenAPI générée.

///

## Réponses JSON { #json-responses }

Par défaut, FastAPI renvoie des réponses JSON.

Si vous déclarez un [Modèle de réponse](../tutorial/response-model.md), FastAPI l'utilisera pour sérialiser les données en JSON, en utilisant Pydantic.

Si vous ne déclarez pas de modèle de réponse, FastAPI utilisera le `jsonable_encoder` expliqué dans [Encodeur compatible JSON](../tutorial/encoder.md) et le placera dans une `JSONResponse`.

Si vous déclarez une `response_class` avec un media type JSON (`application/json`), comme c'est le cas avec `JSONResponse`, les données que vous renvoyez seront automatiquement converties (et filtrées) avec tout `response_model` Pydantic que vous avez déclaré dans le décorateur de *chemin d'accès*. Mais les données ne seront pas sérialisées en octets JSON avec Pydantic, elles seront converties avec le `jsonable_encoder` puis passées à la classe `JSONResponse`, qui les sérialisera en octets en utilisant la bibliothèque JSON standard de Python.

### Performance JSON { #json-performance }

En bref, si vous voulez la performance maximale, utilisez un [Modèle de réponse](../tutorial/response-model.md) et ne déclarez pas de `response_class` dans le décorateur de *chemin d'accès*.

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## Réponse HTML { #html-response }

Pour renvoyer une réponse avec du HTML directement depuis **FastAPI**, utilisez `HTMLResponse`.

- Importez `HTMLResponse`.
- Passez `HTMLResponse` comme paramètre `response_class` de votre *décorateur de chemin d'accès*.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info

Le paramètre `response_class` sera aussi utilisé pour définir le « media type » de la réponse.

Dans ce cas, l'en-tête HTTP `Content-Type` sera défini à `text/html`.

Et il sera documenté comme tel dans OpenAPI.

///

### Renvoyer une `Response` { #return-a-response }

Comme vu dans [Renvoyer une Response directement](response-directly.md), vous pouvez aussi remplacer la réponse directement dans votre *chemin d'accès*, en la renvoyant.

Le même exemple ci-dessus, renvoyant une `HTMLResponse`, pourrait ressembler à :

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | Alertes

Une `Response` renvoyée directement par votre *fonction de chemin d'accès* ne sera pas documentée dans OpenAPI (par exemple, le `Content-Type` ne sera pas documenté) et ne sera pas visible dans les documents interactifs automatiques.

///

/// info

Bien sûr, l'en-tête `Content-Type` réel, le code d'état, etc., proviendront de l'objet `Response` que vous avez renvoyé.

///

### Documenter dans OpenAPI et remplacer `Response` { #document-in-openapi-and-override-response }

Si vous voulez remplacer la réponse depuis l'intérieur de la fonction mais en même temps documenter le « media type » dans OpenAPI, vous pouvez utiliser le paramètre `response_class` ET renvoyer un objet `Response`.

`response_class` sera alors utilisé uniquement pour documenter l’*opération de chemin d'accès* OpenAPI, mais votre `Response` sera utilisée telle quelle.

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

Prend du texte ou des octets et renvoie une réponse HTML, comme vous l'avez vu ci-dessus.

### `PlainTextResponse` { #plaintextresponse }

Prend du texte ou des octets et renvoie une réponse en texte brut.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Prend des données et renvoie une réponse encodée en `application/json`.

C'est la réponse par défaut utilisée dans **FastAPI**, comme vous l'avez lu ci-dessus.

/// note | Détails techniques

Mais si vous déclarez un modèle de réponse ou un type de retour, il sera utilisé directement pour sérialiser les données en JSON, et une réponse avec le bon media type pour JSON sera renvoyée directement, sans utiliser la classe `JSONResponse`.

C'est la manière idéale d'obtenir la meilleure performance.

///

### `RedirectResponse` { #redirectresponse }

Renvoie une redirection HTTP. Utilise par défaut un code d'état 307 (Temporary Redirect).

Vous pouvez renvoyer directement une `RedirectResponse` :

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

Ou vous pouvez l'utiliser dans le paramètre `response_class` :

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

Si vous faites cela, vous pouvez alors renvoyer directement l'URL depuis votre *fonction de chemin d'accès*.

Dans ce cas, le `status_code` utilisé sera celui par défaut pour `RedirectResponse`, c'est-à-dire `307`.

---

Vous pouvez aussi utiliser le paramètre `status_code` combiné avec le paramètre `response_class` :

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Prend un générateur async ou un générateur/itérateur normal (une fonction avec `yield`) et diffuse le corps de la réponse.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | Détails techniques

Une tâche `async` ne peut être annulée que lorsqu'elle atteint un `await`. S'il n'y a pas de `await`, le générateur (fonction avec `yield`) ne peut pas être annulé correctement et peut continuer à s'exécuter même après la demande d'annulation.

Comme ce petit exemple n'a besoin d'aucune instruction `await`, nous ajoutons un `await anyio.sleep(0)` pour donner une chance à la boucle d'événements de gérer l'annulation.

Cela serait encore plus important avec des flux volumineux ou infinis.

///

/// tip | Astuce

Au lieu de renvoyer une `StreamingResponse` directement, vous devriez probablement suivre le style de [Diffuser des données](./stream-data.md), c'est beaucoup plus pratique et gère l'annulation en arrière-plan pour vous.

Si vous diffusez des JSON Lines, suivez le didacticiel [Diffuser des JSON Lines](../tutorial/stream-json-lines.md).

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

Dans ce cas, vous pouvez renvoyer directement le chemin du fichier depuis votre *fonction de chemin d'accès*.

## Classe de réponse personnalisée { #custom-response-class }

Vous pouvez créer votre propre classe de réponse personnalisée, héritant de `Response`, et l'utiliser.

Par exemple, disons que vous voulez utiliser [`orjson`](https://github.com/ijl/orjson) avec certains réglages.

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

### `orjson` ou Modèle de réponse { #orjson-or-response-model }

Si ce que vous recherchez est la performance, vous aurez probablement de meilleurs résultats en utilisant un [Modèle de réponse](../tutorial/response-model.md) qu'une réponse `orjson`.

Avec un modèle de réponse, FastAPI utilisera Pydantic pour sérialiser les données en JSON, sans étapes intermédiaires, comme la conversion avec `jsonable_encoder`, qui se produirait dans tout autre cas.

Et en interne, Pydantic utilise les mêmes mécanismes Rust sous-jacents que `orjson` pour sérialiser en JSON, vous obtiendrez donc déjà la meilleure performance avec un modèle de réponse.

## Classe de réponse par défaut { #default-response-class }

Lors de la création d'une instance de classe **FastAPI** ou d'un `APIRouter`, vous pouvez spécifier quelle classe de réponse utiliser par défaut.

Le paramètre qui le définit est `default_response_class`.

Dans l'exemple ci-dessous, **FastAPI** utilisera `HTMLResponse` par défaut, dans tous les *chemins d'accès*, au lieu de JSON.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | Astuce

Vous pouvez toujours remplacer `response_class` dans les *chemins d'accès* comme auparavant.

///

## Documentation supplémentaire { #additional-documentation }

Vous pouvez aussi déclarer le media type et de nombreux autres détails dans OpenAPI en utilisant `responses` : [Réponses supplémentaires dans OpenAPI](additional-responses.md).
