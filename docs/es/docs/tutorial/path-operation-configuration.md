# Configuración de Path Operation

Hay varios parámetros que puedes pasar a tu *path operation decorator* para configurarlo.

/// warning | Advertencia

Ten en cuenta que estos parámetros se pasan directamente al *path operation decorator*, no a tu *path operation function*.

///

## Código de Estado del Response

Puedes definir el `status_code` (HTTP) que se utilizará en el response de tu *path operation*.

Puedes pasar directamente el código `int`, como `404`.

Pero si no recuerdas para qué es cada código numérico, puedes usar las constantes atajo en `status`:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

Ese código de estado se usará en el response y se añadirá al esquema de OpenAPI.

/// note | Detalles Técnicos

También podrías usar `from starlette import status`.

**FastAPI** ofrece el mismo `starlette.status` como `fastapi.status` solo por conveniencia para ti, el desarrollador. Pero viene directamente de Starlette.

///

## Tags

Puedes añadir tags a tu *path operation*, pasando el parámetro `tags` con un `list` de `str` (comúnmente solo una `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

Serán añadidas al esquema de OpenAPI y usadas por las interfaces de documentación automática:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Tags con Enums

Si tienes una gran aplicación, podrías terminar acumulando **varias tags**, y querrías asegurarte de que siempre uses la **misma tag** para *path operations* relacionadas.

En estos casos, podría tener sentido almacenar las tags en un `Enum`.

**FastAPI** soporta eso de la misma manera que con strings normales:

{* ../../docs_src/path_operation_configuration/tutorial002b.py hl[1,8:10,13,18] *}

## Resumen y Descripción

Puedes añadir un `summary` y `description`:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[18:19] *}

## Descripción desde docstring

Como las descripciones tienden a ser largas y cubrir múltiples líneas, puedes declarar la descripción de la *path operation* en la <abbr title="un string de múltiples líneas como la primera expresión dentro de una función (no asignada a ninguna variable) usada para documentación">docstring</abbr> de la función y **FastAPI** la leerá desde allí.

Puedes escribir <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> en el docstring, se interpretará y mostrará correctamente (teniendo en cuenta la indentación del docstring).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

Será usado en la documentación interactiva:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Descripción del Response

Puedes especificar la descripción del response con el parámetro `response_description`:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[19] *}

/// info | Información

Ten en cuenta que `response_description` se refiere específicamente al response, mientras que `description` se refiere a la *path operation* en general.

///

/// check | Revisa

OpenAPI especifica que cada *path operation* requiere una descripción de response.

Entonces, si no proporcionas una, **FastAPI** generará automáticamente una de "Response exitoso".

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Deprecar una *path operation*

Si necesitas marcar una *path operation* como <abbr title="obsoleta, se recomienda no usarla">deprecated</abbr>, pero sin eliminarla, pasa el parámetro `deprecated`:

{* ../../docs_src/path_operation_configuration/tutorial006.py hl[16] *}

Se marcará claramente como deprecado en la documentación interactiva:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Revisa cómo lucen las *path operations* deprecadas y no deprecadas:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Resumen

Puedes configurar y añadir metadatos a tus *path operations* fácilmente pasando parámetros a los *path operation decorators*.
