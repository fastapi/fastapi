# Eventos de Lifespan { #lifespan-events }

Puedes definir lógica (código) que debería ser ejecutada antes de que la aplicación **inicie**. Esto significa que este código será ejecutado **una vez**, **antes** de que la aplicación **comience a recibir requests**.

De la misma manera, puedes definir lógica (código) que debería ser ejecutada cuando la aplicación esté **cerrándose**. En este caso, este código será ejecutado **una vez**, **después** de haber manejado posiblemente **muchos requests**.

Debido a que este código se ejecuta antes de que la aplicación **comience** a tomar requests, y justo después de que **termine** de manejarlos, cubre todo el **lifespan** de la aplicación (la palabra "lifespan" será importante en un momento 😉).

Esto puede ser muy útil para configurar **recursos** que necesitas usar para toda la app, y que son **compartidos** entre requests, y/o que necesitas **limpiar** después. Por ejemplo, un pool de conexiones a una base de datos, o cargando un modelo de machine learning compartido.

## Caso de Uso { #use-case }

Empecemos con un ejemplo de **caso de uso** y luego veamos cómo resolverlo con esto.

Imaginemos que tienes algunos **modelos de machine learning** que quieres usar para manejar requests. 🤖

Los mismos modelos son compartidos entre requests, por lo que no es un modelo por request, o uno por usuario o algo similar.

Imaginemos que cargar el modelo puede **tomar bastante tiempo**, porque tiene que leer muchos **datos del disco**. Entonces no quieres hacerlo para cada request.

Podrías cargarlo en el nivel superior del módulo/archivo, pero eso también significaría que **cargaría el modelo** incluso si solo estás ejecutando una simple prueba automatizada, entonces esa prueba sería **lenta** porque tendría que esperar a que el modelo se cargue antes de poder ejecutar una parte independiente del código.

Eso es lo que resolveremos, vamos a cargar el modelo antes de que los requests sean manejados, pero solo justo antes de que la aplicación comience a recibir requests, no mientras el código se está cargando.

## Lifespan { #lifespan }

Puedes definir esta lógica de *startup* y *shutdown* usando el parámetro `lifespan` de la app de `FastAPI`, y un "context manager" (te mostraré lo que es en un momento).

Comencemos con un ejemplo y luego veámoslo en detalle.

Creamos una función asíncrona `lifespan()` con `yield` así:

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

Aquí estamos simulando la operación costosa de *startup* de cargar el modelo poniendo la función del (falso) modelo en el diccionario con modelos de machine learning antes del `yield`. Este código será ejecutado **antes** de que la aplicación **comience a tomar requests**, durante el *startup*.

Y luego, justo después del `yield`, quitaremos el modelo de memoria. Este código será ejecutado **después** de que la aplicación **termine de manejar requests**, justo antes del *shutdown*. Esto podría, por ejemplo, liberar recursos como la memoria o una GPU.

/// tip | Consejo

El `shutdown` ocurriría cuando estás **deteniendo** la aplicación.

Quizás necesites iniciar una nueva versión, o simplemente te cansaste de ejecutarla. 🤷

///

### Función de Lifespan { #lifespan-function }

Lo primero que hay que notar es que estamos definiendo una función asíncrona con `yield`. Esto es muy similar a las Dependencias con `yield`.

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

La primera parte de la función, antes del `yield`, será ejecutada **antes** de que la aplicación comience.

Y la parte después del `yield` será ejecutada **después** de que la aplicación haya terminado.

### Async Context Manager { #async-context-manager }

Si revisas, la función está decorada con un `@asynccontextmanager`.

Eso convierte a la función en algo llamado un "**async context manager**".

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

Un **context manager** en Python es algo que puedes usar en un statement `with`, por ejemplo, `open()` puede ser usado como un context manager:

```Python
with open("file.txt") as file:
    file.read()
```

En versiones recientes de Python, también hay un **async context manager**. Lo usarías con `async with`:

```Python
async with lifespan(app):
    await do_stuff()
```

