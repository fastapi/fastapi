# Métadonnées et URL des documents { #metadata-and-docs-urls }

Vous pouvez personnaliser plusieurs configurations de métadonnées dans votre application **FastAPI**.

## Métadonnées pour l'API { #metadata-for-api }

Vous pouvez définir les champs suivants qui sont utilisés dans la spécification OpenAPI et les interfaces utilisateur de documentation automatique de l’API :

| Paramètre | Type | Description |
|------------|------|-------------|
| `title` | `str` | Le titre de l’API. |
| `summary` | `str` | Un court résumé de l’API. <small>Disponible depuis OpenAPI 3.1.0, FastAPI 0.99.0.</small> |
| `description` | `str` | Une brève description de l’API. Elle peut utiliser Markdown. |
| `version` | `string` | La version de l’API. C’est la version de votre propre application, pas d’OpenAPI. Par exemple `2.5.0`. |
| `terms_of_service` | `str` | Une URL vers les Conditions d’utilisation de l’API. Le cas échéant, il doit s’agir d’une URL. |
| `contact` | `dict` | Les informations de contact pour l’API exposée. Cela peut contenir plusieurs champs. <details><summary>champs de <code>contact</code></summary><table><thead><tr><th>Paramètre</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>Le nom identifiant de la personne/organisation de contact.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>L’URL pointant vers les informations de contact. DOIT être au format d’une URL.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>L’adresse e-mail de la personne/organisation de contact. DOIT être au format d’une adresse e-mail.</td></tr></tbody></table></details> |
| `license_info` | `dict` | Les informations de licence pour l’API exposée. Cela peut contenir plusieurs champs. <details><summary>champs de <code>license_info</code></summary><table><thead><tr><th>Paramètre</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>OBLIGATOIRE</strong> (si un <code>license_info</code> est défini). Le nom de la licence utilisée pour l’API.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>Une expression de licence <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> pour l’API. Le champ <code>identifier</code> est mutuellement exclusif du champ <code>url</code>. <small>Disponible depuis OpenAPI 3.1.0, FastAPI 0.99.0.</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>Une URL vers la licence utilisée pour l’API. DOIT être au format d’une URL.</td></tr></tbody></table></details> |

Vous pouvez les définir comme suit :

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip | Astuce

Vous pouvez écrire du Markdown dans le champ `description` et il sera rendu dans la sortie.

///

Avec cette configuration, les documents API automatiques ressembleraient à :

<img src="/img/tutorial/metadata/image01.png">

## Identifiant de licence { #license-identifier }

Depuis OpenAPI 3.1.0 et FastAPI 0.99.0, vous pouvez également définir `license_info` avec un `identifier` au lieu d’une `url`.

Par exemple :

{* ../../docs_src/metadata/tutorial001_1_py310.py hl[31] *}

## Métadonnées pour les tags { #metadata-for-tags }

Vous pouvez également ajouter des métadonnées supplémentaires pour les différents tags utilisés pour regrouper vos chemins d'accès avec le paramètre `openapi_tags`.

Il prend une liste contenant un dictionnaire pour chaque tag.

Chaque dictionnaire peut contenir :

* `name` (**requis**) : un `str` avec le même nom de tag que vous utilisez dans le paramètre `tags` de vos *chemins d'accès* et `APIRouter`s.
* `description` : un `str` avec une courte description pour le tag. Il peut contenir du Markdown et sera affiché dans l’interface utilisateur de la documentation.
* `externalDocs` : un `dict` décrivant une documentation externe avec :
    * `description` : un `str` avec une courte description pour la documentation externe.
    * `url` (**requis**) : un `str` avec l’URL de la documentation externe.

### Créer des métadonnées pour les tags { #create-metadata-for-tags }

Essayons cela avec un exemple de tags pour `users` et `items`.

Créez des métadonnées pour vos tags et transmettez-les au paramètre `openapi_tags` :

{* ../../docs_src/metadata/tutorial004_py310.py hl[3:16,18] *}

Notez que vous pouvez utiliser Markdown à l’intérieur des descriptions, par exemple « login » sera affiché en gras (**login**) et « fancy » sera affiché en italique (_fancy_).

/// tip | Astuce

Vous n’avez pas à ajouter des métadonnées pour tous les tags que vous utilisez.

///

### Utiliser vos tags { #use-your-tags }

Utilisez le paramètre `tags` avec vos *chemins d'accès* (et `APIRouter`s) pour les affecter à différents tags :

{* ../../docs_src/metadata/tutorial004_py310.py hl[21,26] *}

/// info

En savoir plus sur les tags dans [Configuration de chemins d'accès](path-operation-configuration.md#tags){.internal-link target=_blank}.

///

### Consultez les documents { #check-the-docs }

Désormais, si vous consultez les documents, ils afficheront toutes les métadonnées supplémentaires :

<img src="/img/tutorial/metadata/image02.png">

### Définir l’ordre des tags { #order-of-tags }

L’ordre de chaque dictionnaire de métadonnées de tag définit également l’ordre affiché dans l’interface utilisateur de la documentation.

Par exemple, même si `users` viendrait après `items` par ordre alphabétique, il est affiché avant, car nous avons ajouté ses métadonnées comme premier dictionnaire de la liste.

## URL OpenAPI { #openapi-url }

Par défaut, le schéma OpenAPI est servi à `/openapi.json`.

Mais vous pouvez le configurer avec le paramètre `openapi_url`.

Par exemple, pour qu’il soit servi à `/api/v1/openapi.json` :

{* ../../docs_src/metadata/tutorial002_py310.py hl[3] *}

Si vous souhaitez désactiver complètement le schéma OpenAPI, vous pouvez définir `openapi_url=None`, cela désactivera également les interfaces utilisateur de la documentation qui l’utilisent.

## URL des documents { #docs-urls }

Vous pouvez configurer les deux interfaces utilisateur de documentation incluses :

* **Swagger UI** : servie à `/docs`.
    * Vous pouvez définir son URL avec le paramètre `docs_url`.
    * Vous pouvez la désactiver en définissant `docs_url=None`.
* **ReDoc** : servie à `/redoc`.
    * Vous pouvez définir son URL avec le paramètre `redoc_url`.
    * Vous pouvez la désactiver en définissant `redoc_url=None`.

Par exemple, pour que Swagger UI soit servi à `/documentation` et désactiver ReDoc :

{* ../../docs_src/metadata/tutorial003_py310.py hl[3] *}
