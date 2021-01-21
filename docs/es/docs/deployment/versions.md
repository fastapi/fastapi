# Acerca de las versiones de FastAPI

**FastAPI** ya esta siendo usado en producción en muchos sistemas y aplicaciones. Y el test de cobertura es mantenido al 100%. Sin embargo su desarrollo sigue moviéndose rápidamente.

Nuevas funciones son añadidas frecuentemente, bugs están siendo solucionados, y el código sigue mejorando constantemente.

Ese es el porque de que la versión actual siga en `0.x.x`, esto refleja que, potencialmente, cada versión pueda tener cambios mayores. Esto sigue las conversiones de versionamiento semántico, <a href="https://semver.org/" class="external-link" target="_blank">Semantic Versioning</a>.

Puedes crear aplicaciones para producción con **FastAPI** ahora mismo (y probablemente lo has estado haciendo desde hace algún tiempo), solo tienes que asegurarte que usas una version que funciona correctamente con el resto de tu código.

## Marca tu versión de `fastapi`

La primera cosa que deberías hacer es "marcar" la version de **FastAPI** que estas usando, a la última versión específica que sabes que funciona correctamente con tu aplicación.

Por ejemplo, supongamos que estas usando la version `0.45.0` en tu app.

Si usas un archivo de requerimientos como `requirements.txt`, puedes especificar la version de la siguiente manera:

```txt
fastapi==0.45.0
```

eso quiere decir que tu usaras, exactamente, la versión `0.45.0`.

O tu podrías también marcar la version así:

```txt
fastapi>=0.45.0,<0.46.0
```

eso quiere decir que usaras la version `0.45.0` o posterior, pero que sera anterior a la `0.46.0`, por ejemplo, en este caso la version `0.45.2` sigue siendo aceptada.

Si usas cualquier otra herramienta para manejar tus instalaciones, como Poetry, Pipenv, o otras, todas ellas tienen una manera de definir la versión específica de tus paquetes.

## Versiones disponibles

Puedes revisar las versiones disponibles (e.g. revisar cual es la mas reciente) en las [Release Notes](../release-notes.md){.internal-link target=_blank}.

## Acerca de las versiones

Siguiendo las convenciones de version Semantic Versioning, cualquier version por debajo de `1.0.0` puede potencialmente añadir cambios mayores.

FastAPI también sigue la convención que cualquier cambio de version de tipo "PATCH", es para solución de errores y no cambios mayores.

!!! tip
    El "PATCH" es el último numero, por ejemplo, en `0.2.3`, la version del "PATCH" es `3`.

Por lo tanto, deberías de poder marcar una version como:

```txt
fastapi>=0.45.0,<0.46.0
```

Cambios mayores y nuevas características son añadidas en versiones "MENORES"

!!! tip
    La versión "MENOR" corresponde al numero en el medio, por ejemplo, en `0.2.3`, la version "MENOR" es `2`.

## Actualizar las versiones de FastAPI

Debes de añadir tests para tu app.

Con **FastAPI** es muy sencillo (gracias a Starlette), revisa la documentación: [Testing](../tutorial/testing.md){.internal-link target=_blank}.

Después de tener pruebas (tests), entonces puedes actualizar la version de **FastAPI** a una mas reciente, y estar seguro que todo tu código esta funcionando correctamente al ejecutar tus pruebas (tests).

Si todo esta funcionando, o después de haber hecho los cambios necesarios, y todas tus pruebas (tests) han pasado, entonces puedes marcar la version de `fastapi` a una version mas reciente.

## Acerca de Starlette

No debes de marcar la versión de `starlette`.

Diferentes versiones de **FastAPI** usarán una versión especificamente mas reciente de Starlette.

Por lo tanto, puedes solamente dejar que **FastAPI** use la versión correcta de Starlette.

## Acerca de Pydantic

Pydantic incluye los tests de **FastAPI** en sus propios tests, así que nuevas versiones de Pydantic (superiores a `1.0.0`) son siempre compatibles con FastAPI.

Puedes marcar Pydantic a cualquier version, mayor a `1.0.0` y menor a `2.0.0`, que funcione para ti.

Por ejemplo:

```txt
pydantic>=1.2.0,<2.0.0
```
