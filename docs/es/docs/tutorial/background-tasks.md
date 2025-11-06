# Tareas en Segundo Plano

Puedes definir tareas en segundo plano para que se ejecuten *después* de devolver un response.

Esto es útil para operaciones que necesitan ocurrir después de un request, pero para las que el cliente realmente no necesita esperar a que la operación termine antes de recibir el response.

Esto incluye, por ejemplo:

* Notificaciones por email enviadas después de realizar una acción:
  * Como conectarse a un servidor de email y enviar un email tiende a ser "lento" (varios segundos), puedes devolver el response de inmediato y enviar la notificación por email en segundo plano.
* Procesamiento de datos:
  * Por ejemplo, supongamos que recibes un archivo que debe pasar por un proceso lento, puedes devolver un response de "Accepted" (HTTP 202) y procesar el archivo en segundo plano.

## Usando `BackgroundTasks`

Primero, importa `BackgroundTasks` y define un parámetro en tu *path operation function* con una declaración de tipo de `BackgroundTasks`:

{* ../../docs_src/background_tasks/tutorial001.py hl[1,13] *}

**FastAPI** creará el objeto de tipo `BackgroundTasks` por ti y lo pasará como ese parámetro.

## Crear una función de tarea

Crea una función para que se ejecute como la tarea en segundo plano.

Es solo una función estándar que puede recibir parámetros.

Puede ser una función `async def` o una función normal `def`, **FastAPI** sabrá cómo manejarla correctamente.

En este caso, la función de tarea escribirá en un archivo (simulando el envío de un email).

Y como la operación de escritura no usa `async` y `await`, definimos la función con un `def` normal:

{* ../../docs_src/background_tasks/tutorial001.py hl[6:9] *}

## Agregar la tarea en segundo plano

Dentro de tu *path operation function*, pasa tu función de tarea al objeto de *background tasks* con el método `.add_task()`:

{* ../../docs_src/background_tasks/tutorial001.py hl[14] *}

`.add_task()` recibe como argumentos:

* Una función de tarea para ejecutar en segundo plano (`write_notification`).
* Cualquier secuencia de argumentos que deba pasarse a la función de tarea en orden (`email`).
* Cualquier argumento de palabras clave que deba pasarse a la función de tarea (`message="some notification"`).

## Inyección de Dependencias

Usar `BackgroundTasks` también funciona con el sistema de inyección de dependencias, puedes declarar un parámetro de tipo `BackgroundTasks` en varios niveles: en una *path operation function*, en una dependencia (dependable), en una sub-dependencia, etc.

**FastAPI** sabe qué hacer en cada caso y cómo reutilizar el mismo objeto, de modo que todas las tareas en segundo plano se combinan y ejecutan en segundo plano después:

{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}

En este ejemplo, los mensajes se escribirán en el archivo `log.txt` *después* de que se envíe el response.

Si hay un query en el request, se escribirá en el log en una tarea en segundo plano.

Y luego otra tarea en segundo plano generada en la *path operation function* escribirá un mensaje usando el parámetro de path `email`.

## Detalles Técnicos

La clase `BackgroundTasks` proviene directamente de <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>.

Se importa/incluye directamente en FastAPI para que puedas importarla desde `fastapi` y evitar importar accidentalmente la alternativa `BackgroundTask` (sin la `s` al final) de `starlette.background`.

Al usar solo `BackgroundTasks` (y no `BackgroundTask`), es posible usarla como un parámetro de *path operation function* y dejar que **FastAPI** maneje el resto por ti, tal como cuando usas el objeto `Request` directamente.

Todavía es posible usar `BackgroundTask` solo en FastAPI, pero debes crear el objeto en tu código y devolver una `Response` de Starlette incluyéndolo.

Puedes ver más detalles en <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">la documentación oficial de Starlette sobre Background Tasks</a>.

## Advertencia

Si necesitas realizar una computación intensa en segundo plano y no necesariamente necesitas que se ejecute por el mismo proceso (por ejemplo, no necesitas compartir memoria, variables, etc.), podrías beneficiarte del uso de otras herramientas más grandes como <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>.

Tienden a requerir configuraciones más complejas, un gestor de cola de mensajes/trabajos, como RabbitMQ o Redis, pero te permiten ejecutar tareas en segundo plano en múltiples procesos, y especialmente, en múltiples servidores.

Pero si necesitas acceder a variables y objetos de la misma app de **FastAPI**, o necesitas realizar pequeñas tareas en segundo plano (como enviar una notificación por email), simplemente puedes usar `BackgroundTasks`.

## Resumen

Importa y usa `BackgroundTasks` con parámetros en *path operation functions* y dependencias para agregar tareas en segundo plano.
