# OpenAPI Callbacks

Podrías crear una API con una *path operation* que podría desencadenar un request a una *API externa* creada por alguien más (probablemente el mismo desarrollador que estaría *usando* tu API).

El proceso que ocurre cuando tu aplicación API llama a la *API externa* se llama un "callback". Porque el software que escribió el desarrollador externo envía un request a tu API y luego tu API *responde*, enviando un request a una *API externa* (que probablemente fue creada por el mismo desarrollador).

En este caso, podrías querer documentar cómo esa API externa *debería* verse. Qué *path operation* debería tener, qué cuerpo debería esperar, qué response debería devolver, etc.

## Una aplicación con callbacks

Veamos todo esto con un ejemplo.

Imagina que desarrollas una aplicación que permite crear facturas.

Estas facturas tendrán un `id`, `title` (opcional), `customer`, y `total`.

El usuario de tu API (un desarrollador externo) creará una factura en tu API con un request POST.

Luego tu API (imaginemos):

* Enviará la factura a algún cliente del desarrollador externo.
* Recogerá el dinero.
* Enviará una notificación de vuelta al usuario de la API (el desarrollador externo).
    * Esto se hará enviando un request POST (desde *tu API*) a alguna *API externa* proporcionada por ese desarrollador externo (este es el "callback").

## La aplicación normal de **FastAPI**

Primero veamos cómo sería la aplicación API normal antes de agregar el callback.

Tendrá una *path operation* que recibirá un cuerpo `Invoice`, y un parámetro de query `callback_url` que contendrá la URL para el callback.

Esta parte es bastante normal, probablemente ya estés familiarizado con la mayor parte del código:

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[9:13,36:53] *}

/// tip | Consejo

El parámetro de query `callback_url` utiliza un tipo <a href="https://docs.pydantic.dev/latest/api/networks/" class="external-link" target="_blank">Url</a> de Pydantic.

///

Lo único nuevo es el `callbacks=invoices_callback_router.routes` como un argumento para el *decorador de path operation*. Veremos qué es eso a continuación.

## Documentar el callback

El código real del callback dependerá mucho de tu propia aplicación API.

Y probablemente variará mucho de una aplicación a otra.

Podría ser solo una o dos líneas de código, como:

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

Pero posiblemente la parte más importante del callback es asegurarse de que el usuario de tu API (el desarrollador externo) implemente la *API externa* correctamente, de acuerdo con los datos que *tu API* va a enviar en el request body del callback, etc.

Entonces, lo que haremos a continuación es agregar el código para documentar cómo debería verse esa *API externa* para recibir el callback de *tu API*.

Esa documentación aparecerá en la Swagger UI en `/docs` en tu API, y permitirá a los desarrolladores externos saber cómo construir la *API externa*.

Este ejemplo no implementa el callback en sí (eso podría ser solo una línea de código), solo la parte de documentación.

/// tip | Consejo

El callback real es solo un request HTTP.

Cuando implementes el callback tú mismo, podrías usar algo como <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> o <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requests</a>.

///

## Escribir el código de documentación del callback

Este código no se ejecutará en tu aplicación, solo lo necesitamos para *documentar* cómo debería verse esa *API externa*.

Pero, ya sabes cómo crear fácilmente documentación automática para una API con **FastAPI**.

Así que vamos a usar ese mismo conocimiento para documentar cómo debería verse la *API externa*... creando la(s) *path operation(s)* que la API externa debería implementar (las que tu API va a llamar).

/// tip | Consejo

Cuando escribas el código para documentar un callback, podría ser útil imaginar que eres ese *desarrollador externo*. Y que actualmente estás implementando la *API externa*, no *tu API*.

Adoptar temporalmente este punto de vista (del *desarrollador externo*) puede ayudarte a sentir que es más obvio dónde poner los parámetros, el modelo de Pydantic para el body, para el response, etc. para esa *API externa*.

///

### Crear un `APIRouter` de callback

Primero crea un nuevo `APIRouter` que contendrá uno o más callbacks.

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[3,25] *}

### Crear la *path operation* del callback

Para crear la *path operation* del callback utiliza el mismo `APIRouter` que creaste anteriormente.

Debería verse como una *path operation* normal de FastAPI:

* Probablemente debería tener una declaración del body que debería recibir, por ejemplo `body: InvoiceEvent`.
* Y también podría tener una declaración del response que debería devolver, por ejemplo `response_model=InvoiceEventReceived`.

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[16:18,21:22,28:32] *}

Hay 2 diferencias principales respecto a una *path operation* normal:

* No necesita tener ningún código real, porque tu aplicación nunca llamará a este código. Solo se usa para documentar la *API externa*. Así que, la función podría simplemente tener `pass`.
* El *path* puede contener una <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">expresión OpenAPI 3</a> (ver más abajo) donde puede usar variables con parámetros y partes del request original enviado a *tu API*.

### La expresión del path del callback

El *path* del callback puede tener una <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">expresión OpenAPI 3</a> que puede contener partes del request original enviado a *tu API*.

En este caso, es el `str`:

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

Entonces, si el usuario de tu API (el desarrollador externo) envía un request a *tu API* a:

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

con un JSON body de:

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

luego *tu API* procesará la factura, y en algún momento después, enviará un request de callback al `callback_url` (la *API externa*):

```
https://www.external.org/events/invoices/2expen51ve
```

con un JSON body que contiene algo como:

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

y esperaría un response de esa *API externa* con un JSON body como:

```JSON
{
    "ok": true
}
```

/// tip | Consejo

Observa cómo la URL del callback utilizada contiene la URL recibida como parámetro de query en `callback_url` (`https://www.external.org/events`) y también el `id` de la factura desde dentro del JSON body (`2expen51ve`).

///

### Agregar el router de callback

En este punto tienes las *path operation(s)* del callback necesarias (las que el *desarrollador externo* debería implementar en la *API externa*) en el router de callback que creaste antes.

Ahora usa el parámetro `callbacks` en el *decorador de path operation de tu API* para pasar el atributo `.routes` (que en realidad es solo un `list` de rutas/*path operations*) de ese router de callback:

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[35] *}

/// tip | Consejo

Observa que no estás pasando el router en sí (`invoices_callback_router`) a `callback=`, sino el atributo `.routes`, como en `invoices_callback_router.routes`.

///

### Revisa la documentación

Ahora puedes iniciar tu aplicación e ir a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Verás tu documentación incluyendo una sección de "Callbacks" para tu *path operation* que muestra cómo debería verse la *API externa*:

<img src="/img/tutorial/openapi-callbacks/image01.png">
