# Concurrencia y async / await { #concurrency-and-async-await }

Detalles sobre la sintaxis `async def` para *path operation functions* y algunos antecedentes sobre el código asíncrono, la concurrencia y el paralelismo.

## ¿Con prisa? { #in-a-hurry }

<abbr title="too long; didn't read - demasiado largo; no lo leí"><strong>TL;DR:</strong></abbr>

Si estás usando paquetes de terceros que te dicen que los llames con `await`, como:

```Python
results = await some_library()
```

Entonces, declara tus *path operation functions* con `async def` así:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | Nota

Solo puedes usar `await` dentro de funciones creadas con `async def`.

///

---

Si estás usando un paquete de terceros que se comunica con algo (una base de datos, una API, el sistema de archivos, etc.) y no tiene soporte para usar `await` (este es actualmente el caso para la mayoría de los paquetes de base de datos), entonces declara tus *path operation functions* como normalmente, usando simplemente `def`, así:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Si tu aplicación (de alguna manera) no tiene que comunicarse con nada más y esperar a que responda, usa `async def`, incluso si no necesitas usar `await` dentro.

---

Si simplemente no lo sabes, usa `def` normal.

---

**Nota**: Puedes mezclar `def` y `async def` en tus *path operation functions* tanto como necesites y definir cada una utilizando la mejor opción para ti. FastAPI hará lo correcto con ellas.

De todos modos, en cualquiera de los casos anteriores, FastAPI seguirá funcionando de forma asíncrona y será extremadamente rápido.

Pero al seguir los pasos anteriores, podrá hacer algunas optimizaciones de rendimiento.

## Detalles Técnicos { #technical-details }

Las versiones modernas de Python tienen soporte para **"código asíncrono"** utilizando algo llamado **"coroutines"**, con la sintaxis **`async` y `await`**.

Veamos esa frase por partes en las secciones a continuación:

* **Código Asíncrono**
* **`async` y `await`**
* **Coroutines**

## Código Asíncrono { #asynchronous-code }

El código asíncrono simplemente significa que el lenguaje 💬 tiene una forma de decirle a la computadora / programa 🤖 que en algún momento del código, tendrá que esperar que *otra cosa* termine en otro lugar. Digamos que esa *otra cosa* se llama "archivo-lento" 📝.

Entonces, durante ese tiempo, la computadora puede ir y hacer algún otro trabajo, mientras "archivo-lento" 📝 termina.

Luego la computadora / programa 🤖 volverá cada vez que tenga una oportunidad porque está esperando nuevamente, o siempre que 🤖 haya terminado todo el trabajo que tenía en ese punto. Y 🤖 comprobará si alguna de las tareas que estaba esperando ya se han completado, haciendo lo que tenía que hacer.

Después, 🤖 toma la primera tarea que termine (digamos, nuestro "archivo-lento" 📝) y continúa con lo que tenía que hacer con ella.

Ese "esperar otra cosa" normalmente se refiere a las operaciones de <abbr title="Input and Output - Entrada y salida">I/O</abbr> que son relativamente "lentas" (comparadas con la velocidad del procesador y la memoria RAM), como esperar:

* que los datos del cliente se envíen a través de la red
* que los datos enviados por tu programa sean recibidos por el cliente a través de la red
* que el contenido de un archivo en el disco sea leído por el sistema y entregado a tu programa
* que el contenido que tu programa entregó al sistema sea escrito en el disco
* una operación de API remota
* que una operación de base de datos termine
* que una query de base de datos devuelva los resultados
* etc.

Como el tiempo de ejecución se consume principalmente esperando operaciones de <abbr title="Input and Output - Entrada y salida">I/O</abbr>, las llaman operaciones "I/O bound".

Se llama "asíncrono" porque la computadora / programa no tiene que estar "sincronizado" con la tarea lenta, esperando el momento exacto en que la tarea termine, sin hacer nada, para poder tomar el resultado de la tarea y continuar el trabajo.

