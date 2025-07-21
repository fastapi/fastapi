# Parámetros de Query y Validaciones de String

**FastAPI** te permite declarar información adicional y validación para tus parámetros.

Tomemos esta aplicación como ejemplo:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

El parámetro de query `q` es del tipo `Union[str, None]` (o `str | None` en Python 3.10), lo que significa que es de tipo `str` pero también podría ser `None`, y de hecho, el valor por defecto es `None`, así que FastAPI sabrá que no es requerido.

/// note | Nota

FastAPI sabrá que el valor de `q` no es requerido por el valor por defecto `= None`.

El `Union` en `Union[str, None]` permitirá a tu editor darte un mejor soporte y detectar errores.

///

## Validaciones adicionales

Vamos a hacer que, aunque `q` sea opcional, siempre que se proporcione, **su longitud no exceda los 50 caracteres**.

### Importar `Query` y `Annotated`

Para lograr eso, primero importa:

* `Query` desde `fastapi`
* `Annotated` desde `typing` (o desde `typing_extensions` en Python por debajo de 3.9)

//// tab | Python 3.10+

En Python 3.9 o superior, `Annotated` es parte de la biblioteca estándar, así que puedes importarlo desde `typing`.

```Python hl_lines="1  3"
{!> ../../docs_src/query_params_str_validations/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.8+

En versiones de Python por debajo de 3.9 importas `Annotated` desde `typing_extensions`.

Ya estará instalado con FastAPI.

```Python hl_lines="3-4"
{!> ../../docs_src/query_params_str_validations/tutorial002_an.py!}
```

////

/// info | Información

FastAPI añadió soporte para `Annotated` (y empezó a recomendarlo) en la versión 0.95.0.

Si tienes una versión más antigua, obtendrás errores al intentar usar `Annotated`.

Asegúrate de [Actualizar la versión de FastAPI](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} a al menos 0.95.1 antes de usar `Annotated`.

///

## Usar `Annotated` en el tipo del parámetro `q`

¿Recuerdas que te dije antes que `Annotated` puede ser usado para agregar metadatos a tus parámetros en la [Introducción a Tipos de Python](../python-types.md#type-hints-with-metadata-annotations){.internal-link target=_blank}?

Ahora es el momento de usarlo con FastAPI. 🚀

Teníamos esta anotación de tipo:

//// tab | Python 3.10+

```Python
q: str | None = None
```

////

//// tab | Python 3.8+

```Python
q: Union[str, None] = None
```

////

Lo que haremos es envolver eso con `Annotated`, para que se convierta en:

//// tab | Python 3.10+

```Python
q: Annotated[str | None] = None
```

////

//// tab | Python 3.8+

```Python
q: Annotated[Union[str, None]] = None
```

////

Ambas versiones significan lo mismo, `q` es un parámetro que puede ser un `str` o `None`, y por defecto, es `None`.

Ahora vamos a lo divertido. 🎉

## Agregar `Query` a `Annotated` en el parámetro `q`

Ahora que tenemos este `Annotated` donde podemos poner más información (en este caso algunas validaciones adicionales), agrega `Query` dentro de `Annotated`, y establece el parámetro `max_length` a `50`:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

Nota que el valor por defecto sigue siendo `None`, por lo que el parámetro sigue siendo opcional.

Pero ahora, al tener `Query(max_length=50)` dentro de `Annotated`, le estamos diciendo a FastAPI que queremos que tenga **validación adicional** para este valor, queremos que tenga un máximo de 50 caracteres. 😎

/// tip | Consejo

Aquí estamos usando `Query()` porque este es un **parámetro de query**. Más adelante veremos otros como `Path()`, `Body()`, `Header()`, y `Cookie()`, que también aceptan los mismos argumentos que `Query()`.

///

FastAPI ahora:

* **Validará** los datos asegurándose de que la longitud máxima sea de 50 caracteres
* Mostrará un **error claro** para el cliente cuando los datos no sean válidos
* **Documentará** el parámetro en el OpenAPI esquema *path operation* (así aparecerá en la **UI de documentación automática**)

## Alternativa (antigua): `Query` como valor por defecto

Versiones anteriores de FastAPI (antes de <abbr title="antes de 2023-03">0.95.0</abbr>) requerían que usaras `Query` como el valor por defecto de tu parámetro, en lugar de ponerlo en `Annotated`. Hay una alta probabilidad de que veas código usándolo alrededor, así que te lo explicaré.

/// tip | Consejo

Para nuevo código y siempre que sea posible, usa `Annotated` como se explicó arriba. Hay múltiples ventajas (explicadas a continuación) y no hay desventajas. 🍰

///

Así es como usarías `Query()` como el valor por defecto de tu parámetro de función, estableciendo el parámetro `max_length` a 50:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

Ya que en este caso (sin usar `Annotated`) debemos reemplazar el valor por defecto `None` en la función con `Query()`, ahora necesitamos establecer el valor por defecto con el parámetro `Query(default=None)`, esto sirve al mismo propósito de definir ese valor por defecto (al menos para FastAPI).

Entonces:

```Python
q: Union[str, None] = Query(default=None)
```

...hace que el parámetro sea opcional, con un valor por defecto de `None`, lo mismo que:

```Python
q: Union[str, None] = None
```

Y en Python 3.10 y superior:

```Python
q: str | None = Query(default=None)
```

...hace que el parámetro sea opcional, con un valor por defecto de `None`, lo mismo que:

```Python
q: str | None = None
```

Pero las versiones de `Query` lo declaran explícitamente como un parámetro de query.

/// info | Información

Ten en cuenta que la parte más importante para hacer un parámetro opcional es la parte:

```Python
= None
```

o la parte:

```Python
= Query(default=None)
```

ya que usará ese `None` como el valor por defecto, y de esa manera hará el parámetro **no requerido**.

La parte `Union[str, None]` permite que tu editor brinde un mejor soporte, pero no es lo que le dice a FastAPI que este parámetro no es requerido.

///

Luego, podemos pasar más parámetros a `Query`. En este caso, el parámetro `max_length` que se aplica a los strings:

```Python
q: Union[str, None] = Query(default=None, max_length=50)
```

Esto validará los datos, mostrará un error claro cuando los datos no sean válidos, y documentará el parámetro en el esquema del *path operation* de OpenaPI.

### `Query` como valor por defecto o en `Annotated`

Ten en cuenta que cuando uses `Query` dentro de `Annotated` no puedes usar el parámetro `default` para `Query`.

En su lugar utiliza el valor por defecto real del parámetro de la función. De lo contrario, sería inconsistente.

Por ejemplo, esto no está permitido:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...porque no está claro si el valor por defecto debería ser `"rick"` o `"morty"`.

Así que utilizarías (preferentemente):

```Python
q: Annotated[str, Query()] = "rick"
```

...o en code bases más antiguos encontrarás:

```Python
q: str = Query(default="rick")
```

### Ventajas de `Annotated`

**Usar `Annotated` es recomendado** en lugar del valor por defecto en los parámetros de función, es **mejor** por múltiples razones. 🤓

El valor **por defecto** del **parámetro de función** es el valor **real por defecto**, eso es más intuitivo con Python en general. 😌

Podrías **llamar** a esa misma función en **otros lugares** sin FastAPI, y **funcionaría como se espera**. Si hay un parámetro **requerido** (sin un valor por defecto), tu **editor** te avisará con un error, **Python** también se quejará si lo ejecutas sin pasar el parámetro requerido.

Cuando no usas `Annotated` y en su lugar usas el estilo de valor por defecto **(antiguo)**, si llamas a esa función sin FastAPI en **otros lugares**, tienes que **recordar** pasar los argumentos a la función para que funcione correctamente, de lo contrario, los valores serán diferentes de lo que esperas (por ejemplo, `QueryInfo` o algo similar en lugar de `str`). Y tu editor no se quejará, y Python no se quejará al ejecutar esa función, solo cuando los errores dentro de las operaciones hagan que funcione incorrectamente.

Dado que `Annotated` puede tener más de una anotación de metadato, ahora podrías incluso usar la misma función con otras herramientas, como <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">Typer</a>. 🚀

## Agregar más validaciones

También puedes agregar un parámetro `min_length`:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## Agregar expresiones regulares

Puedes definir una <abbr title="Una expresión regular, regex o regexp es una secuencia de caracteres que define un patrón de búsqueda para strings.">expresión regular</abbr> `pattern` que el parámetro debe coincidir:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

Este patrón específico de expresión regular comprueba que el valor recibido del parámetro:

* `^`: comience con los siguientes caracteres, no tiene caracteres antes.
* `fixedquery`: tiene el valor exacto `fixedquery`.
* `$`: termina allí, no tiene más caracteres después de `fixedquery`.

Si te sientes perdido con todas estas ideas de **"expresión regular"**, no te preocupes. Son un tema difícil para muchas personas. Aún puedes hacer muchas cosas sin necesitar expresiones regulares todavía.

Pero cuando las necesites y vayas a aprenderlas, ya sabes que puedes usarlas directamente en **FastAPI**.

### Pydantic v1 `regex` en lugar de `pattern`

Antes de la versión 2 de Pydantic y antes de FastAPI 0.100.0, el parámetro se llamaba `regex` en lugar de `pattern`, pero ahora está en desuso.

Todavía podrías ver algo de código que lo usa:

//// tab | Pydantic v1

{* ../../docs_src/query_params_str_validations/tutorial004_regex_an_py310.py hl[11] *}

////

Pero que sepas que esto está deprecado y debería actualizarse para usar el nuevo parámetro `pattern`. 🤓

## Valores por defecto

Puedes, por supuesto, usar valores por defecto diferentes de `None`.

Digamos que quieres declarar el parámetro de query `q` para que tenga un `min_length` de `3`, y para que tenga un valor por defecto de `"fixedquery"`:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py39.py hl[9] *}

/// note | Nota

Tener un valor por defecto de cualquier tipo, incluyendo `None`, hace que el parámetro sea opcional (no requerido).

///

## Parámetros requeridos

Cuando no necesitamos declarar más validaciones o metadatos, podemos hacer que el parámetro de query `q` sea requerido simplemente no declarando un valor por defecto, como:

```Python
q: str
```

en lugar de:

```Python
q: Union[str, None] = None
```

Pero ahora lo estamos declarando con `Query`, por ejemplo, como:

//// tab | Annotated

```Python
q: Annotated[Union[str, None], Query(min_length=3)] = None
```

////

//// tab | non-Annotated

```Python
q: Union[str, None] = Query(default=None, min_length=3)
```

////

Así que, cuando necesites declarar un valor como requerido mientras usas `Query`, simplemente puedes no declarar un valor por defecto:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py39.py hl[9] *}

### Requerido, puede ser `None`

Puedes declarar que un parámetro puede aceptar `None`, pero que aún así es requerido. Esto obligaría a los clientes a enviar un valor, incluso si el valor es `None`.

Para hacer eso, puedes declarar que `None` es un tipo válido pero aún usar `...` como el valor por defecto:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

/// tip | Consejo

Pydantic, que es lo que impulsa toda la validación y serialización de datos en FastAPI, tiene un comportamiento especial cuando usas `Optional` o `Union[Something, None]` sin un valor por defecto, puedes leer más al respecto en la documentación de Pydantic sobre <a href="https://docs.pydantic.dev/2.3/usage/models/#required-optional-fields" class="external-link" target="_blank">Campos requeridos</a>.

///

/// tip | Consejo

Recuerda que en la mayoría de los casos, cuando algo es requerido, puedes simplemente omitir el default, así que normalmente no tienes que usar `...`.

///

## Lista de parámetros de Query / múltiples valores

Cuando defines un parámetro de query explícitamente con `Query` también puedes declararlo para recibir una lista de valores, o dicho de otra manera, para recibir múltiples valores.

Por ejemplo, para declarar un parámetro de query `q` que puede aparecer varias veces en la URL, puedes escribir:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

Entonces, con una URL como:

```
http://localhost:8000/items/?q=foo&q=bar
```

recibirías los múltiples valores del *query parameter* `q` (`foo` y `bar`) en una `list` de Python dentro de tu *path operation function*, en el *parámetro de función* `q`.

Entonces, el response a esa URL sería:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | Consejo

Para declarar un parámetro de query con un tipo de `list`, como en el ejemplo anterior, necesitas usar explícitamente `Query`, de lo contrario sería interpretado como un request body.

///

La documentación interactiva de API se actualizará en consecuencia, para permitir múltiples valores:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Lista de parámetros de Query / múltiples valores con valores por defecto

Y también puedes definir un valor por defecto `list` de valores si no se proporcionan ninguno:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py39.py hl[9] *}

Si vas a:

```
http://localhost:8000/items/
```

el valor por defecto de `q` será: `["foo", "bar"]` y tu response será:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Usando solo `list`

También puedes usar `list` directamente en lugar de `List[str]` (o `list[str]` en Python 3.9+):

{* ../../docs_src/query_params_str_validations/tutorial013_an_py39.py hl[9] *}

/// note | Nota

Ten en cuenta que en este caso, FastAPI no comprobará el contenido de la lista.

Por ejemplo, `List[int]` comprobaría (y documentaría) que el contenido de la lista son enteros. Pero `list` sola no lo haría.

///

## Declarar más metadatos

Puedes agregar más información sobre el parámetro.

Esa información se incluirá en el OpenAPI generado y será utilizada por las interfaces de usuario de documentación y herramientas externas.

/// note | Nota

Ten en cuenta que diferentes herramientas podrían tener diferentes niveles de soporte de OpenAPI.

Algunas de ellas podrían no mostrar toda la información extra declarada todavía, aunque en la mayoría de los casos, la funcionalidad faltante ya está planificada para desarrollo.

///

Puedes agregar un `title`:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

Y una `description`:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Alias para parámetros

Imagina que quieres que el parámetro sea `item-query`.

Como en:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Pero `item-query` no es un nombre de variable válido en Python.

Lo más cercano sería `item_query`.

Pero aún necesitas que sea exactamente `item-query`...

Entonces puedes declarar un `alias`, y ese alias será usado para encontrar el valor del parámetro:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Declarar parámetros obsoletos

Ahora digamos que ya no te gusta este parámetro.

Tienes que dejarlo allí por un tiempo porque hay clientes usándolo, pero quieres que la documentación lo muestre claramente como <abbr title="obsoleto, se recomienda no usarlo">deprecated</abbr>.

Luego pasa el parámetro `deprecated=True` a `Query`:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

La documentación lo mostrará así:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## Excluir parámetros de OpenAPI

Para excluir un parámetro de query del esquema de OpenAPI generado (y por lo tanto, de los sistemas de documentación automática), establece el parámetro `include_in_schema` de `Query` a `False`:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## Recapitulación

Puedes declarar validaciones y metadatos adicionales para tus parámetros.

Validaciones genéricas y metadatos:

* `alias`
* `title`
* `description`
* `deprecated`

Validaciones específicas para strings:

* `min_length`
* `max_length`
* `pattern`

En estos ejemplos viste cómo declarar validaciones para valores de tipo `str`.

Mira los siguientes capítulos para aprender cómo declarar validaciones para otros tipos, como números.
