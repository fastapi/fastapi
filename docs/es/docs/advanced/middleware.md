# Middleware Avanzado

En el tutorial principal leíste cómo agregar [Middleware Personalizado](../tutorial/middleware.md){.internal-link target=_blank} a tu aplicación.

Y luego también leíste cómo manejar [CORS con el `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

En esta sección veremos cómo usar otros middlewares.

## Agregando middlewares ASGI

Como **FastAPI** está basado en Starlette e implementa la especificación <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>, puedes usar cualquier middleware ASGI.

Un middleware no tiene que estar hecho para FastAPI o Starlette para funcionar, siempre que siga la especificación ASGI.

En general, los middlewares ASGI son clases que esperan recibir una aplicación ASGI como primer argumento.

Entonces, en la documentación de middlewares ASGI de terceros probablemente te indicarán que hagas algo como:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Pero FastAPI (en realidad Starlette) proporciona una forma más simple de hacerlo que asegura que los middlewares internos manejen errores del servidor y los controladores de excepciones personalizadas funcionen correctamente.

Para eso, usas `app.add_middleware()` (como en el ejemplo para CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` recibe una clase de middleware como primer argumento y cualquier argumento adicional que se le quiera pasar al middleware.

## Middlewares integrados

**FastAPI** incluye varios middlewares para casos de uso común, veremos a continuación cómo usarlos.

/// note | Detalles Técnicos

Para los próximos ejemplos, también podrías usar `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** proporciona varios middlewares en `fastapi.middleware` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los middlewares disponibles provienen directamente de Starlette.

///

## `HTTPSRedirectMiddleware`

Impone que todas las requests entrantes deben ser `https` o `wss`.

Cualquier request entrante a `http` o `ws` será redirigida al esquema seguro.

{* ../../docs_src/advanced_middleware/tutorial001.py hl[2,6] *}

## `TrustedHostMiddleware`

Impone que todas las requests entrantes tengan correctamente configurado el header `Host`, para proteger contra ataques de HTTP Host Header.

{* ../../docs_src/advanced_middleware/tutorial002.py hl[2,6:8] *}

Se soportan los siguientes argumentos:

* `allowed_hosts` - Una list de nombres de dominio que deberían ser permitidos como nombres de host. Se soportan dominios comodín como `*.example.com` para hacer coincidir subdominios. Para permitir cualquier nombre de host, usa `allowed_hosts=["*"]` u omite el middleware.

Si una request entrante no se valida correctamente, se enviará un response `400`.

## `GZipMiddleware`

Maneja responses GZip para cualquier request que incluya `"gzip"` en el header `Accept-Encoding`.

El middleware manejará tanto responses estándar como en streaming.

{* ../../docs_src/advanced_middleware/tutorial003.py hl[2,6] *}

Se soportan los siguientes argumentos:

* `minimum_size` - No comprimir con GZip responses que sean más pequeñas que este tamaño mínimo en bytes. Por defecto es `500`.
* `compresslevel` - Usado durante la compresión GZip. Es un entero que varía de 1 a 9. Por defecto es `9`. Un valor más bajo resulta en una compresión más rápida pero archivos más grandes, mientras que un valor más alto resulta en una compresión más lenta pero archivos más pequeños.

## Otros middlewares

Hay muchos otros middlewares ASGI.

Por ejemplo:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">`ProxyHeadersMiddleware` de Uvicorn</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Para ver otros middlewares disponibles, revisa <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">la documentación de Middleware de Starlette</a> y la <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">Lista ASGI Awesome</a>.
