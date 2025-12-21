# Paramètres de chemin { #path-parameters }

Vous pouvez déclarer des «paramètres» ou «variables» de chemin avec la même syntaxe que celle utilisée par les chaînes de formatage Python :

{* ../../docs_src/path_params/tutorial001_py39.py hl[6:7] *}

La valeur du paramètre de chemin `item_id` sera transmise à la fonction dans l'argument `item_id`.

Donc, si vous exécutez cet exemple et allez sur <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, vous verrez comme réponse :

```JSON
{"item_id":"foo"}
```

## Paramètres de chemin typés { #path-parameters-with-types }

Vous pouvez déclarer le type d'un paramètre de chemin dans la fonction, en utilisant les annotations de type Python standard :

{* ../../docs_src/path_params/tutorial002_py39.py hl[7] *}

Ici, `item_id` est déclaré comme `int`.

/// check | vérifier

Ceci vous permettra d'obtenir des fonctionnalités de l'éditeur dans votre fonction, telles que des vérifications d'erreurs, de l'autocomplétion, etc.

///

## <abbr title="aussi connu sous le nom : sérialisation, parsing, marshalling">Conversion</abbr> de données { #data-conversion }

Si vous exécutez cet exemple et allez sur <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, vous aurez comme réponse :

```JSON
{"item_id":3}
```

/// check | vérifier

Comme vous l'avez remarqué, la valeur reçue par la fonction (et renvoyée ensuite) est `3`,
en tant qu'entier (`int`) Python, pas la chaîne de caractères (`string`) «3».

Donc, avec cette déclaration de type, **FastAPI** vous fournit un <abbr title="conversion de la chaîne de caractères venant de la requête HTTP en données Python">«parsing»</abbr> de la requête automatique.

///

## Validation de données { #data-validation }

Si vous allez sur <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, vous aurez une belle erreur HTTP :

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

car le paramètre de chemin `item_id` possède comme valeur «foo», qui n'est pas un `int`.

La même erreur se produira si vous passez un nombre flottant (`float`) et non un entier, comme ici
<a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>.

/// check | vérifier

Donc, avec ces mêmes déclarations de type Python, **FastAPI** vous fournit de la validation de données.

Notez que l'erreur mentionne le point exact où la validation n'a pas réussi.

Ce qui est incroyablement utile au moment de développer et débugger du code qui interagit avec votre API.

///

## Documentation { #documentation }

Et quand vous vous rendez sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, vous verrez la
documentation générée automatiquement et interactive :

<img src="/img/tutorial/path-params/image01.png">

/// check | vérifier

À nouveau, en utilisant uniquement les déclarations de type Python, **FastAPI** vous fournit automatiquement une documentation interactive (intégrant Swagger UI).

On voit bien dans la documentation que `item_id` est déclaré comme entier.

///

## Les avantages d'avoir une documentation basée sur une norme, et la documentation alternative { #standards-based-benefits-alternative-documentation }

Le schéma généré suivant la norme <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>,
il existe de nombreux outils compatibles.

Grâce à cela, **FastAPI** lui-même fournit une documentation alternative (utilisant ReDoc), qui peut être lue
sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> :

<img src="/img/tutorial/path-params/image02.png">

De la même façon, il existe bien d'autres outils compatibles, y compris des outils de génération de code
pour de nombreux langages.

## Pydantic { #pydantic }

Toute la validation de données est effectuée en arrière-plan avec <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>,
dont vous bénéficierez de tous les avantages. Vous savez donc que vous êtes entre de bonnes mains.

Vous pouvez utiliser les mêmes déclarations de type avec `str`, `float`, `bool` et de nombreux autres types de données complexes.

Plusieurs d'entre eux sont explorés dans les prochains chapitres du tutoriel.

## L'ordre importe { #order-matters }

Quand vous créez des *opérations de chemin*, vous pouvez vous retrouver dans une situation où vous avez un chemin fixe.

Tel que `/users/me`, disons pour récupérer les données sur l'utilisateur actuel.

Et vous avez un second chemin : `/users/{user_id}` pour récupérer de la donnée sur un utilisateur spécifique grâce à son identifiant d'utilisateur

Les *opérations de chemin* étant évaluées dans l'ordre, il faut s'assurer que la fonction correspondant à `/users/me` est déclarée avant celle de `/users/{user_id}` :

{* ../../docs_src/path_params/tutorial003_py39.py hl[6,11] *}

Sinon, le chemin `/users/{user_id}` correspondrait aussi à `/users/me`, la fonction «croyant» qu'elle a reçu un paramètre `user_id` avec pour valeur «me».

De même, vous ne pouvez pas redéfinir une opération de chemin :

{* ../../docs_src/path_params/tutorial003b_py39.py hl[6,11] *}

La première sera toujours utilisée car le chemin correspond d'abord.

## Valeurs prédéfinies { #predefined-values }

