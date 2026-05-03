# Transmitir datos { #stream-data }

Si quieres transmitir datos que se puedan estructurar como JSON, deberías [Transmitir JSON Lines](../tutorial/stream-json-lines.md).

Pero si quieres transmitir datos binarios puros o strings, aquí tienes cómo hacerlo.

/// info | Información

Añadido en FastAPI 0.134.0.

///

## Casos de uso { #use-cases }

Podrías usar esto si quieres transmitir strings puros, por ejemplo directamente de la salida de un servicio de AI LLM.

También podrías usarlo para transmitir archivos binarios grandes, donde transmites cada bloque de datos a medida que lo lees, sin tener que leerlo todo en memoria de una sola vez.

También podrías transmitir video o audio de esta manera; incluso podría generarse mientras lo procesas y lo envías.

## Un `StreamingResponse` con `yield` { #a-streamingresponse-with-yield }

Si declaras un `response_class=StreamingResponse` en tu *path operation function*, puedes usar `yield` para enviar cada bloque de datos a su vez.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI entregará cada bloque de datos a `StreamingResponse` tal cual, no intentará convertirlo a JSON ni nada parecido.

### *path operation functions* no async { #non-async-path-operation-functions }

También puedes usar funciones `def` normales (sin `async`) y usar `yield` de la misma manera.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### Sin anotación { #no-annotation }

Realmente no necesitas declarar la anotación de tipo de retorno para transmitir datos binarios.

Como FastAPI no intentará convertir los datos a JSON con Pydantic ni serializarlos de ninguna manera, en este caso la anotación de tipos es solo para que la use tu editor y tus herramientas; FastAPI no la usará.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

Esto también significa que con `StreamingResponse` tienes la libertad y la responsabilidad de producir y codificar los bytes de datos exactamente como necesites enviarlos, independientemente de las anotaciones de tipos. 🤓

### Transmitir bytes { #stream-bytes }

Uno de los casos de uso principales sería transmitir `bytes` en lugar de strings; por supuesto puedes hacerlo.

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## Un `PNGStreamingResponse` personalizado { #a-custom-pngstreamingresponse }

En los ejemplos anteriores, se transmitieron los bytes de datos, pero la response no tenía un header `Content-Type`, así que el cliente no sabía qué tipo de datos estaba recibiendo.

Puedes crear una subclase personalizada de `StreamingResponse` que establezca el header `Content-Type` al tipo de datos que estás transmitiendo.

Por ejemplo, puedes crear un `PNGStreamingResponse` que establezca el header `Content-Type` a `image/png` usando el atributo `media_type`:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

Luego puedes usar esta nueva clase en `response_class=PNGStreamingResponse` en tu *path operation function*:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### Simular un archivo { #simulate-a-file }

En este ejemplo estamos simulando un archivo con `io.BytesIO`, que es un objeto tipo archivo que vive solo en memoria, pero nos permite usar la misma interfaz.

Por ejemplo, podemos iterarlo para consumir su contenido, como podríamos con un archivo.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | Detalles técnicos

Las otras dos variables, `image_base64` y `binary_image`, son una imagen codificada en Base64 y luego convertida a bytes, para después pasarla a `io.BytesIO`.

Solo para que pueda vivir en el mismo archivo para este ejemplo y puedas copiarlo y ejecutarlo tal cual. 🥚

///

Al usar un bloque `with`, nos aseguramos de que el objeto tipo archivo se cierre cuando termine la función generadora (la función con `yield`). Es decir, después de que termine de enviar la response.

No sería tan importante en este ejemplo específico porque es un archivo falso en memoria (con `io.BytesIO`), pero con un archivo real sí sería importante asegurarse de que el archivo se cierre al terminar de trabajar con él.

### Archivos y async { #files-and-async }

En la mayoría de los casos, los objetos tipo archivo no son compatibles con `async` y `await` por defecto.

Por ejemplo, no tienen un `await file.read()`, ni un `async for chunk in file`.

Y en muchos casos leerlos sería una operación bloqueante (que podría bloquear el event loop), porque se leen desde disco o desde la red.

/// info | Información

El ejemplo anterior es en realidad una excepción, porque el objeto `io.BytesIO` ya está en memoria, así que leerlo no bloqueará nada.

Pero en muchos casos leer un archivo u objeto tipo archivo sí bloquearía.

///

Para evitar bloquear el event loop, puedes simplemente declarar la *path operation function* con un `def` normal en lugar de `async def`; de esa forma FastAPI la ejecutará en un worker de threadpool para evitar bloquear el loop principal.

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | Consejo

Si necesitas llamar código bloqueante desde dentro de una función async, o una función async desde dentro de una función bloqueante, podrías usar [Asyncer](https://asyncer.tiangolo.com), un paquete hermano de FastAPI.

///

### `yield from` { #yield-from }

Cuando estés iterando sobre algo, como un objeto tipo archivo, y estés haciendo `yield` para cada elemento, también podrías usar `yield from` para hacer `yield` de cada elemento directamente y saltarte el `for`.

Esto no es particular de FastAPI, es simplemente Python, pero es un truco útil que conviene conocer. 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
