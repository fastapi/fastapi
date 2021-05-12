# Sub-Aplicaciones - Montajes

Si necesitas tener dos aplicaciones independientes de FastAPI, con sus respectivos OpenAPI y documentaciones, puedes tener una aplicación principal y "montar" una (o más) sub-aplicacion(es).

## Montando una aplicación de **FastAPI** 

"Montar" significa añadir una aplicación completamente independiente en un <abbr title="ruta">path</abbr> específico, que se encarga de manejar todo bajo ese path, con las <abbr title="operaciones de ruta">_operaciones de path_</abbr> declaradas en la sub-aplicación.

### Aplicación de nivel superior

Primero, debemos crear la aplicación de nivel superior de **FastAPI**, y sus *operaciones de path*:

```Python hl_lines="3  6-8"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Sub-aplicación

Después, creamos la sub-aplicación, y sus *operaciones de path*.

Esta sub-aplicación es solamente otra aplicación estándar de FastAPI, pero es la que se va a "montar":

```Python hl_lines="11  14-16"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Montando la sub-aplicación

En tu aplicación de nivel superior `app`, montamos la sub-aplicación `subapi`.

En este caso, sera montada en el path `/subapi`:

```Python hl_lines="11  19"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Revisa la documentación automática de la API

Ahora, ejecutamos `uvicorn` con la aplicación principal, si tú archivo se llama `main.py`, sería:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

y abre la documentación en <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Veras la documentación automática de la API para la aplicación principal, incluyendo solamente sus _operaciones de path_:

<img src="https://fastapi.tiangolo.com/img/tutorial/sub-applications/image01.png">

Posteriormente, abre la documentación para la sub-aplicación, en <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

Observaras la documentación automática de la API para la sub-aplicación, incluyendo solamente sus _operaciones de path_, todo esto bajo el sub-path `/subapi`:

<img src="https://fastapi.tiangolo.com/img/tutorial/sub-applications/image02.png">

Si intentas interactuar con cualquiera de las dos interfaces funcionan perfectamente, gracias a que el navegador puede comunicarse especéficamente con la aplicación o con la sub-aplicación.

### Detalles técnicos: <abbr title="ruta raíz">`root_path`</abbr> 

Cuando realizamos el montaje de una sub-aplicación como se describió anteriormente, FastAPI se encargará de comunicar la ruta de montaje con la sub-aplicación usando un mecanismo ASGI llamado <abbr title="ruta raiz">`root_path`</abbr>.

De esta forma, la sub-aplicación sabrá como utilizar esa ruta para la documentación interactiva.

Y la sub-aplicación tambián podría tener sus propias sub-aplicaciones y todo funciona correctamente, todo gracias a que FastAPI maneja todos los <abbr title="ruta raiz">`root_path`</abbr> automáticamente.

Puedes aprender más acerca de `root_path` y como utilizarlo a fondo en la sección [Detras de un proxy](./behind-a-proxy.md){.internal-link target=_blank}.
