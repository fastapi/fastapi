# Testing

Gracias a <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a>, escribir pruebas para aplicaciones de **FastAPI** es fácil y agradable.

Está basado en <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, que a su vez está diseñado basado en Requests, por lo que es muy familiar e intuitivo.

Con él, puedes usar <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> directamente con **FastAPI**.

## Usando `TestClient`

/// info | Información

Para usar `TestClient`, primero instala <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, activarlo y luego instalarlo, por ejemplo:

```console
$ pip install httpx
```

///

Importa `TestClient`.

Crea un `TestClient` pasándole tu aplicación de **FastAPI**.

Crea funciones con un nombre que comience con `test_` (esta es la convención estándar de `pytest`).

Usa el objeto `TestClient` de la misma manera que con `httpx`.

Escribe declaraciones `assert` simples con las expresiones estándar de Python que necesites revisar (otra vez, estándar de `pytest`).

{* ../../docs_src/app_testing/tutorial001.py hl[2,12,15:18] *}

/// tip | Consejo

Nota que las funciones de prueba son `def` normales, no `async def`.

Y las llamadas al cliente también son llamadas normales, sin usar `await`.

Esto te permite usar `pytest` directamente sin complicaciones.

///

/// note | Nota Técnica

También podrías usar `from starlette.testclient import TestClient`.

**FastAPI** proporciona el mismo `starlette.testclient` como `fastapi.testclient` solo por conveniencia para ti, el desarrollador. Pero proviene directamente de Starlette.

///

/// tip | Consejo

Si quieres llamar a funciones `async` en tus pruebas además de enviar solicitudes a tu aplicación FastAPI (por ejemplo, funciones asincrónicas de bases de datos), echa un vistazo a las [Pruebas Asincrónicas](../advanced/async-tests.md){.internal-link target=_blank} en el tutorial avanzado.

///

## Separando pruebas

En una aplicación real, probablemente tendrías tus pruebas en un archivo diferente.

Y tu aplicación de **FastAPI** también podría estar compuesta de varios archivos/módulos, etc.

### Archivo de aplicación **FastAPI**

Digamos que tienes una estructura de archivos como se describe en [Aplicaciones Más Grandes](bigger-applications.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

En el archivo `main.py` tienes tu aplicación de **FastAPI**:

{* ../../docs_src/app_testing/main.py *}

### Archivo de prueba

Entonces podrías tener un archivo `test_main.py` con tus pruebas. Podría estar en el mismo paquete de Python (el mismo directorio con un archivo `__init__.py`):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Debido a que este archivo está en el mismo paquete, puedes usar importaciones relativas para importar el objeto `app` desde el módulo `main` (`main.py`):

{* ../../docs_src/app_testing/test_main.py hl[3] *}

...y tener el código para las pruebas tal como antes.

## Pruebas: ejemplo extendido

Ahora extiende este ejemplo y añade más detalles para ver cómo escribir pruebas para diferentes partes.

### Archivo de aplicación **FastAPI** extendido

Continuemos con la misma estructura de archivos que antes:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Digamos que ahora el archivo `main.py` con tu aplicación de **FastAPI** tiene algunas otras **path operations**.

Tiene una operación `GET` que podría devolver un error.

Tiene una operación `POST` que podría devolver varios errores.

Ambas *path operations* requieren un `X-Token` header.

//// tab | Python 3.10+

```Python
{!> ../../docs_src/app_testing/app_b_an_py310/main.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/app_testing/app_b_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/app_testing/app_b_an/main.py!}
```

////

//// tab | Python 3.10+ sin Anotar

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ sin Anotar

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### Archivo de prueba extendido

Podrías entonces actualizar `test_main.py` con las pruebas extendidas:

{* ../../docs_src/app_testing/app_b/test_main.py *}

Cada vez que necesites que el cliente pase información en el request y no sepas cómo, puedes buscar (Googlear) cómo hacerlo en `httpx`, o incluso cómo hacerlo con `requests`, dado que el diseño de HTTPX está basado en el diseño de Requests.

Luego simplemente haces lo mismo en tus pruebas.

Por ejemplo:

* Para pasar un parámetro de *path* o *query*, añádelo a la URL misma.
* Para pasar un cuerpo JSON, pasa un objeto de Python (por ejemplo, un `dict`) al parámetro `json`.
* Si necesitas enviar *Form Data* en lugar de JSON, usa el parámetro `data` en su lugar.
* Para pasar *headers*, usa un `dict` en el parámetro `headers`.
* Para *cookies*, un `dict` en el parámetro `cookies`.

Para más información sobre cómo pasar datos al backend (usando `httpx` o el `TestClient`) revisa la <a href="https://www.python-httpx.org" class="external-link" target="_blank">documentación de HTTPX</a>.

/// info | Información

Ten en cuenta que el `TestClient` recibe datos que pueden ser convertidos a JSON, no modelos de Pydantic.

Si tienes un modelo de Pydantic en tu prueba y quieres enviar sus datos a la aplicación durante las pruebas, puedes usar el `jsonable_encoder` descrito en [Codificador Compatible con JSON](encoder.md){.internal-link target=_blank}.

///

## Ejecútalo

Después de eso, solo necesitas instalar `pytest`.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, activarlo y luego instalarlo, por ejemplo:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Detectará los archivos y pruebas automáticamente, ejecutará las mismas y te reportará los resultados.

Ejecuta las pruebas con:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
