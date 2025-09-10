# OpenAPI Webhooks { #openapi-webhooks }

Es gibt Fälle, in denen Sie Ihren API-**Benutzern** mitteilen möchten, dass Ihre App *deren* App mit einigen Daten aufrufen (einen <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> senden) könnte, normalerweise um über ein bestimmtes **Event** zu **benachrichtigen**.

Das bedeutet, dass anstelle des normalen Prozesses, bei dem Ihre Benutzer Requests an Ihre API senden, **Ihre API** (oder Ihre App) **Requests an deren System** (an deren API, deren App) senden könnte.

Das wird normalerweise als **Web<abbr title="Haken, Einhängepunkt">hook</abbr>** bezeichnet.

## Webhooks-Schritte { #webhooks-steps }

Der Prozess besteht normalerweise darin, dass **Sie in Ihrem Code definieren**, welche Nachricht Sie senden möchten, den **Body des Requests**.

Sie definieren auch auf irgendeine Weise, in welchen **Momenten** Ihre App diese Requests oder Events senden wird.

Und **Ihre Benutzer** definieren auf irgendeine Weise (zum Beispiel irgendwo in einem Web-<abbr title="Benutzeroberfläche für das Visualisieren und Managen von Daten">Dashboard</abbr>) die **URL**, an die Ihre App diese Requests senden soll.

Die gesamte **Logik** zur Registrierung der URLs für Webhooks und der Code zum tatsächlichen Senden dieser Requests liegt bei Ihnen. Sie schreiben es so, wie Sie möchten, in **Ihrem eigenen Code**.

## Webhooks mit **FastAPI** und OpenAPI dokumentieren { #documenting-webhooks-with-fastapi-and-openapi }

Mit **FastAPI**, mithilfe von OpenAPI, können Sie die Namen dieser Webhooks, die Arten von HTTP-Operationen, die Ihre App senden kann (z. B. `POST`, `PUT`, usw.) und die Request**bodys** definieren, die Ihre App senden würde.

Dies kann es Ihren Benutzern viel einfacher machen, **deren APIs zu implementieren**, um Ihre **Webhook**-Requests zu empfangen. Möglicherweise können diese sogar einen Teil ihres eigenen API-Codes automatisch generieren.

/// info | Info

Webhooks sind in OpenAPI 3.1.0 und höher verfügbar und werden von FastAPI `0.99.0` und höher unterstützt.

///

## Eine App mit Webhooks { #an-app-with-webhooks }

Wenn Sie eine **FastAPI**-Anwendung erstellen, gibt es ein `webhooks`-Attribut, das Sie verwenden können, um *Webhooks* zu definieren, genauso wie Sie *Pfadoperationen* definieren würden, zum Beispiel mit `@app.webhooks.post()`.

{* ../../docs_src/openapi_webhooks/tutorial001.py hl[9:13,36:53] *}

Die von Ihnen definierten Webhooks landen im **OpenAPI**-Schema und der automatischen **Dokumentations-Oberfläche**.

/// info | Info

Das `app.webhooks`-Objekt ist eigentlich nur ein `APIRouter`, derselbe Typ, den Sie verwenden würden, wenn Sie Ihre App mit mehreren Dateien strukturieren.

///

Beachten Sie, dass Sie bei Webhooks tatsächlich keinen *Pfad* (wie `/items/`) deklarieren, der Text, den Sie dort übergeben, ist lediglich eine **Kennzeichnung** des Webhooks (der Name des Events). Zum Beispiel ist in `@app.webhooks.post("new-subscription")` der Webhook-Name `new-subscription`.

Das liegt daran, dass erwartet wird, dass **Ihre Benutzer** den tatsächlichen **URL-Pfad**, an dem sie den Webhook-Request empfangen möchten, auf andere Weise definieren (z. B. über ein Web-Dashboard).

### Die Dokumentation testen { #check-the-docs }

Jetzt können Sie Ihre App starten und auf <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> gehen.

Sie werden sehen, dass Ihre Dokumentation die normalen *Pfadoperationen* und jetzt auch einige **Webhooks** enthält:

<img src="/img/tutorial/openapi-webhooks/image01.png">
