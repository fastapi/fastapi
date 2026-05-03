# Conceptos de Implementación { #deployments-concepts }

Cuando implementas una aplicación **FastAPI**, o en realidad, cualquier tipo de API web, hay varios conceptos que probablemente te importen, y al entenderlos, puedes encontrar la **forma más adecuada** de **implementar tu aplicación**.

Algunos de los conceptos importantes son:

* Seguridad - HTTPS
* Ejecución al iniciar
* Reinicios
* Replicación (la cantidad de procesos en ejecución)
* Memoria
* Pasos previos antes de iniciar

Veremos cómo afectan estas **implementaciones**.

Al final, el objetivo principal es poder **servir a tus clientes de API** de una manera que sea **segura**, para **evitar interrupciones**, y usar los **recursos de cómputo** (por ejemplo, servidores remotos/máquinas virtuales) de la manera más eficiente posible. 🚀

Te contaré un poquito más sobre estos **conceptos** aquí, y eso, con suerte, te dará la **intuición** que necesitarías para decidir cómo implementar tu API en diferentes entornos, posiblemente incluso en aquellos **futuros** que aún no existen.

Al considerar estos conceptos, podrás **evaluar y diseñar** la mejor manera de implementar **tus propias APIs**.

En los próximos capítulos, te daré más **recetas concretas** para implementar aplicaciones de FastAPI.

Pero por ahora, revisemos estas importantes **ideas conceptuales**. Estos conceptos también se aplican a cualquier otro tipo de API web. 💡

## Seguridad - HTTPS { #security-https }

En el [capítulo anterior sobre HTTPS](https.md) aprendimos sobre cómo HTTPS proporciona cifrado para tu API.

También vimos que HTTPS es normalmente proporcionado por un componente **externo** a tu servidor de aplicaciones, un **Proxy de Terminación TLS**.

Y debe haber algo encargado de **renovar los certificados HTTPS**, podría ser el mismo componente o algo diferente.

### Herramientas de Ejemplo para HTTPS { #example-tools-for-https }

Algunas de las herramientas que podrías usar como Proxy de Terminación TLS son:

* Traefik
    * Maneja automáticamente las renovaciones de certificados ✨
* Caddy
    * Maneja automáticamente las renovaciones de certificados ✨
* Nginx
    * Con un componente externo como Certbot para las renovaciones de certificados
* HAProxy
    * Con un componente externo como Certbot para las renovaciones de certificados
* Kubernetes con un Controlador de Ingress como Nginx
    * Con un componente externo como cert-manager para las renovaciones de certificados
* Manejado internamente por un proveedor de nube como parte de sus servicios (lee abajo 👇)

Otra opción es que podrías usar un **servicio de nube** que haga más del trabajo, incluyendo configurar HTTPS. Podría tener algunas restricciones o cobrarte más, etc. Pero en ese caso, no tendrías que configurar un Proxy de Terminación TLS tú mismo.

Te mostraré algunos ejemplos concretos en los próximos capítulos.

---

Luego, los siguientes conceptos a considerar son todos acerca del programa que ejecuta tu API real (por ejemplo, Uvicorn).

## Programa y Proceso { #program-and-process }

Hablaremos mucho sobre el "**proceso**" en ejecución, así que es útil tener claridad sobre lo que significa y cuál es la diferencia con la palabra "**programa**".

### Qué es un Programa { #what-is-a-program }

La palabra **programa** se usa comúnmente para describir muchas cosas:

* El **código** que escribes, los **archivos Python**.
* El **archivo** que puede ser **ejecutado** por el sistema operativo, por ejemplo: `python`, `python.exe` o `uvicorn`.
* Un programa específico mientras está siendo **ejecutado** en el sistema operativo, usando la CPU y almacenando cosas en la memoria. Esto también se llama **proceso**.

### Qué es un Proceso { #what-is-a-process }

La palabra **proceso** se usa normalmente de una manera más específica, refiriéndose solo a lo que está ejecutándose en el sistema operativo (como en el último punto anterior):

* Un programa específico mientras está siendo **ejecutado** en el sistema operativo.
    * Esto no se refiere al archivo, ni al código, se refiere **específicamente** a lo que está siendo **ejecutado** y gestionado por el sistema operativo.
