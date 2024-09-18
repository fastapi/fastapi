# Response - Cambiar el Status Code

Probablemente ya has leído con anterioridad que puedes establecer un [Response Status Code](../tutorial/response-status-code.md){.internal-link target=_blank} por defecto.

Pero en algunos casos necesitas retornar un status code diferente al predeterminado.

## Casos de uso

Por ejemplo, imagina que quieres retornar un HTTP status code de "OK" `200` por defecto.

Pero si los datos no existen, quieres crearlos y retornar un HTTP status code de "CREATED" `201`.

Pero aún quieres poder filtrar y convertir los datos que retornas con un `response_model`.

Para esos casos, puedes usar un parámetro `Response`.

## Usar un parámetro `Response`

Puedes declarar un parámetro de tipo `Response` en tu *función de la operación de path* (como puedes hacer para cookies y headers).

Y luego puedes establecer el `status_code` en ese objeto de respuesta *temporal*.

```Python hl_lines="1  9  12"
{!../../../docs_src/response_change_status_code/tutorial001.py!}
```

Y luego puedes retornar cualquier objeto que necesites, como normalmente lo harías (un `dict`, un modelo de base de datos, etc).

Y si declaraste un `response_model`, aún se usará para filtrar y convertir el objeto que retornaste.

**FastAPI** usará esa respuesta *temporal* para extraer el código de estado (también cookies y headers), y los pondrá en la respuesta final que contiene el valor que retornaste, filtrado por cualquier `response_model`.

También puedes declarar la dependencia del parámetro `Response`, y establecer el código de estado en ellos. Pero ten en cuenta que el último en establecerse será el que gane.
