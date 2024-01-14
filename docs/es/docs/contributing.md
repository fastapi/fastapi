# Desarrollo - Contribuyendo

En primer lugar, es posible que desee ver las formas básicas de [ayudar a FastAPI y obtener ayuda](help-fastapi.md){.internal-link target=_blank}.

## Desarrollando

Si ya clonaste el <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">repositorio fastapi</a> y quieres adentrarte en el código, aquí hay algunas pautas para configurar su entorno.

### Entorno virtual con `venv`

Puede crear un entorno local virtual aislado en un directorio utilizando el módulo `venv` de Python. Hagamos esto en el repositorio clonado (donde está `requirements.txt`):

<div class="termy">

```console
$ python -m venv env
```

</div>

Eso creará un directorio `./env/` con los binarios de Python, y luego podrá instalar paquetes para ese entorno local.

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

    O si usas Bash para Windows (por ejemplo, <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

    <div class="termy">

    ```console
    $ source ./env/Scripts/activate
    ```

    </div>

Para verificar que funcionó, usa:

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

Asegúrate de tener la última versión de pip en su entorno local para evitar errores en los siguientes pasos:

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

!!! tip "Consejo"
    Cada vez que instales un nuevo paquete con `pip` en ese entorno, activa el entorno nuevamente.

    Esto asegura que si usas un programa de la terminal instalado por ese paquete, usa el de tu entorno local y no cualquier otro que pueda instalarse globalmente.

### Instalar requerimientos utilizando pip

Después de activar el entorno como se describe arriba:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

Esto instalará todas las dependencias y tu FastAPI local en tu entorno local.

### Utilizando tu FastAPI local

Si creas un archivo Python que importa y usa FastAPI, y lo ejecutas con Python desde tu entorno local, usará tu código fuente local clonado de FastAPI.

Y si actualizas ese código fuente local de FastAPI cuando vuelvas a ejecutar ese archivo Python, utilizará la versión nueva de FastAPI que acabas de editar.

De esa manera, no tendrás que "instalar" tu versión local para poder probar cada cambio.

!!! note "Detalles Técnicos"
    Esto solo sucede cuando realizas la instalación utilizando el `requirements.txt` incluido en lugar de ejecutar `pip install fastapi` directamente.

    Esto se debe a que dentro del archivo `requirements.txt`, la versión local de FastAPI está marcada para instalarse en modo "editable", con la opción `-e`.

### Formatear el código

Hay un script que puedes ejecutar y que formateará y limpiará todo tu código:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

También ordenará automáticamente todas tus importaciones.

Para ordenarlos correctamente, necesitas tener FastAPI instalado localmente en tu entorno, con el comando de la sección anterior usando `-e`.

## Documentación

Primero, asegúrese de configurar su entorno como se describe anteriormente, eso instalará todos los requisitos.

### Documentación en vivo

Durante el desarrollo local, hay un script que construye el sitio y verifica si hay cambios, recargando en vivo:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Servirá la documentación en `http://127.0.0.1:8008`.

De esa manera, puedes editar los archivos de documentación/código fuente y ver los cambios en vivo.

!!! tip "Consejo"
    Alternativamente, puedes realizar los mismos pasos que los scripts realizan manualmente.

    Ve al directorio de idiomas, para los documentos principales en inglés en `docs/en/`:

    ```console
    $ cd docs/en/
    ```

    Luego ejecuta `mkdocs` en ese directorio:

    ```console
    $ mkdocs serve --dev-addr 8008
    ```

#### Typer CLI (opcional)

Las instrucciones aquí te muestran cómo utilizar el script en `./scripts/docs.py` directamente con el programa `python`.

Pero también puedes usar <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a> y obtendrás el autocompletado en tu terminal para ver los comandos después de instalar el completamiento.

Si instalas Typer CLI, puedes instalar el completamiento con:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Estructura de la Documentación

La documentación utiliza <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

Y hay herramientas/scripts adicionales para manejar las traducciones en `./scripts/docs.py`.

!!! tip "Consejo"
    No necesitas ver el código en `./scripts/docs.py`, solo úsalo en la línea de comando.

Toda la documentación está en formato Markdown en el directorio. `./docs/en/`.

Muchos de los tutoriales tienen bloques de código.

En la mayoría de los casos, estos bloques de código son aplicaciones reales completas que se pueden ejecutar tal cual.

De hecho, esos bloques de código no están escritos dentro de Markdown, son archivos de Python en el directorio `./docs_src/`.

Y esos archivos Python se incluyen/inyectan en la documentación cuando se genera el sitio.

### Documentación para las pruebas

La mayoría de las pruebas en realidad se ejecutan con los archivos de código fuente de ejemplo en la documentación.

Esto ayuda a garantizar que:

*La documentación está actualizada.
* Los ejemplos de documentación se pueden ejecutar tal cual.
* La mayoría de las características están cubiertas por la documentación, garantizado por la cobertura de las pruebas.

#### Aplicaciones y documentación al mismo tiempo

Si ejecuta los ejemplos con, ej.:

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

como Uvicorn utilizará por defecto el puerto `8000`, la documentación sobre el puerto `8008` no entrará en conflicto.

### Traducciones

¡Se agradece MUCHO la ayuda con las traducciones! Y no se puede hacer sin la ayuda de la comunidad. 🌎 🚀

Estos son los pasos para ayudar con las traducciones.

#### Consejos y recomendaciones

* Verifica los <a href="https://github.com/tiangolo/fastapi/pulls" class="external-link" target="_blank">pull requests existentes</a> actualmente para tu idioma. Puedes filtrar los pull requests por aquellas que tienen la etiqueta para tu idioma. Por ejemplo, para español, la etiqueta es <a href="https://github.com/tiangolo/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting- revisión" class="external-link" target="_blank">`lang-es`</a>.

* Revisa esos pull request, solicitando cambios o aprobándolos. Para los idiomas que no hablo, esperaré a que otros revisen la traducción antes de fusionarlos.

!!! tip "Consejo"
    Puedes <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">agregar comentarios con sugerencias de cambios</a> a los pull requests existentes.

    Consulta las documentación sobre <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">agregar una revisión de pull request</a> para aprobar o solicitar cambios.

* Comprueba si hay una <a href="https://github.com/tiangolo/fastapi/discussions/categories/translations" class="external-link" target="_blank">Discusión de GitHub</a> para coordinar las traducciones de tu idioma. Puedes suscribirte y, cuando haya un nuevo pull request para revisar, se agregará un comentario automático a la discusión.

* Si traduces páginas, agrega un único pull request por página traducida. Eso hará que sea mucho más fácil para otros revisarlo.

* Para comprobar el código de 2 letras del idioma que deseas traducir, puedes utilizar la tabla <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target ="_blank">Lista de códigos ISO 639-1</a>.

#### Idioma existente

Digamos que deseas traducir una página a un idioma que ya tiene traducciones para algunas páginas, como el Español.

En el caso del Español, el código de 2 letras es `es`. Entonces, el directorio de traducciones al español se encuentra en `docs/es/`.

!!! tip "Consejo"
    El idioma principal ("oficial") es Inglés, localizado en `docs/en/`.

Ahora ejecuta el servidor para la documentación en vivo en Español:

<div class="termy">

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

!!! tip "Consejo"
    Alternativamente, puedes realizar los mismos pasos que los scripts manualmente.

    Vaya al directorio de idiomas, para las traducciones al Español están en `docs/es/`:

    ```console
    $ cd docs/es/
    ```

    Luego ejecuta `mkdocs` en ese directorio:

    ```console
    $ mkdocs serve --dev-addr 8008
    ```

Ahora puedes ir a <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> y ver tus cambios en vivo.

Verás que cada idioma tiene todas las páginas. Pero algunas páginas no están traducidas y tienen un cuadro de información en la parte superior sobre la traducción faltante.

Ahora digamos que quieres agregar una traducción para la sección [Características](features.md){.internal-link target=_blank}.

* Copia el fichero en:

```
docs/en/docs/features.md
```

* Pégalo exactamente en la misma ubicación pero para el idioma que deseas traducir, por ejemplo:

```
docs/es/docs/features.md
```

!!! tip "Consejo"
    Observa que el único cambio en la ruta y el nombre del archivo es el código de idioma, de `en` a `es`.

Si vas a tu navegador, verás que ahora la documentación muestran tu nueva sección (el cuadro de información en la parte superior desapareció). 🎉

Ahora puedes traducirlo todo y ver cómo queda al guardar el archivo.

#### Idioma nuevo

Digamos que deseas agregar traducciones para un idioma que aún no está traducido, ni siquiera algunas páginas.

Supongamos que desea agregar traducciones para Creole y aún no está en la documentación.

Verificando el enlace de arriba, el código para "Creole" es `ht`.

El siguiente paso es ejecutar el script para generar un nuevo directorio de traducción:

<div class="termy">

```console
// Use the command new-lang, pass the language code as a CLI argument
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
```

</div>

Ahora puedes consultar en tu editor de código el directorio recién creado. `docs/ht/`.

Ese comando creó un archivo `docs/ht/mkdocs.yml` con una configuración simple que hereda todo de la versión `en`:

```yaml
INHERIT: ../en/mkdocs.yml
```

!!! tip "Consejo"
    También puedes simplemente crear ese archivo con ese contenido manualmente.

Ese comando también creó un archivo dummy `docs/ht/index.md` para la página principal, puedes comenzar traduciendo ese.

Puede continuar con las instrucciones anteriores para un "Idioma existente" para ese proceso.

Puedes hacer el primer pull request con estos dos archivos, `docs/ht/mkdocs.yml` y `docs/ht/index.md`. 🎉

#### Previsualizar el resultado

Como ya se mencionó anteriormente, puedes utilizar `./scripts/docs.py` con el comando `live` para obtener una vista previa de los resultados (o `mkdocs serve`).

Una vez que hayas terminado, también puedes probarlo todo tal como se vería en línea, incluidos todos los demás idiomas.

Para hacer eso, primero crea todas las documentaciones:

<div class="termy">

```console
// Use the command "build-all", this will take a bit
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>

Esto crea todos esos sitios MkDocs independientes para cada idioma, los combina y genera el resultado final en `./site/`.

Entonces puedes servir eso con el comando `serve`:

<div class="termy">

```console
// Use the command "serve" after running "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

#### Consejos y pautas específicas de traducción

* Traduce sólo los documentos Markdown (`.md`). No traduce los ejemplos de código en `./docs_src`.

* En bloques de código dentro del documento Markdown, traduce los comentarios ("# un comentario"), pero deje el resto sin cambios.

* No cambie nada incluido en "``" (código en línea).

* En líneas que comienzan con `===` o `!!!`, traduce solo la parte ` "... Texto ..."`. Deja el resto sin cambios.

* Puedes traducir cuadros de información como `!!! warning` con por ejemplo `!!! warning "Alerta"`. Pero no cambies la palabra inmediatamente después de `!!!`, ya que determina el color del cuadro de información.

* No cambies las rutas en enlaces a imágenes, archivos de código, documentos Markdown.

* Sin embargo, cuando se traduce un documento de Markdown, las `#hash-parts` en los enlaces a sus encabezados pueden cambiar. Actualiza estos enlaces si es posible.
     * Busca dichos enlaces en el documento traducido utilizando la expresión regular `#[^# ]`.
     * Busca en todos los documentos ya traducidos a su idioma `su-documento-traducido.md`. Por ejemplo, VS Code tiene una opción "Editar" -> "Buscar en archivos".
     * Al traducir un documento, no "traduzcas previamente" `#hash-parts` que enlacen a encabezados en documentos no traducidos.

## Pruebas

Existe un script que puedes ejecutar localmente para probar todo el código y generar informes de cobertura en HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Este comando genera un directorio `./htmlcov/`, si abre el archivo `./htmlcov/index.html` en tu navegador, puedes explorar interactivamente las regiones de código que están cubiertas por las pruebas y observar si hay falta alguna región.
