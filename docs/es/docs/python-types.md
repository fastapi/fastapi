# Introducción a Tipos en Python

Python tiene soporte para "anotaciones de tipos" opcionales (también llamadas "type hints").

Estas **"anotaciones de tipos"** o type hints son una sintaxis especial que permite declarar el <abbr title="por ejemplo: str, int, float, bool">tipo</abbr> de una variable.

Al declarar tipos para tus variables, los editores y herramientas te pueden proporcionar un mejor soporte.

Este es solo un **tutorial rápido / recordatorio** sobre las anotaciones de tipos en Python. Cubre solo lo mínimo necesario para usarlas con **FastAPI**... que en realidad es muy poco.

**FastAPI** se basa completamente en estas anotaciones de tipos, dándole muchas ventajas y beneficios.

Pero incluso si nunca usas **FastAPI**, te beneficiaría aprender un poco sobre ellas.

/// note | Nota

Si eres un experto en Python, y ya sabes todo sobre las anotaciones de tipos, salta al siguiente capítulo.

///

## Motivación

Comencemos con un ejemplo simple:

{* ../../docs_src/python_types/tutorial001.py *}

Llamar a este programa genera:

```
John Doe
```

La función hace lo siguiente:

* Toma un `first_name` y `last_name`.
* Convierte la primera letra de cada uno a mayúsculas con `title()`.
* <abbr title="Los une, como uno. Con el contenido de uno después del otro.">Concatena</abbr> ambos con un espacio en el medio.

{* ../../docs_src/python_types/tutorial001.py hl[2] *}

### Edítalo

Es un programa muy simple.

Pero ahora imagina que lo escribieras desde cero.

En algún momento habrías empezado la definición de la función, tenías los parámetros listos...

Pero luego tienes que llamar "ese método que convierte la primera letra a mayúscula".

¿Era `upper`? ¿Era `uppercase`? `first_uppercase`? `capitalize`?

Entonces, pruebas con el amigo del viejo programador, el autocompletado del editor.

Escribes el primer parámetro de la función, `first_name`, luego un punto (`.`) y luego presionas `Ctrl+Espacio` para activar el autocompletado.

Pero, tristemente, no obtienes nada útil:

<img src="/img/python-types/image01.png">

### Añadir tipos

Modifiquemos una sola línea de la versión anterior.

Cambiaremos exactamente este fragmento, los parámetros de la función, de:

```Python
    first_name, last_name
```

a:

```Python
    first_name: str, last_name: str
```

Eso es todo.

Esas son las "anotaciones de tipos":

{* ../../docs_src/python_types/tutorial002.py hl[1] *}

Eso no es lo mismo que declarar valores predeterminados como sería con:

```Python
    first_name="john", last_name="doe"
```

Es una cosa diferente.

Estamos usando dos puntos (`:`), no igualdades (`=`).

Y agregar anotaciones de tipos normalmente no cambia lo que sucede de lo que ocurriría sin ellas.

Pero ahora, imagina que nuevamente estás en medio de la creación de esa función, pero con anotaciones de tipos.

En el mismo punto, intentas activar el autocompletado con `Ctrl+Espacio` y ves:

<img src="/img/python-types/image02.png">

Con eso, puedes desplazarte, viendo las opciones, hasta que encuentres la que "te suene":

<img src="/img/python-types/image03.png">

## Más motivación

Revisa esta función, ya tiene anotaciones de tipos:

{* ../../docs_src/python_types/tutorial003.py hl[1] *}

Porque el editor conoce los tipos de las variables, no solo obtienes autocompletado, también obtienes chequeo de errores:

<img src="/img/python-types/image04.png">

Ahora sabes que debes corregirlo, convertir `age` a un string con `str(age)`:

{* ../../docs_src/python_types/tutorial004.py hl[2] *}

## Declaración de tipos

Acabas de ver el lugar principal para declarar anotaciones de tipos. Como parámetros de función.

Este también es el lugar principal donde los utilizarías con **FastAPI**.

### Tipos simples

Puedes declarar todos los tipos estándar de Python, no solo `str`.

Puedes usar, por ejemplo:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005.py hl[1] *}

### Tipos genéricos con parámetros de tipo

