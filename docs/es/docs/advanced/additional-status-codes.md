# Códigos de Estado Adicionales

Por defecto, **FastAPI** devolverá los responses usando un `JSONResponse`, colocando el contenido que devuelves desde tu *path operation* dentro de ese `JSONResponse`.

Usará el código de estado por defecto o el que configures en tu *path operation*.

## Códigos de estado adicionales

Si quieres devolver códigos de estado adicionales aparte del principal, puedes hacerlo devolviendo un `Response` directamente, como un `JSONResponse`, y configurando el código de estado adicional directamente.

Por ejemplo, supongamos que quieres tener una *path operation* que permita actualizar elementos, y devuelva códigos de estado HTTP de 200 "OK" cuando sea exitoso.

Pero también quieres que acepte nuevos elementos. Y cuando los elementos no existían antes, los crea y devuelve un código de estado HTTP de 201 "Created".

Para lograr eso, importa `JSONResponse`, y devuelve tu contenido allí directamente, configurando el `status_code` que deseas:

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | Advertencia

Cuando devuelves un `Response` directamente, como en el ejemplo anterior, se devuelve directamente.

No se serializará con un modelo, etc.

Asegúrate de que tenga los datos que deseas que tenga y que los valores sean JSON válidos (si estás usando `JSONResponse`).

///

/// note | Detalles Técnicos

También podrías usar `from starlette.responses import JSONResponse`.

**FastAPI** proporciona los mismos `starlette.responses` que `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles provienen directamente de Starlette. Lo mismo con `status`.

///

## OpenAPI y documentación de API

Si devuelves códigos de estado adicionales y responses directamente, no se incluirán en el esquema de OpenAPI (la documentación de la API), porque FastAPI no tiene una forma de saber de antemano qué vas a devolver.

Pero puedes documentarlo en tu código, usando: [Responses Adicionales](additional-responses.md){.internal-link target=_blank}.