Si vous avez une *opération de chemin* qui reçoit un *paramètre de chemin*, mais que vous voulez que les valeurs possibles des paramètres soient prédéfinies, vous pouvez utiliser les <abbr title="Enumeration">`Enum`</abbr> de Python.

### Créer une classe `Enum` { #create-an-enum-class }

Importez `Enum` et créez une sous-classe qui hérite de `str` et de `Enum`.

En héritant de `str`, la documentation de l'API saura que les valeurs doivent être de type `string` et pourra donc l'afficher correctement.

Créez ensuite des attributs de classe avec des valeurs fixes, qui seront les valeurs autorisées pour cette énumération.

{* ../../docs_src/path_params/tutorial005_py39.py hl[1,6:9] *}

/// tip | Astuce

Pour ceux qui se demandent, «AlexNet», «ResNet», et «LeNet» sont juste des noms de <abbr title="Techniquement, des architectures de modèles de Deep Learning">modèles</abbr> de Machine Learning.

///

### Déclarer un *paramètre de chemin* { #declare-a-path-parameter }

Créez ensuite un *paramètre de chemin* avec une annotation de type désignant l'énumération créée précédemment (`ModelName`) :

{* ../../docs_src/path_params/tutorial005_py39.py hl[16] *}

### Vérifier la documentation { #check-the-docs }

Les valeurs disponibles pour le *paramètre de chemin* sont bien prédéfinies, la documentation les affiche correctement :

<img src="/img/tutorial/path-params/image03.png">

### Manipuler les *énumérations* Python { #working-with-python-enumerations }

La valeur du *paramètre de chemin* sera un des «membres» de l'énumération.

#### Comparer les *membres d'énumération* { #compare-enumeration-members }

Vous pouvez comparer ce paramètre avec les membres de votre énumération `ModelName` :

{* ../../docs_src/path_params/tutorial005_py39.py hl[17] *}

#### Récupérer la *valeur de l'énumération* { #get-the-enumeration-value }

Vous pouvez obtenir la valeur réelle d'un membre (une chaîne de caractères ici), avec `model_name.value`, ou en général, `votre_membre_d'enum.value` :

{* ../../docs_src/path_params/tutorial005_py39.py hl[20] *}

/// tip | Astuce

Vous pouvez aussi accéder à la valeur «lenet» avec `ModelName.lenet.value`.

///

#### Retourner des *membres d'énumération* { #return-enumeration-members }

Vous pouvez retourner des *membres d'énumération* dans vos *opérations de chemin*, même imbriqués dans un corps JSON (e.g. un `dict`).

Ils seront convertis vers leurs valeurs correspondantes (chaînes de caractères ici) avant d'être transmis au client :

{* ../../docs_src/path_params/tutorial005_py39.py hl[18,21,23] *}

Le client recevra une réponse JSON comme celle-ci :

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Paramètres de chemin contenant des chemins { #path-parameters-containing-paths }

Disons que vous avez une *opération de chemin* liée au chemin `/files/{file_path}`.

Mais que `file_path` lui-même doit contenir un *chemin*, comme `home/johndoe/myfile.txt` par exemple.

Donc, l'URL pour ce fichier pourrait être : `/files/home/johndoe/myfile.txt`.

### Support d'OpenAPI { #openapi-support }

OpenAPI ne supporte pas de manière de déclarer un *paramètre de chemin* contenant un *chemin* à l'intérieur, cela pouvant causer des scénarios difficiles à tester et définir.

Néanmoins, cela reste faisable dans **FastAPI**, via les outils internes de Starlette.

Et la documentation fonctionne quand même, bien qu'aucune section ne soit ajoutée pour dire que le paramètre devrait contenir un *chemin*.

### Convertisseur de *chemin* { #path-convertor }

En utilisant une option de Starlette directement, vous pouvez déclarer un *paramètre de chemin* contenant un *chemin* avec une URL comme :

```
/files/{file_path:path}
```

Dans ce cas, le nom du paramètre est `file_path`, et la dernière partie, `:path`, indique que le paramètre doit correspondre à n'importe quel *chemin*.

Vous pouvez donc l'utiliser comme tel :

{* ../../docs_src/path_params/tutorial004_py39.py hl[6] *}

/// tip | Astuce

Vous pourriez avoir besoin que le paramètre contienne `/home/johndoe/myfile.txt`, avec un slash au début (`/`).

Dans ce cas, l'URL serait : `/files//home/johndoe/myfile.txt`, avec un double slash (`//`) entre `files` et `home`.

///

## Récapitulatif { #recap }

Avec **FastAPI**, en utilisant les déclarations de type rapides, intuitives et standards de Python, vous bénéficiez de :

* Support de l'éditeur : vérification d'erreurs, autocomplétion, etc.
* «<abbr title="conversion de la chaîne de caractères venant de la requête HTTP en données Python">Parsing</abbr>» de données
* Validation de données
* Annotations d'API et documentation automatique

Et vous n'avez besoin de le déclarer qu'une fois.

C'est probablement l'avantage visible principal de **FastAPI** comparé aux autres frameworks (outre les performances pures).
