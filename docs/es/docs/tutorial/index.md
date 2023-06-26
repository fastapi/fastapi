# Tutorial - Guía de Usuario

Este tutorial te muestra cómo usar **FastAPI** con la mayoría de sus características paso a paso.

Cada sección se basa gradualmente en las anteriores, pero está estructurada en temas separados, así puedes ir directamente a cualquier tema en concreto para resolver tus necesidades específicas sobre la API.

Funciona también como una referencia futura, para que puedas volver y ver exactamente lo que necesitas.

## Ejecuta el código

Todos los bloques de código se pueden copiar y usar directamente (en realidad son archivos Python probados).

Para ejecutar cualquiera de los ejemplos, copia el código en un archivo llamado `main.py`, y ejecuta `uvicorn` de la siguiente manera en tu terminal:

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

Se **RECOMIENDA** que escribas o copies el código, lo edites y lo ejecutes localmente.

Usarlo en tu editor de código es lo que realmente te muestra los beneficios de FastAPI, al ver la poca cantidad de código que tienes que escribir, todas las verificaciones de tipo, autocompletado, etc.

---

## Instala FastAPI

El primer paso es instalar FastAPI.

Para el tutorial, es posible que quieras instalarlo con todas las dependencias y características opcionales:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...eso también incluye `uvicorn` que puedes usar como el servidor que ejecuta tu código.

!!! nota
    También puedes instalarlo parte por parte.

    Esto es lo que probablemente harías una vez que desees implementar tu aplicación en producción:

    ```
    pip install fastapi
    ```

    También debes instalar `uvicorn` para que funcione como tu servidor:

    ```
    pip install "uvicorn[standard]"
    ```

    Y lo mismo para cada una de las dependencias opcionales que quieras utilizar.

## Guía Avanzada de Usuario

También hay una **Guía Avanzada de Usuario** que puedes leer luego de este **Tutorial - Guía de Usuario**.

La **Guía Avanzada de Usuario**, se basa en este tutorial, utiliza los mismos conceptos y enseña algunas características adicionales.

Pero primero deberías leer el **Tutorial - Guía de Usuario** (lo que estas leyendo ahora mismo).

La guía esa diseñada para que puedas crear una aplicación completa con solo el **Tutorial - Guía de Usuario**, y luego extenderlo de diferentes maneras, según tus necesidades, utilizando algunas de las ideas adicionales de la **Guía Avanzada de Usuario**.
