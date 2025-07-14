# Response - Cambiar Código de Estado

Probablemente leíste antes que puedes establecer un [Código de Estado de Response](../tutorial/response-status-code.md){.internal-link target=_blank} por defecto.

Pero en algunos casos necesitas devolver un código de estado diferente al predeterminado.

## Caso de uso

Por ejemplo, imagina que quieres devolver un código de estado HTTP de "OK" `200` por defecto.

Pero si los datos no existieran, quieres crearlos y devolver un código de estado HTTP de "CREATED" `201`.

Pero todavía quieres poder filtrar y convertir los datos que devuelves con un `response_model`.

Para esos casos, puedes usar un parámetro `Response`.

## Usa un parámetro `Response`

Puedes declarar un parámetro de tipo `Response` en tu *función de path operation* (como puedes hacer para cookies y headers).

Y luego puedes establecer el `status_code` en ese objeto de response *temporal*.

{* ../../docs_src/response_change_status_code/tutorial001.py hl[1,9,12] *}

Y luego puedes devolver cualquier objeto que necesites, como lo harías normalmente (un `dict`, un modelo de base de datos, etc.).

Y si declaraste un `response_model`, todavía se utilizará para filtrar y convertir el objeto que devolviste.

**FastAPI** usará ese response *temporal* para extraer el código de estado (también cookies y headers), y los pondrá en el response final que contiene el valor que devolviste, filtrado por cualquier `response_model`.

También puedes declarar el parámetro `Response` en dependencias y establecer el código de estado en ellas. Pero ten en cuenta que el último establecido prevalecerá.
