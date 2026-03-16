# Paramètres de chemin { #path-parameters }

Vous pouvez déclarer des « paramètres » ou « variables » de chemin avec la même syntaxe utilisée par les chaînes de format Python :

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

La valeur du paramètre de chemin `item_id` sera transmise à votre fonction dans l'argument `item_id`.

Donc, si vous exécutez cet exemple et allez sur <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, vous verrez comme réponse :

```JSON
{"item_id":"foo"}
```

## Paramètres de chemin typés { #path-parameters-with-types }

Vous pouvez déclarer le type d'un paramètre de chemin dans la fonction, en utilisant les annotations de type Python standard :

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

Ici, `item_id` est déclaré comme `int`.

/// check | Vérifications

Cela vous apporte la prise en charge par l'éditeur dans votre fonction, avec vérifications d'erreurs, autocomplétion, etc.

///

## <dfn title="également appelé : sérialisation, parsing, marshalling">Conversion</dfn> de données { #data-conversion }

Si vous exécutez cet exemple et ouvrez votre navigateur sur <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, vous verrez comme réponse :

```JSON
{"item_id":3}
```

/// check | Vérifications

Remarquez que la valeur reçue par votre fonction (et renvoyée) est `3`, en tant qu'entier (`int`) Python, pas la chaîne de caractères « 3 ».

Ainsi, avec cette déclaration de type, **FastAPI** vous fournit automatiquement le <dfn title="conversion de la chaîne de caractères provenant d'une requête HTTP en données Python">« parsing »</dfn> de la requête.

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

car le paramètre de chemin `item_id` a pour valeur « foo », qui n'est pas un `int`.

La même erreur apparaîtrait si vous fournissiez un `float` au lieu d'un `int`, comme ici : <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check | Vérifications

Ainsi, avec la même déclaration de type Python, **FastAPI** vous fournit la validation de données.

Remarquez que l'erreur indique clairement l'endroit exact où la validation n'a pas réussi.

C'est incroyablement utile lors du développement et du débogage du code qui interagit avec votre API.

///

## Documentation { #documentation }

Et lorsque vous ouvrez votre navigateur sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, vous verrez une documentation d'API automatique et interactive comme :

<img src="/img/tutorial/path-params/image01.png">

/// check | Vérifications

À nouveau, simplement avec cette même déclaration de type Python, **FastAPI** vous fournit une documentation interactive automatique (intégrant Swagger UI).

Remarquez que le paramètre de chemin est déclaré comme entier.

///

## Les avantages d'une norme, documentation alternative { #standards-based-benefits-alternative-documentation }

Et comme le schéma généré suit la norme <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>, il existe de nombreux outils compatibles.

Grâce à cela, **FastAPI** fournit lui-même une documentation d'API alternative (utilisant ReDoc), accessible sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> :

<img src="/img/tutorial/path-params/image02.png">

De la même façon, il existe de nombreux outils compatibles, y compris des outils de génération de code pour de nombreux langages.

## Pydantic { #pydantic }

Toute la validation de données est effectuée sous le capot par <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, vous en bénéficiez donc pleinement. Vous savez ainsi que vous êtes entre de bonnes mains.

Vous pouvez utiliser les mêmes déclarations de type avec `str`, `float`, `bool` et de nombreux autres types de données complexes.

Plusieurs d'entre eux sont explorés dans les prochains chapitres du tutoriel.

## L'ordre importe { #order-matters }

Quand vous créez des *chemins d'accès*, vous pouvez vous retrouver dans une situation avec un chemin fixe.

Par exemple `/users/me`, disons pour récupérer les données de l'utilisateur actuel.

Et vous pouvez aussi avoir un chemin `/users/{user_id}` pour récupérer des données sur un utilisateur spécifique grâce à un identifiant d'utilisateur.

Comme les *chemins d'accès* sont évalués dans l'ordre, vous devez vous assurer que le chemin `/users/me` est déclaré avant celui de `/users/{user_id}` :

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

Sinon, le chemin `/users/{user_id}` correspondrait aussi à `/users/me`, « pensant » qu'il reçoit un paramètre `user_id` avec la valeur « me ».

De même, vous ne pouvez pas redéfinir un chemin d'accès :

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

Le premier sera toujours utilisé puisque le chemin correspond en premier.

## Valeurs prédéfinies { #predefined-values }

Si vous avez un *chemin d'accès* qui reçoit un *paramètre de chemin*, mais que vous voulez que les valeurs possibles de ce *paramètre de chemin* soient prédéfinies, vous pouvez utiliser une <abbr title="Enumeration - Énumération">`Enum`</abbr> Python standard.

