# Configuración Avanzada de la Path Operation

## OpenAPI operationId

!!! warning
    Si no eres una persona "experta" en OpenAPI, probablemente no necesitas leer esto.

Puedes asignar el `operationId` de la OpenAPI para ser usado en tu *path operation* con el parámetro `operation_id`.

Deberías asegurarte de que sea único para cada operación.

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial001.py!}
```

### Usando el nombre de la *función de operación de camino* en el operationId

Si tu quieres usar tus nombres de funciones de API como `operationId`s, puedes iterar sobre todos ellos y sobrescribir `operation_id` de cada *operación de camino* usando su `APIRoute.name`.

Deberías hacerlo después de adicionar todas tus *operaciones de camino*.

```Python hl_lines="2 12 13 14 15 16 17 18 19 20 21 24"
{!../../../docs_src/path_operation_advanced_configuration/tutorial002.py!}
```

!!! tip
    Si llama manualmente a `app.openapi()`, debe actualizar el `operationId`s antes de eso.

!!! warning
    Si hace esto, debes asegurarte de que cada una de tus *funciones de operación de camino* tenga un nombre único.

    Incluso si están en diferentes módulos (archivos Python).

## Excluir de OpenAPI

Para excluir una *operación de camino* del esquema OpenAPI generado (y por tanto del la documentación generada automáticamente), use el parámetro `include_in_schema` y asigne el valor como `False`;

```Python hl_lines="6"
{!../../../docs_src/path_operation_advanced_configuration/tutorial003.py!}
```

## Descripción Avanzada desde docstring

Puedes limitar las líneas usadas desde la docstring de una *operación de camino* para OpenAPI.

Adding an `\f` (an escaped "form feed" character) causes **FastAPI** to truncate the output used for OpenAPI at this point.

Agregar un `\f` (un carácter de "form feed" escapado) hace que **FastAPI** trunque la salida utilizada para OpenAPI en ese punto.

No será mostrado en la documentación, pero otras herramientas (como Sphinx) serán capaces de usar el resto.

```Python hl_lines="19 20 21 22 23 24 25 26 27 28 29"
{!../../../docs_src/path_operation_advanced_configuration/tutorial004.py!}
```
