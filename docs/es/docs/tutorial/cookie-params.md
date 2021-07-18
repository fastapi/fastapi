# Parámetros Cookie

Puedes definir parámetros Cookie de la misma manera en que defines parámetros de `Query` y `Path`.

## Importar `Cookie`

Primero importa `Cookie`:

```Python hl_lines="3"
{!../../../docs_src/cookie_params/tutorial001.py!}
```

## Declarar parámetros `Cookie`

Luego declara los parámetros cookie usando la misma estructura que usamos con `Path` y `Query`.

El primer valor es el valor por defecto, puedes pasar todas las validaciones extras o anotaciones para los parámetros.

```Python hl_lines="9"
{!../../../docs_src/cookie_params/tutorial001.py!}
```

!!! note "Detalles Técnicos"
    `Cookie` es una clase "hermana" de `Path` y `Query`. También hereda de la misma clase común `Param`.

    Pero recuerda que cuando importas `Query`, `Path`, `Cookie` y demás desde `fastapi`, estos son en realidad funciones que retornan una clase especial.

!!! info
    Para declarar cookies, necesitas usar `Cookie`, porque sino los parámetros serían interpretados como parámetros de query.

## Recapitulación

Declara cookies con `Cookie`, usando el mismo patrón común que con `Query` y `Path`.
