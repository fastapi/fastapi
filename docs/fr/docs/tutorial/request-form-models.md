# Modèles de formulaire { #form-models }

Vous pouvez utiliser des **modèles Pydantic** pour déclarer des **champs de formulaire** dans FastAPI.

/// info

Pour utiliser les formulaires, installez d'abord <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Assurez-vous de créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis d'installer le paquet, par exemple :

```console
$ pip install python-multipart
```

///

/// note | Remarque

Ceci est pris en charge depuis la version `0.113.0` de FastAPI. 🤓

///

## Modèles Pydantic pour les formulaires { #pydantic-models-for-forms }

Vous avez simplement besoin de déclarer un **modèle Pydantic** avec les champs que vous souhaitez recevoir comme **champs de formulaire**, puis de déclarer le paramètre comme `Form` :

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** va **extraire** les données pour **chaque champ** à partir des **données de formulaire** de la requête et vous fournir le modèle Pydantic que vous avez défini.

## Consulter les documents { #check-the-docs }

Vous pouvez le vérifier dans l'interface des documents à `/docs` :

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Interdire les champs de formulaire supplémentaires { #forbid-extra-form-fields }

Dans certains cas d'utilisation particuliers (probablement peu courants), vous pourriez vouloir **restreindre** les champs de formulaire à ceux déclarés dans le modèle Pydantic, et **interdire** tout champ **supplémentaire**.

/// note | Remarque

Ceci est pris en charge depuis la version `0.114.0` de FastAPI. 🤓

///

Vous pouvez utiliser la configuration du modèle Pydantic pour `forbid` tout champ `extra` :

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

Si un client tente d'envoyer des données supplémentaires, il recevra une **réponse d'erreur**.

Par exemple, si le client essaie d'envoyer les champs de formulaire :

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

Il recevra une réponse d'erreur lui indiquant que le champ `extra` n'est pas autorisé :

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Résumer { #summary }

Vous pouvez utiliser des modèles Pydantic pour déclarer des champs de formulaire dans FastAPI. 😎
