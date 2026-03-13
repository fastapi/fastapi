# Modèle de réponse - Type de retour { #response-model-return-type }

Vous pouvez déclarer le type utilisé pour la réponse en annotant le **type de retour** de la *fonction de chemin d'accès*.

Vous pouvez utiliser des **annotations de type** de la même manière que pour les données d'entrée dans les **paramètres** de fonction. Vous pouvez utiliser des modèles Pydantic, des listes, des dictionnaires, des valeurs scalaires comme des entiers, des booléens, etc.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI utilisera ce type de retour pour :

* **Valider** les données renvoyées.
    * Si les données sont invalides (par exemple, il manque un champ), cela signifie que le code de *votre* application est défectueux, qu'il ne renvoie pas ce qu'il devrait, et un erreur serveur sera renvoyée au lieu de renvoyer des données incorrectes. De cette façon, vous et vos clients pouvez être certains de recevoir les données attendues et avec la structure attendue.
* Ajouter un **JSON Schema** pour la réponse, dans l’OpenAPI du *chemin d'accès*.
    * Ceci sera utilisé par la **documentation automatique**.
    * Ceci sera également utilisé par les outils de génération automatique de code client.

Mais surtout :

* Il **limitera et filtrera** les données de sortie à ce qui est défini dans le type de retour.
    * C'est particulièrement important pour la **sécurité**, nous verrons cela plus bas.

## Paramètre `response_model` { #response-model-parameter }

Il existe des cas où vous devez ou souhaitez renvoyer des données qui ne correspondent pas exactement à ce que déclare le type.

Par exemple, vous pourriez vouloir **renvoyer un dictionnaire** ou un objet de base de données, mais **le déclarer comme un modèle Pydantic**. Ainsi, le modèle Pydantic ferait toute la documentation des données, la validation, etc. pour l'objet que vous avez renvoyé (par exemple un dictionnaire ou un objet de base de données).

Si vous ajoutez l'annotation du type de retour, les outils et éditeurs se plaindront avec une (juste) erreur vous indiquant que votre fonction renvoie un type (par exemple un dict) différent de ce que vous avez déclaré (par exemple un modèle Pydantic).

Dans ces cas, vous pouvez utiliser le paramètre `response_model` du *décorateur de chemin d'accès* au lieu du type de retour.

Vous pouvez utiliser le paramètre `response_model` dans n'importe lequel des *chemins d'accès* :

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | Remarque

Notez que `response_model` est un paramètre de la méthode « decorator » (`get`, `post`, etc.). Pas de votre *fonction de chemin d'accès*, comme tous les paramètres et le corps.

///

`response_model` reçoit le même type que vous déclareriez pour un champ de modèle Pydantic, il peut donc s'agir d'un modèle Pydantic, mais il peut aussi être, par exemple, une `list` de modèles Pydantic, comme `List[Item]`.

FastAPI utilisera ce `response_model` pour toute la documentation des données, la validation, etc. et aussi pour **convertir et filtrer les données de sortie** selon sa déclaration de type.

/// tip | Astuce

Si vous avez des vérifications de type strictes dans votre éditeur, mypy, etc., vous pouvez déclarer le type de retour de la fonction en `Any`.

Ainsi, vous indiquez à l'éditeur que vous renvoyez intentionnellement n'importe quoi. Mais FastAPI effectuera quand même la documentation, la validation, le filtrage, etc. des données avec `response_model`.

///

### Priorité de `response_model` { #response-model-priority }

Si vous déclarez à la fois un type de retour et un `response_model`, c'est `response_model` qui aura la priorité et sera utilisé par FastAPI.

De cette manière, vous pouvez ajouter des annotations de type correctes à vos fonctions même si vous renvoyez un type différent du modèle de réponse, pour qu'il soit utilisé par l'éditeur et des outils comme mypy. Et vous pouvez toujours laisser FastAPI faire la validation des données, la documentation, etc. avec `response_model`.

Vous pouvez également utiliser `response_model=None` pour désactiver la création d’un modèle de réponse pour ce *chemin d'accès* ; vous pourriez en avoir besoin si vous ajoutez des annotations de type pour des choses qui ne sont pas des champs valides Pydantic, vous verrez un exemple de cela dans une des sections ci-dessous.

