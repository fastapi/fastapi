# Réponses supplémentaires dans OpenAPI

/// warning | Attention

Ceci concerne un sujet plutôt avancé.

Si vous débutez avec **FastAPI**, vous n'en aurez peut-être pas besoin.

///

Vous pouvez déclarer des réponses supplémentaires, avec des codes HTTP, des types de médias, des descriptions, etc.

Ces réponses supplémentaires seront incluses dans le schéma OpenAPI, elles apparaîtront donc également dans la documentation de l'API.

Mais pour ces réponses supplémentaires, vous devez vous assurer de renvoyer directement une `Response` comme `JSONResponse`, avec votre code HTTP et votre contenu.

## Réponse supplémentaire avec `model`

Vous pouvez ajouter à votre décorateur de *paramètre de chemin* un paramètre `responses`.

Il prend comme valeur un `dict` dont les clés sont des codes HTTP pour chaque réponse, comme `200`, et la valeur de ces clés sont d'autres `dict` avec des informations pour chacun d'eux.

Chacun de ces `dict` de réponse peut avoir une clé `model`, contenant un modèle Pydantic, tout comme `response_model`.

**FastAPI** prendra ce modèle, générera son schéma JSON et l'inclura au bon endroit dans OpenAPI.

Par exemple, pour déclarer une autre réponse avec un code HTTP `404` et un modèle Pydantic `Message`, vous pouvez écrire :

{* ../../docs_src/additional_responses/tutorial001.py hl[18,22] *}

/// note | Remarque

Gardez à l'esprit que vous devez renvoyer directement `JSONResponse`.

///

/// info

La clé `model` ne fait pas partie d'OpenAPI.

**FastAPI** prendra le modèle Pydantic à partir de là, générera le `JSON Schema` et le placera au bon endroit.

Le bon endroit est :

* Dans la clé `content`, qui a pour valeur un autre objet JSON (`dict`) qui contient :
    * Une clé avec le type de support, par ex. `application/json`, qui contient comme valeur un autre objet JSON, qui contient :
        * Une clé `schema`, qui a pour valeur le schéma JSON du modèle, voici le bon endroit.
            * **FastAPI** ajoute ici une référence aux schémas JSON globaux à un autre endroit de votre OpenAPI au lieu de l'inclure directement. De cette façon, d'autres applications et clients peuvent utiliser ces schémas JSON directement, fournir de meilleurs outils de génération de code, etc.

///

Les réponses générées au format OpenAPI pour cette *opération de chemin* seront :

```JSON hl_lines="3-12"
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

Les schémas sont référencés à un autre endroit du modèle OpenAPI :

```JSON hl_lines="4-16"
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## Types de médias supplémentaires pour la réponse principale

Vous pouvez utiliser ce même paramètre `responses` pour ajouter différents types de médias pour la même réponse principale.

Par exemple, vous pouvez ajouter un type de média supplémentaire `image/png`, en déclarant que votre *opération de chemin* peut renvoyer un objet JSON (avec le type de média `application/json`) ou une image PNG :

{* ../../docs_src/additional_responses/tutorial002.py hl[19:24,28] *}

/// note | Remarque

Notez que vous devez retourner l'image en utilisant directement un `FileResponse`.

///

/// info

À moins que vous ne spécifiiez explicitement un type de média différent dans votre paramètre `responses`, FastAPI supposera que la réponse a le même type de média que la classe de réponse principale (par défaut `application/json`).

Mais si vous avez spécifié une classe de réponse personnalisée avec `None` comme type de média, FastAPI utilisera `application/json` pour toute réponse supplémentaire associée à un modèle.

///

## Combinaison d'informations

Vous pouvez également combiner des informations de réponse provenant de plusieurs endroits, y compris les paramètres `response_model`, `status_code` et `responses`.

Vous pouvez déclarer un `response_model`, en utilisant le code HTTP par défaut `200` (ou un code personnalisé si vous en avez besoin), puis déclarer des informations supplémentaires pour cette même réponse dans `responses`, directement dans le schéma OpenAPI.

**FastAPI** conservera les informations supplémentaires des `responses` et les combinera avec le schéma JSON de votre modèle.

Par exemple, vous pouvez déclarer une réponse avec un code HTTP `404` qui utilise un modèle Pydantic et a une `description` personnalisée.

Et une réponse avec un code HTTP `200` qui utilise votre `response_model`, mais inclut un `example` personnalisé :

{* ../../docs_src/additional_responses/tutorial003.py hl[20:31] *}

Tout sera combiné et inclus dans votre OpenAPI, et affiché dans la documentation de l'API :

<img src="/img/tutorial/additional-responses/image01.png">

## Combinez les réponses prédéfinies et les réponses personnalisées

Vous voulez peut-être avoir des réponses prédéfinies qui s'appliquent à de nombreux *paramètre de chemin*, mais vous souhaitez les combiner avec des réponses personnalisées nécessaires à chaque *opération de chemin*.

Dans ces cas, vous pouvez utiliser la technique Python "d'affection par décomposition" (appelé _unpacking_ en anglais) d'un `dict` avec `**dict_to_unpack` :

```Python
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Ici, `new_dict` contiendra toutes les paires clé-valeur de `old_dict` plus la nouvelle paire clé-valeur :

```Python
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

Vous pouvez utiliser cette technique pour réutiliser certaines réponses prédéfinies dans vos *paramètres de chemin* et les combiner avec des réponses personnalisées supplémentaires.

Par exemple:

{* ../../docs_src/additional_responses/tutorial004.py hl[13:17,26] *}

## Plus d'informations sur les réponses OpenAPI

Pour voir exactement ce que vous pouvez inclure dans les réponses, vous pouvez consulter ces sections dans la spécification OpenAPI :

* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responsesObject" class="external-link" target="_blank">Objet Responses de OpenAPI </a>, il inclut le `Response Object`.
* <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responseObject" class="external-link" target="_blank">Objet Response de OpenAPI </a>, vous pouvez inclure n'importe quoi directement dans chaque réponse à l'intérieur de votre paramètre `responses`. Y compris `description`, `headers`, `content` (à l'intérieur de cela, vous déclarez différents types de médias et schémas JSON) et `links`.
