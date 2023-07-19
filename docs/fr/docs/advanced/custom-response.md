# Réponse personnalisée - HTML, flux, fichier, autres

Par défaut, **FastAPI** renvoie les réponses à l'aide de `JSONResponse`.

Vous pouvez le remplacer en renvoyant une `Response` directement comme indiqué dans [Renvoyer une réponse directement](response-directly.md){.internal-link target=_blank}.

Mais si vous renvoyez une `Response` directement, les données ne seront pas automatiquement converties et la documentation ne sera pas automatiquement générée (par exemple, le "type de support" spécifique, dans l'en-tête HTTP `Content-Type` ne fera pas partie de l'OpenAPI générée).

Mais vous pouvez aussi déclarer la `Response` que vous souhaitez utiliser, dans le *décorateur de chemin*.

Le contenu que vous renvoyez de votre *fonction d'opération de chemin* sera placé à l'intérieur de cette `Response`.

Et si cette `Response` a un type de média JSON (`application/json`), comme c'est le cas avec `JSONResponse` et `UJSONResponse`, les données que vous renvoyez seront automatiquement converties (et filtrées) avec n'importe quel `response_model` de la bibliothèque de validation Pydantic que vous avez déclaré dans le *décorateur du paramètre de chemin*.

!!! note
     Si vous utilisez une classe de réponse sans type de média, FastAPI s'attendra à ce que votre réponse n'ait pas de contenu, il ne documentera donc pas le format de réponse dans ses documents OpenAPI générés.

## Utilisez `ORJSONResponse`

Par exemple, si vous souhaitez optimiser les performances, vous pouvez installer et utiliser <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a > et définissez la réponse sur `ORJSONResponse`.

Importez la classe `Response` (ou une de ses sous-classe) que vous souhaitez utiliser et déclarez-la dans le *décorateur du paramètre de chemin*.

Pour les réponses volumineuses, renvoyer directement une réponse est beaucoup plus rapide que de renvoyer un dictionnaire.

En effet, par défaut, FastAPI inspectera chaque élément à l'intérieur et s'assurera qu'il est sérialisable avec JSON, en utilisant le même [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank} expliqué dans ce tutoriel. C'est ce qui vous permet de renvoyer des **objets arbitraires**, comme des modèles de base de données.

Mais si vous êtes certain que le contenu que vous renvoyez est **sérialisable en JSON**, vous pouvez le transmettre directement à la classe de réponse et éviter une surcharge que FastAPI aurait en transmettant votre contenu de retour via le `jsonable_encoder` avant en le passant à la classe de réponse.

```Python hl_lines="2 7"
{!../../../docs_src/custom_response/tutorial001b.py!}
```

!!! info
     Le paramètre `response_class` sera également utilisé pour définir le "type de média" de la réponse.

     Dans ce cas, l'en-tête HTTP "Content-Type" sera défini sur "application/json".

     Et il sera documenté comme tel dans OpenAPI.

!!! tip "Astuce"
     Le `ORJSONResponse` n'est actuellement disponible que dans FastAPI, pas dans Starlette.

## Réponse HTML

Pour renvoyer une réponse HTML directement à partir de **FastAPI**, utilisez `HTMLResponse`.

* Importer `HTMLResponse`.
* Passez `HTMLResponse` comme paramètre `response_class` de votre *décorateur de chemin*.

```Python hl_lines="2  7"
{!../../../docs_src/custom_response/tutorial002.py!}
```

!!! info
     Le paramètre `response_class` sera également utilisé pour définir le "type de média" de la réponse.

     Dans ce cas, l'en-tête HTTP `Content-Type` sera défini sur `text/html`.

     Et il sera documenté comme tel dans OpenAPI.

### Renvoie d'une `Response`

Comme on le voit dans [Renvoyer une réponse directement](response-directly.md){.internal-link target=_blank}, vous pouvez également remplacer la réponse directement dans votre *chemin*, en la renvoyant.

Le même exemple ci-dessus, renvoyant une `HTMLResponse`, pourrait ressembler à :

```Python hl_lines="2 7 19"
{!../../../docs_src/custom_response/tutorial003.py!}
```

!!! warning "Attention !"
     Une `Response` renvoyée directement par votre *fonction d'opération de chemin* ne sera pas documentée dans OpenAPI (par exemple, le `Content-Type` ne sera pas documenté) et ne sera pas visible dans les documents interactifs automatiques.

!!! info
     Bien entendu, l'en-tête "Content-Type", le code d'état, etc. proviendront de l'objet "Response" que vous avez renvoyé.

