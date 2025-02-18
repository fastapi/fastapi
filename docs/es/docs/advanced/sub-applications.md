# Sub Aplicaciones - Mounts

Si necesitas tener dos aplicaciones de **FastAPI** independientes, cada una con su propio OpenAPI independiente y su propia interfaz de docs, puedes tener una aplicación principal y "montar" una (o más) sub-aplicación(es).

## Montar una aplicación **FastAPI**

"Montar" significa añadir una aplicación completamente "independiente" en un path específico, que luego se encarga de manejar todo bajo ese path, con las _path operations_ declaradas en esa sub-aplicación.

### Aplicación de nivel superior

Primero, crea la aplicación principal de nivel superior de **FastAPI**, y sus *path operations*:

{* ../../docs_src/sub_applications/tutorial001.py hl[3, 6:8] *}

### Sub-aplicación

Luego, crea tu sub-aplicación, y sus *path operations*.

Esta sub-aplicación es solo otra aplicación estándar de FastAPI, pero es la que se "montará":

{* ../../docs_src/sub_applications/tutorial001.py hl[11, 14:16] *}

### Montar la sub-aplicación

En tu aplicación de nivel superior, `app`, monta la sub-aplicación, `subapi`.

En este caso, se montará en el path `/subapi`:

{* ../../docs_src/sub_applications/tutorial001.py hl[11, 19] *}

### Revisa la documentación automática de la API

Ahora, ejecuta el comando `fastapi` con tu archivo:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Y abre la documentación en <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Verás la documentación automática de la API para la aplicación principal, incluyendo solo sus propias _path operations_:

<img src="/img/tutorial/sub-applications/image01.png">

Y luego, abre la documentación para la sub-aplicación, en <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

Verás la documentación automática de la API para la sub-aplicación, incluyendo solo sus propias _path operations_, todas bajo el prefijo correcto del sub-path `/subapi`:

<img src="/img/tutorial/sub-applications/image02.png">

Si intentas interactuar con cualquiera de las dos interfaces de usuario, funcionarán correctamente, porque el navegador podrá comunicarse con cada aplicación o sub-aplicación específica.

### Detalles Técnicos: `root_path`

Cuando montas una sub-aplicación como se describe arriba, FastAPI se encargará de comunicar el path de montaje para la sub-aplicación usando un mecanismo de la especificación ASGI llamado `root_path`.

De esa manera, la sub-aplicación sabrá usar ese prefijo de path para la interfaz de documentación.

Y la sub-aplicación también podría tener sus propias sub-aplicaciones montadas y todo funcionaría correctamente, porque FastAPI maneja todos estos `root_path`s automáticamente.

Aprenderás más sobre el `root_path` y cómo usarlo explícitamente en la sección sobre [Detrás de un Proxy](behind-a-proxy.md){.internal-link target=_blank}.
