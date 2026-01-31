# Corps de la requête { #request-body }

Quand vous avez besoin d'envoyer des données depuis un client (disons, un navigateur) vers votre API, vous les envoyez en tant que **corps de la requête**.

Le corps d'une **requête** est des données envoyées par le client à votre API. Le corps d'une **réponse** est la donnée envoyée par votre API au client.

Votre API a presque toujours besoin d'envoyer un corps de **réponse**. Mais les clients n'ont pas nécessairement besoin d'envoyer des **corps de requête** en permanence, parfois ils demandent seulement un chemin, peut-être avec des paramètres de requête, mais n'envoient pas de corps.

Pour déclarer un corps de **requête**, on utilise les modèles de <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> en profitant de tous leurs avantages et fonctionnalités.

/// info

Pour envoyer des données, vous devriez utiliser l'une des méthodes suivantes : `POST` (la plus courante), `PUT`, `DELETE` ou `PATCH`.

Envoyer un corps avec une requête `GET` a un comportement non défini dans les spécifications ; néanmoins, cela est supporté par FastAPI, uniquement pour des cas d'utilisation très complexes/extrêmes.

Comme cela est déconseillé, la documentation interactive avec Swagger UI n'affichera pas la documentation du corps lors de l'utilisation de `GET`, et les proxys intermédiaires risquent de ne pas le supporter.

///

## Importer le `BaseModel` de Pydantic { #import-pydantics-basemodel }

Commencez par importer `BaseModel` depuis `pydantic` :

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## Créer votre modèle de données { #create-your-data-model }

Déclarez ensuite votre modèle de données en tant que classe qui hérite de `BaseModel`.

Utilisez les types Python standard pour tous les attributs :

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


Tout comme pour la déclaration de paramètres de requête, quand un attribut de modèle a une valeur par défaut, il n'est pas requis. Sinon, il est requis. Utilisez `None` pour le rendre simplement optionnel.

Par exemple, le modèle ci-dessus déclare un « `object` » JSON (ou `dict` Python) tel que :

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

... comme `description` et `tax` sont optionnels (avec une valeur par défaut de `None`), cet « `object` » JSON serait aussi valide :

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Le déclarer comme paramètre { #declare-it-as-a-parameter }

Pour l'ajouter à votre *chemin d'accès*, déclarez-le de la même manière que vous avez déclaré les paramètres de chemin et de requête :

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

... et déclarez son type comme étant le modèle que vous avez créé, `Item`.

## Résultats { #results }

Avec simplement cette déclaration de type Python, **FastAPI** va :

* Lire le corps de la requête en tant que JSON.
* Convertir les types correspondants (si nécessaire).
* Valider les données.
    * Si les données sont invalides, il renverra une erreur propre et claire, indiquant exactement où et quelles étaient les données incorrectes.
* Vous donner les données reçues dans le paramètre `item`.
    * Comme vous l'avez déclaré dans la fonction comme étant de type `Item`, vous aurez aussi tout le support offert par l'éditeur (autocomplétion, etc.) pour tous les attributs et leurs types.
* Générer des définitions <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> pour votre modèle ; vous pouvez aussi les utiliser ailleurs si cela a du sens pour votre projet.
* Ces schémas feront partie du schéma OpenAPI généré et seront utilisés par la documentation automatique <abbr title="User Interfaces - Interfaces utilisateur">UIs</abbr>.

## Documentation automatique { #automatic-docs }

Les JSON Schemas de vos modèles feront partie du schéma OpenAPI généré de votre application, et seront affichés dans la documentation interactive de l'API :

<img src="/img/tutorial/body/image01.png">

Et seront aussi utilisés dans la documentation de l'API au sein de chaque *chemin d'accès* qui en a besoin :

<img src="/img/tutorial/body/image02.png">

## Support de l'éditeur { #editor-support }

Dans votre éditeur, à l'intérieur de votre fonction, vous obtiendrez des annotations de type et de la complétion partout (cela n'arriverait pas si vous receviez un `dict` au lieu d'un modèle Pydantic) :

<img src="/img/tutorial/body/image03.png">

Vous obtenez aussi des vérifications d'erreur pour les opérations incorrectes de types :

<img src="/img/tutorial/body/image04.png">

Ce n'est pas un hasard, ce framework entier a été bâti autour de ce design.

Et cela a été rigoureusement testé durant la phase de design, avant toute implémentation, pour vous assurer que cela fonctionnerait avec tous les éditeurs.

Des changements ont même été faits sur Pydantic lui-même pour supporter cela.

Les captures d'écrans précédentes ont été prises avec <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Mais vous auriez le même support de l'éditeur avec <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> et la plupart des autres éditeurs Python :

<img src="/img/tutorial/body/image05.png">

/// tip | Astuce

Si vous utilisez <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> comme éditeur, vous pouvez utiliser le <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>.

Il améliore le support de l'éditeur pour les modèles Pydantic, avec :

* autocomplétion
* vérifications de type
* refactoring
* recherche
* inspections

///

## Utiliser le modèle { #use-the-model }

À l'intérieur de la fonction, vous pouvez accéder directement à tous les attributs de l'objet du modèle :

{* ../../docs_src/body/tutorial002_py310.py *}

## Corps de la requête + paramètres de chemin { #request-body-path-parameters }

Vous pouvez déclarer des paramètres de chemin et le corps de la requête en même temps.

**FastAPI** reconnaîtra que les paramètres de la fonction qui correspondent aux paramètres de chemin doivent être **récupérés depuis le chemin**, et que les paramètres de fonction déclarés comme modèles Pydantic doivent être **récupérés depuis le corps de la requête**.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## Corps de la requête + paramètres de chemin et de requête { #request-body-path-query-parameters }

Vous pouvez aussi déclarer des paramètres de **corps**, de **chemin** et de **requête**, tous en même temps.

**FastAPI** reconnaîtra chacun d'entre eux et récupérera les données au bon endroit.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Les paramètres de la fonction seront reconnus comme suit :

* Si le paramètre est aussi déclaré dans le **chemin**, il sera utilisé comme paramètre de chemin.
* Si le paramètre est d'un **type singulier** (comme `int`, `float`, `str`, `bool`, etc.), il sera interprété comme un paramètre de **requête**.
* Si le paramètre est déclaré comme étant du type d'un **modèle Pydantic**, il sera interprété comme faisant partie du **corps** de la requête.

/// note | Remarque

FastAPI saura que la valeur de `q` n'est pas requise grâce à la valeur par défaut `= None`.

Le `str | None` (Python 3.10+) ou `Union` dans `Union[str, None]` (Python 3.9+) n'est pas utilisé par FastAPI pour déterminer que la valeur n'est pas requise ; il saura qu'elle n'est pas requise parce qu'elle a une valeur par défaut `= None`.

Mais ajouter les annotations de type permettra à votre éditeur de vous offrir un meilleur support et de détecter des erreurs.

///

## Sans Pydantic { #without-pydantic }

Si vous ne voulez pas utiliser de modèles Pydantic, vous pouvez aussi utiliser des paramètres **Body**. Consultez les documents pour [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
