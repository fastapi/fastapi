# Modèles de formulaire { #form-models }

Vous pouvez utiliser des **modèles Pydantic** pour déclarer des **champs de formulaire** dans FastAPI.

/// note | Remarque

Pour utiliser les formulaires, installez d'abord [`python-multipart`](https://github.com/Kludex/python-multipart).

Ajoutez-le à votre projet :

```console
$ uv add python-multipart
```

///

/// note | Remarque

Ceci est pris en charge depuis la version `0.113.0` de FastAPI. 🤓

///

## Modèles Pydantic pour les formulaires { #pydantic-models-for-forms }

Vous avez simplement besoin de déclarer un **modèle Pydantic** avec les champs que vous souhaitez recevoir comme **champs de formulaire**, puis de déclarer le paramètre comme `Form` :

{* ../../docs_src/request_form_models/tutorial001.py hl[9:11,15] *}

**FastAPI** va **extraire** les données pour **chaque champ** à partir des **données de formulaire** de la requête et vous fournir le modèle Pydantic que vous avez défini.

Pour les [cases à cocher HTML](request-forms.md#boolean-form-fields), déclarez des champs booléens avec une valeur par défaut de `False`.

## Consultez les documents { #check-the-docs }

Vous pouvez le vérifier dans l'interface des documents à `/docs` :

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Interdire les champs de formulaire supplémentaires { #forbid-extra-form-fields }

Dans certains cas d'utilisation particuliers (probablement peu courants), vous pourriez vouloir **restreindre** les champs de formulaire à ceux déclarés dans le modèle Pydantic. Et **interdire** tout champ **supplémentaire**.

/// note | Remarque

Ceci est pris en charge depuis la version `0.114.0` de FastAPI. 🤓

///

Vous pouvez utiliser la configuration du modèle Pydantic pour `forbid` tout champ `extra` :

{* ../../docs_src/request_form_models/tutorial002.py hl[12] *}

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

## Combiner des modèles de formulaire { #combine-form-models }

Vous pouvez combiner plusieurs modèles de formulaire avec des paramètres `Form` individuels.

{* ../../docs_src/request_form_models/tutorial003.py hl[9:14,19:21] *}

Le client envoie `name`, `tags` et `token` comme champs de formulaire. Chaque modèle valide les champs de formulaire indépendamment.

La configuration `extra` de chaque modèle s'applique à tous les champs de formulaire, y compris les champs et les fichiers déclarés dans d'autres paramètres ou dépendances. Avec `extra="forbid"`, tout champ extérieur à ce modèle est rejeté. Avec `extra="allow"`, ces champs sont inclus comme données supplémentaires du modèle.

Si plusieurs déclarations utilisent le même nom de champ de formulaire, chacune valide la valeur de ce champ. Utilisez des types et des contraintes compatibles pour les champs partagés afin que le schéma OpenAPI puisse les décrire de manière cohérente.

## Modèles de formulaire optionnels { #optional-form-models }

Déclarez un modèle de formulaire avec `| None` et une valeur par défaut de `None` pour rendre le groupe optionnel.

{* ../../docs_src/request_form_models/tutorial005.py hl[17] *}

Si ni `name` ni `age` ne sont envoyés, `profile` vaut `None`. Si l'un des deux est envoyé, FastAPI valide le modèle et exige les deux champs. Une valeur vide soumise compte également comme un champ fourni.

Utiliser `| None` sans valeur par défaut laisse le paramètre obligatoire.

Les champs supplémentaires suivent la configuration `extra` du modèle. Les champs supplémentaires ignorés ne rendent pas le modèle présent.

Un modèle optionnel ne contenant que des cases à cocher non cochées est omis. Envoyez une valeur telle que `enabled=false` pour le fournir explicitement.

## Unions optionnelles de modèles de formulaire { #optional-unions-of-form-models }

Vous pouvez également utiliser une union optionnelle de modèles.

{* ../../docs_src/request_form_models/tutorial006.py hl[9:16,21] *}

Si aucun champ de formulaire n'est envoyé, `contact` vaut `None`. Envoyez `kind=person` avec `name`, ou `kind=company` avec `company_name`. Le discriminateur sélectionne le modèle à valider.

## Combiner des unions de modèles de formulaire { #combine-unions-of-form-models }

Vous pouvez combiner des unions avec d'autres modèles de formulaire, des paramètres `Form` individuels et des paramètres `File`. Chaque union est validée indépendamment.

{* ../../docs_src/request_form_models/tutorial007.py hl[31:35] *}

Envoyez tous les champs dans le même formulaire. Par exemple, envoyez `contact_type=person`, `name=Rick`, `notification_type=email`, `email=rick@example.com` et `token=secret`.

Omettez les champs de notification pour laisser `notification` à `None`.

## Modèles de formulaire et fichiers { #form-models-and-files }

Vous pouvez également combiner un modèle de formulaire avec des [paramètres de fichier](request-files.md).

{* ../../docs_src/request_form_models/tutorial004.py hl[14] *}

Ici, le client envoie le champ `name` et le fichier `avatar` en utilisant `multipart/form-data`.

## Résumer { #summary }

Vous pouvez utiliser des modèles Pydantic pour déclarer des champs de formulaire dans FastAPI. 😎
