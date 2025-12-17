# Parámetros de Path { #path-parameters }

Puedes declarar "parámetros" o "variables" de path con la misma sintaxis que se usa en los format strings de Python:

{* ../../docs_src/path_params/tutorial001_py39.py hl[6:7] *}

El valor del parámetro de path `item_id` se pasará a tu función como el argumento `item_id`.

Así que, si ejecutas este ejemplo y vas a <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, verás un response de:

```JSON
{"item_id":"foo"}
```

## Parámetros de path con tipos { #path-parameters-with-types }

Puedes declarar el tipo de un parámetro de path en la función, usando anotaciones de tipos estándar de Python:

{* ../../docs_src/path_params/tutorial002_py39.py hl[7] *}

En este caso, `item_id` se declara como un `int`.

/// check | Revisa

Esto te dará soporte del editor dentro de tu función, con chequeo de errores, autocompletado, etc.

///

## <abbr title="también conocido como: serialización, parsing, marshalling">Conversión</abbr> de datos { #data-conversion }

Si ejecutas este ejemplo y abres tu navegador en <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, verás un response de:

```JSON
{"item_id":3}
```

/// check | Revisa

Nota que el valor que tu función recibió (y devolvió) es `3`, como un `int` de Python, no un string `"3"`.

Entonces, con esa declaración de tipo, **FastAPI** te ofrece <abbr title="convertir el string que viene de un request HTTP en datos de Python">"parsing"</abbr> automático de request.

///

## Validación de datos { #data-validation }

Pero si vas al navegador en <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, verás un bonito error HTTP de:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

porque el parámetro de path `item_id` tenía un valor de `"foo"`, que no es un `int`.

El mismo error aparecería si proporcionaras un `float` en lugar de un `int`, como en: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check | Revisa

Entonces, con la misma declaración de tipo de Python, **FastAPI** te ofrece validación de datos.

Nota que el error también indica claramente el punto exacto donde la validación falló.

Esto es increíblemente útil mientras desarrollas y depuras código que interactúa con tu API.

///

## Documentación { #documentation }

Y cuando abras tu navegador en <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, verás una documentación de API automática e interactiva como:

<img src="/img/tutorial/path-params/image01.png">

/// check | Revisa

Nuevamente, solo con esa misma declaración de tipo de Python, **FastAPI** te ofrece documentación automática e interactiva (integrando Swagger UI).

Nota que el parámetro de path está declarado como un entero.

///

## Beneficios basados en estándares, documentación alternativa { #standards-based-benefits-alternative-documentation }

Y porque el esquema generado es del estándar <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>, hay muchas herramientas compatibles.

Debido a esto, el propio **FastAPI** proporciona una documentación de API alternativa (usando ReDoc), a la cual puedes acceder en <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>:

<img src="/img/tutorial/path-params/image02.png">

De la misma manera, hay muchas herramientas compatibles. Incluyendo herramientas de generación de código para muchos lenguajes.

## Pydantic { #pydantic }

Toda la validación de datos se realiza internamente con <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, así que obtienes todos los beneficios de esta. Y sabes que estás en buenas manos.

Puedes usar las mismas declaraciones de tipo con `str`, `float`, `bool` y muchos otros tipos de datos complejos.

Varios de estos se exploran en los siguientes capítulos del tutorial.

## El orden importa { #order-matters }

Al crear *path operations*, puedes encontrarte en situaciones donde tienes un path fijo.

Como `/users/me`, imaginemos que es para obtener datos sobre el usuario actual.

Y luego también puedes tener un path `/users/{user_id}` para obtener datos sobre un usuario específico por algún ID de usuario.

Debido a que las *path operations* se evalúan en orden, necesitas asegurarte de que el path para `/users/me` se declara antes que el de `/users/{user_id}`:

{* ../../docs_src/path_params/tutorial003_py39.py hl[6,11] *}

De lo contrario, el path para `/users/{user_id}` también coincidiría para `/users/me`, "pensando" que está recibiendo un parámetro `user_id` con un valor de `"me"`.

De manera similar, no puedes redefinir una path operation:

{* ../../docs_src/path_params/tutorial003b_py39.py hl[6,11] *}

La primera siempre será utilizada ya que el path coincide primero.

## Valores predefinidos { #predefined-values }

Si tienes una *path operation* que recibe un *path parameter*, pero quieres que los valores posibles válidos del *path parameter* estén predefinidos, puedes usar un <abbr title="Enumeration – Enumeración">`Enum`</abbr> estándar de Python.

