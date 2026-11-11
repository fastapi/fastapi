# Modelos de Formulario { #form-models }

Puedes usar **modelos de Pydantic** para declarar **campos de formulario** en FastAPI.

/// note | Nota

Para usar formularios, primero instala [`python-multipart`](https://github.com/Kludex/python-multipart).

Agrégalo a tu proyecto:

```console
$ uv add python-multipart
```

///

/// note | Nota

Esto es compatible desde la versión `0.113.0` de FastAPI. 🤓

///

## Modelos de Pydantic para Formularios { #pydantic-models-for-forms }

Solo necesitas declarar un **modelo de Pydantic** con los campos que quieres recibir como **campos de formulario**, y luego declarar el parámetro como `Form`:

{* ../../docs_src/request_form_models/tutorial001.py hl[9:11,15] *}

**FastAPI** **extraerá** los datos de **cada campo** de los **form data** en el request y te dará el modelo de Pydantic que definiste.

Para las [casillas de verificación HTML](request-forms.md#boolean-form-fields), declara campos booleanos con un valor por defecto de `False`.

## Revisa la Documentación { #check-the-docs }

Puedes verificarlo en la interfaz de documentación en `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Prohíbe Campos de Formulario Extra { #forbid-extra-form-fields }

En algunos casos de uso especiales (probablemente no muy comunes), podrías querer **restringir** los campos de formulario a solo aquellos declarados en el modelo de Pydantic. Y **prohibir** cualquier campo **extra**.

/// note | Nota

Esto es compatible desde la versión `0.114.0` de FastAPI. 🤓

///

Puedes usar la configuración del modelo de Pydantic para `forbid` cualquier campo `extra`:

{* ../../docs_src/request_form_models/tutorial002.py hl[12] *}

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

## Combina Modelos de Formulario { #combine-form-models }

Puedes combinar varios modelos de formulario con parámetros `Form` individuales.

{* ../../docs_src/request_form_models/tutorial003.py hl[9:14,19:21] *}

El cliente envía `name`, `tags` y `token` como campos de formulario. Cada modelo valida los campos de formulario de forma independiente.

La configuración `extra` de cada modelo se aplica a todos los campos de formulario, incluidos los campos y archivos declarados en otros parámetros o dependencias. Con `extra="forbid"`, se rechaza cualquier campo que no forme parte de ese modelo. Con `extra="allow"`, esos campos se incluyen como campos extra del modelo.

Si varias declaraciones usan el mismo nombre de campo de formulario, cada una valida el valor de ese campo. Usa tipos y restricciones compatibles para los campos compartidos, de modo que el esquema OpenAPI pueda describirlos de forma coherente.

## Modelos de Formulario Opcionales { #optional-form-models }

Declara un modelo de formulario con `| None` y un valor por defecto de `None` para hacer que el grupo sea opcional.

{* ../../docs_src/request_form_models/tutorial005.py hl[17] *}

Si no se envía ni `name` ni `age`, `profile` es `None`. Si se envía cualquiera de los dos, FastAPI valida el modelo y requiere ambos campos. Enviar un valor vacío también cuenta como proporcionar un campo.

Usar `| None` sin un valor por defecto sigue haciendo que el parámetro sea obligatorio.

Los campos extra siguen la configuración `extra` del modelo. Los campos extra ignorados no hacen que el modelo se considere presente.

Un modelo opcional que solo contiene casillas de verificación sin marcar se omite. Envía un valor como `enabled=false` para proporcionarlo explícitamente.

## Uniones Opcionales de Modelos de Formulario { #optional-unions-of-form-models }

También puedes usar una unión opcional de modelos.

{* ../../docs_src/request_form_models/tutorial006.py hl[9:16,21] *}

Si no se envían campos de formulario, `contact` es `None`. Envía `kind=person` con `name`, o `kind=company` con `company_name`. El discriminador selecciona qué modelo validar.

## Combina Uniones de Modelos de Formulario { #combine-unions-of-form-models }

Puedes combinar uniones con otros modelos de formulario, parámetros `Form` individuales y parámetros `File`. Cada unión se valida de forma independiente.

{* ../../docs_src/request_form_models/tutorial007.py hl[31:35] *}

Envía todos los campos en el mismo formulario. Por ejemplo, envía `contact_type=person`, `name=Rick`, `notification_type=email`, `email=rick@example.com` y `token=secret`.

Omite los campos de notificación para dejar `notification` como `None`.

## Modelos de Formulario y Archivos { #form-models-and-files }

También puedes combinar un modelo de formulario con [parámetros de archivo](request-files.md).

{* ../../docs_src/request_form_models/tutorial004.py hl[14] *}

Aquí el cliente envía el campo `name` y el archivo `avatar` usando `multipart/form-data`.

## Resumen { #summary }

Puedes usar modelos de Pydantic para declarar campos de formulario en FastAPI. 😎
