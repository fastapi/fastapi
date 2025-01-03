# Response Personalizado - HTML, Stream, Archivo, otros

Por defecto, **FastAPI** devolverá los responses usando `JSONResponse`.

Puedes sobrescribirlo devolviendo un `Response` directamente como se ve en [Devolver una Response directamente](response-directly.md){.internal-link target=_blank}.

Pero si devuelves un `Response` directamente (o cualquier subclase, como `JSONResponse`), los datos no se convertirán automáticamente (incluso si declaras un `response_model`), y la documentación no se generará automáticamente (por ejemplo, incluyendo el "media type" específico, en el HTTP header `Content-Type` como parte del OpenAPI generado).

Pero también puedes declarar el `Response` que quieres usar (por ejemplo, cualquier subclase de `Response`), en el *path operation decorator* usando el parámetro `response_class`.

Los contenidos que devuelvas desde tu *path operation function* se colocarán dentro de esa `Response`.

Y si ese `Response` tiene un media type JSON (`application/json`), como es el caso con `JSONResponse` y `UJSONResponse`, los datos que devuelvas se convertirán automáticamente (y serán filtrados) con cualquier `response_model` de Pydantic que hayas declarado en el *path operation decorator*.

/// note | Nota

Si usas una clase de response sin media type, FastAPI esperará que tu response no tenga contenido, por lo que no documentará el formato del response en su OpenAPI generado.

///

## Usa `ORJSONResponse`

Por ejemplo, si estás exprimendo el rendimiento, puedes instalar y usar <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a> y establecer el response como `ORJSONResponse`.

Importa la clase `Response` (sub-clase) que quieras usar y declárala en el *path operation decorator*.

Para responses grandes, devolver una `Response` directamente es mucho más rápido que devolver un diccionario.

Esto se debe a que, por defecto, FastAPI inspeccionará cada elemento dentro y se asegurará de que sea serializable como JSON, usando el mismo [Codificador Compatible con JSON](../tutorial/encoder.md){.internal-link target=_blank} explicado en el tutorial. Esto es lo que te permite devolver **objetos arbitrarios**, por ejemplo, modelos de bases de datos.

Pero si estás seguro de que el contenido que estás devolviendo es **serializable con JSON**, puedes pasarlo directamente a la clase de response y evitar la sobrecarga extra que FastAPI tendría al pasar tu contenido de retorno a través de `jsonable_encoder` antes de pasarlo a la clase de response.

{* ../../docs_src/custom_response/tutorial001b.py hl[2,7] *}

/// info | Información

El parámetro `response_class` también se utilizará para definir el "media type" del response.

En este caso, el HTTP header `Content-Type` se establecerá en `application/json`.

Y se documentará así en OpenAPI.

///

/// tip | Consejo

El `ORJSONResponse` solo está disponible en FastAPI, no en Starlette.

///

## Response HTML

Para devolver un response con HTML directamente desde **FastAPI**, usa `HTMLResponse`.

* Importa `HTMLResponse`.
* Pasa `HTMLResponse` como parámetro `response_class` de tu *path operation decorator*.

{* ../../docs_src/custom_response/tutorial002.py hl[2,7] *}

/// info | Información

El parámetro `response_class` también se utilizará para definir el "media type" del response.

En este caso, el HTTP header `Content-Type` se establecerá en `text/html`.

Y se documentará así en OpenAPI.

///

### Devuelve una `Response`

Como se ve en [Devolver una Response directamente](response-directly.md){.internal-link target=_blank}, también puedes sobrescribir el response directamente en tu *path operation*, devolviéndolo.

El mismo ejemplo de arriba, devolviendo una `HTMLResponse`, podría verse así:

{* ../../docs_src/custom_response/tutorial003.py hl[2,7,19] *}

/// warning | Advertencia

Una `Response` devuelta directamente por tu *path operation function* no se documentará en OpenAPI (por ejemplo, el `Content-Type` no se documentará) y no será visible en la documentación interactiva automática.

///

/// info | Información

