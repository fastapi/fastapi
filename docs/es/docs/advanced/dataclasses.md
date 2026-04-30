# Usando Dataclasses { #using-dataclasses }

FastAPI está construido sobre **Pydantic**, y te he estado mostrando cómo usar modelos de Pydantic para declarar requests y responses.

Pero FastAPI también soporta el uso de [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) de la misma manera:

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

Esto sigue siendo soportado gracias a **Pydantic**, ya que tiene [soporte interno para `dataclasses`](https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel).

Así que, incluso con el código anterior que no usa Pydantic explícitamente, FastAPI está usando Pydantic para convertir esos dataclasses estándar en su propia versión de dataclasses de Pydantic.

Y por supuesto, soporta lo mismo:

* validación de datos
* serialización de datos
* documentación de datos, etc.

Esto funciona de la misma manera que con los modelos de Pydantic. Y en realidad se logra de la misma manera internamente, utilizando Pydantic.

/// info | Información

Ten en cuenta que los dataclasses no pueden hacer todo lo que los modelos de Pydantic pueden hacer.

Así que, podrías necesitar seguir usando modelos de Pydantic.

Pero si tienes un montón de dataclasses por ahí, este es un buen truco para usarlos para potenciar una API web usando FastAPI. 🤓

///

## Dataclasses en `response_model` { #dataclasses-in-response-model }

También puedes usar `dataclasses` en el parámetro `response_model`:

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

El dataclass será automáticamente convertido a un dataclass de Pydantic.

De esta manera, su esquema aparecerá en la interfaz de usuario de la documentación de la API:

<img src="/img/tutorial/dataclasses/image01.png">

## Dataclasses en Estructuras de Datos Anidadas { #dataclasses-in-nested-data-structures }

También puedes combinar `dataclasses` con otras anotaciones de tipos para crear estructuras de datos anidadas.

En algunos casos, todavía podrías tener que usar la versión de `dataclasses` de Pydantic. Por ejemplo, si tienes errores con la documentación de la API generada automáticamente.

En ese caso, simplemente puedes intercambiar los `dataclasses` estándar con `pydantic.dataclasses`, que es un reemplazo directo:

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. Todavía importamos `field` de los `dataclasses` estándar.

2. `pydantic.dataclasses` es un reemplazo directo para `dataclasses`.

3. El dataclass `Author` incluye una lista de dataclasses `Item`.

4. El dataclass `Author` se usa como el parámetro `response_model`.

5. Puedes usar otras anotaciones de tipos estándar con dataclasses como el request body.

    En este caso, es una lista de dataclasses `Item`.

6. Aquí estamos regresando un diccionario que contiene `items`, que es una lista de dataclasses.

    FastAPI todavía es capaz de <dfn title="convertir los datos a un formato que pueda transmitirse">serializar</dfn> los datos a JSON.

7. Aquí el `response_model` está usando una anotación de tipo de una lista de dataclasses `Author`.

    Nuevamente, puedes combinar `dataclasses` con anotaciones de tipos estándar.

8. Nota que esta *path operation function* usa `def` regular en lugar de `async def`.

    Como siempre, en FastAPI puedes combinar `def` y `async def` según sea necesario.

    Si necesitas un repaso sobre cuándo usar cuál, revisa la sección _"¿Con prisa?"_ en la documentación sobre [`async` y `await`](../async.md#in-a-hurry).

9. Esta *path operation function* no está devolviendo dataclasses (aunque podría), sino una lista de diccionarios con datos internos.

    FastAPI usará el parámetro `response_model` (que incluye dataclasses) para convertir el response.

Puedes combinar `dataclasses` con otras anotaciones de tipos en muchas combinaciones diferentes para formar estructuras de datos complejas.

Revisa las anotaciones en el código arriba para ver más detalles específicos.

## Aprende Más { #learn-more }

También puedes combinar `dataclasses` con otros modelos de Pydantic, heredar de ellos, incluirlos en tus propios modelos, etc.

Para saber más, revisa la [documentación de Pydantic sobre dataclasses](https://docs.pydantic.dev/latest/concepts/dataclasses/).

## Versión { #version }

Esto está disponible desde la versión `0.67.0` de FastAPI. 🔖
