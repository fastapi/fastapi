# Puntos de referencia

Los puntos de referencia  independientes, TechEmpower, colocan a las apliaciones **FastAPI** que se ejecutan bajo Uvicorn como <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank"> uno de los frameworks de python mas rápidos disponibles</a>, solo por debajo de Starlette y Uvicorn (utilizados internamente por FastAPI). (*)

Pero cuando verificas los puntos de referencia y las comparaciones, deberías tener en mente lo siguiente.

## Puntos de referencia y rapidez

Cuando verificas las referencias, es común ver varias herramientas de diferentes tipos comparadas como equivalentes.

Específicamente, al ver Uvicorn, Starlette y FastAPI comparados juntos (entre muchas otras herramientas).

Cuanto más simple sea la solución a un problema por parte de la herramienta, mejor rendimiento obtendrá. Y la mayoría de los puntos de referencia no prueban las funciones adicionales proporcionadas por la herramienta.

La jerarquia es algo como:

* **Uvicorn**: un servidor ASGI (Asynchronous Server Gateway Interface)
  * **Starlette**: (usa Uvicorn) un microframework web
    * **FastAPI**: (usa Starlette) un API microframework con varias funcionaldades adicionales para la creación de APIs, con validación de datos, etc.

* **Uvicorn**:
  * Tendrá el mejor rendimiento, ya que no tiene mucho código adicional aparte del servidor en sí.
  * No escribirías una aplicación en Uvicorn directamente. Eso significaría que tu código tendría que incluir más o menos, al menos, todo el código proporcionado por Starlette (o ** FastAPI **). Y si hiciera eso, su aplicación final tendría la misma sobrecarga que haber usado un framework y minimizando el código y los errores de su aplicación.
  * Si estas comparando Uvicorn, compáralo con Daphne, Hypercorn, uWSGI, etc. Servidores de aplicaciones.
* **Starlette**:
  * Tendrá el siguiente mejor desempeño, después de Uvicorn. De hecho, Starlette usa Uvicorn para ejecutarse. Por lo tanto, probablemente solo se volvería "más lento" que Uvicorn cuando tenga que ejecutar más código.
  * Pero este provee las herramientos para contruir aplicaciones web simples, con direccionamiento basadao en rutas, etc.
  * Si esta comparando Starlette, compare este con Sanic, Flask, Django, etc. frameworks web (o microframeworks).
* **FastAPI**:
  * De la misma manera que Starlette usa Uvicorn y no puede ser más rápido que él, **FastAPI** usa Starlette, entonces no puede ser más rápido que él.
  * FastAPI proporciona más funciones además de Starlette. Funciones que casi siempre se necesitan al crear APIs, como validación y serialización de datos. Y al usarlo, obtienes documentación automática gratis (la documentación automática ni siquiera agrega sobre carga a las aplicaciones en ejecución, esta se genera al inicio).
  * Si no usaste FastAPI y usaste Starlette directamente (u otra herramienta, como Sanic, Flask, Responder, etc.), tendrías que implementar toda la validación y serialización de datos tú mismo. Por lo tanto, tu aplicación final aún tendría la misma sobre carga que si se hubiera creado con FastAPI. Y en muchos casos, esta validación y serialización de datos es la mayor cantidad de código escrito en las aplicaciones.
  * Entonces, usando FastAPI estas ahorrando tiempo de desarrollo, errores, lineas de código y probablemente obtendrias el mismo desempeño (o mejor) que si no usaras este (ya que tendría que implementarlo todo en su código ).
  * Si está comparando FastAPI, compárelo con un framework de aplicación web (o un conjunto de herramientas) que proporciona validación de datos, serialización y documentación, como Flask-apispec, NestJS, Molten, etc. Frameworks con validación de datos automática, serialización y documentación, integrados.
