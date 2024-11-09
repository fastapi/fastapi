# Paramètres de requête et validations de chaînes de caractères

**FastAPI** vous permet de déclarer des informations et des validateurs additionnels pour vos paramètres de requêtes.

Commençons avec cette application pour exemple :

{* ../../docs_src/query_params_str_validations/tutorial001.py hl[9] *}

Le paramètre de requête `q` a pour type `Union[str, None]` (ou `str | None` en Python 3.10), signifiant qu'il est de type `str` mais pourrait aussi être égal à `None`, et bien sûr, la valeur par défaut est `None`, donc **FastAPI** saura qu'il n'est pas requis.

/// note

**FastAPI** saura que la valeur de `q` n'est pas requise grâce à la valeur par défaut `= None`.

Le `Union` dans `Union[str, None]` permettra à votre éditeur de vous offrir un meilleur support et de détecter les erreurs.

///

## Validation additionnelle

Nous allons imposer que bien que `q` soit un paramètre optionnel, dès qu'il est fourni, **sa longueur n'excède pas 50 caractères**.

## Importer `Query`

Pour cela, importez d'abord `Query` depuis `fastapi` :

{* ../../docs_src/query_params_str_validations/tutorial002.py hl[3] *}

## Utiliser `Query` comme valeur par défaut

Construisez ensuite la valeur par défaut de votre paramètre avec `Query`, en choisissant 50 comme `max_length` :

{* ../../docs_src/query_params_str_validations/tutorial002.py hl[9] *}

Comme nous devons remplacer la valeur par défaut `None` dans la fonction par `Query()`, nous pouvons maintenant définir la valeur par défaut avec le paramètre `Query(default=None)`, il sert le même objectif qui est de définir cette valeur par défaut.

Donc :

```Python
q: Union[str, None] = Query(default=None)
```

... rend le paramètre optionnel, et est donc équivalent à :

```Python
q: Union[str, None] = None
```

Mais déclare explicitement `q` comme étant un paramètre de requête.

/// info

Gardez à l'esprit que la partie la plus importante pour rendre un paramètre optionnel est :

```Python
= None
```

ou :

```Python
= Query(None)
```

et utilisera ce `None` pour détecter que ce paramètre de requête **n'est pas requis**.

Le `Union[str, None]` est uniquement là pour permettre à votre éditeur un meilleur support.

///

Ensuite, nous pouvons passer d'autres paramètres à `Query`. Dans cet exemple, le paramètre `max_length` qui s'applique aux chaînes de caractères :

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

Cela va valider les données, montrer une erreur claire si ces dernières ne sont pas valides, et documenter le paramètre dans le schéma `OpenAPI` de cette *path operation*.

## Rajouter plus de validation

Vous pouvez aussi rajouter un second paramètre `min_length` :

{* ../../docs_src/query_params_str_validations/tutorial003.py hl[9] *}

## Ajouter des validations par expressions régulières

On peut définir une <abbr title="Une expression régulière, regex ou regexp est une suite de caractères qui définit un pattern de correspondance pour les chaînes de caractères.">expression régulière</abbr> à laquelle le paramètre doit correspondre :

{* ../../docs_src/query_params_str_validations/tutorial004.py hl[10] *}

Cette expression régulière vérifie que la valeur passée comme paramètre :

* `^` : commence avec les caractères qui suivent, avec aucun caractère avant ceux-là.
* `fixedquery` : a pour valeur exacte `fixedquery`.
* `$` : se termine directement ensuite, n'a pas d'autres caractères après `fixedquery`.

Si vous vous sentez perdu avec le concept d'**expression régulière**, pas d'inquiétudes. Il s'agit d'une notion difficile pour beaucoup, et l'on peut déjà réussir à faire beaucoup sans jamais avoir à les manipuler.

Mais si vous décidez d'apprendre à les utiliser, sachez qu'ensuite vous pouvez les utiliser directement dans **FastAPI**.

## Valeurs par défaut

De la même façon que vous pouvez passer `None` comme premier argument pour l'utiliser comme valeur par défaut, vous pouvez passer d'autres valeurs.

Disons que vous déclarez le paramètre `q` comme ayant une longueur minimale de `3`, et une valeur par défaut étant `"fixedquery"` :

{* ../../docs_src/query_params_str_validations/tutorial005.py hl[7] *}

/// note | Rappel

Avoir une valeur par défaut rend le paramètre optionnel.

///

## Rendre ce paramètre requis

Quand on ne déclare ni validation, ni métadonnée, on peut rendre le paramètre `q` requis en ne lui déclarant juste aucune valeur par défaut :

```Python
q: str
```

à la place de :

```Python
q: Union[str, None] = None
```

Mais maintenant, on déclare `q` avec `Query`, comme ceci :

```Python
q: Union[str, None] = Query(default=None, min_length=3)
```

