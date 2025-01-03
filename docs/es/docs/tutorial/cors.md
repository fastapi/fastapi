# CORS (Cross-Origin Resource Sharing)

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS o "Cross-Origin Resource Sharing"</a> se refiere a situaciones en las que un frontend que se ejecuta en un navegador tiene código JavaScript que se comunica con un backend, y el backend está en un "origen" diferente al frontend.

## Origen

Un origen es la combinación de protocolo (`http`, `https`), dominio (`myapp.com`, `localhost`, `localhost.tiangolo.com`) y puerto (`80`, `443`, `8080`).

Así que, todos estos son orígenes diferentes:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Aunque todos están en `localhost`, usan protocolos o puertos diferentes, por lo tanto, son "orígenes" diferentes.

## Pasos

Entonces, digamos que tienes un frontend corriendo en tu navegador en `http://localhost:8080`, y su JavaScript está tratando de comunicarse con un backend corriendo en `http://localhost` (porque no especificamos un puerto, el navegador asumirá el puerto por defecto `80`).

Entonces, el navegador enviará un request HTTP `OPTIONS` al backend `:80`, y si el backend envía los headers apropiados autorizando la comunicación desde este origen diferente (`http://localhost:8080`), entonces el navegador `:8080` permitirá que el JavaScript en el frontend envíe su request al backend `:80`.

Para lograr esto, el backend `:80` debe tener una lista de "orígenes permitidos".

En este caso, la lista tendría que incluir `http://localhost:8080` para que el frontend `:8080` funcione correctamente.

## Comodines

También es posible declarar la lista como `"*"` (un "comodín") para decir que todos están permitidos.

Pero eso solo permitirá ciertos tipos de comunicación, excluyendo todo lo que implique credenciales: Cookies, headers de autorización como los utilizados con Bearer Tokens, etc.

Así que, para que todo funcione correctamente, es mejor especificar explícitamente los orígenes permitidos.

## Usa `CORSMiddleware`

Puedes configurarlo en tu aplicación **FastAPI** usando el `CORSMiddleware`.

* Importa `CORSMiddleware`.
* Crea una lista de orígenes permitidos (como strings).
* Agrégalo como un "middleware" a tu aplicación **FastAPI**.

También puedes especificar si tu backend permite:

* Credenciales (headers de autorización, cookies, etc).
* Métodos HTTP específicos (`POST`, `PUT`) o todos ellos con el comodín `"*"`.
* Headers HTTP específicos o todos ellos con el comodín `"*"`.

{* ../../docs_src/cors/tutorial001.py hl[2,6:11,13:19] *}

Los parámetros predeterminados utilizados por la implementación de `CORSMiddleware` son restrictivos por defecto, por lo que necesitarás habilitar explícitamente orígenes, métodos o headers particulares para que los navegadores estén permitidos de usarlos en un contexto de Cross-Domain.

Se admiten los siguientes argumentos:

* `allow_origins` - Una lista de orígenes que deberían estar permitidos para hacer requests cross-origin. Por ejemplo, `['https://example.org', 'https://www.example.org']`. Puedes usar `['*']` para permitir cualquier origen.
* `allow_origin_regex` - Una cadena regex para coincidir con orígenes que deberían estar permitidos para hacer requests cross-origin. por ejemplo, `'https://.*\.example\.org'`.
* `allow_methods` - Una lista de métodos HTTP que deberían estar permitidos para requests cross-origin. Por defecto es `['GET']`. Puedes usar `['*']` para permitir todos los métodos estándar.
* `allow_headers` - Una lista de headers de request HTTP que deberían estar soportados para requests cross-origin. Por defecto es `[]`. Puedes usar `['*']` para permitir todos los headers. Los headers `Accept`, `Accept-Language`, `Content-Language` y `Content-Type` siempre están permitidos para <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests" class="external-link" rel="noopener" target="_blank">requests CORS simples</a>.
* `allow_credentials` - Indica que las cookies deberían estar soportadas para requests cross-origin. Por defecto es `False`. Además, `allow_origins` no puede ser configurado a `['*']` para que las credenciales estén permitidas, los orígenes deben ser especificados.
* `expose_headers` - Indica cualquier header de response que debería ser accesible para el navegador. Por defecto es `[]`.
* `max_age` - Establece un tiempo máximo en segundos para que los navegadores almacenen en caché los responses CORS. Por defecto es `600`.

El middleware responde a dos tipos particulares de request HTTP...

### Requests de preflight CORS

Estos son cualquier request `OPTIONS` con headers `Origin` y `Access-Control-Request-Method`.

En este caso, el middleware interceptará el request entrante y responderá con los headers CORS adecuados, y un response `200` o `400` con fines informativos.

### Requests simples

Cualquier request con un header `Origin`. En este caso, el middleware pasará el request a través de lo normal, pero incluirá los headers CORS adecuados en el response.

## Más info

Para más información sobre <abbr title="Cross-Origin Resource Sharing">CORS</abbr>, revisa la <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">documentación de CORS de Mozilla</a>.

/// note | Detalles Técnicos

También podrías usar `from starlette.middleware.cors import CORSMiddleware`.

**FastAPI** proporciona varios middlewares en `fastapi.middleware` como una conveniencia para ti, el desarrollador. Pero la mayoría de los middlewares disponibles provienen directamente de Starlette.

///
