# Modelos de Parámetros Query { #query-parameter-models }

Si tienes un grupo de **parámetros query** que están relacionados, puedes crear un **modelo de Pydantic** para declararlos.

Esto te permitiría **reutilizar el modelo** en **múltiples lugares** y también declarar validaciones y metadatos para todos los parámetros de una vez. 😎

/// note | Nota

Esto es compatible desde la versión `0.115.0` de FastAPI. 🤓

///

## Parámetros Query con un Modelo Pydantic { #query-parameters-with-a-pydantic-model }

Declara los **parámetros query** que necesitas en un **modelo de Pydantic**, y luego declara el parámetro como `Query`:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI** **extraerá** los datos para **cada campo** de los **parámetros query** en el request y te proporcionará el modelo de Pydantic que definiste.

## Revisa la Documentación { #check-the-docs }

Puedes ver los parámetros query en la UI de documentación en `/docs`:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Prohíbe Parámetros Query Extras { #forbid-extra-query-parameters }

En algunos casos de uso especiales (probablemente no muy comunes), podrías querer **restringir** los parámetros query que deseas recibir.

Puedes usar la configuración del modelo de Pydantic para `forbid` cualquier campo `extra`:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Si un cliente intenta enviar algunos datos **extra** en los **parámetros query**, recibirá un response de **error**.

Por ejemplo, si el cliente intenta enviar un parámetro query `tool` con un valor de `plumbus`, como:

```http
https://example.com/items/?limit=10&tool=plumbus
```

Recibirá un response de **error** que le indica que el parámetro query `tool` no está permitido:

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

## Combina Modelos de Parámetros { #combine-parameter-models }

Puedes declarar múltiples modelos de parámetros query y combinarlos con parámetros query individuales o dependencias.

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

Los parámetros del request permanecen en el mismo nivel.

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

No hay claves `pagination` ni `filters` en el query string. Cada modelo valida los parámetros query de forma independiente, con sus propios valores por defecto, validadores de campos y validadores de modelo. Lo mismo se aplica cuando los modelos o los parámetros individuales se declaran en dependencias.

Si los modelos comparten un nombre de parámetro o un alias, cada modelo valida ese parámetro del request de forma independiente. Usa nombres o alias distintos para valores independientes. OpenAPI muestra un parámetro compartido una sola vez, como hace con los parámetros compartidos con dependencias, por lo que las declaraciones compartidas deben describir el mismo tipo y las mismas restricciones.

La configuración `extra` de cada modelo se aplica a todos los parámetros query, incluidos los declarados en otros modelos o dependencias. Con `extra="forbid"`, se rechaza cualquier parámetro ajeno a ese modelo. Con `extra="allow"`, esos parámetros se incluyen como extras del modelo.

Esto también funciona para los modelos de `Header` y `Cookie`.

## Modelos Opcionales de Parámetros Query { #optional-query-parameter-models }

Declara un modelo de parámetros query con `| None` y un valor por defecto de `None` para hacer que el grupo sea opcional.

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

Si no se envía ni `start` ni `end`, `date_range` es `None`. Si se envía cualquiera de los dos, FastAPI valida el modelo y requiere ambos campos.

Usar `| None` sin un valor por defecto sigue haciendo que el parámetro sea obligatorio.

Los parámetros extra siguen la configuración `extra` del modelo. Los extras ignorados no hacen que el modelo se considere presente.

OpenAPI muestra los campos del grupo individualmente y los marca como opcionales.

También puedes declarar [modelos de parámetros header](header-param-models.md#optional-header-parameter-models) y [modelos de parámetros cookie](cookie-param-models.md#optional-cookie-parameter-models) opcionales.

## Resumen { #summary }

Puedes usar **modelos de Pydantic** para declarar **parámetros query** en **FastAPI**. 😎

/// tip | Consejo

Alerta de spoiler: también puedes usar modelos de Pydantic para declarar cookies y headers, pero leerás sobre eso más adelante en el tutorial. 🤫

///
