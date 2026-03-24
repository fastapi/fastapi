# Aplicaciones más grandes - Múltiples archivos { #bigger-applications-multiple-files }

Si estás construyendo una aplicación o una API web, rara vez podrás poner todo en un solo archivo.

**FastAPI** proporciona una herramienta conveniente para estructurar tu aplicación manteniendo toda la flexibilidad.

/// info | Información

Si vienes de Flask, esto sería el equivalente a los Blueprints de Flask.

///

## Un ejemplo de estructura de archivos { #an-example-file-structure }

Digamos que tienes una estructura de archivos como esta:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | Consejo

Hay varios archivos `__init__.py`: uno en cada directorio o subdirectorio.

Esto es lo que permite importar código de un archivo a otro.

Por ejemplo, en `app/main.py` podrías tener una línea como:

```
from app.routers import items
```

///

* El directorio `app` contiene todo. Y tiene un archivo vacío `app/__init__.py`, por lo que es un "paquete de Python" (una colección de "módulos de Python"): `app`.
* Contiene un archivo `app/main.py`. Como está dentro de un paquete de Python (un directorio con un archivo `__init__.py`), es un "módulo" de ese paquete: `app.main`.
* También hay un archivo `app/dependencies.py`, al igual que `app/main.py`, es un "módulo": `app.dependencies`.
* Hay un subdirectorio `app/routers/` con otro archivo `__init__.py`, por lo que es un "subpaquete de Python": `app.routers`.
* El archivo `app/routers/items.py` está dentro de un paquete, `app/routers/`, por lo que es un submódulo: `app.routers.items`.
* Lo mismo con `app/routers/users.py`, es otro submódulo: `app.routers.users`.
* También hay un subdirectorio `app/internal/` con otro archivo `__init__.py`, por lo que es otro "subpaquete de Python": `app.internal`.
* Y el archivo `app/internal/admin.py` es otro submódulo: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

La misma estructura de archivos con comentarios:

```bash
.
├── app                  # "app" es un paquete de Python
│   ├── __init__.py      # este archivo hace que "app" sea un "paquete de Python"
│   ├── main.py          # módulo "main", por ejemplo import app.main
│   ├── dependencies.py  # módulo "dependencies", por ejemplo import app.dependencies
│   └── routers          # "routers" es un "subpaquete de Python"
│   │   ├── __init__.py  # hace que "routers" sea un "subpaquete de Python"
│   │   ├── items.py     # submódulo "items", por ejemplo import app.routers.items
│   │   └── users.py     # submódulo "users", por ejemplo import app.routers.users
│   └── internal         # "internal" es un "subpaquete de Python"
│       ├── __init__.py  # hace que "internal" sea un "subpaquete de Python"
│       └── admin.py     # submódulo "admin", por ejemplo import app.internal.admin
```

## `APIRouter` { #apirouter }

Digamos que el archivo dedicado solo a manejar usuarios es el submódulo en `/app/routers/users.py`.

Quieres tener las *path operations* relacionadas con tus usuarios separadas del resto del código, para mantenerlo organizado.

Pero todavía es parte de la misma aplicación/web API de **FastAPI** (es parte del mismo "paquete de Python").

Puedes crear las *path operations* para ese módulo usando `APIRouter`.

### Importar `APIRouter` { #import-apirouter }

Lo importas y creas una "instance" de la misma manera que lo harías con la clase `FastAPI`:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### *Path operations* con `APIRouter` { #path-operations-with-apirouter }

Y luego lo usas para declarar tus *path operations*.

Úsalo de la misma manera que usarías la clase `FastAPI`:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

Puedes pensar en `APIRouter` como una clase "mini `FastAPI`".

Se soportan todas las mismas opciones.

Todos los mismos `parameters`, `responses`, `dependencies`, `tags`, etc.

/// tip | Consejo

En este ejemplo, la variable se llama `router`, pero puedes nombrarla como quieras.

///

Vamos a incluir este `APIRouter` en la aplicación principal de `FastAPI`, pero primero, revisemos las dependencias y otro `APIRouter`.

## Dependencias { #dependencies }

Vemos que vamos a necesitar algunas dependencias usadas en varios lugares de la aplicación.

Así que las ponemos en su propio módulo `dependencies` (`app/dependencies.py`).

Ahora utilizaremos una dependencia simple para leer un header `X-Token` personalizado:

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | Consejo

Estamos usando un header inventado para simplificar este ejemplo.

Pero en casos reales obtendrás mejores resultados usando las [utilidades de Seguridad](security/index.md) integradas.

///

