# Archivos de Request

Puedes definir archivos que serán subidos por el cliente utilizando `File`.

/// info | Información

Para recibir archivos subidos, primero instala <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, activarlo y luego instalarlo, por ejemplo:

```console
$ pip install python-multipart
```

Esto es porque los archivos subidos se envían como "form data".

///

## Importar `File`

Importa `File` y `UploadFile` desde `fastapi`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[3] *}

## Definir Parámetros `File`

Crea parámetros de archivo de la misma manera que lo harías para `Body` o `Form`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[9] *}

/// info | Información

`File` es una clase que hereda directamente de `Form`.

Pero recuerda que cuando importas `Query`, `Path`, `File` y otros desde `fastapi`, esos son en realidad funciones que devuelven clases especiales.

///

/// tip | Consejo

Para declarar cuerpos de File, necesitas usar `File`, porque de otra manera los parámetros serían interpretados como parámetros query o parámetros de cuerpo (JSON).

///

Los archivos se subirán como "form data".

Si declaras el tipo de tu parámetro de *path operation function* como `bytes`, **FastAPI** leerá el archivo por ti y recibirás el contenido como `bytes`.

Ten en cuenta que esto significa que todo el contenido se almacenará en memoria. Esto funcionará bien para archivos pequeños.

Pero hay varios casos en los que podrías beneficiarte de usar `UploadFile`.

## Parámetros de Archivo con `UploadFile`

Define un parámetro de archivo con un tipo de `UploadFile`:

{* ../../docs_src/request_files/tutorial001_an_py39.py hl[14] *}

Usar `UploadFile` tiene varias ventajas sobre `bytes`:

* No tienes que usar `File()` en el valor por defecto del parámetro.
* Usa un archivo "spooled":
    * Un archivo almacenado en memoria hasta un límite de tamaño máximo, y después de superar este límite, se almacenará en el disco.
* Esto significa que funcionará bien para archivos grandes como imágenes, videos, binarios grandes, etc. sin consumir toda la memoria.
* Puedes obtener metadatos del archivo subido.
* Tiene una interfaz `async` <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">parecida a un archivo</a>.
* Expone un objeto Python real <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> que puedes pasar directamente a otros paquetes que esperan un objeto parecido a un archivo.

### `UploadFile`

`UploadFile` tiene los siguientes atributos:

* `filename`: Un `str` con el nombre original del archivo que fue subido (por ejemplo, `myimage.jpg`).
* `content_type`: Un `str` con el tipo de contenido (MIME type / media type) (por ejemplo, `image/jpeg`).
* `file`: Un <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (un objeto <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">parecido a un archivo</a>). Este es el objeto de archivo Python real que puedes pasar directamente a otras funciones o paquetes que esperan un objeto "parecido a un archivo".

`UploadFile` tiene los siguientes métodos `async`. Todos ellos llaman a los métodos correspondientes del archivo por debajo (usando el `SpooledTemporaryFile` interno).

* `write(data)`: Escribe `data` (`str` o `bytes`) en el archivo.
* `read(size)`: Lee `size` (`int`) bytes/caracteres del archivo.
* `seek(offset)`: Va a la posición de bytes `offset` (`int`) en el archivo.
    * Por ejemplo, `await myfile.seek(0)` iría al inicio del archivo.
    * Esto es especialmente útil si ejecutas `await myfile.read()` una vez y luego necesitas leer el contenido nuevamente.
* `close()`: Cierra el archivo.

Como todos estos métodos son métodos `async`, necesitas "await" para ellos.

Por ejemplo, dentro de una *path operation function* `async` puedes obtener los contenidos con:

```Python
contents = await myfile.read()
```

Si estás dentro de una *path operation function* normal `def`, puedes acceder al `UploadFile.file` directamente, por ejemplo:

```Python
contents = myfile.file.read()
```

/// note | Detalles Técnicos de `async`

Cuando usas los métodos `async`, **FastAPI** ejecuta los métodos del archivo en un threadpool y los espera.

///

/// note | Detalles Técnicos de Starlette

El `UploadFile` de **FastAPI** hereda directamente del `UploadFile` de **Starlette**, pero añade algunas partes necesarias para hacerlo compatible con **Pydantic** y las otras partes de FastAPI.

///

## Qué es "Form Data"

La manera en que los forms de HTML (`<form></form>`) envían los datos al servidor normalmente utiliza una codificación "especial" para esos datos, es diferente de JSON.

**FastAPI** se asegurará de leer esos datos del lugar correcto en lugar de JSON.

/// note | Detalles Técnicos

Los datos de los forms normalmente se codifican usando el "media type" `application/x-www-form-urlencoded` cuando no incluyen archivos.

Pero cuando el formulario incluye archivos, se codifica como `multipart/form-data`. Si usas `File`, **FastAPI** sabrá que tiene que obtener los archivos de la parte correcta del cuerpo.

Si deseas leer más sobre estas codificaciones y campos de formularios, dirígete a la <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs para <code>POST</code></a>.

///

/// warning | Advertencia

Puedes declarar múltiples parámetros `File` y `Form` en una *path operation*, pero no puedes declarar campos `Body` que esperas recibir como JSON, ya que el request tendrá el cuerpo codificado usando `multipart/form-data` en lugar de `application/json`.

Esto no es una limitación de **FastAPI**, es parte del protocolo HTTP.

///

## Subida de Archivos Opcional

Puedes hacer un archivo opcional utilizando anotaciones de tipos estándar y estableciendo un valor por defecto de `None`:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## `UploadFile` con Metadatos Adicionales

También puedes usar `File()` con `UploadFile`, por ejemplo, para establecer metadatos adicionales:

{* ../../docs_src/request_files/tutorial001_03_an_py39.py hl[9,15] *}

## Subidas de Múltiples Archivos

Es posible subir varios archivos al mismo tiempo.

Estarían asociados al mismo "campo de formulario" enviado usando "form data".

Para usar eso, declara una lista de `bytes` o `UploadFile`:

{* ../../docs_src/request_files/tutorial002_an_py39.py hl[10,15] *}

Recibirás, como se declaró, una `list` de `bytes` o `UploadFile`s.

/// note | Detalles Técnicos

También podrías usar `from starlette.responses import HTMLResponse`.

**FastAPI** proporciona las mismas `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette.

///

### Subidas de Múltiples Archivos con Metadatos Adicionales

Y de la misma manera que antes, puedes usar `File()` para establecer parámetros adicionales, incluso para `UploadFile`:

{* ../../docs_src/request_files/tutorial003_an_py39.py hl[11,18:20] *}

## Recapitulación

Usa `File`, `bytes` y `UploadFile` para declarar archivos que se subirán en el request, enviados como form data.
