# Sobre las versiones de FastAPI

**FastAPI** ya se está utilizando en producción en muchas aplicaciones y sistemas. Y la cobertura de tests se mantiene al 100%. Pero su desarrollo sigue avanzando rápidamente.

Se añaden nuevas funcionalidades con frecuencia, se corrigen bugs regularmente, y el código sigue mejorando continuamente.

Por eso las versiones actuales siguen siendo `0.x.x`, esto refleja que cada versión podría tener potencialmente cambios incompatibles. Esto sigue las convenciones de <a href="https://semver.org/" class="external-link" target="_blank">Semantic Versioning</a>.

Puedes crear aplicaciones de producción con **FastAPI** ahora mismo (y probablemente ya lo has estado haciendo desde hace algún tiempo), solo debes asegurarte de que utilizas una versión que funciona correctamente con el resto de tu código.

## Fijar tu versión de `fastapi`

Lo primero que debes hacer es "fijar" la versión de **FastAPI** que estás usando a la versión específica más reciente que sabes que funciona correctamente para tu aplicación.

Por ejemplo, digamos que estás utilizando la versión `0.112.0` en tu aplicación.

Si usas un archivo `requirements.txt` podrías especificar la versión con:

```txt
fastapi[standard]==0.112.0
```

eso significaría que usarías exactamente la versión `0.112.0`.

O también podrías fijarla con:

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

eso significaría que usarías las versiones `0.112.0` o superiores, pero menores que `0.113.0`, por ejemplo, una versión `0.112.2` todavía sería aceptada.

Si utilizas cualquier otra herramienta para gestionar tus instalaciones, como `uv`, Poetry, Pipenv, u otras, todas tienen una forma que puedes usar para definir versiones específicas para tus paquetes.

## Versiones disponibles

Puedes ver las versiones disponibles (por ejemplo, para revisar cuál es la más reciente) en las [Release Notes](../release-notes.md){.internal-link target=_blank}.

## Sobre las versiones

Siguiendo las convenciones del Semantic Versioning, cualquier versión por debajo de `1.0.0` podría potencialmente añadir cambios incompatibles.

FastAPI también sigue la convención de que cualquier cambio de versión "PATCH" es para corrección de bugs y cambios no incompatibles.

/// tip | Consejo

El "PATCH" es el último número, por ejemplo, en `0.2.3`, la versión PATCH es `3`.

///

Así que deberías poder fijar a una versión como:

```txt
fastapi>=0.45.0,<0.46.0
```

Los cambios incompatibles y nuevas funcionalidades se añaden en versiones "MINOR".

/// tip | Consejo

El "MINOR" es el número en el medio, por ejemplo, en `0.2.3`, la versión MINOR es `2`.

///

## Actualizando las versiones de FastAPI

Deberías añadir tests para tu aplicación.

Con **FastAPI** es muy fácil (gracias a Starlette), revisa la documentación: [Testing](../tutorial/testing.md){.internal-link target=_blank}

Después de tener tests, puedes actualizar la versión de **FastAPI** a una más reciente, y asegurarte de que todo tu código está funcionando correctamente ejecutando tus tests.

Si todo está funcionando, o después de hacer los cambios necesarios, y todos tus tests pasan, entonces puedes fijar tu `fastapi` a esa nueva versión más reciente.

## Sobre Starlette

No deberías fijar la versión de `starlette`.

Diferentes versiones de **FastAPI** utilizarán una versión más reciente específica de Starlette.

Así que, puedes simplemente dejar que **FastAPI** use la versión correcta de Starlette.

## Sobre Pydantic

Pydantic incluye los tests para **FastAPI** con sus propios tests, así que nuevas versiones de Pydantic (por encima de `1.0.0`) siempre son compatibles con FastAPI.

Puedes fijar Pydantic a cualquier versión por encima de `1.0.0` que funcione para ti.

Por ejemplo:

```txt
pydantic>=2.7.0,<3.0.0
```
