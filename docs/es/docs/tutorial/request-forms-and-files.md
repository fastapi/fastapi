# Formularios y archivos del request { #request-forms-and-files }

Puedes definir archivos y campos de formulario al mismo tiempo usando `File` y `Form`.

/// info | Información

Para recibir archivos subidos y/o form data, primero instala <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, actívalo y luego instálalo, por ejemplo:

```console
$ pip install python-multipart
```

///

## Importa `File` y `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## Define parámetros `File` y `Form` { #define-file-and-form-parameters }

Crea parámetros de archivo y formulario de la misma manera que lo harías para `Body` o `Query`:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

Los archivos y campos de formulario se subirán como form data y recibirás los archivos y campos de formulario.

Y puedes declarar algunos de los archivos como `bytes` y algunos como `UploadFile`.

/// warning | Advertencia

Puedes declarar múltiples parámetros `File` y `Form` en una *path operation*, pero no puedes también declarar campos `Body` que esperas recibir como JSON, ya que el request tendrá el body codificado usando `multipart/form-data` en lugar de `application/json`.

Esto no es una limitación de **FastAPI**, es parte del protocolo HTTP.

///

## Resumen { #recap }

Usa `File` y `Form` juntos cuando necesites recibir datos y archivos en el mismo request.
