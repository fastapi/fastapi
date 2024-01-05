# Introducción a los Tipos de Python

Python tiene soporte para <abbr title="en español, anotaciones de tipo.">"type hints"</abbr> opcionales (también se conocido como "type annotations").

Estos **type hints** o anotaciones son una sintáxis especial que permite declarar el <abbr title="por ejemplo: str, int, float, bool">tipo</abbr> de una variable.

Usando las declaraciones de tipos para tus variables, los editores y herramientas pueden proveerte un soporte mejor.

Este es solo un **tutorial corto** sobre los Python type hints. Solo cubre lo mínimo necesario para usarlos con **FastAPI**... que actualmente es muy poco.

Todo **FastAPI** está basado en estos type hints, lo que le da muchas ventajas y beneficios.

Pero, así nunca uses **FastAPI** te beneficiarás de aprender un poco sobre los type hints.

!!! note "Nota"
    Si eres un experto en Python y ya lo sabes todo sobre los type hints, salta al siguiente capítulo.

## Motivación

Comencemos con un ejemplo simple:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

Llamar este programa nos muestra el siguiente <abbr title="en español: salida">output</abbr>:

```
John Doe
```

La función hace lo siguiente:

* Toma un `first_name` y un `last_name`.
* Convierte la primera letra de cada uno en una letra mayúscula con `title()`.
* Las <abbr title="las junta como si fuesen una. Con el contenido de una después de la otra. En inlgés: concatenate.">concatena</abbr> con un espacio en la mitad.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Edítalo

Es un programa muy simple.

Ahora, imagina que lo estás escribiendo desde ceros.

En algún punto habrías comenzado con la definición de la función, tenías los parámetros listos...

Pero, luego tienes que llamar "ese método que convierte la primera letra en una mayúscula".

Cómo era `upper`? O era `uppercase`? `first_uppercase`? `capitalize`?

Luego lo intentas con el viejo amigo de los programadores, el autocompletado del editor.

Escribes el primer parámetro de la función `first_name`, luego un punto (`.`) y luego presionas `Ctrl+Space` para iniciar el autocompletado.

Tristemente, no obtienes nada útil:

<img src="https://fastapi.tiangolo.com/img/python-types/image01.png">

### Añade tipos

Vamos a modificar una única línea de la versión previa.

Vamos a cambiar exactamente este fragmento, los parámetros de la función, de:

```Python
    first_name, last_name
```

a:

```Python
    first_name: str, last_name: str
```

Eso es todo.

Esos son los "type hints":

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

No es lo mismo a declarar valores por defecto, como sería con:

```Python
    first_name="john", last_name="doe"
```

Es algo diferente.

Estamos usando los dos puntos (`:`), no un símbolo de igual (`=`).

Añadir los type hints normalmente no cambia lo que sucedería si ellos no estuviesen presentes.

Pero ahora imagina que nuevamente estás creando la función, pero con los type hints.

En el mismo punto intentas iniciar el autocompletado con `Ctrl+Space` y ves:

<img src="https://fastapi.tiangolo.com/img/python-types/image02.png">

Con esto puedes moverte hacia abajo viendo las opciones hasta que encuentras una que te suene:

<img src="https://fastapi.tiangolo.com/img/python-types/image03.png">

## Más motivación

Mira esta función que ya tiene type hints:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Como el editor conoce el tipo de las variables no solo obtienes autocompletado, si no que también obtienes chequeo de errores:

<img src="https://fastapi.tiangolo.com/img/python-types/image04.png">

Ahora que sabes que tienes que arreglarlo convierte `age` a un string con `str(age)`:

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Declarando tipos

Acabas de ver el lugar principal para declarar los type hints. Como parámetros de las funciones.

Este es también el lugar principal en que los usarías con  **FastAPI**.

### Tipos simples

Puedes declarar todos los tipos estándar de Python, no solamente  `str`.

Por ejemplo, puedes usar:

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Tipos genéricos con argumentos de tipo

Existen algunas estructuras de datos que pueden contener otros valores, como `dict`, `list`, `set` y `tuple`. Los valores internos pueden tener su propio tipo también.

Estos tipos que tienen tipos internos se denominan tipos "**genéricos**". Es posible declararlos, incluso con sus tipos internos.

Para declarar esos tipos y sub-tipos puedes usar el módulo estándar de Python `typing`.Él existe específicamente para dar soporte a este tipo de type hints.

