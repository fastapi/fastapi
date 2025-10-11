# Alternativas, Inspiración y Comparaciones

Lo que inspiró a **FastAPI**, cómo se compara con las alternativas y lo que aprendió de ellas.

## Introducción

**FastAPI** no existiría si no fuera por el trabajo previo de otros.

Se han creado muchas herramientas antes que han ayudado a inspirar su creación.

He estado evitando la creación de un nuevo framework durante varios años. Primero intenté resolver todas las funcionalidades cubiertas por **FastAPI** usando muchos frameworks diferentes, plug-ins y herramientas.

Pero en algún punto, no hubo otra opción que crear algo que proporcionara todas estas funcionalidades, tomando las mejores ideas de herramientas previas y combinándolas de la mejor manera posible, usando funcionalidades del lenguaje que ni siquiera estaban disponibles antes (anotaciones de tipos de Python 3.6+).

## Herramientas previas

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a>

Es el framework más popular de Python y es ampliamente confiable. Se utiliza para construir sistemas como Instagram.

Está relativamente acoplado con bases de datos relacionales (como MySQL o PostgreSQL), por lo que tener una base de datos NoSQL (como Couchbase, MongoDB, Cassandra, etc) como motor de almacenamiento principal no es muy fácil.

Fue creado para generar el HTML en el backend, no para crear APIs utilizadas por un frontend moderno (como React, Vue.js y Angular) o por otros sistemas (como dispositivos del <abbr title="Internet of Things">IoT</abbr>) comunicándose con él.

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a>

El framework Django REST fue creado para ser un kit de herramientas flexible para construir APIs Web utilizando Django, mejorando sus capacidades API.

Es utilizado por muchas empresas, incluidas Mozilla, Red Hat y Eventbrite.

Fue uno de los primeros ejemplos de **documentación automática de APIs**, y esto fue específicamente una de las primeras ideas que inspiraron "la búsqueda de" **FastAPI**.

/// note | Nota

Django REST Framework fue creado por Tom Christie. El mismo creador de Starlette y Uvicorn, en los cuales **FastAPI** está basado.

///

/// check | Inspiró a **FastAPI** a

Tener una interfaz de usuario web de documentación automática de APIs.

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a>

Flask es un "microframework", no incluye integraciones de bases de datos ni muchas de las cosas que vienen por defecto en Django.

Esta simplicidad y flexibilidad permiten hacer cosas como usar bases de datos NoSQL como el sistema de almacenamiento de datos principal.

Como es muy simple, es relativamente intuitivo de aprender, aunque la documentación se vuelve algo técnica en algunos puntos.

También se utiliza comúnmente para otras aplicaciones que no necesariamente necesitan una base de datos, gestión de usuarios, o cualquiera de las muchas funcionalidades que vienen preconstruidas en Django. Aunque muchas de estas funcionalidades se pueden añadir con plug-ins.

Esta separación de partes, y ser un "microframework" que podría extenderse para cubrir exactamente lo que se necesita, fue una funcionalidad clave que quise mantener.

Dada la simplicidad de Flask, parecía una buena opción para construir APIs. Lo siguiente a encontrar era un "Django REST Framework" para Flask.

/// check | Inspiró a **FastAPI** a

Ser un micro-framework. Haciendo fácil mezclar y combinar las herramientas y partes necesarias.

Tener un sistema de routing simple y fácil de usar.

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a>

**FastAPI** no es en realidad una alternativa a **Requests**. Su ámbito es muy diferente.

De hecho, sería común usar Requests *dentro* de una aplicación FastAPI.

Aun así, FastAPI se inspiró bastante en Requests.

**Requests** es un paquete para *interactuar* con APIs (como cliente), mientras que **FastAPI** es un paquete para *construir* APIs (como servidor).

Están, más o menos, en extremos opuestos, complementándose entre sí.

Requests tiene un diseño muy simple e intuitivo, es muy fácil de usar, con valores predeterminados sensatos. Pero al mismo tiempo, es muy poderoso y personalizable.

Por eso, como se dice en el sitio web oficial:

> Requests es uno de los paquetes Python más descargados de todos los tiempos

La forma en que lo usas es muy sencilla. Por ejemplo, para hacer un `GET` request, escribirías:

```Python
response = requests.get("http://example.com/some/url")
```

La operación de path equivalente en FastAPI podría verse como:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

Mira las similitudes entre `requests.get(...)` y `@app.get(...)`.

/// check | Inspiró a **FastAPI** a

* Tener un API simple e intuitivo.
* Usar nombres de métodos HTTP (operaciones) directamente, de una manera sencilla e intuitiva.
* Tener valores predeterminados sensatos, pero personalizaciones poderosas.

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a>