* Cualquier programa, cualquier código, **solo puede hacer cosas** cuando está siendo **ejecutado**. Así que, cuando hay un **proceso en ejecución**.
* El proceso puede ser **terminado** (o "matado") por ti, o por el sistema operativo. En ese punto, deja de ejecutarse/ser ejecutado, y ya no puede **hacer cosas**.
* Cada aplicación que tienes en ejecución en tu computadora tiene algún proceso detrás, cada programa en ejecución, cada ventana, etc. Y normalmente hay muchos procesos ejecutándose **al mismo tiempo** mientras una computadora está encendida.
* Puede haber **múltiples procesos** del **mismo programa** ejecutándose al mismo tiempo.

Si revisas el "administrador de tareas" o "monitor del sistema" (o herramientas similares) en tu sistema operativo, podrás ver muchos de esos procesos en ejecución.

Y, por ejemplo, probablemente verás que hay múltiples procesos ejecutando el mismo programa del navegador (Firefox, Chrome, Edge, etc.). Normalmente ejecutan un proceso por pestaña, además de algunos otros procesos extra.

<img class="shadow" src="/img/deployment/concepts/image01.png">

---

Ahora que conocemos la diferencia entre los términos **proceso** y **programa**, sigamos hablando sobre implementaciones.

## Ejecución al Iniciar { #running-on-startup }

En la mayoría de los casos, cuando creas una API web, quieres que esté **siempre en ejecución**, ininterrumpida, para que tus clientes puedan acceder a ella en cualquier momento. Esto, por supuesto, a menos que tengas una razón específica para que se ejecute solo en ciertas situaciones, pero la mayoría de las veces quieres que esté constantemente en ejecución y **disponible**.

### En un Servidor Remoto { #in-a-remote-server }

Cuando configuras un servidor remoto (un servidor en la nube, una máquina virtual, etc.) lo más sencillo que puedes hacer es usar `fastapi run` (que utiliza Uvicorn) o algo similar, manualmente, de la misma manera que lo haces al desarrollar localmente.

Y funcionará y será útil **durante el desarrollo**.

Pero si pierdes la conexión con el servidor, el **proceso en ejecución** probablemente morirá.

Y si el servidor se reinicia (por ejemplo, después de actualizaciones o migraciones del proveedor de la nube) probablemente **no lo notarás**. Y debido a eso, ni siquiera sabrás que tienes que reiniciar el proceso manualmente. Así, tu API simplemente quedará muerta. 😱

### Ejecutar Automáticamente al Iniciar { #run-automatically-on-startup }

En general, probablemente querrás que el programa del servidor (por ejemplo, Uvicorn) se inicie automáticamente al arrancar el servidor, y sin necesidad de ninguna **intervención humana**, para tener siempre un proceso en ejecución con tu API (por ejemplo, Uvicorn ejecutando tu aplicación FastAPI).

### Programa Separado { #separate-program }

Para lograr esto, normalmente tendrás un **programa separado** que se asegurará de que tu aplicación se ejecute al iniciarse. Y en muchos casos, también se asegurará de que otros componentes o aplicaciones se ejecuten, por ejemplo, una base de datos.

### Herramientas de Ejemplo para Ejecutar al Iniciar { #example-tools-to-run-at-startup }

Algunos ejemplos de las herramientas que pueden hacer este trabajo son:

* Docker
* Kubernetes
* Docker Compose
* Docker en Modo Swarm
* Systemd
* Supervisor
* Manejado internamente por un proveedor de nube como parte de sus servicios
* Otros...

Te daré más ejemplos concretos en los próximos capítulos.

## Reinicios { #restarts }

De manera similar a asegurarte de que tu aplicación se ejecute al iniciar, probablemente también quieras asegurarte de que se **reinicie** después de fallos.

### Cometemos Errores { #we-make-mistakes }

Nosotros, como humanos, cometemos **errores**, todo el tiempo. El software casi *siempre* tiene **bugs** ocultos en diferentes lugares. 🐛