En lugar de eso, al ser un sistema "asíncrono", una vez terminado, la tarea puede esperar un poco en la cola (algunos microsegundos) para que la computadora / programa termine lo que salió a hacer, y luego regrese para tomar los resultados y continuar trabajando con ellos.

Para el "sincrónico" (contrario al "asíncrono") comúnmente también usan el término "secuencial", porque la computadora / programa sigue todos los pasos en secuencia antes de cambiar a una tarea diferente, incluso si esos pasos implican esperar.

### Concurrencia y Hamburguesas { #concurrency-and-burgers }

Esta idea de código **asíncrono** descrita anteriormente a veces también se llama **"concurrencia"**. Es diferente del **"paralelismo"**.

**Concurrencia** y **paralelismo** ambos se relacionan con "diferentes cosas sucediendo más o menos al mismo tiempo".

Pero los detalles entre *concurrencia* y *paralelismo* son bastante diferentes.

Para ver la diferencia, imagina la siguiente historia sobre hamburguesas:

### Hamburguesas Concurrentes { #concurrent-burgers }

Vas con tu crush a conseguir comida rápida, te pones en fila mientras el cajero toma los pedidos de las personas frente a ti. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Luego es tu turno, haces tu pedido de 2 hamburguesas muy sofisticadas para tu crush y para ti. 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

El cajero dice algo al cocinero en la cocina para que sepan que tienen que preparar tus hamburguesas (aunque actualmente están preparando las de los clientes anteriores).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

Pagas. 💸

El cajero te da el número de tu turno.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

Mientras esperas, vas con tu crush y eliges una mesa, te sientas y hablas con tu crush por un largo rato (ya que tus hamburguesas son muy sofisticadas y toman un tiempo en prepararse).

Mientras estás sentado en la mesa con tu crush, mientras esperas las hamburguesas, puedes pasar ese tiempo admirando lo increíble, lindo e inteligente que es tu crush ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Mientras esperas y hablas con tu crush, de vez en cuando revisas el número mostrado en el mostrador para ver si ya es tu turno.

Luego, en algún momento, finalmente es tu turno. Vas al mostrador, obtienes tus hamburguesas y vuelves a la mesa.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

Tú y tu crush comen las hamburguesas y pasan un buen rato. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// info | Información

