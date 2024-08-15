# Desarrollo - Contribuciones

Primero, puedes revisar las guías para [ayudar a FastAPI y obtener ayuda](help-fastapi.md){.internal-link target=_blank}.

## Desarrollando

Si ya has clonado el  <a href="https://github.com/fastapi/fastapi" class="external-link" target="_blank">repositorio de fastapi</a> y quieres profundizar más en el código, aqui hay algunas guías para preparar tu entorno.

### Entorno virtual con `venv`

Puedes crear un entorno virtual aislado en un directorio usando el modulo `venv` de Python. Vamos a hacerlo en el repositorio clonado (donde están los `requirements.txt`):

<div class="termy">

```console
$ python -m venv env
```

</div>

Esto creará un directorio `./env/` con los binarios de Python, y luego podrás instalar paquetes en tu entorno local.

### Activar el entorno

Activa el nuevo entorno con:

//// tab | Linux, macos

<div class="termy">

```console
$ source ./env/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .\env\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

O si utilizas Bash para Windows (e.j. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

<div class="termy">

```console
$ source ./env/Scripts/activate
```

</div>

////

Para verificar que todo funciona, usa:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
$ which pip

some/directory/fastapi/env/bin/pip
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ Get-Command pip

some/directory/fastapi/env/bin/pip
```

</div>

////

Si te muestra que el binario de `pip` se encuentra ubicado en `env/bin/pip` es porque todo funcionó. 🎉

Asegúrate de tener la versión más reciente de pip en tu entorno local para evitar errores en los próximos pasos:

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

/// Tip | Consejo

Cada vez que instales un nuevo paquete con `pip` dentro de este entorno, recuerda activar el entorno nuevamente.

Esto asegura que, si usas un programa de terminal instalado por ese paquete, utilices el que está en tu entorno local y no otro que podría estar instalado globalmente.

///


### Instalar los requirements usando pip

Después de activar el entorno como se explica en pasos anteriores:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

Este comando instalará todas las dependencias y tu FastAPI local en tu entorno local.

### Usando FastAPI en tu entorno local

Si creas un archivo de Python que importe y use FastAPI, y lo ejecutas con Python de tu entorno local, este usará el código fuente de FastAPI clonado localmente.

Y si tu actualizas el FastAPI local desde el código fuente local de FastAPI, por lo tanto cuando ejecutes ese archivo de Python de nuevo, entonces se ejecutará la versión más reciente de FastAPI que acabas de editar.

De esta manera, no tienes que "instalar" tu versión local para poder probar cada cambio.

/// note | "Detalles Técnicos"

Esto solo sucede cuando lo instalas usando este archivo `requirements.txt` incluido en lugar de ejecutar `pip install fastapi` directamente.

Eso se debe a que dentro del archivo `requirements.txt`, el FastAPI local está marcado para ser instalado en modo "editable", con la opción `-e`.


///

### Formatea el código

Hay un script que puedes ejecutar que te formateará y limpiará todo tu código:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

Además, también ordenará automáticamente todas tus importaciones.

Para que se ordenen correctamente, necesitas tener FastAPI instalado localmente en tu entorno, con el comando en la sección anterior usando `-e`.

## Docs

Primero, asegúrate de configurar tu entorno como se explica arriba, para que instales todas las dependencias.

### Docs live

Durante el desarrollo local, hay un script que construye el sitio y comprueba si hay cambios, recargando en vivo:


<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Esto servirá la documentación en `http://127.0.0.1:8008`.

Por lo tanto, puedes editar los archivos de documentación y ver los cambios en vivo.

/// Tip | Consejo

Alternativamente, puedes realizar los mismos pasos que los scripts hacen manualmente.

Vamos a la carpeta de idioma, para los documentos principales en inglés es en `docs/en/`:

```console
$ cd docs/en/
```
Entonces ejecuta `mkdocs` en esa carpeta:

```console
$ mkdocs serve --dev-addr 8008
```

///

#### Typer CLI (opcional)

Las instrucciones hasta ahora te han mostrado cómo usar el script en `./scripts/docs.py` con el programa `python` directamente..

Pero también puedes usar <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, y obtendrás autocompletado en tu terminal para los comandos después de instalarlo.

Si instalas Typer CLI, puedes instalar la autocompletación con:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Estructura de la documentación

