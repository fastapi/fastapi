# Dependencias Avanzadas { #advanced-dependencies }

## Dependencias con parámetros { #parameterized-dependencies }

Todas las dependencias que hemos visto son una función o clase fija.

Pero podría haber casos en los que quieras poder establecer parámetros en la dependencia, sin tener que declarar muchas funciones o clases diferentes.

Imaginemos que queremos tener una dependencia que revise si el parámetro de query `q` contiene algún contenido fijo.

Pero queremos poder parametrizar ese contenido fijo.

## Una instance "callable" { #a-callable-instance }

En Python hay una forma de hacer que una instance de una clase sea un "callable".

No la clase en sí (que ya es un callable), sino una instance de esa clase.

Para hacer eso, declaramos un método `__call__`:

{* ../../docs_src/dependencies/tutorial011.py hl[12] *}

En este caso, este `__call__` es lo que **FastAPI** usará para revisar parámetros adicionales y sub-dependencias, y es lo que llamará para pasar un valor al parámetro en tu *path operation function* más adelante.

## Parametriza la instance { #parameterize-the-instance }

Y ahora, podemos usar `__init__` para declarar los parámetros de la instance que podemos usar para "parametrizar" la dependencia:

{* ../../docs_src/dependencies/tutorial011.py hl[9] *}

En este caso, **FastAPI** nunca tocará ni se preocupará por `__init__`, lo usaremos directamente en nuestro código.

## Crea una instance { #create-an-instance }

Podríamos crear una instance de esta clase con:

{* ../../docs_src/dependencies/tutorial011.py hl[18] *}

Y de esa manera podemos "parametrizar" nuestra dependencia, que ahora tiene `"bar"` dentro de ella, como el atributo `checker.fixed_content`.

## Usa la instance como una dependencia { #use-the-instance-as-a-dependency }

Luego, podríamos usar este `checker` en un `Depends(checker)`, en lugar de `Depends(FixedContentQueryChecker)`, porque la dependencia es la instance, `checker`, no la clase en sí.

Y al resolver la dependencia, **FastAPI** llamará a este `checker` así:

```Python
checker(q="somequery")
```