La principal funcionalidad que quería de Django REST Framework era la documentación automática de la API.

Luego descubrí que había un estándar para documentar APIs, usando JSON (o YAML, una extensión de JSON) llamado Swagger.

Y ya existía una interfaz de usuario web para las APIs Swagger. Por lo tanto, ser capaz de generar documentación Swagger para una API permitiría usar esta interfaz de usuario web automáticamente.

En algún punto, Swagger fue entregado a la Linux Foundation, para ser renombrado OpenAPI.

Es por eso que cuando se habla de la versión 2.0 es común decir "Swagger", y para la versión 3+ "OpenAPI".

/// check | Inspiró a **FastAPI** a

Adoptar y usar un estándar abierto para especificaciones de API, en lugar de usar un esquema personalizado.

Y a integrar herramientas de interfaz de usuario basadas en estándares:

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

Estas dos fueron elegidas por ser bastante populares y estables, pero haciendo una búsqueda rápida, podrías encontrar docenas de interfaces de usuario alternativas para OpenAPI (que puedes usar con **FastAPI**).

///

### Frameworks REST para Flask

Existen varios frameworks REST para Flask, pero después de invertir tiempo y trabajo investigándolos, encontré que muchos son descontinuados o abandonados, con varios problemas existentes que los hacían inadecuados.

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a>

Una de las principales funcionalidades necesitadas por los sistemas API es la "<abbr title="también llamada marshalling, conversión">serialización</abbr>" de datos, que consiste en tomar datos del código (Python) y convertirlos en algo que pueda ser enviado a través de la red. Por ejemplo, convertir un objeto que contiene datos de una base de datos en un objeto JSON. Convertir objetos `datetime` en strings, etc.

Otra gran funcionalidad necesaria por las APIs es la validación de datos, asegurarse de que los datos sean válidos, dados ciertos parámetros. Por ejemplo, que algún campo sea un `int`, y no algún string aleatorio. Esto es especialmente útil para los datos entrantes.

Sin un sistema de validación de datos, tendrías que hacer todas las comprobaciones a mano, en código.

Estas funcionalidades son para lo que fue creado Marshmallow. Es un gran paquete, y lo he usado mucho antes.

Pero fue creado antes de que existieran las anotaciones de tipos en Python. Así que, para definir cada <abbr title="la definición de cómo deberían formarse los datos">esquema</abbr> necesitas usar utilidades y clases específicas proporcionadas por Marshmallow.

/// check | Inspiró a **FastAPI** a

Usar código para definir "esquemas" que proporcionen tipos de datos y validación automáticamente.

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a>

Otra gran funcionalidad requerida por las APIs es el <abbr title="lectura y conversión a datos de Python">parse</abbr> de datos de las requests entrantes.

Webargs es una herramienta que fue creada para proporcionar esa funcionalidad sobre varios frameworks, incluido Flask.

Usa Marshmallow por debajo para hacer la validación de datos. Y fue creada por los mismos desarrolladores.

Es una gran herramienta y la he usado mucho también, antes de tener **FastAPI**.

/// info | Información

Webargs fue creada por los mismos desarrolladores de Marshmallow.

///

/// check | Inspiró a **FastAPI** a

Tener validación automática de datos entrantes en una request.

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a>

Marshmallow y Webargs proporcionan validación, parse y serialización como plug-ins.

Pero la documentación todavía falta. Entonces APISpec fue creado.

Es un plug-in para muchos frameworks (y hay un plug-in para Starlette también).

La manera en que funciona es que escribes la definición del esquema usando el formato YAML dentro del docstring de cada función que maneja una ruta.

Y genera esquemas OpenAPI.

Así es como funciona en Flask, Starlette, Responder, etc.

Pero luego, tenemos otra vez el problema de tener una micro-sintaxis, dentro de un string de Python (un gran YAML).

El editor no puede ayudar mucho con eso. Y si modificamos parámetros o esquemas de Marshmallow y olvidamos también modificar ese docstring YAML, el esquema generado estaría obsoleto.

/// info | Información

APISpec fue creado por los mismos desarrolladores de Marshmallow.

///

/// check | Inspiró a **FastAPI** a

Soportar el estándar abierto para APIs, OpenAPI.

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a>

Es un plug-in de Flask, que conecta juntos Webargs, Marshmallow y APISpec.

Usa la información de Webargs y Marshmallow para generar automáticamente esquemas OpenAPI, usando APISpec.

