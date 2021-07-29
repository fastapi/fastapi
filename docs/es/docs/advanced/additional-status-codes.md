# Códigos de estado adicionales

Por defecto, **FastAPI** devolverá las respuestas utilizando una `JSONResponse`, poniendo el contenido que devuelves en tu *operación de path* dentro de esa `JSONResponse`.

Utilizará el código de estado por defecto, o el que hayas asignado en tu *operación de path*.

## Códigos de estado adicionales

Si quieres devolver códigos de estado adicionales además del principal, puedes hacerlo devolviendo directamente una `Response`, como una `JSONResponse`, y asignar directamente el código de estado adicional.

Por ejemplo, digamos que quieres tener una *operación de path* que permita actualizar ítems y devolver códigos de estado HTTP 200 "OK" cuando sea exitosa.

Pero también quieres que acepte nuevos ítems. Cuando los ítems no existan anteriormente, serán creados y devolverá un código de estado HTTP 201 "Created".

Para conseguir esto importa `JSONResponse` y devuelve ahí directamente tu contenido, asignando el `status_code` que quieras:

```Python hl_lines="2  19"
{!../../../docs_src/additional_status_codes/tutorial001.py!}
```

!!! warning "Advertencia"
    Cuando devuelves directamente una `Response`, como en los ejemplos anteriores, será devuelta directamente.

    No será serializado con el modelo, etc.

    Asegurate de que la respuesta tenga los datos que quieras, y que los valores sean JSON válidos (si estás usando `JSONResponse`).

!!! note "Detalles Técnicos"
    También podrías utilizar `from starlette.responses import JSONResponse`.

    **FastAPI** provee las mismas `starlette.responses` que `fastapi.responses` simplemente como una convención para ti, el desarrollador. Pero la mayoría de las respuestas disponibles vienen directamente de Starlette. Lo mismo con `status`.

## OpenAPI y documentación de API

Si quieres devolver códigos de estado y respuestas adicionales directamente, estas no estarán incluidas en el schema de OpenAPI (documentación de API), porque FastAPI no tiene una manera de conocer de antemano lo que vas a devolver.

Pero puedes documentar eso en tu código usando [Respuestas Adicionales](additional-responses.md){.internal-link target=_blank}.