Por supuesto, el `Content-Type` header real, el código de estado, etc., provendrán del objeto `Response` que devolviste.

///

### Documenta en OpenAPI y sobrescribe `Response`

Si quieres sobrescribir el response desde dentro de la función pero al mismo tiempo documentar el "media type" en OpenAPI, puedes usar el parámetro `response_class` Y devolver un objeto `Response`.

El `response_class` solo se usará para documentar el OpenAPI *path operation*, pero tu `Response` se usará tal cual.

#### Devuelve un `HTMLResponse` directamente

Por ejemplo, podría ser algo así:

{* ../../docs_src/custom_response/tutorial004.py hl[7,21,23] *}

En este ejemplo, la función `generate_html_response()` ya genera y devuelve una `Response` en lugar de devolver el HTML en un `str`.

Al devolver el resultado de llamar a `generate_html_response()`, ya estás devolviendo una `Response` que sobrescribirá el comportamiento predeterminado de **FastAPI**.

Pero como pasaste `HTMLResponse` en el `response_class` también, **FastAPI** sabrá cómo documentarlo en OpenAPI y la documentación interactiva como HTML con `text/html`:

<img src="/img/tutorial/custom-response/image01.png">

## Responses disponibles

Aquí hay algunos de los responses disponibles.

Ten en cuenta que puedes usar `Response` para devolver cualquier otra cosa, o incluso crear una sub-clase personalizada.

/// note | Nota Técnica

También podrías usar `from starlette.responses import HTMLResponse`.