## Otro módulo con `APIRouter` { #another-module-with-apirouter }

Digamos que también tienes los endpoints dedicados a manejar "items" de tu aplicación en el módulo `app/routers/items.py`.

Tienes *path operations* para:

* `/items/`
* `/items/{item_id}`

Es toda la misma estructura que con `app/routers/users.py`.

Pero queremos ser más inteligentes y simplificar un poco el código.

Sabemos que todas las *path operations* en este módulo tienen el mismo:

* Prefijo de path: `/items`.
* `tags`: (solo una etiqueta: `items`).
* `responses` extra.
* `dependencies`: todas necesitan esa dependencia `X-Token` que creamos.

Entonces, en lugar de agregar todo eso a cada *path operation*, podemos agregarlo al `APIRouter`.

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

Como el path de cada *path operation* tiene que empezar con `/`, como en:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...el prefijo no debe incluir un `/` final.

Así que, el prefijo en este caso es `/items`.

También podemos agregar una lista de `tags` y `responses` extra que se aplicarán a todas las *path operations* incluidas en este router.

Y podemos agregar una lista de `dependencies` que se añadirá a todas las *path operations* en el router y se ejecutarán/solucionarán por cada request que les haga.

/// tip | Consejo

Nota que, al igual que [dependencias en decoradores de *path operations*](dependencies/dependencies-in-path-operation-decorators.md), ningún valor será pasado a tu *path operation function*.

///

El resultado final es que los paths de item son ahora:

* `/items/`
* `/items/{item_id}`

...como pretendíamos.

* Serán marcados con una lista de tags que contiene un solo string `"items"`.
  * Estos "tags" son especialmente útiles para los sistemas de documentación interactiva automática (usando OpenAPI).
* Todos incluirán las `responses` predefinidas.
* Todas estas *path operations* tendrán la lista de `dependencies` evaluadas/ejecutadas antes de ellas.
  * Si también declaras dependencias en una *path operation* específica, **también se ejecutarán**.
  * Las dependencias del router se ejecutan primero, luego las [`dependencies` en el decorador](dependencies/dependencies-in-path-operation-decorators.md), y luego las dependencias de parámetros normales.
  * También puedes agregar [dependencias de `Security` con `scopes`](../advanced/security/oauth2-scopes.md).

/// tip | Consejo

Tener `dependencies` en el `APIRouter` puede ser usado, por ejemplo, para requerir autenticación para un grupo completo de *path operations*. Incluso si las dependencias no son añadidas individualmente a cada una de ellas.

///

/// check | Revisa

Los parámetros `prefix`, `tags`, `responses`, y `dependencies` son (como en muchos otros casos) solo una funcionalidad de **FastAPI** para ayudarte a evitar la duplicación de código.

///

### Importar las dependencias { #import-the-dependencies }

Este código vive en el módulo `app.routers.items`, el archivo `app/routers/items.py`.

Y necesitamos obtener la función de dependencia del módulo `app.dependencies`, el archivo `app/dependencies.py`.

Así que usamos un import relativo con `..` para las dependencias:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### Cómo funcionan los imports relativos { #how-relative-imports-work }

/// tip | Consejo

Si sabes perfectamente cómo funcionan los imports, continúa a la siguiente sección abajo.

///

Un solo punto `.`, como en:

```Python
from .dependencies import get_token_header
```

significaría:

* Partiendo en el mismo paquete en el que este módulo (el archivo `app/routers/items.py`) habita (el directorio `app/routers/`)...
* busca el módulo `dependencies` (un archivo imaginario en `app/routers/dependencies.py`)...
* y de él, importa la función `get_token_header`.

Pero ese archivo no existe, nuestras dependencias están en un archivo en `app/dependencies.py`.

Recuerda cómo se ve nuestra estructura de aplicación/archivo:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

Los dos puntos `..`, como en:

```Python
from ..dependencies import get_token_header
```

significan:

* Partiendo en el mismo paquete en el que este módulo (el archivo `app/routers/items.py`) habita (el directorio `app/routers/`)...
* ve al paquete padre (el directorio `app/`)...
* y allí, busca el módulo `dependencies` (el archivo en `app/dependencies.py`)...
* y de él, importa la función `get_token_header`.

¡Eso funciona correctamente! 🎉

---

De la misma manera, si hubiéramos usado tres puntos `...`, como en:

```Python
from ...dependencies import get_token_header
```

eso significaría:

* Partiendo en el mismo paquete en el que este módulo (el archivo `app/routers/items.py`) habita (el directorio `app/routers/`)...
* ve al paquete padre (el directorio `app/`)...
* luego ve al paquete padre de ese paquete (no hay paquete padre, `app` es el nivel superior 😱)...
* y allí, busca el módulo `dependencies` (el archivo en `app/dependencies.py`)...
* y de él, importa la función `get_token_header`.

Eso se referiría a algún paquete arriba de `app/`, con su propio archivo `__init__.py`, etc. Pero no tenemos eso. Así que, eso lanzaría un error en nuestro ejemplo. 🚨

Pero ahora sabes cómo funciona, para que puedas usar imports relativos en tus propias apps sin importar cuán complejas sean. 🤓

### Agregar algunos `tags`, `responses`, y `dependencies` personalizados { #add-some-custom-tags-responses-and-dependencies }

No estamos agregando el prefijo `/items` ni los `tags=["items"]` a cada *path operation* porque los hemos añadido al `APIRouter`.

Pero aún podemos agregar _más_ `tags` que se aplicarán a una *path operation* específica, y también algunas `responses` extra específicas para esa *path operation*:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | Consejo

Esta última path operation tendrá la combinación de tags: `["items", "custom"]`.

Y también tendrá ambas responses en la documentación, una para `404` y otra para `403`.

///

## El `FastAPI` principal { #the-main-fastapi }

Ahora, veamos el módulo en `app/main.py`.

Aquí es donde importas y usas la clase `FastAPI`.

Este será el archivo principal en tu aplicación que conecta todo.

Y como la mayor parte de tu lógica ahora vivirá en su propio módulo específico, el archivo principal será bastante simple.

### Importar `FastAPI` { #import-fastapi }

Importas y creas una clase `FastAPI` como normalmente.

Y podemos incluso declarar [dependencias globales](dependencies/global-dependencies.md) que se combinarán con las dependencias para cada `APIRouter`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### Importar el `APIRouter` { #import-the-apirouter }

Ahora importamos los otros submódulos que tienen `APIRouter`s:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

Como los archivos `app/routers/users.py` y `app/routers/items.py` son submódulos que son parte del mismo paquete de Python `app`, podemos usar un solo punto `.` para importarlos usando "imports relativos".

### Cómo funciona la importación { #how-the-importing-works }

La sección:

```Python
from .routers import items, users
```

significa:

* Partiendo en el mismo paquete en el que este módulo (el archivo `app/main.py`) habita (el directorio `app/`)...
* busca el subpaquete `routers` (el directorio en `app/routers/`)...
* y de él, importa el submódulo `items` (el archivo en `app/routers/items.py`) y `users` (el archivo en `app/routers/users.py`)...

El módulo `items` tendrá una variable `router` (`items.router`). Este es el mismo que creamos en el archivo `app/routers/items.py`, es un objeto `APIRouter`.

Y luego hacemos lo mismo para el módulo `users`.

También podríamos importarlos así:

```Python
from app.routers import items, users
```

/// info | Información

La primera versión es un "import relativo":

```Python
from .routers import items, users
```

La segunda versión es un "import absoluto":

```Python
from app.routers import items, users
```

