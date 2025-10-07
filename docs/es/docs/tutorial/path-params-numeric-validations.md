# Parámetros de Path y Validaciones Numéricas

De la misma manera que puedes declarar más validaciones y metadatos para los parámetros de query con `Query`, puedes declarar el mismo tipo de validaciones y metadatos para los parámetros de path con `Path`.

## Importar Path

Primero, importa `Path` de `fastapi`, e importa `Annotated`:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | Información

FastAPI agregó soporte para `Annotated` (y comenzó a recomendar su uso) en la versión 0.95.0.

Si tienes una versión anterior, obtendrás errores al intentar usar `Annotated`.

Asegúrate de [Actualizar la versión de FastAPI](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} a al menos la 0.95.1 antes de usar `Annotated`.

///

## Declarar metadatos

Puedes declarar todos los mismos parámetros que para `Query`.

Por ejemplo, para declarar un valor de metadato `title` para el parámetro de path `item_id` puedes escribir:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | Nota

Un parámetro de path siempre es requerido ya que tiene que formar parte del path. Incluso si lo declaras con `None` o le asignas un valor por defecto, no afectará en nada, siempre será requerido.

///

## Ordena los parámetros como necesites

/// tip | Consejo

Esto probablemente no es tan importante o necesario si usas `Annotated`.

///

Supongamos que quieres declarar el parámetro de query `q` como un `str` requerido.

Y no necesitas declarar nada más para ese parámetro, así que realmente no necesitas usar `Query`.

Pero aún necesitas usar `Path` para el parámetro de path `item_id`. Y no quieres usar `Annotated` por alguna razón.

Python se quejará si pones un valor con un "default" antes de un valor que no tenga un "default".

Pero puedes reordenarlos y poner el valor sin un default (el parámetro de query `q`) primero.

No importa para **FastAPI**. Detectará los parámetros por sus nombres, tipos y declaraciones por defecto (`Query`, `Path`, etc.), no le importa el orden.

Así que puedes declarar tu función como:

{* ../../docs_src/path_params_numeric_validations/tutorial002.py hl[7] *}

Pero ten en cuenta que si usas `Annotated`, no tendrás este problema, no importará ya que no estás usando los valores por defecto de los parámetros de la función para `Query()` o `Path()`.

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py39.py *}

## Ordena los parámetros como necesites, trucos

/// tip | Consejo

Esto probablemente no es tan importante o necesario si usas `Annotated`.

///

Aquí hay un **pequeño truco** que puede ser útil, pero no lo necesitarás a menudo.

Si quieres:

* declarar el parámetro de query `q` sin un `Query` ni ningún valor por defecto
* declarar el parámetro de path `item_id` usando `Path`
* tenerlos en un orden diferente
* no usar `Annotated`

...Python tiene una sintaxis especial para eso.

Pasa `*`, como el primer parámetro de la función.

Python no hará nada con ese `*`, pero sabrá que todos los parámetros siguientes deben ser llamados como argumentos de palabras clave (parejas key-value), también conocidos como <abbr title="De: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. Incluso si no tienen un valor por defecto.

{* ../../docs_src/path_params_numeric_validations/tutorial003.py hl[7] *}

### Mejor con `Annotated`

Ten en cuenta que si usas `Annotated`, como no estás usando valores por defecto de los parámetros de la función, no tendrás este problema y probablemente no necesitarás usar `*`.

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py39.py hl[10] *}

## Validaciones numéricas: mayor o igual

Con `Query` y `Path` (y otros que verás más adelante) puedes declarar restricciones numéricas.

Aquí, con `ge=1`, `item_id` necesitará ser un número entero "`g`reater than or `e`qual" a `1`.

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py39.py hl[10] *}

## Validaciones numéricas: mayor que y menor o igual

Lo mismo aplica para:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py39.py hl[10] *}

## Validaciones numéricas: flotantes, mayor y menor

Las validaciones numéricas también funcionan para valores `float`.

Aquí es donde se convierte en importante poder declarar <abbr title="greater than"><code>gt</code></abbr> y no solo <abbr title="greater than or equal"><code>ge</code></abbr>. Ya que con esto puedes requerir, por ejemplo, que un valor sea mayor que `0`, incluso si es menor que `1`.

Así, `0.5` sería un valor válido. Pero `0.0` o `0` no lo serían.

Y lo mismo para <abbr title="less than"><code>lt</code></abbr>.

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py39.py hl[13] *}

## Resumen

Con `Query`, `Path` (y otros que aún no has visto) puedes declarar metadatos y validaciones de string de las mismas maneras que con [Parámetros de Query y Validaciones de String](query-params-str-validations.md){.internal-link target=_blank}.

Y también puedes declarar validaciones numéricas:

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

/// info | Información

`Query`, `Path` y otras clases que verás más adelante son subclases de una clase común `Param`.

Todas ellas comparten los mismos parámetros para validación adicional y metadatos que has visto.

///

/// note | Nota técnica

Cuando importas `Query`, `Path` y otros de `fastapi`, en realidad son funciones.

Que cuando se llaman, retornan instances de clases con el mismo nombre.

Así que importas `Query`, que es una función. Y cuando la llamas, retorna una instance de una clase también llamada `Query`.

Estas funciones están allí (en lugar de usar simplemente las clases directamente) para que tu editor no marque errores sobre sus tipos.

De esa forma puedes usar tu editor y herramientas de programación normales sin tener que agregar configuraciones personalizadas para omitir esos errores.

///
