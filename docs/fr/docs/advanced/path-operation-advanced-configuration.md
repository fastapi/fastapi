# Configuration avancée des opérations de chemin { #path-operation-advanced-configuration }

## ID d'opération OpenAPI { #openapi-operationid }

/// warning | Attention

Si vous n'êtes pas un «expert» d'OpenAPI, vous n'en avez probablement pas besoin.

///

Vous pouvez définir l'OpenAPI `operationId` à utiliser dans votre *opération de chemin* avec le paramètre `operation_id`.

Vous devrez vous assurer qu'il soit unique pour chaque opération.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py39.py hl[6] *}

### Utiliser le nom de la *fonction d'opération de chemin* comme operationId { #using-the-path-operation-function-name-as-the-operationid }

Si vous souhaitez utiliser les noms de fonction de vos API comme `operationId`, vous pouvez les parcourir tous et remplacer chaque `operation_id` de l’*opération de chemin* en utilisant leur `APIRoute.name`.

Vous devriez le faire après avoir ajouté toutes vos *opérations de chemin*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py39.py hl[2, 12:21, 24] *}

/// tip | Astuce

Si vous appelez manuellement `app.openapi()`, vous devez mettre à jour les `operationId` avant cela.

///

/// warning | Attention

Si vous faites cela, vous devez vous assurer que chacune de vos *fonctions d'opération de chemin* a un nom unique.

Même si elles se trouvent dans des modules différents (fichiers Python).

///

## Exclure d'OpenAPI { #exclude-from-openapi }

Pour exclure une *opération de chemin* du schéma OpenAPI généré (et donc des systèmes de documentation automatiques), utilisez le paramètre `include_in_schema` et assignez-lui la valeur `False` :

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py39.py hl[6] *}

## Description avancée depuis la docstring { #advanced-description-from-docstring }

Vous pouvez limiter les lignes utilisées de la docstring d'une *fonction d'opération de chemin* pour OpenAPI.

L'ajout d'un `\f` (un caractère d'échappement «form feed») fait que **FastAPI** tronque la sortie utilisée pour OpenAPI à cet endroit.

Cela n'apparaîtra pas dans la documentation, mais d'autres outils (tels que Sphinx) pourront utiliser le reste.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## Réponses supplémentaires { #additional-responses }

Vous avez probablement vu comment déclarer le `response_model` et le `status_code` pour une *opération de chemin*.

Cela définit les métadonnées de la réponse principale d'une *opération de chemin*.

Vous pouvez également déclarer des réponses supplémentaires avec leurs modèles, codes de statut, etc.

Il y a un chapitre entier dans la documentation à ce sujet, vous pouvez le lire dans [Réponses supplémentaires dans OpenAPI](additional-responses.md){.internal-link target=_blank}.

## OpenAPI supplémentaire { #openapi-extra }

Lorsque vous déclarez une *opération de chemin* dans votre application, **FastAPI** génère automatiquement les métadonnées pertinentes concernant cette *opération de chemin* à inclure dans le schéma OpenAPI.

/// note | Détails techniques

Dans la spécification OpenAPI, cela s'appelle l’<a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Objet d'opération</a>.

///

Il contient toutes les informations sur l’*opération de chemin* et est utilisé pour générer automatiquement la documentation.

Il inclut les `tags`, `parameters`, `requestBody`, `responses`, etc.

Ce schéma OpenAPI spécifique à l’*opération de chemin* est normalement généré automatiquement par **FastAPI**, mais vous pouvez également l'étendre.

/// tip | Astuce

Ceci est un point d'extension de bas niveau.

Si vous avez seulement besoin de déclarer des réponses supplémentaires, un moyen plus pratique de le faire est d'utiliser [Réponses supplémentaires dans OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Vous pouvez étendre le schéma OpenAPI pour une *opération de chemin* en utilisant le paramètre `openapi_extra`.

### Extensions OpenAPI { #openapi-extensions }

Cet `openapi_extra` peut être utile, par exemple, pour déclarer des [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) :

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py39.py hl[6] *}

Si vous ouvrez la documentation automatique de l'API, votre extension apparaîtra en bas de l’*opération de chemin* spécifique.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

Et si vous regardez l’OpenAPI résultant (à `/openapi.json` dans votre API), vous verrez également votre extension dans le cadre de l’*opération de chemin* spécifique :

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
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

### Schéma OpenAPI personnalisé pour une *opération de chemin* { #custom-openapi-path-operation-schema }

Le dictionnaire dans `openapi_extra` sera fusionné en profondeur avec le schéma OpenAPI généré automatiquement pour l’*opération de chemin*.

Ainsi, vous pouvez ajouter des données supplémentaires au schéma généré automatiquement.

Par exemple, vous pourriez décider de lire et de valider la requête avec votre propre code, sans utiliser les fonctionnalités automatiques de FastAPI avec Pydantic, mais vous pourriez quand même vouloir définir la requête dans le schéma OpenAPI.

Vous pouvez le faire avec `openapi_extra` :

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py39.py hl[19:36, 39:40] *}

Dans cet exemple, nous n'avons déclaré aucun modèle Pydantic. En fait, le corps de la requête n'est même pas <abbr title="converti d'un format simple, comme des octets, en objets Python">parsé</abbr> en tant que JSON, il est lu directement en tant que `bytes`, et la fonction `magic_data_reader()` serait chargée de l'analyser d'une manière ou d'une autre.

Néanmoins, nous pouvons déclarer le schéma attendu pour le corps de la requête.

### Type de contenu OpenAPI personnalisé { #custom-openapi-content-type }

En utilisant cette même astuce, vous pourriez utiliser un modèle Pydantic pour définir le JSON Schema qui est ensuite inclus dans la section de schéma OpenAPI personnalisée pour l’*opération de chemin*.

Et vous pourriez le faire même si le type de données dans la requête n'est pas du JSON.

Par exemple, dans cette application nous n'utilisons pas la fonctionnalité intégrée de FastAPI pour extraire le JSON Schema des modèles Pydantic ni la validation automatique pour JSON. En fait, nous déclarons le type de contenu de la requête comme YAML, et non JSON :

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[15:20, 22] *}

Néanmoins, bien que nous n'utilisions pas la fonctionnalité intégrée par défaut, nous utilisons toujours un modèle Pydantic pour générer manuellement le JSON Schema pour les données que nous souhaitons recevoir en YAML.

Ensuite, nous utilisons directement la requête et extrayons son corps en tant que `bytes`. Cela signifie que FastAPI n'essaiera même pas d'analyser le payload de la requête en tant que JSON.

Et puis, dans notre code, nous analysons directement ce contenu YAML, puis nous utilisons à nouveau le même modèle Pydantic pour valider le contenu YAML :

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[24:31] *}

/// tip | Astuce

Ici, nous réutilisons le même modèle Pydantic.

Mais de la même manière, nous aurions tout aussi bien pu le valider autrement.

///
