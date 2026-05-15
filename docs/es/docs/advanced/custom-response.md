# Response Personalizado - HTML, Stream, Archivo, otros { #custom-response-html-stream-file-others }

Por defecto, **FastAPI** devolverá responses JSON.

Puedes sobrescribirlo devolviendo un `Response` directamente como se ve en [Devolver una Response directamente](response-directly.md).

Pero si devuelves un `Response` directamente (o cualquier subclase, como `JSONResponse`), los datos no se convertirán automáticamente (incluso si declaras un `response_model`), y la documentación no se generará automáticamente (por ejemplo, incluyendo el "media type" específico, en el HTTP header `Content-Type` como parte del OpenAPI generado).

Pero también puedes declarar el `Response` que quieres usar (por ejemplo, cualquier subclase de `Response`), en el *path operation decorator* usando el parámetro `response_class`.

Los contenidos que devuelvas desde tu *path operation function* se colocarán dentro de esa `Response`.

/// note | Nota

Si usas una clase de response sin media type, FastAPI esperará que tu response no tenga contenido, por lo que no documentará el formato del response en su OpenAPI generado.

///

## Responses JSON { #json-responses }

Por defecto FastAPI devuelve responses JSON.

Si declaras un [Response Model](../tutorial/response-model.md) FastAPI lo usará para serializar los datos a JSON, usando Pydantic.

Si no declaras un response model, FastAPI usará el `jsonable_encoder` explicado en [Codificador Compatible con JSON](../tutorial/encoder.md) y lo pondrá en un `JSONResponse`.

Si declaras un `response_class` con un media type JSON (`application/json`), como es el caso con `JSONResponse`, los datos que devuelvas se convertirán automáticamente (y serán filtrados) con cualquier `response_model` de Pydantic que hayas declarado en el *path operation decorator*. Pero los datos no se serializarán a bytes JSON con Pydantic, en su lugar se convertirán con el `jsonable_encoder` y luego se pasarán a la clase `JSONResponse`, que los serializará a bytes usando la librería JSON estándar de Python.

### Rendimiento JSON { #json-performance }

En resumen, si quieres el máximo rendimiento, usa un [Response Model](../tutorial/response-model.md) y no declares un `response_class` en el *path operation decorator*.

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## Response HTML { #html-response }

Para devolver un response con HTML directamente desde **FastAPI**, usa `HTMLResponse`.

* Importa `HTMLResponse`.
* Pasa `HTMLResponse` como parámetro `response_class` de tu *path operation decorator*.

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | Información

El parámetro `response_class` también se utilizará para definir el "media type" del response.

En este caso, el HTTP header `Content-Type` se establecerá en `text/html`.

Y se documentará así en OpenAPI.

///

### Devuelve una `Response` { #return-a-response }

Como se ve en [Devolver una Response directamente](response-directly.md), también puedes sobrescribir el response directamente en tu *path operation*, devolviéndolo.

El mismo ejemplo de arriba, devolviendo una `HTMLResponse`, podría verse así:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | Advertencia

Una `Response` devuelta directamente por tu *path operation function* no se documentará en OpenAPI (por ejemplo, el `Content-Type` no se documentará) y no será visible en la documentación interactiva automática.

///

/// info | Información

Por supuesto, el `Content-Type` header real, el código de estado, etc., provendrán del objeto `Response` que devolviste.

///

### Documenta en OpenAPI y sobrescribe `Response` { #document-in-openapi-and-override-response }

Si quieres sobrescribir el response desde dentro de la función pero al mismo tiempo documentar el "media type" en OpenAPI, puedes usar el parámetro `response_class` Y devolver un objeto `Response`.

El `response_class` solo se usará para documentar el OpenAPI *path operation*, pero tu `Response` se usará tal cual.

#### Devuelve un `HTMLResponse` directamente { #return-an-htmlresponse-directly }

Por ejemplo, podría ser algo así:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

En este ejemplo, la función `generate_html_response()` ya genera y devuelve una `Response` en lugar de devolver el HTML en un `str`.

Al devolver el resultado de llamar a `generate_html_response()`, ya estás devolviendo una `Response` que sobrescribirá el comportamiento por defecto de **FastAPI**.

Pero como pasaste `HTMLResponse` en el `response_class` también, **FastAPI** sabrá cómo documentarlo en OpenAPI y la documentación interactiva como HTML con `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## Responses disponibles { #available-responses }

Aquí hay algunos de los responses disponibles.

Ten en cuenta que puedes usar `Response` para devolver cualquier otra cosa, o incluso crear una sub-clase personalizada.

/// note | Nota Técnica

También podrías usar `from starlette.responses import HTMLResponse`.

**FastAPI** proporciona los mismos `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette.

///

### `Response` { #response }

La clase principal `Response`, todos los otros responses heredan de ella.

Puedes devolverla directamente.

Acepta los siguientes parámetros:

* `content` - Un `str` o `bytes`.
* `status_code` - Un código de estado HTTP `int`.
* `headers` - Un `dict` de strings.
* `media_type` - Un `str` que da el media type. Por ejemplo, `"text/html"`.