### Documentez dans OpenAPI et remplacez `Response`

Si vous souhaitez remplacer la réponse de l'intérieur de la fonction tout en documentant le "type de média" dans OpenAPI, vous pouvez utiliser le paramètre `response_class` ET renvoyer un objet `Response`.

La `response_class` ne sera alors utilisée que pour documenter le *chemin* dans OpenAPI, mais votre `Response` sera utilisée telle quelle.

#### Renvoie directement une `HTMLResponse`

Par exemple, cela pourrait être quelque chose comme :

```Python hl_lines="7 21 23"
{!../../../docs_src/custom_response/tutorial004.py!}
```

Dans cet exemple, la fonction `generate_html_response()` génère déjà et renvoie une `Response` au lieu de renvoyer le HTML dans une `str`.

En renvoyant le résultat de l'appel de `generate_html_response()`, vous renvoyez déjà une `Response` qui remplacera le comportement **FastAPI** par défaut.

Mais comme vous avez également passé `HTMLResponse` dans `response_class`, **FastAPI** saura comment le documenter dans OpenAPI et les documents interactifs au format HTML avec `text/html` :

<img src="/img/tutorial/custom-response/image01.png">

## Réponses disponibles

Voici quelques-unes des réponses disponibles.

Gardez à l'esprit que vous pouvez utiliser `Response` pour renvoyer autre chose, ou même créer une sous-classe personnalisée.

!!! note "Détails techniques"
     Vous pouvez également utiliser `from starlette.responses import HTMLResponse`.

     **FastAPI** fournit le même `starlette.responses` que `fastapi.responses` simplement par commodité. Mais la plupart des réponses disponibles proviennent directement de Starlette.

### `Response`

La classe principale `Response`, toutes les autres réponses en héritent.

Vous pouvez le retourner directement.

Il accepte les paramètres suivants :

* `content` - Une `str` ou `bytes`.
* `status_code` - Un code d'état HTTP `int`.
* `headers` - Un `dict` de chaînes.
* `media_type` - Une `str` donnant le type de média. Par exemple. `"texte/html"`.

FastAPI (en fait Starlette) inclura automatiquement un en-tête Content-Length. Il inclura également un en-tête Content-Type, basé sur le media_type et ajoutant un jeu de caractères pour les types de texte.

```Python hl_lines="1 18"
{!../../../docs_src/response_directly/tutorial002.py!}
```

### `HTMLResponse`

Prend du texte ou des octets et renvoie une réponse HTML, comme vous l'avez lu ci-dessus.

### `PlainTextResponse`

Prend du texte ou des octets et renvoie une réponse en texte brut.

```Python hl_lines="2 7 9"
{!../../../docs_src/custom_response/tutorial005.py!}
```

### `JSONResponse`

Prend des données et renvoie une réponse encodée `application/json`.

Il s'agit de la réponse par défaut utilisée dans **FastAPI**, comme vous l'avez lu ci-dessus.

### `ORJSONResponse`
Une réponse JSON alternative rapide utilisant <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, comme vous l'avez lu ci-dessus.

### `Réponse UJSON`

Une alternative rapide à JSON utilisant <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

!!! warning "Attention !"
     `ujson` est moins fiable que l'implémentation intégrée à Python pour gérer certains cas extrêmes.

```Python hl_lines="2 7"
{!../../../docs_src/custom_response/tutorial001.py !}
```

!!! tip "Astuce"
     Il est possible que `ORJSONResponse` soit une alternative plus rapide.

### `RedirectResponse`

Renvoie une redirection HTTP. Utilise un code d'état 307 (redirection temporaire) par défaut.

Vous pouvez renvoyer directement une `RedirectResponse` :

```Python hl_lines="2 9"
{!../../../docs_src/custom_response/tutorial006.py!}
```

---

Ou vous pouvez l'utiliser dans le paramètre `response_class` :


```Python hl_lines="2 7 9"
{!../../../docs_src/custom_response/tutorial006b.py!}
```

Si vous faites cela, vous pouvez renvoyer l'URL directement à partir de votre fonction *chemin*.

Dans ce cas, le `status_code` utilisé sera celui par défaut pour la `RedirectResponse`, qui est `307`.

---

Vous pouvez également utiliser le paramètre `status_code` combiné avec le paramètre `response_class` :

```Python hl_lines="2 7 9"
{!../../../docs_src/custom_response/tutorial006c.py!}
```

### `StreamingResponse`

Prend un générateur asynchrone ou un générateur/itérateur normal et diffuse le corps de la réponse.

