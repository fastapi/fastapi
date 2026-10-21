# Utiliser des classes comme dépendances { #classes-as-dependencies }

Avant d'aller plus loin dans le système d'**Injection de dépendances**, mettons à niveau l'exemple précédent.

## Un `dict` de l'exemple précédent { #a-dict-from-the-previous-example }

Dans l'exemple précédent, nous renvoyions un `dict` depuis notre dépendance (« dependable ») :

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

Mais nous recevons alors un `dict` dans le paramètre `commons` de la fonction de chemin d'accès.

Et les éditeurs ne peuvent pas apporter beaucoup d'assistance (comme l'autocomplétion) pour les `dict`, car ils ne peuvent pas connaître leurs clés ni les types de valeurs.

Nous pouvons faire mieux ...

## Ce qui fait d'un objet une dépendance { #what-makes-a-dependency }

Jusqu'à présent, vous avez vu des dépendances déclarées sous forme de fonctions.

Mais ce n'est pas la seule manière de déclarer des dépendances (même si c'est probablement la plus courante).

L'élément clé est qu'une dépendance doit être un « callable ».

Un « callable » en Python est tout ce que Python peut « appeler » comme une fonction.

Ainsi, si vous avez un objet `something` (qui n'est peut‑être pas une fonction) et que vous pouvez « l'appeler » (l'exécuter) comme :

```Python
something()
```

ou

```Python
something(some_argument, some_keyword_argument="foo")
```

alors c'est un « callable ».

## Utiliser des classes comme dépendances { #classes-as-dependencies_1 }

Vous remarquerez que pour créer une instance d'une classe Python, vous utilisez la même syntaxe.

Par exemple :

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

Dans ce cas, `fluffy` est une instance de la classe `Cat`.

Et pour créer `fluffy`, vous « appelez » `Cat`.

Donc, une classe Python est aussi un « callable ».

Ainsi, avec **FastAPI**, vous pouvez utiliser une classe Python comme dépendance.

Ce que **FastAPI** vérifie réellement, c'est qu'il s'agit d'un « callable » (fonction, classe ou autre) et des paramètres qui y sont définis.

Si vous passez un « callable » comme dépendance dans **FastAPI**, il en analysera les paramètres et les traitera de la même manière que les paramètres d'une fonction de chemin d'accès. Y compris les sous‑dépendances.

Cela s'applique également aux callables sans aucun paramètre. Comme ce serait le cas pour des fonctions de chemin d'accès sans paramètres.

Nous pouvons alors remplacer la dépendance « dependable » `common_parameters` ci‑dessus par la classe `CommonQueryParams` :

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

Faites attention à la méthode `__init__` utilisée pour créer l'instance de la classe :

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

... il a les mêmes paramètres que notre précédent `common_parameters` :

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

Ce sont ces paramètres que **FastAPI** utilisera pour « résoudre » la dépendance.

Dans les deux cas, il y aura :

- Un paramètre de requête optionnel `q` qui est un `str`.
- Un paramètre de requête `skip` qui est un `int`, avec une valeur par défaut de `0`.
- Un paramètre de requête `limit` qui est un `int`, avec une valeur par défaut de `100`.

Dans les deux cas, les données seront converties, validées, documentées dans le schéma OpenAPI, etc.

## Utiliser { #use-it }

Vous pouvez maintenant déclarer votre dépendance en utilisant cette classe.

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** appelle la classe `CommonQueryParams`. Cela crée une « instance » de cette classe et l'instance sera passée comme paramètre `commons` à votre fonction.

## Annotation de type vs `Depends` { #type-annotation-vs-depends }

Remarquez que nous écrivons `CommonQueryParams` deux fois dans le code ci‑dessus :

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ sans Annotated

/// tip | Astuce

Privilégiez la version avec `Annotated` si possible.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

Le dernier `CommonQueryParams`, dans :

```Python
... Depends(CommonQueryParams)
```

... est ce que **FastAPI** utilisera réellement pour savoir quelle est la dépendance.

C'est à partir de celui‑ci que FastAPI extraira les paramètres déclarés et c'est ce que FastAPI appellera effectivement.

---

Dans ce cas, le premier `CommonQueryParams`, dans :

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.10+ sans Annotated

/// tip | Astuce

Privilégiez la version avec `Annotated` si possible.

///

```Python
commons: CommonQueryParams ...
```

////

... n'a aucune signification particulière pour **FastAPI**. FastAPI ne l'utilisera pas pour la conversion des données, la validation, etc. (car il utilise `Depends(CommonQueryParams)` pour cela).

Vous pourriez en fait écrire simplement :

//// tab | Python 3.10+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ sans Annotated

/// tip | Astuce

Privilégiez la version avec `Annotated` si possible.

///

```Python
commons = Depends(CommonQueryParams)
```

////

... comme dans :

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

Mais il est recommandé de déclarer le type ; ainsi, votre éditeur saura ce qui sera passé comme paramètre `commons`, et pourra vous aider avec l'autocomplétion, les vérifications de type, etc. :

<img src="/img/tutorial/dependencies/image02.png">

## Raccourci { #shortcut }

Mais vous voyez qu'il y a ici de la duplication de code : nous écrivons `CommonQueryParams` deux fois :

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ sans Annotated

/// tip | Astuce

Privilégiez la version avec `Annotated` si possible.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** fournit un raccourci pour ces cas, lorsque la dépendance est spécifiquement une classe que **FastAPI** va « appeler » pour créer une instance de la classe elle‑même.

Pour ces cas précis, vous pouvez faire ce qui suit :

Au lieu d'écrire :

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ sans Annotated

/// tip | Astuce

Privilégiez la version avec `Annotated` si possible.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

... vous écrivez :

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.10+ sans Annotated

/// tip | Astuce

Privilégiez la version avec `Annotated` si possible.

///

```Python
commons: CommonQueryParams = Depends()
```

////

Vous déclarez la dépendance comme type du paramètre et vous utilisez `Depends()` sans aucun paramètre, au lieu d'avoir à réécrire la classe entière à l'intérieur de `Depends(CommonQueryParams)`.

Le même exemple ressemblerait alors à ceci :

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

... et **FastAPI** saura quoi faire.

/// tip | Astuce

Si cela vous semble plus déroutant qu'utile, ignorez‑le, vous n'en avez pas besoin.

Ce n'est qu'un raccourci. Parce que **FastAPI** tient à vous aider à minimiser la duplication de code.

///
