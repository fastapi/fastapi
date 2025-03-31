# Tipos de Datos Extra

Hasta ahora, has estado usando tipos de datos comunes, como:

* `int`
* `float`
* `str`
* `bool`

Pero también puedes usar tipos de datos más complejos.

Y seguirás teniendo las mismas funcionalidades como hasta ahora:

* Gran soporte de editor.
* Conversión de datos de requests entrantes.
* Conversión de datos para datos de response.
* Validación de datos.
* Anotación y documentación automática.

## Otros tipos de datos

Aquí hay algunos de los tipos de datos adicionales que puedes usar:

* `UUID`:
    * Un "Identificador Universalmente Único" estándar, común como un ID en muchas bases de datos y sistemas.
    * En requests y responses se representará como un `str`.
* `datetime.datetime`:
    * Un `datetime.datetime` de Python.
    * En requests y responses se representará como un `str` en formato ISO 8601, como: `2008-09-15T15:53:00+05:00`.
* `datetime.date`:
    * `datetime.date` de Python.
    * En requests y responses se representará como un `str` en formato ISO 8601, como: `2008-09-15`.
* `datetime.time`:
    * Un `datetime.time` de Python.
    * En requests y responses se representará como un `str` en formato ISO 8601, como: `14:23:55.003`.
* `datetime.timedelta`:
    * Un `datetime.timedelta` de Python.
    * En requests y responses se representará como un `float` de segundos totales.
    * Pydantic también permite representarlo como una "codificación de diferencia horaria ISO 8601", <a href="https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers" class="external-link" target="_blank">consulta la documentación para más información</a>.
* `frozenset`:
    * En requests y responses, tratado igual que un `set`:
        * En requests, se leerá una list, eliminando duplicados y convirtiéndola en un `set`.
        * En responses, el `set` se convertirá en una `list`.
        * El esquema generado especificará que los valores del `set` son únicos (usando `uniqueItems` de JSON Schema).
* `bytes`:
    * `bytes` estándar de Python.
    * En requests y responses se tratará como `str`.
    * El esquema generado especificará que es un `str` con "binary" como "format".
* `Decimal`:
    * `Decimal` estándar de Python.
    * En requests y responses, manejado igual que un `float`.
* Puedes revisar todos los tipos de datos válidos de Pydantic aquí: <a href="https://docs.pydantic.dev/latest/usage/types/types/" class="external-link" target="_blank">Tipos de datos de Pydantic</a>.

## Ejemplo

Aquí tienes un ejemplo de una *path operation* con parámetros usando algunos de los tipos anteriores.

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

Nota que los parámetros dentro de la función tienen su tipo de dato natural, y puedes, por ejemplo, realizar manipulaciones de fechas normales, como:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
