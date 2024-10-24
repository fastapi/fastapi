# <abbr title="También conocido como Cuerpo de la Solicitud. En inglés: Request Body">Cuerpo de la Petición</abbr>

Cuando necesitas enviar datos desde un cliente (digamos, un navegador) a tu API, los envías como un **cuerpo de la petición**.

Un cuerpo de **<abbr title="también conocido como solicitud. En inglés: request">petición</abbr>** son datos enviados por el cliente a la API. Un cuerpo de **respuesta** son los datos que la API envía al cliente.

Tu API casi siempre tiene que enviar un cuerpo de **<abbr title="también conocido en inglés como: response">respuesta</abbr>**. Pero los clientes no necesariamente necesitan enviar cuerpos de **<abbr title="también conocido como solicitud. En inglés: request">petición</abbr>** todo el tiempo.

Para declarar un cuerpo de **<abbr title="también conocido como solicitud. En inglés: request">petición</abbr>**, utiliza modelos <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> con todo su potencial y beneficios.

!!! info "Información"
    Para enviar datos, debes usar uno de: `POST` (el más común), `PUT`, `DELETE` o `PATCH`.

    Enviar un cuerpo con una petición `GET` tiene un comportamiento indefinido en las especificaciones, sin embargo, es compatible con FastAPI, solo para casos de uso muy complejos/extremos.

    Como no es recomendado, las documentaciones interactivas de Swagger UI no mostrarán la documentación del cuerpo cuando se use `GET`, y es posible que los servidores proxy en el medio no lo admitan.

## Importar `BaseModel` de Pydantic

Primero, necesitas importar `BaseModel` desde `pydantic`:

=== "Python 3.10+"

    ```Python hl_lines="2"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

## Crea tu modelo de datos

Después declara tu modelo de datos como una clase que hereda de `BaseModel`.

Utiliza tipos estándar de Python para todos los atributos:

=== "Python 3.10+"

    ```Python hl_lines="5-9"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="7-11"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

Lo mismo que cuando se declaran parámetros de consulta, cuando un atributo del modelo tiene un valor predeterminado, no es obligatorio. En caso contrario, es obligatorio. Utiliza `None` para que sea opcional.

Por ejemplo, este modelo declara un "`objeto`" JSON (o un `dict` de Python) como:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...como `description` y `tax` son opcionales (con un `None` como valor por defecto), este "`objeto`" JSON "`object`" también sería válido:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Decláralo como parámetro

Para agregarlo a su *operación de ruta*, decláralo de la misma manera que declaró los parámetros de la ruta y de la consulta:

=== "Python 3.10+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

...y declara su tipo como el modelo que creaste, `Item`.

## Resultados

Con solo esa declaración de tipo Python, **FastAPI** hará lo siguiente:

* Lee el cuerpo de la <abbr title="también conocido como solicitud. En inglés: request">petición</abbr> como JSON.
* Convierte los tipos correspondientes (si es necesario).
* Valida los datos.
     * Si los datos no son válidos, devolverá un error bonito y claro, indicando exactamente dónde y cuál fue el dato incorrecto.
* Te dará los datos recibidos en el parámetro `item`.
     * Como lo declaraste en la función como de tipo `Item`, también tendrás todo el soporte del editor (completado, etc.) para todos los atributos y sus tipos.
* Genera definiciones del <a href="https://json-schema.org" class="external-link" target="_blank"><abbr title="también conocido en inglés como: JSON Schema">Esquema JSON</abbr></a> para su modelo, que también podrás usarlas en cualquier otro lugar que desees si tiene sentido para tu proyecto.
* Esos esquemas formarán parte del esquema OpenAPI generado y serán utilizados por la documentación automática de las <abbr title="User Interfaces">UIs</abbr>.

## Documentación automática

Los <abbr title="también conocido en inglés como: JSON Schemas">Esquemas JSON</abbr> de tus modelos serán parte de su esquema generado por OpenAPI y se mostrarán en las documentaciones interactivas de la API:

<img src="/img/tutorial/body/image01.png">

Y también se usará en la documentación de la API dentro de cada *operación de ruta* que los necesite:

<img src="/img/tutorial/body/image02.png">

## Soporte del editor

En tu editor, dentro de tu función obtendrás sugerencias de tipo y autocompletado en todas partes (esto no sucedería si recibiera un `dict` en lugar de un modelo Pydantic):

<img src="/img/tutorial/body/image03.png">

También obtienes comprobaciones de errores para operaciones incorrectas de tipo:

<img src="/img/tutorial/body/image04.png">

Esto no es casualidad, todo el framework se construyó en torno a ese diseño.

Y se probó minuciosamente en la fase de diseño, antes de cualquier implementación, para garantizar que funcionara con todos los editores.

Incluso hubo algunos cambios en el propio Pydantic para respaldar esto.

Las capturas de pantalla anteriores fueron tomadas con <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Pero obtendrías el mismo soporte de editor con <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> y la mayoría de los otros editores de Python:

<img src="/img/tutorial/body/image05.png">

!!! tip "Consejo"
    Sí usas <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> como tu editor, puedes usar <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>.

    Esto mejora el soporte del editor para modelos Pydantic, con:

    * autocompletado
    * chequeo  de tipo
    * refactorización
    * busquedas
    * inspecciones

## Usa el modelo

Dentro de la función, puedes acceder a todos los atributos del modelo de objeto directamente:

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/body/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="21"
    {!> ../../../docs_src/body/tutorial002.py!}
    ```

## <abbr title="también conocido como Cuerpo de la Solicitud. En inglés: Request Body">Cuerpo de la Petición</abbr> + parámetros de ruta

Puedes declarar parámetros de ruta y cuerpo de la petición al mismo tiempo.

**FastAPI** reconocerá que los parámetros de función que coinciden con los parámetros de la ruta deben **tomarse de la ruta**, y que los parámetros de función que se declaran como modelos de Pydantic deben **tomarse del cuerpo de la petición o solicitud**.

=== "Python 3.10+"

    ```Python hl_lines="15-16"
    {!> ../../../docs_src/body/tutorial003_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="17-18"
    {!> ../../../docs_src/body/tutorial003.py!}
    ```

## <abbr title="también conocido como Cuerpo de la Solicitud. En inglés: Request Body">Cuerpo de la Petición</abbr> + ruta + parámetros de consulta

Puedes declarar **cuerpo**, parámetros  de **ruta** y **consulta**, todos al mismo tiempo.

**FastAPI** reconocerá cada uno de ellos y tomará los datos del lugar correcto.

=== "Python 3.10+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/body/tutorial004_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body/tutorial004.py!}
    ```

Los parámetros de la función se reconocerán de la siguiente manera:

* Si el parámetro también se declara en **ruta**, se utilizará como parámetro de ruta.
* Si el parámetro es de **tipo singular** (como `int`, `float`, `str`, `bool`, etc.) se interpretará como un parámetro de **consulta**.
* Si el parámetro se declara como del tipo de **modelo Pydantic**, se interpretará como un **cuerpo** de la petición.

!!! note "Nota"
    FastAPI sabrá que el valor de `q` no es necesario debido al valor predeterminado `= None`.

    FastAPI no utiliza `Union` en `Union[str, None]`, pero permitirá que su editor le brinde un mejor soporte y detecte errores.

## Sin Pydantic

Si no deseas utilizar modelos de Pydantic, también puedes utilizar los parámetros **Body**. Consulta la documentación para [Cuerpo - Múltiples parámetros: valores singulares en el cuerpo](body-multiple-params.md#valores-singulares-en-el-cuerpo){.internal-link target=_blank}.
