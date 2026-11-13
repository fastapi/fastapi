# Modèles de paramètres d'en-tête { #header-parameter-models }

Si vous avez un groupe de **paramètres d'en-tête** liés, vous pouvez créer un **modèle Pydantic** pour les déclarer.

Cela vous permet de **réutiliser le modèle** à **plusieurs endroits** et aussi de déclarer des validations et des métadonnées pour tous les paramètres en une seule fois. 😎

/// note | Remarque

Cela est pris en charge depuis la version `0.115.0` de FastAPI. 🤓

///

## Paramètres d'en-tête avec un modèle Pydantic { #header-parameters-with-a-pydantic-model }

Déclarez les **paramètres d'en-tête** dont vous avez besoin dans un **modèle Pydantic**, puis déclarez le paramètre comme `Header` :

{* ../../docs_src/header_param_models/tutorial001.py hl[9:14,18] *}

**FastAPI** **extrait** les données de **chaque champ** depuis les **en-têtes** de la requête et vous fournit le modèle Pydantic que vous avez défini.

## Consultez les documents { #check-the-docs }

Vous pouvez voir les en-têtes requis dans l'interface des documents à `/docs` :

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Interdisez les en-têtes supplémentaires { #forbid-extra-headers }

Dans certains cas d'utilisation particuliers (probablement pas très courants), vous pourriez vouloir **restreindre** les en-têtes que vous souhaitez recevoir.

Vous pouvez utiliser la configuration du modèle de Pydantic pour `forbid` tout champ `extra` :

{* ../../docs_src/header_param_models/tutorial002.py hl[10] *}

Si un client essaie d'envoyer des **en-têtes supplémentaires**, il recevra une **réponse d'erreur**.

Par exemple, si le client essaie d'envoyer un en-tête `tool` avec la valeur `plumbus`, il recevra une **réponse d'erreur** lui indiquant que le paramètre d'en-tête `tool` n'est pas autorisé :

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Désactivez la conversion des caractères de soulignement { #disable-convert-underscores }

Comme pour les paramètres d'en-tête classiques, lorsque vous avez des caractères de soulignement dans les noms de paramètres, ils sont **automatiquement convertis en tirets**.

Par exemple, si vous avez un paramètre d'en-tête `save_data` dans le code, l'en-tête HTTP attendu sera `save-data`, et il apparaîtra ainsi dans les documents.

Si, pour une raison quelconque, vous devez désactiver cette conversion automatique, vous pouvez aussi le faire pour les modèles Pydantic de paramètres d'en-tête.

{* ../../docs_src/header_param_models/tutorial003.py hl[19] *}

/// warning | Alertes

Avant de définir `convert_underscores` à `False`, gardez à l'esprit que certains proxys et serveurs HTTP interdisent l'utilisation d'en-têtes contenant des underscores.

///

## Combinez les modèles de paramètres { #combine-parameter-models }

Vous pouvez combiner plusieurs modèles de paramètres d'en-tête avec des paramètres d'en-tête individuels et des dépendances. Chaque modèle est extrait et validé indépendamment, comme expliqué pour les [modèles de paramètres de requête](query-param-models.md#combine-parameter-models).

La configuration `extra` de chaque modèle s'applique à tous les paramètres d'en-tête, y compris ceux déclarés dans d'autres modèles ou dépendances. Avec `extra="forbid"`, tout en-tête extérieur à ce modèle est rejeté. Avec `extra="allow"`, ces en-têtes sont inclus comme champs supplémentaires du modèle.

Chaque modèle utilise son propre réglage `Header(convert_underscores=...)`, aussi bien lors de la lecture de la requête que lors de la génération d'OpenAPI. Les alias de champs explicites restent des noms d'en-tête littéraux.

## Modèles de paramètres d'en-tête optionnels { #optional-header-parameter-models }

Déclarez un modèle de paramètres d'en-tête avec `| None` et une valeur par défaut de `None` pour rendre le groupe optionnel.

{* ../../docs_src/header_param_models/tutorial004.py hl[15] *}

Si ni `x-client-name` ni `x-client-version` n'est envoyé, `client` vaut `None`. Si l'un des deux est envoyé, FastAPI valide le modèle et exige les deux champs.

Les mêmes règles concernant les valeurs par défaut, les champs supplémentaires et OpenAPI s'appliquent que pour les [modèles de paramètres de requête optionnels](query-param-models.md#optional-query-parameter-models).

Les en-têtes tels que `Host` suivent également la configuration `extra` du modèle. Avec `extra="allow"`, ils rendent le modèle présent même si aucun des deux champs déclarés n'est fourni.

## Résumé { #summary }

Vous pouvez utiliser des **modèles Pydantic** pour déclarer des **en-têtes** dans **FastAPI**. 😎
