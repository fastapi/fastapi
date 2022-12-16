# Plantillas

Puedes utilizar cualquier gestor de plantillas con **FastAPI**.

Una selección común es Jinja2, mismo que es utilizado por Flask y otras herramientas.

Existen utilidades que puedes configurar de manera sencilla ,  directamente en tu aplicación de **FastAPI** (proveída por Starlette).

## Instalar dependencias

Instala `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

Si además necesitas utilizar archivos estáticos (como en este ejemplo), instala `aiofiles`:

<div class="termy">

```console
$ pip install aiofiles

---> 100%
```

</div>

## Utilizando `Jinja2Templates`

* Importa `Jinja2Templates`.
* Crea un objeto de tipo `templates` que puedas reutilizar posteriormente.
* Declara un parámetro como <abbr title="Petición">`Request`</abbr> en la *operación de <abbr title="ruta">path</abbr>* que devolverá una plantilla.
* Usa el objeto `templates` que creaste , para renderizar y devolver un `TemplateResponse`, utilizando <abbr title="Petición">`request`</abbr> como una de las parejas clave-valor en el "contexto" de Jinja2.

```Python hl_lines="4  11  15-16"
{!../../../docs_src/templates/tutorial001.py!}
```

!!! Nota
    Observa que debes pasar la petición como parte de las parejas clave-valor en el contexto de Jinja2. por lo tanto , debes declararlo también en tus *operaciones de <abbr title="ruta">path</abbr>*.

!!! tip
    Declarando `response_class=HTMLResponse` , la documentación de la interfaz gráfica sabrá que la respuesta será un HTML.

!!! note "Detalles Técnicos"
    También puedes utilizar `from starlette.templating import Jinja2Templates`.

    **FastAPI** proporciona el mismo `starlette.templating` como `fastapi.templating`, siendo una conveniencia para ti, el desarrollador. Pero la mayoría de respuestas vienen directamente de Starlette. Lo mismo pasa con <abbr title="Petición">`Request`</abbr> y <abbr title="Archivos Estáticos">`StaticFiles`</abbr>.

## Creando plantillas

Puedes crear una plantilla en `templates/item.html` utilizando:

```jinja hl_lines="7"
{!../../../docs_src/templates/templates/item.html!}
```

Esto mostrará el `id`, tomado del `diccionario` utilizado como "contexto":

```Python
{"request": request, "id": id}
```

## Plantillas y archivos estáticos

Además puedes usar `url_for()` dentro de una plantilla, y utilizarlo por ejemplo, con <abbr title="Archivos Estáticos">`StaticFiles`</abbr> que hayas montado.

```jinja hl_lines="4"
{!../../../docs_src/templates/templates/item.html!}
```

En este ejemplo, está apuntando a un archivo CSS ubicado en `static/styles.css` que contiene:

```CSS hl_lines="4"
{!../../../docs_src/templates/static/styles.css!}
```

Y como estas utilizando `StaticFiles`, ese archivo CSS será proporcionado automáticamente por tu aplicación de **FastAPI** en la URL `/static/styles.css` .

## Más detalles

Para más detalles, incluido como probar las plantillas, consulta <a href="https://www.starlette.io/templates/" class="external-link" target="_blank">la documentación de Starlette acerca de plantillas</a>.
