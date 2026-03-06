# Callbacks OpenAPI { #openapi-callbacks }

Vous pourriez créer une API avec un *chemin d'accès* qui déclenche une requête vers une *API externe* créée par quelqu'un d'autre (probablement la même personne développeuse qui utiliserait votre API).

Le processus qui se produit lorsque votre application API appelle l’*API externe* s’appelle un « callback ». Parce que le logiciel écrit par la personne développeuse externe envoie une requête à votre API puis votre API « rappelle », en envoyant une requête à une *API externe* (probablement créée par la même personne développeuse).

Dans ce cas, vous pourriez vouloir documenter à quoi cette API externe devrait ressembler. Quel *chemin d'accès* elle devrait avoir, quel corps elle devrait attendre, quelle réponse elle devrait renvoyer, etc.

## Une application avec des callbacks { #an-app-with-callbacks }

Voyons tout cela avec un exemple.

Imaginez que vous développiez une application qui permet de créer des factures.

Ces factures auront un `id`, un `title` (facultatif), un `customer` et un `total`.

L’utilisateur de votre API (une personne développeuse externe) créera une facture dans votre API avec une requête POST.

Ensuite votre API va (imaginons) :

* Envoyer la facture à un client de la personne développeuse externe.
* Encaisser l’argent.
* Renvoyer une notification à l’utilisateur de l’API (la personne développeuse externe).
    * Cela sera fait en envoyant une requête POST (depuis *votre API*) vers une *API externe* fournie par cette personne développeuse externe (c’est le « callback »).

## L’application **FastAPI** normale { #the-normal-fastapi-app }

Voyons d’abord à quoi ressemble l’application API normale avant d’ajouter le callback.

Elle aura un *chemin d'accès* qui recevra un corps `Invoice`, et un paramètre de requête `callback_url` qui contiendra l’URL pour le callback.

Cette partie est assez normale, la plupart du code vous est probablement déjà familier :

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[7:11,34:51] *}

/// tip | Astuce

Le paramètre de requête `callback_url` utilise un type Pydantic <a href="https://docs.pydantic.dev/latest/api/networks/" class="external-link" target="_blank">Url</a>.

///

La seule nouveauté est `callbacks=invoices_callback_router.routes` comme argument du *décorateur de chemin d'accès*. Nous allons voir ce que c’est ensuite.

## Documenter le callback { #documenting-the-callback }

Le code réel du callback dépendra fortement de votre application API.

Et il variera probablement beaucoup d’une application à l’autre.

Cela pourrait être seulement une ou deux lignes de code, comme :

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

Mais la partie la plus importante du callback est sans doute de vous assurer que l’utilisateur de votre API (la personne développeuse externe) implémente correctement l’*API externe*, conformément aux données que *votre API* va envoyer dans le corps de la requête du callback, etc.

Ainsi, ce que nous allons faire ensuite, c’est ajouter le code pour documenter à quoi cette *API externe* devrait ressembler pour recevoir le callback de *votre API*.

Cette documentation apparaîtra dans Swagger UI à `/docs` dans votre API, et permettra aux personnes développeuses externes de savoir comment construire l’*API externe*.

Cet exemple n’implémente pas le callback lui-même (qui pourrait être une simple ligne de code), uniquement la partie documentation.

/// tip | Astuce

Le callback réel n’est qu’une requête HTTP.

En implémentant vous-même le callback, vous pourriez utiliser quelque chose comme <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> ou <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requests</a>.

///

## Écrire le code de documentation du callback { #write-the-callback-documentation-code }

Ce code ne sera pas exécuté dans votre application, nous en avons seulement besoin pour *documenter* à quoi devrait ressembler cette *API externe*.

Mais vous savez déjà comment créer facilement une documentation automatique pour une API avec **FastAPI**.

Nous allons donc utiliser ce même savoir pour documenter à quoi l’*API externe* devrait ressembler ... en créant le(s) *chemin(s) d'accès* que l’API externe devrait implémenter (ceux que votre API appellera).