Hermosas ilustraciones de [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Imagina que eres la computadora / programa 🤖 en esa historia.

Mientras estás en la fila, estás inactivo 😴, esperando tu turno, sin hacer nada muy "productivo". Pero la fila es rápida porque el cajero solo está tomando los pedidos (no preparándolos), así que está bien.

Luego, cuando es tu turno, haces un trabajo realmente "productivo", procesas el menú, decides lo que quieres, obtienes la elección de tu crush, pagas, verificas que das el billete o tarjeta correctos, verificas que te cobren correctamente, verificas que el pedido tenga los artículos correctos, etc.

Pero luego, aunque todavía no tienes tus hamburguesas, tu trabajo con el cajero está "en pausa" ⏸, porque tienes que esperar 🕙 a que tus hamburguesas estén listas.

Pero como te alejas del mostrador y te sientas en la mesa con un número para tu turno, puedes cambiar 🔀 tu atención a tu crush, y "trabajar" ⏯ 🤓 en eso. Luego, nuevamente estás haciendo algo muy "productivo" como es coquetear con tu crush 😍.

Luego el cajero 💁 dice "he terminado de hacer las hamburguesas" al poner tu número en el mostrador, pero no saltas como loco inmediatamente cuando el número mostrado cambia a tu número de turno. Sabes que nadie robará tus hamburguesas porque tienes el número de tu turno, y ellos tienen el suyo.

Así que esperas a que tu crush termine la historia (termine el trabajo ⏯ / tarea actual que se está procesando 🤓), sonríes amablemente y dices que vas por las hamburguesas ⏸.

Luego vas al mostrador 🔀, a la tarea inicial que ahora está terminada ⏯, recoges las hamburguesas, das las gracias y las llevas a la mesa. Eso termina ese paso / tarea de interacción con el mostrador ⏹. Eso a su vez, crea una nueva tarea, de "comer hamburguesas" 🔀 ⏯, pero la anterior de "obtener hamburguesas" ha terminado ⏹.

### Hamburguesas Paralelas { #parallel-burgers }

Ahora imaginemos que estas no son "Hamburguesas Concurrentes", sino "Hamburguesas Paralelas".

Vas con tu crush a obtener comida rápida paralela.

Te pones en fila mientras varios (digamos 8) cajeros que al mismo tiempo son cocineros toman los pedidos de las personas frente a ti.

Todos antes que tú están esperando a que sus hamburguesas estén listas antes de dejar el mostrador porque cada uno de los 8 cajeros va y prepara la hamburguesa de inmediato antes de obtener el siguiente pedido.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Luego, finalmente es tu turno, haces tu pedido de 2 hamburguesas muy sofisticadas para tu crush y para ti.

Pagas 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

El cajero va a la cocina.

Esperas, de pie frente al mostrador 🕙, para que nadie más tome tus hamburguesas antes que tú, ya que no hay números para los turnos.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

Como tú y tu crush están ocupados no dejando que nadie se interponga y tome tus hamburguesas cuando lleguen, no puedes prestar atención a tu crush. 😞

Este es un trabajo "sincrónico", estás "sincronizado" con el cajero/cocinero 👨‍🍳. Tienes que esperar 🕙 y estar allí en el momento exacto en que el cajero/cocinero 👨‍🍳 termine las hamburguesas y te las entregue, o de lo contrario, alguien más podría tomarlas.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

Luego tu cajero/cocinero 👨‍🍳 finalmente regresa con tus hamburguesas, después de mucho tiempo esperando 🕙 allí frente al mostrador.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

Tomas tus hamburguesas y vas a la mesa con tu crush.

Simplemente las comes, y has terminado. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

No hubo mucho hablar o coquetear ya que la mayor parte del tiempo se dedicó a esperar 🕙 frente al mostrador. 😞

/// info | Información

Hermosas ilustraciones de [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

En este escenario de las hamburguesas paralelas, eres una computadora / programa 🤖 con dos procesadores (tú y tu crush), ambos esperando 🕙 y dedicando su atención ⏯ a estar "esperando en el mostrador" 🕙 por mucho tiempo.

La tienda de comida rápida tiene 8 procesadores (cajeros/cocineros). Mientras que la tienda de hamburguesas concurrentes podría haber tenido solo 2 (un cajero y un cocinero).

Pero aún así, la experiencia final no es la mejor. 😞

---

Esta sería la historia equivalente de las hamburguesas paralelas. 🍔

Para un ejemplo más "de la vida real" de esto, imagina un banco.

Hasta hace poco, la mayoría de los bancos tenían múltiples cajeros 👨‍💼👨‍💼👨‍💼👨‍💼 y una gran fila 🕙🕙🕙🕙🕙🕙🕙🕙.

Todos los cajeros haciendo todo el trabajo con un cliente tras otro 👨‍💼⏯.

Y tienes que esperar 🕙 en la fila por mucho tiempo o pierdes tu turno.

Probablemente no querrías llevar a tu crush 😍 contigo a hacer trámites en el banco 🏦.

### Conclusión de las Hamburguesas { #burger-conclusion }

En este escenario de "hamburguesas de comida rápida con tu crush", como hay mucha espera 🕙, tiene mucho más sentido tener un sistema concurrente ⏸🔀⏯.

Este es el caso para la mayoría de las aplicaciones web.

Muchos, muchos usuarios, pero tu servidor está esperando 🕙 su conexión no tan buena para enviar sus requests.

Y luego esperar 🕙 nuevamente a que los responses retornen.

Esta "espera" 🕙 se mide en microsegundos, pero aún así, sumándolo todo, es mucha espera al final.

Por eso tiene mucho sentido usar código asíncrono ⏸🔀⏯ para las APIs web.

Este tipo de asincronía es lo que hizo popular a NodeJS (aunque NodeJS no es paralelo) y esa es la fortaleza de Go como lenguaje de programación.

Y ese es el mismo nivel de rendimiento que obtienes con **FastAPI**.

Y como puedes tener paralelismo y asincronía al mismo tiempo, obtienes un mayor rendimiento que la mayoría de los frameworks de NodeJS probados y a la par con Go, que es un lenguaje compilado más cercano a C [(todo gracias a Starlette)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1).

### ¿Es la concurrencia mejor que el paralelismo? { #is-concurrency-better-than-parallelism }

¡No! Esa no es la moraleja de la historia.

La concurrencia es diferente del paralelismo. Y es mejor en escenarios **específicos** que implican mucha espera. Debido a eso, generalmente es mucho mejor que el paralelismo para el desarrollo de aplicaciones web. Pero no para todo.

Así que, para equilibrar eso, imagina la siguiente historia corta:

> Tienes que limpiar una casa grande y sucia.

*Sí, esa es toda la historia*.

---

No hay esperas 🕙 en ninguna parte, solo mucho trabajo por hacer, en múltiples lugares de la casa.

Podrías tener turnos como en el ejemplo de las hamburguesas, primero la sala de estar, luego la cocina, pero como no estás esperando 🕙 nada, solo limpiando y limpiando, los turnos no afectarían nada.

Tomaría la misma cantidad de tiempo terminar con o sin turnos (concurrencia) y habrías hecho la misma cantidad de trabajo.

Pero en este caso, si pudieras traer a los 8 ex-cajeros/cocineros/ahora-limpiadores, y cada uno de ellos (más tú) pudiera tomar una zona de la casa para limpiarla, podrías hacer todo el trabajo en **paralelo**, con la ayuda extra, y terminar mucho antes.

En este escenario, cada uno de los limpiadores (incluyéndote) sería un procesador, haciendo su parte del trabajo.

Y como la mayor parte del tiempo de ejecución se dedica al trabajo real (en lugar de esperar), y el trabajo en una computadora lo realiza una <abbr title="Central Processing Unit - Unidad Central de Procesamiento">CPU</abbr>, llaman a estos problemas "CPU bound".

---

Ejemplos comunes de operaciones limitadas por la CPU son cosas que requieren procesamiento matemático complejo.

Por ejemplo:

* **Procesamiento de audio** o **imágenes**.
* **Visión por computadora**: una imagen está compuesta de millones de píxeles, cada píxel tiene 3 valores / colores, procesar eso normalmente requiere calcular algo en esos píxeles, todos al mismo tiempo.
* **Machine Learning**: normalmente requiere muchas multiplicaciones de "matrices" y "vectores". Piensa en una enorme hoja de cálculo con números y multiplicando todos juntos al mismo tiempo.
* **Deep Learning**: este es un subcampo de Machine Learning, por lo tanto, se aplica lo mismo. Es solo que no hay una sola hoja de cálculo de números para multiplicar, sino un enorme conjunto de ellas, y en muchos casos, usas un procesador especial para construir y / o usar esos modelos.

### Concurrencia + Paralelismo: Web + Machine Learning { #concurrency-parallelism-web-machine-learning }

Con **FastAPI** puedes aprovechar la concurrencia que es muy común para el desarrollo web (la misma atracción principal de NodeJS).

Pero también puedes explotar los beneficios del paralelismo y la multiprocesamiento (tener múltiples procesos ejecutándose en paralelo) para cargas de trabajo **CPU bound** como las de los sistemas de Machine Learning.

Eso, más el simple hecho de que Python es el lenguaje principal para **Data Science**, Machine Learning y especialmente Deep Learning, hacen de FastAPI una muy buena opción para APIs web de Data Science / Machine Learning y aplicaciones (entre muchas otras).

Para ver cómo lograr este paralelismo en producción, consulta la sección sobre [Despliegue](deployment/index.md).

## `async` y `await` { #async-and-await }

Las versiones modernas de Python tienen una forma muy intuitiva de definir código asíncrono. Esto hace que se vea igual que el código "secuencial" normal y hace el "wait" por ti en los momentos adecuados.

Cuando hay una operación que requerirá esperar antes de dar los resultados y tiene soporte para estas nuevas funcionalidades de Python, puedes programarlo así:

```Python
burgers = await get_burgers(2)
```

La clave aquí es el `await`. Dice a Python que tiene que esperar ⏸ a que `get_burgers(2)` termine de hacer su cosa 🕙 antes de almacenar los resultados en `burgers`. Con eso, Python sabrá que puede ir y hacer algo más 🔀 ⏯ mientras tanto (como recibir otro request).

Para que `await` funcione, tiene que estar dentro de una función que soporte esta asincronía. Para hacer eso, solo declara la función con `async def`:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Hacer algunas cosas asíncronas para crear las hamburguesas
    return burgers
```

...en lugar de `def`:

```Python hl_lines="2"
# Esto no es asíncrono
def get_sequential_burgers(number: int):
    # Hacer algunas cosas secuenciales para crear las hamburguesas
    return burgers
```

Con `async def`, Python sabe que, dentro de esa función, tiene que estar atento a las expresiones `await`, y que puede "pausar" ⏸ la ejecución de esa función e ir a hacer algo más 🔀 antes de regresar.

Cuando deseas llamar a una función `async def`, tienes que "await" dicha función. Así que, esto no funcionará:

```Python
# Esto no funcionará, porque get_burgers fue definido con: async def
burgers = get_burgers(2)
```

---

Así que, si estás usando un paquete que te dice que puedes llamarlo con `await`, necesitas crear las *path operation functions* que lo usen con `async def`, como en:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Más detalles técnicos { #more-technical-details }

Podrías haber notado que `await` solo se puede usar dentro de funciones definidas con `async def`.

Pero al mismo tiempo, las funciones definidas con `async def` deben ser "awaited". Por lo tanto, las funciones con `async def` solo se pueden llamar dentro de funciones definidas con `async def` también.

Entonces, sobre el huevo y la gallina, ¿cómo llamas a la primera función `async`?

Si estás trabajando con **FastAPI** no tienes que preocuparte por eso, porque esa "primera" función será tu *path operation function*, y FastAPI sabrá cómo hacer lo correcto.

Pero si deseas usar `async` / `await` sin FastAPI, también puedes hacerlo.

### Escribe tu propio código async { #write-your-own-async-code }

Starlette (y **FastAPI**) están basados en [AnyIO](https://anyio.readthedocs.io/en/stable/), lo que lo hace compatible tanto con el [asyncio](https://docs.python.org/3/library/asyncio-task.html) del paquete estándar de Python como con [Trio](https://trio.readthedocs.io/en/stable/).

En particular, puedes usar directamente [AnyIO](https://anyio.readthedocs.io/en/stable/) para tus casos de uso avanzados de concurrencia que requieran patrones más avanzados en tu propio código.

E incluso si no estuvieras usando FastAPI, también podrías escribir tus propias aplicaciones asíncronas con [AnyIO](https://anyio.readthedocs.io/en/stable/) para ser altamente compatibles y obtener sus beneficios (p.ej. *concurrencia estructurada*).

Creé otro paquete sobre AnyIO, como una capa delgada, para mejorar un poco las anotaciones de tipos y obtener mejor **autocompletado**, **errores en línea**, etc. También tiene una introducción amigable y tutorial para ayudarte a **entender** y escribir **tu propio código async**: [Asyncer](https://asyncer.tiangolo.com/). Sería particularmente útil si necesitas **combinar código async con regular** (bloqueante/sincrónico).

### Otras formas de código asíncrono { #other-forms-of-asynchronous-code }

Este estilo de usar `async` y `await` es relativamente nuevo en el lenguaje.

Pero hace que trabajar con código asíncrono sea mucho más fácil.

Esta misma sintaxis (o casi idéntica) también se incluyó recientemente en las versiones modernas de JavaScript (en el Navegador y NodeJS).

Pero antes de eso, manejar el código asíncrono era mucho más complejo y difícil.

En versiones previas de Python, podrías haber usado hilos o [Gevent](https://www.gevent.org/). Pero el código es mucho más complejo de entender, depurar y razonar.

En versiones previas de NodeJS / JavaScript en el Navegador, habrías usado "callbacks". Lo que lleva al "callback hell".

## Coroutines { #coroutines }

**Coroutines** es simplemente el término muy elegante para la cosa que devuelve una función `async def`. Python sabe que es algo parecido a una función, que puede comenzar y que terminará en algún momento, pero que podría pausar ⏸ internamente también, siempre que haya un `await` dentro de él.

Pero toda esta funcionalidad de usar código asíncrono con `async` y `await` a menudo se resume como utilizar "coroutines". Es comparable a la funcionalidad clave principal de Go, las "Goroutines".

## Conclusión { #conclusion }

Veamos la misma frase de arriba:

> Las versiones modernas de Python tienen soporte para **"código asíncrono"** utilizando algo llamado **"coroutines"**, con la sintaxis **`async` y `await`**.

Eso debería tener más sentido ahora. ✨

Todo eso es lo que impulsa FastAPI (a través de Starlette) y lo que hace que tenga un rendimiento tan impresionante.

## Detalles Muy Técnicos { #very-technical-details }

/// warning | Advertencia

Probablemente puedas saltarte esto.

Estos son detalles muy técnicos de cómo **FastAPI** funciona en su interior.

Si tienes bastante conocimiento técnico (coroutines, hilos, bloqueo, etc.) y tienes curiosidad sobre cómo FastAPI maneja `async def` vs `def` normal, adelante.

///

### Funciones de *path operation* { #path-operation-functions }

Cuando declaras una *path operation function* con `def` normal en lugar de `async def`, se ejecuta en un threadpool externo que luego es esperado, en lugar de ser llamado directamente (ya que bloquearía el servidor).

Si vienes de otro framework async que no funciona de la manera descrita anteriormente y estás acostumbrado a definir funciones de *path operation* solo de cómputo trivial con `def` normal para una pequeña ganancia de rendimiento (alrededor de 100 nanosegundos), ten en cuenta que en **FastAPI** el efecto sería bastante opuesto. En estos casos, es mejor usar `async def` a menos que tus *path operation functions* usen código que realice <abbr title="Input/Output - Entrada/Salida: lectura o escritura en disco, comunicaciones de red.">I/O</abbr> de bloqueo.

Aun así, en ambas situaciones, es probable que **FastAPI** [siga siendo más rápida](index.md#performance) que (o al menos comparable a) tu framework anterior.

### Dependencias { #dependencies }

Lo mismo aplica para las [dependencias](tutorial/dependencies/index.md). Si una dependencia es una función estándar `def` en lugar de `async def`, se ejecuta en el threadpool externo.

### Sub-dependencias { #sub-dependencies }

Puedes tener múltiples dependencias y [sub-dependencias](tutorial/dependencies/sub-dependencies.md) requiriéndose mutuamente (como parámetros de las definiciones de funciones), algunas de ellas podrían ser creadas con `async def` y algunas con `def` normal. Aun funcionará, y las que fueron creadas con `def` normal serían llamadas en un hilo externo (del threadpool) en lugar de ser "awaited".

### Otras funciones de utilidad { #other-utility-functions }

Cualquier otra función de utilidad que llames directamente puede ser creada con `def` normal o `async def` y FastAPI no afectará la forma en que la llames.

Esto contrasta con las funciones que FastAPI llama por ti: *path operation functions* y dependencias.

Si tu función de utilidad es una función normal con `def`, será llamada directamente (como la escribas en tu código), no en un threadpool; si la función es creada con `async def` entonces deberías "await" por esa función cuando la llames en tu código.

---

Nuevamente, estos son detalles muy técnicos que probablemente serían útiles si los buscaste.

De lo contrario, deberías estar bien con las pautas de la sección anterior: <a href="#in-a-hurry">¿Con prisa?</a>.
