# Introduction aux types Python { #python-types-intro }

Python prend en charge des « annotations de type » (aussi appelées « type hints ») facultatives.

Ces **« annotations de type »** sont une syntaxe spéciale qui permet de déclarer le <dfn title="par exemple : str, int, float, bool">type</dfn> d'une variable.

En déclarant les types de vos variables, les éditeurs et outils peuvent vous offrir un meilleur support.

Ceci est un **tutoriel rapide / rappel** à propos des annotations de type Python. Il couvre uniquement le minimum nécessaire pour les utiliser avec **FastAPI** ... ce qui est en réalité très peu.

**FastAPI** est totalement basé sur ces annotations de type, elles lui donnent de nombreux avantages et bénéfices.

Mais même si vous n'utilisez jamais **FastAPI**, vous auriez intérêt à en apprendre un peu à leur sujet.

/// note | Remarque

Si vous êtes un expert Python, et que vous savez déjà tout sur les annotations de type, passez au chapitre suivant.

///

## Motivation { #motivation }

Commençons par un exemple simple :

{* ../../docs_src/python_types/tutorial001_py310.py *}

Exécuter ce programme affiche :

```
John Doe
```

La fonction fait ce qui suit :

* Prend un `first_name` et un `last_name`.
* Convertit la première lettre de chacun en majuscule avec `title()`.
* <dfn title="Les met ensemble, en un seul. Avec le contenu de l'un après l'autre.">Concatène</dfn> ces deux valeurs avec un espace au milieu.

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### Modifier le code { #edit-it }

C'est un programme très simple.

Mais maintenant imaginez que vous l'écriviez de zéro.

À un certain moment, vous auriez commencé la définition de la fonction, vous aviez les paramètres prêts ...

Mais ensuite vous devez appeler « cette méthode qui convertit la première lettre en majuscule ».

Était-ce `upper` ? Était-ce `uppercase` ? `first_uppercase` ? `capitalize` ?

Vous essayez alors avec l'ami de toujours des programmeurs, l'autocomplétion de l'éditeur.

Vous tapez le premier paramètre de la fonction, `first_name`, puis un point (`.`) et appuyez sur `Ctrl+Espace` pour déclencher l'autocomplétion.

Mais, malheureusement, vous n'obtenez rien d'utile :

<img src="/img/python-types/image01.png">

### Ajouter des types { #add-types }

Modifions une seule ligne de la version précédente.

Nous allons changer exactement ce fragment, les paramètres de la fonction, de :

```Python
    first_name, last_name
```

à :

```Python
    first_name: str, last_name: str
```

C'est tout.

Ce sont les « annotations de type » :

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

Ce n'est pas la même chose que de déclarer des valeurs par défaut, ce qui serait :

```Python
    first_name="john", last_name="doe"
```

C'est différent.

Nous utilisons des deux-points (`:`), pas des signes égal (`=`).

Et ajouter des annotations de type ne change normalement pas ce qui se passe par rapport à ce qui se passerait sans elles.

Mais maintenant, imaginez que vous êtes à nouveau en train de créer cette fonction, mais avec des annotations de type.

Au même moment, vous essayez de déclencher l'autocomplétion avec `Ctrl+Espace` et vous voyez :

<img src="/img/python-types/image02.png">

Avec cela, vous pouvez faire défiler en voyant les options, jusqu'à trouver celle qui « vous dit quelque chose » :

<img src="/img/python-types/image03.png">

## Plus de motivation { #more-motivation }

Regardez cette fonction, elle a déjà des annotations de type :

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

Comme l'éditeur connaît les types des variables, vous n'obtenez pas seulement l'autocomplétion, vous obtenez aussi des vérifications d'erreurs :

<img src="/img/python-types/image04.png">

