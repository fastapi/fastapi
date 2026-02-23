# Zusätzliche Statuscodes { #additional-status-codes }

FastAPI gibt standardmäßig **Responses** als `JSONResponse` zurück. Der zurückgegebene Statuscode ist entweder der implizite Standard (`200 OK` für erfolgreiche GET‑Requests) oder der in der Pfadoperation explizit angegebene Code.

## Mehrere Statuscodes für eine einzige Pfadoperation { #additional-status-codes_1 }

Manchmal soll eine Endpunkt‑Funktion je nach Situation unterschiedliche Statuscodes zurückliefern – zum Beispiel `200 OK` wenn ein vorhandenes Objekt aktualisiert wird, und `201 Created` wenn das Objekt neu angelegt wird. In solchen Fällen können Sie eine **Response** (z. B. `JSONResponse`) selbst erzeugen und den gewünschten `status_code` festlegen.

### Beispiel

```python
# docs_src/additional_status_codes/tutorial001_an_py310.py
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.put("/items/{item_id}")
async def upsert_item(item_id: int):
    """Aktualisiert ein Item, legt es aber an, falls es noch nicht existiert.

    * Wenn das Item bereits existiert → Rückgabe von 200 OK.
    * Wenn das Item neu erstellt wird → Rückgabe von 201 Created.
    """
    # --- Annahme: Prüfen, ob das Item bereits existiert ---
    if item_exists(item_id):
        return {"item_id": item_id, "result": "updated"}
    # --- Item wird neu angelegt, explizit JSONResponse mit Status 201 ---
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"item_id": item_id, "result": "created"},
    )
```

> **Hinweis**: Die Zeilen 4 – 25 des Beispiel‑Codes werden hervorgehoben, weil dort die wichtigsten Import‑ und Rückgabe‑Logiken zu finden sind.

---

## ⚠️ Warnung

Wenn Sie eine **Response** (z. B. `JSONResponse`) direkt zurückgeben, übernimmt FastAPI **keine** automatische Serialisierung über ein Pydantic‑Modell. Stellen Sie sicher, dass:

* Der zurückgegebene Inhalt bereits gültiges JSON ist.
* Alle erforderlichen Felder enthalten sind, weil FastAPI diese nicht mehr ergänzt.

---

## 🛠️ Technische Details

* Sie können `JSONResponse` sowohl aus `starlette.responses` als auch aus `fastapi.responses` importieren – beide Varianten sind äquivalent.
* Die meisten Response‑Klassen (z. B. `PlainTextResponse`, `HTMLResponse`, `StreamingResponse`) stammen aus **Starlette** und werden von FastAPI nur für Komfort re-exportiert.
* Der Hilfs‑Namespace `fastapi.status` enthält die gängigen HTTP‑Status‑Konstanten (z. B. `status.HTTP_201_CREATED`). Diese sind ebenfalls nur ein thin wrapper über `starlette.status`.

---

## OpenAPI‑ und API‑Dokumentation { #openapi-and-api-docs }

FastAPI kann zusätzliche Statuscodes automatisch in das generierte OpenAPI‑Schema aufnehmen, wenn Sie das **`responses`**‑Argument des Routendekorators verwenden. So dokumentieren Sie die möglichen Rückgabecodes für Clients und Tools wie Swagger UI.

```python
@app.put(
    "/items/{item_id}",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Item wurde erstellt",
            "content": {
                "application/json": {
                    "example": {"item_id": 42, "result": "created"}
                }
            },
        },
        status.HTTP_200_OK: {
            "description": "Item wurde aktualisiert",
            "content": {
                "application/json": {
                    "example": {"item_id": 42, "result": "updated"}
                }
            },
        },
    },
)
async def upsert_item(item_id: int):
    ...
```

*Der obige Code ergänzt das OpenAPI‑Schema um die beiden möglichen Rückgabecodes.*

---

## Zusammenfassung

* Verwenden Sie `JSONResponse` (oder andere `Response`‑Klassen), wenn Sie einen **benutzerdefinierten** Statuscode zurückgeben wollen.
* Denken Sie daran, dass direkte Responses nicht über Pydantic‑Modelle serialisiert werden – Sie müssen das JSON selbst korrekt erzeugen.
* Dokumentieren Sie zusätzliche Statuscodes mit dem `responses`‑Parameter, damit OpenAPI‑Clients die komplette API‑Spezifikation erhalten.

---

*Dieses Dokument wurde aus dem aktuellen Stand der FastAPI‑Codebasis generiert und spiegelt die empfohlenen Praktiken für das Arbeiten mit zusätzlichen HTTP‑Statuscodes wider.*
