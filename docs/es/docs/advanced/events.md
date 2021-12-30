# Eventos: startup - shutdown

Puedes definir controladores de eventos (funciones) que necesiten ser ejecutados antes de que inicie la aplicación, o cuando la aplicación se esté cerrando.

Estas funciones pueden ser declaradas mediante `async def` o de forma normal `def`.

!!! Warning
Solamente los controladores de eventos para la aplicación principal serán ejecutados, no se ejecutarán [Sub Aplicaciones - Montaje](./sub-applications.md){.internal-link target=\_blank}.

## evento <abbr title="inicío">`startup`</abbr>

Para añadir una función que debe ejecutarse antes que la aplicación inicie, debes declararla con el evento <abbr title="inicio">`"startup"`</abbr> :

```Python hl_lines="8"
{!../../../docs_src/events/tutorial001.py!}
```

En este caso, el evento <abbr title="inicio">`startup`</abbr> inicializará los elementos de la "base de datos" (como un `diccionario`) con algunos valores.

Puedes añadir más de una función que controle eventos.

Y tú aplicación no recibirá peticiones hasta que todos los controladores de eventos de tipo <abbr>`startup`</abbr> se hayan completado.

## evento `shutdown`

Para añadir una función que debe ejecutarse cuando la aplicación se está cerrando, debe declararse con el evento <abbr>`"shutdown"`</abbr>:

```Python hl_lines="6"
{!../../../docs_src/events/tutorial002.py!}
```

Aquí , el controlador de evento <abbr>`shutdown`</abbr> escribirá una línea de texto <abbr title="Cierre de aplicación">`"Application shutdown"`</abbr> a un archivo `log.txt`.

!!! info
En la función `open()`, el <abbr title="modo">`mode="a"`</abbr> significa <abbr title="agregar">"append"</abbr>, por lo tanto, la línea será añadida después de cualquier elemento que halla en el archivo, sin llegar a sobreescribir el contenido previo.

!!! tip
    Observa que en este caso estamos utilizando la función estándar `open()` de Python para interactuar con el archivo.

    Entonces, involucramos I/O <abbr title="entrada/salida">(input/output)</abbr>, que requiere "esperar" para que los elementos se escriban en el disco.

    Pero `open()` no utiliza `async` o `await`.

    Para ello, declaramos un controlador de evento usando `def` en vez de `async def`.

!!! info
Puedes consultar más acerca de controladores de eventos en <a href="https://www.starlette.io/events/" class="external-link" target="_blank">la documentación de Starlette acerca de eventos</a>.
