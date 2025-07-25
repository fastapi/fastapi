# Benchmarks

Los benchmarks independientes de TechEmpower muestran aplicaciones de **FastAPI** ejecutándose bajo Uvicorn como <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">uno de los frameworks de Python más rápidos disponibles</a>, solo por debajo de Starlette y Uvicorn en sí mismos (utilizados internamente por FastAPI).

Pero al revisar benchmarks y comparaciones, debes tener en cuenta lo siguiente.

## Benchmarks y velocidad

Cuando ves los benchmarks, es común ver varias herramientas de diferentes tipos comparadas como equivalentes.

Específicamente, ver Uvicorn, Starlette y FastAPI comparados juntos (entre muchas otras herramientas).

Cuanto más simple sea el problema resuelto por la herramienta, mejor rendimiento tendrá. Y la mayoría de los benchmarks no prueban las funcionalidades adicionales proporcionadas por la herramienta.

La jerarquía es como:

* **Uvicorn**: un servidor ASGI
    * **Starlette**: (usa Uvicorn) un microframework web
        * **FastAPI**: (usa Starlette) un microframework para APIs con varias funcionalidades adicionales para construir APIs, con validación de datos, etc.

* **Uvicorn**:
    * Tendrá el mejor rendimiento, ya que no tiene mucho código extra aparte del propio servidor.
    * No escribirías una aplicación directamente en Uvicorn. Eso significaría que tu código tendría que incluir, más o menos, al menos, todo el código proporcionado por Starlette (o **FastAPI**). Y si hicieras eso, tu aplicación final tendría la misma carga que si hubieras usado un framework, minimizando el código de tu aplicación y los bugs.
    * Si estás comparando Uvicorn, compáralo con Daphne, Hypercorn, uWSGI, etc. Servidores de aplicaciones.
* **Starlette**:
    * Tendrá el siguiente mejor rendimiento, después de Uvicorn. De hecho, Starlette usa Uvicorn para ejecutarse. Así que probablemente solo pueda ser "más lento" que Uvicorn por tener que ejecutar más código.
    * Pero te proporciona las herramientas para construir aplicaciones web sencillas, con enrutamiento basado en paths, etc.
    * Si estás comparando Starlette, compáralo con Sanic, Flask, Django, etc. Frameworks web (o microframeworks).
* **FastAPI**:
    * De la misma forma en que Starlette usa Uvicorn y no puede ser más rápido que él, **FastAPI** usa Starlette, por lo que no puede ser más rápido que él.
    * FastAPI ofrece más funcionalidades además de las de Starlette. Funcionalidades que casi siempre necesitas al construir APIs, como la validación y serialización de datos. Y al utilizarlo, obtienes documentación automática gratis (la documentación automática ni siquiera añade carga a las aplicaciones en ejecución, se genera al inicio).
    * Si no usabas FastAPI y utilizabas Starlette directamente (u otra herramienta, como Sanic, Flask, Responder, etc.) tendrías que implementar toda la validación y serialización de datos por ti mismo. Entonces, tu aplicación final aún tendría la misma carga que si hubiera sido construida usando FastAPI. Y en muchos casos, esta validación y serialización de datos es la mayor cantidad de código escrito en las aplicaciones.
    * Entonces, al usar FastAPI estás ahorrando tiempo de desarrollo, bugs, líneas de código, y probablemente obtendrías el mismo rendimiento (o mejor) que si no lo usaras (ya que tendrías que implementarlo todo en tu código).
    * Si estás comparando FastAPI, compáralo con un framework de aplicación web (o conjunto de herramientas) que proporcione validación de datos, serialización y documentación, como Flask-apispec, NestJS, Molten, etc. Frameworks con validación de datos, serialización y documentación automáticas integradas.
