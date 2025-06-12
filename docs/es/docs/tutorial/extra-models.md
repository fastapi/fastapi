# Modelos Extra

Continuando con el ejemplo anterior, será común tener más de un modelo relacionado.

Esto es especialmente el caso para los modelos de usuario, porque:

* El **modelo de entrada** necesita poder tener una contraseña.
* El **modelo de salida** no debería tener una contraseña.
* El **modelo de base de datos** probablemente necesitaría tener una contraseña hasheada.

/// danger | Peligro

Nunca almacenes contraseñas de usuarios en texto plano. Siempre almacena un "hash seguro" que puedas verificar luego.

Si no lo sabes, aprenderás qué es un "hash de contraseña" en los [capítulos de seguridad](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}.

///

## Múltiples modelos

Aquí tienes una idea general de cómo podrían ser los modelos con sus campos de contraseña y los lugares donde se utilizan:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

/// info | Información

En Pydantic v1 el método se llamaba `.dict()`, fue deprecado (pero aún soportado) en Pydantic v2, y renombrado a `.model_dump()`.

Los ejemplos aquí usan `.dict()` para compatibilidad con Pydantic v1, pero deberías usar `.model_dump()` en su lugar si puedes usar Pydantic v2.

///

### Acerca de `**user_in.dict()`

#### `.dict()` de Pydantic

`user_in` es un modelo Pydantic de la clase `UserIn`.

Los modelos Pydantic tienen un método `.dict()` que devuelve un `dict` con los datos del modelo.

Así que, si creamos un objeto Pydantic `user_in` como:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

y luego llamamos a:

```Python
user_dict = user_in.dict()
```

ahora tenemos un `dict` con los datos en la variable `user_dict` (es un `dict` en lugar de un objeto modelo Pydantic).

Y si llamamos a:

```Python
print(user_dict)
```

obtendremos un `dict` de Python con:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Desempaquetando un `dict`

Si tomamos un `dict` como `user_dict` y lo pasamos a una función (o clase) con `**user_dict`, Python lo "desempaquetará". Pasará las claves y valores del `user_dict` directamente como argumentos clave-valor.

Así que, continuando con el `user_dict` anterior, escribir:

```Python
UserInDB(**user_dict)
```

sería equivalente a algo como:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

O más exactamente, usando `user_dict` directamente, con cualquier contenido que pueda tener en el futuro:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### Un modelo Pydantic a partir del contenido de otro

Como en el ejemplo anterior obtuvimos `user_dict` de `user_in.dict()`, este código:

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

sería equivalente a:

```Python
UserInDB(**user_in.dict())
```

...porque `user_in.dict()` es un `dict`, y luego hacemos que Python lo "desempaquete" al pasarlo a `UserInDB` con el prefijo `**`.

Así, obtenemos un modelo Pydantic a partir de los datos en otro modelo Pydantic.

#### Desempaquetando un `dict` y palabras clave adicionales

Y luego agregando el argumento de palabra clave adicional `hashed_password=hashed_password`, como en:

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

...termina siendo como:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | Advertencia

Las funciones adicionales de soporte `fake_password_hasher` y `fake_save_user` son solo para demostrar un posible flujo de datos, pero por supuesto no proporcionan ninguna seguridad real.

///

## Reducir duplicación

Reducir la duplicación de código es una de las ideas centrales en **FastAPI**.

Ya que la duplicación de código incrementa las posibilidades de bugs, problemas de seguridad, problemas de desincronización de código (cuando actualizas en un lugar pero no en los otros), etc.

Y estos modelos están compartiendo muchos de los datos y duplicando nombres y tipos de atributos.

Podríamos hacerlo mejor.

Podemos declarar un modelo `UserBase` que sirva como base para nuestros otros modelos. Y luego podemos hacer subclases de ese modelo que heredan sus atributos (declaraciones de tipo, validación, etc).

Toda la conversión de datos, validación, documentación, etc. seguirá funcionando normalmente.

De esa manera, podemos declarar solo las diferencias entre los modelos (con `password` en texto plano, con `hashed_password` y sin contraseña):

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` o `anyOf`

Puedes declarar un response que sea la `Union` de dos o más tipos, eso significa que el response sería cualquiera de ellos.

Se definirá en OpenAPI con `anyOf`.

Para hacerlo, usa el type hint estándar de Python <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>:

/// note | Nota

Al definir una <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a>, incluye el tipo más específico primero, seguido por el tipo menos específico. En el ejemplo a continuación, el más específico `PlaneItem` viene antes de `CarItem` en `Union[PlaneItem, CarItem]`.

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}


### `Union` en Python 3.10

En este ejemplo pasamos `Union[PlaneItem, CarItem]` como el valor del argumento `response_model`.

Porque lo estamos pasando como un **valor a un argumento** en lugar de ponerlo en una **anotación de tipo**, tenemos que usar `Union` incluso en Python 3.10.

Si estuviera en una anotación de tipo podríamos haber usado la barra vertical, como:

```Python
some_variable: PlaneItem | CarItem
```

Pero si ponemos eso en la asignación `response_model=PlaneItem | CarItem` obtendríamos un error, porque Python intentaría realizar una **operación inválida** entre `PlaneItem` y `CarItem` en lugar de interpretar eso como una anotación de tipo.

## Lista de modelos

De la misma manera, puedes declarar responses de listas de objetos.

Para eso, usa el `typing.List` estándar de Python (o simplemente `list` en Python 3.9 y posteriores):

{* ../../docs_src/extra_models/tutorial004_py39.py hl[18] *}


## Response con `dict` arbitrario

También puedes declarar un response usando un `dict` arbitrario plano, declarando solo el tipo de las claves y valores, sin usar un modelo Pydantic.

Esto es útil si no conoces los nombres de los campos/atributos válidos (que serían necesarios para un modelo Pydantic) de antemano.

En este caso, puedes usar `typing.Dict` (o solo `dict` en Python 3.9 y posteriores):

{* ../../docs_src/extra_models/tutorial005_py39.py hl[6] *}


## Recapitulación

Usa múltiples modelos Pydantic y hereda libremente para cada caso.

No necesitas tener un solo modelo de datos por entidad si esa entidad debe poder tener diferentes "estados". Como el caso con la "entidad" usuario con un estado que incluye `password`, `password_hash` y sin contraseña.