```Python hl_lines="2  14"
{!../../../docs_src/custom_response/tutorial007.py!}
```
#### Utilisation de `StreamingResponse` avec des objets de type fichier

Si vous avez un objet de type fichier (par exemple, un objet renvoyé par `open()`), vous pouvez créer une fonction génératrice pour itérer sur cet objet de type fichier.

De cette façon, vous n'avez pas à tout stocker en mémoire, et vous pouvez passer cette fonction de générateur à `StreamingResponse` et la renvoyer.

Cela inclut de nombreuses bibliothèques pour interagir avec le stockage en ligne (cloud), le traitement vidéo et autres.

```{ .python .annotate hl_lines="2 10-12 14" }
{!../../../docs_src/custom_response/tutorial008.py!}
```

1. C'est une fonction de générateur car elle contient des instructions "yield" à l'intérieur.
2. En utilisant un bloc `with`, nous nous assurons que l'objet de type fichier est fermé une fois la fonction de générateur terminée. Donc, après avoir fini d'envoyer la réponse.
3. Ce `yield from` indique à la fonction d'itérer sur cette chose nommée `file_like`. Et puis, pour chaque partie itérée, donnez cette partie comme provenant de cette fonction génératrice.

C'est donc une fonction génératrice qui transfère le travail "générateur" à autre chose en interne.

En procédant de cette façon, nous pouvons le mettre dans un bloc `with` pour nous assurer qu'il soit fermé à la fin du traitement.

!!! tip "Astuce"
     Notez qu'ici, comme nous utilisons la fonction standart `open()` qui ne prend pas en charge `async` et `wait`, nous devons déclarer l'opération de chemin avec `def` normal.

### `FileResponse`

Diffuse de manière asynchrone un fichier en tant que réponse.

Prend un ensemble d'arguments différent à instancier que les autres types de réponse :

* `path` - Le chemin d'accès au fichier à diffuser.
* `headers` - Tous les en-têtes personnalisés à inclure, sous forme de dictionnaire.
* `media_type` - Une chaîne donnant le type de média. S'il n'est pas défini, le nom de fichier ou le chemin sera utilisé pour déduire un type de média.
* `filename` - Si défini, il sera inclus dans la réponse `Content-Disposition`.

Les réponses de fichier incluront les en-têtes `Content-Length`, `Last-Modified` et `ETag` appropriés.

```Python hl_lines="2 10"
{!../../../docs_src/custom_response/tutorial009.py!}
```

Vous pouvez également utiliser le paramètre `response_class` :

```Python hl_lines="2 8 10"
{!../../../docs_src/custom_response/tutorial009b.py!}
```

Dans ce cas, vous pouvez retourner le chemin du fichier directement depuis votre fonction *chemin*.

## Classe de réponse personnalisée

Vous pouvez créer votre propre classe de réponse personnalisée, en héritant de `Response` et en l'utilisant.

Par exemple, disons que vous voulez utiliser <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, mais avec certains paramètres personnalisés non utilisés dans la classe `ORJSONResponse` incluse.

Supposons que vous souhaitiez qu'il renvoie un JSON indenté et formaté. Vous souhaitez donc utiliser l'option orjson `orjson.OPT_INDENT_2`.

Vous pouvez créer une `CustomORJSONResponse`. La principale chose que vous devez faire est de créer une méthode `Response.render(content)` qui renvoie le contenu sous forme de `bytes` :

```Python hl_lines="9-14 17"
{!../../../docs_src/custom_response/tutorial009c.py!}
```

Maintenant, au lieu de revenir :

```json
{"message": "Bonjour le monde"}
```

...cette réponse renverra :

```json
{
   "message": "Bonjour le monde"
}
```

Bien sûr, vous trouverez probablement de bien meilleurs moyens d'en tirer parti que de formater JSON. 😉

## Classe de réponse par défaut

Lors de la création d'une instance de classe **FastAPI** ou d'un `APIRouter`, vous pouvez spécifier la classe de réponse à utiliser par défaut.

Le paramètre qui définit ceci est `default_response_class`.

Dans l'exemple ci-dessous, **FastAPI** utilisera `ORJSONResponse` par défaut, dans toutes les *opérations de chemin*, au lieu de `JSONResponse`.

```Python hl_lines="2 4"
{!../../../docs_src/custom_response/tutorial010.py!}
```

!!! tip "Astuce"
     Vous pouvez toujours remplacer `response_class` dans votre *chemin* comme avant.

## Documents supplémentaires

Vous pouvez également déclarer le type de média et de nombreux autres détails dans OpenAPI à l'aide de `responses` : [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.