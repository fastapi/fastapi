# Parámetros de Cookie { #cookie-parameters }

Puedes definir parámetros de Cookie de la misma manera que defines los parámetros `Query` y `Path`.

## Importar `Cookie` { #import-cookie }

Primero importa `Cookie`:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## Declarar parámetros de `Cookie` { #declare-cookie-parameters }

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

/// info | Información

Ten en cuenta que, como **los navegadores manejan las cookies** de formas especiales y por detrás, **no** permiten fácilmente que **JavaScript** las toque.

Si vas a la **UI de la documentación de la API** en `/docs` podrás ver la **documentación** de cookies para tus *path operations*.

Pero incluso si **rellenas los datos** y haces clic en "Execute", como la UI de la documentación funciona con **JavaScript**, las cookies no se enviarán y verás un mensaje de **error** como si no hubieras escrito ningún valor.

///

## Resumen { #recap }

Declara cookies con `Cookie`, usando el mismo patrón común que `Query` y `Path`.
