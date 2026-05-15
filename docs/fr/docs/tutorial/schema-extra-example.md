# Déclarer des exemples de données de requête { #declare-request-example-data }

Vous pouvez déclarer des exemples des données que votre application peut recevoir.

Voici plusieurs façons de le faire.

## Ajouter des données JSON Schema supplémentaires dans les modèles Pydantic { #extra-json-schema-data-in-pydantic-models }

Vous pouvez déclarer `examples` pour un modèle Pydantic qui seront ajoutés au JSON Schema généré.

{* ../../docs_src/schema_extra_example/tutorial001_py310.py hl[13:24] *}

Ces informations supplémentaires seront ajoutées telles quelles au **JSON Schema** de sortie pour ce modèle, et elles seront utilisées dans la documentation de l'API.

Vous pouvez utiliser l'attribut `model_config` qui accepte un `dict` comme décrit dans [Documentation de Pydantic : Configuration](https://docs.pydantic.dev/latest/api/config/).

Vous pouvez définir `"json_schema_extra"` avec un `dict` contenant toutes les données supplémentaires que vous souhaitez voir apparaître dans le JSON Schema généré, y compris `examples`.

/// tip | Astuce

Vous pouvez utiliser la même technique pour étendre le JSON Schema et ajouter vos propres informations supplémentaires personnalisées.

Par exemple, vous pourriez l'utiliser pour ajouter des métadonnées pour une interface utilisateur frontend, etc.

///

/// info

OpenAPI 3.1.0 (utilisé depuis FastAPI 0.99.0) a ajouté la prise en charge de `examples`, qui fait partie du standard **JSON Schema**.

Avant cela, seule la clé `example` avec un exemple unique était prise en charge. Elle l'est toujours par OpenAPI 3.1.0, mais elle est dépréciée et ne fait pas partie du standard JSON Schema. Vous êtes donc encouragé à migrer de `example` vers `examples`. 🤓

Vous pouvez en lire davantage à la fin de cette page.

///

## Arguments supplémentaires de `Field` { #field-additional-arguments }

Lorsque vous utilisez `Field()` avec des modèles Pydantic, vous pouvez également déclarer des `examples` supplémentaires :

{* ../../docs_src/schema_extra_example/tutorial002_py310.py hl[2,8:11] *}

## `examples` dans JSON Schema - OpenAPI { #examples-in-json-schema-openapi }

En utilisant l'un des éléments suivants :

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

vous pouvez également déclarer un groupe de `examples` avec des informations supplémentaires qui seront ajoutées à leurs **JSON Schemas** à l'intérieur d'**OpenAPI**.

### `Body` avec `examples` { #body-with-examples }

Ici, nous passons `examples` contenant un exemple des données attendues dans `Body()` :

{* ../../docs_src/schema_extra_example/tutorial003_an_py310.py hl[22:29] *}

### Exemple dans l'interface des documents { #example-in-the-docs-ui }

Avec l'une des méthodes ci-dessus, cela ressemblerait à ceci dans le `/docs` :

<img src="/img/tutorial/body-fields/image01.png">

### `Body` avec plusieurs `examples` { #body-with-multiple-examples }

Vous pouvez bien sûr aussi passer plusieurs `examples` :

{* ../../docs_src/schema_extra_example/tutorial004_an_py310.py hl[23:38] *}

Lorsque vous faites cela, les exemples feront partie du **JSON Schema** interne pour ces données de corps.

Néanmoins, <dfn title="2023-08-26">au moment de la rédaction</dfn>, Swagger UI, l'outil chargé d'afficher l'interface des documents, ne prend pas en charge l'affichage de plusieurs exemples pour les données dans **JSON Schema**. Mais lisez ci-dessous pour un contournement.

### `examples` spécifiques à OpenAPI { #openapi-specific-examples }

Avant que **JSON Schema** ne prenne en charge `examples`, OpenAPI prenait déjà en charge un autre champ également appelé `examples`.

Ce `examples` **spécifique à OpenAPI** se trouve dans une autre section de la spécification OpenAPI. Il se trouve dans les **détails de chaque *chemin d'accès***, et non à l'intérieur de chaque JSON Schema.

Et Swagger UI prend en charge ce champ particulier `examples` depuis un certain temps. Vous pouvez donc l'utiliser pour **afficher** différents **exemples dans l'interface des documents**.

La forme de ce champ `examples` spécifique à OpenAPI est un `dict` avec **plusieurs exemples** (au lieu d'une `list`), chacun avec des informations supplémentaires qui seront également ajoutées à **OpenAPI**.

Cela ne va pas à l'intérieur de chaque JSON Schema contenu dans OpenAPI, cela se place à l'extérieur, directement dans le *chemin d'accès*.

### Utiliser le paramètre `openapi_examples` { #using-the-openapi-examples-parameter }

Vous pouvez déclarer le `examples` spécifique à OpenAPI dans FastAPI avec le paramètre `openapi_examples` pour :

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

Les clés du `dict` identifient chaque exemple, et chaque valeur est un autre `dict`.

Chaque `dict` d'exemple spécifique dans `examples` peut contenir :

* `summary` : une courte description de l'exemple.
* `description` : une description longue qui peut contenir du texte Markdown.
* `value` : c'est l'exemple réel affiché, par ex. un `dict`.
* `externalValue` : alternative à `value`, une URL pointant vers l'exemple. Cependant, cela pourrait ne pas être pris en charge par autant d'outils que `value`.

Vous pouvez l'utiliser ainsi :

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}

