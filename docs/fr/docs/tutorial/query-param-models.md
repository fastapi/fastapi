# Modèles de paramètres de requête { #query-parameter-models }

Si vous avez un groupe de **paramètres de requête** liés, vous pouvez créer un **modèle Pydantic** pour les déclarer.

Cela vous permet de **réutiliser le modèle** à **plusieurs endroits** et aussi de déclarer des validations et des métadonnées pour tous les paramètres en une seule fois. 😎

/// note | Remarque

Pris en charge depuis FastAPI version `0.115.0`. 🤓

///

## Déclarer des paramètres de requête avec un modèle Pydantic { #query-parameters-with-a-pydantic-model }

Déclarez les **paramètres de requête** dont vous avez besoin dans un **modèle Pydantic**, puis déclarez le paramètre en tant que `Query` :

{* ../../docs_src/query_param_models/tutorial001.py hl[9:13,17] *}

**FastAPI** **extrait** les données pour **chaque champ** à partir des **paramètres de requête** de la requête et vous fournit le modèle Pydantic que vous avez défini.

## Consultez les documents { #check-the-docs }

Vous pouvez voir les paramètres de requête dans l'interface des documents à `/docs` :

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Interdisez des paramètres de requête supplémentaires { #forbid-extra-query-parameters }

Dans certains cas d'utilisation particuliers (probablement peu courants), vous pouvez vouloir **restreindre** les paramètres de requête que vous souhaitez recevoir.

Vous pouvez utiliser la configuration du modèle Pydantic pour `forbid` tout champ `extra` :

{* ../../docs_src/query_param_models/tutorial002.py hl[10] *}

Si un client tente d'envoyer des données **supplémentaires** dans les **paramètres de requête**, il recevra une réponse d'**erreur**.

Par exemple, si le client tente d'envoyer un paramètre de requête `tool` avec la valeur `plumbus`, comme :

```http
https://example.com/items/?limit=10&tool=plumbus
```

Il recevra une réponse d'**erreur** lui indiquant que le paramètre de requête `tool` n'est pas autorisé :

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Combinez des modèles de paramètres { #combine-parameter-models }

Vous pouvez déclarer plusieurs modèles de paramètres de requête et les combiner avec des paramètres de requête individuels ou des dépendances.

{* ../../docs_src/query_param_models/tutorial003.py hl[9:15,20:22] *}

Les paramètres de requête restent au même niveau.

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

Il n'y a pas de clés `pagination` ou `filters` dans la chaîne de requête. Chaque modèle valide les paramètres de requête indépendamment, avec ses propres valeurs par défaut, validateurs de champs et validateurs de modèle. Il en va de même lorsque les modèles ou les paramètres individuels sont déclarés dans des dépendances.

Si des modèles partagent un nom de paramètre ou un alias, chaque modèle valide ce paramètre de requête indépendamment. Utilisez des noms ou des alias distincts pour des valeurs indépendantes. OpenAPI ne répertorie un paramètre partagé qu'une seule fois, comme pour les paramètres partagés avec des dépendances ; les déclarations partagées doivent donc décrire le même type et les mêmes contraintes.

La configuration `extra` de chaque modèle s'applique à tous les paramètres de requête, y compris ceux déclarés dans d'autres modèles ou dépendances. Avec `extra="forbid"`, tout paramètre extérieur à ce modèle est rejeté. Avec `extra="allow"`, ces paramètres sont inclus en tant que champs supplémentaires du modèle.

Cela fonctionne aussi pour les modèles `Header` et `Cookie`.

## Modèles de paramètres de requête optionnels { #optional-query-parameter-models }

Déclarez un modèle de paramètres de requête avec `| None` et une valeur par défaut de `None` pour rendre le groupe optionnel.

{* ../../docs_src/query_param_models/tutorial004.py hl[18] *}

Si ni `start` ni `end` n'est envoyé, `date_range` vaut `None`. Si l'un des deux est envoyé, FastAPI valide le modèle et exige les deux champs.

L'utilisation de `| None` sans valeur par défaut laisse le paramètre obligatoire.

Les paramètres supplémentaires suivent la configuration `extra` du modèle. Les paramètres supplémentaires ignorés ne rendent pas le modèle présent.

OpenAPI répertorie les champs du groupe individuellement et les marque comme optionnels.

Vous pouvez aussi déclarer des [modèles de paramètres d'en-tête](header-param-models.md#optional-header-parameter-models) et des [modèles de paramètres de cookie](cookie-param-models.md#optional-cookie-parameter-models) optionnels.

## Résumé { #summary }

Vous pouvez utiliser des **modèles Pydantic** pour déclarer des **paramètres de requête** dans **FastAPI**. 😎

/// tip | Astuce

Alerte spoiler : vous pouvez aussi utiliser des modèles Pydantic pour déclarer des cookies et des en-têtes, mais vous lirez cela plus tard dans le tutoriel. 🤫

///
