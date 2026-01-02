# Body - Paramètres multiples { #body-multiple-parameters }

Maintenant que nous avons vu comment utiliser `Path` et `Query`, voyons des utilisations plus avancées des déclarations du corps de la requête.

## Mélanger les paramètres `Path`, `Query` et body { #mix-path-query-and-body-parameters }

Tout d'abord, sachez que vous pouvez mélanger les déclarations des paramètres `Path`, `Query` et body, **FastAPI** saura quoi faire.

Vous pouvez également déclarer des paramètres body comme étant optionnels, en leur assignant une valeur par défaut à `None` :

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | Remarque

Notez que, dans ce cas, le paramètre `item` provenant du body est optionnel. Sa valeur par défaut est `None`.

///

## Paramètres multiples du body { #multiple-body-parameters }

Dans l'exemple précédent, les *opérations de chemin* attendaient un body JSON avec les attributs d'un `Item`, par exemple :

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Mais vous pouvez également déclarer plusieurs paramètres provenant de body, par exemple `item` et `user` :

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

Dans ce cas, **FastAPI** détectera qu'il y a plus d'un paramètre body dans la fonction (il y a deux paramètres qui sont des modèles Pydantic).

Il utilisera alors les noms des paramètres comme clés (noms de champs) dans le body, et s'attendra à recevoir un body semblable à :

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

Notez que, bien que `item` ait été déclaré de la même manière qu'auparavant, il est maintenant attendu dans le body sous la clé `item`.

///

**FastAPI** effectue la conversion automatique à partir de la requête, de sorte que le paramètre `item` reçoive son contenu spécifique, et de même pour `user`.

Il effectuera la validation des données composées et les documentera ainsi dans le schéma OpenAPI et la documentation automatique.

## Valeurs scalaires dans le body { #singular-values-in-body }

De la même façon qu'il existe `Query` et `Path` pour définir des données supplémentaires pour les paramètres query et path, **FastAPI** fournit un équivalent `Body`.

Par exemple, en étendant le modèle précédent, vous pouvez vouloir ajouter un paramètre `importance` dans le même body, en plus des paramètres `item` et `user`.

Si vous le déclarez tel quel, comme c'est une valeur scalaire, **FastAPI** supposera qu'il s'agit d'un paramètre de requête.

Mais vous pouvez indiquer à **FastAPI** de la traiter comme une variable de body en utilisant `Body` :

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}

Dans ce cas, **FastAPI** s'attendra à un body semblable à :

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

Encore une fois, cela convertira les types de données, les validera, permettra de générer la documentation, etc.

## Paramètres multiples body et query { #multiple-body-params-and-query }

Bien entendu, vous pouvez également déclarer des paramètres de requête supplémentaires quand vous en avez besoin, en plus de tout paramètre body.

Comme, par défaut, les valeurs scalaires sont interprétées comme des paramètres query, vous n'avez pas besoin d'ajouter explicitement `Query`. Vous pouvez simplement écrire :

```Python
q: Union[str, None] = None
```

Ou bien, en Python 3.10 et supérieur :

```Python
q: str | None = None
```

Par exemple :

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}

/// info

`Body` possède les mêmes paramètres de validation additionnels et de gestion des métadonnées que `Query` et `Path`, ainsi que d'autres que nous verrons plus tard.

///

## Inclure un seul paramètre body { #embed-a-single-body-parameter }

Disons que vous avez seulement un paramètre `item` dans le body, correspondant à un modèle Pydantic `Item`.

Par défaut, **FastAPI** attendra sa déclaration directement dans le body.

Cependant, si vous souhaitez qu'il interprète correctement un JSON avec une clé `item` associée au contenu du modèle, comme cela serait le cas si vous déclariez des paramètres body additionnels, vous pouvez utiliser le paramètre spécial `embed` de `Body` :

```Python
item: Item = Body(embed=True)
```

Voici un exemple complet :

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}

Dans ce cas **FastAPI** attendra un body semblable à :

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

## Pour résumer { #recap }

Vous pouvez ajouter plusieurs paramètres body à votre *fonction de chemin*, même si une requête ne peut avoir qu'un seul body.

Cependant, **FastAPI** s'en chargera, vous fournira les bonnes données dans votre fonction, et validera et documentera le schéma correct dans l'*opération de chemin*.

Vous pouvez également déclarer des valeurs scalaires à recevoir dans le body.

Et vous pouvez indiquer à **FastAPI** d'inclure le body dans une clé, même lorsqu'un seul paramètre est déclaré.
