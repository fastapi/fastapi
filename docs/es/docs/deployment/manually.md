# Despliegue manualmente

De igual forma puedes desplegar **FastAPI** de forma manual.

Solo necesitas instalar un servidor ASGI compatible, como:

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, un super rápido servidor ASGI, construido en uvloop y httptools.

    <div class="termy">

    ```console
    $ pip install uvicorn[standard]

    ---> 100%
    ```

    </div>

    !!! tip
        Al añadir el `standard`, Uvicorn instalará y usará algunas dependencias extra recomendadas.

        Eso incluyendo `uvloop`, el remplazo de alto rendimiento para `asyncio`, que provee el gran salto de rendimiento en concurrencia.

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, un servidor ASGI también compatible con HTTP/2.

    <div class="termy">

    ```console
    $ pip install hypercorn

    ---> 100%
    ```

    </div>

    ...o cualquier servidor ASGI.

Y corre tu aplicación de la misma forma que lo has hecho en los tutoriales, pero sin la opción `--reload`, ejemplo:

=== "Uvicorn"

    <div class="termy">

    ```console
    $ uvicorn main:app --host 0.0.0.0 --port 80

    <span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    ```

    </div>

=== "Hypercorn"

    <div class="termy">

    ```console
    $ hypercorn main:app --bind 0.0.0.0:80

    Running on 0.0.0.0:8080 over http (CTRL + C to quit)
    ```

    </div>

Tal vez desearás configurar algunas herramientas, para asegurarte que se reinicie automáticamente si llega a parar.

También desearás instalar <a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a> y <a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">usarlo como administrador de Uvicorn</a>, o usar Hypercorn con multiples workers.

Asegurándose de ajustar el numero de workers, etc.

Pero si estás haciendo todo eso, podrías solamente usar la imagen de Docker que hace todo automáticamente.