Y nosotros, como desarrolladores, seguimos mejorando el código a medida que encontramos esos bugs y a medida que implementamos nuevas funcionalidades (posiblemente agregando nuevos bugs también 😅).

### Errores Pequeños Manejados Automáticamente { #small-errors-automatically-handled }

Al construir APIs web con FastAPI, si hay un error en nuestro código, FastAPI normalmente lo contiene al request único que desencadenó el error. 🛡

El cliente obtendrá un **500 Internal Server Error** para ese request, pero la aplicación continuará funcionando para los siguientes requests en lugar de simplemente colapsar por completo.

### Errores Mayores - Colapsos { #bigger-errors-crashes }

Sin embargo, puede haber casos en los que escribamos algún código que **colapse toda la aplicación** haciendo que Uvicorn y Python colapsen. 💥

Y aún así, probablemente no querrías que la aplicación quede muerta porque hubo un error en un lugar, probablemente querrás que **siga ejecutándose** al menos para las *path operations* que no estén rotas.

### Reiniciar Después del Colapso { #restart-after-crash }

Pero en esos casos con errores realmente malos que colapsan el **proceso en ejecución**, querrías un componente externo encargado de **reiniciar** el proceso, al menos un par de veces...

/// tip | Consejo

...Aunque si la aplicación completa **colapsa inmediatamente**, probablemente no tenga sentido seguir reiniciándola eternamente. Pero en esos casos, probablemente lo notarás durante el desarrollo, o al menos justo después de la implementación.

Así que enfoquémonos en los casos principales, donde podría colapsar por completo en algunos casos particulares **en el futuro**, y aún así tenga sentido reiniciarla.

///

Probablemente querrías que la cosa encargada de reiniciar tu aplicación sea un **componente externo**, porque para ese punto, la misma aplicación con Uvicorn y Python ya colapsó, así que no hay nada en el mismo código de la misma aplicación que pueda hacer algo al respecto.

### Herramientas de Ejemplo para Reiniciar Automáticamente { #example-tools-to-restart-automatically }

En la mayoría de los casos, la misma herramienta que se utiliza para **ejecutar el programa al iniciar** también se utiliza para manejar reinicios automáticos.

Por ejemplo, esto podría ser manejado por:

* Docker
* Kubernetes
* Docker Compose
* Docker en Modo Swarm
* Systemd
* Supervisor
* Manejado internamente por un proveedor de nube como parte de sus servicios
* Otros...

## Replicación - Procesos y Memoria { #replication-processes-and-memory }

Con una aplicación FastAPI, usando un programa servidor como el comando `fastapi` que ejecuta Uvicorn, ejecutarlo una vez en **un proceso** puede servir a múltiples clientes concurrentemente.

Pero en muchos casos, querrás ejecutar varios worker processes al mismo tiempo.

### Múltiples Procesos - Workers { #multiple-processes-workers }

Si tienes más clientes de los que un solo proceso puede manejar (por ejemplo, si la máquina virtual no es muy grande) y tienes **múltiples núcleos** en la CPU del servidor, entonces podrías tener **múltiples procesos** ejecutando la misma aplicación al mismo tiempo, y distribuir todas las requests entre ellos.

Cuando ejecutas **múltiples procesos** del mismo programa de API, comúnmente se les llama **workers**.

### Worker Processes y Puertos { #worker-processes-and-ports }

Recuerda de la documentación [Sobre HTTPS](https.md) que solo un proceso puede estar escuchando en una combinación de puerto y dirección IP en un servidor.

Esto sigue siendo cierto.

Así que, para poder tener **múltiples procesos** al mismo tiempo, tiene que haber un **solo proceso escuchando en un puerto** que luego transmita la comunicación a cada worker process de alguna forma.

### Memoria por Proceso { #memory-per-process }

Ahora, cuando el programa carga cosas en memoria, por ejemplo, un modelo de Machine Learning en una variable, o el contenido de un archivo grande en una variable, todo eso **consume un poco de la memoria (RAM)** del servidor.

Y múltiples procesos normalmente **no comparten ninguna memoria**. Esto significa que cada proceso en ejecución tiene sus propias cosas, variables y memoria. Y si estás consumiendo una gran cantidad de memoria en tu código, **cada proceso** consumirá una cantidad equivalente de memoria.

