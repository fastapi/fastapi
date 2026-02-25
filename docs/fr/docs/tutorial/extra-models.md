# Modèles supplémentaires { #extra-models }

En poursuivant l'exemple précédent, il est courant d'avoir plusieurs modèles liés.

C'est particulièrement vrai pour les modèles d'utilisateur, car :

* Le modèle d'entrée doit pouvoir contenir un mot de passe.
* Le modèle de sortie ne doit pas avoir de mot de passe.
* Le modèle de base de données devra probablement avoir un mot de passe haché.

/// danger | Danger

Ne stockez jamais les mots de passe des utilisateurs en clair. Stockez toujours un « hachage sécurisé » que vous pourrez ensuite vérifier.

Si vous ne savez pas ce que c'est, vous apprendrez ce qu'est un « hachage de mot de passe » dans les [chapitres sur la sécurité](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.

///

## Utiliser plusieurs modèles { #multiple-models }

Voici une idée générale de l'apparence des modèles avec leurs champs de mot de passe et les endroits où ils sont utilisés :

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### À propos de `**user_in.model_dump()` { #about-user-in-model-dump }

#### La méthode `.model_dump()` de Pydantic { #pydantics-model-dump }

`user_in` est un modèle Pydantic de classe `UserIn`.

Les modèles Pydantic ont une méthode `.model_dump()` qui renvoie un `dict` avec les données du modèle.

Ainsi, si nous créons un objet Pydantic `user_in` comme :

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

et que nous appelons ensuite :

```Python
user_dict = user_in.model_dump()
```

nous avons maintenant un `dict` avec les données dans la variable `user_dict` (c'est un `dict` au lieu d'un objet modèle Pydantic).

Et si nous appelons :

```Python
print(user_dict)
```

nous obtiendrions un `dict` Python contenant :

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Déballer un `dict` { #unpacking-a-dict }

Si nous prenons un `dict` comme `user_dict` et que nous le passons à une fonction (ou une classe) avec `**user_dict`, Python va « déballer » ce `dict`. Il passera les clés et valeurs de `user_dict` directement comme arguments nommés.

Ainsi, en reprenant `user_dict` ci-dessus, écrire :

```Python
UserInDB(**user_dict)
```

aurait pour résultat quelque chose d'équivalent à :

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Ou plus exactement, en utilisant `user_dict` directement, quels que soient ses contenus futurs :

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Créer un modèle Pydantic à partir du contenu d'un autre { #a-pydantic-model-from-the-contents-of-another }

Comme dans l'exemple ci-dessus nous avons obtenu `user_dict` depuis `user_in.model_dump()`, ce code :

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

serait équivalent à :

```Python
UserInDB(**user_in.model_dump())
```

... parce que `user_in.model_dump()` est un `dict`, et nous demandons ensuite à Python de « déballer » ce `dict` en le passant à `UserInDB` précédé de `**`.

Ainsi, nous obtenons un modèle Pydantic à partir des données d'un autre modèle Pydantic.

#### Déballer un `dict` et ajouter des mots-clés supplémentaires { #unpacking-a-dict-and-extra-keywords }

Et en ajoutant ensuite l'argument nommé supplémentaire `hashed_password=hashed_password`, comme ici :

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

... revient à :

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | Alertes

Les fonctions auxiliaires `fake_password_hasher` et `fake_save_user` ne servent qu'à démontrer un flux de données possible, mais elles n'offrent évidemment aucune sécurité réelle.

///

## Réduire la duplication { #reduce-duplication }

Réduire la duplication de code est l'une des idées centrales de **FastAPI**.

La duplication de code augmente les risques de bogues, de problèmes de sécurité, de désynchronisation du code (lorsque vous mettez à jour un endroit mais pas les autres), etc.

Et ces modèles partagent beaucoup de données et dupliquent des noms et types d'attributs.

Nous pouvons faire mieux.

Nous pouvons déclarer un modèle `UserBase` qui sert de base à nos autres modèles. Ensuite, nous pouvons créer des sous-classes de ce modèle qui héritent de ses attributs (déclarations de type, validation, etc.).

Toutes les conversions de données, validations, documentation, etc., fonctionneront comme d'habitude.

De cette façon, nous pouvons ne déclarer que les différences entre les modèles (avec `password` en clair, avec `hashed_password` et sans mot de passe) :

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` ou `anyOf` { #union-or-anyof }

Vous pouvez déclarer qu'une réponse est l'`Union` de deux types ou plus, ce qui signifie que la réponse peut être n'importe lequel d'entre eux.

Cela sera défini dans OpenAPI avec `anyOf`.

Pour ce faire, utilisez l'annotation de type Python standard <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a> :

/// note | Remarque

Lors de la définition d'une <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a>, incluez d'abord le type le plus spécifique, suivi du type le moins spécifique. Dans l'exemple ci-dessous, le type le plus spécifique `PlaneItem` précède `CarItem` dans `Union[PlaneItem, CarItem]`.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### `Union` en Python 3.10 { #union-in-python-3-10 }

Dans cet exemple, nous passons `Union[PlaneItem, CarItem]` comme valeur de l'argument `response_model`.

Comme nous le passons comme valeur d'un argument au lieu de l'utiliser dans une annotation de type, nous devons utiliser `Union` même en Python 3.10.

S'il s'agissait d'une annotation de type, nous pourrions utiliser la barre verticale, comme :

```Python
some_variable: PlaneItem | CarItem
```

Mais si nous écrivons cela dans l'affectation `response_model=PlaneItem | CarItem`, nous obtiendrons une erreur, car Python essaierait d'effectuer une « opération invalide » entre `PlaneItem` et `CarItem` au lieu de l'interpréter comme une annotation de type.

## Liste de modèles { #list-of-models }

De la même manière, vous pouvez déclarer des réponses contenant des listes d'objets.

Pour cela, utilisez le `list` Python standard :

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## Réponse avec un `dict` arbitraire { #response-with-arbitrary-dict }

Vous pouvez également déclarer une réponse en utilisant un simple `dict` arbitraire, en déclarant uniquement le type des clés et des valeurs, sans utiliser de modèle Pydantic.

C'est utile si vous ne connaissez pas à l'avance les noms de champs/attributs valides (qui seraient nécessaires pour un modèle Pydantic).

Dans ce cas, vous pouvez utiliser `dict` :

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## Récapitulatif { #recap }

Utilisez plusieurs modèles Pydantic et héritez librement selon chaque cas.

Vous n'avez pas besoin d'avoir un seul modèle de données par entité si cette entité doit pouvoir avoir différents « états ». Comme pour l'« entité » utilisateur, avec un état incluant `password`, `password_hash` et sans mot de passe.
