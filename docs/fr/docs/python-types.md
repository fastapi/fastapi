# Introduction aux Types Python { #python-types-intro }

Python supporte des « type hints » optionnels (aussi appelés « type annotations »).

Ces **« type hints »** ou annotations sont une syntaxe spéciale qui permet de déclarer le <abbr title="par exemple : str, int, float, bool">type</abbr> d'une variable.

En déclarant des types pour vos variables, les éditeurs et les outils peuvent vous offrir un meilleur support.

Ceci n'est qu'un **tutoriel rapide / rappel** sur les « type hints » de Python. Il couvre seulement le minimum nécessaire pour les utiliser avec **FastAPI**... ce qui est en réalité très peu.

**FastAPI** est entièrement basé sur ces « type hints », ils lui donnent de nombreux avantages et bénéfices.

Mais même si vous n'utilisez jamais **FastAPI**, vous auriez intérêt à en apprendre un peu à leur sujet.

/// note | Remarque

Si vous êtes un expert Python, et que vous savez déjà tout sur les « type hints », passez au chapitre suivant.

///

## Motivation { #motivation }

Commençons par un exemple simple :

{* ../../docs_src/python_types/tutorial001_py39.py *}

L'exécution de ce programme affiche :

```
John Doe
```

La fonction fait ce qui suit :

* Prend un `first_name` et un `last_name`.
* Convertit la première lettre de chacun en majuscule avec `title()`.
* Les <abbr title="Puts them together, as one. With the contents of one after the other.">concatène</abbr> avec un espace au milieu.

{* ../../docs_src/python_types/tutorial001_py39.py hl[2] *}

### Le modifier { #edit-it }

C'est un programme très simple.

Mais imaginez maintenant que vous l'écriviez de zéro.

À un certain point, vous auriez commencé la définition de la fonction, vous aviez les paramètres prêts...

Mais ensuite vous devez appeler « cette méthode qui convertit la première lettre en majuscule ».

Était-ce `upper` ? Était-ce `uppercase` ? `first_uppercase` ? `capitalize` ?

Ensuite, vous essayez avec le vieil ami du programmeur, l'autocomplétion de l'éditeur.

Vous tapez le premier paramètre de la fonction, `first_name`, puis un point (`.`) et appuyez sur `Ctrl+Space` pour déclencher la complétion.

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

Ce sont les « type hints » :

{* ../../docs_src/python_types/tutorial002_py39.py hl[1] *}

Ce n'est pas la même chose que de déclarer des valeurs par défaut, comme ce serait le cas avec :

```Python
    first_name="john", last_name="doe"
```

C'est une chose différente.

Nous utilisons des deux-points (`:`), pas des signes égal (`=`).

Et ajouter des « type hints » ne change normalement pas ce qui se passe par rapport à ce qui se passerait sans eux.

Mais maintenant, imaginez que vous êtes à nouveau en plein milieu de la création de cette fonction, mais avec des « type hints ».

Au même endroit, vous essayez de déclencher l'autocomplétion avec `Ctrl+Space` et vous voyez :

<img src="/img/python-types/image02.png">

Avec ça, vous pouvez faire défiler, voir les options, jusqu'à trouver celle qui « vous dit quelque chose » :

<img src="/img/python-types/image03.png">

## Plus de motivation { #more-motivation }

Regardez cette fonction, elle a déjà des « type hints » :

{* ../../docs_src/python_types/tutorial003_py39.py hl[1] *}

Parce que l'éditeur connaît les types des variables, vous n'avez pas seulement la complétion, vous avez aussi des vérifications d'erreurs :

<img src="/img/python-types/image04.png">

Maintenant vous savez que vous devez le corriger, convertir `age` en chaîne de caractères avec `str(age)` :

{* ../../docs_src/python_types/tutorial004_py39.py hl[2] *}

## Déclarer des types { #declaring-types }

Vous venez de voir l'endroit principal pour déclarer des « type hints ». En tant que paramètres de fonction.

C'est aussi l'endroit principal où vous les utiliseriez avec **FastAPI**.

### Types simples { #simple-types }

Vous pouvez déclarer tous les types standards de Python, pas seulement `str`.

Vous pouvez utiliser, par exemple :

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py39.py hl[1] *}