Hay algunas estructuras de datos que pueden contener otros valores, como `dict`, `list`, `set` y `tuple`. Y los valores internos también pueden tener su propio tipo.

Estos tipos que tienen tipos internos se denominan tipos "**genéricos**". Y es posible declararlos, incluso con sus tipos internos.

Para declarar esos tipos y los tipos internos, puedes usar el módulo estándar de Python `typing`. Existe específicamente para soportar estas anotaciones de tipos.

#### Versiones más recientes de Python

La sintaxis que utiliza `typing` es **compatible** con todas las versiones, desde Python 3.6 hasta las versiones más recientes, incluyendo Python 3.9, Python 3.10, etc.

A medida que avanza Python, las **versiones más recientes** vienen con soporte mejorado para estas anotaciones de tipos y en muchos casos ni siquiera necesitarás importar y usar el módulo `typing` para declarar las anotaciones de tipos.

Si puedes elegir una versión más reciente de Python para tu proyecto, podrás aprovechar esa simplicidad adicional.

En toda la documentación hay ejemplos compatibles con cada versión de Python (cuando hay una diferencia).

Por ejemplo, "**Python 3.6+**" significa que es compatible con Python 3.6 o superior (incluyendo 3.7, 3.8, 3.9, 3.10, etc). Y "**Python 3.9+**" significa que es compatible con Python 3.9 o superior (incluyendo 3.10, etc).

Si puedes usar las **últimas versiones de Python**, utiliza los ejemplos para la última versión, esos tendrán la **mejor y más simple sintaxis**, por ejemplo, "**Python 3.10+**".

#### Lista

Por ejemplo, vamos a definir una variable para ser una `list` de `str`.

//// tab | Python 3.9+

Declara la variable, con la misma sintaxis de dos puntos (`:`).

Como tipo, pon `list`.

Como la lista es un tipo que contiene algunos tipos internos, los pones entre corchetes:

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006_py39.py!}
```

////

//// tab | Python 3.8+

De `typing`, importa `List` (con una `L` mayúscula):

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006.py!}
```

Declara la variable, con la misma sintaxis de dos puntos (`:`).

Como tipo, pon el `List` que importaste de `typing`.

Como la lista es un tipo que contiene algunos tipos internos, los pones entre corchetes:

```Python hl_lines="4"
{!> ../../docs_src/python_types/tutorial006.py!}
```

////

/// info | Información

Esos tipos internos en los corchetes se denominan "parámetros de tipo".

En este caso, `str` es el parámetro de tipo pasado a `List` (o `list` en Python 3.9 y superior).

///

Eso significa: "la variable `items` es una `list`, y cada uno de los ítems en esta lista es un `str`".

/// tip | Consejo

Si usas Python 3.9 o superior, no tienes que importar `List` de `typing`, puedes usar el mismo tipo `list` regular en su lugar.

///

Al hacer eso, tu editor puede proporcionar soporte incluso mientras procesa elementos de la lista:

<img src="/img/python-types/image05.png">

Sin tipos, eso es casi imposible de lograr.

Nota que la variable `item` es uno de los elementos en la lista `items`.

Y aún así, el editor sabe que es un `str` y proporciona soporte para eso.

#### Tuple y Set

Harías lo mismo para declarar `tuple`s y `set`s:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial007_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial007.py!}
```

////

Esto significa:

* La variable `items_t` es un `tuple` con 3 ítems, un `int`, otro `int`, y un `str`.
* La variable `items_s` es un `set`, y cada uno de sus ítems es del tipo `bytes`.

#### Dict

Para definir un `dict`, pasas 2 parámetros de tipo, separados por comas.

El primer parámetro de tipo es para las claves del `dict`.

El segundo parámetro de tipo es para los valores del `dict`:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008.py!}
```

////

Esto significa:

* La variable `prices` es un `dict`:
    * Las claves de este `dict` son del tipo `str` (digamos, el nombre de cada ítem).
    * Los valores de este `dict` son del tipo `float` (digamos, el precio de cada ítem).

#### Union

Puedes declarar que una variable puede ser cualquier de **varios tipos**, por ejemplo, un `int` o un `str`.

En Python 3.6 y posterior (incluyendo Python 3.10) puedes usar el tipo `Union` de `typing` y poner dentro de los corchetes los posibles tipos a aceptar.

