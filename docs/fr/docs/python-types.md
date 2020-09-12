# Python Types Introduction

**Python 3.6+** intègre le support des "type hints" optionnels.

Ces **"type hints"** correspondent à une nouvelle syntaxe (depuis Python 3.6+) qui permet de déclarer le <abbr title="par exemple: str, int, float, bool">type</abbr> d'une variable.

En déclarant les types de vos variables, les éditeurs de code et outils vous offrent un meilleur support.

Il s'agit juste d'un **rapide tutoriel / rafraîchissement** au sujet des type hints de Python. Il couvre seulement le minimum nécessaire pour les utiliser avec **FastAPI**... ce qui correspond à très peu de choses.

**FastAPI** est entièrement basé sur les Python type qui lui offrent beaucoup d'avantages et de bénéfices.

Et même si vous n'utilisez jamais **FastAPI**, vous devriez en tirer quelques avantages en en apprenant un peu à leur sujet.

!!! note
    Si vous êtes un expert Python, et que vous connaissez déjà tout à propos des Python type, passez au prochain chapitre.

## Motivation

Commençons avec un exemple simple :

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

En appelant ce programme, on obtient la sortie suivante :

```
John Doe
```

La fonction effectue les points suivants :

* Prend un `first_name` et un `last_name`.
* Convertit la première lettre des contenus de chaque variable et les passe en majuscule à l'aide de `title()`.
* <abbr title="Mets des contenus de variables dans un seul et même ensemble. Utilise les contenus les uns après les autres.">Concatène</abbr> les contenus des 2 variables avec un espace entre les 2.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Modifions le programme

Il s'agit d'un programme très simple.

Mais maintenant, imaginez que vous deviez l'écrire en partant du début.

A un certain moment vous aimeriez commencer la définition de la fonction, vous avez déjà les paramètres prêts... 

Mais, vous devez appeler "la méthode qui convertit la première lettre en majuscule".

Est-ce que c'est `upper` ? Ou alors `uppercase` ? A moins que cela soit `first_uppercase`? Ou qui sait `capitalize`?

Puis, vous essayez avec un autre outil : un éditeur de code avec autocompletion.

Vous tapez le premier paramètre de la fonction, `first_name`, puis un point (`.`) et appuyez ensuite sur `Ctrl+Espace` pour déclencher la completion.

Mais, malheureusement, vous n'obtenez rien d'utile :

<img src="/img/python-types/image01.png">

### Ajouter des types

Modifions une ligne de la précédente version.

Nous allons en modifier un morceau, les paramètres de la fonction, de :

```Python
    first_name, last_name
```

à :

```Python
    first_name: str, last_name: str
```

C'est tout !

Ce sont eux les "type hints" :

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

Ceci n'est pas la même chose que de déclarer des valeurs par défaut comme cela pourrait l'être avec :

```Python
    first_name="john", last_name="doe"
```

C'est une chose différente.

Nous utilisons les 2 points (`:`), mais pas le signe d'égalité (`=`).

Et ajouter des type hints ne change rien à ce qui doit arriver par rapport à ce qui devrait arriver sans eux. C'est transparent.

Maintenant, imaginez que vous êtes encore au milieu de la création de cette fonction, mais avec des type hints.

Au même endroit, vous essayez de déclencher l'autocompletion avec `Ctrl+Espace` et vous voyez :

<img src="/img/python-types/image02.png">

Avec cela, vous pouvez scroller, en regardant les options, jusqu'à ce que vous trouviez la bonne méthode qui fait 'tilt' :

<img src="/img/python-types/image03.png">

## Encore plus de motivation

Analysez cette fonction, elle a déjà des type hints :

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Parce que l'éditeur connait les types des variables, vous n'obtenez pas seulement l'autocompletion, vous obtenez également les analyses d'erreurs :

<img src="/img/python-types/image04.png">

Maintenant vous savez que vous devez corriger quelque chose : convertir `age` en chaîne de caractères avec `str(age)` :

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Déclarer les types

Vous venez juste de voir l'emplacement principal pour déclarer des type hints : les paramètres de fonction.

C'est également l'emplacement principal que vous devriez utiliser pour les définir avec **FastAPI**.

### Des types simple

Vous pouvez déclarer tous les types standard de Python, et pas seulement les `str`.

Par exemple, vous pouvez utiliser :

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Des types génériques avec des types paramètres

Il existe des structures de données qui contiennent d'autres valeurs, comme les `dict`, `list`, `set` et les `tuple`.
Et les valeurs internes peuvent avoir leur propre type également.

Pour déclarer ces types et les types internes, vous pouvez utiliser le module Python standard `typing`.

Ce module existe tout spécialement pour offrir le support relatif aux type hints.

#### `List`

Définissons une variable qui sera une `list` de `str`.

