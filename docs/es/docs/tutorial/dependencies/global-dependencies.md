# Dependencias Globales

Para algunos tipos de aplicaciones, podrías querer agregar dependencias a toda la aplicación.

Similar a como puedes [agregar `dependencies` a los *path operation decorators*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, puedes agregarlos a la aplicación de `FastAPI`.

En ese caso, se aplicarán a todas las *path operations* en la aplicación:

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[16] *}

Y todas las ideas en la sección sobre [agregar `dependencies` a los *path operation decorators*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} siguen aplicándose, pero en este caso, a todas las *path operations* en la app.

## Dependencias para grupos de *path operations*

Más adelante, al leer sobre cómo estructurar aplicaciones más grandes ([Aplicaciones Más Grandes - Múltiples Archivos](../../tutorial/bigger-applications.md){.internal-link target=_blank}), posiblemente con múltiples archivos, aprenderás cómo declarar un solo parámetro de `dependencies` para un grupo de *path operations*.
