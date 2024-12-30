# Clases como dependencias

Antes de profundizar en el sistema de **Inyección de Dependencias**, vamos a mejorar el ejemplo anterior.

## Un `dict` del ejemplo anterior

En el ejemplo anterior, estábamos devolviendo un `dict` de nuestra dependencia ("dependable"):

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

Pero luego obtenemos un `dict` en el parámetro `commons` de la *path operation function*.

Y sabemos que los editores no pueden proporcionar mucho soporte (como autocompletado) para `dict`s, porque no pueden conocer sus claves y tipos de valor.

Podemos hacerlo mejor...

## Qué hace a una dependencia

Hasta ahora has visto dependencias declaradas como funciones.

Pero esa no es la única forma de declarar dependencias (aunque probablemente sea la más común).

El factor clave es que una dependencia debe ser un "callable".

Un "**callable**" en Python es cualquier cosa que Python pueda "llamar" como una función.

Entonces, si tienes un objeto `something` (que podría _no_ ser una función) y puedes "llamarlo" (ejecutarlo) como:

```Python
something()
```

o

```Python
something(some_argument, some_keyword_argument="foo")
```

entonces es un "callable".

## Clases como dependencias

Puedes notar que para crear una instance de una clase en Python, utilizas esa misma sintaxis.

Por ejemplo:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

En este caso, `fluffy` es una instance de la clase `Cat`.

Y para crear `fluffy`, estás "llamando" a `Cat`.

Entonces, una clase en Python también es un **callable**.

Entonces, en **FastAPI**, podrías usar una clase de Python como una dependencia.

Lo que **FastAPI** realmente comprueba es que sea un "callable" (función, clase o cualquier otra cosa) y los parámetros definidos.

Si pasas un "callable" como dependencia en **FastAPI**, analizará los parámetros de ese "callable", y los procesará de la misma manera que los parámetros de una *path operation function*. Incluyendo sub-dependencias.

Eso también se aplica a los callables sin parámetros. Igual que sería para *path operation functions* sin parámetros.

Entonces, podemos cambiar la dependencia "dependable" `common_parameters` de arriba a la clase `CommonQueryParams`:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

Presta atención al método `__init__` usado para crear la instance de la clase:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...tiene los mismos parámetros que nuestros `common_parameters` anteriores:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

Esos parámetros son los que **FastAPI** usará para "resolver" la dependencia.

En ambos casos, tendrá:

* Un parámetro de query `q` opcional que es un `str`.
* Un parámetro de query `skip` que es un `int`, con un valor por defecto de `0`.
* Un parámetro de query `limit` que es un `int`, con un valor por defecto de `100`.

En ambos casos, los datos serán convertidos, validados, documentados en el esquema de OpenAPI, etc.

## Úsalo

Ahora puedes declarar tu dependencia usando esta clase.

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** llama a la clase `CommonQueryParams`. Esto crea una "instance" de esa clase y la instance será pasada como el parámetro `commons` a tu función.

## Anotación de tipos vs `Depends`

Nota cómo escribimos `CommonQueryParams` dos veces en el código anterior:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ sin `Annotated`

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

El último `CommonQueryParams`, en:

```Python
... Depends(CommonQueryParams)
```

...es lo que **FastAPI** utilizará realmente para saber cuál es la dependencia.

Es a partir de este que **FastAPI** extraerá los parámetros declarados y es lo que **FastAPI** realmente llamará.

---

En este caso, el primer `CommonQueryParams`, en:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.8+ sin `Annotated`

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
commons: CommonQueryParams ...
```

////

...no tiene ningún significado especial para **FastAPI**. **FastAPI** no lo usará para la conversión de datos, validación, etc. (ya que está usando `Depends(CommonQueryParams)` para eso).

De hecho, podrías escribir simplemente:

//// tab | Python 3.8+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ sin `Annotated`

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
commons = Depends(CommonQueryParams)
```

////

...como en:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

Pero declarar el tipo es recomendable, ya que de esa manera tu editor sabrá lo que se pasará como el parámetro `commons`, y entonces podrá ayudarte con el autocompletado, chequeo de tipos, etc:

<img src="/img/tutorial/dependencies/image02.png">

## Atajo

Pero ves que estamos teniendo algo de repetición de código aquí, escribiendo `CommonQueryParams` dos veces:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ sin `Annotated`

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** proporciona un atajo para estos casos, en donde la dependencia es *específicamente* una clase que **FastAPI** "llamará" para crear una instance de la clase misma.

Para esos casos específicos, puedes hacer lo siguiente:

En lugar de escribir:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.8+ sin `Annotated`

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...escribes:

//// tab | Python 3.8+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.8 sin `Annotated`

/// tip | Consejo

Prefiere usar la versión `Annotated` si es posible.

///

```Python
commons: CommonQueryParams = Depends()
```

////

Declaras la dependencia como el tipo del parámetro, y usas `Depends()` sin ningún parámetro, en lugar de tener que escribir la clase completa *otra vez* dentro de `Depends(CommonQueryParams)`.

El mismo ejemplo se vería entonces así:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...y **FastAPI** sabrá qué hacer.

/// tip | Consejo

Si eso parece más confuso que útil, ignóralo, no lo *necesitas*.

Es solo un atajo. Porque a **FastAPI** le importa ayudarte a minimizar la repetición de código.

///
