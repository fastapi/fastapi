# Parámetros de Cookie

Puedes definir parámetros de Cookie de la misma manera que defines los parámetros `Query` y `Path`.

## Importar `Cookie`

Primero importa `Cookie`:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## Declarar parámetros de `Cookie`

Luego declara los parámetros de cookie usando la misma estructura que con `Path` y `Query`.

Puedes definir el valor por defecto así como toda la validación extra o los parámetros de anotación:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Detalles Técnicos

`Cookie` es una clase "hermana" de `Path` y `Query`. También hereda de la misma clase común `Param`.

Pero recuerda que cuando importas `Query`, `Path`, `Cookie` y otros desde `fastapi`, en realidad son funciones que devuelven clases especiales.

///

/// info | Información

Para declarar cookies, necesitas usar `Cookie`, porque de lo contrario los parámetros serían interpretados como parámetros de query.

///

## Resumen

Declara cookies con `Cookie`, usando el mismo patrón común que `Query` y `Path`.
