# Webhooks de OpenAPI

Hay casos donde quieres decirle a los **usuarios** de tu API que tu aplicación podría llamar a *su* aplicación (enviando una request) con algunos datos, normalmente para **notificar** de algún tipo de **evento**.

Esto significa que en lugar del proceso normal de tus usuarios enviando requests a tu API, es **tu API** (o tu aplicación) la que podría **enviar requests a su sistema** (a su API, su aplicación).

Esto normalmente se llama un **webhook**.

## Pasos de los webhooks

El proceso normalmente es que **tú defines** en tu código cuál es el mensaje que enviarás, el **body de la request**.

También defines de alguna manera en qué **momentos** tu aplicación enviará esas requests o eventos.

Y **tus usuarios** definen de alguna manera (por ejemplo en un panel web en algún lugar) el **URL** donde tu aplicación debería enviar esas requests.

Toda la **lógica** sobre cómo registrar los URLs para webhooks y el código para realmente enviar esas requests depende de ti. Lo escribes como quieras en **tu propio código**.

## Documentando webhooks con **FastAPI** y OpenAPI

Con **FastAPI**, usando OpenAPI, puedes definir los nombres de estos webhooks, los tipos de operaciones HTTP que tu aplicación puede enviar (por ejemplo, `POST`, `PUT`, etc.) y los **bodies** de las requests que tu aplicación enviaría.

Esto puede hacer mucho más fácil para tus usuarios **implementar sus APIs** para recibir tus requests de **webhook**, incluso podrían ser capaces de autogenerar algo de su propio código de API.

/// info | Información

Los webhooks están disponibles en OpenAPI 3.1.0 y superiores, soportados por FastAPI `0.99.0` y superiores.

///

## Una aplicación con webhooks

Cuando creas una aplicación de **FastAPI**, hay un atributo `webhooks` que puedes usar para definir *webhooks*, de la misma manera que definirías *path operations*, por ejemplo con `@app.webhooks.post()`.

{* ../../docs_src/openapi_webhooks/tutorial001.py hl[9:13,36:53] *}

Los webhooks que defines terminarán en el esquema de **OpenAPI** y en la interfaz automática de **documentación**.

/// info | Información

El objeto `app.webhooks` es en realidad solo un `APIRouter`, el mismo tipo que usarías al estructurar tu aplicación con múltiples archivos.

///

Nota que con los webhooks en realidad no estás declarando un *path* (como `/items/`), el texto que pasas allí es solo un **identificador** del webhook (el nombre del evento), por ejemplo en `@app.webhooks.post("new-subscription")`, el nombre del webhook es `new-subscription`.

Esto es porque se espera que **tus usuarios** definan el actual **URL path** donde quieren recibir la request del webhook de alguna otra manera (por ejemplo, un panel web).

### Revisa la documentación

Ahora puedes iniciar tu app e ir a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Verás que tu documentación tiene las *path operations* normales y ahora también algunos **webhooks**:

<img src="/img/tutorial/openapi-webhooks/image01.png">
