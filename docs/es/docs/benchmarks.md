# <abbr title="evaluación comparativa">Benchmarks</abbr>

<abbr title="evaluación comparativa">Benchmarks</abbr> independientes de TechEmpower muestran aplicaciones **FastAPI** corriendo bajo Uvicorn como <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">uno de los frameworks de Python más rápidos disponibles</a>, solo superado por Starlette y Uvicorn (utilizados internamente por FastAPI). (*)

Pero al verificar los <abbr title="evaluación comparativa">benchmarks</abbr> y las comparaciones, debe tener en cuenta lo siguiente.

## <abbr title="evaluación comparativa">Benchmarks</abbr> y velocidad

Cuando revisas los <abbr title="evaluación comparativa">benchmarks</abbr>, es común ver varias herramientas de diferentes tipos comparadas como equivalentes.

Específicamente, ver comparaciones entre Uvicorn, Starlette y FastAPI (entre muchas otras herramientas).

Cuanto más simple sea el problema resuelto por la herramienta, mejor rendimiento obtendrá. Y la mayoría de los <abbr title="evaluación comparativa">benchmarks</abbr> no prueban las funciones adicionales ofrecidas por la herramienta.

La jerarquía sería:

* **Uvicorn**: un servidor <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>
    * **Starlette**: (usa Uvicorn) un microframework web
        * **FastAPI**: (usa Starlette) un microframework de API con varias características adicionales para construir API, con validación de datos, etc.

* **Uvicorn**:
    * Tendrá el mejor rendimiento, ya que no tiene mucho código adicional aparte del propio servidor.
    * No escribirías una aplicación en Uvicorn directamente. Eso significaría que tu código tendría que incluir más o menos, al menos, todo el código proporcionado por Starlette (o **FastAPI**). Y si lo hicieras, tu aplicación final tendría la misma sobrecarga que si hubiera usado un framework y minimizado el código y los errores de su aplicación.
    * Si estás comparando Uvicorn, compáralo con Daphne, Hypercorn, uWSGI, etc. Servidores de aplicaciones.
* **Starlette**:
    * Tendrá el siguiente mejor rendimiento, luego de Uvicorn. De hecho, Starlette usa Uvicorn para correr. Por lo tanto, probablemente solo pueda volverse "más lento" que Uvicorn al tener que ejecutar más código.
    * Pero proporciona las herramientas para construir aplicaciones web simples, con enrutamiento basado en rutas, etc
    * Si estás comparando Starlette, compáralo con Sanic, Flask, Django, etc. Frameworks web (o microframeworks).
* **FastAPI**:
    * De la misma manera que Starlette usa Uvicorn y no puede ser más rápido que él, **FastAPI** usa Starlette, por lo que no puede ser más rápido que él.
    * FastAPI ofrece más funciones además de Starlette. Funciones que casi siempre se necesitan al crear APIs, como validación y serialización de datos. Y al usarlo, obtiene documentación automática de forma gratuita (la documentación automática ni siquiera agrega gastos generales a las aplicaciones en ejecución, se genera al inicio).
    * Si no utilizaste FastAPI y utilizaste Starlette directamente (u otra herramienta, como Sanic, Flask, Responder, etc.), tendrías que implementar toda la validación y serialización de datos. Por lo tanto, tu aplicación final aún tendría la misma sobrecarga que si se hubiera creado con FastAPI. Y en muchos casos, esta validación y serialización de datos es la mayor cantidad de código escrito en las aplicaciones.
    * Por lo tanto, al usar FastAPI estás ahorrando tiempo de desarrollo, errores, líneas de código y probablemente obtendrás el mismo rendimiento (o mejor) que obtendrías si no lo usaras (ya que tendrías que implementarlo todo en tu código).
    * Si estás comparando FastAPI, compáralo con un framework de aplicación web (o un conjunto de herramientas) que proporcione validación, serialización y documentación de datos, como Flask-apispec, NestJS, Molten, etc. Framework con documentación, serialización y validación de datos automática integrada.
