# Dependencias Avanzadas { #advanced-dependencies }

## Dependencias con parámetros { #parameterized-dependencies }

Todas las dependencias que hemos visto son una función o clase fija.

Pero podría haber casos en los que quieras poder establecer parámetros en la dependencia, sin tener que declarar muchas funciones o clases diferentes.

Imaginemos que queremos tener una dependencia que revise si el parámetro de query `q` contiene algún contenido fijo.

Pero queremos poder parametrizar ese contenido fijo.

## Una *instance* "callable" { #a-callable-instance }

En Python hay una forma de hacer que una instance de una clase sea un "callable".

No la clase en sí (que ya es un callable), sino una instance de esa clase.

Para hacer eso, declaramos un método `__call__`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

En este caso, este `__call__` es lo que **FastAPI** usará para comprobar parámetros adicionales y sub-dependencias, y es lo que llamará para pasar un valor al parámetro en tu *path operation function* más adelante.

## Parametrizar la instance { #parameterize-the-instance }

Y ahora, podemos usar `__init__` para declarar los parámetros de la instance que podemos usar para "parametrizar" la dependencia:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

En este caso, **FastAPI** nunca tocará ni se preocupará por `__init__`, lo usaremos directamente en nuestro código.

## Crear una instance { #create-an-instance }

Podríamos crear una instance de esta clase con:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

Y de esa manera podemos "parametrizar" nuestra dependencia, que ahora tiene `"bar"` dentro de ella, como el atributo `checker.fixed_content`.

## Usar la instance como una dependencia { #use-the-instance-as-a-dependency }

Luego, podríamos usar este `checker` en un `Depends(checker)`, en lugar de `Depends(FixedContentQueryChecker)`, porque la dependencia es la instance, `checker`, no la clase en sí.

Y al resolver la dependencia, **FastAPI** llamará a este `checker` así:

```Python
checker(q="somequery")
```

...y pasará lo que eso retorne como el valor de la dependencia en nuestra *path operation function* como el parámetro `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip | Consejo

Todo esto podría parecer complicado. Y puede que no esté muy claro cómo es útil aún.

Estos ejemplos son intencionalmente simples, pero muestran cómo funciona todo.

En los capítulos sobre seguridad, hay funciones utilitarias que se implementan de esta misma manera.

Si entendiste todo esto, ya sabes cómo funcionan por debajo esas herramientas de utilidad para seguridad.

///

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

/// info | Información

Como verás abajo, esto es muy similar al comportamiento anterior a la versión 0.106.0, pero con varias mejoras y arreglos de bugs para casos límite.

///

#### Casos de uso con salida temprana del código { #use-cases-with-early-exit-code }

Hay algunos casos de uso con condiciones específicas que podrían beneficiarse del comportamiento antiguo de ejecutar el código de salida de dependencias con `yield` antes de enviar la response.

Por ejemplo, imagina que tienes código que usa una sesión de base de datos en una dependencia con `yield` solo para verificar un usuario, pero la sesión de base de datos no se vuelve a usar en la *path operation function*, solo en la dependencia, y la response tarda mucho en enviarse, como un `StreamingResponse` que envía datos lentamente, pero que por alguna razón no usa la base de datos.

En este caso, la sesión de base de datos se mantendría hasta que la response termine de enviarse, pero si no la usas, entonces no sería necesario mantenerla.

Así es como se vería:

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

El código de salida, el cierre automático de la `Session` en:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...se ejecutaría después de que la response termine de enviar los datos lentos:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

Pero como `generate_stream()` no usa la sesión de base de datos, no es realmente necesario mantener la sesión abierta mientras se envía la response.

Si tienes este caso de uso específico usando SQLModel (o SQLAlchemy), podrías cerrar explícitamente la sesión después de que ya no la necesites:

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

De esa manera la sesión liberaría la conexión a la base de datos, para que otras requests puedan usarla.

Si tienes un caso de uso diferente que necesite salir temprano desde una dependencia con `yield`, por favor crea una <a href="https://github.com/fastapi/fastapi/discussions/new?category=questions" class="external-link" target="_blank">Pregunta de Discusión en GitHub</a> con tu caso de uso específico y por qué te beneficiaría tener cierre temprano para dependencias con `yield`.

Si hay casos de uso convincentes para el cierre temprano en dependencias con `yield`, consideraría agregar una nueva forma de optar por el cierre temprano.

### Dependencias con `yield` y `except`, detalles técnicos { #dependencies-with-yield-and-except-technical-details }

Antes de FastAPI 0.110.0, si usabas una dependencia con `yield`, y luego capturabas una excepción con `except` en esa dependencia, y no volvías a elevar la excepción, la excepción se elevaría/remitiría automáticamente a cualquier manejador de excepciones o al manejador de error interno del servidor.

Esto cambió en la versión 0.110.0 para arreglar consumo de memoria no manejado por excepciones reenviadas sin un manejador (errores internos del servidor), y para hacerlo consistente con el comportamiento del código Python normal.

### Tareas en segundo plano y dependencias con `yield`, detalles técnicos { #background-tasks-and-dependencies-with-yield-technical-details }

Antes de FastAPI 0.106.0, elevar excepciones después de `yield` no era posible, el código de salida en dependencias con `yield` se ejecutaba después de que la response era enviada, por lo que [Manejadores de Excepciones](../tutorial/handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank} ya habrían corrido.

Esto se diseñó así principalmente para permitir usar los mismos objetos devueltos con `yield` por las dependencias dentro de tareas en segundo plano, porque el código de salida se ejecutaría después de que las tareas en segundo plano terminaran.

Esto cambió en FastAPI 0.106.0 con la intención de no retener recursos mientras se espera a que la response viaje por la red.

/// tip | Consejo

Adicionalmente, una tarea en segundo plano normalmente es un conjunto independiente de lógica que debería manejarse por separado, con sus propios recursos (por ejemplo, su propia conexión a la base de datos).

Así, probablemente tendrás un código más limpio.

///

Si solías depender de este comportamiento, ahora deberías crear los recursos para las tareas en segundo plano dentro de la propia tarea en segundo plano, y usar internamente solo datos que no dependan de los recursos de dependencias con `yield`.

Por ejemplo, en lugar de usar la misma sesión de base de datos, crearías una nueva sesión de base de datos dentro de la tarea en segundo plano, y obtendrías los objetos de la base de datos usando esta nueva sesión. Y entonces, en lugar de pasar el objeto de la base de datos como parámetro a la función de la tarea en segundo plano, pasarías el ID de ese objeto y luego obtendrías el objeto de nuevo dentro de la función de la tarea en segundo plano.
