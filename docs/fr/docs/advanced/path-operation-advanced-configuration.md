# Configuration avancée des paramètres de chemin

## ID d'opération OpenAPI

/// warning | Attention

Si vous n'êtes pas un "expert" en OpenAPI, vous n'en avez probablement pas besoin.

///

Dans OpenAPI, les chemins sont des ressources, tels que /users/ ou /items/, exposées par votre API, et les opérations sont les méthodes HTTP utilisées pour manipuler ces chemins, telles que GET, POST ou DELETE. Les operationId sont des chaînes uniques facultatives utilisées pour identifier une opération d'un chemin. Vous pouvez définir l'OpenAPI `operationId` à utiliser dans votre *opération de chemin* avec le paramètre `operation_id`.

Vous devez vous assurer qu'il est unique pour chaque opération.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001.py hl[6] *}

### Utilisation du nom *path operation function* comme operationId

Si vous souhaitez utiliser les noms de fonction de vos API comme `operationId`, vous pouvez les parcourir tous et remplacer chaque `operation_id` de l'*opération de chemin* en utilisant leur `APIRoute.name`.

Vous devriez le faire après avoir ajouté toutes vos *paramètres de chemin*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002.py hl[2,12:21,24] *}

/// tip | Astuce

Si vous appelez manuellement `app.openapi()`, vous devez mettre à jour les `operationId` avant.

///

/// warning | Attention

Pour faire cela, vous devez vous assurer que chacun de vos *chemin* ait un nom unique.

Même s'ils se trouvent dans des modules différents (fichiers Python).

///

## Exclusion d'OpenAPI

Pour exclure un *chemin* du schéma OpenAPI généré (et donc des systèmes de documentation automatiques), utilisez le paramètre `include_in_schema` et assignez-lui la valeur `False` :

{* ../../docs_src/path_operation_advanced_configuration/tutorial003.py hl[6] *}

## Description avancée de docstring

Vous pouvez limiter le texte utilisé de la docstring d'une *fonction de chemin* qui sera affiché sur OpenAPI.

L'ajout d'un `\f` (un caractère d'échappement "form feed") va permettre à **FastAPI** de tronquer la sortie utilisée pour OpenAPI à ce stade.

Il n'apparaîtra pas dans la documentation, mais d'autres outils (tel que Sphinx) pourront utiliser le reste.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004.py hl[19:29] *}

## Réponses supplémentaires

Vous avez probablement vu comment déclarer le `response_model` et le `status_code` pour une *opération de chemin*.

Cela définit les métadonnées sur la réponse principale d'une *opération de chemin*.

Vous pouvez également déclarer des réponses supplémentaires avec leurs modèles, codes de statut, etc.

Il y a un chapitre entier ici dans la documentation à ce sujet, vous pouvez le lire sur [Réponses supplémentaires dans OpenAPI](additional-responses.md){.internal-link target=_blank}.

## OpenAPI supplémentaire

Lorsque vous déclarez un *chemin* dans votre application, **FastAPI** génère automatiquement les métadonnées concernant ce *chemin* à inclure dans le schéma OpenAPI.

/// note | Détails techniques

La spécification OpenAPI appelle ces métadonnées des <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Objets d'opération</a>.

///

Il contient toutes les informations sur le *chemin* et est utilisé pour générer automatiquement la documentation.

Il inclut les `tags`, `parameters`, `requestBody`, `responses`, etc.

Ce schéma OpenAPI spécifique aux *operations* est normalement généré automatiquement par **FastAPI**, mais vous pouvez également l'étendre.

/// tip | Astuce

Si vous avez seulement besoin de déclarer des réponses supplémentaires, un moyen plus pratique de le faire est d'utiliser les [réponses supplémentaires dans OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Vous pouvez étendre le schéma OpenAPI pour une *opération de chemin* en utilisant le paramètre `openapi_extra`.

### Extensions OpenAPI

Cet `openapi_extra` peut être utile, par exemple, pour déclarer [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) :

{* ../../docs_src/path_operation_advanced_configuration/tutorial005.py hl[6] *}

Si vous ouvrez la documentation automatique de l'API, votre extension apparaîtra au bas du *chemin* spécifique.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

Et dans le fichier openapi généré (`/openapi.json`), vous verrez également votre extension dans le cadre du *chemin* spécifique :

```JSON hl_lines="22"
{
    "openapi": "3.0.2",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### Personnalisation du Schéma OpenAPI pour un chemin

Le dictionnaire contenu dans la variable `openapi_extra` sera fusionné avec le schéma OpenAPI généré automatiquement pour l'*opération de chemin*.

Ainsi, vous pouvez ajouter des données supplémentaires au schéma généré automatiquement.

Par exemple, vous pouvez décider de lire et de valider la requête avec votre propre code, sans utiliser les fonctionnalités automatiques de validation proposée par Pydantic, mais vous pouvez toujours définir la requête dans le schéma OpenAPI.

Vous pouvez le faire avec `openapi_extra` :

{* ../../docs_src/path_operation_advanced_configuration/tutorial006.py hl[20:37,39:40] *}

Dans cet exemple, nous n'avons déclaré aucun modèle Pydantic. En fait, le corps de la requête n'est même pas <abbr title="converti d'un format simple, comme des octets, en objets Python">parsé</abbr> en tant que JSON, il est lu directement en tant que `bytes`, et la fonction `magic_data_reader()` serait chargé de l'analyser d'une manière ou d'une autre.

Néanmoins, nous pouvons déclarer le schéma attendu pour le corps de la requête.

### Type de contenu OpenAPI personnalisé

En utilisant cette même astuce, vous pouvez utiliser un modèle Pydantic pour définir le schéma JSON qui est ensuite inclus dans la section de schéma OpenAPI personnalisée pour le *chemin* concerné.

Et vous pouvez le faire même si le type de données dans la requête n'est pas au format JSON.

Dans cet exemple, nous n'utilisons pas les fonctionnalités de FastAPI pour extraire le schéma JSON des modèles Pydantic ni la validation automatique pour JSON. En fait, nous déclarons le type de contenu de la requête en tant que YAML, et non JSON :

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[17:22,24] *}

Néanmoins, bien que nous n'utilisions pas la fonctionnalité par défaut, nous utilisons toujours un modèle Pydantic pour générer manuellement le schéma JSON pour les données que nous souhaitons recevoir en YAML.

Ensuite, nous utilisons directement la requête et extrayons son contenu en tant qu'octets. Cela signifie que FastAPI n'essaiera même pas d'analyser le payload de la requête en tant que JSON.

Et nous analysons directement ce contenu YAML, puis nous utilisons à nouveau le même modèle Pydantic pour valider le contenu YAML :

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[26:33] *}

/// tip | Astuce

Ici, nous réutilisons le même modèle Pydantic.

Mais nous aurions pu tout aussi bien pu le valider d'une autre manière.

///