#### Nuevas versiones de Python

La sintaxis que usa `typing` es **compatible** con todas las versiones, desde Python 3.6 hasta las más recientes, incluidas Python 3.9, Python 3.10, etc.

A medida que avanza Python, las **versiones más nuevas** vienen con soporte mejorado para estas anotaciones de tipo y en muchos casos ni siquiera necesitarás importar y usar el módulo `typing` para declarar las anotaciones de tipo.

Si puedes elegir una versión más reciente de Python para tu proyecto, podrás aprovechar esa simplicidad adicional.

En toda la documentación hay ejemplos compatibles con cada versión de Python (cuando existan diferencias).

Por ejemplo, "**Python 3.6+**" significa que es compatible con Python 3.6 o superior (incluidos 3.7, 3.8, 3.9, 3.10, etc.). Y "**Python 3.9+**" significa que es compatible con Python 3.9 o superior (incluido 3.10, etc.).

Si puede utilizar las **últimas versiones de Python**, utilice los ejemplos de la última versión, que tendrán la **mejor y más simple sintaxis**, por ejemplo, "**Python 3.10+**".

#### Listas

Por ejemplo, vamos a definir una variable para que sea una `list` compuesta de `str`.

=== "Python 3.9+"

    Declara la variable con la misma sintáxis de los dos puntos (`:`).

    Como tipo, pon `list`.

    Como la lista es un tipo que contiene algunos tipos internos, colócalos entre corchetes `[]`:

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial006_py39.py!}
    ```

=== "Python 3.8+"

    De `typing`, importa `List` (con una `L` mayúscula):

    ``` Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial006.py!}
    ```

    Declara la variable con la misma sintáxis de los dos puntos (`:`).

    Como tipo, pon la `List` importada desde typing`.

    Como la lista es un tipo que contiene algunos tipos internos, colócalos entre corchetes `[]`:

    ```Python hl_lines="4"
    {!> ../../../docs_src/python_types/tutorial006.py!}
    ```

!!! info "Información"
    Estos tipos internos entre corchetes se denominan "argumentos de tipo".

    En este caso `str` es un argumentos de tipo pasado a la `List` (or `list` in Python 3.9 and above).

Esto significa: "la variable `items` es una `list`, y cada uno de los ítems en esa lista es un `str`".

!!! tip "Consejo"
    Si estas utilizando 3.9 o superior, no tienes que importar `List` desde `typing`, puedes utilizar `list` en su defecto.

Con esta declaración tu editor puede proveerte soporte inclusive mientras está procesando ítems de la lista.

<img src="https://fastapi.tiangolo.com/img/python-types/image05.png">

Sin tipos el autocompletado en este tipo de estructura es casi imposible de lograr:

Observa que la variable `item` es unos de los elementos en la lista `items`.

El editor aún sabe que es un `str` y provee soporte para ello.

#### Tuplas y Sets

Harías lo mismo para declarar `tuple`s y `set`s:

=== "Python 3.9+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial007_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial007.py!}
    ```

Esto significa:

* La variable `items_t` es una `tuple` con 3 ítems, un `int`, otro `int`, y un `str`.
* La variable `items_s` es un `set` y cada uno de sus ítems es de tipo `bytes`.

#### Diccionarios (Dicts)

Para definir un `dict` le pasas 2 sub-tipos separados por comas.

El primer sub-tipo es para los keys del `dict`.

El segundo sub-tipo es para los valores del `dict`:

=== "Python 3.9+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial008_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial008.py!}
    ```

Esto significa:

* La variable `prices` es un `dict`:
    * Los keys de este `dict` son de tipo `str` (digamos que son el nombre de cada ítem).
    * Los valores de este `dict` son de tipo `float` (digamos que son el precio de cada ítem).

#### Union

Puedes declarar que una variable puede ser cualquiera de **varios tipos**, por ejemplo, una `int` o una `str`.

En Python 3.6 y superiores (incluido Python 3.10) puede usar el tipo `Union` de `typing` y poner entre corchetes los tipos posibles a aceptar.

En Python 3.10 también hay una **nueva sintaxis** donde puedes poner los tipos posibles separados por una <abbr title='también llamada "bitwise u operador de bit", pero ese significado no es relevante aquí'>barra vertical (`|` )</abbr>.