### Types génériques avec des paramètres de type { #generic-types-with-type-parameters }

Il existe des structures de données qui peuvent contenir d'autres valeurs, comme `dict`, `list`, `set` et `tuple`. Et les valeurs internes peuvent aussi avoir leur propre type.

Ces types qui ont des types internes sont appelés des types « génériques » (**generic**). Et il est possible de les déclarer, même avec leurs types internes.

Pour déclarer ces types et les types internes, vous pouvez utiliser le module standard Python `typing`. Il existe spécifiquement pour supporter ces « type hints ».

#### Versions plus récentes de Python { #newer-versions-of-python }

La syntaxe utilisant `typing` est **compatible** avec toutes les versions, de Python 3.6 aux plus récentes, y compris Python 3.9, Python 3.10, etc.

Au fur et à mesure que Python évolue, les **versions plus récentes** offrent un support amélioré pour ces annotations de type et, dans de nombreux cas, vous n'aurez même pas besoin d'importer et d'utiliser le module `typing` pour déclarer les annotations de type.

Si vous pouvez choisir une version plus récente de Python pour votre projet, vous pourrez profiter de cette simplicité supplémentaire.

Dans toute la documentation, il y a des exemples compatibles avec chaque version de Python (quand il y a une différence).

Par exemple « **Python 3.6+** » signifie que c'est compatible avec Python 3.6 ou supérieur (y compris 3.7, 3.8, 3.9, 3.10, etc). Et « **Python 3.9+** » signifie que c'est compatible avec Python 3.9 ou supérieur (y compris 3.10, etc).

Si vous pouvez utiliser les **dernières versions de Python**, utilisez les exemples pour la version la plus récente, ceux-ci auront la **meilleure et la plus simple syntaxe**, par exemple, « **Python 3.10+** ».

#### List { #list }

Par exemple, définissons une variable comme une `list` de `str`.

Déclarez la variable, avec la même syntaxe de deux-points (`:`).

Comme type, mettez `list`.

Comme la liste est un type qui contient des types internes, vous les mettez entre crochets :

{* ../../docs_src/python_types/tutorial006_py39.py hl[1] *}

/// info

Ces types internes entre crochets sont appelés des « paramètres de type ».

Dans ce cas, `str` est le paramètre de type passé à `list`.

///

Cela signifie : « la variable `items` est une `list`, et chacun des éléments de cette liste est un `str` ».

En faisant cela, votre éditeur peut fournir du support même pendant le traitement des éléments de la liste :

<img src="/img/python-types/image05.png">

Sans types, c'est presque impossible à réaliser.

Remarquez que la variable `item` est un des éléments de la liste `items`.

Et pourtant, l'éditeur sait que c'est un `str`, et fournit du support pour ça.

#### Tuple et Set { #tuple-and-set }

Vous feriez la même chose pour déclarer des `tuple` et des `set` :

{* ../../docs_src/python_types/tutorial007_py39.py hl[1] *}

Cela signifie :

* La variable `items_t` est un `tuple` avec 3 éléments, un `int`, un autre `int`, et un `str`.
* La variable `items_s` est un `set`, et chacun de ses éléments est de type `bytes`.

#### Dict { #dict }

Pour définir un `dict`, vous passez 2 paramètres de type, séparés par des virgules.

Le premier paramètre de type est pour les clés du `dict`.

Le second paramètre de type est pour les valeurs du `dict` :

{* ../../docs_src/python_types/tutorial008_py39.py hl[1] *}

Cela signifie :

* La variable `prices` est un `dict` :
    * Les clés de ce `dict` sont de type `str` (disons, le nom de chaque élément).
    * Les valeurs de ce `dict` sont de type `float` (disons, le prix de chaque élément).

#### Union { #union }

Vous pouvez déclarer qu'une variable peut être de **plusieurs types**, par exemple, un `int` ou un `str`.

En Python 3.6 et supérieur (y compris Python 3.10) vous pouvez utiliser le type `Union` de `typing` et mettre entre crochets les types possibles à accepter.

