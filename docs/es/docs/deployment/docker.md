# FastAPI en Contenedores - Docker { #fastapi-in-containers-docker }

Al desplegar aplicaciones de FastAPI, un enfoque común es construir una **imagen de contenedor de Linux**. Normalmente se realiza usando [**Docker**](https://www.docker.com/). Luego puedes desplegar esa imagen de contenedor de varias formas.

Usar contenedores de Linux tiene varias ventajas, incluyendo **seguridad**, **replicabilidad**, **simplicidad**, y otras.

/// tip | Consejo

¿Tienes prisa y ya conoces esto? Salta al [`Dockerfile` más abajo 👇](#build-a-docker-image-for-fastapi).

///

<details>
<summary>Vista previa del Dockerfile 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# Si estás detrás de un proxy como Nginx o Traefik añade --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## Qué es un Contenedor { #what-is-a-container }

Los contenedores (principalmente contenedores de Linux) son una forma muy **ligera** de empaquetar aplicaciones incluyendo todas sus dependencias y archivos necesarios, manteniéndolos aislados de otros contenedores (otras aplicaciones o componentes) en el mismo sistema.

Los contenedores de Linux se ejecutan utilizando el mismo núcleo de Linux del host (máquina, máquina virtual, servidor en la nube, etc.). Esto significa que son muy ligeros (en comparación con las máquinas virtuales completas que emulan un sistema operativo completo).

De esta forma, los contenedores consumen **pocos recursos**, una cantidad comparable a ejecutar los procesos directamente (una máquina virtual consumiría mucho más).

Los contenedores también tienen sus propios procesos de ejecución **aislados** (normalmente solo un proceso), sistema de archivos y red, simplificando el despliegue, la seguridad, el desarrollo, etc.

## Qué es una Imagen de Contenedor { #what-is-a-container-image }

Un **contenedor** se ejecuta desde una **imagen de contenedor**.

Una imagen de contenedor es una versión **estática** de todos los archivos, variables de entorno y el comando/programa por defecto que debería estar presente en un contenedor. **Estático** aquí significa que la **imagen** de contenedor no se está ejecutando, no está siendo ejecutada, son solo los archivos empaquetados y los metadatos.

En contraste con una "**imagen de contenedor**" que son los contenidos estáticos almacenados, un "**contenedor**" normalmente se refiere a la instance en ejecución, lo que está siendo **ejecutado**.

Cuando el **contenedor** se inicia y está en funcionamiento (iniciado a partir de una **imagen de contenedor**), puede crear o cambiar archivos, variables de entorno, etc. Esos cambios existirán solo en ese contenedor, pero no persistirán en la imagen de contenedor subyacente (no se guardarán en disco).

Una imagen de contenedor es comparable al archivo de **programa** y sus contenidos, por ejemplo, `python` y algún archivo `main.py`.

Y el **contenedor** en sí (en contraste con la **imagen de contenedor**) es la instance real en ejecución de la imagen, comparable a un **proceso**. De hecho, un contenedor solo se está ejecutando cuando tiene un **proceso en ejecución** (y normalmente es solo un proceso). El contenedor se detiene cuando no hay un proceso en ejecución en él.

## Imágenes de Contenedor { #container-images }

Docker ha sido una de las herramientas principales para crear y gestionar **imágenes de contenedor** y **contenedores**.

Y hay un [Docker Hub](https://hub.docker.com/) público con **imágenes de contenedores oficiales** pre-hechas para muchas herramientas, entornos, bases de datos y aplicaciones.

Por ejemplo, hay una [Imagen de Python](https://hub.docker.com/_/python) oficial.

Y hay muchas otras imágenes para diferentes cosas como bases de datos, por ejemplo para:

* [PostgreSQL](https://hub.docker.com/_/postgres)
* [MySQL](https://hub.docker.com/_/mysql)
* [MongoDB](https://hub.docker.com/_/mongo)
* [Redis](https://hub.docker.com/_/redis), etc.

Usando una imagen de contenedor pre-hecha es muy fácil **combinar** y utilizar diferentes herramientas. Por ejemplo, para probar una nueva base de datos. En la mayoría de los casos, puedes usar las **imágenes oficiales**, y simplemente configurarlas con variables de entorno.

De esta manera, en muchos casos puedes aprender sobre contenedores y Docker y reutilizar ese conocimiento con muchas herramientas y componentes diferentes.

Así, ejecutarías **múltiples contenedores** con diferentes cosas, como una base de datos, una aplicación de Python, un servidor web con una aplicación frontend en React, y conectarlos entre sí a través de su red interna.

Todos los sistemas de gestión de contenedores (como Docker o Kubernetes) tienen estas funcionalidades de redes integradas.

## Contenedores y Procesos { #containers-and-processes }

Una **imagen de contenedor** normalmente incluye en sus metadatos el programa o comando por defecto que debería ser ejecutado cuando el **contenedor** se inicie y los parámetros que deben pasar a ese programa. Muy similar a lo que sería si estuviera en la línea de comandos.

Cuando un **contenedor** se inicia, ejecutará ese comando/programa (aunque puedes sobrescribirlo y hacer que ejecute un comando/programa diferente).

Un contenedor está en ejecución mientras el **proceso principal** (comando o programa) esté en ejecución.

Un contenedor normalmente tiene un **proceso único**, pero también es posible iniciar subprocesos desde el proceso principal, y de esa manera tendrás **múltiples procesos** en el mismo contenedor.

Pero no es posible tener un contenedor en ejecución sin **al menos un proceso en ejecución**. Si el proceso principal se detiene, el contenedor se detiene.

## Construir una Imagen de Docker para FastAPI { #build-a-docker-image-for-fastapi }

¡Bien, construyamos algo ahora! 🚀

Te mostraré cómo construir una **imagen de Docker** para FastAPI **desde cero**, basada en la imagen **oficial de Python**.

Esto es lo que querrías hacer en **la mayoría de los casos**, por ejemplo:

* Usando **Kubernetes** o herramientas similares
* Al ejecutar en un **Raspberry Pi**
* Usando un servicio en la nube que ejecutaría una imagen de contenedor por ti, etc.

### Requisitos del Paquete { #package-requirements }

Normalmente tendrías los **requisitos del paquete** para tu aplicación en algún archivo.

Dependería principalmente de la herramienta que uses para **instalar** esos requisitos.

La forma más común de hacerlo es tener un archivo `requirements.txt` con los nombres de los paquetes y sus versiones, uno por línea.

Por supuesto, usarías las mismas ideas que leíste en [Acerca de las versiones de FastAPI](versions.md) para establecer los rangos de versiones.

Por ejemplo, tu `requirements.txt` podría verse así:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

Y normalmente instalarías esas dependencias de los paquetes con `pip`, por ejemplo:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | Información

Existen otros formatos y herramientas para definir e instalar dependencias de paquetes.

///

### Crear el Código de **FastAPI** { #create-the-fastapi-code }

* Crea un directorio `app` y entra en él.
* Crea un archivo vacío `__init__.py`.
* Crea un archivo `main.py` con:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

Ahora, en el mismo directorio del proyecto, crea un archivo `Dockerfile` con:

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. Comenzar desde la imagen base oficial de Python.

2. Establecer el directorio de trabajo actual a `/code`.

    Aquí es donde pondremos el archivo `requirements.txt` y el directorio `app`.

3. Copiar el archivo con los requisitos al directorio `/code`.

    Copiar **solo** el archivo con los requisitos primero, no el resto del código.

    Como este archivo **no cambia a menudo**, Docker lo detectará y usará la **caché** para este paso, habilitando la caché para el siguiente paso también.

4. Instalar las dependencias de los paquetes en el archivo de requisitos.

    La opción `--no-cache-dir` le dice a `pip` que no guarde los paquetes descargados localmente, ya que eso solo sería si `pip` fuese a ejecutarse de nuevo para instalar los mismos paquetes, pero ese no es el caso al trabajar con contenedores.

    /// note | Nota

    El `--no-cache-dir` está relacionado solo con `pip`, no tiene nada que ver con Docker o contenedores.

    ///

    La opción `--upgrade` le dice a `pip` que actualice los paquetes si ya están instalados.

    Debido a que el paso anterior de copiar el archivo podría ser detectado por la **caché de Docker**, este paso también **usará la caché de Docker** cuando esté disponible.

    Usar la caché en este paso te **ahorrará** mucho **tiempo** al construir la imagen una y otra vez durante el desarrollo, en lugar de **descargar e instalar** todas las dependencias **cada vez**.

5. Copiar el directorio `./app` dentro del directorio `/code`.

    Como esto contiene todo el código, que es lo que **cambia con más frecuencia**, la **caché de Docker** no se utilizará para este u otros **pasos siguientes** fácilmente.

    Así que es importante poner esto **cerca del final** del `Dockerfile`, para optimizar los tiempos de construcción de la imagen del contenedor.

6. Establecer el **comando** para usar `fastapi run`, que utiliza Uvicorn debajo.

    `CMD` toma una lista de cadenas, cada una de estas cadenas es lo que escribirías en la línea de comandos separado por espacios.

    Este comando se ejecutará desde el **directorio de trabajo actual**, el mismo directorio `/code` que estableciste antes con `WORKDIR /code`.

/// tip | Consejo

Revisa qué hace cada línea haciendo clic en cada número en la burbuja del código. 👆

///

/// warning | Advertencia

Asegúrate de **siempre** usar la **forma exec** de la instrucción `CMD`, como se explica a continuación.

///

#### Usar `CMD` - Forma Exec { #use-cmd-exec-form }

La instrucción Docker [`CMD`](https://docs.docker.com/reference/dockerfile/#cmd) se puede escribir usando dos formas:

✅ **Forma Exec**:

```Dockerfile
# ✅ Haz esto
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Forma Shell**:

```Dockerfile
# ⛔️ No hagas esto
CMD fastapi run app/main.py --port 80
```

Asegúrate de siempre usar la **forma exec** para garantizar que FastAPI pueda cerrarse de manera adecuada y que [los eventos de lifespan](../advanced/events.md) sean disparados.

Puedes leer más sobre esto en la [documentación de Docker para formas de shell y exec](https://docs.docker.com/reference/dockerfile/#shell-and-exec-form).

Esto puede ser bastante notorio al usar `docker compose`. Consulta esta sección de preguntas frecuentes de Docker Compose para más detalles técnicos: [¿Por qué mis servicios tardan 10 segundos en recrearse o detenerse?](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop).

#### Estructura de Directorios { #directory-structure }

Ahora deberías tener una estructura de directorios como:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### Detrás de un Proxy de Terminación TLS { #behind-a-tls-termination-proxy }

Si estás ejecutando tu contenedor detrás de un Proxy de Terminación TLS (load balancer) como Nginx o Traefik, añade la opción `--proxy-headers`, esto le dirá a Uvicorn (a través de la CLI de FastAPI) que confíe en los headers enviados por ese proxy indicando que la aplicación se está ejecutando detrás de HTTPS, etc.

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Caché de Docker { #docker-cache }

Hay un truco importante en este `Dockerfile`, primero copiamos **el archivo con las dependencias solo**, no el resto del código. Déjame decirte por qué es así.

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker y otras herramientas **construyen** estas imágenes de contenedor **incrementalmente**, añadiendo **una capa sobre la otra**, empezando desde la parte superior del `Dockerfile` y añadiendo cualquier archivo creado por cada una de las instrucciones del `Dockerfile`.

Docker y herramientas similares también usan una **caché interna** al construir la imagen, si un archivo no ha cambiado desde la última vez que se construyó la imagen del contenedor, entonces reutilizará la misma capa creada la última vez, en lugar de copiar el archivo de nuevo y crear una nueva capa desde cero.

Solo evitar copiar archivos no mejora necesariamente las cosas mucho, pero porque se usó la caché para ese paso, puede **usar la caché para el siguiente paso**. Por ejemplo, podría usar la caché para la instrucción que instala las dependencias con:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

El archivo con los requisitos de los paquetes **no cambiará con frecuencia**. Así que, al copiar solo ese archivo, Docker podrá **usar la caché** para ese paso.

Y luego, Docker podrá **usar la caché para el siguiente paso** que descarga e instala esas dependencias. Y aquí es donde **ahorramos mucho tiempo**. ✨ ...y evitamos el aburrimiento de esperar. 😪😆

Descargar e instalar las dependencias de los paquetes **podría llevar minutos**, pero usando la **caché** tomaría **segundos** como máximo.

Y como estarías construyendo la imagen del contenedor una y otra vez durante el desarrollo para comprobar que los cambios en tu código funcionan, hay una gran cantidad de tiempo acumulado que te ahorrarías.

Luego, cerca del final del `Dockerfile`, copiamos todo el código. Como esto es lo que **cambia con más frecuencia**, lo ponemos cerca del final, porque casi siempre, cualquier cosa después de este paso no podrá usar la caché.

```Dockerfile
COPY ./app /code/app
```

### Construir la Imagen de Docker { #build-the-docker-image }

Ahora que todos los archivos están en su lugar, vamos a construir la imagen del contenedor.

* Ve al directorio del proyecto (donde está tu `Dockerfile`, conteniendo tu directorio `app`).
* Construye tu imagen de FastAPI:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | Consejo

Fíjate en el `.` al final, es equivalente a `./`, le indica a Docker el directorio a usar para construir la imagen del contenedor.

En este caso, es el mismo directorio actual (`.`).

///

### Iniciar el Contenedor Docker { #start-the-docker-container }

* Ejecuta un contenedor basado en tu imagen:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## Revísalo { #check-it }

Deberías poder revisarlo en la URL de tu contenedor de Docker, por ejemplo: [http://192.168.99.100/items/5?q=somequery](http://192.168.99.100/items/5?q=somequery) o [http://127.0.0.1/items/5?q=somequery](http://127.0.0.1/items/5?q=somequery) (o equivalente, usando tu host de Docker).

Verás algo como:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Documentación Interactiva de la API { #interactive-api-docs }

Ahora puedes ir a [http://192.168.99.100/docs](http://192.168.99.100/docs) o [http://127.0.0.1/docs](http://127.0.0.1/docs) (o equivalente, usando tu host de Docker).

Verás la documentación interactiva automática de la API (proporcionada por [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Documentación Alternativa de la API { #alternative-api-docs }

Y también puedes ir a [http://192.168.99.100/redoc](http://192.168.99.100/redoc) o [http://127.0.0.1/redoc](http://127.0.0.1/redoc) (o equivalente, usando tu host de Docker).

Verás la documentación alternativa automática (proporcionada por [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Construir una Imagen de Docker con un FastAPI de Un Solo Archivo { #build-a-docker-image-with-a-single-file-fastapi }

Si tu FastAPI es un solo archivo, por ejemplo, `main.py` sin un directorio `./app`, tu estructura de archivos podría verse así:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

Entonces solo tendrías que cambiar las rutas correspondientes para copiar el archivo dentro del `Dockerfile`:

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. Copia el archivo `main.py` directamente al directorio `/code` (sin ningún directorio `./app`).

2. Usa `fastapi run` para servir tu aplicación en el archivo único `main.py`.

Cuando pasas el archivo a `fastapi run`, detectará automáticamente que es un archivo único y no parte de un paquete y sabrá cómo importarlo y servir tu aplicación FastAPI. 😎

## Conceptos de Despliegue { #deployment-concepts }

Hablemos nuevamente de algunos de los mismos [Conceptos de Despliegue](concepts.md) en términos de contenedores.

Los contenedores son principalmente una herramienta para simplificar el proceso de **construcción y despliegue** de una aplicación, pero no imponen un enfoque particular para manejar estos **conceptos de despliegue**, y hay varias estrategias posibles.

La **buena noticia** es que con cada estrategia diferente hay una forma de cubrir todos los conceptos de despliegue. 🎉

Revisemos estos **conceptos de despliegue** en términos de contenedores:

* HTTPS
* Ejecutar en el inicio
* Reinicios
* Replicación (el número de procesos en ejecución)
* Memoria
* Pasos previos antes de comenzar

## HTTPS { #https }

Si nos enfocamos solo en la **imagen de contenedor** para una aplicación FastAPI (y luego el **contenedor** en ejecución), HTTPS normalmente sería manejado **externamente** por otra herramienta.

Podría ser otro contenedor, por ejemplo, con [Traefik](https://traefik.io/), manejando **HTTPS** y la adquisición **automática** de **certificados**.

/// tip | Consejo

Traefik tiene integraciones con Docker, Kubernetes, y otros, por lo que es muy fácil configurar y configurar HTTPS para tus contenedores con él.

///

Alternativamente, HTTPS podría ser manejado por un proveedor de la nube como uno de sus servicios (mientras que la aplicación aún se ejecuta en un contenedor).

## Ejecutar en el Inicio y Reinicios { #running-on-startup-and-restarts }

Normalmente hay otra herramienta encargada de **iniciar y ejecutar** tu contenedor.

Podría ser **Docker** directamente, **Docker Compose**, **Kubernetes**, un **servicio en la nube**, etc.

En la mayoría (o todas) de las casos, hay una opción sencilla para habilitar la ejecución del contenedor al inicio y habilitar los reinicios en caso de fallos. Por ejemplo, en Docker, es la opción de línea de comandos `--restart`.

Sin usar contenedores, hacer que las aplicaciones se ejecuten al inicio y con reinicios puede ser engorroso y difícil. Pero al **trabajar con contenedores** en la mayoría de los casos, esa funcionalidad se incluye por defecto. ✨

## Replicación - Número de Procesos { #replication-number-of-processes }

Si tienes un <dfn title="Un grupo de máquinas que están configuradas para estar conectadas y trabajar juntas de alguna manera.">clúster</dfn> de máquinas con **Kubernetes**, Docker Swarm Mode, Nomad, u otro sistema complejo similar para gestionar contenedores distribuidos en varias máquinas, entonces probablemente querrás manejar la **replicación** a nivel de **cluster** en lugar de usar un **gestor de procesos** (como Uvicorn con workers) en cada contenedor.

Uno de esos sistemas de gestión de contenedores distribuidos como Kubernetes normalmente tiene alguna forma integrada de manejar la **replicación de contenedores** mientras aún soporta el **load balancing** para las requests entrantes. Todo a nivel de **cluster**.

En esos casos, probablemente desearías construir una **imagen de Docker desde cero** como se [explica arriba](#dockerfile), instalando tus dependencias, y ejecutando **un solo proceso de Uvicorn** en lugar de usar múltiples workers de Uvicorn.

### Load Balancer { #load-balancer }

Al usar contenedores, normalmente tendrías algún componente **escuchando en el puerto principal**. Podría posiblemente ser otro contenedor que es también un **Proxy de Terminación TLS** para manejar **HTTPS** o alguna herramienta similar.

Como este componente tomaría la **carga** de las requests y las distribuiría entre los workers de una manera (esperablemente) **balanceada**, también se le llama comúnmente **Load Balancer**.

/// tip | Consejo

El mismo componente **Proxy de Terminación TLS** usado para HTTPS probablemente también sería un **Load Balancer**.

///

Y al trabajar con contenedores, el mismo sistema que usas para iniciarlos y gestionarlos ya tendría herramientas internas para transmitir la **comunicación en red** (e.g., requests HTTP) desde ese **load balancer** (que también podría ser un **Proxy de Terminación TLS**) a los contenedores con tu aplicación.

### Un Load Balancer - Múltiples Contenedores Worker { #one-load-balancer-multiple-worker-containers }

Al trabajar con **Kubernetes** u otros sistemas de gestión de contenedores distribuidos similares, usar sus mecanismos de red internos permitiría que el único **load balancer** que está escuchando en el **puerto** principal transmita la comunicación (requests) a posiblemente **múltiples contenedores** ejecutando tu aplicación.

Cada uno de estos contenedores ejecutando tu aplicación normalmente tendría **solo un proceso** (e.g., un proceso Uvicorn ejecutando tu aplicación FastAPI). Todos serían **contenedores idénticos**, ejecutando lo mismo, pero cada uno con su propio proceso, memoria, etc. De esa forma, aprovecharías la **paralelización** en **diferentes núcleos** de la CPU, o incluso en **diferentes máquinas**.

Y el sistema de contenedores distribuido con el **load balancer** **distribuiría las requests** a cada uno de los contenedores con tu aplicación **en turnos**. Así, cada request podría ser manejada por uno de los múltiples **contenedores replicados** ejecutando tu aplicación.

Y normalmente este **load balancer** podría manejar requests que vayan a *otras* aplicaciones en tu cluster (p. ej., a un dominio diferente, o bajo un prefijo de path de URL diferente), y transmitiría esa comunicación a los contenedores correctos para *esa otra* aplicación ejecutándose en tu cluster.

### Un Proceso por Contenedor { #one-process-per-container }

En este tipo de escenario, probablemente querrías tener **un solo proceso (Uvicorn) por contenedor**, ya que ya estarías manejando la replicación a nivel de cluster.

Así que, en este caso, **no** querrías tener múltiples workers en el contenedor, por ejemplo, con la opción de línea de comandos `--workers`. Querrías tener solo un **proceso Uvicorn por contenedor** (pero probablemente múltiples contenedores).

Tener otro gestor de procesos dentro del contenedor (como sería con múltiples workers) solo añadiría **complejidad innecesaria** que probablemente ya estés manejando con tu sistema de cluster.

### Contenedores con Múltiples Procesos y Casos Especiales { #containers-with-multiple-processes-and-special-cases }

Por supuesto, hay **casos especiales** donde podrías querer tener **un contenedor** con varios **worker processes de Uvicorn** dentro.

En esos casos, puedes usar la opción de línea de comandos `--workers` para establecer el número de workers que deseas ejecutar:

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. Aquí usamos la opción de línea de comandos `--workers` para establecer el número de workers a 4.

Aquí hay algunos ejemplos de cuándo eso podría tener sentido:

#### Una Aplicación Simple { #a-simple-app }

Podrías querer un gestor de procesos en el contenedor si tu aplicación es **lo suficientemente simple** que pueda ejecutarse en un **servidor único**, no un cluster.

#### Docker Compose { #docker-compose }

Podrías estar desplegando en un **servidor único** (no un cluster) con **Docker Compose**, por lo que no tendrías una forma fácil de gestionar la replicación de contenedores (con Docker Compose) mientras se preserva la red compartida y el **load balancing**.

Entonces podrías querer tener **un solo contenedor** con un **gestor de procesos** iniciando **varios worker processes** dentro.

---

El punto principal es que, **ninguna** de estas son **reglas escritas en piedra** que debas seguir a ciegas. Puedes usar estas ideas para **evaluar tu propio caso de uso** y decidir cuál es el mejor enfoque para tu sistema, verificando cómo gestionar los conceptos de:

* Seguridad - HTTPS
* Ejecutar en el inicio
* Reinicios
* Replicación (el número de procesos en ejecución)
* Memoria
* Pasos previos antes de comenzar

## Memoria { #memory }

Si ejecutas **un solo proceso por contenedor**, tendrás una cantidad de memoria más o menos bien definida, estable y limitada consumida por cada uno de esos contenedores (más de uno si están replicados).

Y luego puedes establecer esos mismos límites de memoria y requisitos en tus configuraciones para tu sistema de gestión de contenedores (por ejemplo, en **Kubernetes**). De esa manera, podrá **replicar los contenedores** en las **máquinas disponibles** teniendo en cuenta la cantidad de memoria necesaria por ellos, y la cantidad disponible en las máquinas en el cluster.

Si tu aplicación es **simple**, probablemente esto **no será un problema**, y puede que no necesites especificar límites de memoria estrictos. Pero si estás **usando mucha memoria** (por ejemplo, con modelos de **Machine Learning**), deberías verificar cuánta memoria estás consumiendo y ajustar el **número de contenedores** que se ejecutan en **cada máquina** (y tal vez agregar más máquinas a tu cluster).

Si ejecutas **múltiples procesos por contenedor**, tendrás que asegurarte de que el número de procesos iniciados no **consuma más memoria** de la que está disponible.

## Pasos Previos Antes de Comenzar y Contenedores { #previous-steps-before-starting-and-containers }

Si estás usando contenedores (por ejemplo, Docker, Kubernetes), entonces hay dos enfoques principales que puedes usar.

### Múltiples Contenedores { #multiple-containers }

Si tienes **múltiples contenedores**, probablemente cada uno ejecutando un **proceso único** (por ejemplo, en un cluster de **Kubernetes**), entonces probablemente querrías tener un **contenedor separado** realizando el trabajo de los **pasos previos** en un solo contenedor, ejecutando un solo proceso, **antes** de ejecutar los contenedores worker replicados.

/// info | Información

Si estás usando Kubernetes, probablemente sería un [Contenedor de Inicialización](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).

///

Si en tu caso de uso no hay problema en ejecutar esos pasos previos **múltiples veces en paralelo** (por ejemplo, si no estás ejecutando migraciones de base de datos, sino simplemente verificando si la base de datos está lista), entonces también podrías simplemente ponerlos en cada contenedor justo antes de iniciar el proceso principal.

### Un Contenedor Único { #single-container }

Si tienes una configuración simple, con un **contenedor único** que luego inicia múltiples **worker processes** (o también solo un proceso), entonces podrías ejecutar esos pasos previos en el mismo contenedor, justo antes de iniciar el proceso con la aplicación.

### Imagen Base de Docker { #base-docker-image }

Solía haber una imagen oficial de Docker de FastAPI: [tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker). Pero ahora está obsoleta. ⛔️

Probablemente **no** deberías usar esta imagen base de Docker (o cualquier otra similar).

Si estás usando **Kubernetes** (u otros) y ya estás configurando la **replicación** a nivel de cluster, con múltiples **contenedores**. En esos casos, es mejor que **construyas una imagen desde cero** como se describe arriba: [Construir una Imagen de Docker para FastAPI](#build-a-docker-image-for-fastapi).

Y si necesitas tener múltiples workers, puedes simplemente utilizar la opción de línea de comandos `--workers`.

/// note | Detalles Técnicos

La imagen de Docker se creó cuando Uvicorn no soportaba gestionar y reiniciar workers muertos, por lo que era necesario usar Gunicorn con Uvicorn, lo que añadía bastante complejidad, solo para que Gunicorn gestionara y reiniciara los worker processes de Uvicorn.

Pero ahora que Uvicorn (y el comando `fastapi`) soportan el uso de `--workers`, no hay razón para utilizar una imagen base de Docker en lugar de construir la tuya propia (es prácticamente la misma cantidad de código 😅).

///

## Desplegar la Imagen del Contenedor { #deploy-the-container-image }

Después de tener una Imagen de Contenedor (Docker) hay varias maneras de desplegarla.

Por ejemplo:

* Con **Docker Compose** en un servidor único
* Con un cluster de **Kubernetes**
* Con un cluster de Docker Swarm Mode
* Con otra herramienta como Nomad
* Con un servicio en la nube que tome tu imagen de contenedor y la despliegue

## Imagen de Docker con `uv` { #docker-image-with-uv }

Si estás usando [uv](https://github.com/astral-sh/uv) para instalar y gestionar tu proyecto, puedes seguir su [guía de Docker de uv](https://docs.astral.sh/uv/guides/integration/docker/).

## Resumen { #recap }

Usando sistemas de contenedores (por ejemplo, con **Docker** y **Kubernetes**) se vuelve bastante sencillo manejar todos los **conceptos de despliegue**:

* HTTPS
* Ejecutar en el inicio
* Reinicios
* Replicación (el número de procesos en ejecución)
* Memoria
* Pasos previos antes de comenzar

En la mayoría de los casos, probablemente no querrás usar ninguna imagen base, y en su lugar **construir una imagen de contenedor desde cero** basada en la imagen oficial de Docker de Python.

Teniendo en cuenta el **orden** de las instrucciones en el `Dockerfile` y la **caché de Docker** puedes **minimizar los tiempos de construcción**, para maximizar tu productividad (y evitar el aburrimiento). 😎