La documentación usa <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

Además, hay herramientas/scripts adicionales para manejar las traducciones en `./scripts/docs.py`.

/// Tip | Consejo

No necesitas ver el código en `./scripts/docs.py`, solo lo usas en la línea de comandos.

///

Toda la documentación está en formato Markdown en la carpeta `./docs/en/`.

Muchos de los tutoriales tienen bloques de código.

En la mayoría de los casos, estos bloques de código son aplicaciones completas que pueden ejecutarse tal cual.

De hecho, esos bloques de código no están escritos en Markdown, son archivos Python del directorio `./docs_src/`.

Y esos archivos Python se incluyen/inyectan en la documentación cuando se genera el sitio.

### Docs para los tests

Muchos de los tests en realidad se ejecutan contra los archivos de ejemplo de la documentación.

Esto ayuda a asegurarse de que:

* La documentación esté actualizada.
* Los ejemplos de documentación se pueden ejecutar tal cual.
* Muchas de las features están cubiertas en la documentación, aseguradas por los tests de cobertura.

#### Apps y docs al mismo tiempo

Si ejecutas los ejemplos, por ejemplo:

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>
como Uvicorn por defecto usa el puerto `8000`, la documentación en el puerto `8008` no entrará en conflicto.

### Traducciones
La ayuda con las traducciones es MUY apreciada! Y no sería posible sin el apoyo de la comunidad. 🌎 🚀

Aquí están los pasos para ayudar con las traducciones.

#### Tip | Consejos y guías

* Verifica los <a href="https://github.com/fastapi/fastapi/pulls" class="external-link" target="_blank">pull requests existentes</a> para tu idioma. Puedes filtar los pull requests por la label de tu idioma. Por ejemplo, para Español, la label es <a href="https://github.com/fastapi/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting-review" class="external-link" target="_blank">`lang-es`</a>.

* Revisa esos pull requests, solicitando cambios o aprobándolos. Para los lenguajes que no hablo, esperaré a que los otros revisen las traducciones antes de realizar el merge.

/// Tip | Consejo

Puedes <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">agregar comentarios con sugerencias de cambio</a> en un pull request existente.

Consulta la documentación acerca de <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank"> cómo agregar una revisión de pull request</a> para aprobarlo o pedir cambios.

///

* Verifica en <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussion</a> para coordinar traducciones en tu idioma. Puedes suscribirte a él, y cuando haya un nuevo pull request para revisar, un comentario automático será añadido a la discusión.

* Si traduces páginas, agrega un único pull request por cada página traducida. Esto hará mucho mas fácil de revisar para los demás.

* Consulta los códigos de 2 letras para el lenguaje que quieres traducir, puedes usar la tabla <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">Lista de códigos ISO 639-1</a>.

#### Idioma existente

Digamos que quieres traducir una página para un idioma que ya tiene traducciones para algunas páginas, como el Español.

En el caso del Español, el código de 2 letras sería `es`. Así que, el directorio para las traducciones en Español están ubicadas en `docs/es/`.

/// Tip | Consejo

El idioma principal ("oficial") es el inglés, y se encuentra ubicado en `docs/en/`.

///

Ahora ejecuta el live server para los documentos en español:

<div class="termy">

