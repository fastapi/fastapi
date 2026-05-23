# Detrás de un Proxy { #behind-a-proxy }

En muchas situaciones, usarías un **proxy** como Traefik o Nginx delante de tu app de FastAPI.

Estos proxies podrían manejar certificados HTTPS y otras cosas.

## Headers reenviados por el Proxy { #proxy-forwarded-headers }

Un **proxy** delante de tu aplicación normalmente establecería algunos headers sobre la marcha antes de enviar los requests a tu **server** para que el servidor sepa que el request fue **reenviado** por el proxy, informándole la URL original (pública), incluyendo el dominio, que está usando HTTPS, etc.

El programa **server** (por ejemplo **Uvicorn** a través de **FastAPI CLI**) es capaz de interpretar esos headers, y luego pasar esa información a tu aplicación.

Pero por seguridad, como el server no sabe que está detrás de un proxy confiable, no interpretará esos headers.

/// note | Detalles Técnicos

Los headers del proxy son:

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

### Habilitar headers reenviados por el Proxy { #enable-proxy-forwarded-headers }

Puedes iniciar FastAPI CLI con la *Opción de CLI* `--forwarded-allow-ips` y pasar las direcciones IP que deberían ser confiables para leer esos headers reenviados.

Si lo estableces a `--forwarded-allow-ips="*"`, confiaría en todas las IPs entrantes.

Si tu **server** está detrás de un **proxy** confiable y solo el proxy le habla, esto haría que acepte cualquiera que sea la IP de ese **proxy**.

<div class="termy">

```console
$ fastapi run --forwarded-allow-ips="*"

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Redirecciones con HTTPS { #redirects-with-https }

Por ejemplo, digamos que defines una *path operation* `/items/`:

{* ../../docs_src/behind_a_proxy/tutorial001_01_py310.py hl[6] *}

Si el cliente intenta ir a `/items`, por defecto, sería redirigido a `/items/`.

Pero antes de configurar la *Opción de CLI* `--forwarded-allow-ips` podría redirigir a `http://localhost:8000/items/`.

Pero quizá tu aplicación está alojada en `https://mysuperapp.com`, y la redirección debería ser a `https://mysuperapp.com/items/`.

Al configurar `--proxy-headers` ahora FastAPI podrá redirigir a la ubicación correcta. 😎

```
https://mysuperapp.com/items/
```

/// tip | Consejo

Si quieres aprender más sobre HTTPS, revisa la guía [Acerca de HTTPS](../deployment/https.md).

///

### Cómo funcionan los headers reenviados por el Proxy { #how-proxy-forwarded-headers-work }

Aquí tienes una representación visual de cómo el **proxy** añade headers reenviados entre el cliente y el **application server**:

```mermaid
sequenceDiagram
    participant Client as Cliente
    participant Proxy as Proxy/Load Balancer
    participant Server as Servidor de FastAPI

    Client->>Proxy: HTTPS Request<br/>Host: mysuperapp.com<br/>Path: /items

    Note over Proxy: El proxy añade headers reenviados

    Proxy->>Server: HTTP Request<br/>X-Forwarded-For: [client IP]<br/>X-Forwarded-Proto: https<br/>X-Forwarded-Host: mysuperapp.com<br/>Path: /items

    Note over Server: El servidor interpreta los headers<br/>(si --forwarded-allow-ips está configurado)

    Server->>Proxy: HTTP Response<br/>con URLs HTTPS correctas

    Proxy->>Client: HTTPS Response
```

El **proxy** intercepta el request original del cliente y añade los *headers* especiales de reenvío (`X-Forwarded-*`) antes de pasar el request al **application server**.

Estos headers preservan información sobre el request original que de otro modo se perdería:

* **X-Forwarded-For**: La IP original del cliente
* **X-Forwarded-Proto**: El protocolo original (`https`)
* **X-Forwarded-Host**: El host original (`mysuperapp.com`)

Cuando **FastAPI CLI** está configurado con `--forwarded-allow-ips`, confía en estos headers y los usa, por ejemplo para generar las URLs correctas en redirecciones.

## Proxy con un prefijo de path eliminado { #proxy-with-a-stripped-path-prefix }

