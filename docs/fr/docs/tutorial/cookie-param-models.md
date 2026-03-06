# Modèles de paramètres de cookies { #cookie-parameter-models }

Si vous avez un groupe de **cookies** liés, vous pouvez créer un **modèle Pydantic** pour les déclarer. 🍪

Cela vous permet de **réutiliser le modèle** à **plusieurs endroits** et aussi de déclarer des validations et des métadonnées pour tous les paramètres en une seule fois. 😎

/// note | Remarque

Ceci est pris en charge depuis la version `0.115.0` de FastAPI. 🤓

///

/// tip | Astuce

Cette même technique s'applique à `Query`, `Cookie` et `Header`. 😎

///

## Déclarer des cookies avec un modèle Pydantic { #cookies-with-a-pydantic-model }

Déclarez les paramètres de **cookie** dont vous avez besoin dans un **modèle Pydantic**, puis déclarez le paramètre comme `Cookie` :

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** va **extraire** les données pour **chaque champ** à partir des **cookies** reçus dans la requête et vous fournir le modèle Pydantic que vous avez défini.

## Consulter la documentation { #check-the-docs }

Vous pouvez voir les cookies définis dans l'interface de la documentation à `/docs` :

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info

Gardez à l'esprit que, comme les **navigateurs gèrent les cookies** de manière particulière et en arrière-plan, ils **n'autorisent pas** facilement **JavaScript** à y accéder.

Si vous allez dans **l'interface de la documentation de l'API** à `/docs`, vous pourrez voir la **documentation** des cookies pour vos *chemins d'accès*.

Mais même si vous **remplissez les données** et cliquez sur « Execute », comme l'interface de la documentation fonctionne avec **JavaScript**, les cookies ne seront pas envoyés et vous verrez un **message d'erreur** comme si vous n'aviez saisi aucune valeur.

///

## Interdire les cookies supplémentaires { #forbid-extra-cookies }

Dans certains cas d'utilisation particuliers (probablement peu courants), vous pourriez vouloir **restreindre** les cookies que vous souhaitez recevoir.

Votre API a désormais le pouvoir de contrôler son propre <dfn title="C'est une blague, au cas où. Cela n'a rien à voir avec les consentements aux cookies, mais c'est amusant que même l'API puisse maintenant rejeter les pauvres cookies. Prenez un cookie. 🍪">consentement aux cookies</dfn>. 🤪🍪

Vous pouvez utiliser la configuration du modèle de Pydantic pour `forbid` tout champ `extra` :

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

Si un client tente d'envoyer des **cookies supplémentaires**, il recevra une **réponse d'erreur**.

Pauvres bannières de cookies, avec tous leurs efforts pour obtenir votre consentement pour que l'<dfn title="C'est encore une blague. Ne faites pas attention à moi. Prenez un café avec votre cookie. ☕">API pour le rejeter</dfn>. 🍪

Par exemple, si le client tente d'envoyer un cookie `santa_tracker` avec la valeur `good-list-please`, il recevra une **réponse d'erreur** lui indiquant que le `santa_tracker` <dfn title="Le Père Noël désapprouve le manque de cookies. 🎅 D'accord, plus de blagues de cookies.">le cookie n'est pas autorisé</dfn> :

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## Récapitulatif { #summary }

Vous pouvez utiliser des **modèles Pydantic** pour déclarer des <dfn title="Prenez un dernier cookie avant de partir. 🍪">**cookies**</dfn> dans **FastAPI**. 😎
