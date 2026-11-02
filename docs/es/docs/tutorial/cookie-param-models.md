# Modelos de Cookies { #cookie-parameter-models }

Si tienes un grupo de **cookies** que están relacionadas, puedes crear un **modelo de Pydantic** para declararlas. 🍪

Esto te permitirá **reutilizar el modelo** en **múltiples lugares** y también declarar validaciones y metadatos para todos los parámetros a la vez. 😎

/// note | Nota

Esto es compatible desde la versión `0.115.0` de FastAPI. 🤓

///

/// tip | Consejo

Esta misma técnica se aplica a `Query`, `Cookie`, y `Header`. 😎

///

## Cookies con un Modelo de Pydantic { #cookies-with-a-pydantic-model }

Declara los parámetros de **cookie** que necesites en un **modelo de Pydantic**, y luego declara el parámetro como `Cookie`:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI** **extraerá** los datos para **cada campo** de las **cookies** recibidas en el request y te entregará el modelo de Pydantic que definiste.

## Revisa la Documentación { #check-the-docs }

Puedes ver las cookies definidas en la UI de la documentación en `/docs`:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note | Nota

Ten en cuenta que, como los **navegadores manejan las cookies** de maneras especiales y detrás de escenas, **no** permiten fácilmente que **JavaScript** las toque.

Si vas a la **UI de la documentación de la API** en `/docs` podrás ver la **documentación** de las cookies para tus *path operations*.

Pero incluso si **rellenas los datos** y haces clic en "Execute", como la UI de la documentación funciona con **JavaScript**, las cookies no serán enviadas y verás un **mensaje de error** como si no hubieras escrito ningún valor.

///

## Prohibir Cookies Extra { #forbid-extra-cookies }

En algunos casos de uso especiales (probablemente no muy comunes), podrías querer **restringir** las cookies que deseas recibir.

Tu API ahora tiene el poder de controlar su propio <dfn title="Esto es una broma, por si acaso. No tiene nada que ver con los consentimientos de cookies, pero es gracioso que incluso la API ahora pueda rechazar las pobres cookies. Toma una cookie. 🍪">consentimiento de cookies</dfn>. 🤪🍪

Puedes usar la configuración del modelo de Pydantic para `prohibir` cualquier campo `extra`:

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

Si un cliente intenta enviar algunas **cookies extra**, recibirán un response de **error**.

Pobres banners de cookies con todo su esfuerzo para obtener tu consentimiento para que la <dfn title="Esta es otra broma. No me prestes atención. Toma un café para tu cookie. ☕">API lo rechace</dfn>. 🍪

Por ejemplo, si el cliente intenta enviar una cookie `santa_tracker` con un valor de `good-list-please`, el cliente recibirá un response de **error** que le informa que la `santa_tracker` <dfn title="Santa desaprueba la falta de cookies. 🎅 Está bien, no más bromas de cookies.">cookie no está permitida</dfn>:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## Resumen { #summary }

Puedes usar **modelos de Pydantic** para declarar <dfn title="Toma una última cookie antes de irte. 🍪">**cookies**</dfn> en **FastAPI**. 😎
