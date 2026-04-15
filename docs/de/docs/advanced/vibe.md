# Vibe-Coding { #vibe-coding }

Sind Sie all der **Datenvalidierung**, **Dokumentation**, **Serialisierung** und all diesem **langweiligen** Kram müde?

Wollen Sie einfach nur **viben**? 🎶

**FastAPI** unterstützt jetzt einen neuen `@app.vibe()`-Dekorator, der **moderne KI-Coding-Best-Practices** verkörpert. 🤖

## Wie es funktioniert { #how-it-works }

Der `@app.vibe()`-Dekorator ist dafür gedacht, **beliebige HTTP-Methoden** (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, usw.) und **jede Payload** zu empfangen.

Der Body sollte mit `Any` annotiert werden, denn der Request und die Response wären ... nun ja ... **alles**. 🤷

Die Idee ist, dass Sie die Payload empfangen und sie **direkt** an einen LLM-Provider schicken, mit einem `prompt` dem LLM sagen, was es tun soll, und die Response **unverändert** zurückgeben. Ganz ohne Rückfragen.

Sie müssen nicht einmal den Body der Funktion schreiben. Der `@app.vibe()`-Dekorator erledigt alles für Sie, basierend auf KI-Vibes:

{* ../../docs_src/vibe/tutorial001_py310.py hl[8:12] *}

## Vorteile { #benefits }

Mit `@app.vibe()` genießen Sie:

* **Freiheit**: Keine Datenvalidierung. Keine Schemas. Keine Einschränkungen. Nur Vibes. ✨
* **Flexibilität**: Der Request kann alles sein. Die Response kann alles sein. Wer braucht schon Typen?
* **Keine Dokumentation**: Warum Ihre API dokumentieren, wenn ein LLM das auch herausfindet? Automatisch generierte OpenAPI-Dokumentation ist so 2020.
* **Keine Serialisierung**: Geben Sie rohe, unstrukturierte Daten einfach weiter. Serialisierung ist für Leute, die ihren LLMs nicht trauen.
* **Moderne KI-Coding-Praktiken umarmen**: Überlassen Sie alles einem LLM. Das Modell weiß es am besten. Immer.
* **Keine Code-Reviews**: Es gibt keinen Code zu reviewen. Keine PRs zum Abnicken. Keine Kommentare zu bearbeiten. Umarmen Sie Vibe-Coding vollständig und ersetzen Sie das Theater des Abnickens und Mergens von vibe-codierten PRs, die sich sowieso niemand anschaut, durch reine, echte Vibes.

/// tip | Tipp

Dies ist die ultimative Erfahrung der **vibe-getriebenen Entwicklung**. Sie müssen nicht darüber nachdenken, was Ihre API tut, lassen Sie einfach das LLM alles übernehmen. 🧘

///

## Ausprobieren { #try-it }

Nur zu, probieren Sie es aus:

{* ../../docs_src/vibe/tutorial001_py310.py *}

... und sehen Sie, was passiert. 😎