=== "Python 3.10+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial008b_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial008b.py!}
    ```

En ambos casos, esto significa que `item` podría ser un `int` o un `str`.

#### Posibilidad `None`

Puedes declarar que un valor podría tener un tipo, como `str`, pero que también podría ser `None`.

En Python 3.6 y superior (incluido Python 3.10), puede declararlo importando y usando `Optional` desde el módulo "escribir".

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

Usar `Optional[str]` en lugar de solo `str` permitirá que el editor te ayude a detectar errores en los que podrías asumir que un valor es siempre una `str`, cuando en realidad también podría ser `None`.

`Optional[Something]` es en realidad un atajo para `Union[Something, None]`, son equivalentes.

Esto también significa que en Python 3.10, puedes usar `Something | None`:

=== "Python 3.10+"

    ```Python hl_lines="1"
    {!> ../../../docs_src/python_types/tutorial009_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial009.py!}
    ```

=== "Python 3.8+ alternative"

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial009b.py!}
    ```

#### Usar `Union` o `Optional`

Si está utilizando una versión de Python inferior a 3.10, aquí tiene un consejo desde mi punto de vista muy **subjetivo**:

* 🚨 Evite el uso de `Optional[SomeType]`
* En su lugar ✨ **use `Union[SomeType, None]`** ✨.

Ambos son equivalentes y en el fondo son iguales, pero recomendaría `Union` en lugar de `Optional` porque la palabra "**optional**" parecería implicar que el valor es opcional, y en realidad significa "puede ser `None`”, incluso si no es opcional y sigue siendo obligatorio.

Creo que "Union[SomeType, None]" es más explícito sobre lo que significa.

Se trata sólo de las palabras y los nombres. Pero esas palabras pueden afectar la forma en que usted y sus compañeros de equipo piensan sobre el código.

Como ejemplo, tomemos esta función:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009c.py!}
```

El parámetro `nombre` se define como `Optional[str]`, pero **no es opcional**, no se puede llamar a la función sin el parámetro:

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

El parámetro `name` es **aún requerido** (no *opcional*) porque no tiene un valor predeterminado. Aún así, `name` acepta `None` como valor:

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

La buena noticia es que una vez que estés en Python 3.10 no tendrás que preocuparte por eso, ya que podrás simplemente usar `|` para definir uniones de tipos:

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009c_py310.py!}
```

Y entonces no tendrá que preocuparse por nombres como `Optional` y `Union`. 😎

#### Tipos Genéricos

Estos tipos que toman parámetros de tipo entre corchetes se denominan **Tipos genéricos** o **Genéricos**, por ejemplo:

=== "Python 3.10+"

    Puede utilizar los mismos tipos integrados que los genéricos (con corchetes y tipos dentro):

    * `list`
    * `tuple`
    * `set`
    * `dict`

    Y lo mismo que con Python 3.8, desde el módulo `typing`:

    * `Union`
    * `Optional` (lo mismo que con Python 3.8)
    * ...y otros.

    En Python 3.10, como alternativa al uso de los genéricos `Union` y `Optional`, puedes usar la <abbr title='también llamada "bitwise u operador de bit", pero ese significado no es relevante aquí'>barra vertical (`| `)</abbr> para declarar uniones de tipos, eso es mucho mejor y más simple.

=== "Python 3.9+"

    Puede utilizar los mismos tipos integrados que los genéricos (con corchetes y tipos dentro):

    * `list`
    * `tuple`
    * `set`
    * `dict`

    Y lo mismo que con Python 3.8, desde el módulo `typing`:

    * `Union`
    * `Optional`
    * ...y otros.

=== "Python 3.8+"

    * `List`
    * `Tuple`
    * `Set`
    * `Dict`
    * `Union`
    * `Optional`
    * ...y otros.

### Clases como tipos

También puedes declarar una clase como el tipo de una variable.

Digamos que tienes una clase `Person`con un nombre:

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Entonces puedes declarar una variable que sea de tipo `Person`:

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

Una vez más tendrás todo el soporte del editor:

<img src="https://fastapi.tiangolo.com/img/python-types/image06.png">

Observe que esto significa que "`one_person` es una <abbr title='instancia'>**instance**</abbr> de la clase `Person`".

No significa que "`one_person` sea la **clase** llamada `Person`".

## Modelos de Pydantic

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> es una library de Python para llevar a cabo validación de datos.

Tú declaras la "forma" de los datos mediante clases con atributos.

Cada atributo tiene un tipo.