**FastAPI** proporciona los mismos `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette.

///

### `Response`

La clase principal `Response`, todos los otros responses heredan de ella.

Puedes devolverla directamente.

Acepta los siguientes parámetros:

* `content` - Un `str` o `bytes`.
* `status_code` - Un código de estado HTTP `int`.
* `headers` - Un `dict` de strings.
* `media_type` - Un `str` que da el media type. Por ejemplo, `"text/html"`.

FastAPI (de hecho Starlette) incluirá automáticamente un header Content-Length. También incluirá un header Content-Type, basado en el `media_type` y añadiendo un conjunto de caracteres para tipos de texto.

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

### `HTMLResponse`

Toma algún texto o bytes y devuelve un response HTML, como leíste arriba.

### `PlainTextResponse`

Toma algún texto o bytes y devuelve un response de texto plano.

{* ../../docs_src/custom_response/tutorial005.py hl[2,7,9] *}

### `JSONResponse`

Toma algunos datos y devuelve un response codificado como `application/json`.

Este es el response predeterminado usado en **FastAPI**, como leíste arriba.

### `ORJSONResponse`

Un response JSON rápido alternativo usando <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, como leíste arriba.

/// info | Información

Esto requiere instalar `orjson`, por ejemplo, con `pip install orjson`.

///

### `UJSONResponse`

Un response JSON alternativo usando <a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>.

/// info | Información

Esto requiere instalar `ujson`, por ejemplo, con `pip install ujson`.

///

/// warning | Advertencia

`ujson` es menos cuidadoso que la implementación integrada de Python en cómo maneja algunos casos extremos.

///

{* ../../docs_src/custom_response/tutorial001.py hl[2,7] *}

/// tip | Consejo

Es posible que `ORJSONResponse` sea una alternativa más rápida.

///

### `RedirectResponse`

Devuelve una redirección HTTP. Usa un código de estado 307 (Redirección Temporal) por defecto.

Puedes devolver un `RedirectResponse` directamente:

{* ../../docs_src/custom_response/tutorial006.py hl[2,9] *}

---

O puedes usarlo en el parámetro `response_class`:

{* ../../docs_src/custom_response/tutorial006b.py hl[2,7,9] *}

Si haces eso, entonces puedes devolver la URL directamente desde tu *path operation function*.

En este caso, el `status_code` utilizado será el predeterminado para `RedirectResponse`, que es `307`.

---

También puedes usar el parámetro `status_code` combinado con el parámetro `response_class`:

{* ../../docs_src/custom_response/tutorial006c.py hl[2,7,9] *}

### `StreamingResponse`

Toma un generador `async` o un generador/iterador normal y transmite el cuerpo del response.

{* ../../docs_src/custom_response/tutorial007.py hl[2,14] *}

#### Usando `StreamingResponse` con objetos similares a archivos

Si tienes un objeto similar a un archivo (por ejemplo, el objeto devuelto por `open()`), puedes crear una función generadora para iterar sobre ese objeto similar a un archivo.

De esa manera, no tienes que leerlo todo primero en memoria, y puedes pasar esa función generadora al `StreamingResponse`, y devolverlo.

Esto incluye muchos paquetes para interactuar con almacenamiento en la nube, procesamiento de video y otros.

{* ../../docs_src/custom_response/tutorial008.py hl[2,10:12,14] *}

1. Esta es la función generadora. Es una "función generadora" porque contiene declaraciones `yield` dentro.
2. Al usar un bloque `with`, nos aseguramos de que el objeto similar a un archivo se cierre después de que la función generadora termine. Así, después de que termina de enviar el response.
3. Este `yield from` le dice a la función que itere sobre esa cosa llamada `file_like`. Y luego, para cada parte iterada, yield esa parte como proveniente de esta función generadora (`iterfile`).

    Entonces, es una función generadora que transfiere el trabajo de "generar" a algo más internamente.

    Al hacerlo de esta manera, podemos ponerlo en un bloque `with`, y de esa manera, asegurarnos de que el objeto similar a un archivo se cierre después de finalizar.

/// tip | Consejo

Nota que aquí como estamos usando `open()` estándar que no admite `async` y `await`, declaramos el path operation con `def` normal.

///

### `FileResponse`

Transmite un archivo asincrónicamente como response.

Toma un conjunto diferente de argumentos para crear un instance que los otros tipos de response:

* `path` - La path del archivo para el archivo a transmitir.
* `headers` - Cualquier header personalizado para incluir, como un diccionario.
* `media_type` - Un string que da el media type. Si no se establece, se usará el nombre de archivo o la path para inferir un media type.
* `filename` - Si se establece, se incluirá en el response `Content-Disposition`.

Los responses de archivos incluirán los headers apropiados `Content-Length`, `Last-Modified` y `ETag`.

{* ../../docs_src/custom_response/tutorial009.py hl[2,10] *}

También puedes usar el parámetro `response_class`:

{* ../../docs_src/custom_response/tutorial009b.py hl[2,8,10] *}

En este caso, puedes devolver la path del archivo directamente desde tu *path operation* function.

## Clase de response personalizada

Puedes crear tu propia clase de response personalizada, heredando de `Response` y usándola.

Por ejemplo, digamos que quieres usar <a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>, pero con algunas configuraciones personalizadas no utilizadas en la clase `ORJSONResponse` incluida.

Digamos que quieres que devuelva JSON con sangría y formato, por lo que quieres usar la opción de orjson `orjson.OPT_INDENT_2`.

Podrías crear un `CustomORJSONResponse`. Lo principal que tienes que hacer es crear un método `Response.render(content)` que devuelva el contenido como `bytes`:

{* ../../docs_src/custom_response/tutorial009c.py hl[9:14,17] *}

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

## Clase de response predeterminada

Al crear una instance de la clase **FastAPI** o un `APIRouter`, puedes especificar qué clase de response usar por defecto.

El parámetro que define esto es `default_response_class`.

En el ejemplo a continuación, **FastAPI** usará `ORJSONResponse` por defecto, en todas las *path operations*, en lugar de `JSONResponse`.

{* ../../docs_src/custom_response/tutorial010.py hl[2,4] *}

/// tip | Consejo

Todavía puedes sobrescribir `response_class` en *path operations* como antes.

///

## Documentación adicional

También puedes declarar el media type y muchos otros detalles en OpenAPI usando `responses`: [Responses Adicionales en OpenAPI](additional-responses.md){.internal-link target=_blank}.
