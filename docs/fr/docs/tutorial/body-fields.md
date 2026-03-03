# Corps - Champs { #body-fields }

De la même manière que vous pouvez déclarer des validations supplémentaires et des métadonnées dans les paramètres d'une fonction de chemin d'accès avec `Query`, `Path` et `Body`, vous pouvez déclarer des validations et des métadonnées à l'intérieur des modèles Pydantic en utilisant `Field` de Pydantic.

## Importer `Field` { #import-field }

D'abord, vous devez l'importer :

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}


/// warning | Alertes

Notez que `Field` est importé directement depuis `pydantic`, et non depuis `fastapi` comme le sont les autres (`Query`, `Path`, `Body`, etc.).

///

## Déclarer les attributs du modèle { #declare-model-attributes }

Vous pouvez ensuite utiliser `Field` avec des attributs de modèle :

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` fonctionne de la même manière que `Query`, `Path` et `Body`, il dispose des mêmes paramètres, etc.

/// note | Détails techniques

En réalité, `Query`, `Path` et d'autres que vous verrez ensuite créent des objets de sous-classes d'une classe commune `Param`, qui est elle-même une sous-classe de la classe `FieldInfo` de Pydantic.

Et `Field` de Pydantic renvoie également une instance de `FieldInfo`.

`Body` renvoie aussi directement des objets d'une sous-classe de `FieldInfo`. Et il y en a d'autres que vous verrez plus tard qui sont des sous-classes de la classe `Body`.

Rappelez-vous que lorsque vous importez `Query`, `Path` et d'autres depuis `fastapi`, ce sont en réalité des fonctions qui renvoient des classes spéciales.

///

/// tip | Astuce

Remarquez comment chaque attribut de modèle avec un type, une valeur par défaut et `Field` a la même structure qu'un paramètre de fonction de chemin d'accès, avec `Field` au lieu de `Path`, `Query` et `Body`.

///

## Ajouter des informations supplémentaires { #add-extra-information }

Vous pouvez déclarer des informations supplémentaires dans `Field`, `Query`, `Body`, etc. Elles seront incluses dans le JSON Schema généré.

Vous en apprendrez davantage sur l'ajout d'informations supplémentaires plus loin dans les documents, lorsque vous apprendrez à déclarer des exemples.

/// warning | Alertes

Les clés supplémentaires passées à `Field` seront également présentes dans le schéma OpenAPI résultant pour votre application.
Comme ces clés ne font pas nécessairement partie de la spécification OpenAPI, certains outils OpenAPI, par exemple [le validateur OpenAPI](https://validator.swagger.io/), peuvent ne pas fonctionner avec votre schéma généré.

///

## Récapitulatif { #recap }

Vous pouvez utiliser `Field` de Pydantic pour déclarer des validations supplémentaires et des métadonnées pour les attributs de modèle.

Vous pouvez également utiliser des arguments nommés supplémentaires pour transmettre des métadonnées JSON Schema additionnelles.