Podrías tener un proxy que añada un prefijo de path a tu aplicación.

En estos casos, puedes usar `root_path` para configurar tu aplicación.

El `root_path` es un mecanismo proporcionado por la especificación ASGI (en la que está construido FastAPI, a través de Starlette).

El `root_path` se usa para manejar estos casos específicos.

Y también se usa internamente al montar subaplicaciones.

Tener un proxy con un prefijo de path eliminado, en este caso, significa que podrías declarar un path en `/app` en tu código, pero luego añades una capa encima (el proxy) que situaría tu aplicación **FastAPI** bajo un path como `/api/v1`.

En este caso, el path original `/app` realmente sería servido en `/api/v1/app`.

Aunque todo tu código esté escrito asumiendo que solo existe `/app`.

{* ../../docs_src/behind_a_proxy/tutorial001_py310.py hl[6] *}

Y el proxy estaría **"eliminando"** el **prefijo del path** sobre la marcha antes de transmitir el request al servidor de aplicaciones (probablemente Uvicorn a través de FastAPI CLI), manteniendo a tu aplicación convencida de que está siendo servida en `/app`, así que no tienes que actualizar todo tu código para incluir el prefijo `/api/v1`.

Hasta aquí, todo funcionaría normalmente.

Pero luego, cuando abres la UI integrada de los docs (el frontend), esperaría obtener el esquema de OpenAPI en `/openapi.json`, en lugar de `/api/v1/openapi.json`.

Entonces, el frontend (que se ejecuta en el navegador) trataría de alcanzar `/openapi.json` y no podría obtener el esquema de OpenAPI.

Porque tenemos un proxy con un prefijo de path de `/api/v1` para nuestra aplicación, el frontend necesita obtener el esquema de OpenAPI en `/api/v1/openapi.json`.

```mermaid
graph LR

browser("Navegador")
proxy["Proxy en http://0.0.0.0:9999/api/v1/app"]
server["Servidor en http://127.0.0.1:8000/app"]

browser --> proxy
proxy --> server
```

/// tip | Consejo

La IP `0.0.0.0` se usa comúnmente para indicar que el programa escucha en todas las IPs disponibles en esa máquina/servidor.

///

La UI de los docs también necesitaría el esquema de OpenAPI para declarar que este API `servidor` se encuentra en `/api/v1` (detrás del proxy). Por ejemplo:

```JSON hl_lines="4-8"
{
    "openapi": "3.1.0",
    // Más cosas aquí
    "servers": [
        {
            "url": "/api/v1"
        }
    ],
    "paths": {
            // Más cosas aquí
    }
}
```

En este ejemplo, el "Proxy" podría ser algo como **Traefik**. Y el servidor sería algo como FastAPI CLI con **Uvicorn**, ejecutando tu aplicación de FastAPI.

### Proporcionando el `root_path` { #providing-the-root-path }

Para lograr esto, puedes usar la opción de línea de comandos `--root-path` como:

<div class="termy">

```console
$ fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Si usas Hypercorn, también tiene la opción `--root-path`.

/// note | Detalles Técnicos

La especificación ASGI define un `root_path` para este caso de uso.

Y la opción de línea de comandos `--root-path` proporciona ese `root_path`.

///

### Revisar el `root_path` actual { #checking-the-current-root-path }

Puedes obtener el `root_path` actual utilizado por tu aplicación para cada request, es parte del diccionario `scope` (que es parte de la especificación ASGI).

Aquí lo estamos incluyendo en el mensaje solo con fines de demostración.

{* ../../docs_src/behind_a_proxy/tutorial001_py310.py hl[8] *}

Luego, si inicias Uvicorn con:

<div class="termy">

```console
$ fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

El response sería algo como:

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

### Configurar el `root_path` en la app de FastAPI { #setting-the-root-path-in-the-fastapi-app }

Alternativamente, si no tienes una forma de proporcionar una opción de línea de comandos como `--root-path` o su equivalente, puedes configurar el parámetro `root_path` al crear tu app de FastAPI:

{* ../../docs_src/behind_a_proxy/tutorial002_py310.py hl[3] *}

