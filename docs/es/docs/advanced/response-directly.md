# Devolver una Response Directamente

Cuando creas una *path operation* en **FastAPI**, normalmente puedes devolver cualquier dato desde ella: un `dict`, una `list`, un modelo de Pydantic, un modelo de base de datos, etc.

Por defecto, **FastAPI** convertiría automáticamente ese valor de retorno a JSON usando el `jsonable_encoder` explicado en [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank}.

Luego, detrás de escena, pondría esos datos compatibles con JSON (por ejemplo, un `dict`) dentro de un `JSONResponse` que se usaría para enviar el response al cliente.

Pero puedes devolver un `JSONResponse` directamente desde tus *path operations*.

Esto podría ser útil, por ejemplo, para devolver headers o cookies personalizados.

## Devolver una `Response`

De hecho, puedes devolver cualquier `Response` o cualquier subclase de ella.

/// tip | Consejo

`JSONResponse` en sí misma es una subclase de `Response`.

///

Y cuando devuelves una `Response`, **FastAPI** la pasará directamente.

No hará ninguna conversión de datos con los modelos de Pydantic, no convertirá los contenidos a ningún tipo, etc.

Esto te da mucha flexibilidad. Puedes devolver cualquier tipo de datos, sobrescribir cualquier declaración o validación de datos, etc.

## Usar el `jsonable_encoder` en una `Response`

Como **FastAPI** no realiza cambios en una `Response` que devuelves, tienes que asegurarte de que sus contenidos estén listos para ello.

Por ejemplo, no puedes poner un modelo de Pydantic en un `JSONResponse` sin primero convertirlo a un `dict` con todos los tipos de datos (como `datetime`, `UUID`, etc.) convertidos a tipos compatibles con JSON.

Para esos casos, puedes usar el `jsonable_encoder` para convertir tus datos antes de pasarlos a un response:

{* ../../docs_src/response_directly/tutorial001.py hl[6:7,21:22] *}

/// note | Nota

También podrías usar `from starlette.responses import JSONResponse`.

**FastAPI** proporciona los mismos `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette.

///

## Devolver una `Response` personalizada

El ejemplo anterior muestra todas las partes que necesitas, pero aún no es muy útil, ya que podrías haber devuelto el `item` directamente, y **FastAPI** lo colocaría en un `JSONResponse` por ti, convirtiéndolo a un `dict`, etc. Todo eso por defecto.

Ahora, veamos cómo podrías usar eso para devolver un response personalizado.

Digamos que quieres devolver un response en <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a>.

Podrías poner tu contenido XML en un string, poner eso en un `Response`, y devolverlo:

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

## Notas

Cuando devuelves una `Response` directamente, sus datos no son validados, convertidos (serializados), ni documentados automáticamente.

Pero aún puedes documentarlo como se describe en [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}.

Puedes ver en secciones posteriores cómo usar/declarar estas `Response`s personalizadas mientras todavía tienes conversión automática de datos, documentación, etc.