### Créer une classe `Enum` { #create-an-enum-class }

Importez `Enum` et créez une sous-classe qui hérite de `str` et de `Enum`.

En héritant de `str`, la documentation de l'API saura que les valeurs doivent être de type `string` et pourra donc s'afficher correctement.

Créez ensuite des attributs de classe avec des valeurs fixes, qui seront les valeurs valides disponibles :

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | Astuce

Si vous vous demandez, « AlexNet », « ResNet » et « LeNet » sont juste des noms de <dfn title="Techniquement, architectures de modèles de Deep Learning">modèles</dfn> de Machine Learning.

///

### Déclarer un paramètre de chemin { #declare-a-path-parameter }

Créez ensuite un *paramètre de chemin* avec une annotation de type utilisant la classe d'énumération que vous avez créée (`ModelName`) :

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### Consulter la documentation { #check-the-docs }

Comme les valeurs disponibles pour le *paramètre de chemin* sont prédéfinies, la documentation interactive peut les afficher clairement :

<img src="/img/tutorial/path-params/image03.png">

### Travailler avec les *énumérations* Python { #working-with-python-enumerations }

La valeur du *paramètre de chemin* sera un *membre d'énumération*.

#### Comparer des *membres d'énumération* { #compare-enumeration-members }

Vous pouvez le comparer avec le *membre d'énumération* dans votre enum `ModelName` :

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### Obtenir la *valeur de l'énumération* { #get-the-enumeration-value }

Vous pouvez obtenir la valeur réelle (une `str` dans ce cas) avec `model_name.value`, ou en général, `votre_membre_d_enum.value` :

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | Astuce

Vous pouvez aussi accéder à la valeur « lenet » avec `ModelName.lenet.value`.

///

#### Retourner des *membres d'énumération* { #return-enumeration-members }

Vous pouvez retourner des *membres d'énumération* depuis votre *chemin d'accès*, même imbriqués dans un corps JSON (par ex. un `dict`).

Ils seront convertis vers leurs valeurs correspondantes (des chaînes de caractères ici) avant d'être renvoyés au client :

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

Dans votre client, vous recevrez une réponse JSON comme :

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Paramètres de chemin contenant des chemins { #path-parameters-containing-paths }

Disons que vous avez un *chemin d'accès* avec un chemin `/files/{file_path}`.

Mais vous avez besoin que `file_path` lui-même contienne un *chemin*, comme `home/johndoe/myfile.txt`.

Ainsi, l'URL pour ce fichier serait : `/files/home/johndoe/myfile.txt`.

### Support d'OpenAPI { #openapi-support }

OpenAPI ne prend pas en charge une manière de déclarer un *paramètre de chemin* contenant un *chemin* à l'intérieur, car cela peut conduire à des scénarios difficiles à tester et à définir.

Néanmoins, vous pouvez toujours le faire dans **FastAPI**, en utilisant l'un des outils internes de Starlette.

Et la documentation fonctionnera quand même, même si aucune indication supplémentaire ne sera ajoutée pour dire que le paramètre doit contenir un chemin.

### Convertisseur de chemin { #path-convertor }

En utilisant une option directement depuis Starlette, vous pouvez déclarer un *paramètre de chemin* contenant un *chemin* avec une URL comme :

```
/files/{file_path:path}
```

Dans ce cas, le nom du paramètre est `file_path`, et la dernière partie, `:path`, indique que le paramètre doit correspondre à n'importe quel *chemin*.

Vous pouvez donc l'utiliser ainsi :

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | Astuce

Vous pourriez avoir besoin que le paramètre contienne `/home/johndoe/myfile.txt`, avec un slash initial (`/`).

Dans ce cas, l'URL serait : `/files//home/johndoe/myfile.txt`, avec un double slash (`//`) entre `files` et `home`.

///

## Récapitulatif { #recap }

Avec **FastAPI**, en utilisant des déclarations de type Python courtes, intuitives et standard, vous obtenez :

* Support de l'éditeur : vérifications d'erreurs, autocomplétion, etc.
* Données « <dfn title="conversion de la chaîne de caractères provenant d'une requête HTTP en données Python">parsing</dfn> »
* Validation de données
* Annotations d'API et documentation automatique

Et vous n'avez besoin de les déclarer qu'une seule fois.

C'est probablement l'avantage visible principal de **FastAPI** comparé aux autres frameworks (outre les performances pures).