/// tip | Astuce

Lorsque vous écrivez le code pour documenter un callback, il peut être utile d’imaginer que vous êtes cette *personne développeuse externe*. Et que vous implémentez actuellement l’*API externe*, pas *votre API*.

Adopter temporairement ce point de vue (celui de la *personne développeuse externe*) peut vous aider à trouver plus évident où placer les paramètres, le modèle Pydantic pour le corps, pour la réponse, etc., pour cette *API externe*.

///

### Créer un `APIRouter` de callback { #create-a-callback-apirouter }

Commencez par créer un nouveau `APIRouter` qui contiendra un ou plusieurs callbacks.

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[1,23] *}

### Créer le *chemin d'accès* du callback { #create-the-callback-path-operation }

Pour créer le *chemin d'accès* du callback, utilisez le même `APIRouter` que vous avez créé ci-dessus.

Il devrait ressembler exactement à un *chemin d'accès* FastAPI normal :

* Il devrait probablement déclarer le corps qu’il doit recevoir, par exemple `body: InvoiceEvent`.
* Et il pourrait aussi déclarer la réponse qu’il doit renvoyer, par exemple `response_model=InvoiceEventReceived`.

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[14:16,19:20,26:30] *}

Il y a 2 principales différences par rapport à un *chemin d'accès* normal :

* Il n’a pas besoin d’avoir de code réel, car votre application n’appellera jamais ce code. Il sert uniquement à documenter l’*API externe*. La fonction peut donc simplement contenir `pass`.
* Le *chemin* peut contenir une <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">expression OpenAPI 3</a> (voir plus bas) où il peut utiliser des variables avec des paramètres et des parties de la requête originale envoyée à *votre API*.

### L’expression du chemin de callback { #the-callback-path-expression }

Le *chemin* du callback peut contenir une <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">expression OpenAPI 3</a> qui peut inclure des parties de la requête originale envoyée à *votre API*.

Dans ce cas, c’est la `str` :

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

Ainsi, si l’utilisateur de votre API (la personne développeuse externe) envoie une requête à *votre API* vers :

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

avec un corps JSON :

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

alors *votre API* traitera la facture et, à un moment ultérieur, enverra une requête de callback à `callback_url` (l’*API externe*) :

```
https://www.external.org/events/invoices/2expen51ve
```

avec un corps JSON contenant quelque chose comme :

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

et elle s’attendra à une réponse de cette *API externe* avec un corps JSON comme :

```JSON
{
    "ok": true
}
```

/// tip | Astuce

Remarquez que l’URL de callback utilisée contient l’URL reçue en paramètre de requête dans `callback_url` (`https://www.external.org/events`) et aussi l’`id` de la facture à l’intérieur du corps JSON (`2expen51ve`).

///

### Ajouter le routeur de callback { #add-the-callback-router }

À ce stade, vous avez le(s) *chemin(s) d'accès de callback* nécessaire(s) (celui/ceux que la *personne développeuse externe* doit implémenter dans l’*API externe*) dans le routeur de callback que vous avez créé ci-dessus.

Utilisez maintenant le paramètre `callbacks` dans *le décorateur de chemin d'accès de votre API* pour passer l’attribut `.routes` (qui est en fait juste une `list` de routes/*chemins d'accès*) depuis ce routeur de callback :

{* ../../docs_src/openapi_callbacks/tutorial001_py310.py hl[33] *}

/// tip | Astuce

Remarquez que vous ne passez pas le routeur lui-même (`invoices_callback_router`) à `callback=`, mais l’attribut `.routes`, comme dans `invoices_callback_router.routes`.

///

### Vérifier la documentation { #check-the-docs }

Vous pouvez maintenant démarrer votre application et aller sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez votre documentation incluant une section « Callbacks » pour votre *chemin d'accès* qui montre à quoi l’*API externe* devrait ressembler :

<img src="/img/tutorial/openapi-callbacks/image01.png">
