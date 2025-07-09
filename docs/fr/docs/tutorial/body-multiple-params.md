# Body - Paramètres multiples

Maintenant que nous avons vu comment manipuler `Path` et `Query`, voyons comment faire pour le corps d'une requête, communément désigné par le terme anglais "body".

## Mélanger les paramètres `Path`, `Query` et body

Tout d'abord, sachez que vous pouvez mélanger les déclarations des paramètres `Path`, `Query` et body, **FastAPI** saura quoi faire.

Vous pouvez également déclarer des paramètres body comme étant optionnels, en leur assignant une valeur par défaut à `None` :

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note

Notez que, dans ce cas, le paramètre `item` provenant du `Body` est optionnel (sa valeur par défaut est `None`).

///

## Paramètres multiples du body

Dans l'exemple précédent, les opérations de routage attendaient un body JSON avec les attributs d'un `Item`, par exemple :

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Mais vous pouvez également déclarer plusieurs paramètres provenant de body, par exemple `item` et `user` simultanément :

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}

Dans ce cas, **FastAPI** détectera qu'il y a plus d'un paramètre dans le body (chacun correspondant à un modèle Pydantic).

Il utilisera alors les noms des paramètres comme clés, et s'attendra à recevoir quelque chose de semblable à :

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

/// note

"Notez que, bien que nous ayons déclaré le paramètre `item` de la même manière que précédemment, il est maintenant associé à la clé `item` dans le corps de la requête."`.

///

**FastAPI** effectue la conversion de la requête de façon transparente, de sorte que les objets `item` et `user` se trouvent correctement définis.

Il effectue également la validation des données (même imbriquées les unes dans les autres), et permet de les documenter correctement (schéma OpenAPI et documentation auto-générée).

## Valeurs scalaires dans le body

De la même façon qu'il existe `Query` et `Path` pour définir des données supplémentaires pour les paramètres query et path, **FastAPI** fournit un équivalent `Body`.

Par exemple, en étendant le modèle précédent, vous pouvez vouloir ajouter un paramètre `importance` dans le même body, en plus des paramètres `item` et `user`.

Si vous le déclarez tel quel, comme c'est une valeur [scalaire](https://docs.github.com/fr/graphql/reference/scalars), **FastAPI** supposera qu'il s'agit d'un paramètre de requête (`Query`).

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

Encore une fois, cela convertira les types de données, les validera, permettra de générer la documentation, etc...

## Paramètres multiples body et query

Bien entendu, vous pouvez déclarer autant de paramètres que vous le souhaitez, en plus des paramètres body déjà déclarés.

Par défaut, les valeurs [scalaires](https://docs.github.com/fr/graphql/reference/scalars) sont interprétées comme des paramètres query, donc inutile d'ajouter explicitement `Query`. Vous pouvez juste écrire :

```Python
q: Union[str, None] = None
```

Ou bien, en Python 3.10 et supérieur :

```Python
q: str | None = None
```

Par exemple :

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[27] *}

/// info

`Body` possède les mêmes paramètres de validation additionnels et de gestion des métadonnées que `Query` et `Path`, ainsi que d'autres que nous verrons plus tard.

///

## Inclure un paramètre imbriqué dans le body

Disons que vous avez seulement un paramètre `item` dans le body, correspondant à un modèle Pydantic `Item`.

Par défaut, **FastAPI** attendra sa déclaration directement dans le body.

Cependant, si vous souhaitez qu'il interprête correctement un JSON avec une clé `item` associée au contenu du modèle, comme cela serait le cas si vous déclariez des paramètres body additionnels, vous pouvez utiliser le paramètre spécial `embed` de `Body` :

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

## Pour résumer

Vous pouvez ajouter plusieurs paramètres body dans votre fonction de routage, même si une requête ne peut avoir qu'un seul body.

Cependant, **FastAPI** se chargera de faire opérer sa magie, afin de toujours fournir à votre fonction des données correctes, les validera et documentera le schéma associé.

Vous pouvez également déclarer des valeurs [scalaires](https://docs.github.com/fr/graphql/reference/scalars) à recevoir dans le body.

Et vous pouvez indiquer à **FastAPI** d'inclure le body dans une autre variable, même lorsqu'un seul paramètre est déclaré.