### Memoria del Servidor { #server-memory }

Por ejemplo, si tu código carga un modelo de Machine Learning con **1 GB de tamaño**, cuando ejecutas un proceso con tu API, consumirá al menos 1 GB de RAM. Y si inicias **4 procesos** (4 workers), cada uno consumirá 1 GB de RAM. Así que, en total, tu API consumirá **4 GB de RAM**.

Y si tu servidor remoto o máquina virtual solo tiene 3 GB de RAM, intentar cargar más de 4 GB de RAM causará problemas. 🚨

### Múltiples Procesos - Un Ejemplo { #multiple-processes-an-example }

En este ejemplo, hay un **Proceso Administrador** que inicia y controla dos **Worker Processes**.

Este Proceso Administrador probablemente sería el que escuche en el **puerto** en la IP. Y transmitirá toda la comunicación a los worker processes.

Esos worker processes serían los que ejecutan tu aplicación, realizarían los cálculos principales para recibir un **request** y devolver un **response**, y cargarían cualquier cosa que pongas en variables en RAM.

<img src="/img/deployment/concepts/process-ram.drawio.svg">

Y por supuesto, la misma máquina probablemente tendría **otros procesos** ejecutándose también, aparte de tu aplicación.

Un detalle interesante es que el porcentaje de **CPU utilizado** por cada proceso puede **variar** mucho con el tiempo, pero la **memoria (RAM)** normalmente permanece más o menos **estable**.

Si tienes una API que hace una cantidad comparable de cálculos cada vez y tienes muchos clientes, entonces la **utilización de CPU** probablemente *también sea estable* (en lugar de constantemente subir y bajar rápidamente).

### Ejemplos de Herramientas y Estrategias de Replicación { #examples-of-replication-tools-and-strategies }

Puede haber varios enfoques para lograr esto, y te contaré más sobre estrategias específicas en los próximos capítulos, por ejemplo, al hablar sobre Docker y contenedores.

La principal restricción a considerar es que tiene que haber un **componente único** manejando el **puerto** en la **IP pública**. Y luego debe tener una forma de **transmitir** la comunicación a los **procesos/workers** replicados.

Aquí hay algunas combinaciones y estrategias posibles:

* **Uvicorn** con `--workers`
    * Un administrador de procesos de Uvicorn **escucharía** en la **IP** y **puerto**, y iniciaría **múltiples worker processes de Uvicorn**.
* **Kubernetes** y otros sistemas de **contenedor distribuidos**
    * Algo en la capa de **Kubernetes** escucharía en la **IP** y **puerto**. La replicación sería al tener **múltiples contenedores**, cada uno con **un proceso de Uvicorn** ejecutándose.
* **Servicios en la Nube** que manejan esto por ti
    * El servicio en la nube probablemente **manejará la replicación por ti**. Posiblemente te permitiría definir **un proceso para ejecutar**, o una **imagen de contenedor** para usar, en cualquier caso, lo más probable es que sería **un solo proceso de Uvicorn**, y el servicio en la nube se encargaría de replicarlo.

/// tip | Consejo

No te preocupes si algunos de estos elementos sobre **contenedores**, Docker, o Kubernetes no tienen mucho sentido todavía.

Te contaré más sobre imágenes de contenedores, Docker, Kubernetes, etc. en un capítulo futuro: [FastAPI en Contenedores - Docker](docker.md).

///

## Pasos Previos Antes de Iniciar { #previous-steps-before-starting }

Hay muchos casos en los que quieres realizar algunos pasos **antes de iniciar** tu aplicación.

Por ejemplo, podrías querer ejecutar **migraciones de base de datos**.

Pero en la mayoría de los casos, querrás realizar estos pasos solo **una vez**.

Así que, querrás tener un **único proceso** para realizar esos **pasos previos**, antes de iniciar la aplicación.

