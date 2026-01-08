# Manejo de Errores { #handling-errors }

Existen muchas situaciones en las que necesitas notificar un error a un cliente que está usando tu API.

Este cliente podría ser un navegador con un frontend, un código de otra persona, un dispositivo IoT, etc.

Podrías necesitar decirle al cliente que:

* El cliente no tiene suficientes privilegios para esa operación.
* El cliente no tiene acceso a ese recurso.
* El ítem al que el cliente intentaba acceder no existe.
* etc.

En estos casos, normalmente devolverías un **código de estado HTTP** en el rango de **400** (de 400 a 499).

Esto es similar a los códigos de estado HTTP 200 (de 200 a 299). Esos códigos de estado "200" significan que de alguna manera hubo un "éxito" en el request.

Los códigos de estado en el rango de 400 significan que hubo un error por parte del cliente.

¿Recuerdas todos esos errores de **"404 Not Found"** (y chistes)?

## Usa `HTTPException` { #use-httpexception }

Para devolver responses HTTP con errores al cliente, usa `HTTPException`.

### Importa `HTTPException` { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py39.py hl[1] *}

### Lanza un `HTTPException` en tu código { #raise-an-httpexception-in-your-code }

`HTTPException` es una excepción de Python normal con datos adicionales relevantes para APIs.

Debido a que es una excepción de Python, no la `return`, sino que la `raise`.

Esto también significa que si estás dentro de una función de utilidad que estás llamando dentro de tu *path operation function*, y lanzas el `HTTPException` desde dentro de esa función de utilidad, no se ejecutará el resto del código en la *path operation function*, terminará ese request de inmediato y enviará el error HTTP del `HTTPException` al cliente.

El beneficio de lanzar una excepción en lugar de `return`ar un valor será más evidente en la sección sobre Dependencias y Seguridad.

En este ejemplo, cuando el cliente solicita un ítem por un ID que no existe, lanza una excepción con un código de estado de `404`:

{* ../../docs_src/handling_errors/tutorial001_py39.py hl[11] *}

### El response resultante { #the-resulting-response }

Si el cliente solicita `http://example.com/items/foo` (un `item_id` `"foo"`), ese cliente recibirá un código de estado HTTP de 200, y un response JSON de:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

Pero si el cliente solicita `http://example.com/items/bar` (un `item_id` inexistente `"bar"`), ese cliente recibirá un código de estado HTTP de 404 (el error "no encontrado"), y un response JSON de:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | Consejo

Cuando lanzas un `HTTPException`, puedes pasar cualquier valor que pueda convertirse a JSON como el parámetro `detail`, no solo `str`.

Podrías pasar un `dict`, un `list`, etc.

Son manejados automáticamente por **FastAPI** y convertidos a JSON.

///

## Agrega headers personalizados { #add-custom-headers }

Existen algunas situaciones en las que es útil poder agregar headers personalizados al error HTTP. Por ejemplo, para algunos tipos de seguridad.

Probablemente no necesitarás usarlos directamente en tu código.

Pero en caso de que los necesites para un escenario avanzado, puedes agregar headers personalizados:

{* ../../docs_src/handling_errors/tutorial002_py39.py hl[14] *}

## Instalar manejadores de excepciones personalizados { #install-custom-exception-handlers }

Puedes agregar manejadores de excepciones personalizados con <a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">las mismas utilidades de excepciones de Starlette</a>.

Supongamos que tienes una excepción personalizada `UnicornException` que tú (o un paquete que usas) podrías lanzar.

Y quieres manejar esta excepción globalmente con FastAPI.

Podrías agregar un manejador de excepciones personalizado con `@app.exception_handler()`:

{* ../../docs_src/handling_errors/tutorial003_py39.py hl[5:7,13:18,24] *}

Aquí, si solicitas `/unicorns/yolo`, la *path operation* lanzará un `UnicornException`.

Pero será manejado por el `unicorn_exception_handler`.

Así que recibirás un error limpio, con un código de estado HTTP de `418` y un contenido JSON de:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Nota Técnica

También podrías usar `from starlette.requests import Request` y `from starlette.responses import JSONResponse`.

