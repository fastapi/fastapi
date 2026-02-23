# Zusätzliche Responses in OpenAPI { #additional-responses-in-openapi }

!!! warning "Achtung"
    Dies ist ein eher fortgeschrittenes Thema.
    
    Wenn Sie mit **FastAPI** beginnen, benötigen Sie dies möglicherweise nicht.

FastAPI erlaubt es, zusätzliche **Responses** zu deklarieren, die nicht nur den Standard‑`200`‑Success‑Response abdecken. Diese können weitere HTTP‑Statuscodes, unterschiedliche Medientypen, detaillierte Beschreibungen und sogar benutzerdefinierte Header enthalten. Alle zusätzlichen Responses werden automatisch in das OpenAPI‑Schema eingefügt, sodass sie in der automatisch generierten API‑Dokumentation (Swagger UI / ReDoc) sichtbar sind.

> **Wichtig:** Damit die zusätzlichen Responses korrekt in das OpenAPI‑Schema übernommen werden, müssen Sie einen **FastAPI‑Response‑Klasse** (z. B. `JSONResponse`, `HTMLResponse`, `PlainTextResponse` …) **direkt** zurückgeben und den gewünschten Statuscode angeben.

---

## Zusätzliche Response mit `model` { #additional-response-with-model }

Der einfachste Weg, zusätzliche Responses zu beschreiben, ist das Verwenden des Parameters `responses` im Dekorator einer Path‑Operation. Der Parameter erwartet ein **Dictionary**, wobei die Schlüssel HTTP‑Statuscodes (als `int` oder `str`) und die Werte wiederum Dictionaries mit den Metadaten der jeweiligen Response sind.

Ein häufiges Szenario ist das Hinzufügen eines `model`‑Eintrags, um ein Pydantic‑Modell als JSON‑Schema zu deklarieren.

```python
# docs_src/additional_responses/tutorial001_py310.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    detail: str

@app.get("/items/{item_id}", responses={
    404: {"model": Message, "description": "Item not found"},
})
async def read_item(item_id: int):
    if item_id != 42:
        # Hinweis: JSONResponse muss direkt zurückgegeben werden.
        return JSONResponse(status_code=404, content={"detail": "Item not found"})
    return {"item_id": item_id}
```

!!! note "Hinweis"
    Sie müssen die `JSONResponse` (oder eine andere Response‑Klasse) **direkt** zurückgeben, weil FastAPI sonst nicht erkennt, welchen Statuscode und welches Schema verwendet werden sollen.

### Wie wird das im OpenAPI‑Schema dargestellt?

FastAPI nimmt das Pydantic‑Modell, generiert daraus das JSON‑Schema und fügt es unter dem jeweiligen Statuscode in den OpenAPI‑Eintrag ein. Der relevante Teil des generierten Schemas sieht dann etwa so aus:

```json
"responses": {
    "404": {
        "description": "Item not found",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/Message"}
            }
        }
    }
}
```

---

## Zusätzliche Response mit `description` { #additional-response-with-description }

Manchmal reicht es, nur eine kurze Beschreibung für einen zusätzlichen Statuscode anzugeben, ohne ein Modell zu definieren. Das ist besonders nützlich für Statuscodes wie `202 Accepted` oder `204 No Content`.

```python
# docs_src/additional_responses/tutorial002_py310.py
from fastapi import FastAPI

app = FastAPI()

@app.post("/upload", responses={
    202: {"description": "Upload accepted and processing started"},
    400: {"description": "Bad request – missing file"},
})
async def upload_file():
    ...
```

Im generierten OpenAPI‑Schema wird lediglich die Beschreibung übernommen – es gibt keinen `content`‑Eintrag, weil kein Rückgabe‑Body erwartet wird.

---

## Zusätzliche Response mit eigenem Medientyp { #additional-response-with-content }

FastAPI unterstützt beliebige Medientypen. Sie können über den Schlüssel `content` angeben, welcher **Media‑Type** verwendet wird und welches Schema (oder welche Beispiel‑Daten) zurückgegeben werden.

```python
# docs_src/additional_responses/tutorial003_py310.py
from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/download", responses={
    200: {
        "content": {
            "text/plain": {
                "example": "Hello, world!"
            }
        },
        "description": "Plain‑text greeting"
    },
    404: {
        "description": "File not found"
    },
})
async def download():
    # Direktes Zurückgeben einer PlainTextResponse, damit FastAPI das
    # `text/plain`‑Schema korrekt registrieren kann.
    return PlainTextResponse("Hello, world!")
```

Im OpenAPI‑Schema erscheint dann ein `content`‑Eintrag für `text/plain` mit dem angegebenen Beispiel.

---

## Zusätzliche Response mit Headern { #additional-response-with-headers }

Für manche APIs möchten Sie zusätzliche Header in einer Response dokumentieren (z. B. `Location` bei `201 Created`). FastAPI lässt das über das Schlüssel‑Wort `headers` zu.

```python
# docs_src/additional_responses/tutorial004_py310.py
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED, responses={
    201: {
        "description": "Item created",
        "headers": {
            "Location": {
                "description": "URL of the newly created item",
                "schema": {"type": "string", "format": "uri"}
            }
        },
        "model": None,  # kein Body, nur Header
    }
})
async def create_item():
    # FastAPI erzeugt automatisch einen `Location`‑Header, weil wir ihn
    # explizit im `responses`‑Dictionary definiert haben.
    return JSONResponse(status_code=201, content={"id": 123}, headers={"Location": "/items/123"})
```

Im generierten OpenAPI‑Schema wird der Header unter `responses[201].headers.Location` aufgeführt.

---

## Zusammenfassung { #summary }

* **`responses`‑Parameter** – ein Dictionary, dessen Schlüssel HTTP‑Statuscodes und dessen Werte weitere Dictionaries mit Metadaten (`model`, `description`, `content`, `headers`) sind.
* **`model`** – ein Pydantic‑Modell, das FastAPI in ein JSON‑Schema umwandelt und im OpenAPI‑`content`‑Abschnitt ablegt.
* **`description`** – liefert eine kurze, menschenlesbare Erklärung des Statuscodes.
* **`content`** – ermöglicht die Angabe benutzerdefinierter Media‑Types und Beispiele.
* **`headers`** – dokumentiert zusätzliche Header, die mit einer Response zurückgeschickt werden.
* **Direktes Zurückgeben einer Response‑Klasse** – notwendig, damit FastAPI den richtigen Statuscode und das passende Schema erkennt.

Durch die Nutzung dieser Optionen können Sie Ihr OpenAPI‑Schema präziser gestalten und Ihren API‑Nutzern klar kommunizieren, welche möglichen Rückgaben eine Endpoint‑Operation hat.

---

**Weiterführende Ressourcen**

* [FastAPI – Response Model Docs (englisch)](https://fastapi.tiangolo.com/advanced/additional-responses/)
* Offizielle OpenAPI‑Spezifikation: <https://spec.openapis.org/oas/v3.1.0>
