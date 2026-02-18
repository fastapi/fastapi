# Paramètres de requête et validations de chaînes de caractères { #query-parameters-and-string-validations }

**FastAPI** vous permet de déclarer des informations et des validations supplémentaires pour vos paramètres.

Prenons cette application comme exemple :

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

Le paramètre de requête `q` est de type `str | None`, cela signifie qu’il est de type `str` mais peut aussi être `None`, et en effet, la valeur par défaut est `None`, donc FastAPI saura qu’il n’est pas requis.

/// note | Remarque

FastAPI saura que la valeur de `q` n’est pas requise grâce à la valeur par défaut `= None`.

Avoir `str | None` permettra à votre éditeur de vous offrir un meilleur support et de détecter les erreurs.

///

## Validation additionnelle { #additional-validation }

Nous allons imposer que, même si `q` est optionnel, dès qu’il est fourni, **sa longueur n’excède pas 50 caractères**.

### Importer `Query` et `Annotated` { #import-query-and-annotated }

Pour ce faire, importez d’abord :

- `Query` depuis `fastapi`
- `Annotated` depuis `typing`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// info

FastAPI a ajouté la prise en charge de `Annotated` (et a commencé à le recommander) dans la version 0.95.0.

Si vous avez une version plus ancienne, vous obtiendrez des erreurs en essayant d’utiliser `Annotated`.

Assurez-vous de [mettre à niveau la version de FastAPI](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} vers au moins 0.95.1 avant d’utiliser `Annotated`.

///

## Utiliser `Annotated` dans le type pour le paramètre `q` { #use-annotated-in-the-type-for-the-q-parameter }

Vous vous souvenez que je vous ai dit plus tôt que `Annotated` peut être utilisé pour ajouter des métadonnées à vos paramètres dans l’[Introduction aux types Python](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank} ?

C’est le moment de l’utiliser avec FastAPI. 🚀

Nous avions cette annotation de type :

```Python
q: str | None = None
```

Ce que nous allons faire, c’est l’englober avec `Annotated`, de sorte que cela devienne :

```Python
q: Annotated[str | None] = None
```

Les deux versions signifient la même chose, `q` est un paramètre qui peut être une `str` ou `None`, et par défaut, c’est `None`.

Passons maintenant aux choses amusantes. 🎉

## Ajouter `Query` à `Annotated` dans le paramètre `q` { #add-query-to-annotated-in-the-q-parameter }

Maintenant que nous avons cet `Annotated` dans lequel nous pouvons mettre plus d’informations (dans ce cas une validation supplémentaire), ajoutez `Query` à l’intérieur de `Annotated`, et définissez le paramètre `max_length` à `50` :

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

Remarquez que la valeur par défaut est toujours `None`, donc le paramètre est toujours optionnel.

Mais maintenant, avec `Query(max_length=50)` à l’intérieur de `Annotated`, nous indiquons à FastAPI que nous voulons **une validation supplémentaire** pour cette valeur, nous voulons qu’elle ait au maximum 50 caractères. 😎

/// tip | Astuce

Ici nous utilisons `Query()` parce qu’il s’agit d’un **paramètre de requête**. Plus tard nous verrons d’autres comme `Path()`, `Body()`, `Header()` et `Cookie()`, qui acceptent également les mêmes arguments que `Query()`.

///

FastAPI va maintenant :

- **Valider** les données en s’assurant que la longueur maximale est de 50 caractères
- Afficher une **erreur claire** au client quand les données ne sont pas valides
- **Documenter** le paramètre dans la *chemin d'accès* du schéma OpenAPI (il apparaîtra donc dans l’**interface de documentation automatique**)

## Alternative (ancienne) : `Query` comme valeur par défaut { #alternative-old-query-as-the-default-value }

Les versions précédentes de FastAPI (avant <dfn title="avant 2023-03">0.95.0</dfn>) exigeaient d’utiliser `Query` comme valeur par défaut de votre paramètre, au lieu de le mettre dans `Annotated`. Il y a de fortes chances que vous voyiez du code qui l’utilise encore, je vais donc vous l’expliquer.

/// tip | Astuce

Pour du nouveau code et dès que possible, utilisez `Annotated` comme expliqué ci-dessus. Il y a de multiples avantages (expliqués ci-dessous) et aucun inconvénient. 🍰

///

