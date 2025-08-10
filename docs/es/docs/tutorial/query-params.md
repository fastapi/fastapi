# Parámetros de Query

Cuando declaras otros parámetros de función que no son parte de los parámetros de path, son automáticamente interpretados como parámetros de "query".

{* ../../docs_src/query_params/tutorial001.py hl[9] *}

La query es el conjunto de pares clave-valor que van después del `?` en una URL, separados por caracteres `&`.

Por ejemplo, en la URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...los parámetros de query son:

* `skip`: con un valor de `0`
* `limit`: con un valor de `10`

Como son parte de la URL, son "naturalmente" strings.

Pero cuando los declaras con tipos de Python (en el ejemplo anterior, como `int`), son convertidos a ese tipo y validados respecto a él.

Todo el mismo proceso que se aplica para los parámetros de path también se aplica para los parámetros de query:

* Soporte del editor (obviamente)
* <abbr title="convirtiendo el string que viene de un request HTTP en datos de Python">"Parsing"</abbr> de datos
* Validación de datos
* Documentación automática

## Valores por defecto

Como los parámetros de query no son una parte fija de un path, pueden ser opcionales y pueden tener valores por defecto.

En el ejemplo anterior, tienen valores por defecto de `skip=0` y `limit=10`.

Entonces, ir a la URL:

```
http://127.0.0.1:8000/items/
```

sería lo mismo que ir a:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Pero si vas a, por ejemplo:

```
http://127.0.0.1:8000/items/?skip=20
```

Los valores de los parámetros en tu función serán:

* `skip=20`: porque lo configuraste en la URL
* `limit=10`: porque ese era el valor por defecto

## Parámetros opcionales

De la misma manera, puedes declarar parámetros de query opcionales, estableciendo su valor por defecto en `None`:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

/// check | Revisa

Además, nota que **FastAPI** es lo suficientemente inteligente para notar que el parámetro de path `item_id` es un parámetro de path y `q` no lo es, por lo tanto, es un parámetro de query.

///

## Conversión de tipos en parámetros de query

También puedes declarar tipos `bool`, y serán convertidos:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

En este caso, si vas a:

```
http://127.0.0.1:8000/items/foo?short=1
```

o

```
http://127.0.0.1:8000/items/foo?short=True
```

o

```
http://127.0.0.1:8000/items/foo?short=true
```

o

```
http://127.0.0.1:8000/items/foo?short=on
```

o

```
http://127.0.0.1:8000/items/foo?short=yes
```

o cualquier otra variación (mayúsculas, primera letra en mayúscula, etc.), tu función verá el parámetro `short` con un valor `bool` de `True`. De lo contrario, será `False`.

## Múltiples parámetros de path y de query

Puedes declarar múltiples parámetros de path y de query al mismo tiempo, **FastAPI** sabe cuál es cuál.

Y no tienes que declararlos en un orden específico.

Serán detectados por nombre:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Parámetros de query requeridos

Cuando declaras un valor por defecto para parámetros que no son de path (por ahora, solo hemos visto parámetros de query), entonces no es requerido.

Si no quieres agregar un valor específico pero solo hacer que sea opcional, establece el valor por defecto como `None`.

Pero cuando quieres hacer un parámetro de query requerido, simplemente no declares ningún valor por defecto:

{* ../../docs_src/query_params/tutorial005.py hl[6:7] *}

Aquí el parámetro de query `needy` es un parámetro de query requerido de tipo `str`.

Si abres en tu navegador una URL como:

```
http://127.0.0.1:8000/items/foo-item
```

...sin agregar el parámetro requerido `needy`, verás un error como:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

Como `needy` es un parámetro requerido, necesitarías establecerlo en la URL:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...esto funcionaría:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

Y por supuesto, puedes definir algunos parámetros como requeridos, algunos con un valor por defecto, y algunos enteramente opcionales:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

En este caso, hay 3 parámetros de query:

* `needy`, un `str` requerido.
* `skip`, un `int` con un valor por defecto de `0`.
* `limit`, un `int` opcional.

/// tip | Consejo

También podrías usar `Enum`s de la misma manera que con [Parámetros de Path](path-params.md#predefined-values){.internal-link target=_blank}.

///
