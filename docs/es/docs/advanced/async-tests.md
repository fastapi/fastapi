# Tests Asíncronos

Ya has visto cómo probar tus aplicaciones de **FastAPI** usando el `TestClient` proporcionado. Hasta ahora, solo has visto cómo escribir tests sincrónicos, sin usar funciones `async`.

Poder usar funciones asíncronas en tus tests puede ser útil, por ejemplo, cuando consultas tu base de datos de forma asíncrona. Imagina que quieres probar el envío de requests a tu aplicación FastAPI y luego verificar que tu backend escribió exitosamente los datos correctos en la base de datos, mientras usas un paquete de base de datos asíncrono.

Veamos cómo podemos hacer que esto funcione.

## pytest.mark.anyio

Si queremos llamar funciones asíncronas en nuestros tests, nuestras funciones de test tienen que ser asíncronas. AnyIO proporciona un plugin útil para esto, que nos permite especificar que algunas funciones de test deben ser llamadas de manera asíncrona.

## HTTPX

Incluso si tu aplicación de **FastAPI** usa funciones `def` normales en lugar de `async def`, sigue siendo una aplicación `async` por debajo.

El `TestClient` hace algo de magia interna para llamar a la aplicación FastAPI asíncrona en tus funciones de test `def` normales, usando pytest estándar. Pero esa magia ya no funciona cuando lo usamos dentro de funciones asíncronas. Al ejecutar nuestros tests de manera asíncrona, ya no podemos usar el `TestClient` dentro de nuestras funciones de test.

El `TestClient` está basado en <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, y afortunadamente, podemos usarlo directamente para probar la API.

## Ejemplo

Para un ejemplo simple, consideremos una estructura de archivos similar a la descrita en [Aplicaciones Más Grandes](../tutorial/bigger-applications.md){.internal-link target=_blank} y [Testing](../tutorial/testing.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

El archivo `main.py` tendría:

{* ../../docs_src/async_tests/main.py *}

El archivo `test_main.py` tendría los tests para `main.py`, podría verse así ahora:

{* ../../docs_src/async_tests/test_main.py *}

## Ejecútalo

Puedes ejecutar tus tests como de costumbre vía:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## En Detalle

El marcador `@pytest.mark.anyio` le dice a pytest que esta función de test debe ser llamada asíncronamente:

{* ../../docs_src/async_tests/test_main.py hl[7] *}

/// tip | Consejo

Note que la función de test ahora es `async def` en lugar de solo `def` como antes al usar el `TestClient`.

///

Luego podemos crear un `AsyncClient` con la app y enviar requests asíncronos a ella, usando `await`.

{* ../../docs_src/async_tests/test_main.py hl[9:12] *}

Esto es equivalente a:

```Python
response = client.get('/')
```

...que usábamos para hacer nuestros requests con el `TestClient`.

/// tip | Consejo

Nota que estamos usando async/await con el nuevo `AsyncClient`: el request es asíncrono.

///

/// warning | Advertencia

Si tu aplicación depende de eventos de lifespan, el `AsyncClient` no activará estos eventos. Para asegurarte de que se activen, usa `LifespanManager` de <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>.

///

## Otras Llamadas a Funciones Asíncronas

Al ser la función de test asíncrona, ahora también puedes llamar (y `await`) otras funciones `async` además de enviar requests a tu aplicación FastAPI en tus tests, exactamente como las llamarías en cualquier otro lugar de tu código.

/// tip | Consejo

Si encuentras un `RuntimeError: Task attached to a different loop` al integrar llamadas a funciones asíncronas en tus tests (por ejemplo, cuando usas <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MotorClient de MongoDB</a>), recuerda crear instances de objetos que necesiten un loop de eventos solo dentro de funciones async, por ejemplo, en un callback `'@app.on_event("startup")`.

///