Voici comment vous utiliseriez `Query()` comme valeur par défaut du paramètre de votre fonction, en définissant le paramètre `max_length` à 50 :

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

Comme, dans ce cas (sans utiliser `Annotated`), nous devons remplacer la valeur par défaut `None` dans la fonction par `Query()`, nous devons maintenant définir la valeur par défaut avec le paramètre `Query(default=None)`, cela sert le même objectif de définir cette valeur par défaut (au moins pour FastAPI).

Donc :

```Python
q: str | None = Query(default=None)
```

... rend le paramètre optionnel, avec une valeur par défaut de `None`, comme :

```Python
q: str | None = None
```

Mais la version avec `Query` le déclare explicitement comme étant un paramètre de requête.

Ensuite, nous pouvons passer plus de paramètres à `Query`. Dans ce cas, le paramètre `max_length` qui s’applique aux chaînes de caractères :

```Python
q: str | None = Query(default=None, max_length=50)
```

Cela validera les données, affichera une erreur claire lorsque les données ne sont pas valides et documentera le paramètre dans la *chemin d'accès* du schéma OpenAPI.

### `Query` comme valeur par défaut ou dans `Annotated` { #query-as-the-default-value-or-in-annotated }

Gardez à l’esprit qu’en utilisant `Query` à l’intérieur de `Annotated`, vous ne pouvez pas utiliser le paramètre `default` de `Query`.

Utilisez à la place la valeur par défaut réelle du paramètre de fonction. Sinon, ce serait incohérent.

Par exemple, ceci n’est pas autorisé :

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

... parce qu’il n’est pas clair si la valeur par défaut doit être « rick » ou « morty ».

Donc, vous utiliseriez (de préférence) :

```Python
q: Annotated[str, Query()] = "rick"
```

... ou dans des bases de code plus anciennes, vous trouverez :

```Python
q: str = Query(default="rick")
```

### Avantages de `Annotated` { #advantages-of-annotated }

**L’utilisation de `Annotated` est recommandée** plutôt que la valeur par défaut dans les paramètres de fonction, c’est **mieux** pour plusieurs raisons. 🤓

La valeur **par défaut** du **paramètre de fonction** est la **vraie valeur par défaut**, c’est plus intuitif en Python en général. 😌

Vous pouvez **appeler** cette même fonction dans **d’autres endroits** sans FastAPI, et elle **fonctionnera comme prévu**. S’il y a un paramètre **requis** (sans valeur par défaut), votre **éditeur** vous le signalera avec une erreur, **Python** se plaindra aussi si vous l’exécutez sans passer le paramètre requis.

Quand vous n’utilisez pas `Annotated` et utilisez à la place l’**ancienne** méthode avec la **valeur par défaut**, si vous appelez cette fonction sans FastAPI dans **d’autres endroits**, vous devez **penser** à passer les arguments à la fonction pour qu’elle fonctionne correctement, sinon les valeurs seront différentes de ce que vous attendez (par ex. `QueryInfo` ou quelque chose de similaire au lieu d’une `str`). Et votre éditeur ne se plaindra pas, et Python ne se plaindra pas en exécutant cette fonction, seulement quand les opérations internes échoueront.

Comme `Annotated` peut avoir plus d’une annotation de métadonnées, vous pouvez maintenant même utiliser la même fonction avec d’autres outils, comme <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>. 🚀

## Ajouter plus de validations { #add-more-validations }

Vous pouvez également ajouter un paramètre `min_length` :

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## Ajouter des expressions régulières { #add-regular-expressions }

Vous pouvez définir un `pattern` d’<dfn title="Une expression régulière, regex ou regexp, est une suite de caractères qui définit un motif de recherche pour les chaînes de caractères.">expression régulière</dfn> auquel le paramètre doit correspondre :

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

Ce pattern d’expression régulière spécifique vérifie que la valeur reçue pour le paramètre :

- `^` : commence avec les caractères qui suivent, n’a pas de caractères avant.
- `fixedquery` : a exactement la valeur `fixedquery`.
- `$` : se termine là, n’a pas d’autres caractères après `fixedquery`.

Si vous vous sentez perdu avec toutes ces idées d’**« expression régulière »**, pas d’inquiétude. C’est un sujet difficile pour beaucoup. Vous pouvez déjà faire beaucoup de choses sans avoir besoin d’expressions régulières.

Désormais, vous savez que, lorsque vous en aurez besoin, vous pourrez les utiliser dans **FastAPI**.

