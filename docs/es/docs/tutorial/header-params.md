# Parámetros de Header

Puedes definir los parámetros de Header de la misma manera que defines los parámetros de `Query`, `Path` y `Cookie`.

## Importar `Header`

Primero importa `Header`:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## Declarar parámetros de `Header`

Luego declara los parámetros de header usando la misma estructura que con `Path`, `Query` y `Cookie`.

Puedes definir el valor por defecto así como toda la validación extra o los parámetros de anotaciones:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | Detalles Técnicos

`Header` es una clase "hermana" de `Path`, `Query` y `Cookie`. También hereda de la misma clase común `Param`.

Pero recuerda que cuando importas `Query`, `Path`, `Header`, y otros de `fastapi`, en realidad son funciones que retornan clases especiales.

///

/// info | Información

Para declarar headers, necesitas usar `Header`, porque de otra forma los parámetros serían interpretados como parámetros de query.

///

## Conversión automática

`Header` tiene un poquito de funcionalidad extra además de lo que proporcionan `Path`, `Query` y `Cookie`.

La mayoría de los headers estándar están separados por un carácter "guion", también conocido como el "símbolo menos" (`-`).

Pero una variable como `user-agent` es inválida en Python.

Así que, por defecto, `Header` convertirá los caracteres de los nombres de los parámetros de guion bajo (`_`) a guion (`-`) para extraer y documentar los headers.

Además, los headers HTTP no diferencian entre mayúsculas y minúsculas, por lo que los puedes declarar con el estilo estándar de Python (también conocido como "snake_case").

Así que, puedes usar `user_agent` como normalmente lo harías en código Python, en lugar de necesitar capitalizar las primeras letras como `User_Agent` o algo similar.

Si por alguna razón necesitas desactivar la conversión automática de guiones bajos a guiones, establece el parámetro `convert_underscores` de `Header` a `False`:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | Advertencia

Antes de establecer `convert_underscores` a `False`, ten en cuenta que algunos proxies y servidores HTTP no permiten el uso de headers con guiones bajos.

///

## Headers duplicados

Es posible recibir headers duplicados. Eso significa, el mismo header con múltiples valores.

Puedes definir esos casos usando una lista en la declaración del tipo.

Recibirás todos los valores del header duplicado como una `list` de Python.

Por ejemplo, para declarar un header de `X-Token` que puede aparecer más de una vez, puedes escribir:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

Si te comunicas con esa *path operation* enviando dos headers HTTP como:

```
X-Token: foo
X-Token: bar
```

El response sería como:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Recapitulación

Declara headers con `Header`, usando el mismo patrón común que `Query`, `Path` y `Cookie`.

Y no te preocupes por los guiones bajos en tus variables, **FastAPI** se encargará de convertirlos.