## Renvoyer les mêmes données d'entrée { #return-the-same-input-data }

Ici, nous déclarons un modèle `UserIn`, il contiendra un mot de passe en clair :

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | Info

Pour utiliser `EmailStr`, installez d'abord <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email-validator`</a>.

Assurez-vous de créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis de l'installer, par exemple :

```console
$ pip install email-validator
```

ou avec :

```console
$ pip install "pydantic[email]"
```

///

Et nous utilisons ce modèle pour déclarer notre entrée et le même modèle pour déclarer notre sortie :

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

Désormais, chaque fois qu'un navigateur crée un utilisateur avec un mot de passe, l'API renverra le même mot de passe dans la réponse.

Dans ce cas, cela peut ne pas poser de problème, car c'est le même utilisateur qui envoie le mot de passe.

Mais si nous utilisons le même modèle pour un autre *chemin d'accès*, nous pourrions envoyer les mots de passe de nos utilisateurs à tous les clients.

/// danger | Danger

Ne stockez jamais le mot de passe en clair d'un utilisateur et ne l'envoyez pas dans une réponse de cette manière, à moins de connaître tous les écueils et de savoir exactement ce que vous faites.

///

## Ajouter un modèle de sortie { #add-an-output-model }

Nous pouvons à la place créer un modèle d'entrée avec le mot de passe en clair et un modèle de sortie sans celui-ci :

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

Ici, même si notre *fonction de chemin d'accès* renvoie le même utilisateur d'entrée qui contient le mot de passe :

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

... nous avons déclaré `response_model` comme étant notre modèle `UserOut`, qui n'inclut pas le mot de passe :

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

Ainsi, **FastAPI** se chargera de filtrer toutes les données qui ne sont pas déclarées dans le modèle de sortie (en utilisant Pydantic).

### `response_model` ou type de retour { #response-model-or-return-type }

Dans ce cas, comme les deux modèles sont différents, si nous annotions le type de retour de la fonction en `UserOut`, l’éditeur et les outils se plaindraient que nous renvoyons un type invalide, car ce sont des classes différentes.

C'est pourquoi, dans cet exemple, nous devons le déclarer dans le paramètre `response_model`.

... mais continuez à lire ci-dessous pour voir comment contourner cela.

## Type de retour et filtrage des données { #return-type-and-data-filtering }

Continuons l'exemple précédent. Nous voulions **annoter la fonction avec un type**, mais nous voulions pouvoir renvoyer depuis la fonction quelque chose qui inclut **plus de données**.

Nous voulons que FastAPI continue de **filtrer** les données à l’aide du modèle de réponse. Ainsi, même si la fonction renvoie plus de données, la réponse n’inclura que les champs déclarés dans le modèle de réponse.

Dans l'exemple précédent, comme les classes étaient différentes, nous avons dû utiliser le paramètre `response_model`. Mais cela signifie aussi que nous ne bénéficions pas de la prise en charge de l'éditeur et des outils pour la vérification du type de retour de la fonction.

Mais dans la plupart des cas où nous avons besoin de quelque chose comme cela, nous voulons que le modèle **filtre/supprime** simplement une partie des données comme dans cet exemple.

Et dans ces cas, nous pouvons utiliser des classes et l'héritage pour tirer parti des **annotations de type** de fonction afin d'obtenir une meilleure prise en charge dans l'éditeur et les outils, tout en bénéficiant du **filtrage de données** de FastAPI.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

Avec cela, nous obtenons la prise en charge des outils, des éditeurs et de mypy car ce code est correct en termes de types, et nous bénéficions également du filtrage des données par FastAPI.

Comment cela fonctionne-t-il ? Voyons cela. 🤓

### Annotations de type et outils { #type-annotations-and-tooling }

Voyons d'abord comment les éditeurs, mypy et autres outils considèreraient cela.

`BaseUser` a les champs de base. Puis `UserIn` hérite de `BaseUser` et ajoute le champ `password`, il inclura donc tous les champs des deux modèles.

