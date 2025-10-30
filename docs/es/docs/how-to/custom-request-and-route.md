# Clase personalizada de Request y APIRoute

En algunos casos, puede que quieras sobrescribir la lógica utilizada por las clases `Request` y `APIRoute`.

En particular, esta puede ser una buena alternativa a la lógica en un middleware.

Por ejemplo, si quieres leer o manipular el request body antes de que sea procesado por tu aplicación.

/// danger | Advertencia

Esta es una funcionalidad "avanzada".

Si apenas estás comenzando con **FastAPI**, quizás quieras saltar esta sección.

///

## Casos de uso

Algunos casos de uso incluyen:

* Convertir cuerpos de requests no-JSON a JSON (por ejemplo, <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>).
* Descomprimir cuerpos de requests comprimidos con gzip.
* Registrar automáticamente todos los request bodies.

## Manejo de codificaciones personalizadas de request body

Veamos cómo hacer uso de una subclase personalizada de `Request` para descomprimir requests gzip.

Y una subclase de `APIRoute` para usar esa clase de request personalizada.

### Crear una clase personalizada `GzipRequest`

/// tip | Consejo

Este es un ejemplo sencillo para demostrar cómo funciona. Si necesitas soporte para Gzip, puedes usar el [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank} proporcionado.

///

Primero, creamos una clase `GzipRequest`, que sobrescribirá el método `Request.body()` para descomprimir el cuerpo si hay un header apropiado.

Si no hay `gzip` en el header, no intentará descomprimir el cuerpo.

De esa manera, la misma clase de ruta puede manejar requests comprimidos con gzip o no comprimidos.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[8:15] *}

### Crear una clase personalizada `GzipRoute`

A continuación, creamos una subclase personalizada de `fastapi.routing.APIRoute` que hará uso de `GzipRequest`.

Esta vez, sobrescribirá el método `APIRoute.get_route_handler()`.

Este método devuelve una función. Y esa función es la que recibirá un request y devolverá un response.

Aquí lo usamos para crear un `GzipRequest` a partir del request original.

{* ../../docs_src/custom_request_and_route/tutorial001.py hl[18:26] *}

/// note | Detalles técnicos

Un `Request` tiene un atributo `request.scope`, que es simplemente un `dict` de Python que contiene los metadatos relacionados con el request.

Un `Request` también tiene un `request.receive`, que es una función para "recibir" el cuerpo del request.

El `dict` `scope` y la función `receive` son ambos parte de la especificación ASGI.

Y esas dos cosas, `scope` y `receive`, son lo que se necesita para crear una nueva *Request instance*.

Para aprender más sobre el `Request`, revisa <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">la documentación de Starlette sobre Requests</a>.

///

La única cosa que la función devuelta por `GzipRequest.get_route_handler` hace diferente es convertir el `Request` en un `GzipRequest`.

Haciendo esto, nuestro `GzipRequest` se encargará de descomprimir los datos (si es necesario) antes de pasarlos a nuestras *path operations*.

Después de eso, toda la lógica de procesamiento es la misma.

Pero debido a nuestros cambios en `GzipRequest.body`, el request body se descomprimirá automáticamente cuando sea cargado por **FastAPI** si es necesario.

## Accediendo al request body en un manejador de excepciones

/// tip | Consejo

Para resolver este mismo problema, probablemente sea mucho más fácil usar el `body` en un manejador personalizado para `RequestValidationError` ([Manejo de Errores](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}).

Pero este ejemplo sigue siendo válido y muestra cómo interactuar con los componentes internos.

///

También podemos usar este mismo enfoque para acceder al request body en un manejador de excepciones.

Todo lo que necesitamos hacer es manejar el request dentro de un bloque `try`/`except`:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[13,15] *}

Si ocurre una excepción, la `Request instance` aún estará en el alcance, así que podemos leer y hacer uso del request body cuando manejamos el error:

{* ../../docs_src/custom_request_and_route/tutorial002.py hl[16:18] *}

## Clase personalizada `APIRoute` en un router

También puedes establecer el parámetro `route_class` de un `APIRouter`:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[26] *}

En este ejemplo, las *path operations* bajo el `router` usarán la clase personalizada `TimedRoute`, y tendrán un header `X-Response-Time` extra en el response con el tiempo que tomó generar el response:

{* ../../docs_src/custom_request_and_route/tutorial003.py hl[13:20] *}