En Python 3.10, il existe aussi une **nouvelle syntaxe** où vous pouvez mettre les types possibles séparés par une <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>barre verticale (`|`)</abbr>.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b_py39.py!}
```

////

Dans les deux cas, cela signifie que `item` pourrait être un `int` ou un `str`.

#### Possiblement `None` { #possibly-none }

Vous pouvez déclarer qu'une valeur pourrait avoir un type, comme `str`, mais qu'elle pourrait aussi être `None`.

En Python 3.6 et supérieur (y compris Python 3.10) vous pouvez le déclarer en important et en utilisant `Optional` depuis le module `typing`.

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009_py39.py!}
```

Utiliser `Optional[str]` au lieu de seulement `str` permettra à l'éditeur de vous aider à détecter des erreurs où vous pourriez supposer qu'une valeur est toujours un `str`, alors qu'elle pourrait aussi être `None`.

`Optional[Something]` est en fait un raccourci pour `Union[Something, None]`, ils sont équivalents.

Cela signifie aussi qu'en Python 3.10, vous pouvez utiliser `Something | None` :

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009_py39.py!}
```

////

//// tab | Alternative Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b_py39.py!}
```

////

#### Utiliser `Union` ou `Optional` { #using-union-or-optional }

Si vous utilisez une version de Python inférieure à 3.10, voici une astuce de mon point de vue très **subjectif** :

* 🚨 Évitez d'utiliser `Optional[SomeType]`
* À la place ✨ **utilisez `Union[SomeType, None]`** ✨.

Les deux sont équivalents et, en dessous, c'est la même chose, mais je recommande `Union` plutôt que `Optional` parce que le mot « optional » semblerait impliquer que la valeur est optionnelle, et cela signifie en réalité « elle peut être `None` », même si elle n'est pas optionnelle et est toujours requise.

Je pense que `Union[SomeType, None]` est plus explicite sur ce que cela signifie.

Ce n'est qu'une question de mots et de noms. Mais ces mots peuvent affecter la façon dont vous et vos coéquipiers pensez au code.

Par exemple, prenons cette fonction :

{* ../../docs_src/python_types/tutorial009c_py39.py hl[1,4] *}

Le paramètre `name` est défini comme `Optional[str]`, mais il n'est **pas optionnel**, vous ne pouvez pas appeler la fonction sans le paramètre :

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

Le paramètre `name` est **toujours requis** (pas *optionnel*) parce qu'il n'a pas de valeur par défaut. Pourtant, `name` accepte `None` comme valeur :

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

La bonne nouvelle est qu'une fois que vous serez sur Python 3.10, vous n'aurez plus à vous en soucier, car vous pourrez simplement utiliser `|` pour définir des unions de types :

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

Et ensuite vous n'aurez plus à vous soucier de noms comme `Optional` et `Union`. 😎

#### Types génériques { #generic-types }

Ces types qui prennent des paramètres de type entre crochets sont appelés des **Generic types** ou **Generics**, par exemple :

//// tab | Python 3.10+

