# Paramètres de requête { #query-parameters }

Quand vous déclarez d'autres paramètres de fonction qui ne font pas partie des paramètres de chemin, ils sont automatiquement interprétés comme des paramètres de « requête ».

{* ../../docs_src/query_params/tutorial001_py39.py hl[9] *}

La requête est l'ensemble des paires clé-valeur qui suivent le `?` dans une URL, séparées par des caractères `&`.

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

* Support de l'éditeur (évidemment)
* <abbr title="converting the string that comes from an HTTP request into Python data - conversion de la chaîne de caractères venant d'une requête HTTP en données Python">« parsing »</abbr> des données
* Validation des données
* Documentation automatique

## Valeurs par défaut { #defaults }

Comme les paramètres de requête ne constituent pas une partie fixe d'un chemin, ils peuvent être optionnels et peuvent avoir des valeurs par défaut.

Dans l'exemple ci-dessus, ils ont des valeurs par défaut `skip=0` et `limit=10`.

Ainsi, aller à l'URL :

```
http://127.0.0.1:8000/items/
```

serait équivalent à aller à :

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Mais si vous allez à, par exemple :

```
http://127.0.0.1:8000/items/?skip=20
```

Les valeurs des paramètres dans votre fonction seront :

* `skip=20` : parce que vous l'avez défini dans l'URL
* `limit=10` : parce que c'était la valeur par défaut

## Paramètres optionnels { #optional-parameters }

De la même façon, vous pouvez déclarer des paramètres de requête optionnels, en définissant leur valeur par défaut à `None` :

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

Dans ce cas, le paramètre de fonction `q` sera optionnel, et aura `None` comme valeur par défaut.

/// check | Vérifications

Notez également que **FastAPI** est suffisamment intelligent pour remarquer que le paramètre de chemin `item_id` est un paramètre de chemin et que `q` n'en est pas un, donc c'est un paramètre de requête.

///

## Conversion du type des paramètres de requête { #query-parameter-type-conversion }

Vous pouvez aussi déclarer des types `bool`, et ils seront convertis :

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

Dans ce cas, si vous allez à :

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

ou toute autre variation de casse (majuscules, première lettre en majuscule, etc.), votre fonction verra le paramètre `short` avec une valeur `bool` de `True`. Sinon, `False`.


## Paramètres de chemin et de requête multiples { #multiple-path-and-query-parameters }

Vous pouvez déclarer plusieurs paramètres de chemin et paramètres de requête en même temps, **FastAPI** sait lesquels sont lesquels.

Et vous n'avez pas besoin de les déclarer dans un ordre spécifique.

Ils seront détectés par leur nom :

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Paramètres de requête requis { #required-query-parameters }

Lorsque vous déclarez une valeur par défaut pour des paramètres qui ne sont pas des paramètres de chemin (pour l'instant, nous n'avons vu que des paramètres de requête), alors ils ne sont pas requis.

Si vous ne voulez pas ajouter une valeur spécifique mais juste le rendre optionnel, définissez la valeur par défaut sur `None`.

Mais lorsque vous voulez rendre un paramètre de requête requis, vous pouvez simplement ne pas déclarer de valeur par défaut :

{* ../../docs_src/query_params/tutorial005_py39.py hl[6:7] *}

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

Vous pouvez aussi utiliser des `Enum`s de la même façon qu'avec les [Paramètres de chemin](path-params.md#predefined-values){.internal-link target=_blank}.

///
