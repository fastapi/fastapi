# Deploy con Docker

En esta sección verás instrucciones y enlaces a guías para saber como:

* Haz de tu app con **FastAPI**, una imagen/contenedor de Docker con un máximo rendimiento. En cerca de **5 min**.
* (Opcionalmente) entender que, como desarrollador, necesitas conocer sobre HTTPS.
* Configurar un cluster de Docker Swarm mode con HTTPS automatico, incluso en un simple servidor por $5 USD/mes. En cerca de **20 min**.
* Generar y desplegar en toda su totalidad una aplicación con **FastAPI**, usando tu cluster de Docker Swarm, con HTTPS, etc. En cerca de **10 min**.

Usar <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a> para el deployment, tiene algunas ventajas como seguridad, replicabilidad, simplicdad en el desarrollo, etc.

Si estás usando Docker, puedes usar la imagen oficial de Docker en:

## <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>

Esta imagen tiene un mecanismo de "auto-calibración" incluido, así que puedes solamente añadir tu código y obtener muy alto rendimiento de forma automática. Y sin necesidad de hacer sacrificios.

Pero aun puedes cambiar y actualizar todas las configuraciones con variables de environment o otros archivos de configuración.

!!! tip
    Para ver todas las configuraciones y opciones, ve a la pagina de la imagen de Docker: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.

## Crea un `Dockerfile`

* Ve al directorio de tu proyecto.
* Crea un `Dockerfile` con:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
```

### Aplicaciones mas grandes

Si seguiste la sección sobre crear [Aplicaciones más Grandes con Multiples Archivos](../tutorial/bigger-applications.md){.internal-link target=_blank}, tu `Dockerfile` puede tal vez lucir así:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app
```

### Raspberry Pi y otras arquitecturas

Si estas corriendo Docker en una Raspberry Pi (la cual tiene un procesador ARM) o cualquier otra arquitectura, puedes crear un `Dockerfile` desde 0, basandote en una imagen de Python (la cual es de multi-arquitectura) y usar Uvicorn solamente.

Es este caso, tu `Dockerfile` podría lucir así:

```Dockerfile
FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

## Crea el código de **FastAPI**

* Crea un directorio para tu `app` e ingresa a el.
* Crea un archivo `main.py` con:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

* Deberías de tener un directorio estructurado de esta manera:

```
.
├── app
│   └── main.py
└── Dockerfile
```

## Construye la imagen de Docker

* Ve al directorio del proyecto (donde se encuentra tu `Dockerfile`, conteniendo el directorio de tu `app`).
* Construye tu imagen de FastAPI:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

## Inicializa tu contenedor de Docker

* Corre un contenedor basado en tu imagen:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

Ahora tienes un servidor de FastAPI optimizado en un contenedor de Docker. Auto-ajustado para tu servidor actual (y un numero de CPU cores).

## Revisalo

Deberías de poder revisarlo en el URL de tu contenedor de Docker, por ejemplo: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> or <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (o equivalente, usando tu Docker host)

Verás algo como esto:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Documentación Interactiva de la API

Ahora puedes ir a <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> o <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (o equivalente, usando tu Docker host).

Veras la documentación interactiva automática de tu API (proveída por <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Documentación Alternativa de la API

Ademas puedes ir a <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> o <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (o equivalente, usando tu Docker host).

Veras la documentación alternativa automática de tu API (proveída por <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Traefik

<a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a> es un balanceador de carga/proxy inverso de alto rendimiento. Puede hacer la tarea de "TLS Termination Proxy" (ademas de otras características).

Tiene una integración con Let's Encrypt. Por lo que, puede manejar todas las partes de HTTPS, incluyendo adquisición y renovación de certificados.

Ademas tiene integraciones con Docker. Por lo que, puedes declarar tus dominios en cada configuración de tu aplicación y poder leer esas configuraciones, generar el certificado HTTPS y servir HTTPS a tu aplicación de manera automática, sin requerir algún cambio en la configuración.

---

Con esta información y herramientas, continua con la siguiente sección para combinar todo.

## Docker Swarm mode cluster con Traefik y HTTPS

Puedes configurar un cluster de Docker Swarm mode, en minutos (cerca de 20) con un manejador de HTTPS de Traefik.

Al usar Docker Swarm mode, puedes iniciar con un "cluster" de una sola maquina (incluso puede ser un servidor de  $5 USD/mes)

Para configurar un cluster de Docker Swarm Mode con Traefik y manejo de HTTPS, sigue esta guía:

### <a href="https://medium.com/@tiangolo/docker-swarm-mode-and-traefik-for-a-https-cluster-20328dba6232" class="external-link" target="_blank">Docker Swarm Mode y Traefik para un HTTPS cluster</a>

### Deploy una aplicación de FastAPI

La manera mas facil de configurar todo, sera usando los [Project Generators de **FastAPI**](../project-generation.md){.internal-link target=_blank}.

Esta diseñado para ser integrado con este cluster de Docker Swarm con Traefik y HTTPS descrito arriba.

Puedes generar un proyecto en alrededor de 2 minutos.

El proyecto generado tiene instrucciones de desplegarlo, hacerlo toma otros 2 minutos.
