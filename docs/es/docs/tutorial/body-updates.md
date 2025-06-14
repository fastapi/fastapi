# Cuerpo - Actualizaciones

## Actualización reemplazando con `PUT`

Para actualizar un ítem puedes utilizar la operación de <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a>.

Puedes usar el `jsonable_encoder` para convertir los datos de entrada en datos que se puedan almacenar como JSON (por ejemplo, con una base de datos NoSQL). Por ejemplo, convirtiendo `datetime` a `str`.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` se usa para recibir datos que deben reemplazar los datos existentes.

### Advertencia sobre el reemplazo

Esto significa que si quieres actualizar el ítem `bar` usando `PUT` con un body que contenga:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

debido a que no incluye el atributo ya almacenado `"tax": 20.2`, el modelo de entrada tomaría el valor por defecto de `"tax": 10.5`.

Y los datos se guardarían con ese "nuevo" `tax` de `10.5`.

## Actualizaciones parciales con `PATCH`

También puedes usar la operación de <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> para actualizar *parcialmente* datos.

Esto significa que puedes enviar solo los datos que deseas actualizar, dejando el resto intacto.

/// note | Nota

`PATCH` es menos usado y conocido que `PUT`.

Y muchos equipos utilizan solo `PUT`, incluso para actualizaciones parciales.

Eres **libre** de usarlos como desees, **FastAPI** no impone ninguna restricción.

Pero esta guía te muestra, más o menos, cómo se pretende que se usen.

///

### Uso del parámetro `exclude_unset` de Pydantic

Si quieres recibir actualizaciones parciales, es muy útil usar el parámetro `exclude_unset` en el `.model_dump()` del modelo de Pydantic.

Como `item.model_dump(exclude_unset=True)`.

/// info | Información

En Pydantic v1 el método se llamaba `.dict()`, fue deprecado (pero aún soportado) en Pydantic v2, y renombrado a `.model_dump()`.

Los ejemplos aquí usan `.dict()` para compatibilidad con Pydantic v1, pero deberías usar `.model_dump()` si puedes usar Pydantic v2.

///

Eso generaría un `dict` solo con los datos que se establecieron al crear el modelo `item`, excluyendo los valores por defecto.

Luego puedes usar esto para generar un `dict` solo con los datos que se establecieron (enviados en el request), omitiendo los valores por defecto:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### Uso del parámetro `update` de Pydantic

Ahora, puedes crear una copia del modelo existente usando `.model_copy()`, y pasar el parámetro `update` con un `dict` que contenga los datos a actualizar.

/// info | Información

En Pydantic v1 el método se llamaba `.copy()`, fue deprecado (pero aún soportado) en Pydantic v2, y renombrado a `.model_copy()`.

Los ejemplos aquí usan `.copy()` para compatibilidad con Pydantic v1, pero deberías usar `.model_copy()` si puedes usar Pydantic v2.

///

Como `stored_item_model.model_copy(update=update_data)`:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### Resumen de actualizaciones parciales

En resumen, para aplicar actualizaciones parciales deberías:

* (Opcionalmente) usar `PATCH` en lugar de `PUT`.
* Recuperar los datos almacenados.
* Poner esos datos en un modelo de Pydantic.
* Generar un `dict` sin valores por defecto del modelo de entrada (usando `exclude_unset`).
    * De esta manera puedes actualizar solo los valores realmente establecidos por el usuario, en lugar de sobrescribir valores ya almacenados con valores por defecto en tu modelo.
* Crear una copia del modelo almacenado, actualizando sus atributos con las actualizaciones parciales recibidas (usando el parámetro `update`).
* Convertir el modelo copiado en algo que pueda almacenarse en tu base de datos (por ejemplo, usando el `jsonable_encoder`).
    * Esto es comparable a usar el método `.model_dump()` del modelo de nuevo, pero asegura (y convierte) los valores a tipos de datos que pueden convertirse a JSON, por ejemplo, `datetime` a `str`.
* Guardar los datos en tu base de datos.
* Devolver el modelo actualizado.

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | Consejo

Puedes realmente usar esta misma técnica con una operación HTTP `PUT`.

Pero el ejemplo aquí usa `PATCH` porque fue creado para estos casos de uso.

///

/// note | Nota

Observa que el modelo de entrada sigue siendo validado.

Entonces, si deseas recibir actualizaciones parciales que puedan omitir todos los atributos, necesitas tener un modelo con todos los atributos marcados como opcionales (con valores por defecto o `None`).

Para distinguir entre los modelos con todos los valores opcionales para **actualizaciones** y modelos con valores requeridos para **creación**, puedes utilizar las ideas descritas en [Modelos Extra](extra-models.md){.internal-link target=_blank}.

///
