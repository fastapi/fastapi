# Benchmarks

Los benchmarks independientes de TechEmpower muestran aplicaciones de **FastAPI** que se ejecutan en Uvicorn como <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l= zijzen-7" class="external-link" target="_blank">uno de los frameworks de Python más rápidos disponibles</a>, solo por debajo de Starlette y Uvicorn (utilizados internamente por FastAPI). (*)

Pero al comprobar benchmarks y comparaciones debes tener en cuenta lo siguiente.

## Benchmarks y velocidad

Cuando revisas los benchmarks, es común ver varias herramientas de diferentes tipos comparadas como equivalentes.

Específicamente, para ver Uvicorn, Starlette y FastAPI comparadas entre sí (entre muchas otras herramientas).

Cuanto más sencillo sea el problema resuelto por la herramienta, mejor rendimiento obtendrá. Y la mayoría de los benchmarks no prueban las funciones adicionales proporcionadas por la herramienta.

La jerarquía sería:

* **Uvicorn**: como servidor ASGI
    * **Starlette**: (usa Uvicorn) un microframework web
         * **FastAPI**: (usa Starlette) un microframework API con varias características adicionales para construir APIs, con validación de datos, etc.
* **Uvicorn**:
    * Tendrá el mejor rendimiento, ya que no tiene mucho código extra aparte del propio servidor.
    * No escribirías una aplicación directamente en Uvicorn. Eso significaría que tu código tendría que incluir más o menos, al menos, todo el código proporcionado por Starlette (o **FastAPI**). Y si hicieras eso, tu aplicación final tendría la misma sobrecarga que si hubieras usado un framework y minimizado el código de tu aplicación y los errores.
    * Si estás comparando Uvicorn, compáralo con los servidores de aplicaciones Daphne, Hypercorn, uWSGI, etc.
* **Starlette**:
    * Tendrá el siguiente mejor desempeño, después de Uvicorn. De hecho, Starlette usa Uvicorn para correr. Por lo tanto, probablemente sólo pueda volverse "más lento" que Uvicorn al tener que ejecutar más código.
    * Pero te proporciona las herramientas para crear aplicaciones web simples, con <abbr title="también conocido en español como: enrutamiento">routing</abbr> basado en <abbr title="tambien conocido en español como: rutas">paths</abbr>, etc.
    * Si estás comparando Starlette, compáralo con Sanic, Flask, Django, etc. Frameworks web (o microframeworks).
* **FastAPI**:
    * De la misma manera que Starlette usa Uvicorn y no puede ser más rápido que él, **FastAPI** usa Starlette, por lo que no puede ser más rápido que él.
    * * FastAPI ofrece más características además de las de Starlette. Funciones que casi siempre necesitas al crear una API, como validación y serialización de datos. Y al usarlo, obtienes documentación automática de forma gratuita (la documentación automática ni siquiera agrega gastos generales a las aplicaciones en ejecución, se genera al iniciar).
    * Si no usaras FastAPI y usaras Starlette directamente (u otra herramienta, como Sanic, Flask, Responder, etc.), tendrías que implementar toda la validación y serialización de datos tu mismo. Por lo tanto, tu aplicación final seguirá teniendo la misma sobrecarga que si se hubiera creado con FastAPI. Y en muchos casos, esta validación y serialización de datos constituye la mayor cantidad de código escrito en las aplicaciones.
    * Entonces, al usar FastAPI estás ahorrando tiempo de desarrollo, errores, líneas de código y probablemente obtendrías el mismo rendimiento (o mejor) que obtendrías si no lo usaras (ya que tendrías que implementarlo todo en tu código).
    * Si estás comparando FastAPI, compáralo con un framework de aplicaciones web (o conjunto de herramientas) que proporciona validación, serialización y documentación de datos, como Flask-apispec, NestJS, Molten, etc. Frameworks con validación, serialización y documentación automáticas integradas.
