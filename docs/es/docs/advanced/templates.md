# Plantillas

Puedes usar cualquier motor de plantillas que desees con **FastAPI**.

Una elección común es Jinja2, el mismo que usa Flask y otras herramientas.

Hay utilidades para configurarlo fácilmente que puedes usar directamente en tu aplicación de **FastAPI** (proporcionadas por Starlette).

## Instalar dependencias

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, activarlo e instalar `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Usando `Jinja2Templates`

* Importa `Jinja2Templates`.
* Crea un objeto `templates` que puedas reutilizar más tarde.
* Declara un parámetro `Request` en la *path operation* que devolverá una plantilla.
* Usa los `templates` que creaste para renderizar y devolver un `TemplateResponse`, pasa el nombre de la plantilla, el objeto de request, y un diccionario "context" con pares clave-valor que se usarán dentro de la plantilla Jinja2.

{* ../../docs_src/templates/tutorial001.py hl[4,11,15:18] *}

/// note | Nota

Antes de FastAPI 0.108.0, Starlette 0.29.0, el `name` era el primer parámetro.

Además, antes de eso, en versiones anteriores, el objeto `request` se pasaba como parte de los pares clave-valor en el contexto para Jinja2.

///

/// tip | Consejo

Al declarar `response_class=HTMLResponse`, la interfaz de usuario de la documentación podrá saber que el response será HTML.

///

/// note | Nota Técnica

También podrías usar `from starlette.templating import Jinja2Templates`.

**FastAPI** proporciona el mismo `starlette.templating` como `fastapi.templating`, solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette. Lo mismo con `Request` y `StaticFiles`.

///

## Escribiendo plantillas

Luego puedes escribir una plantilla en `templates/item.html` con, por ejemplo:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Valores de Contexto de la Plantilla

En el HTML que contiene:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...mostrará el `id` tomado del `dict` de "contexto" que pasaste:

```Python
{"id": id}
```

Por ejemplo, con un ID de `42`, esto se renderizaría como:

```html
Item ID: 42
```

### Argumentos de la Plantilla `url_for`

También puedes usar `url_for()` dentro de la plantilla, toma como argumentos los mismos que usaría tu *path operation function*.

Entonces, la sección con:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...generará un enlace hacia la misma URL que manejaría la *path operation function* `read_item(id=id)`.

Por ejemplo, con un ID de `42`, esto se renderizaría como:

```html
<a href="/items/42">
```

## Plantillas y archivos estáticos

También puedes usar `url_for()` dentro de la plantilla, y usarlo, por ejemplo, con los `StaticFiles` que montaste con el `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

En este ejemplo, enlazaría a un archivo CSS en `static/styles.css` con:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

Y porque estás usando `StaticFiles`, ese archivo CSS sería servido automáticamente por tu aplicación de **FastAPI** en la URL `/static/styles.css`.

## Más detalles

Para más detalles, incluyendo cómo testear plantillas, revisa <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">la documentación de Starlette sobre plantillas</a>.