A partir de `typing`, importez `List` (avec un `L` majuscule) :

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial006.py!}
```

Déclarez la variable avec la même syntaxe utilisant les 2 points (`:`).

Comme type, saisissez `List`.

Comme `List` est un type qui contient d'autres types internes, vous devez les mettre entre crochets :

```Python hl_lines="4"
{!../../../docs_src/python_types/tutorial006.py!}
```

!!! astuce
    Les types internes placés entre crochets sont appelés "type parameters".

    Dans ce cas, `str` est le "type parameter" passé à la `List`.

Traduction : "la variable `items` est une `list`, et chacun des éléments de cette liste est un `str`".

Grâce à cela, votre éditeur de code vous fournira de l'aide même sur les éléments contenus dans la liste :

<img src="/img/python-types/image05.png">

Sans les types, c'est presque impossible à faire.

Notez que la variable `item` est un des éléments contenus dans la liste `items`.

Encore plus fort : l'éditeur de code sait que `item` est de type `str` et fournit donc du support pour cela.

#### `Tuple` et `Set`

Vous pourriez en faire de même pour déclarer des `tuple`s et des `set`s :

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial007.py!}
```

Traduction :

* La variable `items_t` est un `tuple` avec 3 éléments, un `int`, un autre `int`, et un `str`.
* La variable `items_s` est un `set`, et chacun de ces éléments est de type `bytes`.

#### `Dict`

Pour définir un `dict`, vous devez passer 2 "type parameters", séparés par des virgules.

Le premier "type parameter" est utilisé pour les 'keys' du `dict`.

Le second "type parameter" est utilisé pour les 'values' du `dict` :

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial008.py!}
```

Traduction :

* La variable `prices` est un `dict`:
    * Les 'keys' de ce `dict` sont de type `str` (par exemple, le nom de chaque élément).
    * Les 'values' de ce `dict` sont de type `float` (par exemple, le prix de chaque élément).

#### `Optional`

Vous pouvez utiliser `Optional` pour déclarer qu'une variable a un type, comme `str`, mais qu'il est "optional", ce qui signifie qu'il peut également être `None` :

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

En utilisant `Optional[str]` à la place de `str`, votre éditeur de code pourra détecter les erreurs ou vous pourriez croire qu'une valeur est toujours un `str`, alors que la valeur pourrait être `None`.

#### Types génériques

Ces types qui prennent des "types parameters" entre crochets, comme :

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...et d'autres.

sont appelés des **Generic types** or **Generics**.

### Des classes comme types

Vous pouvez également déclarer une classe comme étant un type de variable.

Imaginons que vous avez une classe `Person`, avec un nom :

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Vous pouvez alors déclarer une variable comme étant de type `Person` :

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

Et une fois de plus, vous bénéficiez de tout le support de votre éditeur de code :

<img src="/img/python-types/image06.png">

## Modèles Pydantic

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> est une librarie Python library qui effectue la validation de données.

Vous déclarez la "forme" de la donnée via des classes avec des attributs.

Et chaque attribut a un type.

Vous créerez ensuite une instance de cette classe avec quelques valeurs et Pydantic validera les valeurs, les convertira en type approprié (si c'est le cas) et vous rendra un objet avec toutes les données.

Et vous obtiendrez tout le support de votre éditeur de code sur votre objet retourné. 

Source en provenance des documentations officielles Pydantic :

```Python
{!../../../docs_src/python_types/tutorial011.py!}
```

!!! Info
    Pour en apprendre plus sur <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic, vérifiez ces documentations</a>.

**FastAPI** est basé sur Pydantic.

Vous obtiendrez plus de détails à partir du [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

## Utilisation des Type hints dans **FastAPI**

**FastAPI** tire parti des ces type hints pour faire plusieurs choses.

Avec **FastAPI** vous déclarez les paramètres avec des type hints et vous obtenez :

* **Du support de la part de votre éditeur de code**.
* **Une analyse des Type**.

...et **FastAPI** utilise les mêmes déclarations pour :

* **Definir des pré-requis** : à partir des 'path parameters' en provenance de requêtes, 'query parameters', headers, bodies, dépendances, etc.
* **Convertir les données** : à partir de la requête jusqu'au type requis.
* **Validation de données** : en provenance de chaque requête :
    * Génération **automatique d'erreurs** retournées au client quand la données est invalide.
* **Documenter** l'API en utilisant OpenAPI :
    * Qui est alors utilisée via les interfaces utilisateur de documentation automatique interactive.

Ceci peut vous sembler abstrait. Mais ne vous inquiétez pas, vous verrez tout ceci en action dans le [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

La chose importante à retenir est qu'en utilisant les Python types, à un seul endroit (au lieu d'ajouter plus de classes, des décorateurs, etc), **FastAPI** fera plein de choses pour vous.

!!! Info
    Si vous avez déjà parcouru l'ensemble du tutoriel et revenez pour en savoir plus au sujet des Python types, une bonne ressource est <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">La "cheat sheet" de `mypy`</a>.
