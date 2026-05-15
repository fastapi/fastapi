# Modelos de Formulario { #form-models }

Puedes usar **modelos de Pydantic** para declarar **campos de formulario** en FastAPI.

/// info | Información

Para usar formularios, primero instala [`python-multipart`](https://github.com/Kludex/python-multipart).

Asegúrate de crear un [entorno virtual](../virtual-environments.md), activarlo, y luego instalarlo, por ejemplo:

```console
$ pip install python-multipart
```

///

/// note | Nota

Esto es compatible desde la versión `0.113.0` de FastAPI. 🤓

///

## Modelos de Pydantic para Formularios { #pydantic-models-for-forms }

Solo necesitas declarar un **modelo de Pydantic** con los campos que quieres recibir como **campos de formulario**, y luego declarar el parámetro como `Form`:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** **extraerá** los datos de **cada campo** de los **form data** en el request y te dará el modelo de Pydantic que definiste.

## Revisa la Documentación { #check-the-docs }

Puedes verificarlo en la interfaz de documentación en `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Prohibir Campos de Formulario Extra { #forbid-extra-form-fields }

En algunos casos de uso especiales (probablemente no muy comunes), podrías querer **restringir** los campos de formulario a solo aquellos declarados en el modelo de Pydantic. Y **prohibir** cualquier campo **extra**.

/// note | Nota

Esto es compatible desde la versión `0.114.0` de FastAPI. 🤓

///

Puedes usar la configuración del modelo de Pydantic para `forbid` cualquier campo `extra`:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

Si un cliente intenta enviar datos extra, recibirá un response de **error**.

Por ejemplo, si el cliente intenta enviar los campos de formulario:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

Recibirá un response de error indicando que el campo `extra` no está permitido:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Resumen { #summary }

Puedes usar modelos de Pydantic para declarar campos de formulario en FastAPI. 😎