...y pasará lo que eso retorne como el valor de la dependencia en nuestra *path operation function* como el parámetro `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011.py hl[22] *}

/// tip | Consejo

Todo esto podría parecer complicado. Y puede que no esté muy claro cómo es útil aún.

Estos ejemplos son intencionalmente simples, pero muestran cómo funciona todo.

En los capítulos sobre seguridad, hay funciones utilitarias que se implementan de esta misma manera.

Si entendiste todo esto, ya sabes cómo funcionan por debajo esas herramientas de utilidad para seguridad.

///

## Limita la concurrencia de dependencias { #limit-dependency-concurrency }

En algunos casos, puede que quieras limitar cuántas requests pueden usar una dependencia al mismo tiempo.

Por ejemplo, tu base de datos podría tener un número limitado de conexiones disponibles. Podrías hacer que las nuevas requests esperen antes de crear una sesión, hasta que otra request termine de usar su sesión.

Puedes hacer esto con `max_concurrency` en `Depends()`.

Actualicemos el alias `SessionDep` del [tutorial de bases de datos SQL](../tutorial/sql-databases.md):

```Python
SessionDep = Annotated[Session, Depends(get_session, max_concurrency=5)]
```

Ahora, hasta **cinco requests** pueden tener una sesión de base de datos abierta a través de esta dependencia al mismo tiempo.

Si otra request necesita una sesión, espera hasta que se cierre una de esas sesiones.

Mientras espera, **no ocupa un hilo de worker**, por lo que esos hilos están disponibles para ejecutar otro código.

El valor debe ser un entero positivo. El valor por defecto es `None`, lo que significa que FastAPI no limita cuántas veces puede ejecutarse la dependencia al mismo tiempo.

### Comparte el límite entre rutas { #share-the-limit-between-routes }

Todas las rutas de ese ejemplo usan el mismo alias `SessionDep`, por lo que comparten el límite de cinco sesiones.

Para compartir un límite, reutiliza el **mismo objeto `Depends()`**, por ejemplo en un alias `Annotated` como este.

Si escribes un nuevo `Depends(get_session, max_concurrency=5)` para cada ruta, cada una tendrá su propio límite de cinco. Esto es así aunque todas usen la misma función `get_session`.

Reutilizar el mismo `SessionDep` en otra aplicación también comparte el límite, siempre que ambas aplicaciones se ejecuten en el mismo loop de eventos. Esto incluye las aplicaciones montadas.

Por ejemplo, si dos aplicaciones usan este `SessionDep` para el mismo pool de conexiones de base de datos, entre las dos pueden tener hasta cinco sesiones abiertas a través de esta dependencia.

Si las aplicaciones usan pools separados y necesitan límites independientes, crea un objeto `Depends()` separado para cada aplicación.

### Cierra la sesión antes de permitir otra { #close-the-session-before-allowing-another-one }

En este ejemplo, `get_session` usa `yield`. La sesión cuenta para el límite hasta que el código de salida termina de cerrarla.

El `scope` de la dependencia determina cuándo se ejecuta ese código de salida:

* Con `scope="request"`, el valor por defecto, se ejecuta después de que se envía la response.
* Con `scope="function"`, se ejecuta después de que termina la *path operation function*, antes de enviar la response.

Puedes leer más sobre [salida temprana y scope](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

Para una dependencia sin `yield`, la llamada cuenta para el límite solo hasta que termina la función.

Si usas una dependencia con `yield` en un manejador de WebSocket, cuenta para el límite hasta que el manejador termina y finaliza el código de salida de la dependencia.

/// note | Nota

Reutilizar un [valor de dependencia en caché](../tutorial/dependencies/sub-dependencies.md#using-the-same-dependency-multiple-times) no vuelve a contar para el límite. Si diferentes declaraciones comparten ese valor, solo la declaración que llama a la dependencia cuenta para su límite.

///

### Elige un límite para tu aplicación { #choose-a-limit-for-your-application }

Elige un límite que se ajuste al número de conexiones de base de datos disponibles para estas sesiones.

Si otras partes de tu aplicación también usan esas conexiones, deja espacio para ellas también. FastAPI no conoce el tamaño de tu pool de conexiones de base de datos.

Cada worker process tiene su propio límite. Por ejemplo, dos worker processes con esta dependencia podrían tener hasta diez sesiones abiertas entre los dos.

/// note | Detalles técnicos

Los límites también son independientes para cada loop de eventos. Las aplicaciones que se ejecutan en diferentes loops de eventos no comparten un límite, aunque reutilicen el mismo objeto `Depends()`.

///

### Dependencias que necesitan más de un recurso { #dependencies-that-need-more-than-one-resource }

FastAPI ejecuta las sub-dependencias de una dependencia antes de aplicar el límite de esa dependencia.

Por lo tanto, para limitar las sesiones de base de datos, pon `max_concurrency` en `Depends(get_session, ...)`, donde se crea la sesión.

Una request puede quedarse bloqueada si necesita otra sesión mientras aún mantiene una que solo se cerrará al final de la request.

Por ejemplo, imagina un `Depends(get_session, max_concurrency=1, use_cache=False)` compartido que se usa dos veces en la misma request.

La primera llamada crea una sesión. La segunda llamada espera a que se cierre. Pero la primera sesión no puede cerrarse hasta que termine la request, y la request está esperando a la segunda llamada.

Dos requests también pueden quedarse bloqueadas si una mantiene una sesión mientras espera otro recurso, y la otra mantiene ese recurso mientras espera una sesión.

Si tus requests necesitan varios recursos, adquiérelos en el mismo orden. FastAPI aplica cada límite por separado, no reserva de antemano todos los recursos que necesitará una request.

## Dependencias con `yield`, `HTTPException`, `except` y Tareas en segundo plano { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | Advertencia

Muy probablemente no necesites estos detalles técnicos.

Estos detalles son útiles principalmente si tenías una aplicación de FastAPI anterior a la 0.121.0 y estás enfrentando problemas con dependencias con `yield`.

///

Las dependencias con `yield` han evolucionado con el tiempo para cubrir diferentes casos de uso y arreglar algunos problemas; aquí tienes un resumen de lo que ha cambiado.

### Dependencias con `yield` y `scope` { #dependencies-with-yield-and-scope }

En la versión 0.121.0, FastAPI agregó soporte para `Depends(scope="function")` para dependencias con `yield`.

Usando `Depends(scope="function")`, el código de salida después de `yield` se ejecuta justo después de que la *path operation function* termina, antes de que la response se envíe de vuelta al cliente.

Y al usar `Depends(scope="request")` (el valor por defecto), el código de salida después de `yield` se ejecuta después de que la response es enviada.

Puedes leer más al respecto en la documentación de [Dependencias con `yield` - Salida temprana y `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

### Dependencias con `yield` y `StreamingResponse`, detalles técnicos { #dependencies-with-yield-and-streamingresponse-technical-details }

Antes de FastAPI 0.118.0, si usabas una dependencia con `yield`, ejecutaba el código de salida después de que la *path operation function* retornaba pero justo antes de enviar la response.

La intención era evitar retener recursos por más tiempo del necesario, esperando a que la response viajara por la red.

Este cambio también significaba que si retornabas un `StreamingResponse`, el código de salida de la dependencia con `yield` ya se habría ejecutado.

Por ejemplo, si tenías una sesión de base de datos en una dependencia con `yield`, el `StreamingResponse` no podría usar esa sesión mientras hace streaming de datos porque la sesión ya se habría cerrado en el código de salida después de `yield`.

