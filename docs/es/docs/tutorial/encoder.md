# JSON Compatible Encoder

Hay algunos casos en los que podrías necesitar convertir un tipo de dato (como un modelo de Pydantic) a algo compatible con JSON (como un `dict`, `list`, etc).

Por ejemplo, si necesitas almacenarlo en una base de datos.

Para eso, **FastAPI** proporciona una función `jsonable_encoder()`.

## Usando el `jsonable_encoder`

Imaginemos que tienes una base de datos `fake_db` que solo recibe datos compatibles con JSON.

Por ejemplo, no recibe objetos `datetime`, ya que no son compatibles con JSON.

Entonces, un objeto `datetime` tendría que ser convertido a un `str` que contenga los datos en formato <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO</a>.

De la misma manera, esta base de datos no recibiría un modelo de Pydantic (un objeto con atributos), solo un `dict`.

Puedes usar `jsonable_encoder` para eso.

Recibe un objeto, como un modelo de Pydantic, y devuelve una versión compatible con JSON:

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

En este ejemplo, convertiría el modelo de Pydantic a un `dict`, y el `datetime` a un `str`.

El resultado de llamarlo es algo que puede ser codificado con la función estándar de Python <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a>.

No devuelve un gran `str` que contenga los datos en formato JSON (como una cadena de texto). Devuelve una estructura de datos estándar de Python (por ejemplo, un `dict`) con valores y sub-valores que son todos compatibles con JSON.

/// note | Nota

`jsonable_encoder` es utilizado internamente por **FastAPI** para convertir datos. Pero es útil en muchos otros escenarios.

///
