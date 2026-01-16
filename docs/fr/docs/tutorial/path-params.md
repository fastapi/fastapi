# Paramètres de chemin { #path-parameters }

Vous pouvez déclarer des « paramètres » ou « variables » de chemin avec la même syntaxe que celle utilisée par les chaînes de format Python :

{* ../../docs_src/path_params/tutorial001_py39.py hl[6:7] *}

La valeur du paramètre de chemin `item_id` sera transmise à votre fonction comme argument `item_id`.

Donc, si vous exécutez cet exemple et allez sur <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, vous verrez comme réponse :

```JSON
{"item_id":"foo"}
```

## Paramètres de chemin typés { #path-parameters-with-types }

Vous pouvez déclarer le type d'un paramètre de chemin dans la fonction, en utilisant les annotations de type standard de Python :

{* ../../docs_src/path_params/tutorial002_py39.py hl[7] *}

Dans ce cas, `item_id` est déclaré comme `int`.

/// check | Vérifications

Cela vous donnera le support de l'éditeur dans votre fonction, avec des vérifications d'erreurs, l'autocomplétion, etc.

///

## <abbr title="aussi connu sous le nom de : serialization, parsing, marshalling">Conversion</abbr> de données { #data-conversion }

Si vous exécutez cet exemple et ouvrez votre navigateur sur <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, vous verrez comme réponse :

```JSON
{"item_id":3}
```

/// check | Vérifications

Remarquez que la valeur reçue par votre fonction (et renvoyée) est `3`, comme un `int` Python, pas une chaîne « 3 ».

Ainsi, avec cette déclaration de type, **FastAPI** vous fournit le <abbr title="conversion de la chaîne provenant d'une requête HTTP en données Python">« parsing »</abbr> automatique de la requête.

///

## Validation de données { #data-validation }

Mais si vous allez dans le navigateur sur <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, vous verrez une belle erreur HTTP :

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

car le paramètre de chemin `item_id` avait la valeur « foo », qui n'est pas un `int`.

La même erreur apparaîtrait si vous fournissiez un `float` au lieu d'un `int`, comme ici : <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check | Vérifications

Ainsi, avec la même déclaration de type Python, **FastAPI** vous fournit une validation de données.

Remarquez que l'erreur indique aussi clairement le point exact où la validation n'est pas passée.

C'est incroyablement utile lors du développement et du débogage de code qui interagit avec votre API.

///

## Documentation { #documentation }

Et lorsque vous ouvrez votre navigateur sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, vous verrez une documentation d'API automatique et interactive comme :

<img src="/img/tutorial/path-params/image01.png">

/// check | Vérifications

Encore une fois, uniquement avec cette même déclaration de type Python, **FastAPI** vous fournit une documentation automatique et interactive (intégrant Swagger UI).

Remarquez que le paramètre de chemin est déclaré comme un entier.

///

## Avantages basés sur les standards, documentation alternative { #standards-based-benefits-alternative-documentation }

Et comme le schéma généré provient du standard <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>, il existe de nombreux outils compatibles.

Grâce à cela, **FastAPI** lui-même fournit une documentation d'API alternative (utilisant ReDoc), à laquelle vous pouvez accéder sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> :

<img src="/img/tutorial/path-params/image02.png">

De la même façon, il existe de nombreux outils compatibles. Y compris des outils de génération de code pour de nombreux langages.

## Pydantic { #pydantic }

Toute la validation de données est effectuée en arrière-plan par <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, vous bénéficiez donc de tous ses avantages. Et vous savez que vous êtes entre de bonnes mains.

Vous pouvez utiliser les mêmes déclarations de type avec `str`, `float`, `bool` et de nombreux autres types de données complexes.

Plusieurs d'entre eux sont abordés dans les prochains chapitres du tutoriel.

## L'ordre importe { #order-matters }

Lors de la création de *chemins d'accès*, vous pouvez vous retrouver dans des situations où vous avez un chemin fixe.

Comme `/users/me`, disons que c'est pour obtenir des données sur l'utilisateur actuel.

Et vous pouvez aussi avoir un chemin `/users/{user_id}` pour obtenir des données sur un utilisateur spécifique via un identifiant utilisateur.

Comme les *chemins d'accès* sont évalués dans l'ordre, vous devez vous assurer que le chemin pour `/users/me` est déclaré avant celui pour `/users/{user_id}` :

{* ../../docs_src/path_params/tutorial003_py39.py hl[6,11] *}

Sinon, le chemin pour `/users/{user_id}` correspondrait aussi à `/users/me`, en « pensant » qu'il reçoit un paramètre `user_id` avec la valeur « me ».

De la même manière, vous ne pouvez pas redéfinir un chemin d'accès :

{* ../../docs_src/path_params/tutorial003b_py39.py hl[6,11] *}

Le premier sera toujours utilisé puisque le chemin correspond en premier.

## Valeurs prédéfinies { #predefined-values }