Este comportamiento se revirtió en la 0.118.0, para hacer que el código de salida después de `yield` se ejecute después de que la response sea enviada.

/// note | Nota

Como verás abajo, esto es muy similar al comportamiento anterior a la versión 0.106.0, pero con varias mejoras y arreglos de bugs para casos límite.

///

#### Casos de uso con salida temprana del código { #use-cases-with-early-exit-code }

Hay algunos casos de uso con condiciones específicas que podrían beneficiarse del comportamiento antiguo de ejecutar el código de salida de dependencias con `yield` antes de enviar la response.

Por ejemplo, imagina que tienes código que usa una sesión de base de datos en una dependencia con `yield` solo para verificar un usuario, pero la sesión de base de datos no se vuelve a usar en la *path operation function*, solo en la dependencia, **y** la response tarda mucho en enviarse, como un `StreamingResponse` que envía datos lentamente, pero que por alguna razón no usa la base de datos.

En este caso, la sesión de base de datos se mantendría hasta que la response termine de enviarse, pero si no la usas, entonces no sería necesario mantenerla.

Así es como se vería:

{* ../../docs_src/dependencies/tutorial013.py *}

El código de salida, el cierre automático de la `Session` en:

{* ../../docs_src/dependencies/tutorial013.py ln[19:21] *}

...se ejecutaría después de que la response termine de enviar los datos lentos:

{* ../../docs_src/dependencies/tutorial013.py ln[30:38] hl[31:33] *}

Pero como `generate_stream()` no usa la sesión de base de datos, no es realmente necesario mantener la sesión abierta mientras se envía la response.

Si tienes este caso de uso específico usando SQLModel (o SQLAlchemy), podrías cerrar explícitamente la sesión después de que ya no la necesites:

{* ../../docs_src/dependencies/tutorial014.py ln[24:28] hl[28] *}

De esa manera la sesión liberaría la conexión a la base de datos, para que otras requests puedan usarla.

Si tienes un caso de uso diferente que necesite salir temprano desde una dependencia con `yield`, por favor crea una [Pregunta de Discusión en GitHub](https://github.com/fastapi/fastapi/discussions/new?category=questions) con tu caso de uso específico y por qué te beneficiaría tener cierre temprano para dependencias con `yield`.

Si hay casos de uso convincentes para el cierre temprano en dependencias con `yield`, consideraría agregar una nueva forma de optar por el cierre temprano.

### Dependencias con `yield` y `except`, detalles técnicos { #dependencies-with-yield-and-except-technical-details }

Antes de FastAPI 0.110.0, si usabas una dependencia con `yield`, y luego capturabas una excepción con `except` en esa dependencia, y no volvías a elevar la excepción, la excepción se elevaría/remitiría automáticamente a cualquier manejador de excepciones o al manejador de error interno del servidor.

Esto cambió en la versión 0.110.0 para arreglar consumo de memoria no manejado por excepciones reenviadas sin un manejador (errores internos del servidor), y para hacerlo consistente con el comportamiento del código Python normal.

### Tareas en segundo plano y dependencias con `yield`, detalles técnicos { #background-tasks-and-dependencies-with-yield-technical-details }

Antes de FastAPI 0.106.0, elevar excepciones después de `yield` no era posible, el código de salida en dependencias con `yield` se ejecutaba *después* de que la response era enviada, por lo que [Manejadores de Excepciones](../tutorial/handling-errors.md#install-custom-exception-handlers) ya habrían corrido.

Esto se diseñó así principalmente para permitir usar los mismos objetos devueltos con `yield` por las dependencias dentro de tareas en segundo plano, porque el código de salida se ejecutaría después de que las tareas en segundo plano terminaran.

Esto cambió en FastAPI 0.106.0 con la intención de no retener recursos mientras se espera a que la response viaje por la red.

/// tip | Consejo

Adicionalmente, una tarea en segundo plano normalmente es un conjunto independiente de lógica que debería manejarse por separado, con sus propios recursos (por ejemplo, su propia conexión a la base de datos).

Así, probablemente tendrás un código más limpio.

///

Si solías depender de este comportamiento, ahora deberías crear los recursos para las tareas en segundo plano dentro de la propia tarea en segundo plano, y usar internamente solo datos que no dependan de los recursos de dependencias con `yield`.

Por ejemplo, en lugar de usar la misma sesión de base de datos, crearías una nueva sesión de base de datos dentro de la tarea en segundo plano, y obtendrías los objetos de la base de datos usando esta nueva sesión. Y entonces, en lugar de pasar el objeto de la base de datos como parámetro a la función de la tarea en segundo plano, pasarías el ID de ese objeto y luego obtendrías el objeto de nuevo dentro de la función de la tarea en segundo plano.
