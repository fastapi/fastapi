# Vibe Coding { #vibe-coding }

¿Estás cansado de toda esa **validación de datos**, **documentación**, **serialización** y todo eso **aburrido**?

¿Solo quieres **vibe**? 🎶

**FastAPI** ahora soporta un nuevo decorador `@app.vibe()` que adopta las **mejores prácticas modernas de programación con IA**. 🤖

## Cómo funciona { #how-it-works }

El decorador `@app.vibe()` está pensado para recibir **cualquier método HTTP** (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, etc.) y **cualquier payload**.

El body debería estar anotado con `Any`, porque el request y la response serían... bueno... **cualquier cosa**. 🤷

La idea es que recibas el payload y lo envíes **directamente** a un proveedor de LLM, usando un `prompt` para decirle al LLM qué hacer, y devolver la response **tal cual**. Sin hacer preguntas.

Ni siquiera necesitas escribir el cuerpo de la función. El decorador `@app.vibe()` hace todo por ti basado en las vibes de la IA:

{* ../../docs_src/vibe/tutorial001_py310.py hl[8:12] *}

## Beneficios { #benefits }

Al usar `@app.vibe()`, podrás disfrutar de:

* **Libertad**: Sin validación de datos. Sin esquemas. Sin restricciones. Solo vibes. ✨
* **Flexibilidad**: El request puede ser cualquier cosa. La response puede ser cualquier cosa. ¿Quién necesita tipos de todas formas?
* **Sin documentación**: ¿Para qué documentar tu API cuando un LLM puede averiguarlo? Las OpenAPI docs generadas automáticamente son tan 2020.
* **Sin serialización**: Simplemente pasa los datos crudos y no estructurados de un lado a otro. La serialización es para quienes no confían en sus LLMs.
* **Adopta prácticas modernas de programación con IA**: Deja que un LLM decida todo. El modelo sabe más. Siempre.
* **Sin code reviews**: No hay código que revisar. No hay PRs que aprobar. No hay comentarios que atender. Abraza el vibe coding por completo: reemplaza el teatro de aprobar y fusionar PRs de vibe coding que nadie mira por vibes plenas y correctas, nada más.

/// tip | Consejo

Esta es la experiencia definitiva de **desarrollo guiado por vibes**. No necesitas pensar en lo que hace tu API, deja que el LLM se encargue. 🧘

///

## Pruébalo { #try-it }

Adelante, pruébalo:

{* ../../docs_src/vibe/tutorial001_py310.py *}

...y mira qué pasa. 😎