Donc pour déclarer une valeur comme requise tout en utilisant `Query`, il faut utiliser `...` comme premier argument :

{* ../../docs_src/query_params_str_validations/tutorial006.py hl[7] *}

/// info

Si vous n'avez jamais vu ce `...` auparavant : c'est une des constantes natives de Python <a href="https://docs.python.org/fr/3/library/constants.html#Ellipsis" class="external-link" target="_blank">appelée "Ellipsis"</a>.

///

Cela indiquera à **FastAPI** que la présence de ce paramètre est obligatoire.

## Liste de paramètres / valeurs multiples via Query

Quand on définit un paramètre de requête explicitement avec `Query` on peut aussi déclarer qu'il reçoit une liste de valeur, ou des "valeurs multiples".

Par exemple, pour déclarer un paramètre de requête `q` qui peut apparaître plusieurs fois dans une URL, on écrit :

{* ../../docs_src/query_params_str_validations/tutorial011.py hl[9] *}

Ce qui fait qu'avec une URL comme :

```
http://localhost:8000/items/?q=foo&q=bar
```

vous recevriez les valeurs des multiples paramètres de requête `q` (`foo` et `bar`) dans une `list` Python au sein de votre fonction de **path operation**, dans le paramètre de fonction `q`.

Donc la réponse de cette URL serait :

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | Astuce

Pour déclarer un paramètre de requête de type `list`, comme dans l'exemple ci-dessus, il faut explicitement utiliser `Query`, sinon cela sera interprété comme faisant partie du corps de la requête.

///

La documentation sera donc mise à jour automatiquement pour autoriser plusieurs valeurs :

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Combiner liste de paramètres et valeurs par défaut

Et l'on peut aussi définir une liste de valeurs par défaut si aucune n'est fournie :

{* ../../docs_src/query_params_str_validations/tutorial012.py hl[9] *}

Si vous allez à :

```
http://localhost:8000/items/
```

la valeur par défaut de `q` sera : `["foo", "bar"]`

et la réponse sera :

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Utiliser `list`

Il est aussi possible d'utiliser directement `list` plutôt que `List[str]` :

{* ../../docs_src/query_params_str_validations/tutorial013.py hl[7] *}

/// note

Dans ce cas-là, **FastAPI** ne vérifiera pas le contenu de la liste.

Par exemple, `List[int]` vérifiera (et documentera) que la liste est bien entièrement composée d'entiers. Alors qu'un simple `list` ne ferait pas cette vérification.

///

## Déclarer des métadonnées supplémentaires

On peut aussi ajouter plus d'informations sur le paramètre.

Ces informations seront incluses dans le schéma `OpenAPI` généré et utilisées par la documentation interactive ou les outils externes utilisés.

/// note

Gardez en tête que les outils externes utilisés ne supportent pas forcément tous parfaitement OpenAPI.

Il se peut donc que certains d'entre eux n'utilisent pas toutes les métadonnées que vous avez déclarées pour le moment, bien que dans la plupart des cas, les fonctionnalités manquantes ont prévu d'être implémentées.

///

Vous pouvez ajouter un `title` :

{* ../../docs_src/query_params_str_validations/tutorial007.py hl[10] *}

Et une `description` :

{* ../../docs_src/query_params_str_validations/tutorial008.py hl[13] *}

## Alias de paramètres

Imaginez que vous vouliez que votre paramètre se nomme `item-query`.

Comme dans la requête :

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Mais `item-query` n'est pas un nom de variable valide en Python.

Le nom le plus proche serait `item_query`.

Mais vous avez vraiment envie que ce soit exactement `item-query`...

Pour cela vous pouvez déclarer un `alias`, et cet alias est ce qui sera utilisé pour trouver la valeur du paramètre :

{* ../../docs_src/query_params_str_validations/tutorial009.py hl[9] *}

## Déprécier des paramètres

Disons que vous ne vouliez plus utiliser ce paramètre désormais.

Il faut qu'il continue à exister pendant un certain temps car vos clients l'utilisent, mais vous voulez que la documentation mentionne clairement que ce paramètre est <abbr title="obsolète, recommandé de ne pas l'utiliser">déprécié</abbr>.

On utilise alors l'argument `deprecated=True` de `Query` :

{* ../../docs_src/query_params_str_validations/tutorial010.py hl[18] *}

La documentation le présentera comme il suit :

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Pour résumer

Il est possible d'ajouter des validateurs et métadonnées pour vos paramètres.

Validateurs et métadonnées génériques:

* `alias`
* `title`
* `description`
* `deprecated`

Validateurs spécifiques aux chaînes de caractères :

* `min_length`
* `max_length`
* `regex`

Parmi ces exemples, vous avez pu voir comment déclarer des validateurs pour les chaînes de caractères.

Dans les prochains chapitres, vous verrez comment déclarer des validateurs pour d'autres types, comme les nombres.
