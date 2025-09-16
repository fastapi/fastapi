# Seguridad

Hay muchas formas de manejar la seguridad, autenticación y autorización.

Y normalmente es un tema complejo y "difícil".

En muchos frameworks y sistemas, solo manejar la seguridad y autenticación requiere una gran cantidad de esfuerzo y código (en muchos casos puede ser el 50% o más de todo el código escrito).

**FastAPI** proporciona varias herramientas para ayudarte a manejar la **Seguridad** de manera fácil, rápida y estándar, sin tener que estudiar y aprender todas las especificaciones de seguridad.

Pero primero, vamos a revisar algunos pequeños conceptos.

## ¿Con prisa?

Si no te importan ninguno de estos términos y solo necesitas agregar seguridad con autenticación basada en nombre de usuario y contraseña *ahora mismo*, salta a los siguientes capítulos.

## OAuth2

OAuth2 es una especificación que define varias maneras de manejar la autenticación y autorización.

Es una especificación bastante extensa y cubre varios casos de uso complejos.

Incluye formas de autenticarse usando un "tercero".

Eso es lo que todos los sistemas con "iniciar sesión con Facebook, Google, X (Twitter), GitHub" utilizan internamente.

### OAuth 1

Hubo un OAuth 1, que es muy diferente de OAuth2, y más complejo, ya que incluía especificaciones directas sobre cómo encriptar la comunicación.

No es muy popular o usado hoy en día.

OAuth2 no especifica cómo encriptar la comunicación, espera que tengas tu aplicación servida con HTTPS.

/// tip | Consejo

En la sección sobre **deployment** verás cómo configurar HTTPS de forma gratuita, usando Traefik y Let's Encrypt.

///

## OpenID Connect

OpenID Connect es otra especificación, basada en **OAuth2**.

Solo extiende OAuth2 especificando algunas cosas que son relativamente ambiguas en OAuth2, para intentar hacerla más interoperable.

Por ejemplo, el login de Google usa OpenID Connect (que internamente usa OAuth2).

Pero el login de Facebook no soporta OpenID Connect. Tiene su propia versión de OAuth2.

### OpenID (no "OpenID Connect")

Hubo también una especificación "OpenID". Que intentaba resolver lo mismo que **OpenID Connect**, pero no estaba basada en OAuth2.

Entonces, era un sistema completo adicional.

No es muy popular o usado hoy en día.

## OpenAPI

OpenAPI (anteriormente conocido como Swagger) es la especificación abierta para construir APIs (ahora parte de la Linux Foundation).

**FastAPI** se basa en **OpenAPI**.

Eso es lo que hace posible tener múltiples interfaces de documentación interactiva automática, generación de código, etc.

OpenAPI tiene una forma de definir múltiples "esquemas" de seguridad.

Al usarlos, puedes aprovechar todas estas herramientas basadas en estándares, incluidos estos sistemas de documentación interactiva.

OpenAPI define los siguientes esquemas de seguridad:

* `apiKey`: una clave específica de la aplicación que puede provenir de:
  * Un parámetro de query.
  * Un header.
  * Una cookie.
* `http`: sistemas de autenticación HTTP estándar, incluyendo:
  * `bearer`: un header `Authorization` con un valor de `Bearer ` más un token. Esto se hereda de OAuth2.
  * Autenticación básica HTTP.
  * Digest HTTP, etc.
* `oauth2`: todas las formas de OAuth2 para manejar la seguridad (llamadas "flujos").
  * Varios de estos flujos son apropiados para construir un proveedor de autenticación OAuth 2.0 (como Google, Facebook, X (Twitter), GitHub, etc.):
    * `implicit`
    * `clientCredentials`
    * `authorizationCode`
  * Pero hay un "flujo" específico que puede usarse perfectamente para manejar la autenticación directamente en la misma aplicación:
    * `password`: algunos de los próximos capítulos cubrirán ejemplos de esto.
* `openIdConnect`: tiene una forma de definir cómo descubrir automáticamente los datos de autenticación OAuth2.
  * Este descubrimiento automático es lo que se define en la especificación de OpenID Connect.

/// tip | Consejo

Integrar otros proveedores de autenticación/autorización como Google, Facebook, X (Twitter), GitHub, etc. también es posible y relativamente fácil.

El problema más complejo es construir un proveedor de autenticación/autorización como esos, pero **FastAPI** te da las herramientas para hacerlo fácilmente, mientras hace el trabajo pesado por ti.

///

## Utilidades de **FastAPI**

FastAPI proporciona varias herramientas para cada uno de estos esquemas de seguridad en el módulo `fastapi.security` que simplifican el uso de estos mecanismos de seguridad.

En los siguientes capítulos verás cómo agregar seguridad a tu API usando esas herramientas proporcionadas por **FastAPI**.

Y también verás cómo se integra automáticamente en el sistema de documentación interactiva.
