# Étendre OpenAPI { #extending-openapi }

Il existe des cas où vous pouvez avoir besoin de modifier le schéma OpenAPI généré.

Dans cette section, vous verrez comment faire.

## Le processus normal { #the-normal-process }

Le processus normal (par défaut) est le suivant.

Une application (instance) `FastAPI` a une méthode `.openapi()` censée retourner le schéma OpenAPI.

Lors de la création de l'objet application, un *chemin d'accès* pour `/openapi.json` (ou pour l'URL que vous avez définie dans votre `openapi_url`) est enregistré.

Il renvoie simplement une réponse JSON avec le résultat de la méthode `.openapi()` de l'application.

Par défaut, la méthode `.openapi()` vérifie la propriété `.openapi_schema` pour voir si elle contient des données et les renvoie.

Sinon, elle les génère à l'aide de la fonction utilitaire `fastapi.openapi.utils.get_openapi`.

Et cette fonction `get_openapi()` reçoit comme paramètres :

* `title` : Le titre OpenAPI, affiché dans les documents.
* `version` : La version de votre API, p. ex. `2.5.0`.
* `openapi_version` : La version de la spécification OpenAPI utilisée. Par défaut, la plus récente : `3.1.0`.
* `summary` : Un court résumé de l'API.
* `description` : La description de votre API ; elle peut inclure du markdown et sera affichée dans la documentation.
* `routes` : Une liste de routes ; chacune correspond à un *chemin d'accès* enregistré. Elles sont extraites de `app.routes`.

/// info

Le paramètre `summary` est disponible à partir d'OpenAPI 3.1.0, pris en charge par FastAPI 0.99.0 et versions ultérieures.

///

## Remplacer les valeurs par défaut { #overriding-the-defaults }

En vous appuyant sur les informations ci-dessus, vous pouvez utiliser la même fonction utilitaire pour générer le schéma OpenAPI et remplacer chaque partie dont vous avez besoin.

Par exemple, ajoutons <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">l’extension OpenAPI de ReDoc pour inclure un logo personnalisé</a>.

### **FastAPI** normal { #normal-fastapi }

Tout d’abord, écrivez votre application **FastAPI** comme d’habitude :

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### Générer le schéma OpenAPI { #generate-the-openapi-schema }

Ensuite, utilisez la même fonction utilitaire pour générer le schéma OpenAPI, dans une fonction `custom_openapi()` :

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### Modifier le schéma OpenAPI { #modify-the-openapi-schema }

Vous pouvez maintenant ajouter l’extension ReDoc, en ajoutant un `x-logo` personnalisé à l’« objet » `info` dans le schéma OpenAPI :

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### Mettre en cache le schéma OpenAPI { #cache-the-openapi-schema }

Vous pouvez utiliser la propriété `.openapi_schema` comme « cache » pour stocker votre schéma généré.

Ainsi, votre application n’aura pas à générer le schéma à chaque fois qu’un utilisateur ouvre les documents de votre API.

Il ne sera généré qu’une seule fois, puis le même schéma en cache sera utilisé pour les requêtes suivantes.

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### Remplacer la méthode { #override-the-method }

Vous pouvez maintenant remplacer la méthode `.openapi()` par votre nouvelle fonction.

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### Vérifier { #check-it }

Une fois que vous allez sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>, vous verrez que vous utilisez votre logo personnalisé (dans cet exemple, le logo de **FastAPI**) :

<img src="/img/tutorial/extending-openapi/image01.png">
