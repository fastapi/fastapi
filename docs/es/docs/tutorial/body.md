# Petición Body

Cuando necesitas enviar datos desde un cliente (digamos, un navegador) a tu API, los envías como una **petición body**.

Una **petición** body son datos enviados por el cliente a tu API. Una **respuesta** body son los datos que tu API le envía al cliente.

Tu API casi siempre debe enviar una **respuesta** body, pero el cliente no necesariamente necesita enviar **peticiones** body todo el tiempo.

Para declarar una **petición** body, usas modelos de <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> con todo su poder y sus beneficios.

!!! info
    Para enviar datos, debes usar uno de estos: `POST` (el más común), `PUT`, `DELETE` o `PATCH`.

    Enviar un body con una petición `GET` tiene un comportamiento indefinido en las especificaciones, no obstante, es soportado por FastAPI, solo para casos de uso muy complejos o extremos.

    Como se desaconseja, la documentación interactiva con Swagger UI no mostrará la documentación del cuerpo cuando se use `GET`, y puede ser que los proxies en el medio no lo soporten.

## Importar `BaseModel` de Pydantic

Primero, necesitas importar `BaseModel` de `pydantic`:

```Python hl_lines="4"
{!../../../docs_src/body/tutorial001.py!}
```

## Crea tu modelo de datos

Luego, declara tu modelo de datos como una clase que hereda de `BaseModel`.

Usa tipos estándar de Python para todos los atributos:

```Python hl_lines="7-11"
{!../../../docs_src/body/tutorial001.py!}
```

Lo mismo que al declarar parámetros de consulta [query], cuando un atributo de un modelo tiene un valor por defecto, no es requerido. De lo contrario, es requerido. Usa `None` para hacerlo opcional.

Por ejemplo, el siguiente modelo declara un "`objeto`" JSON (o un `dict` de Python) así:

```JSON
{
    "nombre": "Foo",
    "descripción": "Una descripción opcional",
    "precio": 45.2,
    "impuesto": 3.5
}
```

... como `descripción` e `impuesto` son opcionales (con un valor por defecto `None`), este "`objeto`" JSON también sería válido:

```JSON
{
    "nombre": "Foo",
    "precio": 45.2
}
```

## Declararlo como parámetro

Para agregarlo a tu *ruta de operación*, decláralo de la misma manera que declaraste la ruta y los parámetros de consulta:

```Python hl_lines="18"
{!../../../docs_src/body/tutorial001.py!}
```

... y declara su tipo como el del modelo que creaste, `Item`.

## Resultados

Solo con esa declaración de tipo Python, **FastAPI** hará lo siguiente:

* Leerá el cuerpo de la petición como JSON.
* Convertirá los correspondientes tipos (si es necesario).
* Validará los datos.
    * Si los datos son inválidos, retornará un error lindo y claro, indicando exactamente cuáles son los datos incorrectos y dónde están.
* Te dará los datos recibidos en el parámetro `item`.
    * Como lo declaraste en la función para ser de tipo `Item`, también tendrás el soporte del editor (completación, etc.) para todos los atributos y sus tipos.
* Generará definiciones de <a href="https://json-schema.org" class="external-link" target="_blank">Esquema JSON</a> para tu modelo que también puedes usar en cualquier otro lugar, si tiene sentido para tu proyecto.
* Estos esquemas harán parte del esquema OpenAPI generado, y serán usados por la documentación <abbr title="User Interfaces">UIs</abbr> automática.

## Documentación automática

Los Esquemas JSON de tus modelos serán parte de tu esquema OpenAPI generado, y se mostrarán en la documentación API interactiva:

<img src="/img/tutorial/body/image01.png">

Y también serán usados en la documentación de la API dentro de cada *ruta de operaciones* que los necesite:

<img src="/img/tutorial/body/image02.png">

## Soporte del editor

En tu editor, dentro de tu función obtendrás sugerencias de tipo y completación en todas partes (esto no debería pasar si recibes un `dict` en vez de un modelo Pydantic):

<img src="/img/tutorial/body/image03.png">

También obtienes comprobaciones de error para operaciones de tipo incorrecto:

<img src="/img/tutorial/body/image04.png">

Esto no es casual, todo el marco se construyó alrededor de ese diseño.

Y fue probado a fondo en la fase de diseño, antes de cualquier implementación, para asegurarse de que funcionara con todos los editores. Incluso hubo algunos cambios en Pydantic para respaldar esto.

Las capturas de pantalla anteriores fueron tomadas con <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>, pero obtendrías el mismo soporte de editor con <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> y la mayoría de los editores de Python:

<img src="/img/tutorial/body/image05.png">

!!! tip
    Si usas <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> como editor, puedes usar el <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Plugin Pydantic PyCharm</a>.

    Esto mejora el soporte del editor para modelos de Pydantic, con:

    * auto-completación
    * verificación de tipos
    * refactorización
    * búsqueda
    * inspecciones

## Uso del modelo

Dentro de la función, puedes acceder a todos los atributos del objeto modelo directamente:

```Python hl_lines="21"
{!../../../docs_src/body/tutorial002.py!}
```

## Petición body + parámetros de ruta

Puedes declarar parámetros de ruta y peticiones del body al mismo tiempo.

**FastAPI** reconocerá que los parámetros de la función que coinciden con los parámetros de ruta deben ser **tomados de la ruta**, y que los parámetros de la función que son declarados para ser modelos de Pydantic deben ser **tomados de la petición body**.

```Python hl_lines="17-18"
{!../../../docs_src/body/tutorial003.py!}
```

## Petición body + ruta + parámetros de consulta [query]

También puedes declarar los parámetros del **body**, la **ruta** y la **consulta**, todo al mismo tiempo.

**FastAPI** reconocerá cada uno de ellos y tomará los datos del lugar correcto.

```Python hl_lines="18"
{!../../../docs_src/body/tutorial004.py!}
```

Los parámetros de la función se reconocerán de la siguiente manera:

* Si el parámetro también se declara en la **ruta**, se utilizará como parámetro de ruta.
* Si el parámetro es de **tipo singular** (como `int`, `float`, `str`, `bool`, etc.) se interpretará como un parámetro de **consulta**.
* Si se declara que el parámetro es de un tipo de **modelo de Pydantic**, se interpretará como una petición **body**.

!!! nota
    **FastAPI** sabrá que el valor de `q` no es necesario debido al valor predeterminado `= None`.

    **FastAPI** no utiliza el `Optional` en` Optional [str] `, pero le permitirá a tu editor brindarle un mejor soporte y detectar errores.

## Sin Pydantic

Si no quieres usar los modelos de Pydantic, también puedes usar parámetros **Body**. Consulta la documentación para [Body - Parámetros Múltiples: Valores singulares en el cuerpo] (body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
