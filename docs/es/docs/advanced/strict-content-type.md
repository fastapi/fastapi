# Chequeo estricto de Content-Type { #strict-content-type-checking }

Por defecto, **FastAPI** usa un chequeo estricto del header `Content-Type` para request bodies JSON, esto significa que las requests JSON deben incluir un header `Content-Type` válido (p. ej. `application/json`) para que el request body se parse como JSON.

## Riesgo de CSRF { #csrf-risk }

Este comportamiento por defecto provee protección contra una clase de ataques de **Cross-Site Request Forgery (CSRF)** en un escenario muy específico.

Estos ataques aprovechan que los navegadores permiten que los scripts envíen requests sin hacer un preflight de CORS cuando:

* no tienen un header `Content-Type` (p. ej. usando `fetch()` con un body `Blob`)
* y no envían credenciales de autenticación.

Este tipo de ataque es relevante principalmente cuando:

* la aplicación corre localmente (p. ej. en `localhost`) o en una red interna
* y la aplicación no tiene ninguna autenticación, espera que cualquier request de la misma red sea confiable.

## Ejemplo de ataque { #example-attack }

Imagina que construyes una forma de ejecutar un agente de IA local.

Provee un API en

```
http://localhost:8000/v1/agents/multivac
```

También hay un frontend en

```
http://localhost:8000
```

/// tip | Consejo

Ten en cuenta que ambos tienen el mismo host.

///

Luego, usando el frontend, puedes hacer que el agente de IA haga cosas en tu nombre.

Como está corriendo localmente y no en Internet abierta, decides no tener ninguna autenticación configurada, confiando simplemente en el acceso a la red local.

Entonces, uno de tus usuarios podría instalarlo y ejecutarlo localmente.

Después podría abrir un sitio web malicioso, por ejemplo algo como

```
https://evilhackers.example.com
```

Y ese sitio malicioso envía requests usando `fetch()` con un body `Blob` al API local en

```
http://localhost:8000/v1/agents/multivac
```

Aunque el host del sitio malicioso y el de la app local sea diferente, el navegador no disparará un preflight de CORS porque:

* Está corriendo sin ninguna autenticación, no tiene que enviar credenciales.
* El navegador cree que no está enviando JSON (por la falta del header `Content-Type`).

Entonces el sitio malicioso podría hacer que el agente de IA local envíe mensajes agresivos al exjefe del usuario... o peor. 😅

## Internet abierta { #open-internet }

Si tu app está en Internet abierta, no “confiarías en la red” ni permitirías que cualquiera envíe requests privilegiadas sin autenticación.

Los atacantes podrían simplemente ejecutar un script para enviar requests a tu API, sin necesidad de interacción del navegador, así que probablemente ya estás asegurando cualquier endpoint privilegiado.

En ese caso, este ataque/riesgo no aplica a ti.

Este riesgo y ataque es relevante principalmente cuando la app corre en la red local y esa es la única protección asumida.

## Permitir requests sin Content-Type { #allowing-requests-without-content-type }

Si necesitas soportar clientes que no envían un header `Content-Type`, puedes desactivar el chequeo estricto configurando `strict_content_type=False`:

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

Con esta configuración, las requests sin un header `Content-Type` tendrán su body parseado como JSON, que es el mismo comportamiento de versiones anteriores de FastAPI.

/// info | Información

Este comportamiento y configuración se añadieron en FastAPI 0.132.0.

///
