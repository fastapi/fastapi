# Return a Response Directly
# Retornar Directamente una Respuesta

Cuando tu creas una *operación de camino*, tu puedes retornar normalmente cualquier dato: un `dict`, una `list`, un modelo Pydantic, modelo de base de datos, etc.

Por defecto, **FastAPI** convertirá automáticamente ese valor de retorno para JSON usando el `jsonable_encoder` explicado en [Codificador Compatible JSON](../tutorial/encoder.md){.internal-link target=_blank}.

Luego, detrás de escena, pondría esos datos compatibles con JSON (por ejemplo, un `dict`) dentro de una `JSONResponse` que se usaría para enviar la respuesta al cliente.

Pero tu puedes retornar una `JSONResponse` directamente de tu *operación de camino*.

Esto puede ser útil, por ejemplo, para retornar cookies o encabezados personalizados.

## Retornar una `Response`

De hecho, puedes retornar cualquier `Response` o cualquier subclase de la misma.

!!! tip
    `JSONResponse` en si misma es una subclase de `Response`.

Y cuando retornas una `Response`, **FastAPI** la pasará directamente.

No será realizado ninguna conversión de datos con modelos Pydantic, no se convertirán los contenidos de ningún tipo, etc.

Esto te da mucha flexibilidad. Puedes retornar cualquier tipo de datos, sobrescribir cualquer declaración de datos o validación, etc.

## Usando el `jsonable_encoder` en la `Response`

Como **FastAPI** no realiza ningún cambion en la `Response` que tu retornas, debes asegurate que el contenido esta pronto.

Por ejemplo, no puedes poner un modelo Pydantic en una `JSONResponse` sin previamente convertirlo a un `dict` con todos los tipos de datos (como `datetime`, `UUID`, etc) convertidos para tipos compatibles con JSON.

Para esos casos, puedes usar el `jsonable_encoder` para convertir tus datos antes de pasarlos a la respuesta:

```Python hl_lines="4 6 20 21"
{!../../../docs_src/response_directly/tutorial001.py!}
```

!!! note "Detalles Técnicos"
    También puedes usar `from starlette.responses import JSONResponse`.

    **FastAPI** provee las mismas `starlette.responses` que `fastapi.responses` simplemente como una convención para ti, el desarrollador. Pero la mayoría de las respuestas disponibles vienen directamente de Starlette.

## Retornando una `Response` personalizada

El ejemplo anterior muestra las partes que tu precisas, pero no es muy útil todavía, como tu podrias simplemente retornar el `item` directamente, y **FastAPI** no pondría en una `JSONResponse` para ti, convirtiéndolo en un `dict`, etc. Todo esto por defecto.

Ahora, veamos cómo puedes usarlo, para retornar una respuesta personalizada.

Digamos que tu quieres retornar una respuesta <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a>.

Puedes poner tu contenido    XML en una string, ponerla en una `Response` y retornarla:

```Python hl_lines="1  18"
{!../../../docs_src/response_directly/tutorial002.py!}
```

## Notas

Cuando retornas una `Response` directamente, los datos no son validados, convertidos (serializados), ni documentados automáticamente.

Pero todavía es posible documentarlo, como es descrito en [Respuestas Adicionales en OpenAPI](additional-responses.md){.internal-link target=_blank}.

Puedes ver en secciones posteriores como usar/declarar esas `Response`s personalizadas mientras continúas teniendo la conversión automática de datos, documentación, etc.