### Crear una clase `Enum` { #create-an-enum-class }

Importa `Enum` y crea una subclase que herede de `str` y de `Enum`.

Al heredar de `str`, la documentación de la API podrá saber que los valores deben ser de tipo `string` y podrá representarlos correctamente.

Luego crea atributos de clase con valores fijos, que serán los valores válidos disponibles:

{* ../../docs_src/path_params/tutorial005_py39.py hl[1,6:9] *}

/// tip | Consejo

Si te estás preguntando, "AlexNet", "ResNet" y "LeNet" son solo nombres de <abbr title="Técnicamente, arquitecturas de modelos de Deep Learning">modelos</abbr> de Machine Learning.

///

### Declarar un *path parameter* { #declare-a-path-parameter }

Luego crea un *path parameter* con una anotación de tipo usando la clase enum que creaste (`ModelName`):

{* ../../docs_src/path_params/tutorial005_py39.py hl[16] *}

### Revisa la documentación { #check-the-docs }

Como los valores disponibles para el *path parameter* están predefinidos, la documentación interactiva puede mostrarlos de manera ordenada:

<img src="/img/tutorial/path-params/image03.png">

### Trabajando con *enumeraciones* de Python { #working-with-python-enumerations }

El valor del *path parameter* será un *miembro* de enumeración.

#### Comparar *miembros* de enumeraciones { #compare-enumeration-members }

Puedes compararlo con el *miembro* de enumeración en tu enum creada `ModelName`:

{* ../../docs_src/path_params/tutorial005_py39.py hl[17] *}

#### Obtener el valor de *enumeración* { #get-the-enumeration-value }

Puedes obtener el valor actual (un `str` en este caso) usando `model_name.value`, o en general, `your_enum_member.value`:

{* ../../docs_src/path_params/tutorial005_py39.py hl[20] *}

/// tip | Consejo

También podrías acceder al valor `"lenet"` con `ModelName.lenet.value`.

///

#### Devolver *miembros* de enumeración { #return-enumeration-members }

Puedes devolver *miembros de enum* desde tu *path operation*, incluso anidados en un cuerpo JSON (por ejemplo, un `dict`).

Serán convertidos a sus valores correspondientes (cadenas en este caso) antes de devolverlos al cliente:

{* ../../docs_src/path_params/tutorial005_py39.py hl[18,21,23] *}

En tu cliente recibirás un response JSON como:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Parámetros de path conteniendo paths { #path-parameters-containing-paths }

Imaginemos que tienes una *path operation* con un path `/files/{file_path}`.

Pero necesitas que `file_path` en sí mismo contenga un *path*, como `home/johndoe/myfile.txt`.

Entonces, la URL para ese archivo sería algo como: `/files/home/johndoe/myfile.txt`.

### Soporte de OpenAPI { #openapi-support }

OpenAPI no soporta una manera de declarar un *path parameter* para que contenga un *path* dentro, ya que eso podría llevar a escenarios que son difíciles de probar y definir.

Sin embargo, todavía puedes hacerlo en **FastAPI**, usando una de las herramientas internas de Starlette.

Y la documentación seguiría funcionando, aunque no agregue ninguna documentación indicando que el parámetro debe contener un path.

### Convertidor de Path { #path-convertor }

Usando una opción directamente de Starlette puedes declarar un *path parameter* conteniendo un *path* usando una URL como:

```
/files/{file_path:path}
```

En este caso, el nombre del parámetro es `file_path`, y la última parte, `:path`, indica que el parámetro debería coincidir con cualquier *path*.

Así que, puedes usarlo con:

{* ../../docs_src/path_params/tutorial004_py39.py hl[6] *}

/// tip | Consejo

Podrías necesitar que el parámetro contenga `/home/johndoe/myfile.txt`, con una barra inclinada (`/`) inicial.

En ese caso, la URL sería: `/files//home/johndoe/myfile.txt`, con una doble barra inclinada (`//`) entre `files` y `home`.

///

## Resumen { #recap }

Con **FastAPI**, al usar declaraciones de tipo estándar de Python, cortas e intuitivas, obtienes:

* Soporte del editor: chequeo de errores, autocompletado, etc.
* "<abbr title="convertir el string que viene de un request HTTP en datos de Python">parsing</abbr>" de datos
* Validación de datos
* Anotación de API y documentación automática

Y solo tienes que declararlos una vez.

Probablemente esa sea la principal ventaja visible de **FastAPI** en comparación con otros frameworks alternativos (aparte del rendimiento bruto).
