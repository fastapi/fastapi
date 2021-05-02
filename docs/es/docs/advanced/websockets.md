# WebSockets

Puedes utilizar <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank"> <abbr>WebSockets</abbr> </a> con **FastAPI**.

## Cliente de WebSockets 

### En producción

En tu sistema de producción, posiblemente tienes un <abbr>frontend</abbr> creado con algún <abbr>framework</abbr> moderno como lo puede ser React , Vue.js o Angular.

Y si utilizas <abbr>WebSockets</abbr> para comunicarte con tu <abbr>backend</abbr> muy probablemente utilices las funcionalidades de tú aplicación <abbr>frontend</abbr>. 

O posiblemente cuentes con una aplicación móvil nativa que se comunique con el <abbr>WebSocket</abbr> de tu <abbr>backend</abbr> directamente , utilizando código nativo. 

O tal vez tengas otra forma de comunicarte con el <abbr>endpoint</abbr> del <abbr>WebSocket</abbr>.

---

Pero para este ejemplo , utilizaremos un documento muy simple de HTML con un poco de Javascript , todo dentro de un largo string. 

Esto , por supuesto , no es óptimo y tampoco deberías utilizarlo para producción. 

En producción tendrás una de las opciones anteriormente comentadas. 

Pero es la forma más simple de enfocarnos en el lado del servidor de los <abbr>WebSockets</abbr> y tener un ejemplo práctico: 

```Python hl_lines="2  6-38  41-43"
{!../../../docs_src/websockets/tutorial001.py!}
```

## Creando un `websocket`

En tu aplicación de **FastAPI** , crea un <abbr>`websocket`</abbr> :

```Python hl_lines="1  46-47"
{!../../../docs_src/websockets/tutorial001.py!}
```

!!! note "Detalles Técnicos"
    También puedes utilizar `from starlette.websockets import WebSocket`.

    **FastAPI** proporciona el mismo <abbr>`WebSocket`</abbr> directamente por comodidad para ti, el desarrollador. Pero viene directamente de Starlette. 

## Esperar por mensajes y enviar mensajes 

En la ruta de tu <abbr>WebSocket</abbr> puedes <abbr title="await">`esperar`</abbr> por mensajes y enviar mensajes.

```Python hl_lines="48-52"
{!../../../docs_src/websockets/tutorial001.py!}
```

Puedes enviar y recibir archivos binarios , textos e información en formato JSON.

## Pruébalo

Si el nombre de tu archivo es `main.py`, ejecuta tu aplicación utilizando:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abre tu navegador en <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.
 
Verás una pagina simple parecida a esta: 

<img src="https://fastapi.tiangolo.com/img/tutorial/websockets/image01.png">

Puedes escribir mensajes en el cuadro de texto, y luego enviarlos: 

<img src="https://fastapi.tiangolo.com/img/tutorial/websockets/image02.png">

Y tú aplicación de **FastAPI** con <abbr>WebSockets</abbr> te responderá:

<img src="https://fastapi.tiangolo.com/img/tutorial/websockets/image03.png">

Puedes enviar ( y recibir ) muchos mensajes: 

<img src="https://fastapi.tiangolo.com/img/tutorial/websockets/image04.png">

Y todos ellos utilizaran la misma conexión de <abbr>WebSocket</abbr>.

## Usando `Depends` y otros

En los <abbr>endpoints</abbr> del <abbr>WebSocket</abbr> puedes importar desde `fastapi` y utilizar: 

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

Funcionan de las misma forma que otros <abbr>endpoints</abbr>/*operaciones de <abbr title="ruta">path</abbr>* en FastAPI:

```Python hl_lines="58-65  68-83"
{!../../../docs_src/websockets/tutorial002.py!}
```

!!! info
    Debido a que en un <abbr>WebSocket</abbr> no es necesario lanzar un <abbr>`HTTPException`</abbr>, lo mejor sería cerrar directamente la conexión al <abbr>WebSocket</abbr>.

    Puedes utilizar un código de cierre basado en <a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">códigos válidos definidos en las especificaciones</a>.

    En el futuro , existirá un <abbr>`WebSocketException`</abbr> que te permitirá ejecutarlo desde cualquier parte , y añadir <abbr>exception handlers</abbr> para ello. Todo depende de la <a href="https://github.com/encode/starlette/pull/527" class="external-link" target="_blank">PR #527</a> en Starlette.

### Prueba WebSockets con dependencias

Si el nombre de tu archivo es `main.py`, ejecuta tu aplicación con:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Abre tú navegador en <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Allí puedes definir:

* el "Item ID", usado en el <abbr>path</abbr>.
* El "Token" es usado como un parámetro de <abbr>query</abbr>.

!!! tip
    Observa que el `token` de <abbr>query</abbr> será manejado por una dependencia.

Con todo esto podemos conectar el <abbr>WebSocket</abbr> y empezar a enviar y recibir mensajes:

<img src="https://fastapi.tiangolo.com/img/tutorial/websockets/image05.png">

## Manejando desconexiones y múltiples clientes 

Cuando una conexión de <abbr>WebSocket</abbr> está cerrada, el `await websocket.receive_text()` ejecutará una excepción de tipo <abbr>`WebSocketDisconnect`</abbr>, el cual puedes tomar y manejar como en este ejemplo.

```Python hl_lines="81-83"
{!../../../docs_src/websockets/tutorial003.py!}
```

Para intentarlo:

* Abre la aplicación en varias pestañas del navegador.
* Escribe un mensaje para ellas.
* Ahora , cierra una de las pestañas.

Esto ejecutará la excepción de tipo <abbr>`WebSocketDisconnect`</abbr>, y todos los demás clientes recibirán un mensaje como:

```
Client #1596980209979 left the chat
```

!!! tip
    La aplicación anteriormente descrita , es un ejemplo simple y sencillo para demostrar cómo manejar y emitir mensajes a varias conexiones de <abbr>WebSocket</abbr>     
    
    Pero debes tener en cuenta , como todo es manejado en memoria , en una única lista , solo funcionará mientras el proceso se está ejecutando , y solo servirá con un único proceso.    
    
    Si necesitas algo fácil para integrar con FastAPI pero que sea más robusto, que soporte Redis, PostgreSQL o algún otro, puedes mirar <a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a>.

## Más información

Para aprender más acerca de estas opciones , revisa la documentación de Starlette para:

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank">La clase <abbr>`WebSocket`</abbr><a>.
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">Manejo basado en clases para <abbr>WebSockets</abbr></a>.
