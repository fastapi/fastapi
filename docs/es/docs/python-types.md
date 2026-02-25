# Introducción a Tipos en Python { #python-types-intro }

Python tiene soporte para "anotaciones de tipos" opcionales (también llamadas "type hints").

Estas **"anotaciones de tipos"** o type hints son una sintaxis especial que permite declarar el <dfn title="por ejemplo: str, int, float, bool">tipo</dfn> de una variable.

Al declarar tipos para tus variables, los editores y herramientas te pueden proporcionar un mejor soporte.

Este es solo un **tutorial rápido / recordatorio** sobre las anotaciones de tipos en Python. Cubre solo lo mínimo necesario para usarlas con **FastAPI**... que en realidad es muy poco.

**FastAPI** se basa completamente en estas anotaciones de tipos, dándole muchas ventajas y beneficios.

Pero incluso si nunca usas **FastAPI**, te beneficiaría aprender un poco sobre ellas.

/// note | Nota

Si eres un experto en Python, y ya sabes todo sobre las anotaciones de tipos, salta al siguiente capítulo.

///

## Motivación { #motivation }

Comencemos con un ejemplo simple:

{* ../../docs_src/python_types/tutorial001_py310.py *}

Llamar a este programa genera:

```
John Doe
```

La función hace lo siguiente:

* Toma un `first_name` y `last_name`.
* Convierte la primera letra de cada uno a mayúsculas con `title()`.
* <dfn title="Los une, como uno. Con el contenido de uno después del otro.">Concatena</dfn> ambos con un espacio en el medio.

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### Edítalo { #edit-it }

Es un programa muy simple.

Pero ahora imagina que lo escribieras desde cero.

En algún momento habrías empezado la definición de la función, tenías los parámetros listos...

Pero luego tienes que llamar "ese método que convierte la primera letra a mayúscula".

¿Era `upper`? ¿Era `uppercase`? `first_uppercase`? `capitalize`?

Entonces, pruebas con el amigo del viejo programador, el autocompletado del editor.

Escribes el primer parámetro de la función, `first_name`, luego un punto (`.`) y luego presionas `Ctrl+Espacio` para activar el autocompletado.

Pero, tristemente, no obtienes nada útil:

<img src="/img/python-types/image01.png">

### Añadir tipos { #add-types }

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

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

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

## Más motivación { #more-motivation }

Revisa esta función, ya tiene anotaciones de tipos:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

Porque el editor conoce los tipos de las variables, no solo obtienes autocompletado, también obtienes chequeo de errores:

<img src="/img/python-types/image04.png">

