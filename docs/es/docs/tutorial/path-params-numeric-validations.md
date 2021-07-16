# Parámetros de path y validaciones numéricas

De la misma forma en que puedes declarar más validaciones y metadata para parámetros de query con `Query`, también puedes declarar el mismo tipo de validaciones y metadata para parámetros de path con `Path`.

## Importar Path

Primero, importa `Path` desde `fastapi`:


```Python hl_lines="3"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

## Declarar metadata

Tú puedes declarar todos los mismos parámetros que para `Query`.

Por ejemplo, para declarar un `title` como valor de metadata para el parámetro de path `item_id` puedes escribir:

```Python hl_lines="10"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

!!! nota
    Un parámetro de path siempre es requerido ya que tiene que ser parte de la <abbr title="path">*ruta*</abbr>.
    
    Por esto, deberías declararlo con `...` para marcarlo como requerido.

    Sin embargo, incluso si lo declaraste con `None` o asignaste un valor por defecto, no afectaría en nada, él seguiría siendo requerido.

## Ordena los parámetros como necesites

Digamos que tú quieres declarar el parámetro de query `q` como un `str` requerido.

Y no necesitas declarar nada más para ese parámetro, es decir, realmente no necesitas usar `Query`.

Pero si necesitas usar `Path` para el parámetro de path `item_id`.

Python se quejará si colocas un atributo con un valor por defecto antes que un atributo que no tienes valor por defecto.

Pero tu puedes reordenarlos, y tener el attributo sin valor por defecto (el parámetro de query `q`) primero.

Para **FastAPI** esto no importa. FastAPI detectará los parámetros por sus nombres, tipos y declaraciones predeterminadas (`Query`, `Path`, etc), no se preocupa por el orden.

Siendo así, puedes declarar tu función de la siguiente manera:

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

## Ordena los parámetros como necesites, trucos

Si quieres declarar el parámetro de query `q` sin un `Query` or cualquier valor por defecto, y el parámetro de path `item_id` usando `Path`, y tenerlos en un orden diferente, Python tiene una sintaxis especial para eso.

Pasa `*`, como el primer parámetro de la función.

Python no hará nada con ese `*`, pero sabrá que todos los parámetros siguientes deberán ser llamados como argumentos keyword (pares clave-valor), también conocidos como <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. Incluso si no tienen un valor por defecto.

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

## Validaciones numéricas: mayor o igual que

Con `Query` y `Path` (y otros que verás más adelante) puedes declarar restriciones para strings, pero también restricciones para números.

Aquí, con `ge=1`, `item_id` tendrá que ser un número entero mayor o igual que `1`.

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

## Validaciones numéricas: mayor que y menor o igual que

Lo mismo aplica para:

* `gt`: mayor que
* `le`: menor o igual que

```Python hl_lines="9"
{!../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

## Validaciones numéricas: floats, mayor que y menor que

Validaciones numéricas también funcionan para valores `float`.

Aquí es donde se vuelve importante ser capaces de declarar <abbr title="mayor que"><code>gt</code></abbr> y no solo <abbr title="mayor o igual que"><code>ge</code></abbr>. Ya que con `gt` puedes requerir, por ejemplo, que el valor tenga que ser mayor que `0`, incluso si es menor que `1`. 

Así, `0.5` sería un valor válido. Pero `0.0` o `0` no lo serían.

Y lo mismo para <abbr title="menor que"><code>lt</code></abbr>.

```Python hl_lines="11"
{!../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

## Recapitulación

Con `Query`, `Path` (y otros que no has visto aún) puedes declarar metadata y validaciones de strings de la misma manera que con [Parámetros de query y Validaciones de String](query-params-str-validations.md){.internal-link target=_blank}.

Y también puedes declarar validaciones numéricas:

* `gt`: mayor que
* `ge`: mayor o igual que
* `lt`: menor que
* `le`: menor o igual que

!!! info
    `Query`, `Path`, y otros que verás más adelante son subclases de la clase común `Param` (que no necesitas usar).

    Todos ellos comparten los mismos parámetros de validaciones adicionales y metadata que ya has visto.

!!! note "Detalles técnicos"
    Cuando importas `Query`, `Path` y demás desde `fastapi`, ellos en realidad son funciones.

    Que cuando son llamados, retornan instancias de clases del mismo nombre.

    Entonces, tú importas `Query`, que es una función. Y cuando la llamas, la función retorna una instancia de la clase también llamada `Query`.

    Estas funciones estan allí (en vez de usar las clases directamente) para que tu editor no marque errores por sus tipos.

    De esta manera puedes usar tu editor y herramientas para codificar sin tener que agregar configuraciones especiales para ignorar esos errores.
