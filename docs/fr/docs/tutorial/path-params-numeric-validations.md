# Paramètres de chemin et validations numériques { #path-parameters-and-numeric-validations }

De la même façon que vous pouvez déclarer plus de validations et de métadonnées pour les paramètres de requête avec `Query`, vous pouvez déclarer le même type de validations et de métadonnées pour les paramètres de chemin avec `Path`.

## Importer `Path` { #import-path }

Tout d'abord, importez `Path` de `fastapi`, et importez `Annotated` :

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info

FastAPI a ajouté le support pour `Annotated` (et a commencé à le recommander) dans la version 0.95.0.

Si vous avez une version plus ancienne, vous obtiendrez des erreurs en essayant d'utiliser `Annotated`.

Assurez-vous de [Mettre à niveau la version de FastAPI](../deployment/versions.md#upgrading-the-fastapi-versions) à la version 0.95.1 à minima avant d'utiliser `Annotated`.

///

## Déclarer des métadonnées { #declare-metadata }

Vous pouvez déclarer les mêmes paramètres que pour `Query`.

Par exemple, pour déclarer une valeur de métadonnée `title` pour le paramètre de chemin `item_id`, vous pouvez écrire :

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | Remarque

Un paramètre de chemin est toujours requis car il doit faire partie du chemin. Même si vous l'avez déclaré avec `None` ou défini une valeur par défaut, cela ne changerait rien, il serait toujours requis.

///

## Ordonner les paramètres comme vous le souhaitez { #order-the-parameters-as-you-need }

/// tip | Astuce

Ce n'est probablement pas aussi important ou nécessaire si vous utilisez `Annotated`.

///

Disons que vous voulez déclarer le paramètre de requête `q` comme un `str` requis.

Et vous n'avez pas besoin de déclarer autre chose pour ce paramètre, donc vous n'avez pas vraiment besoin d'utiliser `Query`.

Mais vous avez toujours besoin d'utiliser `Path` pour le paramètre de chemin `item_id`. Et vous ne voulez pas utiliser `Annotated` pour une raison quelconque.

Python se plaindra si vous mettez une valeur avec une « valeur par défaut » avant une valeur qui n'a pas de « valeur par défaut ».

Mais vous pouvez les réorganiser, et avoir la valeur sans défaut (le paramètre de requête `q`) en premier.

Cela n'a pas d'importance pour **FastAPI**. Il détectera les paramètres par leurs noms, types et déclarations par défaut (`Query`, `Path`, etc), il ne se soucie pas de l'ordre.

Ainsi, vous pouvez déclarer votre fonction comme suit :

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

Mais gardez à l'esprit que si vous utilisez `Annotated`, vous n'aurez pas ce problème, cela n'aura pas d'importance car vous n'utilisez pas les valeurs par défaut des paramètres de fonction pour `Query()` ou `Path()`.

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## Ordonner les paramètres comme vous le souhaitez, astuces { #order-the-parameters-as-you-need-tricks }

/// tip | Astuce

Ce n'est probablement pas aussi important ou nécessaire si vous utilisez `Annotated`.

///

Voici une **petite astuce** qui peut être pratique, mais vous n'en aurez pas souvent besoin.

Si vous voulez :

* déclarer le paramètre de requête `q` sans `Query` ni valeur par défaut
* déclarer le paramètre de chemin `item_id` en utilisant `Path`
* les avoir dans un ordre différent
* ne pas utiliser `Annotated`

... Python a une petite syntaxe spéciale pour cela.

Passez `*`, comme premier paramètre de la fonction.

Python ne fera rien avec ce `*`, mais il saura que tous les paramètres suivants doivent être appelés comme arguments « mots-clés » (paires clé-valeur), également connus sous le nom de <abbr title="De : K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. Même s'ils n'ont pas de valeur par défaut.

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### Mieux avec `Annotated` { #better-with-annotated }

Gardez à l'esprit que si vous utilisez `Annotated`, comme vous n'utilisez pas les valeurs par défaut des paramètres de fonction, vous n'aurez pas ce problème, et vous n'aurez probablement pas besoin d'utiliser `*`.

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## Validations numériques : supérieur ou égal { #number-validations-greater-than-or-equal }

Avec `Query` et `Path` (et d'autres que vous verrez plus tard) vous pouvez déclarer des contraintes numériques.

Ici, avec `ge=1`, `item_id` devra être un nombre entier « `g`reater than or `e`qual » à `1`.

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## Validations numériques : supérieur et inférieur ou égal { #number-validations-greater-than-and-less-than-or-equal }

La même chose s'applique pour :

* `gt` : `g`reater `t`han
* `le` : `l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## Validations numériques : flottants, supérieur et inférieur { #number-validations-floats-greater-than-and-less-than }

Les validations numériques fonctionnent également pour les valeurs `float`.

C'est ici qu'il devient important de pouvoir déclarer <abbr title="greater than - supérieur à"><code>gt</code></abbr> et pas seulement <abbr title="greater than or equal - supérieur ou égal"><code>ge</code></abbr>. Avec cela, vous pouvez exiger, par exemple, qu'une valeur doit être supérieure à `0`, même si elle est inférieure à `1`.

Ainsi, `0.5` serait une valeur valide. Mais `0.0` ou `0` ne le serait pas.

Et la même chose pour <abbr title="less than - inférieur à"><code>lt</code></abbr>.

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## Pour résumer { #recap }

Avec `Query`, `Path` (et d'autres que vous verrez plus tard) vous pouvez déclarer des métadonnées et des validations de chaînes de la même manière qu'avec les [Paramètres de requête et validations de chaînes](query-params-str-validations.md).

Et vous pouvez également déclarer des validations numériques :

* `gt` : `g`reater `t`han
* `ge` : `g`reater than or `e`qual
* `lt` : `l`ess `t`han
* `le` : `l`ess than or `e`qual

/// info

`Query`, `Path`, et d'autres classes que vous verrez plus tard sont des sous-classes d'une classe commune `Param`.

Tous partagent les mêmes paramètres pour des validations supplémentaires et des métadonnées que vous avez vu précédemment.

///

/// note | Détails techniques

Lorsque vous importez `Query`, `Path` et d'autres de `fastapi`, ce sont en fait des fonctions.

Ces dernières, lorsqu'elles sont appelées, renvoient des instances de classes du même nom.

Ainsi, vous importez `Query`, qui est une fonction. Et lorsque vous l'appelez, elle renvoie une instance d'une classe également nommée `Query`.

Ces fonctions sont là (au lieu d'utiliser simplement les classes directement) pour que votre éditeur ne marque pas d'erreurs sur leurs types.

De cette façon, vous pouvez utiliser votre éditeur et vos outils de codage habituels sans avoir à ajouter des configurations personnalisées pour ignorer ces erreurs.

///
