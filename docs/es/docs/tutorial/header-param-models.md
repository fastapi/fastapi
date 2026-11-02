# Modelos de Parámetros de Header { #header-parameter-models }

Si tienes un grupo de **parámetros de header** relacionados, puedes crear un **modelo Pydantic** para declararlos.

Esto te permitirá **reutilizar el modelo** en **múltiples lugares** y también declarar validaciones y metadatos para todos los parámetros al mismo tiempo. 😎

/// note | Nota

Esto es compatible desde la versión `0.115.0` de FastAPI. 🤓

///

## Parámetros de Header con un Modelo Pydantic { #header-parameters-with-a-pydantic-model }

Declara los **parámetros de header** que necesitas en un **modelo Pydantic**, y luego declara el parámetro como `Header`:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** **extraerá** los datos para **cada campo** de los **headers** en el request y te dará el modelo Pydantic que definiste.

## Revisa la Documentación { #check-the-docs }

Puedes ver los headers requeridos en la interfaz de documentación en `/docs`:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Prohíbe Headers Extra { #forbid-extra-headers }

En algunos casos de uso especiales (probablemente no muy comunes), podrías querer **restringir** los headers que deseas recibir.

Puedes usar la configuración del modelo de Pydantic para prohibir (`forbid`) cualquier campo `extra`:

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

## Desactiva la conversión de guiones bajos { #disable-convert-underscores }

De la misma forma que con los parámetros de header normales, cuando tienes caracteres de guion bajo en los nombres de los parámetros, se **convierten automáticamente en guiones**.

Por ejemplo, si tienes un parámetro de header `save_data` en el código, el header HTTP esperado será `save-data`, y aparecerá así en la documentación.

Si por alguna razón necesitas desactivar esta conversión automática, también puedes hacerlo para los modelos Pydantic de parámetros de header.

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | Advertencia

Antes de establecer `convert_underscores` a `False`, ten en cuenta que algunos proxies y servidores HTTP no permiten el uso de headers con guiones bajos.

///

## Combina Modelos de Parámetros { #combine-parameter-models }

Puedes combinar múltiples modelos de parámetros de header con parámetros de header individuales y dependencias. Cada modelo se extrae y se valida de forma independiente, como se explica para los [modelos de parámetros de query](query-param-models.md#combine-parameter-models).

La configuración `extra` de cada modelo se aplica a todos los parámetros de header, incluidos los declarados en otros modelos o dependencias. Con `extra="forbid"`, se rechaza cualquier header que no forme parte de ese modelo. Con `extra="allow"`, esos headers se incluyen como campos extra del modelo.

Cada modelo usa su propia configuración `Header(convert_underscores=...)`, tanto al leer el request como al generar OpenAPI. Los alias explícitos de los campos se mantienen como nombres literales de headers.

## Modelos Opcionales de Parámetros de Header { #optional-header-parameter-models }

Declara un modelo de parámetros de header con `| None` y un valor por defecto de `None` para que el grupo sea opcional.

{* ../../docs_src/header_param_models/tutorial004_an_py310.py hl[15] *}

Si no se envía ni `x-client-name` ni `x-client-version`, `client` es `None`. Si se envía cualquiera de los dos, FastAPI valida el modelo y requiere ambos campos.

Se aplican las mismas reglas para los valores por defecto, los campos extra y OpenAPI que para los [modelos opcionales de parámetros de query](query-param-models.md#optional-query-parameter-models).

Los headers como `Host` también siguen la configuración `extra` del modelo. Con `extra="allow"`, hacen que el modelo esté presente incluso si no se proporciona ninguno de los campos declarados.

## Resumen { #summary }

Puedes usar **modelos Pydantic** para declarar **headers** en **FastAPI**. 😎
