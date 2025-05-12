# Modelos de Parámetros de Header

Si tienes un grupo de **parámetros de header** relacionados, puedes crear un **modelo Pydantic** para declararlos.

Esto te permitirá **reutilizar el modelo** en **múltiples lugares** y también declarar validaciones y metadatos para todos los parámetros al mismo tiempo. 😎

/// note | Nota

Esto es compatible desde la versión `0.115.0` de FastAPI. 🤓

///

## Parámetros de Header con un Modelo Pydantic

Declara los **parámetros de header** que necesitas en un **modelo Pydantic**, y luego declara el parámetro como `Header`:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** **extraerá** los datos para **cada campo** de los **headers** en el request y te dará el modelo Pydantic que definiste.

## Revisa la Documentación

Puedes ver los headers requeridos en la interfaz de documentación en `/docs`:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Prohibir Headers Extra

En algunos casos de uso especiales (probablemente no muy comunes), podrías querer **restringir** los headers que deseas recibir.

Puedes usar la configuración del modelo de Pydantic para `prohibir` cualquier campo `extra`:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

Si un cliente intenta enviar algunos **headers extra**, recibirán un response de **error**.

Por ejemplo, si el cliente intenta enviar un header `tool` con un valor de `plumbus`, recibirán un response de **error** indicando que el parámetro de header `tool` no está permitido:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Resumen

Puedes usar **modelos Pydantic** para declarar **headers** en **FastAPI**. 😎
