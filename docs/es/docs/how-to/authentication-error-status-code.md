# Usar los códigos de estado antiguos 403 para errores de autenticación { #use-old-403-authentication-error-status-codes }

Antes de FastAPI versión `0.122.0`, cuando las utilidades de seguridad integradas devolvían un error al cliente después de una autenticación fallida, usaban el código de estado HTTP `403 Forbidden`.

A partir de FastAPI versión `0.122.0`, usan el código de estado HTTP `401 Unauthorized`, más apropiado, y devuelven un `WWW-Authenticate` header adecuado en la response, siguiendo las especificaciones HTTP, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Pero si por alguna razón tus clientes dependen del comportamiento anterior, puedes volver a él sobrescribiendo el método `make_not_authenticated_error` en tus clases de seguridad.

Por ejemplo, puedes crear una subclase de `HTTPBearer` que devuelva un error `403 Forbidden` en lugar del `401 Unauthorized` por defecto:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py39.py hl[9:13] *}

/// tip | Consejo

Ten en cuenta que la función devuelve la instance de la excepción, no la lanza. El lanzamiento se hace en el resto del código interno.

///