En Python 3.10 también hay una **nueva sintaxis** donde puedes poner los posibles tipos separados por una <abbr title='también llamado "operador OR a nivel de bits", pero ese significado no es relevante aquí'>barra vertical (`|`)</abbr>.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b.py!}
```

////

En ambos casos, esto significa que `item` podría ser un `int` o un `str`.

#### Posiblemente `None`

Puedes declarar que un valor podría tener un tipo, como `str`, pero que también podría ser `None`.

En Python 3.6 y posteriores (incluyendo Python 3.10) puedes declararlo importando y usando `Optional` del módulo `typing`.

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009.py!}
```

Usar `Optional[str]` en lugar de solo `str` te permitirá al editor ayudarte a detectar errores donde podrías estar asumiendo que un valor siempre es un `str`, cuando en realidad también podría ser `None`.

`Optional[Something]` es realmente un atajo para `Union[Something, None]`, son equivalentes.

Esto también significa que en Python 3.10, puedes usar `Something | None`:

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009.py!}
```

////

//// tab | Python 3.8+ alternative

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b.py!}
```

////

#### Uso de `Union` u `Optional`

Si estás usando una versión de Python inferior a 3.10, aquí tienes un consejo desde mi punto de vista muy **subjetivo**:

* 🚨 Evita usar `Optional[SomeType]`
* En su lugar ✨ **usa `Union[SomeType, None]`** ✨.

Ambos son equivalentes y debajo son lo mismo, pero recomendaría `Union` en lugar de `Optional` porque la palabra "**opcional**" parecería implicar que el valor es opcional, y en realidad significa "puede ser `None`", incluso si no es opcional y aún es requerido.

Creo que `Union[SomeType, None]` es más explícito sobre lo que significa.

Se trata solo de las palabras y nombres. Pero esas palabras pueden afectar cómo tú y tus compañeros de equipo piensan sobre el código.

Como ejemplo, tomemos esta función:

{* ../../docs_src/python_types/tutorial009c.py hl[1,4] *}

El parámetro `name` está definido como `Optional[str]`, pero **no es opcional**, no puedes llamar a la función sin el parámetro:

```Python
say_hi()  # ¡Oh, no, esto lanza un error! 😱
```

El parámetro `name` sigue siendo **requerido** (no *opcional*) porque no tiene un valor predeterminado. Aún así, `name` acepta `None` como valor:

```Python
say_hi(name=None)  # Esto funciona, None es válido 🎉
```

La buena noticia es que, una vez que estés en Python 3.10, no tendrás que preocuparte por eso, ya que podrás simplemente usar `|` para definir uniones de tipos:

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

Y entonces no tendrás que preocuparte por nombres como `Optional` y `Union`. 😎

#### Tipos genéricos

Estos tipos que toman parámetros de tipo en corchetes se llaman **Tipos Genéricos** o **Genéricos**, por ejemplo:

//// tab | Python 3.10+

Puedes usar los mismos tipos integrados como genéricos (con corchetes y tipos dentro):

* `list`
* `tuple`
* `set`
* `dict`

Y lo mismo que con Python 3.8, desde el módulo `typing`:

* `Union`
* `Optional` (lo mismo que con Python 3.8)
* ...y otros.

En Python 3.10, como alternativa a usar los genéricos `Union` y `Optional`, puedes usar la <abbr title='también llamado "operador OR a nivel de bits", pero ese significado no es relevante aquí'>barra vertical (`|`)</abbr> para declarar uniones de tipos, eso es mucho mejor y más simple.

////

//// tab | Python 3.9+

Puedes usar los mismos tipos integrados como genéricos (con corchetes y tipos dentro):

* `list`
* `tuple`
* `set`
* `dict`

Y lo mismo que con Python 3.8, desde el módulo `typing`:

* `Union`
* `Optional`
* ...y otros.

////

