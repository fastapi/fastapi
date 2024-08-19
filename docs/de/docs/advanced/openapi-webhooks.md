# OpenAPI-Webhooks

Es gibt Fälle, in denen Sie Ihren API-Benutzern mitteilen möchten, dass Ihre Anwendung mit einigen Daten *deren* Anwendung aufrufen (ein Request senden) könnte, normalerweise um über ein bestimmtes **Event** zu **benachrichtigen**.

Das bedeutet, dass anstelle des normalen Prozesses, bei dem Benutzer Requests an Ihre API senden, **Ihre API** (oder Ihre Anwendung) **Requests an deren System** (an deren API, deren Anwendung) senden könnte.

Das wird normalerweise als **Webhook** bezeichnet.

## Webhooks-Schritte

Der Prozess besteht normalerweise darin, dass **Sie in Ihrem Code definieren**, welche Nachricht Sie senden möchten, den **Body des Requests**.

Sie definieren auch auf irgendeine Weise, zu welchen **Momenten** Ihre Anwendung diese Requests oder Events sendet.

Und **Ihre Benutzer** definieren auf irgendeine Weise (zum Beispiel irgendwo in einem Web-Dashboard) die **URL**, an die Ihre Anwendung diese Requests senden soll.

Die gesamte **Logik** zur Registrierung der URLs für Webhooks und der Code zum tatsächlichen Senden dieser Requests liegt bei Ihnen. Sie schreiben es so, wie Sie möchten, in **Ihrem eigenen Code**.

## Webhooks mit **FastAPI** und OpenAPI dokumentieren

Mit **FastAPI** können Sie mithilfe von OpenAPI die Namen dieser Webhooks, die Arten von HTTP-Operationen, die Ihre Anwendung senden kann (z. B. `POST`, `PUT`, usw.) und die Request**bodys** definieren, die Ihre Anwendung senden würde.

Dies kann es Ihren Benutzern viel einfacher machen, **deren APIs zu implementieren**, um Ihre **Webhook**-Requests zu empfangen. Möglicherweise können diese sogar einen Teil des eigenem API-Codes automatisch generieren.

/// info

Webhooks sind in OpenAPI 3.1.0 und höher verfügbar und werden von FastAPI `0.99.0` und höher unterstützt.

///

## Eine Anwendung mit Webhooks

Wenn Sie eine **FastAPI**-Anwendung erstellen, gibt es ein `webhooks`-Attribut, mit dem Sie *Webhooks* definieren können, genauso wie Sie *Pfadoperationen* definieren würden, zum Beispiel mit `@app.webhooks.post()`.

```Python hl_lines="9-13  36-53"
{!../../../docs_src/openapi_webhooks/tutorial001.py!}
```

Die von Ihnen definierten Webhooks landen im **OpenAPI**-Schema und der automatischen **Dokumentations-Oberfläche**.

/// info

Das `app.webhooks`-Objekt ist eigentlich nur ein `APIRouter`, derselbe Typ, den Sie verwenden würden, wenn Sie Ihre Anwendung mit mehreren Dateien strukturieren.

///

Beachten Sie, dass Sie bei Webhooks tatsächlich keinen *Pfad* (wie `/items/`) deklarieren, sondern dass der Text, den Sie dort übergeben, lediglich eine **Kennzeichnung** des Webhooks (der Name des Events) ist. Zum Beispiel ist in `@app.webhooks.post("new-subscription")` der Webhook-Name `new-subscription`.

Das liegt daran, dass erwartet wird, dass **Ihre Benutzer** den tatsächlichen **URL-Pfad**, an dem diese den Webhook-Request empfangen möchten, auf andere Weise definieren (z. B. über ein Web-Dashboard).

### Es in der Dokumentation ansehen

Jetzt können Sie Ihre Anwendung mit Uvicorn starten und auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> gehen.

Sie werden sehen, dass Ihre Dokumentation die normalen *Pfadoperationen* und jetzt auch einige **Webhooks** enthält:

<img src="/img/tutorial/openapi-webhooks/image01.png">