Luego creas una <abbr title='instancia'>instance</abbr> de esa clase con algunos valores y Pydantic validará los valores, los convertirá al tipo apropiado (si ese es el caso) y te dará un objeto con todos los datos.

Y obtienes todo el soporte del editor con el objeto resultante.

Un ejemplo de la documentación oficial de Pydantic:

=== "Python 3.10+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011_py310.py!}
    ```

=== "Python 3.9+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011_py39.py!}
    ```

=== "Python 3.8+"

    ```Python
    {!> ../../../docs_src/python_types/tutorial011.py!}
    ```

!!! info "Información"
    Para aprender más sobre <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic mira su documentación</a>.

**FastAPI** está todo basado en Pydantic.

Vas a ver mucho más de esto en práctica en el [Tutorial - Guía de Usuario](tutorial/index.md){.internal-link target=_blank}.

!!! tip "Consejo"
    Pydantic tiene un comportamiento especial cuando usas `Optional` o `Union[Something, None]` sin un valor predeterminado, puedes leer más sobre esto en la documentación de Pydantic acerca de <a href="https://pydantic-docs.helpmanual .io/usage/models/#required-optional-fields" class="external-link" target="_blank">Campos opcionales obligatorios</a>.

## <abbr title="en español, anotaciones de tipo.">"Type Hints"</abbr> con Anotaciones de Metadatos

Python también tiene una característica que permite poner **metadatos adicionales** en estas sugerencias de tipo usando "Annotated".

=== "Python 3.9+"

    En Python 3.9, `Annotated` es parte de la biblioteca estándar, por lo que puedes importarlo desde `typing`.

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial013_py39.py!}
    ```

=== "Python 3.8+"

    En versiones anteriores a Python 3.9, importa  `Annotated` desde `typing_extensions`.

    Ya estará instalado con **FastAPI**.

    ```Python hl_lines="1  4"
    {!> ../../../docs_src/python_types/tutorial013.py!}
    ```

Python en sí no hace nada con este `Annotated`. Y para editores y otras herramientas, el tipo sigue siendo "str".

Pero puedes usar este espacio en `Annotated` para proporcionar a **FastAPI** metadatos adicionales sobre cómo quieres que se comporte tu aplicación.

Lo importante que debe recordar es que **el primer *argumento de tipo*** que pasa a `Annotated` es el **tipo real**. El resto son solo metadatos para otras herramientas.

Por ahora, sólo necesitas saber que `Annotated` existe y que es tandard Python. 😎

Más adelante verás lo **poderoso** que puede ser.

!!! tip "Consejo"
    El hecho de que sea **standard Python** significa que seguirás obteniendo la **mejor experiencia de desarrollador posible** en tu editor, con las herramientas que utilizas para analizar y refactorizar tu código, etc. ✨

     Y también que su código será muy compatible con muchas otras herramientas y bibliotecas de Python. 🚀

## <abbr title="en español, anotaciones de tipo.">"Type Hints"</abbr>  en **FastAPI**

**FastAPI** aprovecha estos <abbr title="en español, anotaciones de tipo.">"type hints"</abbr>  para hacer varias cosas.

Con **FastAPI** declaras los parámetros con <abbr title="en español, anotaciones de tipo.">"type hints"</abbr> y obtienes:

* **Soporte en el editor**.
* **Chequeos de tipo**.

...y **FastAPI** usa las mismas declaraciones para:

* **Definir requerimientos**: desde `request path parameters`, `query parameters`, `headers`, `bodies`, `dependencies`, etc.
* **Convertir datos**: desde el `request` al tipo requerido.
* **Validar datos**: viniendo de cada `request`:
    * Generando **errores automáticos** devueltos al cliente cuando los datos son inválidos.
* **Documentar** la API usando OpenAPI:
    * que en su caso es usada por las interfaces de usuario de la documentación automática e interactiva.

Puede que todo esto suene abstracto. Pero no te preocupes que todo lo verás en acción en el [Tutorial - Guía de Usuario](tutorial/index.md){.internal-link target=_blank}.

Lo importante es que usando los tipos estándar de Python en un único lugar (en vez de añadir más clases, decorators, etc.) **FastAPI** hará mucho del trabajo por ti.

!!! info "Información"
    Si ya pasaste por todo el tutorial y volviste a la sección de los tipos, una buena referencia es <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">la "cheat sheet" de `mypy`</a>.