Nous annotons le type de retour de la fonction en `BaseUser`, mais nous renvoyons en réalité une instance de `UserIn`.

L’éditeur, mypy et d'autres outils ne s’en plaindront pas car, en termes de typage, `UserIn` est une sous-classe de `BaseUser`, ce qui signifie que c’est un type *valide* lorsque ce qui est attendu est n'importe quoi de type `BaseUser`.

### Filtrage des données par FastAPI { #fastapi-data-filtering }

Maintenant, pour FastAPI, il verra le type de retour et s'assurera que ce que vous renvoyez inclut **uniquement** les champs qui sont déclarés dans le type.

FastAPI fait plusieurs choses en interne avec Pydantic pour s'assurer que ces mêmes règles d'héritage de classes ne sont pas utilisées pour le filtrage des données renvoyées, sinon vous pourriez finir par renvoyer beaucoup plus de données que prévu.

De cette façon, vous obtenez le meilleur des deux mondes : annotations de type avec **prise en charge par les outils** et **filtrage des données**.

## Le voir dans la documentation { #see-it-in-the-docs }

Dans la documentation automatique, vous pouvez vérifier que le modèle d'entrée et le modèle de sortie auront chacun leur propre JSON Schema :

<img src="/img/tutorial/response-model/image01.png">

Et les deux modèles seront utilisés pour la documentation API interactive :

<img src="/img/tutorial/response-model/image02.png">

## Autres annotations de type de retour { #other-return-type-annotations }

Il peut y avoir des cas où vous renvoyez quelque chose qui n'est pas un champ Pydantic valide et vous l'annotez dans la fonction, uniquement pour obtenir la prise en charge fournie par les outils (l’éditeur, mypy, etc.).

### Renvoyer directement une Response { #return-a-response-directly }

Le cas le plus courant serait [de renvoyer directement une Response comme expliqué plus loin dans la documentation avancée](../advanced/response-directly.md){.internal-link target=_blank}.

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

Ce cas simple est géré automatiquement par FastAPI car l'annotation du type de retour est la classe (ou une sous-classe de) `Response`.

Et les outils seront également satisfaits car `RedirectResponse` et `JSONResponse` sont des sous-classes de `Response`, donc l'annotation de type est correcte.

### Annoter une sous-classe de Response { #annotate-a-response-subclass }

Vous pouvez aussi utiliser une sous-classe de `Response` dans l'annotation de type :

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

Cela fonctionnera également car `RedirectResponse` est une sous-classe de `Response`, et FastAPI gérera automatiquement ce cas simple.

### Annotations de type de retour invalides { #invalid-return-type-annotations }

Mais lorsque vous renvoyez un autre objet arbitraire qui n'est pas un type Pydantic valide (par exemple un objet de base de données) et que vous l'annotez ainsi dans la fonction, FastAPI essaiera de créer un modèle de réponse Pydantic à partir de cette annotation de type, et échouera.

Il en serait de même si vous aviez quelque chose comme une <dfn title="Une union entre plusieurs types signifie « n'importe lequel de ces types ».">union</dfn> entre différents types dont un ou plusieurs ne sont pas des types Pydantic valides, par exemple ceci échouerait 💥 :

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