Si vous avez un *chemin d'accès* qui reçoit un *paramètre de chemin*, mais que vous voulez que les valeurs valides possibles du *paramètre de chemin* soient prédéfinies, vous pouvez utiliser un <abbr title="Enumeration">`Enum`</abbr> Python standard.

### Créer une classe `Enum` { #create-an-enum-class }

Importez `Enum` et créez une sous-classe qui hérite de `str` et de `Enum`.

En héritant de `str`, les documents de l'API pourront savoir que les valeurs doivent être de type `string` et pourront les afficher correctement.

Créez ensuite des attributs de classe avec des valeurs fixes, qui seront les valeurs valides disponibles :

{* ../../docs_src/path_params/tutorial005_py39.py hl[1,6:9] *}

/// tip | Astuce

Si vous vous demandez, « AlexNet », « ResNet » et « LeNet » sont simplement des noms de <abbr title="Technically, Deep Learning model architectures">modèles</abbr> de Machine Learning.

///

### Déclarer un *paramètre de chemin* { #declare-a-path-parameter }

Créez ensuite un *paramètre de chemin* avec une annotation de type utilisant la classe enum que vous avez créée (`ModelName`) :

{* ../../docs_src/path_params/tutorial005_py39.py hl[16] *}

### Vérifier la documentation { #check-the-docs }

Comme les valeurs disponibles pour le *paramètre de chemin* sont prédéfinies, la documentation interactive peut bien les afficher :

<img src="/img/tutorial/path-params/image03.png">

### Travailler avec les *énumérations* Python { #working-with-python-enumerations }

La valeur du *paramètre de chemin* sera un *membre d'énumération*.

#### Comparer des *membres d'énumération* { #compare-enumeration-members }

Vous pouvez la comparer avec le *membre d'énumération* de votre enum créée `ModelName` :

{* ../../docs_src/path_params/tutorial005_py39.py hl[17] *}

#### Obtenir la *valeur de l'énumération* { #get-the-enumeration-value }

Vous pouvez obtenir la valeur réelle (un `str` dans ce cas) en utilisant `model_name.value`, ou de manière générale, `your_enum_member.value` :

{* ../../docs_src/path_params/tutorial005_py39.py hl[20] *}

/// tip | Astuce

Vous pouvez aussi accéder à la valeur « lenet » avec `ModelName.lenet.value`.

///

#### Retourner des *membres d'énumération* { #return-enumeration-members }

Vous pouvez retourner des *membres d'enum* depuis votre *chemin d'accès*, même imbriqués dans un corps JSON (par ex. un `dict`).

Ils seront convertis en leurs valeurs correspondantes (des chaînes dans ce cas) avant de les renvoyer au client :

{* ../../docs_src/path_params/tutorial005_py39.py hl[18,21,23] *}

Dans votre client, vous obtiendrez une réponse JSON comme :

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Paramètres de chemin contenant des chemins { #path-parameters-containing-paths }

Disons que vous avez un *chemin d'accès* avec le chemin `/files/{file_path}`.

Mais vous avez besoin que `file_path` lui-même contienne un *chemin*, comme `home/johndoe/myfile.txt`.

Donc, l'URL pour ce fichier serait quelque chose comme : `/files/home/johndoe/myfile.txt`.

### Support d'OpenAPI { #openapi-support }

OpenAPI ne supporte pas une manière de déclarer qu'un *paramètre de chemin* contient un *chemin* à l'intérieur, car cela pourrait conduire à des scénarios difficiles à tester et à définir.

Néanmoins, vous pouvez quand même le faire dans **FastAPI**, en utilisant un des outils internes de Starlette.

Et les documents fonctionneraient quand même, bien qu'ils n'ajoutent aucune documentation indiquant que le paramètre devrait contenir un chemin.

### Convertisseur de chemin { #path-convertor }

En utilisant une option directement depuis Starlette, vous pouvez déclarer un *paramètre de chemin* contenant un *chemin* avec une URL comme :

```
/files/{file_path:path}
```

Dans ce cas, le nom du paramètre est `file_path`, et la dernière partie, `:path`, indique que le paramètre doit correspondre à n'importe quel *chemin*.

Ainsi, vous pouvez l'utiliser avec :

{* ../../docs_src/path_params/tutorial004_py39.py hl[6] *}

/// tip | Astuce

Vous pourriez avoir besoin que le paramètre contienne `/home/johndoe/myfile.txt`, avec un slash initial (`/`).

Dans ce cas, l'URL serait : `/files//home/johndoe/myfile.txt`, avec un double slash (`//`) entre `files` et `home`.

///

## Récapitulatif { #recap }

Avec **FastAPI**, en utilisant des déclarations de type Python courtes, intuitives et standard, vous obtenez :

* Support de l'éditeur : vérifications d'erreurs, autocomplétion, etc.
* « parsing » de données <abbr title="conversion de la chaîne provenant d'une requête HTTP en données Python">parsing</abbr>
* Validation de données
* Annotation de l'API et documentation automatique

Et vous n'avez à les déclarer qu'une seule fois.

C'est probablement le principal avantage visible de **FastAPI** comparé aux frameworks alternatifs (en dehors de la performance brute).