Es una gran herramienta, muy subestimada. Debería ser mucho más popular que muchos plug-ins de Flask por ahí. Puede que se deba a que su documentación es demasiado concisa y abstracta.

Esto resolvió tener que escribir YAML (otra sintaxis) dentro de docstrings de Python.

Esta combinación de Flask, Flask-apispec con Marshmallow y Webargs fue mi stack de backend favorito hasta construir **FastAPI**.

Usarlo llevó a la creación de varios generadores de full-stack para Flask. Estos son los principales stacks que yo (y varios equipos externos) hemos estado usando hasta ahora:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

Y estos mismos generadores de full-stack fueron la base de los [Generadores de Proyectos **FastAPI**](project-generation.md){.internal-link target=_blank}.

/// info | Información

Flask-apispec fue creado por los mismos desarrolladores de Marshmallow.

///

/// check | Inspiró a **FastAPI** a

Generar el esquema OpenAPI automáticamente, desde el mismo código que define la serialización y validación.

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (y <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>)

Esto ni siquiera es Python, NestJS es un framework de JavaScript (TypeScript) NodeJS inspirado por Angular.

Logra algo algo similar a lo que se puede hacer con Flask-apispec.

Tiene un sistema de inyección de dependencias integrado, inspirado por Angular 2. Requiere pre-registrar los "inyectables" (como todos los otros sistemas de inyección de dependencias que conozco), por lo que añade a la verbosidad y repetición de código.

Como los parámetros se describen con tipos de TypeScript (similar a las anotaciones de tipos en Python), el soporte editorial es bastante bueno.

Pero como los datos de TypeScript no se preservan después de la compilación a JavaScript, no puede depender de los tipos para definir validación, serialización y documentación al mismo tiempo. Debido a esto y algunas decisiones de diseño, para obtener validación, serialización y generación automática del esquema, es necesario agregar decoradores en muchos lugares. Por lo tanto, se vuelve bastante verboso.

No puede manejar muy bien modelos anidados. Entonces, si el cuerpo JSON en la request es un objeto JSON que tiene campos internos que a su vez son objetos JSON anidados, no puede ser documentado y validado apropiadamente.

/// check | Inspiró a **FastAPI** a

Usar tipos de Python para tener un gran soporte del editor.

Tener un poderoso sistema de inyección de dependencias. Encontrar una forma de minimizar la repetición de código.

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a>

Fue uno de los primeros frameworks de Python extremadamente rápidos basados en `asyncio`. Fue hecho para ser muy similar a Flask.

/// note | Detalles Técnicos

Usó <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> en lugar del loop `asyncio` por defecto de Python. Eso fue lo que lo hizo tan rápido.

Claramente inspiró a Uvicorn y Starlette, que actualmente son más rápidos que Sanic en benchmarks abiertos.

///

/// check | Inspiró a **FastAPI** a

Encontrar una manera de tener un rendimiento impresionante.

Por eso **FastAPI** se basa en Starlette, ya que es el framework más rápido disponible (probado por benchmarks de terceros).

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a>

Falcon es otro framework de Python de alto rendimiento, está diseñado para ser minimalista y funcionar como la base de otros frameworks como Hug.

Está diseñado para tener funciones que reciben dos parámetros, un "request" y un "response". Luego "lees" partes del request y "escribes" partes en el response. Debido a este diseño, no es posible declarar parámetros de request y cuerpos con las anotaciones de tipos estándar de Python como parámetros de función.

Por lo tanto, la validación de datos, la serialización y la documentación, tienen que hacerse en código, no automáticamente. O tienen que implementarse como un framework sobre Falcon, como Hug. Esta misma distinción ocurre en otros frameworks que se inspiran en el diseño de Falcon, de tener un objeto request y un objeto response como parámetros.

/// check | Inspiró a **FastAPI** a

Buscar maneras de obtener un gran rendimiento.

Junto con Hug (ya que Hug se basa en Falcon), inspiraron a **FastAPI** a declarar un parámetro `response` en las funciones.

Aunque en FastAPI es opcional, y se utiliza principalmente para configurar headers, cookies y códigos de estado alternativos.

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a>

Descubrí Molten en las primeras etapas de construcción de **FastAPI**. Y tiene ideas bastante similares:

* Basado en las anotaciones de tipos de Python.
* Validación y documentación a partir de estos tipos.
* Sistema de Inyección de Dependencias.

No utiliza un paquete de validación de datos, serialización y documentación de terceros como Pydantic, tiene el suyo propio. Por lo tanto, estas definiciones de tipos de datos no serían reutilizables tan fácilmente.

