# Paramètres de requête { #query-parameters }

Quand vous déclarez d'autres paramètres de fonction qui ne font pas partie des paramètres de chemin, ils sont automatiquement interprétés comme des paramètres de « query ».

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

La query est l'ensemble des paires clé-valeur placées après le `?` dans une URL, séparées par des caractères `&`.

Par exemple, dans l'URL :

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

... les paramètres de requête sont :

* `skip` : avec une valeur de `0`
* `limit` : avec une valeur de `10`

Comme ils font partie de l'URL, ce sont « naturellement » des chaînes de caractères.

Mais lorsque vous les déclarez avec des types Python (dans l'exemple ci-dessus, en tant que `int`), ils sont convertis vers ce type et validés par rapport à celui-ci.

Tous les mêmes processus qui s'appliquaient aux paramètres de chemin s'appliquent aussi aux paramètres de requête :

* Prise en charge de l'éditeur (évidemment)
* <dfn title="conversion de la chaîne provenant d'une requête HTTP en données Python">« parsing »</dfn> des données
* Validation des données
* Documentation automatique

## Valeurs par défaut { #defaults }

Comme les paramètres de requête ne sont pas une partie fixe d'un chemin, ils peuvent être optionnels et avoir des valeurs par défaut.

Dans l'exemple ci-dessus, ils ont des valeurs par défaut `skip=0` et `limit=10`.

Donc, accéder à l'URL :

```
http://127.0.0.1:8000/items/
```

serait équivalent à accéder à :

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Mais si vous accédez, par exemple, à :

```
http://127.0.0.1:8000/items/?skip=20
```

Les valeurs des paramètres dans votre fonction seront :

* `skip=20` : car vous l'avez défini dans l'URL
* `limit=10` : car c'était la valeur par défaut

## Paramètres optionnels { #optional-parameters }

De la même façon, vous pouvez déclarer des paramètres de requête optionnels, en définissant leur valeur par défaut à `None` :

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

Dans ce cas, le paramètre de fonction `q` sera optionnel et vaudra `None` par défaut.

/// check | Vérifications

Notez également que **FastAPI** est suffisamment intelligent pour remarquer que le paramètre de chemin `item_id` est un paramètre de chemin et que `q` ne l'est pas, c'est donc un paramètre de requête.

///

## Conversion des types des paramètres de requête { #query-parameter-type-conversion }

Vous pouvez aussi déclarer des types `bool`, ils seront convertis :

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

Dans ce cas, si vous allez sur :

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

ou n'importe quelle autre variation de casse (tout en majuscules, uniquement la première lettre en majuscule, etc.), votre fonction verra le paramètre `short` avec une valeur `bool` à `True`. Sinon la valeur sera à `False`.

## Multiples paramètres de chemin et de requête { #multiple-path-and-query-parameters }

Vous pouvez déclarer plusieurs paramètres de chemin et paramètres de requête en même temps, FastAPI sait lequel est lequel.

Et vous n'avez pas besoin de les déclarer dans un ordre spécifique.

Ils seront détectés par leur nom :

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Paramètres de requête requis { #required-query-parameters }

Quand vous déclarez une valeur par défaut pour des paramètres qui ne sont pas des paramètres de chemin (pour l'instant, nous n'avons vu que les paramètres de requête), alors ils ne sont pas requis.

Si vous ne voulez pas leur donner de valeur spécifique mais simplement les rendre optionnels, définissez la valeur par défaut à `None`.

Mais si vous voulez rendre un paramètre de requête obligatoire, vous pouvez simplement ne déclarer aucune valeur par défaut :

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

Ici, le paramètre de requête `needy` est un paramètre de requête requis de type `str`.

Si vous ouvrez dans votre navigateur une URL comme :

```
http://127.0.0.1:8000/items/foo-item
```

... sans ajouter le paramètre requis `needy`, vous verrez une erreur comme :

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

Comme `needy` est un paramètre requis, vous devez le définir dans l'URL :

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

Et bien sûr, vous pouvez définir certains paramètres comme requis, certains avec une valeur par défaut et certains entièrement optionnels :

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

Dans ce cas, il y a 3 paramètres de requête :

* `needy`, un `str` requis.
* `skip`, un `int` avec une valeur par défaut de `0`.
* `limit`, un `int` optionnel.

/// tip | Astuce

Vous pourriez aussi utiliser des `Enum`s de la même façon qu'avec les [Paramètres de chemin](path-params.md#predefined-values){.internal-link target=_blank}.

///
