# Modelos de Parámetros Query

Si tienes un grupo de **parámetros query** que están relacionados, puedes crear un **modelo de Pydantic** para declararlos.

Esto te permitiría **reutilizar el modelo** en **múltiples lugares** y también declarar validaciones y metadatos para todos los parámetros de una vez. 😎

/// note | Nota

Esto es compatible desde la versión `0.115.0` de FastAPI. 🤓

///

## Parámetros Query con un Modelo Pydantic

Declara los **parámetros query** que necesitas en un **modelo de Pydantic**, y luego declara el parámetro como `Query`:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** **extraerá** los datos para **cada campo** de los **parámetros query** en el request y te proporcionará el modelo de Pydantic que definiste.

## Revisa la Documentación

Puedes ver los parámetros query en la UI de documentación en `/docs`:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Prohibir Parámetros Query Extras

En algunos casos de uso especiales (probablemente no muy comunes), podrías querer **restringir** los parámetros query que deseas recibir.

Puedes usar la configuración del modelo de Pydantic para `forbid` cualquier campo `extra`:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Si un cliente intenta enviar algunos datos **extra** en los **parámetros query**, recibirán un response de **error**.

Por ejemplo, si el cliente intenta enviar un parámetro query `tool` con un valor de `plumbus`, como:

```http
https://example.com/items/?limit=10&tool=plumbus
```

Recibirán un response de **error** que les indica que el parámetro query `tool` no está permitido:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Resumen

Puedes usar **modelos de Pydantic** para declarar **parámetros query** en **FastAPI**. 😎

/// tip | Consejo

Alerta de spoiler: también puedes usar modelos de Pydantic para declarar cookies y headers, pero leerás sobre eso más adelante en el tutorial. 🤫

///