Requiere configuraciones un poquito más verbosas. Y dado que se basa en WSGI (en lugar de ASGI), no está diseñado para aprovechar el alto rendimiento proporcionado por herramientas como Uvicorn, Starlette y Sanic.

El sistema de inyección de dependencias requiere pre-registrar las dependencias y las dependencias se resuelven en base a los tipos declarados. Por lo tanto, no es posible declarar más de un "componente" que proporcione cierto tipo.

Las rutas se declaran en un solo lugar, usando funciones declaradas en otros lugares (en lugar de usar decoradores que pueden colocarse justo encima de la función que maneja el endpoint). Esto se acerca más a cómo lo hace Django que a cómo lo hace Flask (y Starlette). Separa en el código cosas que están relativamente acopladas.

/// check | Inspiró a **FastAPI** a

Definir validaciones extra para tipos de datos usando el valor "default" de los atributos del modelo. Esto mejora el soporte del editor y no estaba disponible en Pydantic antes.

Esto en realidad inspiró la actualización de partes de Pydantic, para soportar el mismo estilo de declaración de validación (toda esta funcionalidad ya está disponible en Pydantic).

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a>

Hug fue uno de los primeros frameworks en implementar la declaración de tipos de parámetros API usando las anotaciones de tipos de Python. Esta fue una gran idea que inspiró a otras herramientas a hacer lo mismo.

Usaba tipos personalizados en sus declaraciones en lugar de tipos estándar de Python, pero aún así fue un gran avance.

También fue uno de los primeros frameworks en generar un esquema personalizado declarando toda la API en JSON.

No se basaba en un estándar como OpenAPI y JSON Schema. Por lo que no sería sencillo integrarlo con otras herramientas, como Swagger UI. Pero, nuevamente, fue una idea muy innovadora.

Tiene una funcionalidad interesante e inusual: usando el mismo framework, es posible crear APIs y también CLIs.

Dado que se basa en el estándar previo para frameworks web Python sincrónicos (WSGI), no puede manejar Websockets y otras cosas, aunque aún así tiene un alto rendimiento también.

/// info | Información

Hug fue creado por Timothy Crosley, el mismo creador de <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>, una gran herramienta para ordenar automáticamente imports en archivos Python.

///

/// check | Ideas que inspiraron a **FastAPI**

Hug inspiró partes de APIStar, y fue una de las herramientas que encontré más prometedoras, junto a APIStar.

Hug ayudó a inspirar a **FastAPI** a usar anotaciones de tipos de Python para declarar parámetros, y a generar un esquema definiendo la API automáticamente.

Hug inspiró a **FastAPI** a declarar un parámetro `response` en funciones para configurar headers y cookies.

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5)

Justo antes de decidir construir **FastAPI** encontré **APIStar** server. Tenía casi todo lo que estaba buscando y tenía un gran diseño.

Era una de las primeras implementaciones de un framework utilizando las anotaciones de tipos de Python para declarar parámetros y requests que jamás vi (antes de NestJS y Molten). Lo encontré más o menos al mismo tiempo que Hug. Pero APIStar usaba el estándar OpenAPI.

Tenía validación de datos automática, serialización de datos y generación del esquema OpenAPI basada en las mismas anotaciones de tipos en varios lugares.

Las definiciones de esquema de cuerpo no usaban las mismas anotaciones de tipos de Python como Pydantic, era un poco más similar a Marshmallow, por lo que el soporte del editor no sería tan bueno, pero aún así, APIStar era la mejor opción disponible.

Tenía los mejores benchmarks de rendimiento en ese momento (solo superado por Starlette).

Al principio, no tenía una interfaz de usuario web de documentación de API automática, pero sabía que podía agregar Swagger UI a él.

Tenía un sistema de inyección de dependencias. Requería pre-registrar componentes, como otras herramientas discutidas anteriormente. Pero aún así, era una gran funcionalidad.

Nunca pude usarlo en un proyecto completo, ya que no tenía integración de seguridad, por lo que no podía reemplazar todas las funcionalidades que tenía con los generadores de full-stack basados en Flask-apispec. Tenía en mi lista de tareas pendientes de proyectos crear un pull request agregando esa funcionalidad.

Pero luego, el enfoque del proyecto cambió.

Ya no era un framework web API, ya que el creador necesitaba enfocarse en Starlette.

Ahora APIStar es un conjunto de herramientas para validar especificaciones OpenAPI, no un framework web.

/// info | Información

APIStar fue creado por Tom Christie. El mismo que creó:

* Django REST Framework
* Starlette (en la cual **FastAPI** está basado)
* Uvicorn (usado por Starlette y **FastAPI**)