Vous savez maintenant qu'il faut corriger, convertir `age` en chaîne avec `str(age)` :

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Déclarer des types { #declaring-types }

Vous venez de voir l'endroit principal pour déclarer des annotations de type : dans les paramètres des fonctions.

C'est aussi l'endroit principal où vous les utiliserez avec **FastAPI**.

### Types simples { #simple-types }

Vous pouvez déclarer tous les types standards de Python, pas seulement `str`.

Vous pouvez utiliser, par exemple :

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### Module `typing` { #typing-module }

Pour certains cas d'utilisation supplémentaires, vous pourriez avoir besoin d'importer certains éléments depuis le module standard `typing`, par exemple lorsque vous voulez déclarer que quelque chose a « n'importe quel type », vous pouvez utiliser `Any` depuis `typing` :

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Types génériques { #generic-types }

Certains types peuvent prendre des « paramètres de type » entre crochets, pour définir leurs types internes, par exemple une « liste de chaînes » se déclarerait `list[str]`.

Ces types qui peuvent prendre des paramètres de type sont appelés des **types génériques** ou **Generics**.

Vous pouvez utiliser les mêmes types intégrés comme génériques (avec des crochets et des types à l'intérieur) :

* `list`
* `tuple`
* `set`
* `dict`

#### Liste { #list }

Par exemple, définissons une variable comme une `list` de `str`.

Déclarez la variable, en utilisant la même syntaxe avec deux-points (`:`).

Comme type, mettez `list`.

Comme la liste est un type qui contient des types internes, mettez-les entre crochets :

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | Info

Ces types internes entre crochets sont appelés « paramètres de type ».

Dans ce cas, `str` est le paramètre de type passé à `list`.

///

Cela signifie : « la variable `items` est une `list`, et chacun des éléments de cette liste est un `str` ».

En faisant cela, votre éditeur peut vous fournir de l'aide même pendant le traitement des éléments de la liste :

<img src="/img/python-types/image05.png">

Sans types, c'est presque impossible à réaliser.

Remarquez que la variable `item` est l'un des éléments de la liste `items`.

Et pourtant, l'éditeur sait que c'est un `str` et fournit le support approprié.

#### Tuple et Set { #tuple-and-set }

Vous feriez la même chose pour déclarer des `tuple` et des `set` :

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

Cela signifie :

* La variable `items_t` est un `tuple` avec 3 éléments, un `int`, un autre `int`, et un `str`.
* La variable `items_s` est un `set`, et chacun de ses éléments est de type `bytes`.

#### Dict { #dict }

Pour définir un `dict`, vous passez 2 paramètres de type, séparés par des virgules.

Le premier paramètre de type est pour les clés du `dict`.

Le second paramètre de type est pour les valeurs du `dict` :

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

Cela signifie :

* La variable `prices` est un `dict` :
    * Les clés de ce `dict` sont de type `str` (disons, le nom de chaque article).
    * Les valeurs de ce `dict` sont de type `float` (disons, le prix de chaque article).

#### Union { #union }

Vous pouvez déclarer qu'une variable peut être **plusieurs types**, par exemple, un `int` ou un `str`.

Pour le définir, vous utilisez la <dfn title='aussi appelé « opérateur OU bit à bit », mais ce sens n’est pas pertinent ici'>barre verticale (`|`)</dfn> pour séparer les deux types.

C'est ce qu'on appelle une « union », car la variable peut être n'importe quoi dans l'union de ces deux ensembles de types.

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

Cela signifie que `item` peut être un `int` ou un `str`.

#### Possiblement `None` { #possibly-none }

Vous pouvez déclarer qu'une valeur peut avoir un type, comme `str`, mais qu'elle peut aussi être `None`.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

Utiliser `str | None` au lieu de simplement `str` permettra à l'éditeur de vous aider à détecter des erreurs où vous supposeriez qu'une valeur est toujours un `str`, alors qu'elle pourrait en fait aussi être `None`.

### Classes en tant que types { #classes-as-types }

Vous pouvez aussi déclarer une classe comme type d'une variable.

Disons que vous avez une classe `Person`, avec un nom :

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

Vous pouvez ensuite déclarer une variable de type `Person` :

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

Et là encore, vous obtenez tout le support de l'éditeur :

<img src="/img/python-types/image06.png">

Remarquez que cela signifie « `one_person` est une **instance** de la classe `Person` ».

Cela ne signifie pas « `one_person` est la **classe** appelée `Person` ».

## Modèles Pydantic { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> est une bibliothèque Python pour effectuer de la validation de données.

Vous déclarez la « forme » de la donnée sous forme de classes avec des attributs.

Et chaque attribut a un type.

Ensuite, vous créez une instance de cette classe avec certaines valeurs et elle validera les valeurs, les convertira dans le type approprié (le cas échéant) et vous donnera un objet avec toutes les données.

Et vous obtenez tout le support de l'éditeur avec cet objet résultant.

Un exemple tiré de la documentation officielle de Pydantic :

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | Info

Pour en savoir plus à propos de <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, consultez sa documentation</a>.

///

**FastAPI** est entièrement basé sur Pydantic.

Vous verrez beaucoup plus de tout cela en pratique dans le [Tutoriel - Guide utilisateur](tutorial/index.md){.internal-link target=_blank}.

## Annotations de type avec métadonnées { #type-hints-with-metadata-annotations }

Python dispose également d'une fonctionnalité qui permet de mettre des **<dfn title="Données sur les données, dans ce cas, des informations sur le type, p. ex. une description.">métadonnées</dfn> supplémentaires** dans ces annotations de type en utilisant `Annotated`.

Vous pouvez importer `Annotated` depuis `typing`.

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python lui-même ne fait rien avec ce `Annotated`. Et pour les éditeurs et autres outils, le type est toujours `str`.

Mais vous pouvez utiliser cet espace dans `Annotated` pour fournir à **FastAPI** des métadonnées supplémentaires sur la façon dont vous voulez que votre application se comporte.

L'important à retenir est que **le premier « paramètre de type »** que vous passez à `Annotated` est le **type réel**. Le reste n'est que des métadonnées pour d'autres outils.

Pour l'instant, vous avez juste besoin de savoir que `Annotated` existe, et que c'est du Python standard. 😎

Plus tard, vous verrez à quel point cela peut être **puissant**.

/// tip | Astuce

Le fait que ce soit du **Python standard** signifie que vous bénéficierez toujours de la **meilleure expérience développeur possible** dans votre éditeur, avec les outils que vous utilisez pour analyser et refactoriser votre code, etc. ✨

Et aussi que votre code sera très compatible avec de nombreux autres outils et bibliothèques Python. 🚀

///

## Annotations de type dans **FastAPI** { #type-hints-in-fastapi }

**FastAPI** tire parti de ces annotations de type pour faire plusieurs choses.

Avec **FastAPI**, vous déclarez des paramètres avec des annotations de type et vous obtenez :

* **Du support de l'éditeur**.
* **Des vérifications de types**.

... et **FastAPI** utilise les mêmes déclarations pour :

* **Définir des prérequis** : à partir des paramètres de chemin de la requête, des paramètres de requête, des en-têtes, des corps, des dépendances, etc.
* **Convertir des données** : de la requête vers le type requis.
* **Valider des données** : provenant de chaque requête :
    * En générant des **erreurs automatiques** renvoyées au client lorsque la donnée est invalide.
* **Documenter** l'API avec OpenAPI :
    * ce qui est ensuite utilisé par les interfaces utilisateur de documentation interactive automatiques.

Tout cela peut sembler abstrait. Ne vous inquiétez pas. Vous verrez tout cela en action dans le [Tutoriel - Guide utilisateur](tutorial/index.md){.internal-link target=_blank}.

L'important est qu'en utilisant les types standards de Python, en un seul endroit (au lieu d'ajouter plus de classes, de décorateurs, etc.), **FastAPI** fera une grande partie du travail pour vous.

/// info | Info

Si vous avez déjà parcouru tout le tutoriel et êtes revenu pour en voir plus sur les types, une bonne ressource est <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">l'« aide-mémoire » de `mypy`</a>.

///