Pasar el `root_path` a `FastAPI` sería el equivalente a pasar la opción de línea de comandos `--root-path` a Uvicorn o Hypercorn.

### Acerca de `root_path` { #about-root-path }

Ten en cuenta que el servidor (Uvicorn) no usará ese `root_path` para nada, a excepción de pasárselo a la app.

Pero si vas con tu navegador a [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app) verás el response normal:

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

Así que no se esperará que sea accedido en `http://127.0.0.1:8000/api/v1/app`.

Uvicorn esperará que el proxy acceda a Uvicorn en `http://127.0.0.1:8000/app`, y luego será responsabilidad del proxy añadir el prefijo extra `/api/v1` encima.

## Sobre proxies con un prefijo de path eliminado { #about-proxies-with-a-stripped-path-prefix }

Ten en cuenta que un proxy con prefijo de path eliminado es solo una de las formas de configurarlo.

Probablemente en muchos casos, el valor por defecto será que el proxy no tenga un prefijo de path eliminado.

En un caso así (sin un prefijo de path eliminado), el proxy escucharía algo como `https://myawesomeapp.com`, y luego si el navegador va a `https://myawesomeapp.com/api/v1/app` y tu servidor (por ejemplo, Uvicorn) escucha en `http://127.0.0.1:8000`, el proxy (sin un prefijo de path eliminado) accedería a Uvicorn en el mismo path: `http://127.0.0.1:8000/api/v1/app`.

## Probando localmente con Traefik { #testing-locally-with-traefik }