**FastAPI** ofrece las mismas `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette. Lo mismo con `Request`.

///

## Sobrescribir los manejadores de excepciones predeterminados { #override-the-default-exception-handlers }

**FastAPI** tiene algunos manejadores de excepciones predeterminados.

Estos manejadores se encargan de devolver los responses JSON predeterminadas cuando lanzas un `HTTPException` y cuando el request tiene datos inválidos.

Puedes sobrescribir estos manejadores de excepciones con los tuyos propios.

### Sobrescribir excepciones de validación de request { #override-request-validation-exceptions }

Cuando un request contiene datos inválidos, **FastAPI** lanza internamente un `RequestValidationError`.

Y también incluye un manejador de excepciones predeterminado para ello.

Para sobrescribirlo, importa el `RequestValidationError` y úsalo con `@app.exception_handler(RequestValidationError)` para decorar el manejador de excepciones.

El manejador de excepciones recibirá un `Request` y la excepción.

{* ../../docs_src/handling_errors/tutorial004_py39.py hl[2,14:19] *}

Ahora, si vas a `/items/foo`, en lugar de obtener el error JSON por defecto con:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

obtendrás una versión en texto, con:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### Sobrescribir el manejador de errores de `HTTPException` { #override-the-httpexception-error-handler }

De la misma manera, puedes sobrescribir el manejador de `HTTPException`.

Por ejemplo, podrías querer devolver un response de texto plano en lugar de JSON para estos errores:

{* ../../docs_src/handling_errors/tutorial004_py39.py hl[3:4,9:11,25] *}

/// note | Nota Técnica

También podrías usar `from starlette.responses import PlainTextResponse`.

**FastAPI** ofrece las mismas `starlette.responses` como `fastapi.responses` solo como una conveniencia para ti, el desarrollador. Pero la mayoría de los responses disponibles vienen directamente de Starlette.

///

/// warning | Advertencia

Ten en cuenta que `RequestValidationError` contiene la información del nombre de archivo y la línea donde ocurre el error de validación, para que puedas mostrarla en tus logs con la información relevante si quieres.

Pero eso significa que si simplemente lo conviertes a un string y devuelves esa información directamente, podrías estar filtrando un poquito de información sobre tu sistema, por eso aquí el código extrae y muestra cada error de forma independiente.

///

### Usar el body de `RequestValidationError` { #use-the-requestvalidationerror-body }

El `RequestValidationError` contiene el `body` que recibió con datos inválidos.

Podrías usarlo mientras desarrollas tu aplicación para registrar el body y depurarlo, devolverlo al usuario, etc.

{* ../../docs_src/handling_errors/tutorial005_py39.py hl[14] *}

Ahora intenta enviar un ítem inválido como:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

Recibirás un response que te dirá que los datos son inválidos conteniendo el body recibido:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### `HTTPException` de FastAPI vs `HTTPException` de Starlette { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** tiene su propio `HTTPException`.

Y la clase de error `HTTPException` de **FastAPI** hereda de la clase de error `HTTPException` de Starlette.

La única diferencia es que el `HTTPException` de **FastAPI** acepta cualquier dato JSON-able para el campo `detail`, mientras que el `HTTPException` de Starlette solo acepta strings para ello.

Así que puedes seguir lanzando un `HTTPException` de **FastAPI** como de costumbre en tu código.

Pero cuando registras un manejador de excepciones, deberías registrarlo para el `HTTPException` de Starlette.

De esta manera, si alguna parte del código interno de Starlette, o una extensión o plug-in de Starlette, lanza un `HTTPException` de Starlette, tu manejador podrá capturarlo y manejarlo.

En este ejemplo, para poder tener ambos `HTTPException` en el mismo código, las excepciones de Starlette son renombradas a `StarletteHTTPException`:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### Reutilizar los manejadores de excepciones de **FastAPI** { #reuse-fastapis-exception-handlers }

Si quieres usar la excepción junto con los mismos manejadores de excepciones predeterminados de **FastAPI**, puedes importar y reutilizar los manejadores de excepciones predeterminados de `fastapi.exception_handlers`:

{* ../../docs_src/handling_errors/tutorial006_py39.py hl[2:5,15,21] *}

En este ejemplo solo estás `print`eando el error con un mensaje muy expresivo, pero te haces una idea. Puedes usar la excepción y luego simplemente reutilizar los manejadores de excepciones predeterminados.