Para aprender más sobre Paquetes y Módulos de Python, lee [la documentación oficial de Python sobre Módulos](https://docs.python.org/3/tutorial/modules.html).

///

### Evitar colisiones de nombres { #avoid-name-collisions }

Estamos importando el submódulo `items` directamente, en lugar de importar solo su variable `router`.

Esto se debe a que también tenemos otra variable llamada `router` en el submódulo `users`.

Si hubiéramos importado uno después del otro, como:

```Python
from .routers.items import router
from .routers.users import router
```

el `router` de `users` sobrescribiría el de `items` y no podríamos usarlos al mismo tiempo.

Así que, para poder usar ambos en el mismo archivo, importamos los submódulos directamente:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### Incluir los `APIRouter`s para `users` y `items` { #include-the-apirouters-for-users-and-items }

Ahora, incluyamos los `router`s de los submódulos `users` y `items`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info | Información

`users.router` contiene el `APIRouter` dentro del archivo `app/routers/users.py`.

Y `items.router` contiene el `APIRouter` dentro del archivo `app/routers/items.py`.

///

Con `app.include_router()` podemos agregar cada `APIRouter` a la aplicación principal de `FastAPI`.

Incluirá todas las rutas de ese router como parte de ella.

/// note | Detalles Técnicos

En realidad creará internamente una *path operation* para cada *path operation* que fue declarada en el `APIRouter`.

Así, detrás de escena, funcionará como si todo fuera la misma única app.

///

/// check | Revisa

No tienes que preocuparte por el rendimiento al incluir routers.

Esto tomará microsegundos y solo sucederá al inicio.

Así que no afectará el rendimiento. ⚡

///

### Incluir un `APIRouter` con un `prefix`, `tags`, `responses`, y `dependencies` personalizados { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

Ahora, imaginemos que tu organización te dio el archivo `app/internal/admin.py`.

Contiene un `APIRouter` con algunas *path operations* de administración que tu organización comparte entre varios proyectos.

Para este ejemplo será súper simple. Pero digamos que porque está compartido con otros proyectos en la organización, no podemos modificarlo y agregar un `prefix`, `dependencies`, `tags`, etc. directamente al `APIRouter`:

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

Pero aún queremos configurar un `prefix` personalizado al incluir el `APIRouter` para que todas sus *path operations* comiencen con `/admin`, queremos asegurarlo con las `dependencies` que ya tenemos para este proyecto, y queremos incluir `tags` y `responses`.

Podemos declarar todo eso sin tener que modificar el `APIRouter` original pasando esos parámetros a `app.include_router()`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

De esa manera, el `APIRouter` original permanecerá sin modificar, por lo que aún podemos compartir ese mismo archivo `app/internal/admin.py` con otros proyectos en la organización.

El resultado es que, en nuestra app, cada una de las *path operations* del módulo `admin` tendrá:

* El prefix `/admin`.
* El tag `admin`.
* La dependencia `get_token_header`.
* La response `418`. 🍵

Pero eso solo afectará a ese `APIRouter` en nuestra app, no en ningún otro código que lo utilice.

Así, por ejemplo, otros proyectos podrían usar el mismo `APIRouter` con un método de autenticación diferente.

### Incluir una *path operation* { #include-a-path-operation }

También podemos agregar *path operations* directamente a la app de `FastAPI`.

Aquí lo hacemos... solo para mostrar que podemos 🤷:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

y funcionará correctamente, junto con todas las otras *path operations* añadidas con `app.include_router()`.

/// info | Detalles Muy Técnicos

**Nota**: este es un detalle muy técnico que probablemente puedes **simplemente omitir**.

---

Los `APIRouter`s no están "montados", no están aislados del resto de la aplicación.

Esto se debe a que queremos incluir sus *path operations* en el esquema de OpenAPI y las interfaces de usuario.

Como no podemos simplemente aislarlos y "montarlos" independientemente del resto, las *path operations* se "clonan" (se vuelven a crear), no se incluyen directamente.

///

## Configurar el `entrypoint` en `pyproject.toml` { #configure-the-entrypoint-in-pyproject-toml }

Como tu objeto `app` de FastAPI vive en `app/main.py`, puedes configurar el `entrypoint` en tu archivo `pyproject.toml` así:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

que es equivalente a importar como:

```python
from app.main import app
```

De esa manera el comando `fastapi` sabrá dónde encontrar tu app.

/// Note | Nota

También podrías pasar la ruta al comando, como:

```console
$ fastapi dev app/main.py
```

Pero tendrías que recordar pasar la ruta correcta cada vez que llames al comando `fastapi`.

Además, otras herramientas podrían no ser capaces de encontrarla, por ejemplo la [Extensión de VS Code](../editor-support.md) o [FastAPI Cloud](https://fastapicloud.com), así que se recomienda usar el `entrypoint` en `pyproject.toml`.

///

## Revisa la documentación automática de la API { #check-the-automatic-api-docs }

Ahora, ejecuta tu app:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Y abre la documentación en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Verás la documentación automática de la API, incluyendo los paths de todos los submódulos, usando los paths correctos (y prefijos) y los tags correctos:

<img src="/img/tutorial/bigger-applications/image01.png">

## Incluir el mismo router múltiples veces con diferentes `prefix` { #include-the-same-router-multiple-times-with-different-prefix }

También puedes usar `.include_router()` múltiples veces con el *mismo* router usando diferentes prefijos.

Esto podría ser útil, por ejemplo, para exponer la misma API bajo diferentes prefijos, por ejemplo, `/api/v1` y `/api/latest`.

Este es un uso avanzado que quizás no necesites realmente, pero está allí en caso de que lo necesites.

## Incluir un `APIRouter` en otro { #include-an-apirouter-in-another }

De la misma manera que puedes incluir un `APIRouter` en una aplicación `FastAPI`, puedes incluir un `APIRouter` en otro `APIRouter` usando:

```Python
router.include_router(other_router)
```

Asegúrate de hacerlo antes de incluir `router` en la app de `FastAPI`, para que las *path operations* de `other_router` también se incluyan.