## Valeurs par défaut { #default-values }

Vous pouvez, bien sûr, utiliser des valeurs par défaut autres que `None`.

Disons que vous voulez déclarer le paramètre de requête `q` avec un `min_length` de `3`, et avec une valeur par défaut de « fixedquery » :

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | Remarque

Avoir une valeur par défaut de n’importe quel type, y compris `None`, rend le paramètre optionnel (non requis).

///

## Paramètres requis { #required-parameters }

Quand nous n’avons pas besoin de déclarer plus de validations ou de métadonnées, nous pouvons rendre le paramètre de requête `q` requis en n’indiquant simplement pas de valeur par défaut, comme :

```Python
q: str
```

au lieu de :

```Python
q: str | None = None
```

Mais maintenant nous le déclarons avec `Query`, par exemple ainsi :

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

Donc, lorsque vous avez besoin de déclarer une valeur comme requise tout en utilisant `Query`, vous pouvez simplement ne pas déclarer de valeur par défaut :

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### Requis, peut valoir `None` { #required-can-be-none }

Vous pouvez déclarer qu’un paramètre accepte `None`, mais qu’il est tout de même requis. Cela obligerait les clients à envoyer une valeur, même si la valeur est `None`.

Pour ce faire, vous pouvez déclarer que `None` est un type valide tout en ne déclarant pas de valeur par défaut :

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## Liste de paramètres de requête / valeurs multiples { #query-parameter-list-multiple-values }

Quand vous définissez un paramètre de requête explicitement avec `Query`, vous pouvez aussi déclarer qu’il reçoit une liste de valeurs, autrement dit, qu’il reçoit des valeurs multiples.

Par exemple, pour déclarer un paramètre de requête `q` qui peut apparaître plusieurs fois dans l’URL, vous pouvez écrire :

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

Ensuite, avec une URL comme :

```
http://localhost:8000/items/?q=foo&q=bar
```

vous recevriez les valeurs des multiples paramètres de requête `q` (`foo` et `bar`) dans une `list` Python à l’intérieur de votre fonction de *chemin d'accès*, dans le *paramètre de fonction* `q`.

Donc, la réponse pour cette URL serait :

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | Astuce

Pour déclarer un paramètre de requête avec un type `list`, comme dans l’exemple ci-dessus, vous devez explicitement utiliser `Query`, sinon il serait interprété comme faisant partie du corps de la requête.

///

