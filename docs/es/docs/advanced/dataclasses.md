# Usando Dataclasses

FastAPI está construido sobre **Pydantic**, y te he estado mostrando cómo usar modelos de Pydantic para declarar requests y responses.

Pero FastAPI también soporta el uso de <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> de la misma manera:

{* ../../docs_src/dataclasses/tutorial001.py hl[1,7:12,19:20] *}

Esto sigue siendo soportado gracias a **Pydantic**, ya que tiene <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">soporte interno para `dataclasses`</a>.

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

## Dataclasses en `response_model`

También puedes usar `dataclasses` en el parámetro `response_model`:

{* ../../docs_src/dataclasses/tutorial002.py hl[1,7:13,19] *}

El dataclass será automáticamente convertido a un dataclass de Pydantic.

De esta manera, su esquema aparecerá en la interfaz de usuario de la documentación de la API:

<img src="/img/tutorial/dataclasses/image01.png">

## Dataclasses en Estructuras de Datos Anidadas

También puedes combinar `dataclasses` con otras anotaciones de tipos para crear estructuras de datos anidadas.

En algunos casos, todavía podrías tener que usar la versión de `dataclasses` de Pydantic. Por ejemplo, si tienes errores con la documentación de la API generada automáticamente.

En ese caso, simplemente puedes intercambiar los `dataclasses` estándar con `pydantic.dataclasses`, que es un reemplazo directo:

{* ../../docs_src/dataclasses/tutorial003.py hl[1,5,8:11,14:17,23:25,28] *}

1. Todavía importamos `field` de los `dataclasses` estándar.

2. `pydantic.dataclasses` es un reemplazo directo para `dataclasses`.

3. El dataclass `Author` incluye una lista de dataclasses `Item`.

4. El dataclass `Author` se usa como el parámetro `response_model`.

5. Puedes usar otras anotaciones de tipos estándar con dataclasses como el request body.

    En este caso, es una lista de dataclasses `Item`.

6. Aquí estamos regresando un diccionario que contiene `items`, que es una lista de dataclasses.

    FastAPI todavía es capaz de <abbr title="converting the data to a format that can be transmitted">serializar</abbr> los datos a JSON.

7. Aquí el `response_model` está usando una anotación de tipo de una lista de dataclasses `Author`.

    Nuevamente, puedes combinar `dataclasses` con anotaciones de tipos estándar.

8. Nota que esta *path operation function* usa `def` regular en lugar de `async def`.

    Como siempre, en FastAPI puedes combinar `def` y `async def` según sea necesario.

    Si necesitas un repaso sobre cuándo usar cuál, revisa la sección _"¿Con prisa?"_ en la documentación sobre [`async` y `await`](../async.md#in-a-hurry){.internal-link target=_blank}.

9. Esta *path operation function* no está devolviendo dataclasses (aunque podría), sino una lista de diccionarios con datos internos.

    FastAPI usará el parámetro `response_model` (que incluye dataclasses) para convertir el response.

Puedes combinar `dataclasses` con otras anotaciones de tipos en muchas combinaciones diferentes para formar estructuras de datos complejas.

Revisa las anotaciones en el código arriba para ver más detalles específicos.

## Aprende Más

También puedes combinar `dataclasses` con otros modelos de Pydantic, heredar de ellos, incluirlos en tus propios modelos, etc.

Para saber más, revisa la <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">documentación de Pydantic sobre dataclasses</a>.

## Versión

Esto está disponible desde la versión `0.67.0` de FastAPI. 🔖