Puedes ejecutar fácilmente el experimento localmente con un prefijo de path eliminado usando [Traefik](https://docs.traefik.io/).

[Descarga Traefik](https://github.com/containous/traefik/releases), es un archivo binario único, puedes extraer el archivo comprimido y ejecutarlo directamente desde la terminal.

Luego crea un archivo `traefik.toml` con:

```TOML hl_lines="3"
[entryPoints]
  [entryPoints.http]
    address = ":9999"

[providers]
  [providers.file]
    filename = "routes.toml"
```

Esto le dice a Traefik que escuche en el puerto 9999 y que use otro archivo `routes.toml`.

/// tip | Consejo

Estamos utilizando el puerto 9999 en lugar del puerto HTTP estándar 80 para que no tengas que ejecutarlo con privilegios de administrador (`sudo`).

///

Ahora crea ese otro archivo `routes.toml`:

```TOML hl_lines="5  12  20"
[http]
  [http.middlewares]

    [http.middlewares.api-stripprefix.stripPrefix]
      prefixes = ["/api/v1"]

  [http.routers]

    [http.routers.app-http]
      entryPoints = ["http"]
      service = "app"
      rule = "PathPrefix(`/api/v1`)"
      middlewares = ["api-stripprefix"]

  [http.services]

    [http.services.app]
      [http.services.app.loadBalancer]
        [[http.services.app.loadBalancer.servers]]
          url = "http://127.0.0.1:8000"
```

Este archivo configura Traefik para usar el prefijo de path `/api/v1`.

Y luego Traefik redireccionará sus requests a tu Uvicorn ejecutándose en `http://127.0.0.1:8000`.

Ahora inicia Traefik:

<div class="termy">

```console
$ ./traefik --configFile=traefik.toml

INFO[0000] Configuration loaded from file: /home/user/awesomeapi/traefik.toml
```

</div>

Y ahora inicia tu app, utilizando la opción `--root-path`:

<div class="termy">

```console
$ fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Revisa los responses { #check-the-responses }

Ahora, si vas a la URL con el puerto para Uvicorn: [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app), verás el response normal:

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

/// tip | Consejo

Nota que incluso aunque estés accediendo en `http://127.0.0.1:8000/app`, muestra el `root_path` de `/api/v1`, tomado de la opción `--root-path`.

///

Y ahora abre la URL con el puerto para Traefik, incluyendo el prefijo de path: [http://127.0.0.1:9999/api/v1/app](http://127.0.0.1:9999/api/v1/app).

Obtenemos el mismo response:

```JSON
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

pero esta vez en la URL con el prefijo de path proporcionado por el proxy: `/api/v1`.

Por supuesto, la idea aquí es que todos accedan a la app a través del proxy, así que la versión con el prefijo de path `/api/v1` es la "correcta".

Y la versión sin el prefijo de path (`http://127.0.0.1:8000/app`), proporcionada directamente por Uvicorn, sería exclusivamente para que el _proxy_ (Traefik) la acceda.

Eso demuestra cómo el Proxy (Traefik) usa el prefijo de path y cómo el servidor (Uvicorn) usa el `root_path` de la opción `--root-path`.

### Revisa la UI de los docs { #check-the-docs-ui }

Pero aquí está la parte divertida. ✨

La forma "oficial" de acceder a la app sería a través del proxy con el prefijo de path que definimos. Así que, como esperaríamos, si intentas usar la UI de los docs servida por Uvicorn directamente, sin el prefijo de path en la URL, no funcionará, porque espera ser accedida a través del proxy.

Puedes verificarlo en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs):

<img src="/img/tutorial/behind-a-proxy/image01.png">

Pero si accedemos a la UI de los docs en la URL "oficial" usando el proxy con puerto `9999`, en `/api/v1/docs`, ¡funciona correctamente! 🎉

Puedes verificarlo en [http://127.0.0.1:9999/api/v1/docs](http://127.0.0.1:9999/api/v1/docs):

<img src="/img/tutorial/behind-a-proxy/image02.png">

Justo como queríamos. ✔️

Esto es porque FastAPI usa este `root_path` para crear el `server` por defecto en OpenAPI con la URL proporcionada por `root_path`.

## Servidores adicionales { #additional-servers }

/// warning | Advertencia

Este es un caso de uso más avanzado. Siéntete libre de omitirlo.

///

Por defecto, **FastAPI** creará un `server` en el esquema de OpenAPI con la URL para el `root_path`.

Pero también puedes proporcionar otros `servers` alternativos, por ejemplo, si deseas que *la misma* UI de los docs interactúe con un entorno de pruebas y de producción.

Si pasas una lista personalizada de `servers` y hay un `root_path` (porque tu API existe detrás de un proxy), **FastAPI** insertará un "server" con este `root_path` al comienzo de la lista.

Por ejemplo:

{* ../../docs_src/behind_a_proxy/tutorial003_py310.py hl[4:7] *}

Generará un esquema de OpenAPI como:

```JSON hl_lines="5-7"
{
    "openapi": "3.1.0",
    // Más cosas aquí
    "servers": [
        {
            "url": "/api/v1"
        },
        {
            "url": "https://stag.example.com",
            "description": "Staging environment"
        },
        {
            "url": "https://prod.example.com",
            "description": "Production environment"
        }
    ],
    "paths": {
            // Más cosas aquí
    }
}
```

/// tip | Consejo

Observa el server auto-generado con un valor `url` de `/api/v1`, tomado del `root_path`.

///

En la UI de los docs en [http://127.0.0.1:9999/api/v1/docs](http://127.0.0.1:9999/api/v1/docs) se vería como:

<img src="/img/tutorial/behind-a-proxy/image03.png">

/// tip | Consejo

La UI de los docs interactuará con el server que selecciones.

///

/// note | Detalles Técnicos

La propiedad `servers` en la especificación de OpenAPI es opcional.

Si no especificas el parámetro `servers` y `root_path` es igual a `/`, la propiedad `servers` en el esquema de OpenAPI generado se omitirá por completo por defecto, lo cual es equivalente a un único server con un valor `url` de `/`.

///

### Desactivar el server automático de `root_path` { #disable-automatic-server-from-root-path }

Si no quieres que **FastAPI** incluya un server automático usando el `root_path`, puedes usar el parámetro `root_path_in_servers=False`:

{* ../../docs_src/behind_a_proxy/tutorial004_py310.py hl[9] *}

y entonces no lo incluirá en el esquema de OpenAPI.

## Montando una sub-aplicación { #mounting-a-sub-application }

Si necesitas montar una sub-aplicación (como se describe en [Aplicaciones secundarias - Monturas](sub-applications.md)) mientras usas un proxy con `root_path`, puedes hacerlo normalmente, como esperarías.

FastAPI usará internamente el `root_path` de manera inteligente, así que simplemente funcionará. ✨