L’interface de documentation interactive de l’API sera mise à jour en conséquence, pour autoriser plusieurs valeurs :

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Liste de paramètres de requête / valeurs multiples avec valeurs par défaut { #query-parameter-list-multiple-values-with-defaults }

Vous pouvez également définir une `list` de valeurs par défaut si aucune n’est fournie :

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

Si vous allez à :

```
http://localhost:8000/items/
```

la valeur par défaut de `q` sera : `["foo", "bar"]` et votre réponse sera :

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Utiliser simplement `list` { #using-just-list }

Vous pouvez aussi utiliser `list` directement au lieu de `list[str]` :

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | Remarque

Gardez à l’esprit que dans ce cas, FastAPI ne vérifiera pas le contenu de la liste.

Par exemple, `list[int]` vérifierait (et documenterait) que le contenu de la liste est composé d’entiers. Mais un simple `list` ne le ferait pas.

///

## Déclarer plus de métadonnées { #declare-more-metadata }

Vous pouvez ajouter plus d’informations à propos du paramètre.

Ces informations seront incluses dans l’OpenAPI généré et utilisées par les interfaces de documentation et les outils externes.

/// note | Remarque

Gardez à l’esprit que différents outils peuvent avoir des niveaux de prise en charge d’OpenAPI différents.

Certains d’entre eux pourraient ne pas encore afficher toutes les informations supplémentaires déclarées, bien que, dans la plupart des cas, la fonctionnalité manquante soit déjà prévue au développement.

///

Vous pouvez ajouter un `title` :

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

Et une `description` :

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Paramètres avec alias { #alias-parameters }

Imaginez que vous vouliez que le paramètre soit `item-query`.

Comme dans :

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Mais `item-query` n’est pas un nom de variable Python valide.

Le plus proche serait `item_query`.

Mais vous avez quand même besoin que ce soit exactement `item-query` ...

Vous pouvez alors déclarer un `alias`, et cet alias sera utilisé pour trouver la valeur du paramètre :

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Déprécier des paramètres { #deprecating-parameters }

Disons que vous n’aimez plus ce paramètre.

Vous devez le laisser là quelque temps car des clients l’utilisent, mais vous voulez que les documents l’affichent clairement comme <dfn title="obsolète, il est recommandé de ne pas l’utiliser">déprécié</dfn>.

Passez alors le paramètre `deprecated=True` à `Query` :

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

Les documents l’afficheront ainsi :

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Exclure des paramètres d’OpenAPI { #exclude-parameters-from-openapi }

Pour exclure un paramètre de requête du schéma OpenAPI généré (et donc, des systèmes de documentation automatiques), définissez le paramètre `include_in_schema` de `Query` à `False` :

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## Validation personnalisée { #custom-validation }

Il peut y avoir des cas où vous devez faire une **validation personnalisée** qui ne peut pas être réalisée avec les paramètres montrés ci-dessus.

Dans ces cas, vous pouvez utiliser une **fonction de validation personnalisée** qui est appliquée après la validation normale (par ex. après avoir validé que la valeur est une `str`).

Vous pouvez y parvenir en utilisant <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator" class="external-link" target="_blank">`AfterValidator` de Pydantic</a> à l’intérieur de `Annotated`.

/// tip | Astuce

Pydantic a aussi <a href="https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator" class="external-link" target="_blank">`BeforeValidator`</a> et d’autres. 🤓

///

Par exemple, ce validateur personnalisé vérifie que l’ID d’item commence par `isbn-` pour un numéro de livre <abbr title="International Standard Book Number - Numéro international normalisé du livre">ISBN</abbr> ou par `imdb-` pour un ID d’URL de film <abbr title="Internet Movie Database - Base de données de films sur Internet: un site web contenant des informations sur les films">IMDB</abbr> :

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// info

C’est disponible avec Pydantic version 2 ou supérieure. 😎

///

/// tip | Astuce

Si vous devez faire un type de validation qui nécessite de communiquer avec un **composant externe**, comme une base de données ou une autre API, vous devez plutôt utiliser les **Dépendances de FastAPI**, vous en apprendrez davantage plus tard.

Ces validateurs personnalisés sont destinés aux éléments qui peuvent être vérifiés **uniquement** avec les **mêmes données** fournies dans la requête.

///

### Comprendre ce code { #understand-that-code }

Le point important est simplement d’utiliser **`AfterValidator` avec une fonction à l’intérieur de `Annotated`**. N’hésitez pas à passer cette partie. 🤸

---

Mais si vous êtes curieux de cet exemple de code spécifique et que vous êtes toujours partant, voici quelques détails supplémentaires.

#### Chaîne avec `value.startswith()` { #string-with-value-startswith }

Avez-vous remarqué ? Une chaîne utilisant `value.startswith()` peut prendre un tuple, et elle vérifiera chaque valeur du tuple :

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### Un élément aléatoire { #a-random-item }

Avec `data.items()` nous obtenons un <dfn title="Quelque chose que l’on peut itérer avec une boucle for, comme une liste, un set, etc.">objet itérable</dfn> avec des tuples contenant la clé et la valeur pour chaque élément du dictionnaire.

Nous convertissons cet objet itérable en une `list` propre avec `list(data.items())`.

Ensuite, avec `random.choice()` nous pouvons obtenir une **valeur aléatoire** depuis la liste, nous obtenons donc un tuple `(id, name)`. Ce sera quelque chose comme `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")`.

Puis nous **affectons ces deux valeurs** du tuple aux variables `id` et `name`.

Ainsi, si l’utilisateur n’a pas fourni d’ID d’item, il recevra quand même une suggestion aléatoire.

... nous faisons tout cela en **une seule ligne simple**. 🤯 Vous n’adorez pas Python ? 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## Récapitulatif { #recap }

Vous pouvez déclarer des validations et des métadonnées supplémentaires pour vos paramètres.

Validations et métadonnées génériques :

- `alias`
- `title`
- `description`
- `deprecated`

Validations spécifiques aux chaînes :

- `min_length`
- `max_length`
- `pattern`

Validations personnalisées avec `AfterValidator`.

Dans ces exemples, vous avez vu comment déclarer des validations pour des valeurs `str`.

Voyez les prochains chapitres pour apprendre à déclarer des validations pour d’autres types, comme les nombres.
