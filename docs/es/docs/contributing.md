# Desarrollo - Contribución

Primero, es posible que desees ver las formas básicas de [ayudar a FastAPI y obtener ayuda](help-fastapi.md){.internal-link target=_blank}.

## Desarrollo

Si ya clonaste el repositorio y sabes que necesitas sumergirte profundamente en el código, aquí tienes algunas pautas para configurar tu entorno.

### Entorno virtual con `venv`

Puedes crear un entorno virtual en un directorio utilizando el módulo `venv` de Python:


<div class="termy">

```console
$ python -m venv env
```

</div>

Eso creará un directorio `./env/` con los binarios de Python y luego podrás instalar paquetes para ese entorno aislado.

### Activar el entorno

Activa el nuevo entorno con:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ source ./env/bin/activate
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ .\env\Scripts\Activate.ps1
    ```

    </div>

=== "Windows Bash"

    O si usas Bash para Windows (p.ej. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

    <div class="termy">

    ```console
    $ source ./env/Scripts/activate
    ```

    </div>

Para comprobar que funcionó, usa:

=== "Linux, macOS, Windows Bash"

    <div class="termy">

    ```console
    $ which pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ Get-Command pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

Si muestra el binario `pip` en `env/bin/pip`, entonces funcionó. 🎉

Asegúrate de tener la última versión de `pip` en tu entorno virtual para evitar errores en los siguientes pasos:

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

!!! tip "Consejo"
    Cada vez que instales un nuevo paquete con `pip` en ese entorno, activa el entorno de nuevo.

    Esto se asegura de que si usas un programa de terminal instalado por ese paquete, uses el de tu entorno local y no cualquier otro que pueda estar instalado globalmente.

### pip

Después de activar el entorno como se describe arriba:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

Esto instalará todas las dependencias y tu FastAPI local en tu entorno local.

#### Usando tu FastAPI local

Si creas un archivo Python que importa y usa FastAPI, y lo ejecutas con el Python de tu entorno local, usará el código fuente local de FastAPI.

Y si actualizas ese código fuente local de FastAPI cuando ejecutes ese archivo Python de nuevo, usará la versión fresca de FastAPI que acabas de editar.

De esta manera, no tienes que "instalar" tu versión local para poder probar cada cambio.

!!! note "Detalles Técnicos"
    Esto sólo ocurre cuando instalas usando este `requirements.txt` incluido en lugar de instalar `pip install fastapi` directamente.

    Eso es porque dentro del archivo `requirements.txt`, la versión local de FastAPI está marcada para ser instalada en modo "editable", con la opción `-e`.

### Formato

Hay un script que puedes ejecutar que formateará y limpiará todo tu código:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

Esto también ordenará automáticamente todos tus imports.

Para que los ordene correctamente, necesitas tener FastAPI instalado localmente en tu entorno, con el comando de la sección anterior usando `-e`.

## Documentación

Primero, asegúrate de configurar tu entorno como se describe arriba, eso instalará todos los requisitos.

La documentación utiliza <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

Y hay herramientas/scripts adicionales para manejar las traducciones en `./scripts/docs.py`.

!!! tip "Consejo"
    No necesitas ver el código en `./scripts/docs.py`, sólo lo usas en la línea de comandos.

Toda la documentación está en formato Markdown en el directorio `./docs/en/`.

Muchos de los tutoriales tienen bloques de código.

En la mayoría de los casos, estos bloques de código son aplicaciones completas que se pueden ejecutar tal cual.

De hecho, esos bloques de código no están escritos dentro del Markdown, son archivos Python en el directorio `./docs_src/`.

Y esos archivos Python se incluyen/inyectan en la documentación al generar el sitio.

### Documentación para pruebas

La mayoría de las pruebas realmente se ejecutan contra los archivos de código de ejemplo en la documentación.

Esto ayuda a asegurar que:

* La documentación está actualizada.
* Los ejemplos de la documentación se pueden ejecutar tal cual.
* La mayoría de las características están cubiertas por la documentación, aseguradas por la cobertura de las pruebas.

Durante el desarrollo local, hay un script que construye el sitio y comprueba si hay cambios, recarga en vivo:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Servirá la documentación en http://127.0.0.1:8008.

De esta manera, puedes editar los archivos de documentación/fuente y ver los cambios en vivo.

!!! tip "Consejo"
    Alternativamente, puedes realizar los mismos pasos que el script hace manualmente.

    Ve al directorio del idioma, para la documentación principal en inglés está en `docs/en/`:

    ```console
    $ cd docs/en/
    ```

    Luego ejecuta `mkdocs` en ese directorio:

    ```console
    $ mkdocs serve --dev-addr 8008
    ```

#### Typer CLI (opcional)

Las instrucciones aquí te muestran cómo usar el script en `./scripts/docs.py` con el programa `python` directamente.

Pero también puedes usar <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, y obtendrás autocompletado en tu terminal para los comandos después de instalar la finalización.

Si instalas Typer CLI, puedes instalar la finalización con:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Aplicaciones y documentación al mismo tiempo

Si ejecutas los ejemplos con, por ejemplo:

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

como Uvicorn por defecto usará el puerto `8000`, la documentación en el puerto `8008` no chocará.

### Traducciones

¡La ayuda con las traducciones es MUY apreciada! Y no se puede hacer sin la ayuda de la comunidad. 🌎 🚀

Aquí están los pasos para ayudar con las traducciones.

<!-- #### Tips and guidelines -->
#### Consejos y guías

* Revisa las <a href="https://github.com/tiangolo/fastapi/pulls" class="external-link" target="_blank">pull requests existentes</a> para tu idioma y agrega revisiones solicitando cambios o aprobándolos.