```console
// Usa el comando "live" y pásale el código de idioma como argumento en la CLI
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

/// Tip | Consejo

Alternativamente, puedes hacer los pasos de los scripts manualmente.

Ve al directorio del idioma, para las traducciones al Español sería en `docs/es/`:

```console
$ cd docs/es/
```
Entonces ejecuta `mkdocs` en ese directorio:


```console
$ mkdocs serve --dev-addr 8008
```

///

Ahora puedes ir a <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> y ver tus cambios en vivo.

Ahora puedes ver que cada lenguaje tiene todas las páginas. Pero algunas de las páginas no están traducidas y tienen un cuadro de información en la parte superior, advirtiendo de que hace falta la traducción.

Digamos que quieres añadir una traducción para la sección [Features](features.md){.internal-link target=_blank}.

* Copiar el archivo en:

```
docs/en/docs/features.md
```

* Pégalo exactamente en la misma ubicación pero en el lenguaje que quieres traducir, ej.:

```
docs/es/docs/features.md
```

/// Tip | Consejo

Nota que el único cambio en la ruta y el nombre del archivo es el código del idioma, de `en` a `es`.

///

Si vas a tu navegador vas a ver que ahora la documentación se muestra en tu nueva sección (el cuadro de información en la parte superior ha desaparecido). 🎉

Ahora puedes traducirlo todo y ver como se ve cuando guardas el archivo.

#### No traduzcas estás Páginas

🚨 No traducir:

* Archivos ubicados en `reference/`
* `release-notes.md`
* `fastapi-people.md`
* `external-links.md`
* `newsletter.md`
* `management-tasks.md`
* `management.md`

Algunos de estos archivos son actualizados muy frecuentemente y una traducción siempre estaría atrasada, o incluso incluyen el contenido principal en Inglés de los archivos fuente, etc.

#### Nuevo Idioma

Digamos que quieres agregar traducciones para un idioma que aún no está traducido, ni siquiera algunas páginas.

Digamos que quieres agregar traducciones para el Creole, y aún no está allí en la documentación.

Verificamos el link de arriba, el código para "Creole" es `ht`.

El siguiente paso sería ejecutar el script para generar un nuevo directorio de traducción:

<div class="termy">

```console
// Usa el comando new-lang, pásale el código de idioma como argumento en la CLI
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
```

</div>

Ahora puedes consultar en tu editor de código el nuevo directorio creado `docs/ht/`.

El comando creó un archivo `docs/ht/mkdocs.yml` con una configuración simple que hereda todo de la versión `en`:

```yaml
INHERIT: ../en/mkdocs.yml
```

/// Tip | Consejo

Además puedes simplemente crear ese archivo con esos contenidos manualmente.

///

Ese comando también creó un archivo "dummy" `docs/ht/index.md` para la página principal, puedes comenzar traduciendo esa.

Puedes continuar con las instrucciones anteriores para un "Idioma Existente" para ese proceso.

Puedes hacer el primer pull request con esos dos archivos, `docs/ht/mkdocs.yml` y `docs/ht/index.md`. 🎉

#### Revisa el resultado

Como ya se mencionó arriba, puedes user el `./scripts/docs.py` con el comando `live` para previsualizar los resultados (o `mkdocs serve`).

Una vez que estés listo, también puedes probarlo todo como se vería en línea, incluyendo todos los otros idiomas.

Para hacerlo, primero construye todas las documentaciones:

<div class="termy">

```console
// Usa el comando "build-all", esto llevará un rato
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>
Esto construye todos esos sitios independientes de MkDocs para cada idioma, los combina y genera el resultado final en `./site/`.

Entonces puedes servir eso con el comando `serve`:

<div class="termy">

```console
// Usa el comando "serve" después de ejecutar "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

#### Guías y Tip | Consejos específicos de traducción

* Traduce solo la documentación en Markdown (`.md`). No traducir los códigos de ejemplo ubicados en `./docs_src`.

* En bloques de código de la documentación en Markdown, traduce comentarios (`# un comentario`), pero deja el resto sin modificar.

* No cambies nada que esté entre "``" (inline code).

* En lineas que inicien con `///` traduce solo la parte del ` "... Text ..."`. Deja el resto sin modificar.

* Puedes traducir la información de los cuadros como `/// warning` como por ejemplo `/// warning | Achtung`. Pero no modifiques la palabra inmediatamente despues del `///`, esto determina el color de la caja de información.

* No modifiques las rutas de las imágenes, archivos de código, documentación en Markdown.

* Sin embargo, cuando un documento en Markdown es traducido, el `#hash-parts` los links a sus headings pueden cambiar. Actualiza esos links si es posible.
    * Busca esos links donde se tradujo el documento usando el regex `#[^# ]`.
    * Busca entre todos los documentos que ya se han traducido en su idioma por `tu-documento-traducido.md`. Por ejemplo VS Code tiene una opción "Edit" -> "Find in Files".
    * Cuando estés traduciendo un documento, no pre-traduzcas los `#hash-parts` que enlacen a encabezados que no tengan la documentación traducida.

## Tests

Hay un script que puedes ejecutar localmente para probar todo el código y generar informes de cobertura en HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Este comando genera un directorio `./htmlcov/`, si abres el archivo `./htmlcov/index.html` en tu navegador, podrás explorar interactivamente las regiones de código que están cubiertas por los tests y notar si hay alguna región que falta.

