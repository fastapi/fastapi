# Parámetros de consulta y validaciones para cadenas de texto

**FastAPI** te permite declarar información adicional y validación de tus parámetros.

Tomemos esta aplicación como ejemplo:

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial001.py!}
```

El parámetro de consulta `q` es de tipo `Optional[str]`, eso significa que es de tipo `str` pero tambien podria ser `None`, y de hecho, el valor predeterminado es `None`, así FastAPI sabrá que no es necesario.

!!! nota
    FastAPI sabrá que el valor de `q` no es necesario debido al valor predeterminado `= None`.

    El `Optional` en `Optional[str]` no es usado por FastAPI, pero le permitirá a tu editor de texto darte un mejor soporte y detectar errores.

## Validación adicional

Vamos a enfatizar que aunque  `q` es opcional, siempre que se proporcione, **su longitud no superé los 50 caracteres**.

### Importar `Query`

Para lograr esto, primero debes importar `Query` desde `fastapi`:

```Python hl_lines="3"
{!../../../docs_src/query_params_str_validations/tutorial002.py!}
```

## Usar `Query` como el valor predeterminado

Y ahora utilízalo como el valor predeterminado de su parámetro, configurando el parámetro `max_length` a 50:

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial002.py!}
```

Como tenemos que reemplazar el valor predeterminado `None` con `Query(None)`, el primer parámetro para `Query` cumple el mismo propósito de definir el valor predeterminado.

Entonces:

```Python
q: Optional[str] = Query(None)
```

...hace que el parámetro sea opcional, al igual que:

```Python
q: Optional[str] = None
```

Pero lo declara explícitamente como si fuese un parámetro de consulta.

!!! información
    Ten en mente que FastAPI se ocupa de la parte de:

    ```Python
    = None
    ```

    o de:

    ```Python
    = Query(None)
    ```

    y usará `None` para detectar que el parámatro de consulta no es requerido.

    La parte `Optional` es solo para permitirle a tu editor proveer un mejor soporte.

Entonces, podemos pasar más parámetros a `Query`. En este caso, el parámetro `max_length` que aplica para cadenas de texto:

```Python
q: str = Query(None, max_length=50)
```

Esto validará los datos, mostrará un error claro cuando los datos no sean válidos y documentará el parámetro en el esquema de OpenAPI *ruta de operación*.

## Agrega más validaciones

Tambien puedes agregar el parametro `min_length`:

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial003.py!}
```

## Agrega una expresión regular

Puedes definir una <abbr title="Una expresión regular, regex o regexp es una secuencia de caracteres que define un patrón de búsqueda para cadenas de texto.">expresión regular</abbr> que el parámetro debería cumplir:

```Python hl_lines="10"
{!../../../docs_src/query_params_str_validations/tutorial004.py!}
```

Esta expresión regular verifica que el valor del parámetro recibido:

* `^`:  comienza con los caracteres que siguen y no tiene otros caracteres antes.
* `fixedquery`: tiene el valor exacto de `fixedquery`.
* `$`: termina allí, no tiene más caracteres después de `fixedquery`.

Si te sientes perdido con todo estos de **"expresiones regulares"**, no te preocupes. Son un tema difícil para mucha gente. Todavía puedes hacer muchas cosas sin necesitar expresiones regulares todavía.

Pero en el momento que las necesites y aprendas a utilizarlas, debes saber que puedes usarlas directamente en **FastAPI**.

## Valores predeterminados

De la misma manera que puedes pasar `None` como primer argumento a utilizar como valor predeterminado, puedes pasar otros valores.

Digamos que quieres declarar el parámetro de consulta `q` que tendrá un `min_length` de `3`, y un valor predeterminado de `"fixedquery"`:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial005.py!}
```

!!! nota
    Tener un valor predeterminado también hace que el parámetro sea opcional.

## Hazlo requerido

Cuando no necesitemos declarar más validaciones o metadatos, podemos hacer el parámetro de consulta `q` sea requerido simplemente dejando de declarar un valor predeterminado, como:

```Python
q: str
```

en vez de:

```Python
q: Optional[str] = None
```

Pero ahora lo estamos declarando con `Query`, por ejemplo como:

```Python
q: Optional[str] = Query(None, min_length=3)
```

