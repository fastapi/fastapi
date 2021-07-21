# Desarrollo - Contribuciones

Si te interesa formar parte del proyecto, empieza por revisar las maneras de [apoyar a FastAPI y conseguir apoyo.](help-fastapi.md){.internal-link target=_blank}.

## Desarrollo

Si ya has copiado el repositorio y sabes con certeza que necesitas indagar a fondo del código fuente,
aquí encontrarás unas pautas a seguir con respecto a cómo desplegar tu entorno.



### Entorno virtual con `venv`

Puedes crear un entorno virtual utilizando el módulo de Python `venv` :

<div class="termy">

```console
$ python -m venv env
```

</div>

Eso creará un directorio con el nombre `./env/` con los archivos binarios de Python y a partir de ese momento podrás instalar
módulos y paquetes aislados del entorno global.

### Activa el entorno

Activa el entorno virtual, utilizando los comandos pertinentes a tu sistema operativo local:

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

    Or if you use Bash for Windows (e.g. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

    <div class="termy">

    ```console
    $ source ./env/Scripts/activate
    ```

    </div>

Para verificar que funciona:

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

Si el resultado demuestra `pip` binary at `env/bin/pip` entonces está en orden. ¡ Enhorabuena ! 🎉



!!! tip
    Siempre que quieras instalar un paquete en ese entorno utilizando pip, no olvides de activar el entorno de antemano.
    Así aseguras que cualquier programa de terminal instalado por ese paquete (por ejemplo `flit`), utilizará el instante local
    y no cualquier otro que puediera existir en el entorno global.


### Flit

**FastAPI** utiliza <a href="https://flit.readthedocs.io/en/latest/index.html" class="external-link" target="_blank">Flit</a> para
construir, empaquetar y publicar el proyecto.

Después de activar el entorno tal cómo hemos descrito, debes instalar `flit`:

<div class="termy">

```console
$ pip install flit

---> 100%
```

</div>

Vuelve a activar el entorno para asegurar que estás utilizando ese`flit` recién instalado,
 y no algún otro del entorno global.

Y ahora utilzas `flit` para installar las dependencias para el desarrollo:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ flit install --deps develop --symlink

    ---> 100%
    ```

    </div>

=== "Windows"

    If you are on Windows, use `--pth-file` instead of `--symlink`:

    <div class="termy">

    ```console
    $ flit install --deps develop --pth-file

    ---> 100%
    ```

    </div>

Se encargará de instalar en tu entorno un FastAPI local con todas sus dependencias.


#### Utilizando tu FastAPI local

Si fueras a crear un archivo de Python que utiliza FastAPI, y lo ejecutas desde tu entorno local,
se utilizará el código fuente de tu FastAPI local.

Y si fueras a actualizar el código fuente de ese FastAPI local, puesto que está instalado con `--symlink` (o `--pth-file` en Windows),
se utilizará esa versión modificada de FastAPI.

De esa forma, no hace falta instalar tu versión local para comprobar cada cambio.


### Formato

Existe un script que puedes ejectutar que se encarga de organizar y poner en orden tu código:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

y además, pondrá en orden alfabético las lista de modulos importados. Claro, para que funcione, es preciso tener FastAPI instalado en el entorno local utilizando
 `--symlink` (o bien`--pth-file` en Windows).

###  Formatear las lista de importaciones

Existe otro script que se encarga de formatear la lista de There is another script that formats all the imports and makes sure you don't have unused imports:

<div class="termy">

```console
$ bash scripts/format-imports.sh
```

</div>

Puesto que ejecuta comandos en secuencia y también modifica muchos ficheros, toma más tiempo. Puede resultar más fácil utilizar `scripts/format.sh`
frecuentemente y solamente `scripts/format-imports.sh` antes de someter.

## Docs

Lo primero es comprobar que tienes tu entorno tal como hemos descrito, así se instalarán todos los requisitos.

Los documentos se desarollan con <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.
También se encuentran utlidades para facilitar las traducciones en `./scripts/docs.py`.

!!! tip
    No hace falta aceder al código en `./scripts/docs.py`, simplemente lo utilizas desde la linea de comandos.

Todo el contenido de los documentos se encuentra en formato Markdown dentro del directorio `./docs/en/`. El texto en castellano se encuentra
en `./docs/es/`, según vaya progresando la traducción.

Muchos de los tutoriales incluyen bloques de código.

En la mayoría de los casos, los bloques son aplicaciones completas que se pueden ejecutar tal cual.

De hecho, esos bloques de código no se ecuentran dentro del Markdown, son ficheros de Python dentro del directorio `./docs_src/` .
Cuando el sitio es generado, esos ficheros se incluyen automáticamente.

### Docs for tests

La mayor parte de las pruebas se llevan a cabo contra los ejemplos de código en los documentos.


De esta forma se compreuba que:

* Los documentos están al día.
* Los ejemplos se pueden ejecutar tál como están.
* La mayoría de las prestaciones se describen en los documentos, aseguradas por pruebas de cobertura.

Durante el desarrollo local, se utiliza un script que construye el sitio y detecta cambios, recargando sobre la marcha.

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Sirve los documentos desde `http://127.0.0.1:8008`.
Así podras editar documentos y código fuente y ver los resultados en vivo.

#### Typer CLI (opcional)

Las siguentes instrucciones muestran cómo utilizar `./scripts/docs.py` con el programa `python` directamente.

Tambien puedes aprovechar <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, para obtener auto-completado.

Si instalas Typer CLI, puedes obtener auto-completado:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Aplicaciones y documentos a la vez

Si fueras a ejecutar los ejemplos :

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

como Uvicorn utiliza el puerto `8000` por defecto, los documentos en el puerto `8008` no chocarán.

### Traducciones

Se agradece muchísimo cualquier ayuda con las traducciones, puesto que es imposible hacerlas sin el apoyo de la comunidad. 🌎 🚀

Para ayuda con las traducciones, estos son los pasos a seguir.

#### Normas y Sugerencias

* Consulta la lista de <a href="https://github.com/tiangolo/fastapi/pulls" class="external-link" target="_blank">pull requests actuales</a> para tu idioma y aporta revisiones solicitando o aprobando cambios.

!!! tip
    Puedes <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">aportar comentarios con sugerencias</a> a pull requests actuales.

* Consulta los documentos acerca de <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">cómo aportar una reseña de pull request</a> para aprobar o solicitar cambios.

* Consulta la lista de <a href="https://github.com/tiangolo/fastapi/issues" class="external-link" target="_blank">issues</a> para determinar si hay alguien coordinando las traducciones para tu idioma.

* Crea un sólo pull request por página traducida, para facilitar las revisiones y reseñas.

Para aquellos idiomas que no puedo hablar, esperaré a que otros puedan revisar la traducción antes de incorporar.

* También puedes investigar si hay traducciones que puedas reseñar, asi me ayudarás a saber si la traducción está lista para incorporar.

* Sólo utiliza los ejemplos en los documentos y traduce el texto. No hace falta crear nada nuevo para que esto funcione.

* Utiliz las mismas imágenes, nombres de ficheros y enlaces. No hace falta cambiar nada para que funcione.

* Para determinar el código (de dos letras) para el idioma al que quieres traducir, puedes utilizar la tabla <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">List of ISO 639-1 codes</a>.

#### Un idioma existente

Supongamos que quisieras traducir a un idioma que ya tiene algunas páginas traducidas, como castellano.
En ese caso, el código de dos letras es `es`. Por tanto, el directorio para las traducciones castellanas se encuentra en `docs/es/`.

!!! tip
    El idioma principal ("oficial") es el inglés, situado en `docs/en/`.

Ahora puedes arrancar el servidor para los documentos en castellano.

<div class="termy">

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Para ver tus cambios sobre la marcha, visita <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a>.

Si consultas el sitio de documentos de FastAPI, que cada idioma tiene todas las páginas. Notarás que algunas páginas estan sin traducir y aparecen con un aviso acerca de la falta de traducción.

Sin embargo, cuando arrancas el servidor localmente, verás sólamente aquellas páginas ya traducidas.

Ahora, supongamos que quieras añadir una traducción para la sección [Features](features.md){.internal-link target=_blank}.

* Copia el fichero de:

```
docs/en/docs/features.md
```

* Pega el ficher en el mismo lugar, correspondiente al idioma al que quieres traducir, por ejemplo:

```
docs/es/docs/features.md
```

!!! tip
    Ten en cuenta que el único cambio en el destino es del código del idioma de `en` a `es`.

* Ahora, abre el fichero de configuración de MkDocs para inglés:

```
docs/en/docs/mkdocs.yml
```

* Busca el lugar donde se encuentra `docs/features.md` en la configuración. Algo parecido a este ejemplo:

```YAML hl_lines="8"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

* Y ahora abre el fichero donde se encuentra la configuración de MkDocs del idioma que vas a editar, por ejemplo:

```
docs/es/docs/mkdocs.yml
```

* Añade la referencia en la misma posición que está en el fichero de inglés.

```YAML hl_lines="8"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

Si existieran otras referencias, asegurate de conservar la misma secuencia que en la versión de inglés.

Si consultas tu buscador, verás que los documentos incluyen tu nueva sección. 🎉

Ahora podrás traducir el resto, ya verás cómo aparece según vayas progresando.

#### Un idioma nuevo: partiendo de zero

Digamos que quieras aportar traducciones para un idioma aún no traducido en ninguna de las páginas.

Supongamos que quieres aportart traducciones al criollo haitiano, y todavía no aparece en los documentos.

Consultando la tabla de códigos, veras que la secuencia para "Creole" es `ht`.

Lo sigiuente sería ejecutar el script que genera un nuevo directorio de traducciones:

<div class="termy">

```console
// Use the command new-lang, pass the language code as a CLI argument
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
Updating ht
Updating en
```

</div>

Now you can check in your code editor the newly created directory `docs/ht/`.
Ahora podrás ver el nuevo directorio  `docs/ht/` en tu editor.

!!! tip
    Crea el primer pull request con tan solo esto, incluso antes de añadir traducciones, para preparar la configuración del conjunto para el nuevo idioma.

    Asi otros podrán aportar cambios mientras traduces. 🚀

Comienza por traducir la página principal, `docs/ht/index.md`.

A partir de ahí, puedes seguir las instrucciones de la sección previa "Un idioma existente".

##### Un nuevo idioma no apoyado

Si fuera a aparecer un error con relación a la falta de apoyo para el idioma nuevo, por ejemplo:

```
 raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: partials/language/xx.html
```

quiere decir que el tema no apoya ese idioma (en este caso de debe al código inválido `xx`).

No te apures, puedes cambiar el idioma del tema a inglés y proceder a traducir el contenido de los documentos.
En ese case, edita el `mkdocs.yml` para tu nuevo idioma:

```YAML hl_lines="5"
site_name: FastAPI
# More stuff
theme:
  # More stuff
  language: xx
```

Cambia el código del `xx` al código de `en`.

Y vuelve a arrancar el servidor local.

#### Prever los resultados

Cuando ejectas el script `./scripts/docs.py` con el parámetro `live` sólo muestra los ficheros disponibles en el entorno local.

Cuando terminas, puedes comprobar como se va ver en línea si construyes el conjunto completo de documentos:

<div class="termy">

```console
// Use the command "build-all", this will take a bit
$ python ./scripts/docs.py build-all

Updating es
Updating en
Building docs for: en
Building docs for: es
Successfully built docs for: es
Copying en index.md to README.md
```

</div>

Ahora tienes el conjunto entero de todos los documentos bajo `./docs_build/` en todos los idiomas. Se incluyen también aquellos ficheros que carecen de traducción, con
una nota diciendo "this file doesn't have a translation yet". Ese directorio lo puedes ignorar.

Luego, el comando construye el sitio de MkDocs para cada idioma, los combina y finalmente produce las salida dentro de `./site/`.

A partir de entonces puedes servir el contenido utilizando `serve`:

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

## Pruebas

Existe un script que puedes ejecutar localmente para comprobar el código y generar informes de cobertura en HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Este comando crea un directorio `./htmlcov/`, si abres `./htmlcov/index.html` en tu buscador, puedes explorar interactivamente
 las regiones del código cubiertos por las pruebas y observar si falta alguna región.

### Pruebas dentro del editor

Si quieres utilizar las pruebas dentro del editor, debes añadir `./docs_src` a tu variable de `PYTHONPATH`.

Por ejemplo, en el case de VSCode, puedes crear un fichero  `.env` con el contenido:

```env
PYTHONPATH=./docs_src
```
