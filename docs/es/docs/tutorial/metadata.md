# Metadata y URLs de Docs

Puedes personalizar varias configuraciones de metadata en tu aplicación **FastAPI**.

## Metadata para la API

Puedes establecer los siguientes campos que se usan en la especificación OpenAPI y en las interfaces automáticas de documentación de la API:

| Parámetro | Tipo | Descripción |
|------------|------|-------------|
| `title` | `str` | El título de la API. |
| `summary` | `str` | Un resumen corto de la API. <small>Disponible desde OpenAPI 3.1.0, FastAPI 0.99.0.</small> |
| `description` | `str` | Una breve descripción de la API. Puede usar Markdown. |
| `version` | `string` | La versión de la API. Esta es la versión de tu propia aplicación, no de OpenAPI. Por ejemplo, `2.5.0`. |
| `terms_of_service` | `str` | Una URL a los Términos de Servicio para la API. Si se proporciona, debe ser una URL. |
| `contact` | `dict` | La información de contacto para la API expuesta. Puede contener varios campos. <details><summary><code>contact</code> fields</summary><table><thead><tr><th>Parámetro</th><th>Tipo</th><th>Descripción</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>El nombre identificativo de la persona/organización de contacto.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>La URL que apunta a la información de contacto. DEBE tener el formato de una URL.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>La dirección de correo electrónico de la persona/organización de contacto. DEBE tener el formato de una dirección de correo.</td></tr></tbody></table></details> |
| `license_info` | `dict` | La información de la licencia para la API expuesta. Puede contener varios campos. <details><summary><code>license_info</code> fields</summary><table><thead><tr><th>Parámetro</th><th>Tipo</th><th>Descripción</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>REQUERIDO</strong> (si se establece un <code>license_info</code>). El nombre de la licencia utilizada para la API.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>Una expresión de licencia <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> para la API. El campo <code>identifier</code> es mutuamente excluyente del campo <code>url</code>. <small>Disponible desde OpenAPI 3.1.0, FastAPI 0.99.0.</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>Una URL a la licencia utilizada para la API. DEBE tener el formato de una URL.</td></tr></tbody></table></details> |

Puedes configurarlos de la siguiente manera:

{* ../../docs_src/metadata/tutorial001.py hl[3:16, 19:32] *}

/// tip | Consejo

Puedes escribir Markdown en el campo `description` y se mostrará en el resultado.

///

Con esta configuración, la documentación automática de la API se vería así:

<img src="/img/tutorial/metadata/image01.png">

## Identificador de licencia

Desde OpenAPI 3.1.0 y FastAPI 0.99.0, también puedes establecer la `license_info` con un `identifier` en lugar de una `url`.

Por ejemplo:

{* ../../docs_src/metadata/tutorial001_1.py hl[31] *}

## Metadata para etiquetas

También puedes agregar metadata adicional para las diferentes etiquetas usadas para agrupar tus path operations con el parámetro `openapi_tags`.

Este toma una list que contiene un diccionario para cada etiqueta.

Cada diccionario puede contener:

* `name` (**requerido**): un `str` con el mismo nombre de etiqueta que usas en el parámetro `tags` en tus *path operations* y `APIRouter`s.
* `description`: un `str` con una breve descripción de la etiqueta. Puede tener Markdown y se mostrará en la interfaz de documentación.
* `externalDocs`: un `dict` que describe documentación externa con:
    * `description`: un `str` con una breve descripción para la documentación externa.
    * `url` (**requerido**): un `str` con la URL para la documentación externa.

### Crear metadata para etiquetas

Probemos eso en un ejemplo con etiquetas para `users` y `items`.

Crea metadata para tus etiquetas y pásala al parámetro `openapi_tags`:

{* ../../docs_src/metadata/tutorial004.py hl[3:16,18] *}

Nota que puedes utilizar Markdown dentro de las descripciones, por ejemplo "login" se mostrará en negrita (**login**) y "fancy" se mostrará en cursiva (_fancy_).

/// tip | Consejo

No tienes que agregar metadata para todas las etiquetas que uses.

///

### Usar tus etiquetas

Usa el parámetro `tags` con tus *path operations* (y `APIRouter`s) para asignarlas a diferentes etiquetas:

{* ../../docs_src/metadata/tutorial004.py hl[21,26] *}

/// info | Información

Lee más sobre etiquetas en [Configuración de Path Operation](path-operation-configuration.md#tags){.internal-link target=_blank}.

///

### Revisa la documentación

Ahora, si revisas la documentación, mostrará toda la metadata adicional:

<img src="/img/tutorial/metadata/image02.png">

### Orden de las etiquetas

El orden de cada diccionario de metadata de etiqueta también define el orden mostrado en la interfaz de documentación.

Por ejemplo, aunque `users` iría después de `items` en orden alfabético, se muestra antes porque agregamos su metadata como el primer diccionario en la list.

## URL de OpenAPI

Por defecto, el esquema OpenAPI se sirve en `/openapi.json`.

Pero puedes configurarlo con el parámetro `openapi_url`.

Por ejemplo, para configurarlo para que se sirva en `/api/v1/openapi.json`:

{* ../../docs_src/metadata/tutorial002.py hl[3] *}

Si quieres deshabilitar el esquema OpenAPI completamente, puedes establecer `openapi_url=None`, eso también deshabilitará las interfaces de usuario de documentación que lo usan.

## URLs de Docs

Puedes configurar las dos interfaces de usuario de documentación incluidas:

* **Swagger UI**: servida en `/docs`.
    * Puedes establecer su URL con el parámetro `docs_url`.
    * Puedes deshabilitarla estableciendo `docs_url=None`.
* **ReDoc**: servida en `/redoc`.
    * Puedes establecer su URL con el parámetro `redoc_url`.
    * Puedes deshabilitarla estableciendo `redoc_url=None`.

Por ejemplo, para configurar Swagger UI para que se sirva en `/documentation` y deshabilitar ReDoc:

{* ../../docs_src/metadata/tutorial003.py hl[3] *}