///

/// check | Inspiró a **FastAPI** a

Existir.

La idea de declarar múltiples cosas (validación de datos, serialización y documentación) con los mismos tipos de Python, que al mismo tiempo proporcionaban un gran soporte del editor, era algo que consideré una idea brillante.

Y después de buscar durante mucho tiempo un framework similar y probar muchas alternativas diferentes, APIStar fue la mejor opción disponible.

Luego APIStar dejó de existir como servidor y Starlette fue creado, y fue una nueva y mejor base para tal sistema. Esa fue la inspiración final para construir **FastAPI**.

Considero a **FastAPI** un "sucesor espiritual" de APIStar, mientras mejora y aumenta las funcionalidades, el sistema de tipos y otras partes, basándose en los aprendizajes de todas estas herramientas previas.

///

## Usado por **FastAPI**

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>

Pydantic es un paquete para definir validación de datos, serialización y documentación (usando JSON Schema) basándose en las anotaciones de tipos de Python.

Eso lo hace extremadamente intuitivo.

Es comparable a Marshmallow. Aunque es más rápido que Marshmallow en benchmarks. Y como está basado en las mismas anotaciones de tipos de Python, el soporte del editor es estupendo.

/// check | **FastAPI** lo usa para

Manejar toda la validación de datos, serialización de datos y documentación automática de modelos (basada en JSON Schema).

**FastAPI** luego toma esos datos JSON Schema y los coloca en OpenAPI, aparte de todas las otras cosas que hace.

///

### <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>

Starlette es un framework/toolkit <abbr title="El nuevo estándar para construir aplicaciones web asíncronas en Python">ASGI</abbr> liviano, ideal para construir servicios asyncio de alto rendimiento.

Es muy simple e intuitivo. Está diseñado para ser fácilmente extensible y tener componentes modulares.

Tiene:

* Un rendimiento seriamente impresionante.
* Soporte para WebSocket.
* Tareas en segundo plano dentro del proceso.
* Eventos de inicio y apagado.
* Cliente de pruebas basado en HTTPX.
* CORS, GZip, Archivos estáticos, Responses en streaming.
* Soporte para sesiones y cookies.
* Cobertura de tests del 100%.
* Base de código 100% tipada.
* Pocas dependencias obligatorias.

Starlette es actualmente el framework de Python más rápido probado. Solo superado por Uvicorn, que no es un framework, sino un servidor.

Starlette proporciona toda la funcionalidad básica de un microframework web.

Pero no proporciona validación de datos automática, serialización o documentación.

Esa es una de las principales cosas que **FastAPI** agrega, todo basado en las anotaciones de tipos de Python (usando Pydantic). Eso, además del sistema de inyección de dependencias, utilidades de seguridad, generación de esquemas OpenAPI, etc.

/// note | Detalles Técnicos

ASGI es un nuevo "estándar" que está siendo desarrollado por miembros del equipo central de Django. Todavía no es un "estándar de Python" (un PEP), aunque están en proceso de hacerlo.

No obstante, ya está siendo usado como un "estándar" por varias herramientas. Esto mejora enormemente la interoperabilidad, ya que podrías cambiar Uvicorn por cualquier otro servidor ASGI (como Daphne o Hypercorn), o podrías añadir herramientas compatibles con ASGI, como `python-socketio`.

///

/// check | **FastAPI** lo usa para

Manejar todas las partes web centrales. Añadiendo funcionalidades encima.

La clase `FastAPI` en sí misma hereda directamente de la clase `Starlette`.

Por lo tanto, cualquier cosa que puedas hacer con Starlette, puedes hacerlo directamente con **FastAPI**, ya que es básicamente Starlette potenciado.

///

### <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>

Uvicorn es un servidor ASGI extremadamente rápido, construido sobre uvloop y httptools.

No es un framework web, sino un servidor. Por ejemplo, no proporciona herramientas para el enrutamiento por paths. Eso es algo que un framework como Starlette (o **FastAPI**) proporcionaría encima.

Es el servidor recomendado para Starlette y **FastAPI**.

/// check | **FastAPI** lo recomienda como

El servidor web principal para ejecutar aplicaciones **FastAPI**.

También puedes usar la opción de línea de comandos `--workers` para tener un servidor multiproceso asíncrono.

Revisa más detalles en la sección [Despliegue](deployment/index.md){.internal-link target=_blank}.

///

## Benchmarks y velocidad

Para entender, comparar, y ver la diferencia entre Uvicorn, Starlette y FastAPI, revisa la sección sobre [Benchmarks](benchmarks.md){.internal-link target=_blank}.
