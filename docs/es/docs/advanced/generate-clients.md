# Generando SDKs { #generating-sdks }

Como **FastAPI** está basado en la especificación **OpenAPI**, sus APIs se pueden describir en un formato estándar que muchas herramientas entienden.

Esto facilita generar **documentación** actualizada, paquetes de cliente (<abbr title="Software Development Kits – Kits de Desarrollo de Software">**SDKs**</abbr>) en múltiples lenguajes y **escribir pruebas** o **flujos de automatización** que se mantengan sincronizados con tu código.

En esta guía, aprenderás a generar un **SDK de TypeScript** para tu backend con FastAPI.

## Generadores de SDKs de código abierto { #open-source-sdk-generators }

Una opción versátil es el <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>, que soporta **muchos lenguajes de programación** y puede generar SDKs a partir de tu especificación OpenAPI.

Para **clientes de TypeScript**, <a href="https://heyapi.dev/" class="external-link" target="_blank">Hey API</a> es una solución diseñada específicamente, que ofrece una experiencia optimizada para el ecosistema de TypeScript.

Puedes descubrir más generadores de SDK en <a href="https://openapi.tools/#sdk" class="external-link" target="_blank">OpenAPI.Tools</a>.

/// tip | Consejo

FastAPI genera automáticamente especificaciones **OpenAPI 3.1**, así que cualquier herramienta que uses debe soportar esta versión.

///

## Generadores de SDKs de sponsors de FastAPI { #sdk-generators-from-fastapi-sponsors }

Esta sección destaca soluciones **respaldadas por empresas** y **venture-backed** de compañías que sponsorean FastAPI. Estos productos ofrecen **funcionalidades adicionales** e **integraciones** además de SDKs generados de alta calidad.