Ahora sabes que debes corregirlo, convertir `age` a un string con `str(age)`:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Declaración de tipos { #declaring-types }

Acabas de ver el lugar principal para declarar anotaciones de tipos. Como parámetros de función.

Este también es el lugar principal donde los utilizarías con **FastAPI**.

### Tipos simples { #simple-types }

Puedes declarar todos los tipos estándar de Python, no solo `str`.

Puedes usar, por ejemplo:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### Módulo `typing` { #typing-module }

Para algunos casos adicionales, podrías necesitar importar algunas cosas del módulo `typing` de la standard library, por ejemplo cuando quieres declarar que algo tiene "cualquier tipo", puedes usar `Any` de `typing`:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Tipos genéricos { #generic-types }

Algunos tipos pueden tomar "parámetros de tipo" entre corchetes, para definir sus tipos internos, por ejemplo una "lista de strings" se declararía `list[str]`.

Estos tipos que pueden tomar parámetros de tipo se llaman **Tipos Genéricos** o **Genéricos**.

Puedes usar los mismos tipos integrados como genéricos (con corchetes y tipos dentro):

* `list`
* `tuple`
* `set`
* `dict`

#### Lista { #list }

Por ejemplo, vamos a definir una variable para ser una `list` de `str`.

Declara la variable, con la misma sintaxis de dos puntos (`:`).

Como tipo, pon `list`.

Como la lista es un tipo que contiene algunos tipos internos, los pones entre corchetes:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// info | Información

Esos tipos internos en los corchetes se denominan "parámetros de tipo".

En este caso, `str` es el parámetro de tipo pasado a `list`.

///

Eso significa: "la variable `items` es una `list`, y cada uno de los ítems en esta lista es un `str`".

Al hacer eso, tu editor puede proporcionar soporte incluso mientras procesa elementos de la lista:

<img src="/img/python-types/image05.png">

Sin tipos, eso es casi imposible de lograr.

Nota que la variable `item` es uno de los elementos en la lista `items`.

Y aún así, el editor sabe que es un `str` y proporciona soporte para eso.

#### Tuple y Set { #tuple-and-set }

Harías lo mismo para declarar `tuple`s y `set`s:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

Esto significa:

* La variable `items_t` es un `tuple` con 3 ítems, un `int`, otro `int`, y un `str`.
* La variable `items_s` es un `set`, y cada uno de sus ítems es del tipo `bytes`.

#### Dict { #dict }

Para definir un `dict`, pasas 2 parámetros de tipo, separados por comas.

El primer parámetro de tipo es para las claves del `dict`.

El segundo parámetro de tipo es para los valores del `dict`:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

Esto significa:

* La variable `prices` es un `dict`:
    * Las claves de este `dict` son del tipo `str` (digamos, el nombre de cada ítem).
    * Los valores de este `dict` son del tipo `float` (digamos, el precio de cada ítem).

#### Union { #union }

Puedes declarar que una variable puede ser cualquiera de **varios tipos**, por ejemplo, un `int` o un `str`.

Para definirlo usas la <dfn title='también llamado "operador OR a nivel de bits", pero ese significado no es relevante aquí'>barra vertical (`|`)</dfn> para separar ambos tipos.

Esto se llama una "unión", porque la variable puede ser cualquiera en la unión de esos dos conjuntos de tipos.

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

Esto significa que `item` podría ser un `int` o un `str`.

#### Posiblemente `None` { #possibly-none }

Puedes declarar que un valor podría tener un tipo, como `str`, pero que también podría ser `None`.

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

Usar `str | None` en lugar de solo `str` te permitirá al editor ayudarte a detectar errores donde podrías estar asumiendo que un valor siempre es un `str`, cuando en realidad también podría ser `None`.

### Clases como tipos { #classes-as-types }

También puedes declarar una clase como el tipo de una variable.

Digamos que tienes una clase `Person`, con un nombre:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

Luego puedes declarar una variable para que sea de tipo `Person`:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

Y luego, nuevamente, obtienes todo el soporte del editor:

<img src="/img/python-types/image06.png">

Nota que esto significa "`one_person` es una **instance** de la clase `Person`".

No significa "`one_person` es la **clase** llamada `Person`".

## Modelos Pydantic { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> es un paquete de Python para realizar la validación de datos.

Declaras la "forma" de los datos como clases con atributos.

Y cada atributo tiene un tipo.

Entonces creas un instance de esa clase con algunos valores y validará los valores, los convertirá al tipo adecuado (si es el caso) y te dará un objeto con todos los datos.

Y obtienes todo el soporte del editor con ese objeto resultante.

Un ejemplo de la documentación oficial de Pydantic:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | Información

Para saber más sobre <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, revisa su documentación</a>.

///

**FastAPI** está completamente basado en Pydantic.

Verás mucho más de todo esto en práctica en el [Tutorial - Guía del Usuario](tutorial/index.md){.internal-link target=_blank}.

## Anotaciones de tipos con metadata { #type-hints-with-metadata-annotations }

Python también tiene una funcionalidad que permite poner **<dfn title="Datos sobre los datos, en este caso, información sobre el tipo, por ejemplo, una descripción.">metadata</dfn> adicional** en estas anotaciones de tipos usando `Annotated`.

Puedes importar `Annotated` desde `typing`.

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python en sí no hace nada con este `Annotated`. Y para los editores y otras herramientas, el tipo sigue siendo `str`.

Pero puedes usar este espacio en `Annotated` para proporcionar a **FastAPI** metadata adicional sobre cómo quieres que se comporte tu aplicación.

Lo importante a recordar es que **el primer *parámetro de tipo*** que pasas a `Annotated` es el **tipo real**. El resto es solo metadata para otras herramientas.

Por ahora, solo necesitas saber que `Annotated` existe, y que es Python estándar. 😎

Luego verás lo **poderoso** que puede ser.

/// tip | Consejo

El hecho de que esto sea **Python estándar** significa que seguirás obteniendo la **mejor experiencia de desarrollador posible** en tu editor, con las herramientas que usas para analizar y refactorizar tu código, etc. ✨

Y también que tu código será muy compatible con muchas otras herramientas y paquetes de Python. 🚀

///

## Anotaciones de tipos en **FastAPI** { #type-hints-in-fastapi }

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
