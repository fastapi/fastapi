# Paramètres de requête { #query-parameters }

Lorsque vous déclarez d'autres paramètres de fonction qui ne font pas partie des paramètres de chemin, ils sont automatiquement interprétés comme des paramètres de «requête».

{* ../../docs_src/query_params/tutorial001_py39.py hl[9] *}

La partie appelée requête (ou «query») dans une URL est l'ensemble des paires clé-valeur placées après le `?`, séparées par des `&`.

Par exemple, dans l'URL :

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

... les paramètres de requête sont :

* `skip` : avec une valeur de `0`
* `limit` : avec une valeur de `10`

Faisant partie de l'URL, ces valeurs sont des chaînes de caractères (`str`).

Mais quand on les déclare avec des types Python (dans l'exemple précédent, en tant qu'`int`), elles sont converties dans les types renseignés.

Toutes les fonctionnalités qui s'appliquent aux paramètres de chemin s'appliquent aussi aux paramètres de requête :

* Prise en charge par l'éditeur (évidemment)
* <abbr title="conversion de la chaîne de caractères venant de la requête HTTP en données Python">«parsing»</abbr> des données
* Validation des données
* Documentation automatique

## Valeurs par défaut { #defaults }

Les paramètres de requête ne sont pas une partie fixe d'un chemin, ils peuvent être optionnels et avoir des valeurs par défaut.

Dans l'exemple ci-dessus, ils ont des valeurs par défaut qui sont `skip=0` et `limit=10`.

Donc, accéder à l'URL :

```
http://127.0.0.1:8000/items/
```

serait équivalent à accéder à l'URL :

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Mais si vous accédez à, par exemple :

```
http://127.0.0.1:8000/items/?skip=20
```

Les valeurs des paramètres de votre fonction seront :

* `skip=20` : car c'est la valeur déclarée dans l'URL.
* `limit=10` : car `limit` n'a pas été déclaré dans l'URL, et que la valeur par défaut était `10`.

## Paramètres optionnels { #optional-parameters }

De la même façon, vous pouvez définir des paramètres de requête comme optionnels, en leur donnant comme valeur par défaut `None` :

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

Ici, le paramètre `q` sera optionnel, et aura `None` comme valeur par défaut.

/// check | vérifier

On peut voir que **FastAPI** est capable de détecter que le paramètre de chemin `item_id` est un paramètre de chemin et que `q` n'en est pas un, c'est donc un paramètre de requête.

///

## Conversion des types des paramètres de requête { #query-parameter-type-conversion }

Vous pouvez aussi déclarer des types `bool`, ils seront convertis :

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

Avec ce code, en allant sur :

```
http://127.0.0.1:8000/items/foo?short=1
```

ou

```
http://127.0.0.1:8000/items/foo?short=True
```

ou

```
http://127.0.0.1:8000/items/foo?short=true
```

ou

```
http://127.0.0.1:8000/items/foo?short=on
```

ou

```
http://127.0.0.1:8000/items/foo?short=yes
```

ou n'importe quelle autre variation de casse (tout en majuscules, uniquement la première lettre en majuscule, etc.), votre fonction considérera le paramètre `short` comme ayant une valeur booléenne à `True`. Sinon la valeur sera à `False`.

## Multiples paramètres de chemin et de requête { #multiple-path-and-query-parameters }

Vous pouvez déclarer plusieurs paramètres de chemin et paramètres de requête dans la même fonction, **FastAPI** saura comment les gérer.

Et vous n'avez pas besoin de les déclarer dans un ordre spécifique.

Ils seront détectés par leurs noms :

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Paramètres de requête requis { #required-query-parameters }

Quand vous déclarez une valeur par défaut pour un paramètre qui n'est pas un paramètre de chemin (actuellement, nous n'avons vu que les paramètres de requête), alors ce paramètre n'est pas requis.

Si vous ne voulez pas leur donner de valeur par défaut mais juste les rendre optionnels, utilisez `None` comme valeur par défaut.

Mais si vous voulez rendre un paramètre de requête obligatoire, vous pouvez juste ne pas y affecter de valeur par défaut :

{* ../../docs_src/query_params/tutorial005_py39.py hl[6:7] *}

Ici le paramètre `needy` est un paramètre requis (ou obligatoire) de type `str`.

Si vous ouvrez une URL comme :

```
http://127.0.0.1:8000/items/foo-item
```

... sans ajouter le paramètre requis `needy`, vous verrez une erreur semblable à :

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

La présence de `needy` étant nécessaire, vous auriez besoin de l'insérer dans l'URL :

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

... cela fonctionnerait :

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

Et bien sûr, vous pouvez définir certains paramètres comme requis, certains avec des valeurs par défaut et certains entièrement optionnels :

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

Dans ce cas, on a 3 paramètres de requête :

* `needy`, requis et de type `str`.
* `skip`, un `int` avec comme valeur par défaut `0`.
* `limit`, un `int` optionnel.

/// tip | Astuce

Vous pouvez utiliser les `Enum`s de la même façon qu'avec les [Paramètres de chemin](path-params.md#predefined-values){.internal-link target=_blank}.

///