FastAPI (de hecho Starlette) incluirá automáticamente un header Content-Length. También incluirá un header Content-Type, basado en el `media_type` y añadiendo un conjunto de caracteres para tipos de texto.

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

Toma algún texto o bytes y devuelve un response HTML, como leíste arriba.

### `PlainTextResponse` { #plaintextresponse }

Toma algún texto o bytes y devuelve un response de texto plano.

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

Toma algunos datos y devuelve un response codificado como `application/json`.

Este es el response usado por defecto en **FastAPI**, como leíste arriba.

/// note | Nota Técnica

Pero si declaras un response model o un tipo de retorno, eso se usará directamente para serializar los datos a JSON, y se devolverá directamente un response con el media type correcto para JSON, sin usar la clase `JSONResponse`.

Esta es la forma ideal de obtener el mejor rendimiento.

///

### `RedirectResponse` { #redirectresponse }

Devuelve una redirección HTTP. Usa un código de estado 307 (Redirección Temporal) por defecto.

Puedes devolver un `RedirectResponse` directamente:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

O puedes usarlo en el parámetro `response_class`:


{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

Si haces eso, entonces puedes devolver la URL directamente desde tu *path operation* function.

En este caso, el `status_code` utilizado será el por defecto para `RedirectResponse`, que es `307`.

---

También puedes usar el parámetro `status_code` combinado con el parámetro `response_class`:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

Toma un generador `async` o un generador/iterador normal (una función con `yield`) y transmite el cuerpo del response.

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | Nota Técnica

Una tarea `async` solo puede cancelarse cuando llega a un `await`. Si no hay `await`, el generador (función con `yield`) no se puede cancelar correctamente y puede seguir ejecutándose incluso después de solicitar la cancelación.

Como este pequeño ejemplo no necesita ninguna sentencia `await`, añadimos un `await anyio.sleep(0)` para darle al loop de eventos la oportunidad de manejar la cancelación.

Esto sería aún más importante con streams grandes o infinitos.

///

/// tip | Consejo

En lugar de devolver un `StreamingResponse` directamente, probablemente deberías seguir el estilo en [Stream Data](./stream-data.md), es mucho más conveniente y maneja la cancelación por detrás de escena por ti.

Si estás transmitiendo JSON Lines, sigue el tutorial [Stream JSON Lines](../tutorial/stream-json-lines.md).

///

### `FileResponse` { #fileresponse }

Transmite un archivo asincrónicamente como response.

Toma un conjunto diferente de argumentos para crear un instance que los otros tipos de response:

* `path` - La path del archivo para el archivo a transmitir.
* `headers` - Cualquier header personalizado para incluir, como un diccionario.
* `media_type` - Un string que da el media type. Si no se establece, se usará el nombre de archivo o la path para inferir un media type.
* `filename` - Si se establece, se incluirá en el response `Content-Disposition`.

Los responses de archivos incluirán los headers apropiados `Content-Length`, `Last-Modified` y `ETag`.

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

También puedes usar el parámetro `response_class`:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

En este caso, puedes devolver la path del archivo directamente desde tu *path operation* function.

## Clase de response personalizada { #custom-response-class }

Puedes crear tu propia clase de response personalizada, heredando de `Response` y usándola.

Por ejemplo, digamos que quieres usar [`orjson`](https://github.com/ijl/orjson) con algunas configuraciones.

Digamos que quieres que devuelva JSON con sangría y formato, por lo que quieres usar la opción de orjson `orjson.OPT_INDENT_2`.

Podrías crear un `CustomORJSONResponse`. Lo principal que tienes que hacer es crear un método `Response.render(content)` que devuelva el contenido como `bytes`:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

Ahora en lugar de devolver:

```json
{"message": "Hello World"}
```

...este response devolverá:

```json
{
  "message": "Hello World"
}
```

Por supuesto, probablemente encontrarás formas mucho mejores de aprovechar esto que formatear JSON. 😉

### `orjson` o Response Model { #orjson-or-response-model }

Si lo que buscas es rendimiento, probablemente te convenga más usar un [Response Model](../tutorial/response-model.md) que un response con `orjson`.

Con un response model, FastAPI usará Pydantic para serializar los datos a JSON, sin pasos intermedios, como convertirlos con `jsonable_encoder`, que ocurriría en cualquier otro caso.

Y por debajo, Pydantic usa los mismos mecanismos en Rust que `orjson` para serializar a JSON, así que ya obtendrás el mejor rendimiento con un response model.

## Clase de response por defecto { #default-response-class }

Al crear una instance de la clase **FastAPI** o un `APIRouter`, puedes especificar qué clase de response usar por defecto.

El parámetro que define esto es `default_response_class`.

En el ejemplo a continuación, **FastAPI** usará `HTMLResponse` por defecto, en todas las *path operations*, en lugar de JSON.

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | Consejo

Todavía puedes sobrescribir `response_class` en *path operations* como antes.

///

## Documentación adicional { #additional-documentation }

También puedes declarar el media type y muchos otros detalles en OpenAPI usando `responses`: [Responses Adicionales en OpenAPI](additional-responses.md).
