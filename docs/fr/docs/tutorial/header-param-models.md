# Modèles de paramètres d'en-tête { #header-parameter-models }

Si vous avez un groupe de **paramètres d'en-tête** liés, vous pouvez créer un **modèle Pydantic** pour les déclarer.

Cela vous permet de **réutiliser le modèle** à **plusieurs endroits** et aussi de déclarer des validations et des métadonnées pour tous les paramètres en une seule fois. 😎

/// note | Remarque

Cela est pris en charge depuis la version `0.115.0` de FastAPI. 🤓

///

## Paramètres d'en-tête avec un modèle Pydantic { #header-parameters-with-a-pydantic-model }

Déclarez les **paramètres d'en-tête** dont vous avez besoin dans un **modèle Pydantic**, puis déclarez le paramètre comme `Header` :

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** extrait les données de **chaque champ** depuis les **en-têtes** de la requête et vous fournit le modèle Pydantic que vous avez défini.

## Consulter la documentation { #check-the-docs }

Vous pouvez voir les en-têtes requis dans l'interface de la documentation à `/docs` :

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Interdire les en-têtes supplémentaires { #forbid-extra-headers }

Dans certains cas d'utilisation particuliers (probablement pas très courants), vous pourriez vouloir **restreindre** les en-têtes que vous souhaitez recevoir.

Vous pouvez utiliser la configuration du modèle de Pydantic pour `forbid` tout champ `extra` :

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

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

## Désactiver convert_underscores { #disable-convert-underscores }

Comme pour les paramètres d'en-tête classiques, lorsque vous avez des caractères de soulignement dans les noms de paramètres, ils sont **automatiquement convertis en tirets**.

Par exemple, si vous avez un paramètre d'en-tête `save_data` dans le code, l'en-tête HTTP attendu sera `save-data`, et il apparaîtra ainsi dans la documentation.

Si, pour une raison quelconque, vous devez désactiver cette conversion automatique, vous pouvez aussi le faire pour les modèles Pydantic de paramètres d'en-tête.

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | Alertes

Avant de définir `convert_underscores` à `False`, gardez à l'esprit que certains proxys et serveurs HTTP interdisent l'utilisation d'en-têtes contenant des underscores.

///

## Résumé { #summary }

Vous pouvez utiliser des **modèles Pydantic** pour déclarer des **en-têtes** dans **FastAPI**. 😎
