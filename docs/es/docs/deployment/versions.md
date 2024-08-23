# Acerca de las versiones de FastAPI

**FastAPI** está siendo utilizado en producción en muchas aplicaciones y sistemas. La cobertura de los tests se mantiene al 100%. Sin embargo, su desarrollo sigue siendo rápido.

Se agregan nuevas características frecuentemente, se corrigen errores continuamente y el código está constantemente mejorando.

Por eso las versiones actuales siguen siendo `0.x.x`, esto significa que cada versión puede potencialmente tener <abbr title="cambios que rompen funcionalidades o compatibilidad">*breaking changes*</abbr>. Las versiones siguen las convenciones de <a href="https://semver.org/" class="external-link" target="_blank"><abbr title="versionado semántico">*Semantic Versioning*</abbr></a>.

Puedes crear aplicaciones listas para producción con **FastAPI** ahora mismo (y probablemente lo has estado haciendo por algún tiempo), solo tienes que asegurarte de usar la versión que funciona correctamente con el resto de tu código.

## Fijar la versión de `fastapi`

Lo primero que debes hacer en tu proyecto es "fijar" la última versión específica de **FastAPI** que sabes que funciona bien con tu aplicación.

Por ejemplo, digamos que estás usando la versión `0.45.0` en tu aplicación.

Si usas el archivo `requirements.txt` puedes especificar la versión con:

```txt
fastapi==0.45.0
```

esto significa que usarás específicamente la versión `0.45.0`.

También puedes fijar las versiones de esta forma:

```txt
fastapi>=0.45.0,<0.46.0
```

esto significa que usarás la versión `0.45.0` o superiores, pero menores a la versión `0.46.0`, por ejemplo, la versión `0.45.2` sería aceptada.

Si usas cualquier otra herramienta para manejar tus instalaciones, como Poetry, Pipenv, u otras, todas tienen una forma que puedes usar para definir versiones específicas para tus paquetes.

## Versiones disponibles

Puedes ver las versiones disponibles (por ejemplo, para revisar cuál es la actual) en las [Release Notes](../release-notes.md){.internal-link target=_blank}.

## Acerca de las versiones

Siguiendo las convenciones de *Semantic Versioning*, cualquier versión por debajo de `1.0.0` puede potencialmente tener <abbr title="cambios que rompen funcionalidades o compatibilidad">*breaking changes*</abbr>.

FastAPI también sigue la convención de que cualquier cambio hecho en una <abbr title="versiones de parche">"PATCH" version</abbr> es para solucionar errores y <abbr title="cambios que no rompan funcionalidades o compatibilidad">*non-breaking changes*</abbr>.

/// tip | Consejo

El <abbr title="parche">"PATCH"</abbr> es el último número, por ejemplo, en `0.2.3`, la <abbr title="versiones de parche">PATCH version</abbr> es `3`.

///

Entonces, deberías fijar la versión así:

```txt
fastapi>=0.45.0,<0.46.0
```

En versiones <abbr title="versiones menores">"MINOR"</abbr> son añadidas nuevas características y posibles <abbr title="Cambios que rompen posibles funcionalidades o compatibilidad">breaking changes</abbr>.

/// tip | Consejo

La versión "MINOR" es el número en el medio, por ejemplo, en `0.2.3`, la <abbr title="versión menor">"MINOR" version</abbr> es `2`.

///

## Actualizando las versiones de FastAPI

Para esto es recomendable primero añadir tests a tu aplicación.

Con **FastAPI** es muy fácil (gracias a Starlette), revisa la documentación [Testing](../tutorial/testing.md){.internal-link target=_blank}

Luego de tener los tests, puedes actualizar la versión de **FastAPI** a una más reciente y asegurarte de que tu código funciona correctamente ejecutando los tests.

Si todo funciona correctamente, o haces los cambios necesarios para que esto suceda, y todos tus tests pasan, entonces puedes fijar tu versión de `fastapi` a la más reciente.

## Acerca de Starlette

No deberías fijar la versión de `starlette`.

Diferentes versiones de **FastAPI** pueden usar una versión específica de Starlette.

Entonces, puedes dejar que **FastAPI** se asegure por sí mismo de qué versión de Starlette usar.

## Acerca de Pydantic

Pydantic incluye los tests para **FastAPI** dentro de sus propios tests, esto significa que las versiones de Pydantic (superiores a `1.0.0`) son compatibles con FastAPI.

Puedes fijar Pydantic a cualquier versión superior a `1.0.0` e inferior a `2.0.0` que funcione para ti.

Por ejemplo:

```txt
pydantic>=1.2.0,<2.0.0
```
