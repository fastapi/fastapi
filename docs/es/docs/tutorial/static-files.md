# Archivos estáticos

Puede servir archivos estáticos automáticamente desde un directorio usando `StaticFiles`.

## Usar `StaticFiles`

* importar `StaticFiles`.
* "Montar" una instancia de `StaticFiles()` en una ruta específica.

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "Detalles técnicos"
    También podrías usar `from starlette.staticfiles import StaticFiles`.

    **FastAPI** proporciona lo mismo `starlette.staticfiles` como `fastapi.staticfiles` sólo como una comodidad para usted, el desarrollador. Pero en realidad viene directamente de Starlette.

### Qué es "Montaje"

"Montar" significa agregar una aplicación "independiente" completa en una ruta específica, que luego se encarga de manejar todas las subrutas.

Esto es diferente a usar un `APIRouter` ya que una aplicación montada es completamente independiente. OpenAPI y los documentos de su aplicación principal no incluirán nada de la aplicación montada, etc.

Puede leer más sobre esto en la **Guía de usuario avanzada**.

## Detalles

El primer `"/static"` se refiere a la subruta en la que se "montará" esta "sub-aplicación". Por lo tanto, cualquier ruta que comience con `"/static"` será manejada por él.

`directory="static"` se refiere al nombre del directorio que contiene sus archivos estáticos.

`name="static"` le da un nombre que **FastAPI** puede usar internamente.

Todos estos parámetros pueden ser diferentes a `"static"`, ajústelos con las necesidades y detalles específicos de su propia aplicación.

## Más información

Para más detalles y opciones consultar <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Documentos de Starlette sobre archivos estáticos</a>.
