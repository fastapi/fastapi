# WebSockets

Puedes usar <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a> con **FastAPI**.

## Instalar `WebSockets`

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, activarlo e instalar `websockets`:

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## Cliente WebSockets

### En producción

En tu sistema de producción, probablemente tengas un frontend creado con un framework moderno como React, Vue.js o Angular.

Y para comunicarte usando WebSockets con tu backend probablemente usarías las utilidades de tu frontend.

O podrías tener una aplicación móvil nativa que se comunica con tu backend de WebSocket directamente, en código nativo.

O podrías tener alguna otra forma de comunicarte con el endpoint de WebSocket.

---

Pero para este ejemplo, usaremos un documento HTML muy simple con algo de JavaScript, todo dentro de un string largo.

Esto, por supuesto, no es lo ideal y no lo usarías para producción.

En producción tendrías una de las opciones anteriores.

Pero es la forma más sencilla de enfocarse en el lado del servidor de WebSockets y tener un ejemplo funcional:

{* ../../docs_src/websockets/tutorial001.py hl[2,6:38,41:43] *}

## Crear un `websocket`

En tu aplicación de **FastAPI**, crea un `websocket`:

{* ../../docs_src/websockets/tutorial001.py hl[1,46:47] *}

/// note | Detalles Técnicos

También podrías usar `from starlette.websockets import WebSocket`.

**FastAPI** proporciona el mismo `WebSocket` directamente solo como una conveniencia para ti, el desarrollador. Pero viene directamente de Starlette.

///

## Esperar mensajes y enviar mensajes

En tu ruta de WebSocket puedes `await` para recibir mensajes y enviar mensajes.

{* ../../docs_src/websockets/tutorial001.py hl[48:52] *}

Puedes recibir y enviar datos binarios, de texto y JSON.

## Pruébalo

Si tu archivo se llama `main.py`, ejecuta tu aplicación con:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abre tu navegador en <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Verás una página simple como:

<img src="/img/tutorial/websockets/image01.png">

Puedes escribir mensajes en el cuadro de entrada y enviarlos:

<img src="/img/tutorial/websockets/image02.png">

Y tu aplicación **FastAPI** con WebSockets responderá de vuelta:

<img src="/img/tutorial/websockets/image03.png">

Puedes enviar (y recibir) muchos mensajes:

<img src="/img/tutorial/websockets/image04.png">

Y todos usarán la misma conexión WebSocket.

## Usando `Depends` y otros

En endpoints de WebSocket puedes importar desde `fastapi` y usar:

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Funcionan de la misma manera que para otros endpoints de FastAPI/*path operations*:

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | Información

Como esto es un WebSocket no tiene mucho sentido lanzar un `HTTPException`, en su lugar lanzamos un `WebSocketException`.

Puedes usar un código de cierre de los <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">códigos válidos definidos en la especificación</a>.

///

### Prueba los WebSockets con dependencias

Si tu archivo se llama `main.py`, ejecuta tu aplicación con:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abre tu navegador en <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Ahí puedes establecer:

* El "ID del Ítem", usado en el path.
* El "Token" usado como un parámetro query.

/// tip | Consejo

Nota que el query `token` será manejado por una dependencia.

///

Con eso puedes conectar el WebSocket y luego enviar y recibir mensajes:

<img src="/img/tutorial/websockets/image05.png">

## Manejar desconexiones y múltiples clientes

Cuando una conexión de WebSocket se cierra, el `await websocket.receive_text()` lanzará una excepción `WebSocketDisconnect`, que puedes capturar y manejar como en este ejemplo.

{* ../../docs_src/websockets/tutorial003_py39.py hl[79:81] *}

Para probarlo:

* Abre la aplicación con varias pestañas del navegador.
* Escribe mensajes desde ellas.
* Luego cierra una de las pestañas.

Eso lanzará la excepción `WebSocketDisconnect`, y todos los otros clientes recibirán un mensaje como:

```
Client #1596980209979 left the chat
```

/// tip | Consejo

La aplicación anterior es un ejemplo mínimo y simple para demostrar cómo manejar y transmitir mensajes a varias conexiones WebSocket.

Pero ten en cuenta que, como todo se maneja en memoria, en una sola lista, solo funcionará mientras el proceso esté en ejecución, y solo funcionará con un solo proceso.

Si necesitas algo fácil de integrar con FastAPI pero que sea más robusto, soportado por Redis, PostgreSQL u otros, revisa <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

///

## Más información

Para aprender más sobre las opciones, revisa la documentación de Starlette para:

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">La clase `WebSocket`</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">Manejo de WebSocket basado en clases</a>.
