# Cuerpo de la Petición (Request Body)

Cuando tienes que enviar datos desde un cliente (un navegador, por ejemplo) a tu API, lo haces en el cuerpo de la petición (**request body**).

Cuando hablamos del cuerpo de una petición (**request body**), nos referimos a los datos que se envían tanto desde el cliente hacia tu API como desde tu API al cliente.

Si bien en la mayoría de los casos tu API requiere enviar peticiones con los datos en el cuerpo (**request body**), en el caso de los clientes, no tiene por qué ser así.

Para declarar los datos del cuerpo de una petición (**request body**), tienes que usar los modelos de <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>, los cuales son muy versatiles y de gran ayuda.

!!! info
Para enviar datos, deberás usar uno de los siguentes métodos:`POST` (el metódo más común), `PUT`, `DELETE` o `PATCH`.

    Aunque el envío de datos en el cuerpo de una petición (**request body**) usando un método `GET` tiene un comportamiento inesperado según las especificaciones HTTP, FastAPI permite dicha acción para casos extremadamente complejos.

    Debido a que el envío de datos en el cuerpo de una petición en métodos `GET` es una acción no recomendada, por lo que la documentación interactiva del Swagger UI no mostrará dicha opción, con el fin de evitar posibles incompatibilidades.

## Importa `BaseModel` desde Pydantic

Primero, necesitarás importar `BaseModel` desde `pydantic`:

```Python hl_lines="4"
{!../../../docs_src/body/tutorial001.py!}
```

## Crea un modelo de datos

Debes declarar tu modelo de datos como una clase que hereda de `BaseModel`.

Utiliza los tipos de datos estándar de Python para los atributos:

```Python hl_lines="7-11"
{!../../../docs_src/body/tutorial001.py!}
```

Tendrás que hacer lo mismo a la hora de declarar los parametros de una consulta (query). Cuando un atributo de un modelo tiene un valor por defecto, no es obligatorio declararlo. Puedes usar `None` para hacer que sea opcional.

Por ejemplo, este modelo declara un objeto JSON (JSON "`object`") o un diccionario de Python (Python `dict`):

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...como `description` y `tax` son opcionales (con valor por defecto `None`), el siguiente objeto JSON (JSON "`object`") debería ser válido:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Declaración de parámetros

Para añadir la ruta de operación (_path operation_) como parámetro, puedes hacerlo de la misma forma en la que has declarado los parámetros de ruta (path) y consulta (query):

```Python hl_lines="18"
{!../../../docs_src/body/tutorial001.py!}
```

...y declara el tipo `Item` igual que el modelo que has creado anteriormente.

## Resultados

Solo con las declaraciones de tipos de Python, **FastAPI** realizará las siguientes acciones:

- Leer el cuerpo de una consulta como JSON.
- Convertir (en caso de ser necesario), los tipos correspondientes.
- Validar datos.
  - Si los datos no son válidos, se devolverá un error claro y preciso, indicando exactamente dónde y cuál es el dato incorrecto.
- Tener disponibles los datos recibidos en el parámetro `item`.
  - Como has declarado el parámetro en la función para que sea de tipo `Item`, además contarás con ayuda en tu editor (autocompletado, etc) para todos los atributos y sus tipos.
- Generar las definiciones en un <a href="https://json-schema.org" class="external-link" target="_blank">Esquema JSON</a> para tu modelo, que también puedes utilizar en cualquier otra parte que tenga sentido dentro de tu proyecto.
- Estos esquemas formarán parte de los esquemas generados por OpenAPI, y que ademas serán incorporados de forma automática en la documentación <abbr title="Interfaces de Usuarios">UIs</abbr>.

## Documentación automática

Los esquemas JSON de tus modelos serán parte del esquema generado por OpenApi, y serán mostrados en la documentación interactiva de API Docs:

<img src="/img/tutorial/body/image01.png">

Y además, se utilizarán en cada ruta de operación (_path operation_) que sea necesaria:

<img src="/img/tutorial/body/image02.png">

## Ayuda del Editor

En tu editor, dentro de todas tus funciones, tendrás autocompletado y ayuda con los tipos (Type hints). Esto no sería posible si en lugar del modelo de Pydantic, hubiéramos utilizado un dictionario (`dict`):

<img src="/img/tutorial/body/image03.png">

Además, tendrás señalamiento de errores para las operaciones que sean incorrectas:

<img src="/img/tutorial/body/image04.png">

No se trata de una casualidad, **FastAPI** ha sido construido entorno a este diseño.

Y ha sido probado a fondo durante la etapa de diseño, antes de realizar cualquier implementación, con el fin de asegurar que funcionará en todos los editores.

Para conseguir esto, incluso ha sido necesario realizar cambios en Pydantic.

Las capturas de pantalla anteriormente mostradas han sido obtenidas de<a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Sin embargo, todas las funcionalidades son completamente compatibles con <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> y la mayoría de editores para Python:

<img src="/img/tutorial/body/image05.png">

!!! tip
Si estás utilizando <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> como editor, puedes usar el<a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Plugin de Pydantic para PyCharm</a>.

    El uso de los modelos Pydantic mejoran la ayuda del editor en:
    * autocompletado
    * verificación de tipos
    * refactorización
    * búsquedas
    * inspecciones

## Uso del modelo

Tendrás acceso a todos los atributos del objecto del modelo desde dentro de la función:

```Python hl_lines="21"
{!../../../docs_src/body/tutorial002.py!}
```

## Cuerpo de la Petición (Request body) + parámetros de ruta (Path)

Puedes declarar al mismo tiempo parámetros de ruta y peticiones con datos en el cuerpo (**request body**)

**FastAPI** reconocerá tanto los parámetros de la función que deban ser **obtenidos desde la ruta (Path)**, así como aquellos parámetros que deban formar parte del modelo de Pydantic y que tengan que **obtenerse del cuerpo de la petición (Request Body)**

```Python hl_lines="17-18"
{!../../../docs_src/body/tutorial003.py!}
```

## Cuerpo de la Petición (Request body) + ruta (Path) + parámetros de consulta (Query)

También puedes declarar al mismo tiempo, parámetros de cuerpo (**body**), ruta (**path**) y consulta (**query**)

**FastAPI** reconocerá cada uno de ellos y recogerá los datos del sitio correcto.

```Python hl_lines="18"
{!../../../docs_src/body/tutorial004.py!}
```

Los parámetros de la función serán reconocidas de la siguente forma:

- Si el parámetro está declarado en la ruta (**path**), será utilizado como parámetro de ruta.
- Si el parámetro es un **tipo singular**, como entero (`int`), flotante (`float`), cadena de caracteres (`str`), booleano (`bool`), etcétera, serán interpretados como consulta (**query**)
- Si el parámetro ha sido declarado como **modelo Pydantic**, será interpretado como petición con cuerpo (**Request body**).

  !!! note
  FastAPI sabrá que el valor de `q` no es obligatorio, porque su valor por defecto es `= None`.

      En las cadenas de caracteres (`str`), `Optional` no es utilizado por FastAPI `Optional[str]`, pero su uso mejora la experiencia de usuario en tu editor a la hora de detectar errores.

## Sin Pydantic

Si no deseas usar los modelos de Pydantic, puedes usar directamente parámetros en el cuerpo (**Body**). Echa un vistazo a [Body - Parámetros Múltiples: Valores Singulares en el cuerpo](body-multiple-params.md#singular-values-in-body){.internal-link target=\_blank}.