!!! tip "Consejo"
    Puedes <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">agregar comentarios con sugerencias de cambios</a> a las pull requests existentes.

    Revisa la documentación sobre <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">cómo agregar una revisión de pull request</a> para aprobarla o solicitar cambios.

* Revisa las < href="https://github.com/tiangolo/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussions</a> para coordinar las traducciones para tu idioma. Puedes suscribirte a ella, y cuando haya una nueva pull request para revisar, se agregará un comentario automático a la discusión.

* Agrega una sola pull request por página traducida. Eso hará que sea mucho más fácil para otros revisarla.

Para los idiomas que no hablo, esperaré a que varios otros revisen la traducción antes de fusionarla.

* También puedes revisar si hay traducciones para tu idioma y agregar una revisión a ellas, eso me ayudará a saber que la traducción es correcta y puedo fusionarla.
    * Puedes revisar en las <a href="https://github.com/tiangolo/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussions</a> para tu idioma.
    * O puedes filtrar las PR existentes por las que tienen la etiqueta para tu idioma, por ejemplo, para español, la etiqueta es <a href="https://github.com/tiangolo/fastapi/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3A%22awaiting+review%22" class="external-link" target="_blank">`lang-es`</a>.

* Usa los mismos ejemplos de Python y solo traduce el texto en la documentación. No tienes que cambiar nada para que funcione.

* Usa las mismas imágenes, nombres de archivos y enlaces. No tienes que cambiar nada para que funcione.

* Para verificar el código de 2 letras para el idioma que deseas traducir, puedes usar la tabla <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">List of ISO 639-1 codes</a>.

#### Idioma existente

Digamos que quieres traducir una página para un idioma que ya tiene traducciones para algunas páginas, como el español.

En el caso del español, el código de 2 letras es `es`. Entonces, el directorio para las traducciones en español se encuentra en `docs/es/`.

!!! tip "Consejo"
    El idioma principal ("oficial") es el inglés, ubicado en `docs/en/`.

<div class="termy">

```console
// Usa el comando "live" y pasa el código de idioma como argumento de CLI
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

!!! tip "Consejo"
    Alternativamente, puedes realizar los mismos pasos que hace el script manualmente.

    Ve al directorio del idioma, para las traducciones en español está en `docs/es/`:

    ```console
    $ cd docs/es/
    ```

    Luego ejecuta `mkdocs` en ese directorio:

    ```console
    $ mkdocs serve --dev-addr 8008
    ```

Ahora puedes ir a <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> y ver tus cambios en vivo.

Verás que cada idioma tiene todas las páginas. Pero algunas páginas no están traducidas y tienen una notificación sobre la traducción faltante.

Ahora digamos que quieres agregar una traducción para la sección [Características](features.md){.internal-link target=_blank}.

* Copia el archivo en:

```
docs/en/docs/features.md
```

* Pégalo en exactamente la misma ubicación pero para el idioma que deseas traducir, por ejemplo:

```
docs/es/docs/features.md
```

!!! tip "Consejo"
    Nota que el único cambio en la ruta y el nombre del archivo es el código de idioma, de `en` a `es`.

Si vas a tu navegador verás que ahora la documentación muestra tu nueva sección. 🎉

Ahora puedes traducirlo todo y ver cómo se ve a medida que guardas el archivo.

#### Nuevo idioma

Digamos que quieres agregar traducciones para un idioma que aún no está traducido, ni siquiera algunas páginas.

Digamos que quieres agregar traducciones para el criollo, y aún no está allí en la documentación.

Revisando el enlace de arriba, el código para "Criollo" es `ht`.

El siguiente paso es ejecutar el script para generar un nuevo directorio de traducción:

<div class="termy">

```console
// Usa el comando "new-lang" y pasa el código de idioma como argumento de CLI
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
```

</div>

A continuación, puede verificar en su editor de código el directorio recién creado `docs/ht/`.

Ese comando creó un archivo `docs/ht/mkdocs.yml` con una configuración simple que hereda todo de la versión `en`:

```yaml
INHERIT: ../en/mkdocs.yml
```

!!! tip "Consejo"
    También podría simplemente crear ese archivo con esos contenidos manualmente.

Ese comando también creó un archivo ficticio `docs/ht/index.md` para la página principal, puede comenzar traduciendo ese.

Puede continuar con las instrucciones anteriores para un "Idioma existente" para ese proceso.

Puede hacer la primera solicitud de extracción con esos dos archivos, `docs/ht/mkdocs.yml` y `docs/ht/index.md`. 🎉

#### Vista previa del resultado

Puede usar `./scripts/docs.py` con el comando `live` para obtener una vista previa de los resultados (o `mkdocs serve`).

Una vez que haya terminado, también puede probar todo como si estuviera en línea, incluidos todos los demás idiomas.

Para hacer eso, primero construya todos los documentos:

<div class="termy">

```console
// Use el comando "build-all", esto tomará un poco
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>


Esto construye todos esos sitios MkDocs independientes para cada idioma, los combina y genera la salida final en `./site/`.

Luego puede servir eso con el comando `serve`:

<div class="termy">

```console
// Use el comando "serve" después de ejecutar "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

## Pruebas

Hay un script que puedes ejecutar localmente para probar todo el código y generar informes de cobertura en HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Este comando genera un directorio `./htmlcov/`, si abres el archivo `./htmlcov/index.html` en tu navegador, puedes explorar de forma interactiva las regiones de código que están cubiertas por las pruebas, y notar si hay alguna región que falte.
