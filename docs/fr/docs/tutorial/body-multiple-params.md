# Body - Paramètres multiples { #body-multiple-parameters }

Maintenant que nous avons vu comment utiliser `Path` et `Query`, voyons des usages plus avancés des déclarations de paramètres du corps de la requête.

## Mélanger les paramètres `Path`, `Query` et du corps de la requête { #mix-path-query-and-body-parameters }

Tout d'abord, sachez que vous pouvez mélanger librement les déclarations des paramètres `Path`, `Query` et du corps de la requête, **FastAPI** saura quoi faire.

Et vous pouvez également déclarer des paramètres du corps de la requête comme étant optionnels, en leur assignant une valeur par défaut à `None` :

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | Remarque

Notez que, dans ce cas, l'élément `item` récupéré depuis le corps de la requête est optionnel. Comme sa valeur par défaut est `None`.

///

## Paramètres multiples du corps de la requête { #multiple-body-parameters }

Dans l'exemple précédent, les chemins d'accès attendraient un corps de la requête JSON avec les attributs d'un `Item`, par exemple :

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Mais vous pouvez également déclarer plusieurs paramètres provenant du corps de la requête, par exemple `item` et `user` :

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

Dans ce cas, **FastAPI** détectera qu'il y a plus d'un paramètre du corps de la requête dans la fonction (il y a deux paramètres qui sont des modèles Pydantic).

Il utilisera alors les noms des paramètres comme clés (noms de champs) dans le corps de la requête, et s'attendra à recevoir un corps de la requête semblable à :

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

Notez que, bien que `item` ait été déclaré de la même manière qu'auparavant, il est désormais attendu à l'intérieur du corps de la requête sous la clé `item`.

///

**FastAPI** effectuera la conversion automatique depuis la requête, de sorte que le paramètre `item` reçoive son contenu spécifique, et de même pour `user`.

Il effectuera la validation des données composées, et les documentera ainsi pour le schéma OpenAPI et la documentation automatique.

## Valeurs singulières dans le corps de la requête { #singular-values-in-body }

De la même façon qu'il existe `Query` et `Path` pour définir des données supplémentaires pour les paramètres de requête et de chemin, **FastAPI** fournit un équivalent `Body`.

Par exemple, en étendant le modèle précédent, vous pourriez décider d'avoir une autre clé `importance` dans le même corps de la requête, en plus de `item` et `user`.

Si vous le déclarez tel quel, comme c'est une valeur singulière, **FastAPI** supposera qu'il s'agit d'un paramètre de requête.

Mais vous pouvez indiquer à **FastAPI** de la traiter comme une autre clé du corps de la requête en utilisant `Body` :

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}

Dans ce cas, **FastAPI** s'attendra à un corps de la requête semblable à :

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

Encore une fois, il convertira les types de données, validera, documentera, etc.

## Paramètres multiples du corps de la requête et paramètres de requête { #multiple-body-params-and-query }

Bien entendu, vous pouvez également déclarer des paramètres de requête supplémentaires quand vous en avez besoin, en plus de tout paramètre du corps de la requête.

Comme, par défaut, les valeurs singulières sont interprétées comme des paramètres de requête, vous n'avez pas besoin d'ajouter explicitement `Query`, vous pouvez simplement écrire :

```Python
q: str | None = None
```

Par exemple :

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}

/// info

`Body` possède également les mêmes paramètres supplémentaires de validation et de métadonnées que `Query`, `Path` et d'autres que vous verrez plus tard.

///

## Intégrer un seul paramètre du corps de la requête { #embed-a-single-body-parameter }

Supposons que vous n'ayez qu'un seul paramètre `item` dans le corps de la requête, provenant d'un modèle Pydantic `Item`.

Par défaut, **FastAPI** attendra alors son contenu directement.

Mais si vous voulez qu'il attende un JSON avec une clé `item` contenant le contenu du modèle, comme lorsqu'on déclare des paramètres supplémentaires du corps de la requête, vous pouvez utiliser le paramètre spécial `embed` de `Body` :

```Python
item: Item = Body(embed=True)
```

comme dans :

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}

Dans ce cas **FastAPI** s'attendra à un corps de la requête semblable à :

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

Vous pouvez ajouter plusieurs paramètres du corps de la requête à votre fonction de chemin d'accès, même si une requête ne peut avoir qu'un seul corps de la requête.

Mais **FastAPI** s'en chargera, vous fournira les bonnes données dans votre fonction, et validera et documentera le schéma correct dans le chemin d'accès.

Vous pouvez également déclarer des valeurs singulières à recevoir dans le corps de la requête.

Et vous pouvez indiquer à **FastAPI** d'intégrer le corps de la requête sous une clé même lorsqu'un seul paramètre est déclaré.
