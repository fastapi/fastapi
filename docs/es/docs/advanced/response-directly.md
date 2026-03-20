# Devolver una Response Directamente { #return-a-response-directly }

Cuando creas una *path operation* en **FastAPI**, normalmente puedes devolver cualquier dato desde ella: un `dict`, una `list`, un modelo de Pydantic, un modelo de base de datos, etc.

Si declaras un [Response Model](../tutorial/response-model.md) FastAPI lo usará para serializar los datos a JSON, usando Pydantic.

Si no declaras un response model, FastAPI usará el `jsonable_encoder` explicado en [JSON Compatible Encoder](../tutorial/encoder.md) y lo pondrá en un `JSONResponse`.

También podrías crear un `JSONResponse` directamente y devolverlo.

/// tip | Consejo

Normalmente tendrás mucho mejor rendimiento usando un [Response Model](../tutorial/response-model.md) que devolviendo un `JSONResponse` directamente, ya que de esa forma serializa los datos usando Pydantic, en Rust.

///

## Devolver una `Response` { #return-a-response }

De hecho, puedes devolver cualquier `Response` o cualquier subclase de ella.

/// info | Información

`JSONResponse` en sí misma es una subclase de `Response`.

///

Y cuando devuelves una `Response`, **FastAPI** la pasará directamente.

No hará ninguna conversión de datos con los modelos de Pydantic, no convertirá los contenidos a ningún tipo, etc.

Esto te da mucha flexibilidad. Puedes devolver cualquier tipo de datos, sobrescribir cualquier declaración o validación de datos, etc.

También te da mucha responsabilidad. Tienes que asegurarte de que los datos que devuelves sean correctos, en el formato correcto, que se puedan serializar, etc.

## Usar el `jsonable_encoder` en una `Response` { #using-the-jsonable-encoder-in-a-response }

Como **FastAPI** no realiza cambios en una `Response` que devuelves, tienes que asegurarte de que sus contenidos estén listos para ello.

Por ejemplo, no puedes poner un modelo de Pydantic en un `JSONResponse` sin primero convertirlo a un `dict` con todos los tipos de datos (como `datetime`, `UUID`, etc.) convertidos a tipos compatibles con JSON.

Para esos casos, puedes usar el `jsonable_encoder` para convertir tus datos antes de pasarlos a un response:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | Detalles técnicos

También podrías usar `from starlette.responses import JSONResponse`.

**FastAPI** proporciona los mismos `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette.

///

## Devolver una `Response` personalizada { #returning-a-custom-response }

El ejemplo anterior muestra todas las partes que necesitas, pero aún no es muy útil, ya que podrías haber devuelto el `item` directamente, y **FastAPI** lo colocaría en un `JSONResponse` por ti, convirtiéndolo a un `dict`, etc. Todo eso por defecto.

Ahora, veamos cómo podrías usar eso para devolver un response personalizado.

Digamos que quieres devolver un response en [XML](https://en.wikipedia.org/wiki/XML).

Podrías poner tu contenido XML en un string, poner eso en un `Response`, y devolverlo:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Cómo funciona un Response Model { #how-a-response-model-works }

Cuando declaras un [Response Model - Return Type](../tutorial/response-model.md) en una *path operation*, **FastAPI** lo usará para serializar los datos a JSON, usando Pydantic.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

Como eso sucederá del lado de Rust, el rendimiento será mucho mejor que si se hiciera con Python normal y la clase `JSONResponse`.

Al usar un `response_model` o tipo de retorno, FastAPI no usará el `jsonable_encoder` para convertir los datos (lo cual sería más lento) ni la clase `JSONResponse`.

En su lugar, toma los bytes JSON generados con Pydantic usando el response model (o tipo de retorno) y devuelve una `Response` con el media type correcto para JSON directamente (`application/json`).

## Notas { #notes }

Cuando devuelves una `Response` directamente, sus datos no son validados, convertidos (serializados), ni documentados automáticamente.

Pero aún puedes documentarlo como se describe en [Additional Responses in OpenAPI](additional-responses.md).

Puedes ver en secciones posteriores cómo usar/declarar estas `Response`s personalizadas mientras todavía tienes conversión automática de datos, documentación, etc.
