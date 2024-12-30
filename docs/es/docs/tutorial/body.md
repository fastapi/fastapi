# Request Body

Cuando necesitas enviar datos desde un cliente (digamos, un navegador) a tu API, los envías como un **request body**.

Un **request** body es un dato enviado por el cliente a tu API. Un **response** body es el dato que tu API envía al cliente.

Tu API casi siempre tiene que enviar un **response** body. Pero los clientes no necesariamente necesitan enviar **request bodies** todo el tiempo, a veces solo solicitan un path, quizás con algunos parámetros de query, pero no envían un body.

Para declarar un **request** body, usas modelos de <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> con todo su poder y beneficios.

/// info | Información

Para enviar datos, deberías usar uno de estos métodos: `POST` (el más común), `PUT`, `DELETE` o `PATCH`.

Enviar un body con un request `GET` tiene un comportamiento indefinido en las especificaciones, no obstante, es soportado por FastAPI, solo para casos de uso muy complejos/extremos.

Como no se recomienda, la documentación interactiva con Swagger UI no mostrará la documentación para el body cuando se usa `GET`, y los proxies intermedios podrían no soportarlo.

///

## Importar `BaseModel` de Pydantic

Primero, necesitas importar `BaseModel` de `pydantic`:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## Crea tu modelo de datos

Luego, declaras tu modelo de datos como una clase que hereda de `BaseModel`.

Usa tipos estándar de Python para todos los atributos:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

Al igual que al declarar parámetros de query, cuando un atributo del modelo tiene un valor por defecto, no es obligatorio. De lo contrario, es obligatorio. Usa `None` para hacerlo opcional.

Por ejemplo, el modelo anterior declara un “`object`” JSON (o `dict` en Python) como:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...dado que `description` y `tax` son opcionales (con un valor por defecto de `None`), este “`object`” JSON también sería válido:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Decláralo como un parámetro

Para añadirlo a tu *path operation*, decláralo de la misma manera que declaraste parámetros de path y query:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...y declara su tipo como el modelo que creaste, `Item`.

## Resultados

Con solo esa declaración de tipo en Python, **FastAPI** hará lo siguiente:

* Leer el body del request como JSON.
* Convertir los tipos correspondientes (si es necesario).
* Validar los datos.
    * Si los datos son inválidos, devolverá un error claro e indicado, señalando exactamente dónde y qué fue lo incorrecto.
* Proporcionar los datos recibidos en el parámetro `item`.
    * Como lo declaraste en la función como de tipo `Item`, también tendrás todo el soporte del editor (autocompletado, etc.) para todos los atributos y sus tipos.
* Generar definiciones de <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> para tu modelo, que también puedes usar en cualquier otro lugar si tiene sentido para tu proyecto.
* Esquemas que serán parte del esquema de OpenAPI generado y usados por la <abbr title="User Interfaces">UIs</abbr> de documentación automática.

## Documentación automática

Los JSON Schemas de tus modelos serán parte del esquema OpenAPI generado y se mostrarán en la documentación API interactiva:

<img src="/img/tutorial/body/image01.png">

Y también se utilizarán en la documentación API dentro de cada *path operation* que los necesite:

<img src="/img/tutorial/body/image02.png">

## Soporte del editor

En tu editor, dentro de tu función, obtendrás anotaciones de tipos y autocompletado en todas partes (esto no sucedería si recibieras un `dict` en lugar de un modelo de Pydantic):

<img src="/img/tutorial/body/image03.png">

También recibirás chequeos de errores para operaciones de tipo incorrecto:

<img src="/img/tutorial/body/image04.png">

No es por casualidad, todo el framework fue construido alrededor de ese diseño.

Y fue rigurosamente probado en la fase de diseño, antes de cualquier implementación, para garantizar que funcionaría con todos los editores.

Incluso se hicieron algunos cambios en Pydantic para admitir esto.

Las capturas de pantalla anteriores se tomaron con <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Pero obtendrías el mismo soporte en el editor con <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> y la mayoría de los otros editores de Python:

<img src="/img/tutorial/body/image05.png">

/// tip | Consejo

Si usas <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> como tu editor, puedes usar el <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>.

Mejora el soporte del editor para modelos de Pydantic, con:

* autocompletado
* chequeo de tipos
* refactorización
* búsqueda
* inspecciones

///

## Usa el modelo

Dentro de la función, puedes acceder a todos los atributos del objeto modelo directamente:

{* ../../docs_src/body/tutorial002_py310.py *}

## Request body + parámetros de path

Puedes declarar parámetros de path y request body al mismo tiempo.

**FastAPI** reconocerá que los parámetros de función que coinciden con los parámetros de path deben ser **tomados del path**, y que los parámetros de función que se declaran como modelos de Pydantic deben ser **tomados del request body**.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## Request body + path + parámetros de query

También puedes declarar parámetros de **body**, **path** y **query**, todos al mismo tiempo.

**FastAPI** reconocerá cada uno de ellos y tomará los datos del lugar correcto.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Los parámetros de la función se reconocerán de la siguiente manera:

* Si el parámetro también se declara en el **path**, se utilizará como un parámetro de path.
* Si el parámetro es de un **tipo singular** (como `int`, `float`, `str`, `bool`, etc.), se interpretará como un parámetro de **query**.
* Si el parámetro se declara como del tipo de un **modelo de Pydantic**, se interpretará como un **request body**.

/// note | Nota

FastAPI sabrá que el valor de `q` no es requerido debido al valor por defecto `= None`.

El `str | None` (Python 3.10+) o `Union` en `Union[str, None]` (Python 3.8+) no es utilizado por FastAPI para determinar que el valor no es requerido, sabrá que no es requerido porque tiene un valor por defecto de `= None`.

Pero agregar las anotaciones de tipos permitirá que tu editor te brinde un mejor soporte y detecte errores.

///

## Sin Pydantic

Si no quieres usar modelos de Pydantic, también puedes usar parámetros **Body**. Consulta la documentación para [Body - Multiples Parametros: Valores singulares en body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