Cuando creas un context manager o un async context manager como arriba, lo que hace es que, antes de entrar al bloque `with`, ejecutará el código antes del `yield`, y al salir del bloque `with`, ejecutará el código después del `yield`.

En nuestro ejemplo de código arriba, no lo usamos directamente, pero se lo pasamos a FastAPI para que lo use.

El parámetro `lifespan` de la app de `FastAPI` toma un **async context manager**, por lo que podemos pasar nuestro nuevo `lifespan` async context manager a él.

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## Eventos Alternativos (obsoleto) { #alternative-events-deprecated }

/// warning | Advertencia

La forma recomendada de manejar el *startup* y el *shutdown* es usando el parámetro `lifespan` de la app de `FastAPI` como se describió arriba. Si proporcionas un parámetro `lifespan`, los manejadores de eventos `startup` y `shutdown` ya no serán llamados. Es solo `lifespan` o solo los eventos, no ambos.

Probablemente puedas saltarte esta parte.

///

Hay una forma alternativa de definir esta lógica para ser ejecutada durante el *startup* y durante el *shutdown*.

Puedes definir manejadores de eventos (funciones) que necesitan ser ejecutadas antes de que la aplicación se inicie, o cuando la aplicación se está cerrando.

Estas funciones pueden ser declaradas con `async def` o `def` normal.

### Evento `startup` { #startup-event }

Para añadir una función que debería ejecutarse antes de que la aplicación inicie, declárala con el evento `"startup"`:

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

En este caso, la función manejadora del evento `startup` inicializará los ítems de la "base de datos" (solo un `dict`) con algunos valores.

Puedes añadir más de un manejador de eventos.

Y tu aplicación no comenzará a recibir requests hasta que todos los manejadores de eventos `startup` hayan completado.

### Evento `shutdown` { #shutdown-event }

Para añadir una función que debería ejecutarse cuando la aplicación se esté cerrando, declárala con el evento `"shutdown"`:

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

Aquí, la función manejadora del evento `shutdown` escribirá una línea de texto `"Application shutdown"` a un archivo `log.txt`.

/// info | Información

En la función `open()`, el `mode="a"` significa "añadir", por lo tanto, la línea será añadida después de lo que sea que esté en ese archivo, sin sobrescribir el contenido anterior.

///

/// tip | Consejo

Nota que en este caso estamos usando una función estándar de Python `open()` que interactúa con un archivo.

Entonces, involucra I/O (entrada/salida), que requiere "esperar" para que las cosas se escriban en el disco.

Pero `open()` no usa `async` y `await`.

Por eso, declaramos la función manejadora del evento con `def` estándar en vez de `async def`.

///

### `startup` y `shutdown` juntos { #startup-and-shutdown-together }

Hay una gran posibilidad de que la lógica para tu *startup* y *shutdown* esté conectada, podrías querer iniciar algo y luego finalizarlo, adquirir un recurso y luego liberarlo, etc.

Hacer eso en funciones separadas que no comparten lógica o variables juntas es más difícil ya que necesitarías almacenar valores en variables globales o trucos similares.

Debido a eso, ahora se recomienda en su lugar usar el `lifespan` como se explicó arriba.

## Detalles Técnicos { #technical-details }

Solo un detalle técnico para los nerds curiosos. 🤓

Por debajo, en la especificación técnica ASGI, esto es parte del [Protocolo de Lifespan](https://asgi.readthedocs.io/en/latest/specs/lifespan.html), y define eventos llamados `startup` y `shutdown`.

/// info | Información

Puedes leer más sobre los manejadores `lifespan` de Starlette en [la documentación de `Lifespan` de Starlette](https://www.starlette.dev/lifespan/).

Incluyendo cómo manejar el estado de lifespan que puede ser usado en otras áreas de tu código.

///

## Sub Aplicaciones { #sub-applications }

🚨 Ten en cuenta que estos eventos de lifespan (startup y shutdown) solo serán ejecutados para la aplicación principal, no para [Sub Aplicaciones - Mounts](sub-applications.md).
