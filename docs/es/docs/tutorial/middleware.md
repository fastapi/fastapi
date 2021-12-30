# Middleware

Puedes añadir middlewares a tus aplicaciones de **FastAPI**.

Un "middleware" es una función que se ejecuta con cada **petición** antes de que sea procesada por cualquier <abbr title="path operation">*operación de ruta*</abbr>. Y antes de devolver cada **respuesta**.

* Toma cada **petición** que llega a tu aplicación.
* Luego puede hacer algo con esa **petición** o ejecutar cualquier código necesario.
* Posteriormente, toma la **petición** para ser procesada por el resto de la aplicación (por alguna *operación de path*).
* Luego toma la **respuesta** generada por la aplicación (por alguna *operación de path*).
* Puede realizar algo con esa **respuesta** o ejecutar cualquier código necesario.
* Y por ultimo, retornar la **respuesta**.

!!! note " Detalles Técnicos "
    Si tienes dependencias que utilicen `yield`, el código de salida se ejecutara *después* del middleware.

    Si existen tareas ejecutándose en segundo plano (documentadas posteriormente), se ejecutaran *después* del middleware.

## Crear un middleware

Para crear un middleware debemos usar el decorador `@app.middleware("http")` encima de la función.

La función del middleware recibe:

* La `petición`.
* Una función <abbr title="para llamar después">`call_next`</abbr> que recibirá la `petición` como parámetro.
    * Esta función pasará la `petición` a la correspondiente <abbr title="path operation">*operación de path*</abbr>.
    * Posteriormente, retorna la `respuesta` generada por la *operación de path*.
* Luego, puedes modificar aún más la `respuesta` antes de devolverla.

```Python hl_lines="8-9  11  14"
{!../../../docs_src/middleware/tutorial001.py!}
```

!!! tip
    Ten en cuenta que puedes añadir <abbr title="encabezados">headers</abbr> personalizados <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">utilizando el prefijo 'X-' </a>.

    Pero, si tienes headers personalizados que deseas que un cliente pueda visualizar en un navegador, debes agregarlos a tus configuraciones de CORS ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}) usando el parámetro `expose_headers`, puedes consultar más en <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">la documentación de Starlette acerca de CORS</a>.

!!! note "Detalles Técnicos"
    También puedes utilizar `from starlette.requests import Request`.

    **FastAPI** lo proporciona directamente como una convencía para ti, el desarrollador. Pero viene directamente de Starlette.

### Antes y después de la `respuesta`

Puedes añadir código que se ejecute con la `petición`, antes de que cualquier *operación de path* la reciba.

También después de que la `respuesta` es generada, pero antes de devolverla.

Por ejemplo, puedes añadir un <abbr>header</abbr> personalizado `X-Process-Time` que contenga el tiempo en segundos que se requiere para procesar la petición y generar una respuesta:

```Python hl_lines="10  12-13"
{!../../../docs_src/middleware/tutorial001.py!}
```

## Otros middlewares

Puedes leer más acerca de otros middlewares en [Guia de Usuario Avanzado: Middleware Avanzado](../advanced/middleware.md){.internal-link target=_blank}.

Aprenderás como manejar el <abbr title="Cross-Origin Resource Sharing">CORS</abbr> con un middleware en la siguiente sección.
