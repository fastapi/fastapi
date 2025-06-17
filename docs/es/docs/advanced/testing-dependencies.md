# Probando Dependencias con Overrides

## Sobrescribir dependencias durante las pruebas

Hay algunos escenarios donde podrías querer sobrescribir una dependencia durante las pruebas.

No quieres que la dependencia original se ejecute (ni ninguna de las sub-dependencias que pueda tener).

En cambio, quieres proporcionar una dependencia diferente que se usará solo durante las pruebas (posiblemente solo algunas pruebas específicas), y que proporcionará un valor que pueda ser usado donde se usó el valor de la dependencia original.

### Casos de uso: servicio externo

Un ejemplo podría ser que tienes un proveedor de autenticación externo al que necesitas llamar.

Le envías un token y te devuelve un usuario autenticado.

Este proveedor podría estar cobrándote por cada request, y llamarlo podría tomar más tiempo adicional que si tuvieras un usuario de prueba fijo para los tests.

Probablemente quieras probar el proveedor externo una vez, pero no necesariamente llamarlo para cada test que se realice.

En este caso, puedes sobrescribir la dependencia que llama a ese proveedor y usar una dependencia personalizada que devuelva un usuario de prueba, solo para tus tests.

### Usa el atributo `app.dependency_overrides`

Para estos casos, tu aplicación **FastAPI** tiene un atributo `app.dependency_overrides`, es un simple `dict`.

Para sobrescribir una dependencia para las pruebas, colocas como clave la dependencia original (una función), y como valor, tu dependencia para sobreescribir (otra función).

Y entonces **FastAPI** llamará a esa dependencia para sobreescribir en lugar de la dependencia original.

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | Consejo

Puedes sobreescribir una dependencia utilizada en cualquier lugar de tu aplicación **FastAPI**.

La dependencia original podría ser utilizada en una *path operation function*, un *path operation decorator* (cuando no usas el valor de retorno), una llamada a `.include_router()`, etc.

FastAPI todavía podrá sobrescribirla.

///

Entonces puedes restablecer las dependencias sobreescritas configurando `app.dependency_overrides` para que sea un `dict` vacío:

```Python
app.dependency_overrides = {}
```

/// tip | Consejo

Si quieres sobrescribir una dependencia solo durante algunos tests, puedes establecer la sobrescritura al inicio del test (dentro de la función del test) y restablecerla al final (al final de la función del test).

///