Entonces, cuando necesites declarar un valor como requerido mientras usas `Query`, puedes usar `...` como el primer argumento:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial006.py!}
```

!!! información
    Si no has visto `...` antes: es un valor único especial, es <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">parte de Python y se llama "Elipsis"</a>.

Esto le permitira a **FastAPI** saber cuando es un parámetro es requerido.

## Lista de parámetros de consulta / valores múltiples


Cuando defines un parámetro de consulta explícitamente con `Query`, también puedes declararlo para recibir una lista de valores, o dicho de otra forma, para recibir múltiples valores.

Por ejemplo, para declarar un parámetro de consulta `q` que puede aparecer varias veces en la URL, puedes escribir:

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial011.py!}
```

Entonces, con una URL como:

```
http://localhost:8000/items/?q=foo&q=bar
```

recibirás los múltiples parámetros de consulta `q` (`foo` y `bar`) en un `list` de Python dentro de tu *función de operación de ruta*, en el *parámetro de función* `q`.

Entonces, la respuesta de esa URL sería:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

!!! tip
    Para declarar un parámetro de consulta de tipo `list`, como en el ejemplo anterior, necesitas usar explícitamente `Query`, de lo contrario, se interpretaría como el cuerpo de solicitud.

Los documentos de la API interactiva se actualizarán en concordancia para permitir múltiples valores:

<img src="https://fastapi.tiangolo.com/img/tutorial/query-params-str-validations/image02.png">

### Consultar lista de parámetros / valores múltiples con valores predeterminados

 Y también puedes definir una lista (`list`) predeterminada de valores si no se proporciona ninguno:

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial012.py!}
```

Si vas a:

```
http://localhost:8000/items/
```

el valor predeterminado de `q` sera: `["foo", "bar"]` y tu respuesta será:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### Usando `list`

También puedes usar `list` directamente en lugar de `List[str]`:

```Python hl_lines="7"
{!../../../docs_src/query_params_str_validations/tutorial013.py!}
```

!!! nota
    Ten en cuenta que, en este caso, FastAPI no comprobará el contenido de la lista

    Por ejemplo, `List[int]` comprobaría (y documentaria) que el contenido de la lista son números enteros. Pero la `list` sola no lo haría.

## Declare más metadatos

Puedes agregar más información sobre el parámetro.

Esa información se incluirá en la documentación OpenAPI generada y se utilizarán por las interfaces de usuario y herramientas externas de documentación.

!!! nota
    Ten en cuenta que diferentes herramientas pueden tener diferentes niveles de soporte con OpenAPI.

    Algunas podrían no mostrar aún toda la información extra declarada todavía, aunque en la mayoría de los casos esta funcionalidad faltante ya ha sido planificada para ser desarrollada.

Puedes agregar un título `title`:

```Python hl_lines="10"
{!../../../docs_src/query_params_str_validations/tutorial007.py!}
```

y una descripción `description`:

```Python hl_lines="13"
{!../../../docs_src/query_params_str_validations/tutorial008.py!}
```

## Parámetros de alias

Imagina que quieres que el parámetro sea `item-query`.

Como en:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

Pero `item-query` no es un nombre de variable de Python válido.

la opción más parecida sería `item_query`.

Pero aún necesitas que sea exactamente `item-query`...

Entonces puedes declarar un `alias`, y ese alias es lo que se utilizará para encontrar el valor del parámetro:

```Python hl_lines="9"
{!../../../docs_src/query_params_str_validations/tutorial009.py!}
```

## Desactivación de parámetros

Ahora digamos que ya no te gusta un parámetro.

Tienes que dejarlo ahí un rato porque hay clientes usándolo, pero quieres que los documentos lo muestren claramente como <abbr title="obsoleto, se recomienda no usarlo">obsoleto</abbr>.

Entonces pasa el parámetro `deprecated=True` to `Query`:

```Python hl_lines="18"
{!../../../docs_src/query_params_str_validations/tutorial010.py!}
```

Los documentos lo mostrarán así:

<img src="https://fastapi.tiangolo.com/img/tutorial/query-params-str-validations/image01.png">

## Resumen

Puedes declarar validaciones y metadatos adicionales para sus parámetros.

Validaciones genéricas y metadatos:

* `alias`
* `title`
* `description`
* `deprecated`

Validaciones específicas para cadenas de texto:

* `min_length`
* `max_length`
* `regex`

En estos ejemplos, viste cómo declarar validaciones para valores `str`.

Revisa los siguientes capítulos para ver cómo declarar validaciones para otros tipos, como números.
