# Modelo de Response - Tipo de Retorno

Puedes declarar el tipo utilizado para el response anotando el **tipo de retorno** de la *path operation function*.

Puedes utilizar **anotaciones de tipos** de la misma manera que lo harías para datos de entrada en **parámetros** de función, puedes utilizar modelos de Pydantic, listas, diccionarios, valores escalares como enteros, booleanos, etc.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI usará este tipo de retorno para:

* **Validar** los datos devueltos.
    * Si los datos son inválidos (por ejemplo, falta un campo), significa que el código de *tu* aplicación está defectuoso, no devolviendo lo que debería, y retornará un error del servidor en lugar de devolver datos incorrectos. De esta manera, tú y tus clientes pueden estar seguros de que recibirán los datos y la forma de los datos esperada.
* Agregar un **JSON Schema** para el response, en la *path operation* de OpenAPI.
    * Esto será utilizado por la **documentación automática**.
    * También será utilizado por herramientas de generación automática de código de cliente.

Pero lo más importante:

* **Limitará y filtrará** los datos de salida a lo que se define en el tipo de retorno.
    * Esto es particularmente importante para la **seguridad**, veremos más sobre eso a continuación.

## Parámetro `response_model`

Hay algunos casos en los que necesitas o quieres devolver algunos datos que no son exactamente lo que declara el tipo.

Por ejemplo, podrías querer **devolver un diccionario** u objeto de base de datos, pero **declararlo como un modelo de Pydantic**. De esta manera el modelo de Pydantic haría toda la documentación de datos, validación, etc. para el objeto que devolviste (por ejemplo, un diccionario u objeto de base de datos).

Si añadiste la anotación del tipo de retorno, las herramientas y editores se quejarían con un error (correcto) diciéndote que tu función está devolviendo un tipo (por ejemplo, un dict) que es diferente de lo que declaraste (por ejemplo, un modelo de Pydantic).

En esos casos, puedes usar el parámetro del decorador de path operation `response_model` en lugar del tipo de retorno.

Puedes usar el parámetro `response_model` en cualquiera de las *path operations*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | Nota

Observa que `response_model` es un parámetro del método "decorador" (`get`, `post`, etc). No de tu *path operation function*, como todos los parámetros y el cuerpo.

///

`response_model` recibe el mismo tipo que declararías para un campo de modelo Pydantic, por lo que puede ser un modelo de Pydantic, pero también puede ser, por ejemplo, un `list` de modelos de Pydantic, como `List[Item]`.

FastAPI usará este `response_model` para hacer toda la documentación de datos, validación, etc. y también para **convertir y filtrar los datos de salida** a su declaración de tipo.

/// tip | Consejo

Si tienes chequeos estrictos de tipos en tu editor, mypy, etc., puedes declarar el tipo de retorno de la función como `Any`.

De esa manera le dices al editor que intencionalmente estás devolviendo cualquier cosa. Pero FastAPI todavía hará la documentación de datos, validación, filtrado, etc. con `response_model`.

///

### Prioridad del `response_model`

Si declaras tanto un tipo de retorno como un `response_model`, el `response_model` tomará prioridad y será utilizado por FastAPI.

De esta manera puedes añadir anotaciones de tipos correctas a tus funciones incluso cuando estás devolviendo un tipo diferente al modelo de response, para ser utilizado por el editor y herramientas como mypy. Y aún así puedes hacer que FastAPI realice la validación de datos, documentación, etc. usando el `response_model`.

También puedes usar `response_model=None` para desactivar la creación de un modelo de response para esa *path operation*, podrías necesitar hacerlo si estás añadiendo anotaciones de tipos para cosas que no son campos válidos de Pydantic, verás un ejemplo de eso en una de las secciones a continuación.

## Devolver los mismos datos de entrada

Aquí estamos declarando un modelo `UserIn`, contendrá una contraseña en texto plano:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// info | Información