Y tendrás que asegurarte de que sea un único proceso ejecutando esos pasos previos incluso si después, inicias **múltiples procesos** (múltiples workers) para la propia aplicación. Si esos pasos fueran ejecutados por **múltiples procesos**, **duplicarían** el trabajo al ejecutarlo en **paralelo**, y si los pasos fueran algo delicado como una migración de base de datos, podrían causar conflictos entre sí.

Por supuesto, hay algunos casos en los que no hay problema en ejecutar los pasos previos múltiples veces, en ese caso, es mucho más fácil de manejar.

/// tip | Consejo

También, ten en cuenta que dependiendo de tu configuración, en algunos casos **quizás ni siquiera necesites realizar pasos previos** antes de iniciar tu aplicación.

En ese caso, no tendrías que preocuparte por nada de esto. 🤷

///

### Ejemplos de Estrategias para Pasos Previos { #examples-of-previous-steps-strategies }

Esto **dependerá mucho** de la forma en que **implementarás tu sistema**, y probablemente estará conectado con la forma en que inicias programas, manejas reinicios, etc.

Aquí hay algunas ideas posibles:

* Un "Contenedor de Inicio" en Kubernetes que se ejecuta antes de tu contenedor de aplicación
* Un script de bash que ejecuta los pasos previos y luego inicia tu aplicación
    * Aún necesitarías una forma de iniciar/reiniciar *ese* script de bash, detectar errores, etc.

/// tip | Consejo

Te daré más ejemplos concretos para hacer esto con contenedores en un capítulo futuro: [FastAPI en Contenedores - Docker](docker.md).

///

## Utilización de Recursos { #resource-utilization }

Tu(s) servidor(es) es(son) un **recurso** que puedes consumir o **utilizar**, con tus programas, el tiempo de cómputo en las CPUs y la memoria RAM disponible.

¿Cuánto de los recursos del sistema quieres consumir/utilizar? Podría ser fácil pensar "no mucho", pero en realidad, probablemente querrás consumir **lo más posible sin colapsar**.

Si estás pagando por 3 servidores pero solo estás usando un poquito de su RAM y CPU, probablemente estés **desperdiciando dinero** 💸, y probablemente **desperdiciando la energía eléctrica del servidor** 🌎, etc.

En ese caso, podría ser mejor tener solo 2 servidores y usar un mayor porcentaje de sus recursos (CPU, memoria, disco, ancho de banda de red, etc.).

Por otro lado, si tienes 2 servidores y estás usando **100% de su CPU y RAM**, en algún momento un proceso pedirá más memoria y el servidor tendrá que usar el disco como "memoria" (lo cual puede ser miles de veces más lento), o incluso **colapsar**. O un proceso podría necesitar hacer algún cálculo y tendría que esperar hasta que la CPU esté libre de nuevo.

En este caso, sería mejor obtener **un servidor extra** y ejecutar algunos procesos en él para que todos tengan **suficiente RAM y tiempo de CPU**.

También existe la posibilidad de que, por alguna razón, tengas un **pico** de uso de tu API. Tal vez se volvió viral, o tal vez otros servicios o bots comienzan a usarla. Y podrías querer tener recursos extra para estar a salvo en esos casos.

Podrías establecer un **número arbitrario** para alcanzar, por ejemplo, algo **entre 50% a 90%** de utilización de recursos. El punto es que esas son probablemente las principales cosas que querrás medir y usar para ajustar tus implementaciones.

Puedes usar herramientas simples como `htop` para ver la CPU y RAM utilizadas en tu servidor o la cantidad utilizada por cada proceso. O puedes usar herramientas de monitoreo más complejas, que pueden estar distribuidas a través de servidores, etc.

## Resumen { #recap }

Has estado leyendo aquí algunos de los conceptos principales que probablemente necesitarás tener en mente al decidir cómo implementar tu aplicación:

* Seguridad - HTTPS
* Ejecución al iniciar
* Reinicios
* Replicación (la cantidad de procesos en ejecución)
* Memoria
* Pasos previos antes de iniciar

Comprender estas ideas y cómo aplicarlas debería darte la intuición necesaria para tomar decisiones al configurar y ajustar tus implementaciones. 🤓

En las próximas secciones, te daré más ejemplos concretos de posibles estrategias que puedes seguir. 🚀
