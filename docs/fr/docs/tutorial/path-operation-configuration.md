# Configurer les chemins d'accès { #path-operation-configuration }

Vous pouvez passer plusieurs paramètres à votre *décorateur de chemin d'accès* pour le configurer.

/// warning | Alertes

Notez que ces paramètres sont passés directement au *décorateur de chemin d'accès*, et non à votre *fonction de chemin d'accès*.

///

## Définir le code d'état de la réponse { #response-status-code }

Vous pouvez définir le `status_code` (HTTP) à utiliser dans la réponse de votre *chemin d'accès*.

Vous pouvez passer directement le code `int`, comme `404`.

Mais si vous ne vous souvenez pas à quoi correspond chaque code numérique, vous pouvez utiliser les constantes abrégées dans `status` :

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

Ce code d'état sera utilisé dans la réponse et ajouté au schéma OpenAPI.

/// note | Détails techniques

Vous pouvez également utiliser `from starlette import status`.

**FastAPI** fournit le même `starlette.status` sous le nom `fastapi.status` pour votre commodité, en tant que développeur. Mais cela provient directement de Starlette.

///

## Ajouter des tags { #tags }

Vous pouvez ajouter des tags à votre *chemin d'accès*, en passant le paramètre `tags` avec une `list` de `str` (généralement un seul `str`) :

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

Ils seront ajoutés au schéma OpenAPI et utilisés par les interfaces de documentation automatiques :

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Utiliser des tags avec Enum { #tags-with-enums }

Si vous avez une grande application, vous pourriez finir par accumuler **plusieurs tags**, et vous voudrez vous assurer d'utiliser toujours le **même tag** pour les *chemins d'accès* associés.

Dans ces cas, il peut être judicieux de stocker les tags dans un `Enum`.

**FastAPI** le prend en charge de la même manière qu'avec des chaînes simples :

{* ../../docs_src/path_operation_configuration/tutorial002b_py310.py hl[1,8:10,13,18] *}

## Ajouter un résumé et une description { #summary-and-description }

Vous pouvez ajouter un `summary` et une `description` :

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[17:18] *}

## Utiliser la description depuis la docstring { #description-from-docstring }

Comme les descriptions ont tendance à être longues et à couvrir plusieurs lignes, vous pouvez déclarer la description du *chemin d'accès* dans la <dfn title="une chaîne multilignes comme première expression à l'intérieur d'une fonction (non assignée à une variable) utilisée pour la documentation">docstring</dfn> de la fonction et **FastAPI** la lira à partir de là.

Vous pouvez écrire <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> dans la docstring, il sera interprété et affiché correctement (en tenant compte de l'indentation de la docstring).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

Elle sera utilisée dans les documents interactifs :

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Définir la description de la réponse { #response-description }

Vous pouvez spécifier la description de la réponse avec le paramètre `response_description` :

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[18] *}

/// info

Notez que `response_description` se réfère spécifiquement à la réponse, tandis que `description` se réfère au *chemin d'accès* en général.

///

/// check | Vérifications

OpenAPI spécifie que chaque *chemin d'accès* requiert une description de réponse.

Donc, si vous n'en fournissez pas, **FastAPI** en générera automatiquement une « Réponse réussie ».

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Déprécier un *chemin d'accès* { #deprecate-a-path-operation }

Si vous devez marquer un *chemin d'accès* comme <dfn title="obsolète, il est recommandé de ne pas l'utiliser">déprécié</dfn>, sans pour autant le supprimer, passez le paramètre `deprecated` :

{* ../../docs_src/path_operation_configuration/tutorial006_py310.py hl[16] *}

Il sera clairement marqué comme déprécié dans les documents interactifs :

<img src="/img/tutorial/path-operation-configuration/image04.png">

Voyez à quoi ressemblent les *chemins d'accès* dépréciés et non dépréciés :

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Récapitulatif { #recap }

Vous pouvez facilement configurer et ajouter des métadonnées à vos *chemins d'accès* en passant des paramètres aux *décorateurs de chemin d'accès*.
