# Corps de la requête { #request-body }

Quand vous avez besoin d'envoyer de la donnée depuis un client (comme un navigateur) vers votre API, vous l'envoyez en tant que **corps de requête**.

Le corps d'une **requête** est de la donnée envoyée par le client à votre API. Le corps d'une **réponse** est la donnée envoyée par votre API au client.

Votre API aura presque toujours à envoyer un corps de **réponse**. Mais un client n'a pas toujours à envoyer un **corps de requête** : parfois il demande seulement un chemin, peut-être avec quelques paramètres de requête, mais n'envoie pas de corps.

Pour déclarer un corps de **requête**, on utilise les modèles de <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> en profitant de tous leurs avantages et fonctionnalités.

/// info

Pour envoyer de la donnée, vous devez utiliser : `POST` (le plus populaire), `PUT`, `DELETE` ou `PATCH`.

Envoyer un corps dans une requête `GET` a un comportement non défini dans les spécifications, cela est néanmoins supporté par **FastAPI**, seulement pour des cas d'utilisation très complexes/extrêmes.

Ceci étant découragé, la documentation interactive générée par Swagger UI ne montrera pas de documentation pour le corps d'une requête `GET`, et les proxys intermédiaires risquent de ne pas le supporter.

///

## Importer le `BaseModel` de Pydantic { #import-pydantics-basemodel }

Commencez par importer la classe `BaseModel` du module `pydantic` :

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## Créer votre modèle de données { #create-your-data-model }

Déclarez ensuite votre modèle de données en tant que classe qui hérite de `BaseModel`.

Utilisez les types Python standard pour tous les attributs :

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

Tout comme pour la déclaration de paramètres de requête, quand un attribut de modèle a une valeur par défaut, il n'est pas nécessaire. Sinon, cet attribut doit être renseigné dans le corps de la requête. Utilisez `None` pour le rendre simplement optionnel.

Par exemple, le modèle ci-dessus déclare un JSON « `object` » (ou `dict` Python) tel que :

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

... `description` et `tax` étant des attributs optionnels (avec `None` comme valeur par défaut), ce JSON « `object` » serait aussi valide :

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Le déclarer comme paramètre { #declare-it-as-a-parameter }

Pour l'ajouter à votre *chemin d'accès*, déclarez-le comme vous déclareriez des paramètres de chemin ou de requête :

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

... et déclarez que son type est le modèle que vous avez créé : `Item`.

## Résultats { #results }

En utilisant uniquement les déclarations de type Python, **FastAPI** réussit à :

* Lire le contenu de la requête en tant que JSON.
* Convertir les types correspondants (si nécessaire).
* Valider la donnée.
    * Si la donnée est invalide, une erreur propre et claire sera renvoyée, indiquant exactement où et quelle était la donnée incorrecte.
* Passer la donnée reçue dans le paramètre `item`.
    * Ce paramètre ayant été déclaré dans la fonction comme étant de type `Item`, vous aurez aussi tout le support offert par l'éditeur (autocomplétion, etc.) pour tous les attributs de ce paramètre et les types de ces attributs.
* Générer des définitions <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> pour votre modèle ; vous pouvez également les utiliser partout ailleurs si cela a du sens pour votre projet.
* Ces schémas participeront à la constitution du schéma généré OpenAPI, et seront utilisés par les documentations automatiques <abbr title="User Interfaces - Interfaces utilisateur">UIs</abbr>.

## Documentation automatique { #automatic-docs }

Les schémas JSON de vos modèles seront intégrés au schéma OpenAPI global de votre application, et seront donc affichés dans la documentation interactive de l'API :

<img src="/img/tutorial/body/image01.png">

Et seront aussi utilisés dans chaque *chemin d'accès* de la documentation utilisant ces modèles :

<img src="/img/tutorial/body/image02.png">

## Support de l'éditeur { #editor-support }

Dans votre éditeur, vous aurez des annotations de type et de l'autocomplétion partout dans votre fonction (ce qui n'aurait pas été le cas si vous aviez reçu un `dict` plutôt qu'un modèle Pydantic) :

<img src="/img/tutorial/body/image03.png">

Et vous obtenez aussi des vérifications d'erreurs pour les opérations de types incorrectes :

<img src="/img/tutorial/body/image04.png">

Ce n'est pas un hasard, ce framework entier a été bâti avec ce design comme objectif.

Et cela a été rigoureusement testé durant la phase de design, avant toute implémentation, pour vous assurer que cela fonctionnerait avec tous les éditeurs.

Des changements sur Pydantic ont même été faits pour supporter cela.

Les captures d'écran précédentes ont été prises sur <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Mais vous auriez le même support de l'éditeur avec <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> et la majorité des autres éditeurs de code Python :

<img src="/img/tutorial/body/image05.png">

/// tip | Astuce

Si vous utilisez <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> comme éditeur, vous pouvez utiliser le plug-in <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>.

Ce qui améliore le support pour les modèles Pydantic avec :

* de l'autocomplétion
* des vérifications de type
* du « refactoring »
* de la recherche
* des inspections

///

## Utiliser le modèle { #use-the-model }

Dans la fonction, vous pouvez accéder à tous les attributs de l'objet du modèle directement :

{* ../../docs_src/body/tutorial002_py310.py *}

## Corps de la requête + paramètres de chemin { #request-body-path-parameters }

Vous pouvez déclarer des paramètres de chemin et un corps de requête pour la même *chemin d'accès*.

**FastAPI** est capable de reconnaître que les paramètres de la fonction qui correspondent aux paramètres de chemin doivent être **récupérés depuis le chemin**, et que les paramètres de fonctions déclarés comme modèles Pydantic devraient être **récupérés depuis le corps de la requête**.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## Corps de la requête + paramètres de chemin et de requête { #request-body-path-query-parameters }

Vous pouvez aussi déclarer un **corps**, et des paramètres de **chemin** et de **requête** dans la même *chemin d'accès*.

**FastAPI** saura reconnaître chacun d'entre eux et récupérer la bonne donnée au bon endroit.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Les paramètres de la fonction seront reconnus comme tel :

* Si le paramètre est aussi déclaré dans le **chemin**, il sera utilisé comme paramètre de chemin.
* Si le paramètre est d'un **type singulier** (comme `int`, `float`, `str`, `bool`, etc.), il sera interprété comme un paramètre de **requête**.
* Si le paramètre est déclaré comme ayant pour type un **modèle Pydantic**, il sera interprété comme faisant partie du **corps** de la requête.

/// note | Remarque

**FastAPI** saura que la valeur de `q` n'est pas requise grâce à la valeur par défaut `= None`.

L'annotation de type `str | None` n'est pas utilisée par **FastAPI** pour déterminer que la valeur n'est pas requise, il le saura parce qu'elle a une valeur par défaut `= None`.

Mais ajouter ces annotations de type permettra à votre éditeur de vous offrir un meilleur support et de détecter des erreurs.

///

## Sans Pydantic { #without-pydantic }

Si vous ne voulez pas utiliser des modèles Pydantic, vous pouvez aussi utiliser des paramètres de **Body**. Pour cela, allez voir la documentation sur [Corps de la requête - Paramètres multiples : Valeurs singulières dans le corps](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
