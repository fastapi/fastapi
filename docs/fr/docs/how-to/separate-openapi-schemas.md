# Séparer les schémas OpenAPI pour l'entrée et la sortie ou non { #separate-openapi-schemas-for-input-and-output-or-not }

Depuis la sortie de **Pydantic v2**, l'OpenAPI généré est un peu plus précis et **correct** qu'avant. 😎

En fait, dans certains cas, il y aura même **deux schémas JSON** dans OpenAPI pour le même modèle Pydantic, pour l'entrée et pour la sortie, selon s'ils ont des **valeurs par défaut**.

Voyons comment cela fonctionne et comment le modifier si vous devez le faire.

## Utiliser des modèles Pydantic pour l'entrée et la sortie { #pydantic-models-for-input-and-output }

Supposons que vous ayez un modèle Pydantic avec des valeurs par défaut, comme celui‑ci :

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### Modèle pour l'entrée { #model-for-input }

Si vous utilisez ce modèle en entrée comme ici :

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

... alors, le champ `description` ne sera **pas requis**. Parce qu'il a une valeur par défaut de `None`.

### Modèle d'entrée dans les documents { #input-model-in-docs }

Vous pouvez le confirmer dans les documents, le champ `description` n'a pas d'**astérisque rouge**, il n'est pas indiqué comme requis :

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### Modèle pour la sortie { #model-for-output }

Mais si vous utilisez le même modèle en sortie, comme ici :

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

... alors, comme `description` a une valeur par défaut, si vous ne retournez rien pour ce champ, il aura tout de même cette **valeur par défaut**.

### Modèle pour les données de réponse en sortie { #model-for-output-response-data }

Si vous interagissez avec les documents et vérifiez la réponse, même si le code n'a rien ajouté dans l'un des champs `description`, la réponse JSON contient la valeur par défaut (`null`) :

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

Cela signifie qu'il aura **toujours une valeur**, simplement, parfois la valeur pourra être `None` (ou `null` en JSON).

Cela signifie que les clients utilisant votre API n'ont pas à vérifier si la valeur existe ou non, ils peuvent **supposer que le champ sera toujours présent**, mais que, dans certains cas, il aura la valeur par défaut `None`.

La manière de décrire cela dans OpenAPI est de marquer ce champ comme **requis**, car il sera toujours présent.

Pour cette raison, le schéma JSON d'un modèle peut être différent selon qu'il est utilisé pour **l'entrée ou la sortie** :

- pour **l'entrée**, `description` ne sera **pas requis**
- pour **la sortie**, il sera **requis** (et éventuellement `None`, ou en termes JSON, `null`)

### Modèle de sortie dans les documents { #model-for-output-in-docs }

Vous pouvez également vérifier le modèle de sortie dans les documents, **à la fois** `name` et `description` sont marqués comme **requis** avec un **astérisque rouge** :

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### Modèle pour l'entrée et la sortie dans les documents { #model-for-input-and-output-in-docs }

Et si vous consultez tous les schémas disponibles (schémas JSON) dans OpenAPI, vous verrez qu'il y en a deux, un `Item-Input` et un `Item-Output`.

Pour `Item-Input`, `description` n'est **pas requis**, il n'a pas d'astérisque rouge.

Mais pour `Item-Output`, `description` est **requis**, il a un astérisque rouge.

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

Avec cette fonctionnalité de **Pydantic v2**, la documentation de votre API est plus **précise**, et si vous avez des clients et SDKs générés automatiquement, ils seront eux aussi plus précis, avec une meilleure **expérience développeur** et davantage de cohérence. 🎉

## Ne pas séparer les schémas { #do-not-separate-schemas }

Il existe des cas où vous pourriez vouloir avoir le **même schéma pour l'entrée et la sortie**.

Le cas d'usage principal est probablement que vous avez déjà du code client/SDKs générés automatiquement et que vous ne souhaitez pas encore mettre à jour tout ce code client/ces SDKs générés automatiquement ; vous le ferez sans doute à un moment donné, mais peut‑être pas tout de suite.

Dans ce cas, vous pouvez désactiver cette fonctionnalité dans **FastAPI**, avec le paramètre `separate_input_output_schemas=False`.

/// info | info

La prise en charge de `separate_input_output_schemas` a été ajoutée dans FastAPI `0.102.0`. 🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### Utiliser le même schéma pour les modèles d'entrée et de sortie dans les documents { #same-schema-for-input-and-output-models-in-docs }

Désormais, il n'y aura qu'un seul schéma pour l'entrée et la sortie du modèle, uniquement `Item`, et `description` ne sera pas requis :

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