... cela échoue parce que l'annotation de type n'est pas un type Pydantic et n'est pas juste une unique classe `Response` ou une sous-classe, c'est une union (l'un des deux) entre une `Response` et un `dict`.

### Désactiver le modèle de réponse { #disable-response-model }

En reprenant l'exemple ci-dessus, vous pourriez ne pas vouloir avoir la validation par défaut des données, la documentation, le filtrage, etc. effectués par FastAPI.

Mais vous pourriez vouloir tout de même conserver l’annotation du type de retour dans la fonction pour bénéficier de la prise en charge des outils comme les éditeurs et les vérificateurs de type (par exemple mypy).

Dans ce cas, vous pouvez désactiver la génération du modèle de réponse en définissant `response_model=None` :

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

Cela fera en sorte que FastAPI ignore la génération du modèle de réponse et vous permettra ainsi d’avoir toutes les annotations de type de retour dont vous avez besoin sans que cela n’affecte votre application FastAPI. 🤓

## Paramètres d'encodage du modèle de réponse { #response-model-encoding-parameters }

Votre modèle de réponse peut avoir des valeurs par défaut, par exemple :

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (ou `str | None = None` en Python 3.10) a une valeur par défaut `None`.
* `tax: float = 10.5` a une valeur par défaut `10.5`.
* `tags: List[str] = []` a une valeur par défaut de liste vide : `[]`.

mais vous pourriez vouloir les omettre du résultat si elles n'ont pas été réellement stockées.

Par exemple, si vous avez des modèles avec de nombreux attributs optionnels dans une base NoSQL, mais que vous ne voulez pas envoyer de très longues réponses JSON remplies de valeurs par défaut.

### Utiliser le paramètre `response_model_exclude_unset` { #use-the-response-model-exclude-unset-parameter }

Vous pouvez définir le paramètre du *décorateur de chemin d'accès* `response_model_exclude_unset=True` :

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

et ces valeurs par défaut ne seront pas incluses dans la réponse, uniquement les valeurs effectivement définies.

Ainsi, si vous envoyez une requête à ce *chemin d'accès* pour l'article avec l'ID `foo`, la réponse (sans les valeurs par défaut) sera :

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | Info

Vous pouvez également utiliser :

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

comme décrit dans <a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">la documentation Pydantic</a> pour `exclude_defaults` et `exclude_none`.

///

#### Données avec des valeurs pour des champs avec des valeurs par défaut { #data-with-values-for-fields-with-defaults }

Mais si vos données ont des valeurs pour les champs du modèle avec des valeurs par défaut, comme l'article avec l'ID `bar` :

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

elles seront incluses dans la réponse.

#### Données avec les mêmes valeurs que les valeurs par défaut { #data-with-the-same-values-as-the-defaults }

Si les données ont les mêmes valeurs que les valeurs par défaut, comme l'article avec l'ID `baz` :

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI est suffisamment intelligent (en fait, Pydantic l’est) pour comprendre que, même si `description`, `tax` et `tags` ont les mêmes valeurs que les valeurs par défaut, elles ont été définies explicitement (au lieu d'être prises depuis les valeurs par défaut).

Elles seront donc incluses dans la réponse JSON.

/// tip | Astuce

Notez que les valeurs par défaut peuvent être n'importe quoi, pas seulement `None`.

Elles peuvent être une liste (`[]`), un `float` de `10.5`, etc.

///

### `response_model_include` et `response_model_exclude` { #response-model-include-and-response-model-exclude }

Vous pouvez également utiliser les paramètres du *décorateur de chemin d'accès* `response_model_include` et `response_model_exclude`.

Ils prennent un `set` de `str` avec les noms des attributs à inclure (en omettant le reste) ou à exclure (en incluant le reste).

Cela peut être utilisé comme un raccourci rapide si vous n'avez qu'un seul modèle Pydantic et que vous souhaitez supprimer certaines données de la sortie.

/// tip | Astuce

Mais il est toujours recommandé d'utiliser les idées ci-dessus, en utilisant plusieurs classes, plutôt que ces paramètres.

En effet, le JSON Schema généré dans l’OpenAPI de votre application (et la documentation) restera celui du modèle complet, même si vous utilisez `response_model_include` ou `response_model_exclude` pour omettre certains attributs.

Cela s'applique également à `response_model_by_alias` qui fonctionne de manière similaire.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | Astuce

La syntaxe `{"name", "description"}` crée un `set` avec ces deux valeurs.

Elle est équivalente à `set(["name", "description"])`.

///

#### Utiliser des `list` au lieu de `set` { #using-lists-instead-of-sets }

Si vous oubliez d'utiliser un `set` et utilisez une `list` ou un `tuple` à la place, FastAPI le convertira quand même en `set` et cela fonctionnera correctement :

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Récapitulatif { #recap }

Utilisez le paramètre du *décorateur de chemin d'accès* `response_model` pour définir les modèles de réponse et surtout pour garantir que les données privées sont filtrées.

Utilisez `response_model_exclude_unset` pour ne renvoyer que les valeurs définies explicitement.