Para usar `EmailStr`, primero instala <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email-validator`</a>.

Asegúrate de crear un [entorno virtual](../virtual-environments.md){.internal-link target=_blank}, activarlo, y luego instalarlo, por ejemplo:

```console
$ pip install email-validator
```

o con:

```console
$ pip install "pydantic[email]"
```

///

Y estamos usando este modelo para declarar nuestra entrada y el mismo modelo para declarar nuestra salida:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

Ahora, cada vez que un navegador esté creando un usuario con una contraseña, la API devolverá la misma contraseña en el response.

En este caso, podría no ser un problema, porque es el mismo usuario que envía la contraseña.

Pero si usamos el mismo modelo para otra *path operation*, podríamos estar enviando las contraseñas de nuestros usuarios a cada cliente.

/// danger | Peligro

Nunca almacenes la contraseña en texto plano de un usuario ni la envíes en un response como esta, a menos que conozcas todas las advertencias y sepas lo que estás haciendo.

///

## Añadir un modelo de salida

Podemos en cambio crear un modelo de entrada con la contraseña en texto plano y un modelo de salida sin ella:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

Aquí, aunque nuestra *path operation function* está devolviendo el mismo usuario de entrada que contiene la contraseña:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...hemos declarado el `response_model` para ser nuestro modelo `UserOut`, que no incluye la contraseña:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

Entonces, **FastAPI** se encargará de filtrar todos los datos que no estén declarados en el modelo de salida (usando Pydantic).

### `response_model` o Tipo de Retorno

En este caso, como los dos modelos son diferentes, si anotáramos el tipo de retorno de la función como `UserOut`, el editor y las herramientas se quejarían de que estamos devolviendo un tipo inválido, ya que son clases diferentes.

Por eso en este ejemplo tenemos que declararlo en el parámetro `response_model`.

...pero sigue leyendo abajo para ver cómo superar eso.

## Tipo de Retorno y Filtrado de Datos

Continuemos con el ejemplo anterior. Queríamos **anotar la función con un tipo**, pero queríamos poder devolver desde la función algo que en realidad incluya **más datos**.

Queremos que FastAPI continúe **filtrando** los datos usando el modelo de response. Para que, incluso cuando la función devuelva más datos, el response solo incluya los campos declarados en el modelo de response.

En el ejemplo anterior, debido a que las clases eran diferentes, tuvimos que usar el parámetro `response_model`. Pero eso también significa que no obtenemos el soporte del editor y las herramientas verificando el tipo de retorno de la función.

Pero en la mayoría de los casos en los que necesitamos hacer algo como esto, queremos que el modelo solo **filtre/elimine** algunos de los datos como en este ejemplo.

Y en esos casos, podemos usar clases y herencia para aprovechar las **anotaciones de tipos** de funciones para obtener mejor soporte en el editor y herramientas, y aún así obtener el **filtrado de datos** de FastAPI.

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

Con esto, obtenemos soporte de las herramientas, de los editores y mypy ya que este código es correcto en términos de tipos, pero también obtenemos el filtrado de datos de FastAPI.

¿Cómo funciona esto? Vamos a echarle un vistazo. 🤓

### Anotaciones de Tipos y Herramientas

Primero vamos a ver cómo los editores, mypy y otras herramientas verían esto.

`BaseUser` tiene los campos base. Luego `UserIn` hereda de `BaseUser` y añade el campo `password`, por lo que incluirá todos los campos de ambos modelos.

Anotamos el tipo de retorno de la función como `BaseUser`, pero en realidad estamos devolviendo una instancia de `UserIn`.

El editor, mypy y otras herramientas no se quejarán de esto porque, en términos de tipificación, `UserIn` es una subclase de `BaseUser`, lo que significa que es un tipo *válido* cuando se espera algo que es un `BaseUser`.

### Filtrado de Datos en FastAPI

Ahora, para FastAPI, verá el tipo de retorno y se asegurará de que lo que devuelves incluya **solo** los campos que están declarados en el tipo.

FastAPI realiza varias cosas internamente con Pydantic para asegurarse de que esas mismas reglas de herencia de clases no se utilicen para el filtrado de datos devueltos, de lo contrario, podrías terminar devolviendo muchos más datos de los que esperabas.

De esta manera, puedes obtener lo mejor de ambos mundos: anotaciones de tipos con **soporte de herramientas** y **filtrado de datos**.

## Verlo en la documentación

Cuando veas la documentación automática, puedes verificar que el modelo de entrada y el modelo de salida tendrán cada uno su propio JSON Schema:

<img src="/img/tutorial/response-model/image01.png">

Y ambos modelos se utilizarán para la documentación interactiva de la API:

<img src="/img/tutorial/response-model/image02.png">

## Otras Anotaciones de Tipos de Retorno

Podría haber casos en los que devuelvas algo que no es un campo válido de Pydantic y lo anotes en la función, solo para obtener el soporte proporcionado por las herramientas (el editor, mypy, etc).

### Devolver un Response Directamente

El caso más común sería [devolver un Response directamente como se explica más adelante en la documentación avanzada](../advanced/response-directly.md){.internal-link target=_blank}.

{* ../../docs_src/response_model/tutorial003_02.py hl[8,10:11] *}

Este caso simple es manejado automáticamente por FastAPI porque la anotación del tipo de retorno es la clase (o una subclase de) `Response`.

Y las herramientas también estarán felices porque tanto `RedirectResponse` como `JSONResponse` son subclases de `Response`, por lo que la anotación del tipo es correcta.

### Anotar una Subclase de Response

También puedes usar una subclase de `Response` en la anotación del tipo:

{* ../../docs_src/response_model/tutorial003_03.py hl[8:9] *}

Esto también funcionará porque `RedirectResponse` es una subclase de `Response`, y FastAPI manejará automáticamente este caso simple.

### Anotaciones de Tipos de Retorno Inválidas

Pero cuando devuelves algún otro objeto arbitrario que no es un tipo válido de Pydantic (por ejemplo, un objeto de base de datos) y lo anotas así en la función, FastAPI intentará crear un modelo de response de Pydantic a partir de esa anotación de tipo, y fallará.

Lo mismo sucedería si tuvieras algo como un <abbr title='Una unión entre múltiples tipos significa "cualquiera de estos tipos".'>union</abbr> entre diferentes tipos donde uno o más de ellos no son tipos válidos de Pydantic, por ejemplo esto fallaría 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...esto falla porque la anotación de tipo no es un tipo de Pydantic y no es solo una sola clase `Response` o subclase, es una unión (cualquiera de los dos) entre una `Response` y un `dict`.

### Desactivar el Modelo de Response

Continuando con el ejemplo anterior, puede que no quieras tener la validación de datos por defecto, documentación, filtrado, etc. que realiza FastAPI.

Pero puedes querer mantener la anotación del tipo de retorno en la función para obtener el soporte de herramientas como editores y verificadores de tipos (por ejemplo, mypy).

En este caso, puedes desactivar la generación del modelo de response configurando `response_model=None`:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

Esto hará que FastAPI omita la generación del modelo de response y de esa manera puedes tener cualquier anotación de tipo de retorno que necesites sin que afecte a tu aplicación FastAPI. 🤓

## Parámetros de codificación del Modelo de Response

Tu modelo de response podría tener valores por defecto, como:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (o `str | None = None` en Python 3.10) tiene un valor por defecto de `None`.
* `tax: float = 10.5` tiene un valor por defecto de `10.5`.
* `tags: List[str] = []` tiene un valor por defecto de una lista vacía: `[]`.

pero podrías querer omitirlos del resultado si no fueron en realidad almacenados.

Por ejemplo, si tienes modelos con muchos atributos opcionales en una base de datos NoSQL, pero no quieres enviar responses JSON muy largos llenos de valores por defecto.

### Usa el parámetro `response_model_exclude_unset`

Puedes configurar el parámetro del decorador de path operation `response_model_exclude_unset=True`:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

y esos valores por defecto no serán incluidos en el response, solo los valores realmente establecidos.

Entonces, si envías un request a esa *path operation* para el ítem con ID `foo`, el response (no incluyendo valores por defecto) será:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// info | Información

En Pydantic v1 el método se llamaba `.dict()`, fue deprecado (pero aún soportado) en Pydantic v2, y renombrado a `.model_dump()`.

Los ejemplos aquí usan `.dict()` para compatibilidad con Pydantic v1, pero deberías usar `.model_dump()` en su lugar si puedes usar Pydantic v2.

///

/// info | Información

FastAPI usa el método `.dict()` del modelo de Pydantic con <a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">su parámetro `exclude_unset`</a> para lograr esto.

///

/// info | Información

También puedes usar:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

como se describe en <a href="https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict" class="external-link" target="_blank">la documentación de Pydantic</a> para `exclude_defaults` y `exclude_none`.

///

#### Datos con valores para campos con valores por defecto

Pero si tus datos tienen valores para los campos del modelo con valores por defecto, como el artículo con ID `bar`:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

serán incluidos en el response.

#### Datos con los mismos valores que los valores por defecto

Si los datos tienen los mismos valores que los valores por defecto, como el artículo con ID `baz`:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI es lo suficientemente inteligente (de hecho, Pydantic es lo suficientemente inteligente) para darse cuenta de que, a pesar de que `description`, `tax` y `tags` tienen los mismos valores que los valores por defecto, fueron establecidos explícitamente (en lugar de tomados de los valores por defecto).

Por lo tanto, se incluirán en el response JSON.

/// tip | Consejo

Ten en cuenta que los valores por defecto pueden ser cualquier cosa, no solo `None`.

Pueden ser una lista (`[]`), un `float` de `10.5`, etc.

///

### `response_model_include` y `response_model_exclude`

También puedes usar los parámetros del decorador de path operation `response_model_include` y `response_model_exclude`.

Aceptan un `set` de `str` con el nombre de los atributos a incluir (omitiendo el resto) o excluir (incluyendo el resto).

Esto se puede usar como un atajo rápido si solo tienes un modelo de Pydantic y quieres eliminar algunos datos de la salida.

/// tip | Consejo

Pero todavía se recomienda usar las ideas anteriores, usando múltiples clases, en lugar de estos parámetros.

Esto se debe a que el JSON Schema generado en el OpenAPI de tu aplicación (y la documentación) aún será el del modelo completo, incluso si usas `response_model_include` o `response_model_exclude` para omitir algunos atributos.

Esto también se aplica a `response_model_by_alias` que funciona de manera similar.

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | Consejo

La sintaxis `{"name", "description"}` crea un `set` con esos dos valores.

Es equivalente a `set(["name", "description"])`.

///

#### Usar `list`s en lugar de `set`s

Si olvidas usar un `set` y usas un `list` o `tuple` en su lugar, FastAPI todavía lo convertirá a un `set` y funcionará correctamente:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Resumen

Usa el parámetro `response_model` del *decorador de path operation* para definir modelos de response y especialmente para asegurarte de que los datos privados sean filtrados.

Usa `response_model_exclude_unset` para devolver solo los valores establecidos explícitamente.