Al ✨ [**sponsorear FastAPI**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨, estas compañías ayudan a asegurar que el framework y su **ecosistema** se mantengan saludables y **sustentables**.

Su sponsorship también demuestra un fuerte compromiso con la **comunidad** de FastAPI (tú), mostrando que no solo les importa ofrecer un **gran servicio**, sino también apoyar un **framework robusto y próspero**, FastAPI. 🙇

Por ejemplo, podrías querer probar:

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainless.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

Algunas de estas soluciones también pueden ser open source u ofrecer niveles gratuitos, así que puedes probarlas sin un compromiso financiero. Hay otros generadores de SDK comerciales disponibles y se pueden encontrar en línea. 🤓

## Crea un SDK de TypeScript { #create-a-typescript-sdk }

Empecemos con una aplicación simple de FastAPI:

{* ../../docs_src/generate_clients/tutorial001_py39.py hl[7:9,12:13,16:17,21] *}

Nota que las *path operations* definen los modelos que usan para el payload del request y el payload del response, usando los modelos `Item` y `ResponseMessage`.

### Documentación de la API { #api-docs }

Si vas a `/docs`, verás que tiene los **esquemas** para los datos a enviar en requests y recibir en responses:

<img src="/img/tutorial/generate-clients/image01.png">

Puedes ver esos esquemas porque fueron declarados con los modelos en la app.

Esa información está disponible en el **OpenAPI schema** de la app, y luego se muestra en la documentación de la API.

Y esa misma información de los modelos que está incluida en OpenAPI es lo que puede usarse para **generar el código del cliente**.

### Hey API { #hey-api }

Una vez que tenemos una app de FastAPI con los modelos, podemos usar Hey API para generar un cliente de TypeScript. La forma más rápida de hacerlo es con npx.

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

Esto generará un SDK de TypeScript en `./src/client`.

Puedes aprender cómo <a href="https://heyapi.dev/openapi-ts/get-started" class="external-link" target="_blank">instalar `@hey-api/openapi-ts`</a> y leer sobre el <a href="https://heyapi.dev/openapi-ts/output" class="external-link" target="_blank">output generado</a> en su sitio web.

### Usar el SDK { #using-the-sdk }

Ahora puedes importar y usar el código del cliente. Podría verse así, nota que tienes autocompletado para los métodos:

<img src="/img/tutorial/generate-clients/image02.png">

También obtendrás autocompletado para el payload a enviar:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | Consejo

Nota el autocompletado para `name` y `price`, que fue definido en la aplicación de FastAPI, en el modelo `Item`.

///

Tendrás errores en línea para los datos que envíes:

<img src="/img/tutorial/generate-clients/image04.png">

El objeto de response también tendrá autocompletado:

<img src="/img/tutorial/generate-clients/image05.png">

## App de FastAPI con tags { #fastapi-app-with-tags }

En muchos casos tu app de FastAPI será más grande, y probablemente usarás tags para separar diferentes grupos de *path operations*.

Por ejemplo, podrías tener una sección para **items** y otra sección para **users**, y podrían estar separadas por tags:

{* ../../docs_src/generate_clients/tutorial002_py39.py hl[21,26,34] *}

### Genera un Cliente TypeScript con tags { #generate-a-typescript-client-with-tags }

Si generas un cliente para una app de FastAPI usando tags, normalmente también separará el código del cliente basándose en los tags.

De esta manera podrás tener las cosas ordenadas y agrupadas correctamente para el código del cliente:

<img src="/img/tutorial/generate-clients/image06.png">

En este caso tienes:

* `ItemsService`
* `UsersService`

### Nombres de los métodos del cliente { #client-method-names }

Ahora mismo los nombres de los métodos generados como `createItemItemsPost` no se ven muy limpios:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...eso es porque el generador del cliente usa el **operation ID** interno de OpenAPI para cada *path operation*.

OpenAPI requiere que cada operation ID sea único a través de todas las *path operations*, por lo que FastAPI usa el **nombre de la función**, el **path**, y el **método/operación HTTP** para generar ese operation ID, porque de esa manera puede asegurarse de que los operation IDs sean únicos.

Pero te mostraré cómo mejorar eso a continuación. 🤓

## Operation IDs personalizados y mejores nombres de métodos { #custom-operation-ids-and-better-method-names }

Puedes **modificar** la forma en que estos operation IDs son **generados** para hacerlos más simples y tener **nombres de métodos más simples** en los clientes.

En este caso tendrás que asegurarte de que cada operation ID sea **único** de alguna otra manera.

Por ejemplo, podrías asegurarte de que cada *path operation* tenga un tag, y luego generar el operation ID basado en el **tag** y el **name** de la *path operation* (el nombre de la función).

### Función personalizada para generar ID único { #custom-generate-unique-id-function }

FastAPI usa un **ID único** para cada *path operation*, se usa para el **operation ID** y también para los nombres de cualquier modelo personalizado necesario, para requests o responses.

Puedes personalizar esa función. Toma un `APIRoute` y retorna un string.

Por ejemplo, aquí está usando el primer tag (probablemente tendrás solo un tag) y el nombre de la *path operation* (el nombre de la función).

Puedes entonces pasar esa función personalizada a **FastAPI** como el parámetro `generate_unique_id_function`:

{* ../../docs_src/generate_clients/tutorial003_py39.py hl[6:7,10] *}

### Genera un Cliente TypeScript con operation IDs personalizados { #generate-a-typescript-client-with-custom-operation-ids }

Ahora, si generas el cliente de nuevo, verás que tiene los nombres de métodos mejorados:

<img src="/img/tutorial/generate-clients/image07.png">

Como ves, los nombres de métodos ahora tienen el tag y luego el nombre de la función, ahora no incluyen información del path de la URL y la operación HTTP.

### Preprocesa la especificación OpenAPI para el generador de clientes { #preprocess-the-openapi-specification-for-the-client-generator }

El código generado aún tiene algo de **información duplicada**.

Ya sabemos que este método está relacionado con los **items** porque esa palabra está en el `ItemsService` (tomado del tag), pero aún tenemos el nombre del tag prefijado en el nombre del método también. 😕

Probablemente aún querremos mantenerlo para OpenAPI en general, ya que eso asegurará que los operation IDs sean **únicos**.

Pero para el cliente generado podríamos **modificar** los operation IDs de OpenAPI justo antes de generar los clientes, solo para hacer esos nombres de métodos más bonitos y **limpios**.

Podríamos descargar el JSON de OpenAPI a un archivo `openapi.json` y luego podríamos **remover ese tag prefijado** con un script como este:

{* ../../docs_src/generate_clients/tutorial004_py39.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

Con eso, los operation IDs serían renombrados de cosas como `items-get_items` a solo `get_items`, de esa manera el generador del cliente puede generar nombres de métodos más simples.

### Genera un Cliente TypeScript con el OpenAPI preprocesado { #generate-a-typescript-client-with-the-preprocessed-openapi }

Como el resultado final ahora está en un archivo `openapi.json`, necesitas actualizar la ubicación de la entrada:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

Después de generar el nuevo cliente, ahora tendrías nombres de métodos **limpios**, con todo el **autocompletado**, **errores en línea**, etc:

<img src="/img/tutorial/generate-clients/image08.png">

## Beneficios { #benefits }

Cuando uses los clientes generados automáticamente obtendrás **autocompletado** para:

* Métodos.
* Payloads de request en el body, parámetros de query, etc.
* Payloads de response.

También tendrás **errores en línea** para todo.

Y cada vez que actualices el código del backend, y **regeneres** el frontend, tendrás las nuevas *path operations* disponibles como métodos, las antiguas eliminadas, y cualquier otro cambio se reflejará en el código generado. 🤓

Esto también significa que si algo cambió será **reflejado** automáticamente en el código del cliente. Y si haces **build** del cliente, dará error si tienes algún **desajuste** en los datos utilizados.

Así que, **detectarás muchos errores** muy temprano en el ciclo de desarrollo en lugar de tener que esperar a que los errores se muestren a tus usuarios finales en producción para luego intentar depurar dónde está el problema. ✨
