# Archivos Estáticos

Puedes servir archivos estáticos automáticamente desde un directorio utilizando `StaticFiles`.

## Usa `StaticFiles`

* Importa `StaticFiles`.
* "Monta" una instance de `StaticFiles()` en un path específico.

{* ../../docs_src/static_files/tutorial001.py hl[2,6] *}

/// note | Detalles Técnicos

También podrías usar `from starlette.staticfiles import StaticFiles`.

**FastAPI** proporciona el mismo `starlette.staticfiles` como `fastapi.staticfiles` solo como una conveniencia para ti, el desarrollador. Pero en realidad viene directamente de Starlette.

///

### Qué es "Montar"

"Montar" significa agregar una aplicación completa "independiente" en un path específico, que luego se encargará de manejar todos los sub-paths.

Esto es diferente a usar un `APIRouter`, ya que una aplicación montada es completamente independiente. El OpenAPI y la documentación de tu aplicación principal no incluirán nada de la aplicación montada, etc.

Puedes leer más sobre esto en la [Guía de Usuario Avanzada](../advanced/index.md){.internal-link target=_blank}.

## Detalles

El primer `"/static"` se refiere al sub-path en el que esta "sub-aplicación" será "montada". Por lo tanto, cualquier path que comience con `"/static"` será manejado por ella.

El `directory="static"` se refiere al nombre del directorio que contiene tus archivos estáticos.

El `name="static"` le da un nombre que puede ser utilizado internamente por **FastAPI**.

Todos estos parámetros pueden ser diferentes a "`static`", ajústalos según las necesidades y detalles específicos de tu propia aplicación.

## Más info

Para más detalles y opciones revisa <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">la documentación de Starlette sobre Archivos Estáticos</a>.
