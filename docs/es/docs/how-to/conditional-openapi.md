# OpenAPI Condicional

Si lo necesitaras, podrías usar configuraciones y variables de entorno para configurar OpenAPI condicionalmente según el entorno, e incluso desactivarlo por completo.

## Sobre seguridad, APIs y documentación

Ocultar las interfaces de usuario de la documentación en producción *no debería* ser la forma de proteger tu API.

Eso no añade ninguna seguridad extra a tu API, las *path operations* seguirán estando disponibles donde están.

Si hay una falla de seguridad en tu código, seguirá existiendo.

Ocultar la documentación solo hace que sea más difícil entender cómo interactuar con tu API y podría dificultar más depurarla en producción. Podría considerarse simplemente una forma de <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">Seguridad mediante oscuridad</a>.

Si quieres asegurar tu API, hay varias cosas mejores que puedes hacer, por ejemplo:

* Asegúrate de tener modelos Pydantic bien definidos para tus request bodies y responses.
* Configura los permisos y roles necesarios usando dependencias.
* Nunca guardes contraseñas en texto plano, solo hashes de contraseñas.
* Implementa y utiliza herramientas criptográficas bien conocidas, como Passlib y JWT tokens, etc.
* Añade controles de permisos más detallados con OAuth2 scopes donde sea necesario.
* ...etc.

No obstante, podrías tener un caso de uso muy específico donde realmente necesites desactivar la documentación de la API para algún entorno (por ejemplo, para producción) o dependiendo de configuraciones de variables de entorno.

## OpenAPI condicional desde configuraciones y variables de entorno

Puedes usar fácilmente las mismas configuraciones de Pydantic para configurar tu OpenAPI generado y las interfaces de usuario de la documentación.

Por ejemplo:

{* ../../docs_src/conditional_openapi/tutorial001.py hl[6,11] *}

Aquí declaramos la configuración `openapi_url` con el mismo valor predeterminado de `"/openapi.json"`.

Y luego la usamos al crear la app de `FastAPI`.

Entonces podrías desactivar OpenAPI (incluyendo las UI de documentación) configurando la variable de entorno `OPENAPI_URL` a una string vacía, así:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Luego, si vas a las URLs en `/openapi.json`, `/docs`, o `/redoc`, solo obtendrás un error `404 Not Found` como:

```JSON
{
    "detail": "Not Found"
}
```
