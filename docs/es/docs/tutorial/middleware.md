# Middleware

Puedes añadir middleware a las aplicaciones de **FastAPI**.

Un "middleware" es una función que trabaja con cada **request** antes de que sea procesada por cualquier *path operation* específica. Y también con cada **response** antes de devolverla.

* Toma cada **request** que llega a tu aplicación.
* Puede entonces hacer algo a esa **request** o ejecutar cualquier código necesario.
* Luego pasa la **request** para que sea procesada por el resto de la aplicación (por alguna *path operation*).
* Después toma la **response** generada por la aplicación (por alguna *path operation*).
* Puede hacer algo a esa **response** o ejecutar cualquier código necesario.
* Luego devuelve la **response**.

/// note | Detalles Técnicos

Si tienes dependencias con `yield`, el código de salida se ejecutará *después* del middleware.

Si hubiera alguna tarea en segundo plano (documentada más adelante), se ejecutará *después* de todo el middleware.

///

## Crear un middleware

Para crear un middleware usas el decorador `@app.middleware("http")` encima de una función.

La función middleware recibe:

* La `request`.
* Una función `call_next` que recibirá la `request` como parámetro.
    * Esta función pasará la `request` a la correspondiente *path operation*.
    * Luego devuelve la `response` generada por la correspondiente *path operation*.
* Puedes entonces modificar aún más la `response` antes de devolverla.

{* ../../docs_src/middleware/tutorial001.py hl[8:9,11,14] *}

/// tip | Consejo

Ten en cuenta que los custom proprietary headers se pueden añadir <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">usando el prefijo 'X-'</a>.

Pero si tienes custom headers que deseas que un cliente en un navegador pueda ver, necesitas añadirlos a tus configuraciones de CORS ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}) usando el parámetro `expose_headers` documentado en <a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">la documentación de CORS de Starlette</a>.

///

/// note | Detalles Técnicos

También podrías usar `from starlette.requests import Request`.

**FastAPI** lo proporciona como una conveniencia para ti, el desarrollador. Pero viene directamente de Starlette.

///

### Antes y después de la `response`

Puedes añadir código que se ejecute con la `request`, antes de que cualquier *path operation* la reciba.

Y también después de que se genere la `response`, antes de devolverla.

Por ejemplo, podrías añadir un custom header `X-Process-Time` que contenga el tiempo en segundos que tomó procesar la request y generar una response:

{* ../../docs_src/middleware/tutorial001.py hl[10,12:13] *}

/// tip | Consejo

Aquí usamos <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a> en lugar de `time.time()` porque puede ser más preciso para estos casos de uso. 🤓

///

## Otros middlewares

Más adelante puedes leer sobre otros middlewares en la [Guía del Usuario Avanzado: Middleware Avanzado](../advanced/middleware.md){.internal-link target=_blank}.

Leerás sobre cómo manejar <abbr title="Cross-Origin Resource Sharing">CORS</abbr> con un middleware en la siguiente sección.
