# Código de Estado del Response

De la misma manera que puedes especificar un modelo de response, también puedes declarar el código de estado HTTP usado para el response con el parámetro `status_code` en cualquiera de las *path operations*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

{* ../../docs_src/response_status_code/tutorial001.py hl[6] *}

/// note | Nota

Observa que `status_code` es un parámetro del método "decorador" (`get`, `post`, etc). No de tu *path operation function*, como todos los parámetros y body.

///

El parámetro `status_code` recibe un número con el código de estado HTTP.

/// info | Información

`status_code` también puede recibir un `IntEnum`, como por ejemplo el <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a> de Python.

///

Esto hará:

* Devolver ese código de estado en el response.
* Documentarlo como tal en el esquema de OpenAPI (y por lo tanto, en las interfaces de usuario):

<img src="/img/tutorial/response-status-code/image01.png">

/// note | Nota

Algunos códigos de response (ver la siguiente sección) indican que el response no tiene un body.

FastAPI sabe esto, y producirá documentación OpenAPI que establece que no hay un response body.

///

## Acerca de los códigos de estado HTTP

/// note | Nota

Si ya sabes qué son los códigos de estado HTTP, salta a la siguiente sección.

///

En HTTP, envías un código de estado numérico de 3 dígitos como parte del response.

Estos códigos de estado tienen un nombre asociado para reconocerlos, pero la parte importante es el número.

En breve:

* `100` y superiores son para "Información". Rara vez los usas directamente. Los responses con estos códigos de estado no pueden tener un body.
* **`200`** y superiores son para responses "Exitosos". Estos son los que usarías más.
    * `200` es el código de estado por defecto, lo que significa que todo estaba "OK".
    * Otro ejemplo sería `201`, "Created". Comúnmente se usa después de crear un nuevo registro en la base de datos.
    * Un caso especial es `204`, "No Content". Este response se usa cuando no hay contenido para devolver al cliente, por lo tanto, el response no debe tener un body.
* **`300`** y superiores son para "Redirección". Los responses con estos códigos de estado pueden o no tener un body, excepto `304`, "Not Modified", que no debe tener uno.
* **`400`** y superiores son para responses de "Error del Cliente". Este es el segundo tipo que probablemente más usarías.
    * Un ejemplo es `404`, para un response "Not Found".
    * Para errores genéricos del cliente, puedes usar simplemente `400`.
* `500` y superiores son para errores del servidor. Casi nunca los usas directamente. Cuando algo sale mal en alguna parte de tu código de aplicación, o del servidor, automáticamente devolverá uno de estos códigos de estado.

/// tip | Consejo

Para saber más sobre cada código de estado y qué código es para qué, revisa la <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank">documentación de <abbr title="Mozilla Developer Network">MDN</abbr> sobre códigos de estado HTTP</a>.

///

## Atajo para recordar los nombres

Veamos de nuevo el ejemplo anterior:

{* ../../docs_src/response_status_code/tutorial001.py hl[6] *}

`201` es el código de estado para "Created".

Pero no tienes que memorizar lo que significa cada uno de estos códigos.

Puedes usar las variables de conveniencia de `fastapi.status`.

{* ../../docs_src/response_status_code/tutorial002.py hl[1,6] *}

Son solo una conveniencia, mantienen el mismo número, pero de esa manera puedes usar el autocompletado del editor para encontrarlos:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | Nota Técnica

También podrías usar `from starlette import status`.

**FastAPI** proporciona el mismo `starlette.status` como `fastapi.status` solo como una conveniencia para ti, el desarrollador. Pero proviene directamente de Starlette.

///

## Cambiando el valor por defecto

Más adelante, en la [Guía de Usuario Avanzada](../advanced/response-change-status-code.md){.internal-link target=_blank}, verás cómo devolver un código de estado diferente al valor por defecto que estás declarando aquí.
