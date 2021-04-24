# Deploy FastAPI en Deta

En esta sección aprenderás a desplegar fácilmente una aplicación con **FastAPI** en <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> usando el plan gratuito. 🎁

Te tomará alrededor de **10 minutos**.

!!! info
    <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> es un patrocinador de **FastAPI**. 🎉

## Una app de **FastAPI** básica

* Crea un directorio para tu app, por ejemplo `./fastapideta/` y entra a el.

### Código de FastAPI

* Crea un archivo `main.py` con:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### Requerimientos

Ahora, en el mismo directorio crea el archivo `requirements.txt` con:

```text
fastapi
```

!!! tip
    No necesitas instalar Uvicorn para desplegar en Deta, aunque quizás quedrás instalarlo localmente para probar tu aplicación.

### Estructura del directorio

Tendrás ahora un directorio `./fastapideta/` con dos archivos:

```
.
└── main.py
└── requirements.txt
```

## Crea una cuenta gratuita de Deta

Ahora crea una <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">cuenta gratuita en Deta</a>, solamente necesitas un email y una contraseña.

Ni siquiera necesitas una tarjeta de crédito.

## Instala el CLI

Una vez que tienes tu cuenta, instala el <abbr title="Command Line Interface application (aplicación con interfaz de linea de comandos)">CLI</abbr> de Deta:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ curl -fsSL https://get.deta.dev/cli.sh | sh
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ iwr https://get.deta.dev/cli.ps1 -useb | iex
    ```

    </div>

Después de instalarlo, abre una nueva terminal para el CLI instalado sea detectado.

En una nueva terminal, confirma que fue correctamente instalado con:

<div class="termy">

```console
$ deta --help

Deta command line interface for managing deta micros.
Complete documentation available at https://docs.deta.sh

Usage:
  deta [flags]
  deta [command]

Available Commands:
  auth        Change auth settings for a deta micro

...
```

</div>

!!! tip
    Si tienes problemas instalando el CLI, revisa la <a href="https://docs.deta.sh/docs/micros/getting_started?ref=fastapi" class="external-link" target="_blank">documentación oficial de Deta</a>.

## Ingresa con el CLI

Ahora ingresa a Deta desde el CLI con:

<div class="termy">

```console
$ deta login

Please, log in from the web page. Waiting..
Logged in successfully.
```

</div>

Esto abrirá un navegador web y se autenticara automáticamente

## Haz el deployment con Deta

Después, despliega tu aplicación con el CLI de Deta:

<div class="termy">

```console
$ deta new

Successfully created a new micro

// Notice the "endpoint" 🔍

{
    "name": "fastapideta",
    "runtime": "python3.7",
    "endpoint": "https://qltnci.deta.dev",
    "visor": "enabled",
    "http_auth": "enabled"
}

Adding dependencies...


---> 100%


Successfully installed fastapi-0.61.1 pydantic-1.7.2 starlette-0.13.6
```

</div>

Veras un mensaje de tipo JSON semejante a:

```JSON hl_lines="4"
{
        "name": "fastapideta",
        "runtime": "python3.7",
        "endpoint": "https://qltnci.deta.dev",
        "visor": "enabled",
        "http_auth": "enabled"
}
```

!!! tip
    Tu <abbr title="despliegue">deployment<abbr> tendrá una URL `"endpoint"` diferente.

## Revísalo

Ahora abre tu explorador en tu URL `endpoint`. En el ejemplo anterior era `https://qltnci.deta.dev`, pero el tuyo será diferente.

Verás la respuesta JSON desde tu app de FastAPI:

```JSON
{
    "Hello": "World"
}
```

Ahora ve a los `/docs` de tu API, en el ejemplo anterior sería `https://qltnci.deta.dev/docs`.

Te mostrara tu documentación como:

<img src="https://fastapi.tiangolo.com/img/deployment/deta/image01.png">

## Activa el acceso público

Por defecto, Deta manejara la autenticación usando cookies para tu cuenta.

Pero una vez que estes listo, puedes hacerla pública con:

<div class="termy">

```console
$ deta auth disable

Successfully disabled http auth
```

</div>

Ahora puedes compartir la URL con quien sea y ellos podrán acceder a tu API. 🚀

## HTTPS

¡Felicidades!, ¡desplegaste tu app de FastAPI en Deta! 🎉 🍰

Ademas revisa que Deta maneja correctamente HTTPS por ti, para que tu no tengas que preocuparte por eso y puedas estar seguro que tus clientes tendrán una conexión segura y encriptada. ✅ 🔒

## Revisa el Visor

Desde la UI de tu documentación( estaran en una URL como `https://qltnci.deta.dev/docs`) envía una petición a tu *path operation* `/items/{item_id}`.

Por ejemplo con el ID `5`.

Ahora ve a <a href="https://web.deta.sh/" class="external-link" target="_blank">https://web.deta.sh</a>.

Vera que existe una sección a la izquierda llamada <abbr title="proviene de Micro(server)">"Micros"</abbr> con cada una de tus apps.

Verás una pestaña con los <abbr title"Detalles">"Details"</abbr>, y también una pestaña "Visor", ve a la pestaña "Visor".

Ahí puede revisar las peticiones recientes enviadas a tu app.

Ademas puedes editarlas y reproducirlas.

<img src="https://fastapi.tiangolo.com/img/deployment/deta/image02.png">

## Aprende más

En algún punto probablemente quedras almacenar algunos datos para tu app de una manera que persistan con el tiempo. Para eso puedes usar <a href="https://docs.deta.sh/docs/base/py_tutorial?ref=fastapi" class="external-link" target="_blank">Deta Base</a>, que también tine un generoso **free tier**

Puedes leer mas en la <a href="https://docs.deta.sh?ref=fastapi" class="external-link" target="_blank">documentación de Deta</a>.