### Exemples OpenAPI dans l'interface des documents { #openapi-examples-in-the-docs-ui }

Avec `openapi_examples` ajouté à `Body()`, le `/docs` ressemblerait à :

<img src="/img/tutorial/body-fields/image02.png">

## Détails techniques { #technical-details }

/// tip | Astuce

Si vous utilisez déjà **FastAPI** en version **0.99.0 ou supérieure**, vous pouvez probablement **passer** ces détails.

Ils sont plus pertinents pour les versions plus anciennes, avant que OpenAPI 3.1.0 ne soit disponible.

Vous pouvez considérer ceci comme une courte leçon d'histoire d'OpenAPI et de JSON Schema. 🤓

///

/// warning | Alertes

Ce sont des détails très techniques au sujet des standards **JSON Schema** et **OpenAPI**.

Si les idées ci-dessus fonctionnent déjà pour vous, cela pourrait suffire, et vous n'avez probablement pas besoin de ces détails, n'hésitez pas à les ignorer.

///

Avant OpenAPI 3.1.0, OpenAPI utilisait une version plus ancienne et modifiée de **JSON Schema**.

JSON Schema n'avait pas `examples`, donc OpenAPI a ajouté son propre champ `example` à sa version modifiée.

OpenAPI a également ajouté les champs `example` et `examples` à d'autres parties de la spécification :

* [`Parameter Object` (dans la spécification)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object) qui était utilisé par les éléments FastAPI :
    * `Path()`
    * `Query()`
    * `Header()`
    * `Cookie()`
* [`Request Body Object`, dans le champ `content`, sur le `Media Type Object` (dans la spécification)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object) qui était utilisé par les éléments FastAPI :
    * `Body()`
    * `File()`
    * `Form()`

/// info

Ce paramètre `examples` ancien et spécifique à OpenAPI est désormais `openapi_examples` depuis FastAPI `0.103.0`.

///

### Le champ `examples` de JSON Schema { #json-schemas-examples-field }

Ensuite, JSON Schema a ajouté un champ [`examples`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5) dans une nouvelle version de la spécification.

Puis le nouveau OpenAPI 3.1.0 s'est basé sur la dernière version (JSON Schema 2020-12) qui incluait ce nouveau champ `examples`.

Et désormais, ce nouveau champ `examples` a priorité sur l'ancien champ unique (et personnalisé) `example`, qui est maintenant déprécié.

Ce nouveau champ `examples` dans JSON Schema est **juste une `list`** d'exemples, et non pas un dict avec des métadonnées supplémentaires comme dans les autres endroits d'OpenAPI (décrits ci-dessus).

/// info

Même après la sortie d'OpenAPI 3.1.0 avec cette nouvelle intégration plus simple avec JSON Schema, pendant un temps, Swagger UI, l'outil qui fournit la documentation automatique, ne prenait pas en charge OpenAPI 3.1.0 (il le fait depuis la version 5.0.0 🎉).

À cause de cela, les versions de FastAPI antérieures à 0.99.0 utilisaient encore des versions d'OpenAPI inférieures à 3.1.0.

///

### `examples` avec Pydantic et FastAPI { #pydantic-and-fastapi-examples }

Lorsque vous ajoutez `examples` dans un modèle Pydantic, en utilisant `schema_extra` ou `Field(examples=["something"])`, cet exemple est ajouté au **JSON Schema** de ce modèle Pydantic.

Et ce **JSON Schema** du modèle Pydantic est inclus dans l'**OpenAPI** de votre API, puis il est utilisé dans l'interface de la documentation.

Dans les versions de FastAPI antérieures à 0.99.0 (0.99.0 et supérieures utilisent le nouveau OpenAPI 3.1.0), lorsque vous utilisiez `example` ou `examples` avec l'une des autres utilitaires (`Query()`, `Body()`, etc.), ces exemples n'étaient pas ajoutés au JSON Schema qui décrit ces données (pas même à la version de JSON Schema propre à OpenAPI), ils étaient ajoutés directement à la déclaration du *chemin d'accès* dans OpenAPI (en dehors des parties d'OpenAPI qui utilisent JSON Schema).

Mais maintenant que FastAPI 0.99.0 et supérieures utilisent OpenAPI 3.1.0, qui utilise JSON Schema 2020-12, et Swagger UI 5.0.0 et supérieures, tout est plus cohérent et les exemples sont inclus dans JSON Schema.

### Swagger UI et `examples` spécifiques à OpenAPI { #swagger-ui-and-openapi-specific-examples }

Comme Swagger UI ne prenait pas en charge plusieurs exemples JSON Schema (au 2023-08-26), les utilisateurs n'avaient pas de moyen d'afficher plusieurs exemples dans les documents.

Pour résoudre cela, FastAPI `0.103.0` a **ajouté la prise en charge** de la déclaration du même ancien champ `examples` **spécifique à OpenAPI** avec le nouveau paramètre `openapi_examples`. 🤓

### Résumé { #summary }

Je disais que je n'aimais pas trop l'histoire ... et me voilà maintenant à donner des leçons d'« tech history ». 😅

En bref, **mettez à niveau vers FastAPI 0.99.0 ou supérieur**, et les choses sont bien plus **simples, cohérentes et intuitives**, et vous n'avez pas besoin de connaître tous ces détails historiques. 😎
