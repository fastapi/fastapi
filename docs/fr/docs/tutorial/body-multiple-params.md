# Body - Paramètres multiples { #body-multiple-parameters }

Maintenant que nous avons vu comment utiliser `Path` et `Query`, voyons des usages plus avancés des déclarations du corps de la requête.

## Mélanger les paramètres `Path`, `Query` et body { #mix-path-query-and-body-parameters }

Tout d'abord, bien entendu, vous pouvez mélanger librement les déclarations de paramètres `Path`, `Query` et du corps de la requête, et **FastAPI** saura quoi faire.

Et vous pouvez également déclarer des paramètres body comme étant optionnels, en définissant la valeur par défaut à `None` :

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | Remarque

Notez que, dans ce cas, le `item` qui serait pris depuis le corps est optionnel, car il a une valeur par défaut à `None`.

///

## Paramètres multiples du body { #multiple-body-parameters }

Dans l'exemple précédent, les *chemins d'accès* s'attendraient à un corps JSON avec les attributs d'un `Item`, comme :

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Mais vous pouvez aussi déclarer plusieurs paramètres body, par ex. `item` et `user` :

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}


Dans ce cas, **FastAPI** remarquera qu'il y a plus d'un paramètre body dans la fonction (il y a deux paramètres qui sont des modèles Pydantic).

Il utilisera alors les noms des paramètres comme clés (noms de champs) dans le corps, et s'attendra à un corps comme :

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | Remarque

Notez que, même si le `item` a été déclaré de la même manière qu'avant, il est maintenant attendu dans le corps avec une clé `item`.

///

**FastAPI** fera la conversion automatique à partir de la requête, de sorte que le paramètre `item` reçoive son contenu spécifique, et de même pour `user`.

Il effectuera la validation des données composées, et les documentera ainsi pour le schéma OpenAPI et les documents automatiques.

## Valeurs scalaires dans le body { #singular-values-in-body }

De la même manière qu'il existe `Query` et `Path` pour définir des données supplémentaires pour les paramètres de requête et de chemin, **FastAPI** fournit un équivalent `Body`.

Par exemple, en étendant le modèle précédent, vous pourriez décider que vous voulez une autre clé `importance` dans le même corps, en plus de `item` et `user`.

Si vous le déclarez tel quel, comme c'est une valeur scalaire, **FastAPI** supposera qu'il s'agit d'un paramètre de requête.

Mais vous pouvez indiquer à **FastAPI** de la traiter comme une autre clé dans le corps en utilisant `Body` :

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}


Dans ce cas, **FastAPI** s'attendra à un corps comme :

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

Là encore, il convertira les types de données, validera, documentera, etc.

## Plusieurs paramètres body et query { #multiple-body-params-and-query }

Bien entendu, vous pouvez aussi déclarer des paramètres de requête supplémentaires dès que vous en avez besoin, en plus de n'importe quels paramètres body.

Comme, par défaut, les valeurs scalaires sont interprétées comme des paramètres de requête, vous n'avez pas besoin d'ajouter explicitement un `Query`, vous pouvez simplement faire :

```Python
q: str | None = None
```

Ou en Python 3.10 et supérieur :

```Python
q: Union[str, None] = None
```

Par exemple :

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}


/// info | info

`Body` possède aussi les mêmes paramètres supplémentaires de validation et de métadonnées que `Query`, `Path` et d'autres que vous verrez plus tard.

///

## Inclure un seul paramètre body { #embed-a-single-body-parameter }

Disons que vous n'avez qu'un seul paramètre body `item` issu d'un modèle Pydantic `Item`.

Par défaut, **FastAPI** s'attendra alors à son corps directement.

Mais si vous voulez qu'il s'attende à un JSON avec une clé `item` et, à l'intérieur, le contenu du modèle, comme il le fait lorsque vous déclarez des paramètres body supplémentaires, vous pouvez utiliser le paramètre spécial `embed` de `Body` :

```Python
item: Item = Body(embed=True)
```

comme dans :

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}


Dans ce cas **FastAPI** s'attendra à un corps comme :

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

au lieu de :

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Récapitulatif { #recap }

Vous pouvez ajouter plusieurs paramètres body à votre *fonction de chemin d'accès*, même si une requête ne peut avoir qu'un seul corps.

Mais **FastAPI** le gérera, vous donnera les données correctes dans votre fonction, et validera et documentera le schéma correct dans le *chemin d'accès*.

Vous pouvez aussi déclarer des valeurs scalaires à recevoir dans le corps.

Et vous pouvez indiquer à **FastAPI** d'inclure le corps dans une clé même lorsqu'il n'y a qu'un seul paramètre déclaré.
