# Depuración

Puedes conectar el depurador en tu editor, por ejemplo con Visual Studio Code o PyCharm.

## Llama a `uvicorn`

En tu aplicación de FastAPI, importa y ejecuta `uvicorn` directamente:

{* ../../docs_src/debugging/tutorial001.py hl[1,15] *}

### Acerca de `__name__ == "__main__"`

El objetivo principal de `__name__ == "__main__"` es tener algo de código que se ejecute cuando tu archivo es llamado con:

<div class="termy">

```console
$ python myapp.py
```

</div>

pero no es llamado cuando otro archivo lo importa, como en:

```Python
from myapp import app
```

#### Más detalles

Supongamos que tu archivo se llama `myapp.py`.

Si lo ejecutas con:

<div class="termy">

```console
$ python myapp.py
```

</div>

entonces la variable interna `__name__` en tu archivo, creada automáticamente por Python, tendrá como valor el string `"__main__"`.

Así que, la sección:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

se ejecutará.

---

Esto no ocurrirá si importas ese módulo (archivo).

Entonces, si tienes otro archivo `importer.py` con:

```Python
from myapp import app

# Algún código adicional
```

en ese caso, la variable creada automáticamente dentro de `myapp.py` no tendrá la variable `__name__` con un valor de `"__main__"`.

Así que, la línea:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

no se ejecutará.

/// info | Información

Para más información, revisa <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">la documentación oficial de Python</a>.

///

## Ejecuta tu código con tu depurador

Dado que estás ejecutando el servidor Uvicorn directamente desde tu código, puedes llamar a tu programa de Python (tu aplicación FastAPI) directamente desde el depurador.

---

Por ejemplo, en Visual Studio Code, puedes:

* Ir al panel de "Debug".
* "Add configuration...".
* Seleccionar "Python".
* Ejecutar el depurador con la opción "`Python: Current File (Integrated Terminal)`".

Luego, iniciará el servidor con tu código **FastAPI**, deteniéndose en tus puntos de interrupción, etc.

Así es como podría verse:

<img src="/img/tutorial/debugging/image01.png">

---

Si usas PyCharm, puedes:

* Abrir el menú "Run".
* Seleccionar la opción "Debug...".
* Luego aparece un menú contextual.
* Selecciona el archivo para depurar (en este caso, `main.py`).

Luego, iniciará el servidor con tu código **FastAPI**, deteniéndose en tus puntos de interrupción, etc.

Así es como podría verse:

<img src="/img/tutorial/debugging/image02.png">
