# Tutorial - Guía de usuario - Introducción

Este tutorial te muestra como usar **FastAPI** con la mayoría de sus características paso a paso.

Cada sección se basa gradualmente en las anteriores, pero está estructurada por temas separados, así puedes ir directamente a cualquier tema en específico para resolver sus necesidades específicas sobre el API.

También está diseñado para funcionar como una referencia futura.

Para que puedas volver y ver exactamente lo que necesitas.

## Ejecuta el código

Todos los bloques de código se pueden copiar y usar directamente (en realidad son archivos Python probados).

Para ejecutar cualquiera de los ejemplos, copie el código en un archivo llamado `main.py`, y ejecute `uvicorn` de la siguiente manera en su terminal:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

Se **RECOMIENDA** que escriba o copie el código, lo edite y lo ejecute localmente.

Usarlo en tu editor de código es lo que realmente te muestra los beneficios de FastAPI, al ver la poca cantidad de código que tienes que escribir, todas las verificaciones de tipo, autocompletado, etc.

---

## Instalando FastAPI

El primer paso es instalar FastAPI.

Para el tutorial, es posible que desee instalarlo con todas las dependencias y características opcionales:

<div class="termy">

```console
$ pip install fastapi[all]

---> 100%
```

</div>

...eso también incluye `uvicorn` que se usa como el servidor que ejecuta su código.

!!! nota
    También puede instalarlo parte por parte.

    Esto es lo que probablemente haría una vez que desee implementar su aplicación en producción:

    ```
    pip install fastapi
    ```

    También instale `uvicorn` para que funcione como servidor:

    ```
    pip install uvicorn
    ```

    Y lo mismo para cada una de las dependencias opcionales que desea utilizar.

## Guía avanzada del usuario 

También hay una **Guía avanzada del usuario** que puede leer luego de este  **Tutorial - Guía de usuario**.

La **Guía avanzada del usuario**, se basa en este tutorial, utiliza los mismos conceptos y enseña algunas características adicionales.

Pero primero debe leer el **Tutorial - Guía de usuario** (lo que está leyendo en este momento).

Está diseñado para que pueda crear una aplicación completa con solo el **Tutorial - Guía de usuario**, y luego extenderlo de diferentes maneras, según sus necesidades, utilizando algunas de las ideas adicionales de la **Guía avanzada del usuario**.