//// tab | Python 3.8+

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Union`
* `Optional`
* ...y otros.

////

### Clases como tipos

También puedes declarar una clase como el tipo de una variable.

Digamos que tienes una clase `Person`, con un nombre:

{* ../../docs_src/python_types/tutorial010.py hl[1:3] *}

Luego puedes declarar una variable para que sea de tipo `Person`:

{* ../../docs_src/python_types/tutorial010.py hl[6] *}

Y luego, nuevamente, obtienes todo el soporte del editor:

<img src="/img/python-types/image06.png">

Nota que esto significa "`one_person` es una **instance** de la clase `Person`".

No significa "`one_person` es la **clase** llamada `Person`".

## Modelos Pydantic

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> es un paquete de Python para realizar la validación de datos.

Declaras la "forma" de los datos como clases con atributos.

Y cada atributo tiene un tipo.

Entonces creas un instance de esa clase con algunos valores y validará los valores, los convertirá al tipo adecuado (si es el caso) y te dará un objeto con todos los datos.

Y obtienes todo el soporte del editor con ese objeto resultante.

Un ejemplo de la documentación oficial de Pydantic:

//// tab | Python 3.10+

```Python
{!> ../../docs_src/python_types/tutorial011_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/python_types/tutorial011_py39.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/python_types/tutorial011.py!}
```

////

/// info | Información

Para saber más sobre <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, revisa su documentación</a>.

///

**FastAPI** está completamente basado en Pydantic.

Verás mucho más de todo esto en práctica en el [Tutorial - Guía del Usuario](tutorial/index.md){.internal-link target=_blank}.

/// tip | Consejo

Pydantic tiene un comportamiento especial cuando utilizas `Optional` o `Union[Something, None]` sin un valor por defecto, puedes leer más sobre ello en la documentación de Pydantic sobre <a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Required Optional fields</a>.

///

## Anotaciones de tipos con metadata

Python también tiene una funcionalidad que permite poner **<abbr title="Datos sobre los datos, en este caso, información sobre el tipo, por ejemplo, una descripción.">metadata</abbr> adicional** en estas anotaciones de tipos usando `Annotated`.

//// tab | Python 3.9+

En Python 3.9, `Annotated` es parte de la librería estándar, así que puedes importarlo desde `typing`.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013_py39.py!}
```

////

//// tab | Python 3.8+

En versiones por debajo de Python 3.9, importas `Annotated` de `typing_extensions`.

Ya estará instalado con **FastAPI**.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013.py!}
```

////

Python en sí no hace nada con este `Annotated`. Y para los editores y otras herramientas, el tipo sigue siendo `str`.

Pero puedes usar este espacio en `Annotated` para proporcionar a **FastAPI** metadata adicional sobre cómo quieres que se comporte tu aplicación.

Lo importante a recordar es que **el primer *parámetro de tipo*** que pasas a `Annotated` es el **tipo real**. El resto es solo metadata para otras herramientas.

Por ahora, solo necesitas saber que `Annotated` existe, y que es Python estándar. 😎

Luego verás lo **poderoso** que puede ser.

/// tip | Consejo

El hecho de que esto sea **Python estándar** significa que seguirás obteniendo la **mejor experiencia de desarrollador posible** en tu editor, con las herramientas que usas para analizar y refactorizar tu código, etc. ✨

Y también que tu código será muy compatible con muchas otras herramientas y paquetes de Python. 🚀

///

## Anotaciones de tipos en **FastAPI**

**FastAPI** aprovecha estas anotaciones de tipos para hacer varias cosas.

Con **FastAPI** declaras parámetros con anotaciones de tipos y obtienes:

* **Soporte del editor**.
* **Chequeo de tipos**.

...y **FastAPI** usa las mismas declaraciones para:

* **Definir requerimientos**: de parámetros de path de la request, parámetros de query, headers, bodies, dependencias, etc.
* **Convertir datos**: de la request al tipo requerido.
* **Validar datos**: provenientes de cada request:
    * Generando **errores automáticos** devueltos al cliente cuando los datos son inválidos.
* **Documentar** la API usando OpenAPI:
    * Que luego es usada por las interfaces de documentación interactiva automática.

Todo esto puede sonar abstracto. No te preocupes. Verás todo esto en acción en el [Tutorial - Guía del Usuario](tutorial/index.md){.internal-link target=_blank}.

Lo importante es que al usar tipos estándar de Python, en un solo lugar (en lugar de agregar más clases, decoradores, etc.), **FastAPI** hará gran parte del trabajo por ti.

/// info | Información

Si ya revisaste todo el tutorial y volviste para ver más sobre tipos, un buen recurso es <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">la "cheat sheet" de `mypy`</a>.

///