Vous pouvez utiliser les mêmes types intégrés comme generics (avec des crochets et des types à l'intérieur) :

* `list`
* `tuple`
* `set`
* `dict`

Et comme avec les versions précédentes de Python, depuis le module `typing` :

* `Union`
* `Optional`
* ...et d'autres.

En Python 3.10, comme alternative à l'utilisation des generics `Union` et `Optional`, vous pouvez utiliser la <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>barre verticale (`|`)</abbr> pour déclarer des unions de types, c'est bien mieux et plus simple.

////

//// tab | Python 3.9+

Vous pouvez utiliser les mêmes types intégrés comme generics (avec des crochets et des types à l'intérieur) :

* `list`
* `tuple`
* `set`
* `dict`

Et des generics depuis le module `typing` :

* `Union`
* `Optional`
* ...et d'autres.

////

### Classes en tant que types { #classes-as-types }

Vous pouvez aussi déclarer une classe comme type d'une variable.

Disons que vous avez une classe `Person`, avec un nom :

{* ../../docs_src/python_types/tutorial010_py39.py hl[1:3] *}

Vous pouvez ensuite déclarer une variable de type `Person` :

{* ../../docs_src/python_types/tutorial010_py39.py hl[6] *}

Et alors, encore une fois, vous obtenez tout le support de l'éditeur :

<img src="/img/python-types/image06.png">

Remarquez que cela signifie que « `one_person` est une **instance** de la classe `Person` ».

Cela ne signifie pas que « `one_person` est la **classe** appelée `Person` ».

## Les modèles Pydantic { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> est une bibliothèque Python pour effectuer de la validation de données.

Vous déclarez la « forme » de la donnée comme des classes avec des attributs.

Et chaque attribut a un type.

Ensuite vous créez une instance de cette classe avec certaines valeurs et elle validera les valeurs, les convertira dans le type approprié (si c'est le cas) et vous donnera un objet avec toutes les données.

Et vous obtenez tout le support de l'éditeur avec cet objet résultant.

Un exemple des documents officiels de Pydantic :

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info

Pour en savoir plus sur <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, consultez sa documentation</a>.

///

**FastAPI** est entièrement basé sur Pydantic.

Vous verrez beaucoup plus tout cela en pratique dans le [Tutoriel - Guide utilisateur](tutorial/index.md){.internal-link target=_blank}.

/// tip | Astuce

Pydantic a un comportement spécial lorsque vous utilisez `Optional` ou `Union[Something, None]` sans valeur par défaut, vous pouvez en lire plus à ce sujet dans la documentation Pydantic sur les <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Required Optional fields</a>.

///

## Type Hints avec des annotations de métadonnées { #type-hints-with-metadata-annotations }

Python a aussi une fonctionnalité qui permet de mettre des **<abbr title="Data about the data, in this case, information about the type, e.g. a description.">métadonnées</abbr> supplémentaires** dans ces « type hints » en utilisant `Annotated`.

Depuis Python 3.9, `Annotated` fait partie de la bibliothèque standard, vous pouvez donc l'importer depuis `typing`.

{* ../../docs_src/python_types/tutorial013_py39.py hl[1,4] *}

Python lui-même ne fait rien avec ce `Annotated`. Et pour les éditeurs et d'autres outils, le type est toujours `str`.

Mais vous pouvez utiliser cet espace dans `Annotated` pour fournir à **FastAPI** des métadonnées supplémentaires sur la manière dont vous voulez que votre application se comporte.

La chose importante à retenir est que **le premier *paramètre de type*** que vous passez à `Annotated` est le **vrai type**. Le reste n'est que des métadonnées pour d'autres outils.

Pour le moment, vous devez juste savoir que `Annotated` existe, et que c'est du Python standard. 😎

Plus tard, vous verrez à quel point cela peut être **puissant**.

/// tip | Astuce

Le fait que ce soit du **Python standard** signifie que vous aurez toujours la **meilleure expérience développeur possible** dans votre éditeur, avec les outils que vous utilisez pour analyser et refactoriser votre code, etc. ✨

Et aussi que votre code sera très compatible avec de nombreux autres outils et bibliothèques Python. 🚀

///

## Les annotations de type dans **FastAPI** { #type-hints-in-fastapi }

**FastAPI** tire parti de ces « type hints » pour faire plusieurs choses.

Avec **FastAPI** vous déclarez des paramètres avec des « type hints » et vous obtenez :

* **Support de l'éditeur**.
* **Vérifications de types**.

... et **FastAPI** utilise les mêmes déclarations pour :

* **Définir des exigences** : à partir des paramètres de chemin de la requête, des paramètres de requête, des en-têtes, des corps, des dépendances, etc.
* **Convertir les données** : de la requête vers le type requis.
* **Valider les données** : provenant de chaque requête :
    * Générant des **erreurs automatiques** renvoyées au client lorsque les données sont invalides.
* **Documenter** l'API avec OpenAPI :
    * ce qui est ensuite utilisé par les interfaces utilisateur automatiques de documentation interactive.

Tout cela peut sembler abstrait. Ne vous inquiétez pas. Vous verrez tout cela en action dans le [Tutoriel - Guide utilisateur](tutorial/index.md){.internal-link target=_blank}.

L'important est qu'en utilisant les types standards de Python, à un seul endroit (au lieu d'ajouter plus de classes, de décorateurs, etc.), **FastAPI** fera une grande partie du travail pour vous.

/// info

Si vous avez déjà parcouru tout le tutoriel et que vous êtes revenu pour en voir plus sur les types, une bonne ressource est <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">la « cheat sheet » de `mypy`</a>.

///
