# FastAPI CLI

**FastAPI CLI** es un programa de línea de comandos que puedes usar para servir tu aplicación FastAPI, gestionar tu proyecto FastAPI, y más.

Cuando instalas FastAPI (por ejemplo, con `pip install "fastapi[standard]"`), incluye un paquete llamado `fastapi-cli`, este paquete proporciona el comando `fastapi` en la terminal.

Para ejecutar tu aplicación FastAPI en modo de desarrollo, puedes usar el comando `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

El programa de línea de comandos llamado `fastapi` es **FastAPI CLI**.

FastAPI CLI toma el path de tu programa Python (por ejemplo, `main.py`), detecta automáticamente la `FastAPI` instance (comúnmente llamada `app`), determina el proceso de import correcto, y luego la sirve.

Para producción usarías `fastapi run` en su lugar. 🚀

Internamente, **FastAPI CLI** usa <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>, un servidor ASGI de alto rendimiento y listo para producción. 😎

## `fastapi dev`

Ejecutar `fastapi dev` inicia el modo de desarrollo.

Por defecto, **auto-reload** está habilitado, recargando automáticamente el servidor cuando realizas cambios en tu código. Esto consume muchos recursos y podría ser menos estable que cuando está deshabilitado. Deberías usarlo solo para desarrollo. También escucha en la dirección IP `127.0.0.1`, que es la IP para que tu máquina se comunique solo consigo misma (`localhost`).

## `fastapi run`

Ejecutar `fastapi run` inicia FastAPI en modo de producción por defecto.

Por defecto, **auto-reload** está deshabilitado. También escucha en la dirección IP `0.0.0.0`, lo que significa todas las direcciones IP disponibles, de esta manera será accesible públicamente por cualquiera que pueda comunicarse con la máquina. Esta es la manera en la que normalmente lo ejecutarías en producción, por ejemplo, en un contenedor.

En la mayoría de los casos tendrías (y deberías) tener un "proxy de terminación" manejando HTTPS por ti, esto dependerá de cómo despliegues tu aplicación, tu proveedor podría hacer esto por ti, o podrías necesitar configurarlo tú mismo.

/// tip | Consejo

Puedes aprender más al respecto en la [documentación de despliegue](deployment/index.md){.internal-link target=_blank}.

///
