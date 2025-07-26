# Genera Clientes

Como **FastAPI** está basado en la especificación OpenAPI, obtienes compatibilidad automática con muchas herramientas, incluyendo la documentación automática de la API (proporcionada por Swagger UI).

Una ventaja particular que no es necesariamente obvia es que puedes **generar clientes** (a veces llamados <abbr title="Software Development Kits">**SDKs**</abbr> ) para tu API, para muchos **lenguajes de programación** diferentes.

## Generadores de Clientes OpenAPI

Hay muchas herramientas para generar clientes desde **OpenAPI**.

Una herramienta común es <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>.

Si estás construyendo un **frontend**, una alternativa muy interesante es <a href="https://github.com/hey-api/openapi-ts" class="external-link" target="_blank">openapi-ts</a>.

## Generadores de Clientes y SDKs - Sponsor

También hay algunos generadores de Clientes y SDKs **respaldados por empresas** basados en OpenAPI (FastAPI), en algunos casos pueden ofrecerte **funcionalidades adicionales** además de SDKs/clientes generados de alta calidad.

Algunos de ellos también ✨ [**sponsorean FastAPI**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨, esto asegura el **desarrollo** continuo y saludable de FastAPI y su **ecosistema**.

Y muestra su verdadero compromiso con FastAPI y su **comunidad** (tú), ya que no solo quieren proporcionarte un **buen servicio** sino también asegurarse de que tengas un **buen y saludable framework**, FastAPI. 🙇

Por ejemplo, podrías querer probar:

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainlessapi.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi/?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

También hay varias otras empresas que ofrecen servicios similares que puedes buscar y encontrar en línea. 🤓

## Genera un Cliente Frontend en TypeScript

Empecemos con una aplicación simple de FastAPI:

{* ../../docs_src/generate_clients/tutorial001_py39.py hl[7:9,12:13,16:17,21] *}

Nota que las *path operations* definen los modelos que usan para el payload de la petición y el payload del response, usando los modelos `Item` y `ResponseMessage`.

### Documentación de la API

Si vas a la documentación de la API, verás que tiene los **esquemas** para los datos que se enviarán en las peticiones y se recibirán en los responses:

<img src="/img/tutorial/generate-clients/image01.png">

Puedes ver esos esquemas porque fueron declarados con los modelos en la aplicación.

Esa información está disponible en el **JSON Schema** de OpenAPI de la aplicación, y luego se muestra en la documentación de la API (por Swagger UI).

Y esa misma información de los modelos que está incluida en OpenAPI es lo que puede usarse para **generar el código del cliente**.

### Genera un Cliente en TypeScript

Ahora que tenemos la aplicación con los modelos, podemos generar el código del cliente para el frontend.

#### Instalar `openapi-ts`

Puedes instalar `openapi-ts` en tu código de frontend con:

<div class="termy">

```console
$ npm install @hey-api/openapi-ts --save-dev

---> 100%
```

</div>

#### Generar el Código del Cliente

Para generar el código del cliente puedes usar la aplicación de línea de comandos `openapi-ts` que ahora estaría instalada.

Como está instalada en el proyecto local, probablemente no podrías llamar a ese comando directamente, pero podrías ponerlo en tu archivo `package.json`.

Podría verse como esto:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
```

Después de tener ese script de NPM `generate-client` allí, puedes ejecutarlo con:

<div class="termy">

```console
$ npm run generate-client

frontend-app@1.0.0 generate-client /home/user/code/frontend-app
> openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios
```

</div>

Ese comando generará código en `./src/client` y usará `axios` (el paquete HTTP de frontend) internamente.

### Prueba el Código del Cliente

Ahora puedes importar y usar el código del cliente, podría verse así, nota que tienes autocompletado para los métodos:

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

## App de FastAPI con Tags

En muchos casos tu aplicación de FastAPI será más grande, y probablemente usarás tags para separar diferentes grupos de *path operations*.

Por ejemplo, podrías tener una sección para **items** y otra sección para **usuarios**, y podrían estar separadas por tags:

{* ../../docs_src/generate_clients/tutorial002_py39.py hl[21,26,34] *}

### Genera un Cliente TypeScript con Tags

Si generas un cliente para una aplicación de FastAPI usando tags, normalmente también separará el código del cliente basándose en los tags.

De esta manera podrás tener las cosas ordenadas y agrupadas correctamente para el código del cliente:

<img src="/img/tutorial/generate-clients/image06.png">

En este caso tienes:

* `ItemsService`
* `UsersService`

### Nombres de los Métodos del Cliente

Ahora mismo los nombres de los métodos generados como `createItemItemsPost` no se ven muy limpios:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...eso es porque el generador del cliente usa el **operation ID** interno de OpenAPI para cada *path operation*.

OpenAPI requiere que cada operation ID sea único a través de todas las *path operations*, por lo que FastAPI usa el **nombre de la función**, el **path**, y el **método/operación HTTP** para generar ese operation ID, porque de esa manera puede asegurarse de que los operation IDs sean únicos.

Pero te mostraré cómo mejorar eso a continuación. 🤓

## Operation IDs Personalizados y Mejores Nombres de Métodos

Puedes **modificar** la forma en que estos operation IDs son **generados** para hacerlos más simples y tener **nombres de métodos más simples** en los clientes.

En este caso tendrás que asegurarte de que cada operation ID sea **único** de alguna otra manera.

Por ejemplo, podrías asegurarte de que cada *path operation* tenga un tag, y luego generar el operation ID basado en el **tag** y el nombre de la *path operation* **name** (el nombre de la función).

### Función Personalizada para Generar ID Único

FastAPI usa un **ID único** para cada *path operation*, se usa para el **operation ID** y también para los nombres de cualquier modelo personalizado necesario, para requests o responses.

Puedes personalizar esa función. Toma un `APIRoute` y retorna un string.

Por ejemplo, aquí está usando el primer tag (probablemente tendrás solo un tag) y el nombre de la *path operation* (el nombre de la función).

Puedes entonces pasar esa función personalizada a **FastAPI** como el parámetro `generate_unique_id_function`:

{* ../../docs_src/generate_clients/tutorial003_py39.py hl[6:7,10] *}

### Generar un Cliente TypeScript con Operation IDs Personalizados

Ahora si generas el cliente de nuevo, verás que tiene los nombres de métodos mejorados:

<img src="/img/tutorial/generate-clients/image07.png">

Como ves, los nombres de métodos ahora tienen el tag y luego el nombre de la función, ahora no incluyen información del path de la URL y la operación HTTP.

### Preprocesa la Especificación OpenAPI para el Generador de Clientes

El código generado aún tiene algo de **información duplicada**.

Ya sabemos que este método está relacionado con los **items** porque esa palabra está en el `ItemsService` (tomado del tag), pero aún tenemos el nombre del tag prefijado en el nombre del método también. 😕

Probablemente aún querremos mantenerlo para OpenAPI en general, ya que eso asegurará que los operation IDs sean **únicos**.

Pero para el cliente generado podríamos **modificar** los operation IDs de OpenAPI justo antes de generar los clientes, solo para hacer esos nombres de métodos más bonitos y **limpios**.

Podríamos descargar el JSON de OpenAPI a un archivo `openapi.json` y luego podríamos **remover ese tag prefijado** con un script como este:

{* ../../docs_src/generate_clients/tutorial004.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

Con eso, los operation IDs serían renombrados de cosas como `items-get_items` a solo `get_items`, de esa manera el generador del cliente puede generar nombres de métodos más simples.

### Generar un Cliente TypeScript con el OpenAPI Preprocesado

Ahora como el resultado final está en un archivo `openapi.json`, modificarías el `package.json` para usar ese archivo local, por ejemplo:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input ./openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
```

Después de generar el nuevo cliente, ahora tendrías nombres de métodos **limpios**, con todo el **autocompletado**, **errores en línea**, etc:

<img src="/img/tutorial/generate-clients/image08.png">

## Beneficios

Cuando usas los clientes generados automáticamente obtendrás **autocompletado** para:

* Métodos.
* Payloads de peticiones en el cuerpo, parámetros de query, etc.
* Payloads de responses.

También tendrás **errores en línea** para todo.

Y cada vez que actualices el código del backend, y **regeneres** el frontend, tendrás las nuevas *path operations* disponibles como métodos, las antiguas eliminadas, y cualquier otro cambio se reflejará en el código generado. 🤓

Esto también significa que si algo cambió será **reflejado** automáticamente en el código del cliente. Y si haces **build** del cliente, te dará error si tienes algún **desajuste** en los datos utilizados.

Así que, **detectarás muchos errores** muy temprano en el ciclo de desarrollo en lugar de tener que esperar a que los errores se muestren a tus usuarios finales en producción para luego intentar depurar dónde está el problema. ✨
