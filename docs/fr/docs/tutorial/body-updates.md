# Corps - Mises à jour { #body-updates }

## Mettre à jour en remplaçant avec `PUT` { #update-replacing-with-put }

Pour mettre à jour un élément, vous pouvez utiliser l’opération <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a>.

Vous pouvez utiliser le `jsonable_encoder` pour convertir les données d’entrée en données pouvant être stockées au format JSON (par exemple, avec une base de données NoSQL). Par exemple, convertir `datetime` en `str`.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

On utilise `PUT` pour recevoir des données qui doivent remplacer les données existantes.

### Avertissement concernant le remplacement { #warning-about-replacing }

Cela signifie que si vous souhaitez mettre à jour l’élément `bar` avec `PUT` et un corps contenant :

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

comme il n’inclut pas l’attribut déjà enregistré « tax »: 20.2, le modèle d’entrée prendrait la valeur par défaut « tax »: 10.5.

Et les données seraient enregistrées avec cette « nouvelle » `tax` de `10.5`.

## Effectuer des mises à jour partielles avec `PATCH` { #partial-updates-with-patch }

Vous pouvez également utiliser l’opération <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> pour mettre à jour des données de manière partielle.

Cela signifie que vous pouvez n’envoyer que les données que vous souhaitez mettre à jour, en laissant le reste intact.

/// note | Remarque

`PATCH` est moins utilisé et moins connu que `PUT`.

Et de nombreuses équipes n’utilisent que `PUT`, même pour les mises à jour partielles.

Vous êtes libre de les utiliser comme vous le souhaitez, **FastAPI** n’impose aucune restriction.

Mais ce guide vous montre, plus ou moins, la façon dont ils sont censés être utilisés.

///

### Utiliser le paramètre `exclude_unset` de Pydantic { #using-pydantics-exclude-unset-parameter }

Si vous souhaitez recevoir des mises à jour partielles, il est très utile d’utiliser le paramètre `exclude_unset` dans la méthode `.model_dump()` du modèle Pydantic.

Comme `item.model_dump(exclude_unset=True)`.

Cela génère un `dict` ne contenant que les données définies lors de la création du modèle `item`, en excluant les valeurs par défaut.

Vous pouvez ensuite l’utiliser pour produire un `dict` avec uniquement les données définies (envoyées dans la requête), en omettant les valeurs par défaut :

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### Utiliser le paramètre `update` de Pydantic { #using-pydantics-update-parameter }

Vous pouvez maintenant créer une copie du modèle existant avec `.model_copy()`, et passer le paramètre `update` avec un `dict` contenant les données à mettre à jour.

Comme `stored_item_model.model_copy(update=update_data)` :

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### Récapitulatif des mises à jour partielles { #partial-updates-recap }

En résumé, pour appliquer des mises à jour partielles, vous procédez ainsi :

* (Optionnel) utilisez `PATCH` au lieu de `PUT`.
* Récupérez les données stockées.
* Placez ces données dans un modèle Pydantic.
* Générez un `dict` sans valeurs par défaut à partir du modèle d’entrée (en utilisant `exclude_unset`).
    * De cette façon, vous mettez à jour uniquement les valeurs effectivement définies par l’utilisateur, au lieu d’écraser des valeurs déjà stockées par des valeurs par défaut de votre modèle.
* Créez une copie du modèle stocké, en mettant à jour ses attributs avec les mises à jour partielles reçues (en utilisant le paramètre `update`).
* Convertissez le modèle copié en quelque chose qui peut être stocké dans votre base de données (par exemple en utilisant le `jsonable_encoder`).
    * Cela est comparable à l’utilisation à nouveau de la méthode `.model_dump()` du modèle, mais cela vérifie (et convertit) les valeurs vers des types pouvant être convertis en JSON, par exemple `datetime` en `str`.
* Enregistrez les données dans votre base de données.
* Retournez le modèle mis à jour.

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | Astuce

Vous pouvez en réalité utiliser cette même technique avec une opération HTTP `PUT`.

Mais l’exemple ici utilise `PATCH` car il a été créé pour ces cas d’usage.

///

/// note | Remarque

Remarquez que le modèle d’entrée est toujours validé.

Ainsi, si vous souhaitez recevoir des mises à jour partielles pouvant omettre tous les attributs, vous devez disposer d’un modèle avec tous les attributs marqués comme optionnels (avec des valeurs par défaut ou `None`).

Pour distinguer les modèles avec toutes les valeurs optionnelles pour les mises à jour et les modèles avec des valeurs requises pour la création, vous pouvez utiliser les idées décrites dans [Modèles supplémentaires](extra-models.md){.internal-link target=_blank}.

///
